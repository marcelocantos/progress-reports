"""Exercise the reporting CLIs against known Git histories in this checkout."""

import os
import re
import subprocess
import sys
import unittest
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from zoneinfo import ZoneInfo

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
MELBOURNE = ZoneInfo("Australia/Melbourne")

# Repositories in parent-to-child order. Each row gives the subject, committer
# instant, and (when different) author instant. Dates use the recorded offsets.
APRIL = {
    "boundaries": [
        ("before first day", "2026-04-26T13:59:59+00:00"),
        ("exactly at first midnight", "2026-04-26T14:00:00+00:00"),
        ("one second into Monday", "2026-04-26T14:00:01+00:00"),
        ("last Sunday second", "2026-05-03T13:59:59+00:00"),
        ("exactly at exclusive end", "2026-05-03T14:00:00+00:00"),
    ],
    "skewed-clock": [
        ("in-window ancestor", "2026-04-27T06:00:00+00:00", "2026-04-11T21:00:00+00:00"),
        ("older descendant", "2026-04-25T23:00:00+00:00", "2026-04-28T03:00:00+00:00"),
    ],
    "midnight": [
        ("end of Wednesday", "2026-04-29T13:59:59+00:00"),
        ("start of Thursday", "2026-04-29T14:00:00+00:00"),
    ],
    "thursday-only": [("Thursday midnight only", "2026-04-29T14:00:00+00:00")],
    "outside": [("later committer", "2026-05-04T00:00:00+10:00", "2026-05-03T22:00:00+10:00")],
}

DST = {
    "transition": [
        ("Saturday last second", "2026-04-04T23:59:59+11:00"),
        ("Sunday first second", "2026-04-05T00:00:00+11:00"),
        ("before clocks change", "2026-04-05T02:59:59+11:00"),
        ("after clocks change", "2026-04-05T02:00:00+10:00"),
        ("Sunday last second", "2026-04-05T23:59:59+10:00"),
    ],
    "late-sunday": [("within the 25th hour", "2026-04-05T23:30:00+10:00")],
    "sunday-start": [("first second in UTC", "2026-04-04T13:00:00+00:00")],
    "monday-only": [("after the 25-hour day", "2026-04-06T00:00:00+10:00")],
}

# Melbourne's clocks go forward on Sunday 4 October 2026 (a 23-hour day). The
# Monday commits are an hour or less after midnight; a bound or day bucket that
# keeps Sunday's +10:00 offset would put them on Sunday.
DST_START = {
    "transition": [
        ("Saturday last second", "2026-10-03T23:59:59+10:00"),
        ("Sunday first second", "2026-10-04T00:00:00+10:00"),
        ("before clocks go forward", "2026-10-04T01:59:59+10:00"),
        ("after clocks go forward", "2026-10-04T03:00:00+11:00"),
        ("Sunday last second", "2026-10-04T23:59:59+11:00"),
    ],
    "monday-only": [("first second after the 23-hour day", "2026-10-05T00:00:00+11:00")],
    "half-past-monday": [("Sunday 23:30 at the old offset", "2026-10-05T00:30:00+11:00")],
    "sunday-start": [("first second in UTC", "2026-10-03T14:00:00+00:00")],
}

# Histories with merges, replayed in order. Steps:
#   ("commit", branch, subject, committer instant[, author instant])
#   ("branch", new branch, start point)
#   ("merge", into, from, subject, committer instant)   # always --no-ff
#   ("delete", branch)                                  # merged branch removed
# Merged branches are deleted, as after a pull request, so the slow-clock merge
# is the only path from master to the commits beneath it.
MERGES = {
    "merges": [
        ("commit", "master", "trunk before period", "2026-04-26T12:00:00+00:00"),
        ("branch", "feature", "master"),
        ("commit", "feature", "branch before period", "2026-04-26T13:59:59+00:00", "2026-04-27T01:00:00+00:00"),
        ("commit", "feature", "branch at first midnight", "2026-04-26T14:00:00+00:00"),
        ("merge", "master", "feature", "merge at first midnight", "2026-04-26T14:00:00+00:00"),
        ("delete", "feature"),
        ("branch", "skewed", "master"),
        ("commit", "skewed", "branch under slow merge", "2026-04-28T03:00:00+00:00"),
        ("merge", "master", "skewed", "merge with slow clock", "2026-04-25T23:00:00+00:00"),
        ("delete", "skewed"),
        ("commit", "master", "trunk after slow merge", "2026-04-30T02:00:00+00:00"),
        ("branch", "old", "master"),
        ("commit", "old", "branch from last week", "2026-04-20T02:00:00+00:00"),
        ("merge", "master", "old", "merge alone on Friday", "2026-05-01T02:00:00+00:00"),
        ("delete", "old"),
        ("branch", "late", "master"),
        ("commit", "late", "branch at last second", "2026-05-03T13:59:59+00:00"),
        ("merge", "master", "late", "merge at exclusive end", "2026-05-03T14:00:00+00:00"),
        ("delete", "late"),
        ("branch", "wip", "master"),
        ("commit", "wip", "unmerged in period", "2026-04-29T02:00:00+00:00"),
        ("commit", "wip", "unmerged at exclusive end", "2026-05-03T14:00:00+00:00"),
    ],
}

WEEKS = {
    "weekly-activity": [
        ("leading partial week", "2026-04-21T12:00:00+10:00"),
        ("complete week", "2026-04-27T12:00:00+10:00"),
        ("start of the next week", "2026-05-04T00:00:00+10:00"),
        ("Sunday activity", "2026-05-10T12:00:00+10:00"),
        ("future week", "2026-05-11T12:00:00+10:00"),
    ],
}

# Set only the reporting clock while executing the real CLI and Git scan.
TIMELINE_WITH_FROZEN_CLOCK = """
from datetime import datetime
from importlib.util import module_from_spec, spec_from_file_location
import sys

script, now, *args = sys.argv[1:]
fixed = datetime.fromisoformat(now)

class FixedDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return fixed.astimezone(tz)

sys.argv = [script, *args]
spec = spec_from_file_location('timeline_chart', script)
timeline = module_from_spec(spec)
spec.loader.exec_module(timeline)
timeline.datetime = FixedDatetime
timeline.main()
"""


class FixtureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = TemporaryDirectory(prefix=".reporting-oracle-", dir=ROOT)
        cls.addClassCleanup(temporary.cleanup)
        cls.suite_tmp = Path(temporary.name)

    def setUp(self):
        temporary = TemporaryDirectory(dir=self.suite_tmp)
        self.addCleanup(temporary.cleanup)
        self.tmp = Path(temporary.name)
        self.work = self.tmp / "work"
        self.work.mkdir()
        config = self.tmp / "gitconfig"
        config.write_text("[user]\n\tname = Fixture author\n")
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.env.update(
            GIT_CONFIG_GLOBAL=str(config),
            GIT_CONFIG_NOSYSTEM="1",
            GIT_AUTHOR_NAME="Fixture author",
            GIT_AUTHOR_EMAIL="author@example.test",
            GIT_COMMITTER_NAME="Fixture committer",
            GIT_COMMITTER_EMAIL="committer@example.test",
            GIT_TEST_DATE_NOW="1777881600",  # 2026-05-04 08:00 UTC
            LC_ALL="C",
            TZ="UTC",
            TMPDIR=str(self.tmp),
            XDG_CACHE_HOME=str(self.tmp / "cache"),
            MPLCONFIGDIR=str(self.suite_tmp / "matplotlib"),
            PROGRESS_WORK_ROOT=str(self.work),
            PROGRESS_LINE_EXCLUDES=str(self.tmp / "no-excludes.yaml"),
        )

    def command(self, *args, **env):
        result = subprocess.run(
            args, cwd=self.tmp, env=self.env | env, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, f"{args}\n{result.stdout}{result.stderr}")
        return result.stdout

    def make_repos(self, fixtures):
        for name, commits in fixtures.items():
            repo = self.work / "fixture" / name
            self.command("git", "init", "--quiet", "--template=", "-b", "master", str(repo))
            for subject, committed, *author in commits:
                with (repo / "activity.txt").open("a") as activity:
                    activity.write(f"{subject}\n")
                self.command("git", "-C", str(repo), "add", "activity.txt")
                self.command(
                    "git", "-C", str(repo), "commit", "--quiet", "-m", subject,
                    GIT_COMMITTER_DATE=committed,
                    GIT_AUTHOR_DATE=author[0] if author else committed,
                )

    def make_histories(self, fixtures):
        for name, steps in fixtures.items():
            repo = self.work / "fixture" / name
            git = ("git", "-C", str(repo))
            self.command("git", "init", "--quiet", "--template=", "-b", "master", str(repo))

            def switch(branch):
                # The initial master is unborn until its first commit.
                if self.command(*git, "symbolic-ref", "--short", "HEAD").strip() != branch:
                    self.command(*git, "checkout", "--quiet", branch)

            for kind, *step in steps:
                if kind == "commit":
                    branch, subject, committed, *author = step
                    switch(branch)
                    with (repo / f"{branch}.txt").open("a") as activity:
                        activity.write(f"{subject}\n")
                    self.command(*git, "add", f"{branch}.txt")
                    self.command(
                        *git, "commit", "--quiet", "-m", subject,
                        GIT_COMMITTER_DATE=committed,
                        GIT_AUTHOR_DATE=author[0] if author else committed,
                    )
                elif kind == "branch":
                    self.command(*git, "branch", *step)
                elif kind == "merge":
                    into, source, subject, committed = step
                    switch(into)
                    self.command(
                        *git, "merge", "--quiet", "--no-ff", "-m", subject, source,
                        GIT_COMMITTER_DATE=committed, GIT_AUTHOR_DATE=committed,
                    )
                elif kind == "delete":
                    self.command(*git, "branch", "--quiet", "-D", *step)
                else:
                    raise ValueError(kind)
            switch("master")

    def timeline(self, start, end, *, now=None, **paths):
        output = self.tmp / "timeline.svg"
        args = ["--since", str(start), "--work-root", str(self.work), "-o", str(output)]
        if end is not None:
            args.extend(("--until", str(end)))
        for flag, path in paths.items():
            args.extend((f"--{flag.replace('_', '-')}", str(path)))
        python = [sys.executable, "-B"]
        timeline = SCRIPTS / "timeline-chart.py"
        if now is None:
            self.command(*python, str(timeline), *args)
        else:
            self.command(*python, "-c", TIMELINE_WITH_FROZEN_CLOCK, str(timeline), now, *args)
        self.assertIn("<svg", output.read_text())


class T1(FixtureTest):
    def expected(self, fixtures, start, end):
        daily = Counter({start + timedelta(days=offset): 0 for offset in range((end - start).days)})
        subjects = []
        for commits in fixtures.values():
            active_days = set()
            for subject, committed, *_ in commits:
                day = datetime.fromisoformat(committed).astimezone(MELBOURNE).date()
                if start <= day < end:
                    active_days.add(day)
                    subjects.append(subject)
            daily.update(active_days)
        return sorted(subjects), dict(daily)

    def expected_histories(self, fixtures, start, end):
        """Replay the steps as sets of subjects per branch.

        Membership is the committer instant's Melbourne date in [start, end).
        gather.sh counts non-merge commits reachable from master as landed and
        other non-merge commits as in flight. timeline-chart.py counts any
        commit, merges included, reachable from any ref.
        """
        landed, in_flight = [], []
        gather_daily = Counter({start + timedelta(days=offset): 0 for offset in range((end - start).days)})
        timeline_daily = Counter(dict.fromkeys(gather_daily, 0))
        for steps in fixtures.values():
            refs = {"master": set()}
            commits = {}
            for kind, *step in steps:
                if kind == "commit":
                    branch, subject, committed, *_ = step
                    commits[subject] = (committed, False)
                    refs[branch].add(subject)
                elif kind == "branch":
                    refs[step[0]] = set(refs[step[1]])
                elif kind == "merge":
                    into, source, subject, committed = step
                    commits[subject] = (committed, True)
                    refs[into] |= refs[source] | {subject}
                elif kind == "delete":
                    del refs[step[0]]

            def in_period(subject):
                day = datetime.fromisoformat(commits[subject][0]).astimezone(MELBOURNE).date()
                return day if start <= day < end else None

            reachable = set().union(*refs.values())
            gather_days, timeline_days = set(), set()
            for subject in reachable:
                day = in_period(subject)
                if day is None:
                    continue
                timeline_days.add(day)
                if commits[subject][1]:
                    continue
                if subject in refs["master"]:
                    landed.append(subject)
                    gather_days.add(day)
                else:
                    in_flight.append(subject)
            gather_daily.update(gather_days)
            timeline_daily.update(timeline_days)
        return sorted(landed), sorted(in_flight), dict(gather_daily), dict(timeline_daily)

    def run_gather(self, start, end, subjects, daily, in_flight=0):
        output = self.command("/bin/bash", str(SCRIPTS / "gather.sh"), str(start), str(end))
        total = re.search(r"^Total landed commits: (\d+)$", output, re.MULTILINE)
        observed = sorted(re.findall(r"^[0-9a-f]+ (.+)$", output, re.MULTILINE))
        self.assertEqual((int(total[1]) if total else 0, observed), (len(subjects), subjects))
        self.assertIn(f"Total landed lines (excl. progress-report paths): +{len(subjects)}/-0", output)
        self.assertIn(f"Total in-flight commits: {in_flight}\n", output)
        observed_days = {
            date.fromisoformat(day): int(count)
            for day, count in re.findall(r"^[A-Z][a-z]{2} (\d{4}-\d\d-\d\d) (\d+)$", output, re.MULTILINE)
        }
        self.assertEqual(observed_days, daily)

    def check_gather(self, fixtures, start, end):
        subjects, daily = self.expected(fixtures, start, end)
        self.run_gather(start, end, subjects, daily)

    def check_timeline(self, fixtures, start, end):
        _, daily = self.expected(fixtures, start, end)
        self.run_timeline(start, end, daily)

    def run_timeline(self, start, end, daily):
        cache = self.tmp / "daily.yaml"
        self.timeline(start, end - timedelta(days=1), cache=cache)
        observed = {
            date.fromisoformat(str(day)): count
            for day, count in yaml.safe_load(cache.read_text())["dates"].items()
        }
        self.assertEqual(observed, daily)

    def test_gather_historical_week(self):
        self.make_repos(APRIL)
        self.check_gather(APRIL, date(2026, 4, 27), date(2026, 5, 4))

    def test_gather_daylight_saving(self):
        self.make_repos(DST)
        self.check_gather(DST, date(2026, 4, 5), date(2026, 4, 6))

    def test_timeline_historical_week(self):
        self.make_repos(APRIL)
        self.check_timeline(APRIL, date(2026, 4, 27), date(2026, 5, 4))

    def test_timeline_daylight_saving(self):
        self.make_repos(DST)
        self.check_timeline(DST, date(2026, 4, 5), date(2026, 4, 6))

    def test_gather_daylight_saving_start(self):
        self.make_repos(DST_START)
        self.check_gather(DST_START, date(2026, 10, 4), date(2026, 10, 5))

    def test_timeline_daylight_saving_start(self):
        self.make_repos(DST_START)
        self.check_timeline(DST_START, date(2026, 10, 4), date(2026, 10, 5))

    def test_gather_merges(self):
        self.make_histories(MERGES)
        start, end = date(2026, 4, 27), date(2026, 5, 4)
        landed, in_flight, daily, _ = self.expected_histories(MERGES, start, end)
        self.assertEqual(len(landed), 4)  # guards the model against an empty fixture
        self.run_gather(start, end, landed, daily, len(in_flight))

    def test_timeline_merges(self):
        self.make_histories(MERGES)
        start, end = date(2026, 4, 27), date(2026, 5, 4)
        *_, daily = self.expected_histories(MERGES, start, end)
        self.assertEqual(sum(daily.values()), 6)  # guards the model against an empty fixture
        self.run_timeline(start, end, daily)


class T2(FixtureTest):
    def setUp(self):
        super().setUp()
        self.make_repos(WEEKS)
        self.weekly = self.tmp / "weekly"
        self.weekly.mkdir()

    def check_weekly(self, start, end, now):
        self.timeline(start, end, now=now, weekly_dir=self.weekly)
        self.assertEqual(
            {path.name for path in self.weekly.iterdir()},
            {"daily-activity-2026-05-03.svg"},
        )
        self.assertIn("<svg", (self.weekly / "daily-activity-2026-05-03.svg").read_text())

    def test_historical_sunday_cutoff_and_rerun(self):
        # It is already Monday in Melbourne, though still Sunday on the host.
        for _ in range(2):
            self.check_weekly("2026-04-27", "2026-05-03", "2026-05-03T14:00:00+00:00")

    def test_partial_weeks_at_window_edges(self):
        self.check_weekly("2026-04-21", "2026-05-06", "2026-05-18T00:00:00+10:00")

    def test_in_progress_sunday_and_future_week(self):
        self.check_weekly("2026-04-27", "2026-05-17", "2026-05-10T23:59:59+10:00")

    def test_default_cutoff_on_monday(self):
        self.check_weekly("2026-04-27", None, "2026-05-03T14:00:00+00:00")


if __name__ == "__main__":
    unittest.main(verbosity=2)

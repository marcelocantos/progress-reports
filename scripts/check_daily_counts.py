#!/usr/bin/env python3
"""Assert the three daily-activity oracles agree.

A weekly report states its per-day active-repository counts in three places:

  1. `data/daily-repos.yaml` — the ledger the chart renderer reads.
  2. `reports/daily-activity-<date>.svg` — the rendered bar chart, whose
     matplotlib bar labels appear as XML comments after the "Active repos"
     axis label.
  3. `reports/weekly-report-<date>.md` — the prose caption under the chart.

They have drifted before (2026-08-16 shipped caption 3/1/0/0/0/4/6 against a
ledger of 4/3/0/0/0/4/12). This check fails whenever any of the three disagree
for any report that carries a caption.

Run: python3 scripts/check_daily_counts.py
"""

from __future__ import annotations

import datetime as dt
import itertools
import pathlib
import re
import sys

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_FILE = REPO_ROOT / "data" / "daily-repos.yaml"
REPORTS_DIR = REPO_ROOT / "reports"

DAYS_PER_WEEK = 7
# Caption form: "Mon 08-10 3, Tue 08-11 1, ... Sun 08-16 6."
CAPTION_RE = re.compile(r"\*\(Active repositories per day: (.+?)[.)]", re.DOTALL)
CAPTION_DAY_RE = re.compile(r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\d{2})-(\d{2}) (\d+)")
REPORT_NAME_RE = re.compile(r"weekly-report-(\d{4}-\d{2}-\d{2})\.md$")
# Bar-value labels follow the y-axis title comment in matplotlib's SVG output.
SVG_COMMENT_RE = re.compile(r"<!-- (.*?) -->")
SVG_AXIS_TITLE = "Active repos"


def week_dates(end: dt.date) -> list[dt.date]:
    return [end - dt.timedelta(days=n) for n in range(DAYS_PER_WEEK - 1, -1, -1)]


def caption_counts(report: pathlib.Path, dates: list[dt.date]) -> list[int] | None:
    """Per-day counts written in the report's prose caption, or None if absent."""
    match = CAPTION_RE.search(report.read_text())
    if match is None:
        return None
    days = CAPTION_DAY_RE.findall(match.group(1))
    if len(days) != DAYS_PER_WEEK:
        raise ValueError(f"{report.name}: caption lists {len(days)} days, want {DAYS_PER_WEEK}")
    for (month, day, _), date in zip(days, dates):
        if (int(month), int(day)) != (date.month, date.day):
            raise ValueError(f"{report.name}: caption date {month}-{day} is not {date}")
    return [int(count) for _, _, count in days]


def svg_counts(svg: pathlib.Path, ledger: list[int]) -> list[int] | None:
    """Bar labels from the rendered chart, re-expanded to a full week.

    matplotlib omits a label for a zero-height bar, so the labels are the
    non-zero counts in day order; we place them back against the ledger's own
    zero/non-zero shape and let the comparison catch any mismatch.
    """
    if not svg.exists():
        return None
    comments = SVG_COMMENT_RE.findall(svg.read_text())
    if SVG_AXIS_TITLE not in comments:
        raise ValueError(f"{svg.name}: no '{SVG_AXIS_TITLE}' axis label comment")
    tail = comments[comments.index(SVG_AXIS_TITLE) + 1 :]
    # The bar labels run until the figure title comment, which is not a number.
    bars = [int(label) for label in itertools.takewhile(str.isdigit, tail)]
    expanded: list[int] = []
    for value in ledger:
        if value == 0:
            expanded.append(0)
        elif bars:
            expanded.append(bars.pop(0))
        else:
            expanded.append(-1)  # ran out of labels; guaranteed mismatch
    return expanded + [int(label) for label in bars]


def main() -> int:
    ledger_all = yaml.safe_load(DATA_FILE.read_text())["dates"]
    failures: list[str] = []
    checked = 0

    for report in sorted(REPORTS_DIR.glob("weekly-report-*.md")):
        name_match = REPORT_NAME_RE.search(report.name)
        if name_match is None:
            continue
        end = dt.date.fromisoformat(name_match.group(1))
        dates = week_dates(end)
        caption = caption_counts(report, dates)
        if caption is None:
            continue
        checked += 1

        missing = [str(date) for date in dates if str(date) not in ledger_all]
        if missing:
            failures.append(f"{report.name}: {DATA_FILE.name} has no entry for {', '.join(missing)}")
            continue
        ledger = [ledger_all[str(date)] for date in dates]

        if caption != ledger:
            failures.append(
                f"{report.name}: caption {caption} != {DATA_FILE.name} {ledger}"
            )
        svg = REPORTS_DIR / f"daily-activity-{end}.svg"
        bars = svg_counts(svg, ledger)
        if bars is None:
            failures.append(f"{report.name}: chart {svg.name} is missing")
        elif bars != ledger:
            failures.append(f"{svg.name}: bar labels {bars} != {DATA_FILE.name} {ledger}")

    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(f"\n{len(failures)} inconsistency(ies) across {checked} captioned report(s)", file=sys.stderr)
        return 1
    print(f"OK: {checked} captioned report(s) agree with {DATA_FILE.name} and their charts")
    return 0


if __name__ == "__main__":
    sys.exit(main())

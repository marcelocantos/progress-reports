#!/usr/bin/env python3
"""Fail when this tree's ledger claims producer scripts it does not contain.

T1/T2 in bullseye.yaml name gather.sh and timeline-chart.py. Those files
live in the /progress-report skill (~/.claude/skills/progress-report/),
not in this repo. While they stay status: identified, they are
structurally unclosable here.

Also fail if docs/guide.md still publishes the bare-date
`git log --after=... --before=... --all` recipe — git treats a bare
YYYY-MM-DD as an incomplete timestamp and can drop the boundary day
(the 2026-04-27 undercount that created T1).

Run: python3 scripts/check_producer_boundary.py
"""

from __future__ import annotations

import pathlib
import re
import sys

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BULLSEYE = REPO_ROOT / "bullseye.yaml"
GUIDE = REPO_ROOT / "docs" / "guide.md"
PRODUCER_NAMES = ("gather.sh", "timeline-chart.py")
# The defect: a recipe that passes bare date placeholders and --all.
BARE_RECIPE_RE = re.compile(
    r'--after="<start>"\s+--before="<end\+1day>"\s+--all',
    re.DOTALL,
)
TIMESTAMP_HINT_RE = re.compile(r"T00:00:00|00:00:00|to_local_midnight")
SKILL_HINT_RE = re.compile(r"progress-report/gather\.sh|skills/progress-report")


def tracked_producers() -> list[str]:
    return [
        path.name
        for path in REPO_ROOT.rglob("*")
        if path.name in PRODUCER_NAMES and ".git" not in path.parts
    ]


def main() -> int:
    failures: list[str] = []
    present = tracked_producers()
    ledger = yaml.safe_load(BULLSEYE.read_text())
    targets = ledger.get("targets") or {}

    for target_id in ("T1", "T2"):
        target = targets.get(target_id) or {}
        status = target.get("status")
        if status == "identified" and not present:
            failures.append(
                f"{target_id} is identified but {', '.join(PRODUCER_NAMES)} "
                "are absent from this tree — the target is unclosable here"
            )

    guide = GUIDE.read_text()
    if BARE_RECIPE_RE.search(guide):
        failures.append(
            "docs/guide.md still publishes the bare-date "
            "`--after=\"<start>\" --before=\"<end+1day>\" --all` recipe"
        )
    if not TIMESTAMP_HINT_RE.search(guide):
        failures.append(
            "docs/guide.md does not document explicit timestamped git bounds"
        )
    if not SKILL_HINT_RE.search(guide):
        failures.append(
            "docs/guide.md does not point gather/timeline production at "
            "the /progress-report skill"
        )

    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(f"\n{len(failures)} producer-boundary failure(s)", file=sys.stderr)
        return 1
    print(
        "OK: ledger does not claim missing producers; "
        "guide documents skill + timestamped bounds"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

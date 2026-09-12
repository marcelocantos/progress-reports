#!/usr/bin/env python3
"""Render per-week daily-activity SVGs from data/daily-repos.yaml.

The ledger is the authority; captions and charts are derivations. This
rewrites `reports/daily-activity-<Sunday>.svg` for every complete Mon–Sun
week present in the cache — it does not scan git and does not rewrite
the cache.

Run: python3 scripts/render_weekly_charts.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_FILE = REPO_ROOT / "data" / "daily-repos.yaml"
REPORTS_DIR = REPO_ROOT / "reports"
DAYS_PER_WEEK = 7


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "sundays",
        nargs="*",
        help="Optional Sunday end-dates (YYYY-MM-DD). Default: every complete week in the ledger.",
    )
    args = parser.parse_args()
    only = {dt.date.fromisoformat(value) for value in args.sundays}

    ledger = yaml.safe_load(DATA_FILE.read_text())["dates"]
    dates = sorted(dt.date.fromisoformat(str(key)) for key in ledger)
    if not dates:
        print("no dates in ledger", file=sys.stderr)
        return 1

    mondays = [day for day in dates if day.weekday() == 0]
    written = 0
    for monday in mondays:
        sunday = monday + dt.timedelta(days=DAYS_PER_WEEK - 1)
        week = [monday + dt.timedelta(days=offset) for offset in range(DAYS_PER_WEEK)]
        if only and sunday not in only:
            continue
        if any(str(day) not in ledger for day in week):
            continue
        counts = [int(ledger[str(day)]) for day in week]
        _write_week(REPORTS_DIR / f"daily-activity-{sunday.isoformat()}.svg", week, counts)
        written += 1
    print(f"OK: wrote {written} weekly chart(s) from {DATA_FILE.name}")
    return 0


def _write_week(path: pathlib.Path, week: list[dt.date], counts: list[int]) -> None:
    labels = [f"{day.strftime('%a')} {day.day}" for day in week]
    fig, ax = plt.subplots(figsize=(7, 3))
    bars = ax.bar(range(len(counts)), counts, color="#2563eb", width=0.6)
    for bar, count in zip(bars, counts):
        if count > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.15,
                str(count),
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
            )
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Active repos", fontsize=9)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_ylim(0, max(counts) * 1.25 if counts else 1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Daily Active Repositories", fontsize=11, fontweight="bold", pad=10)
    fig.tight_layout()
    fig.savefig(path, format="svg", transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())

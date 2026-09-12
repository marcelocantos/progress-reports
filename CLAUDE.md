# Progress Reports

Weekly progress reports for Marcelo Cantos's AI-assisted development work.

**Commercial dual-home:** HMS, minicades, and non-`ge` Squz **detail** lives in
the private sibling [`progress-reports-private`](https://github.com/marcelocantos/progress-reports-private).
This public repo keeps names, rolled-up metrics, stubs with private links, and
full narrative for non-commercial work including open-source `squz/ge`. See
[docs/guide.md](docs/guide.md) (Dual-home series).

## Generating Reports

Follow [docs/guide.md](docs/guide.md) for detailed instructions on data gathering, structure, and formatting.

The repos to scan live under `~/work/github.com/` in these organisations:
`squz`, `marcelocantos`, `arr-ai`, `anz-bank`, plus client orgs as needed
(`Health-Management-Systems`, `minicadesmobile`).

## Conventions

- British English spelling (colour, behaviour, minimise, etc.).
- No emojis.
- Tone: confident, technically precise, dense. No filler.
- Report filenames: `reports/weekly-report-<YYYY-MM-DD>.md` (date = last day of period).
- After writing a report, update `README.md` (newest first) and commit both together.

## Gates

profile: base
override:
  - pr-workflow: skip
  - tests-exist: skip
  - ci-green: skip

This repo has no CI and contains only narrative reports + supporting
data/docs. Push directly to `master` — no PR ceremony, no feature
branch, no review gate. `/push` will commit and push to `master` in
place.

## Consistency gate

`data/daily-repos.yaml` is the single source of truth for daily activity
counts; the chart and the report caption are derivations of it. After
generating or editing a weekly report, run:

    python3 scripts/check_daily_counts.py

It fails when a report's caption, its `daily-activity-<date>.svg` bar
labels, and the ledger disagree. Never hand-write the caption day-tuple.

`gather.sh` and `timeline-chart.py` live in the `/progress-report` skill
(`~/.claude/skills/progress-report/`), not in this repo. After editing
`docs/guide.md` or `bullseye.yaml` targets that name those producers,
run:

    python3 scripts/check_producer_boundary.py

It fails if T1/T2 are still `identified` while the scripts are absent,
or if the guide republishes the bare-date `--after/--before --all` recipe.

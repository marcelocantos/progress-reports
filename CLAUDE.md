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

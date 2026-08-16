# [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports)

The weekly progress report series itself: one report per Monday-to-Sunday period covering every repository that landed work, with a documented metrics methodology, a ranked achievements list, per-week activity charts, and these per-repo pages.

## The journey

The series began as reporting and quickly acquired an apparatus. By late February the repo carried both the weekly reports and a [Marp](https://marp.app/) slide deck on agentic AI development, with an outline document, HTML export and diagram images — 18 commits and +4,806 lines in one week. Early maintenance was structural: a **"Journey So Far"** narrative added to the README contextualising what was then a 25-day, 746-commit, 1.9–3.3-year-equivalent body of work, and a period realignment putting every report on Mon–Sun boundaries with a backfill for the 20 January–4 February gap.

Through April the *method* was extracted from the reports and written down. Achievements were linked back to the week that produced them, a scoring rubric for executive-summary item selection was added to `docs/guide.md`, and the metrics methodology was split out into its own `docs/methodology.md` — the four scoring axes (impact, platform depth, correctness surface, scope of change), the two traditional-development baselines (a single talented generalist with itemised ramp-up, and an idealised specialist team with coordination overhead), the Diversity Tax, and the standing rule that every figure is a range because estimation uncertainty is reported rather than hidden. The "Journey So Far" was rewritten twice more as the body of work outgrew its own summary.

May was spent on presentation under a hostile renderer. The README's per-week metrics table folded five columns into a single packed cell to reclaim space for Highlights, added a lines-of-code roll-up, and then went through several iterations of wrap suppression — `&nbsp;` in stats cells, U+2060 word joiners after images and emoji, and a switch to letter glyphs (ℂ for commits, ☲ for kloc, bold **AI**/**H** for actual hours and single-generalist months) — because GitHub's renderer would otherwise line-break the cells apart.

The series' most consequential changes are its **honesty ratchets**, each of which made the reported numbers smaller. The first, in late May, split landed from in-flight: unmerged branch work moved into a dedicated "In-Flight / Work-in-Progress" section reported as a forward signal and deliberately excluded from shipped metrics, ending the cross-report double-counting that had inflated totals by counting dev commits now and the eventual squash-merge again later. The immediate vindication was rustuml: ~203 in-flight commits reported that week as a forward signal, then counted once when they merged the following week as v0.7.0. The second ratchet was self-restraint on length — the Journey section recast as an overview rather than an enumeration, given a **sub-linear length budget**, with report-entry length caps applied retroactively to re-compress seven bloated weeks.

The third and largest ratchet landed in the final week of July. After publishing the 2026-07-13…19 report, its line statistics were corrected and the **entire series was restamped** to exclude `vendor/` and `node_modules/` from the ☲ kloc figure, stripping roughly +3.0M vendor adds across 26 weeks (series net ≈ +3.0M excluding vendor against ≈ +5.6M raw) while leaving commits and effort ranges untouched. The mechanism was made general rather than one-off: `data/line-excludes.yaml` is a single fleet-wide exclude configuration with a documented schema, so per-repo rules for generated mirrors, amalgamations, goldens and lockfiles live here and never scatter into the project repos. The cost is declared in the reports rather than smoothed over — the 07-26 report notes that its six new entries make ☲ stricter than in prior weeks, that the total excluded bulk was +2,877/−1,211, and that because earlier reports were not restamped for those paths, week-on-week comparison now understates the current week.

Alongside the reports the repo carries the durable artefacts they feed: a per-week daily-activity chart and a series timeline, the ranked top-50 [achievements list](../achievements.md) scored by "meatiness" and linked to the week that earned each entry, and this directory of per-repo pages, each distilling one project's arc across the whole series.

## Highlights

- **Series plus a Marp talk on agentic AI development** — reports and an 18-commit slide deck with outline, HTML export and architecture diagrams. ([2026-02-22](../../reports/weekly-report-2026-02-22.md))
- **"The Journey So Far"** — a README narrative contextualising the then-25-day, 746-commit, 1.9–3.3-year-equivalent body of work. ([2026-03-08](../../reports/weekly-report-2026-03-08.md))
- **Mon–Sun realignment and gap backfill** — every report aligned to week boundaries, with the 20 January–4 February gap filled in. ([2026-03-15](../../reports/weekly-report-2026-03-15.md))
- **A scoring rubric for what makes the summary** — executive-summary item selection written down in `docs/guide.md`, and achievements linked to their week. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **Methodology split into its own document** — the scoring axes, the two traditional baselines, the Diversity Tax and the ranges-not-point-estimates rule moved into `docs/methodology.md`. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))
- **Metrics table compaction** — five columns folded into one packed cell with a kloc roll-up, then glyph and word-joiner iterations to stop GitHub's renderer breaking the cells apart. ([2026-05-17](../../reports/weekly-report-2026-05-17.md))
- **Landed-versus-in-flight split** — unmerged branch work reported separately and excluded from shipped totals, ending the double-counting of dev commits and their later squash-merge. ([2026-05-24](../../reports/weekly-report-2026-05-24.md))
- **Length budgets applied to its own output** — the Journey recast as an overview under a sub-linear budget, with entry caps re-compressing seven bloated weeks. ([2026-06-21](../../reports/weekly-report-2026-06-21.md))
- **Full-series vendor restamp** — every report and the README metrics table remeasured excluding `vendor/` and `node_modules/`, stripping ~+3.0M vendor adds across 26 weeks without touching commits or effort ranges. ([2026-07-26](../../reports/weekly-report-2026-07-26.md))
- **`data/line-excludes.yaml` as the fleet's single exclude file** — a documented schema for per-repo exclusions held centrally, so project repos stay clean and the honesty note declares exactly what each run removed. ([2026-07-26](../../reports/weekly-report-2026-07-26.md))
- **Split into a public series and a private commercial companion** — the classifier, residual rules and dual-write procedure written into the guide, with the public repository's history rewritten and its own line stats excluded from ☲ as a result. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))

## Standouts

- **A ratchet that made its own numbers smaller** — moving unmerged work into a separate in-flight section ended the double-counting of dev commits and their later squash-merge; rustuml's ~203 in-flight commits were reported that week as a forward signal and counted once when they landed. ([2026-05-24](../../reports/weekly-report-2026-05-24.md))
- **Restamping twenty-six weeks of published history** — the whole series was remeasured to exclude `vendor/` and `node_modules/`, stripping roughly +3.0M vendor adds from the kloc figure while leaving commits and effort ranges untouched. ([2026-07-26](../../reports/weekly-report-2026-07-26.md))
- **The exclude rules live in the reporting repo, not the projects** — `data/line-excludes.yaml` is one fleet-wide configuration with a documented schema, so per-repo rules for generated mirrors, amalgamations and lockfiles never scatter across the fleet. ([2026-07-26](../../reports/weekly-report-2026-07-26.md))
- **Length budgets turned on its own output** — the Journey section was recast as an overview under a sub-linear budget, and entry caps were applied retroactively to re-compress seven bloated weeks. ([2026-06-21](../../reports/weekly-report-2026-06-21.md))
- **Fighting GitHub's renderer with word joiners and glyphs** — `&nbsp;` in stats cells, U+2060 after images and emoji, and letter glyphs (ℂ for commits, ☲ for kloc) were all needed to stop the packed metrics cell line-breaking apart. ([2026-05-17](../../reports/weekly-report-2026-05-17.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 13 |
| Commits | ~62 |
| Human attention | not broken out in report tables |
| Traditional equivalent | not broken out in report tables |
| Multiplier | ~25–95× |

## Weekly reports

[02-22](../../reports/weekly-report-2026-02-22.md), [03-08](../../reports/weekly-report-2026-03-08.md), [03-15](../../reports/weekly-report-2026-03-15.md), [04-19](../../reports/weekly-report-2026-04-19.md), [04-26](../../reports/weekly-report-2026-04-26.md), [05-03](../../reports/weekly-report-2026-05-03.md), [05-10](../../reports/weekly-report-2026-05-10.md), [05-17](../../reports/weekly-report-2026-05-17.md), [05-24](../../reports/weekly-report-2026-05-24.md), [06-21](../../reports/weekly-report-2026-06-21.md), [07-19](../../reports/weekly-report-2026-07-19.md), [07-26](../../reports/weekly-report-2026-07-26.md), [08-03](../../reports/weekly-report-2026-08-09.md)

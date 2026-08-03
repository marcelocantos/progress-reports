# [marcelocantos/skills](https://github.com/marcelocantos/skills)

skills is the published mirror of the shared agent skill tree — the workflow definitions (`/release`, `/cv`, `/push`, `/waw`, `/docs`, `/open-source`, `progress-report` and the rest) that drive the fleet's day-to-day operations. The canonical copy lives in `~/.claude/skills/`; this repository is where every change to it lands.

## The journey

The repository was created in February 2026 with six skills and a build file that did the publishing: `/docs` (an end-to-end documentation sherpa with a document-type taxonomy and agent-guide generation), `/open-source` (audit, fix, document, publish, release — delegating documentation to `/docs`), `/release` (version, release notes, CI, Homebrew tap, GitHub release), `/republish-skills`, `/progress-report`, and `/where` for concise session status. The build file handled syncing from `~/.claude/skills/`, README generation, diffing, committing and pushing — so the repository was a mirror by construction rather than a place work happened.

Through March the skills tracked the emergence of the convergence workflow. Thirty-one publishes in a single week carried convergence-system improvements, a new `/wrap` skill, context-compression handling and **parallel fan-out support in `/cv`**; the following weeks brought further `/cv` refinements and a `CLAUDE.md` restructuring. By late April the catalogue had settled into the shape it still has — `/open-source`, `/release`, `/cv`, `/waw`, `/push`, `progress-report` — and had begun spinning off products: [ytt](ytt.md), the YouTube transcript CLI, exists because `/open-source` was applied to a previously-internal tool and carried it to three public releases.

The publishing loop then formalised: every change under `~/.claude/skills/*` triggers `/republish-skills`, which mirrors into this repository as an `Update skills from ~/.claude/skills` commit. The weekly reports consistently footnote the resulting line deltas as **auto-sync rather than authorship** — six syncs worth +1,143/−329 in one week, twelve worth +1,069/−193 in another — and exclude them from the hand-authored totals. Several weeks are net negative (−713, −290, −117), and the reason is the most interesting thing about the repository: capability kept migrating out of the skills and into binaries. [bullseye](bullseye.md) v0.25.0 moved ledger auto-commit inside the MCP server and explicitly *replaced the `/cv` skill workaround*; [claudia](claudia.md)'s public session probes let `/waw` and `/cv` stop re-implementing a session-discovery walk. A skill that shrinks because a tool absorbed its logic is the healthy outcome.

The tree also owns this series. The `progress-report` skill generates the weekly reports, and a single commit in June rewrote its `gather.sh` to separate landed from in-flight commits and handle exact week boundaries — **the methodology every subsequent report runs on**, and the reason the reports distinguish shipped totals from unmerged work. Routine maintenance since has been just that: the `mk` → `cv` migration and stale-doc removal, and a steady tail of syncs as the workflows behind `/release`, `/cv` and `/push` continue to be tuned against real use.

## Highlights

- **Six skills and a self-publishing build** — the repository opens with `/docs`, `/open-source`, `/release`, `/republish-skills`, `/progress-report` and `/where`, and a build file that syncs, diffs, commits and pushes. ([2026-02-22](../../reports/weekly-report-2026-02-22.md))
- **Convergence workflow matures** — thirty-one publishes carrying convergence-system improvements, the `/wrap` skill, context-compression handling and parallel fan-out in `/cv`. ([2026-03-08](../../reports/weekly-report-2026-03-08.md))
- **`/open-source` produces a product** — the skill applied to an internal tool yields [ytt](ytt.md), taken to its first public releases in the same week the catalogue settles on `/cv`, `/waw`, `/push` and `/ytt`. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))
- **The publish loop, stated plainly** — every change to `~/.claude/skills/*` triggers `/republish-skills`, which mirrors here; the improvement loop and its record become the same thing. ([2026-05-10](../../reports/weekly-report-2026-05-10.md))
- **`gather.sh` sets the reporting methodology** — landed-versus-in-flight commit counting and exact week-boundary handling, which this whole series has run on since. ([2026-06-07](../../reports/weekly-report-2026-06-07.md))
- **`mk` → `cv` migration and stale-doc removal** — the skill tree follows the build-tool rename along with the rest of the fleet. ([2026-06-14](../../reports/weekly-report-2026-06-14.md))
- **Auto-sync footnoted out of authorship** — +1,143/−329 across six syncs is recorded as a non-development delta, keeping the fleet's hand-authored figures honest. ([2026-06-21](../../reports/weekly-report-2026-06-21.md))

## Standouts

- **A repository that is a mirror by construction** — the opening commit set ships six skills *and* the build file that syncs them from `~/.claude/skills/`, regenerates the README, diffs, commits and pushes. There is no place in this repository where work happens; every change arrives from the canonical tree. ([2026-02-22](../../reports/weekly-report-2026-02-22.md))
- **Skills shrinking as binaries absorb them** — bullseye v0.25.0 moved ledger auto-commit inside the MCP server and explicitly replaced the `/cv` skill's workaround, and claudia's public session probes let `/waw` and `/cv` stop re-implementing a session-discovery walk. Several weeks are net negative (−713, −290, −117) for exactly this reason, which is the healthy outcome rather than decay. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **`gather.sh` sets the methodology this series runs on** — one commit separated landed from in-flight commits and fixed exact week-boundary handling, and every subsequent weekly report distinguishes shipped totals from unmerged work because of it. ([2026-06-07](../../reports/weekly-report-2026-06-07.md))
- **Auto-sync footnoted out of authorship** — six syncs worth +1,143/−329 are recorded as a non-development delta rather than counted as hand-authored lines, which is what keeps the fleet's own figures honest about the tree that generates them. ([2026-06-21](../../reports/weekly-report-2026-06-21.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 16 |
| Commits | ~155 |
| Human attention | not broken out in report tables |
| Traditional equivalent | not broken out in report tables |
| Multiplier | ~18–95× |

## Weekly reports

[02-22](../../reports/weekly-report-2026-02-22.md), [03-01](../../reports/weekly-report-2026-03-01.md), [03-08](../../reports/weekly-report-2026-03-08.md), [03-15](../../reports/weekly-report-2026-03-15.md), [04-19](../../reports/weekly-report-2026-04-19.md), [04-26](../../reports/weekly-report-2026-04-26.md), [05-03](../../reports/weekly-report-2026-05-03.md), [05-10](../../reports/weekly-report-2026-05-10.md), [05-17](../../reports/weekly-report-2026-05-17.md), [05-24](../../reports/weekly-report-2026-05-24.md), [05-31](../../reports/weekly-report-2026-05-31.md), [06-07](../../reports/weekly-report-2026-06-07.md), [06-14](../../reports/weekly-report-2026-06-14.md), [06-21](../../reports/weekly-report-2026-06-21.md), [06-28](../../reports/weekly-report-2026-06-28.md), [07-05](../../reports/weekly-report-2026-07-05.md)

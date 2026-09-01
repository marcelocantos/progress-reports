# [canticode/orthograph](https://github.com/canticode/orthograph)

A Pencil-first shared sketch surface for a human and their agents. A Mac daemon owns a vector document in SQLite with an append-only op log; agents read and write it over MCP; an iPad app takes per-sample Pencil force. Born as `marcelocantos/orthograph`, it now ships as a Canticode product.

## The journey

Orthograph went from an empty repository to a `brew install`-able product in six days in early August 2026. The stated problem: agents can read code, logs and screenshots, but cannot share a drawing surface with a human in real time, so technical discussion collapses into ASCII, PlantUML links, or "describe what you mean". The Mac daemon (Homebrew service) owns a vector document in SQLite with an append-only op log, an HTTP MCP server giving agents a full observation and mutation surface over stable ULID-keyed objects, a deterministic render hash so an agent can tell whether the canvas changed, content-addressed media with four export formats, and an iPad SwiftUI app taking per-sample Apple Pencil force and tilt with Pencil-only ink and three-finger viewport control. Pairing runs the [pigeon](pigeon.md) QR ceremony, proven through the shipped binary rather than in a test harness. Dual-pipe intent/truth prediction sits on [sqlpipe](sqlpipe.md). 86 commits, +43,945/−3,269, 399 tests.

Two weeks later the project moved to Canticode as a closed-source product. The conversion squash re-adds the existing tree plus the work since 22 August: HTTP MCP on the daemon at `:13720/mcp` with a flock instance lock (a second start fails closed naming the incumbent), padlink/presence/recognize/render (PNG/PDF/SVG, iso lattice, paper), and a peer-app study with a steal/avoid matrix (stretch vs scale inverted from the desktop convention because touch precision is worse; multi-tap replicate rejected because iPadOS already spent those gestures). Homebrew formulae are published from the dev Mac by [tapper](https://github.com/marcelocantos/tapper), not by a CI job holding a tap token. The +41k line count is a conversion squash, not that week's authorship.

## Highlights

- **Empty repo to brew-installable in six days** — Mac daemon, MCP scene graph with stable ULIDs, Pencil iPad app, pigeon QR pairing proven through the shipped binary. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))
- **Canticode product, tap token out of CI** — closed-source conversion, daemon HTTP MCP with flock instance lock, padlink/render expansion, formulae published by tapper. ([2026-08-30](../../reports/weekly-report-2026-08-30.md))

## Standouts

- **A drawing surface agents can actually share** — the document is a vector scene graph with stable ULIDs and a deterministic render hash, not a screenshot the model has to describe. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))
- **Pairing proven through the shipped binary** — the pigeon QR ceremony is not a harness demo; the installable product is what pairs. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))
- **Instance lock is flock, daemon.json is advisory** — a second start fails closed naming the incumbent pid/addr; a crashed daemon leaves no stale lock to reap. ([2026-08-30](../../reports/weekly-report-2026-08-30.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 2 |
| Commits | ~90 |
| Human attention | ~8–14 h |
| Traditional equivalent | ~1.1–1.8 months |
| Multiplier | ~25–95× |

## Weekly reports

[08-03](../../reports/weekly-report-2026-08-09.md), [08-24](../../reports/weekly-report-2026-08-30.md)

# [marcelocantos/crosshair](https://github.com/marcelocantos/crosshair)

A Rust convergence-executor daemon that drives [bullseye](bullseye.md) targets toward satisfaction: it reads `bullseye.yaml` directly, runs each target's declared strategy on a tick, and records the outcome.

## The journey

crosshair began as a two-commit skeleton with an architectural commitment already made: it reads `bullseye.yaml` directly and treats a target's `strategy` block as the executor's per-target configuration, so there is no second config file to keep in sync. The Cargo skeleton (Rust edition 2024, toolchain 1.94+, Apache-2.0) pulled in `chrono`, `rusqlite`, `serde`, `serde_yaml_ng` and `tokio`, and bullseye gained `cross_enables` edges wiring crosshair into its dependency graph — but the README said plainly that there was no functionality yet.

A week later a single PR made it real. 🎯T1 delivered the convergence loop: a YAML loader, a per-target satisfaction check, a command runner with per-attempt timeout, SQLite-backed state, a tick loop on a **30 m → 2 h → 6 h → 24 h backoff ladder**, and a `crosshair status` subcommand. The design's economy is that **each tick is completely independent** — is the target satisfied? if not, run the strategy, note the outcome, wait — so stranded work, missed runs and transient failures all converge without a retry state machine, a resume path or a transient-versus-systemic failure classification. The backoff ladder replaces that entire surface, and the SQLite state stays purely descriptive (when was this last attempted, what happened) rather than prescriptive. The same release added `--help-agent` with an embedded agents guide, a seeded CHANGELOG, a README rewritten from its "no functionality yet" stub, a `bullseye` Makefile rule wiring fmt/clippy/test/clean-tree as standing invariants for `/cv`, and a release workflow building macOS arm64 and Linux amd64/arm64 binaries that updates the [Homebrew tap](homebrew-tap.md) on tag push.

July hardened it against its own children. Triggers gained 5-field `cron:`, `every:` and `manual` forms; each attempt now runs in its own process group so a backgrounded descendant cannot wedge later ticks; attempt state is WAL-persisted; and the backoff ladder was carried into 🎯T2 alongside a Fable-audit remediation, with ~21 new test declarations.

## Highlights

- **Bootstrap with no duplicate config** — the target's own `strategy` block is the executor's configuration, read straight from `bullseye.yaml`. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **v0.1.0 convergence loop** — satisfaction check, timed command runner, SQLite state and a 30 m → 2 h → 6 h → 24 h backoff ladder, all in one PR. ([2026-05-10](../../reports/weekly-report-2026-05-10.md))
- **Stateless loop, stateful audit log** — independent ticks make retry state machines, resume paths and failure classification unnecessary. ([2026-05-10](../../reports/weekly-report-2026-05-10.md))
- **Release pipeline to the tap** — three platform binaries built on tag push and the Homebrew formula updated automatically. ([2026-05-10](../../reports/weekly-report-2026-05-10.md))
- **Process-group isolation per attempt** — a backgrounded descendant can no longer wedge later ticks, with WAL-persisted attempt state and cron/interval/manual triggers. ([2026-07-12](../../reports/weekly-report-2026-07-12.md))

## Standouts

- **The target file is the executor's config** — the `strategy` block inside `bullseye.yaml` is read directly, so there is no second configuration to drift out of sync with the thing it drives. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **A backoff ladder instead of a retry state machine** — because every tick re-asks *is the target satisfied?* from scratch, 30 m → 2 h → 6 h → 24 h replaces resume paths, stranded-run recovery and transient-versus-systemic failure classification entirely. ([2026-05-10](../../reports/weekly-report-2026-05-10.md))
- **Stateless loop, stateful audit log** — SQLite records only what was attempted and what happened, never what should happen next, which is what keeps the loop free of prescriptive state. ([2026-05-10](../../reports/weekly-report-2026-05-10.md))
- **Each attempt in its own process group** — a backgrounded descendant of a strategy command can no longer wedge every later tick, with attempt state WAL-persisted across restarts. ([2026-07-12](../../reports/weekly-report-2026-07-12.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 3 |
| Commits | ~4 |
| Human attention | ~2–3 h |
| Traditional equivalent | ~0.4–0.7 months |
| Multiplier | ~25–60× |

## Weekly reports

[05-03](../../reports/weekly-report-2026-05-03.md), [05-10](../../reports/weekly-report-2026-05-10.md), [07-12](../../reports/weekly-report-2026-07-12.md)

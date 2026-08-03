# [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift)

sqlift is a declarative SQLite schema migration library with a pure C public API and a parallel Go implementation. It extracts schemas from live databases, diffs them structurally, generates JSON-serialisable migration plans, and applies them under a strict-by-default policy expressed as independent flag bits.

## The journey

sqlift opened with roughly 1,040 lines of header-only C++ covering the whole loop — schema extraction from a live database, structural diffing across tables, columns, indices, triggers, and views, and migration plan generation and application. `MigrationPlan` round-trips through nlohmann/json so plans can be inspected and stored, doctest was vendored to remove the brew dependency, and 56 tests across seven files landed alongside a `CLAUDE.md` and a complete `agents-guide.md` API reference.

The following week was a thirty-eight-commit expansion built around a **full Go port** with 127 tests. The interesting constraint is that two implementations of a fingerprinting tool must agree exactly: hash divergence between C++ and Go would surface as false-positive drift alerts, so dedicated cross-language tests verify byte-identical SHA-256 output for the same schema inputs, which demanded care over field ordering, string encoding, and numeric serialisation across the language boundary. Around it came redundant-index detection identifying prefix-duplicate, PK-duplicate, and exact-duplicate indices as `Warning` entries in `Diff()` output; constraint-name preservation through migration with a `migration_version()` counter; a documentation overhaul with C++/Go example parity; and audit fixes including FK-enforcement restoration on failed `apply()` (PRAGMA being connection-level, not transactional) and a string-literal-aware parser that stops CHECK constraints being mis-parsed. Six releases in seven days, ending at 149 Go and 122 C++ tests. The next release consolidated the surface: `sqlift_c.h`/`sqlift_c.cpp` merged into `sqlift.h`/`sqlift.cpp` so the public header is **pure C** with `extern "C"` linkage and JSON interchange, C++ types became implementation-internal, and every test and document was rewritten against the C API.

The defining design change came in May. The boolean `allow_destructive` parameter had been load-bearing for too many distinct concerns: SQLite's twelve-step rebuild for a column-type change is not destructive in the data-dropping sense, dropping a CHECK or FK is a strict relaxation, and a new FK may succeed or fail depending on existing data. v0.13.0 and v0.14.0 split these into independent atomic bits — `SQLIFT_ALLOW_REBUILD`, `SQLIFT_ALLOW_DESTRUCTIVE`, `SQLIFT_ALLOW_LOOSEN`, `SQLIFT_ALLOW_DATA_DEPENDENT` — with themed combinations and a strict default under which only pure additive changes succeed. A pure-loosening rebuild passes either `_REBUILD` or `_LOOSEN`, so "backwards-compatible only" is expressible as `AllowLoosen` alone. The deeper move is that `BreakingChangeError` shifted from diff time to **apply time**: a plan carrying `data_dependent: true` operations is still a valid plan, and whether it may run depends on the caller's contract rather than on the plan's shape. Being pre-1.0, the breaking surface change shipped as a normal minor release and reset the 1.0 settling clock, with STABILITY.md re-annotated Fluid.

The remaining arc is distribution and consumption. v0.15.0–v0.17.0 added `CREATE VIRTUAL TABLE` support for fts5, fts3-4, and rtree, bundled the C++ sources inside the Go module for cgo consumers, and dropped the unconditional `-lsqlite3` from cgo LDFLAGS — the repo's +29,472 lines that week are the bundled SQLite C++ amalgamation, vendored rather than authored. Downstream, [sqlpipe](sqlpipe.md) bundles sqlift and propagated the strict-by-default policy through its own C surface in v0.22.0 and v0.23.0, and [mnemo](mnemo.md) routed all of its schema change through sqlift to enforce a strict additive-only store contract. Maintenance since has been light — ccache wiring, the `mk`→`cv` migration — with v0.18.0 adding richer apply error messages for on-device diagnosis.

## Highlights

- **Initial release** — header-only C++ schema extraction, structural diffing, and plan generation across tables, columns, indices, triggers, and views, with JSON round-tripping and 56 tests. ([02-22](../../reports/weekly-report-2026-02-22.md))
- **Go port with cross-language hash verification** — a full reimplementation with 127 tests, plus dedicated tests proving C++ and Go emit byte-identical SHA-256 fingerprints so drift detection interoperates across languages. ([03-01](../../reports/weekly-report-2026-03-01.md))
- **Redundant index detection** — `DetectRedundantIndexes()` flags prefix-duplicate, PK-duplicate, and exact-duplicate indices, surfaced as typed warnings in `Diff()` output. ([03-01](../../reports/weekly-report-2026-03-01.md))
- **Audit fixes on the apply path** — FK enforcement restored after a failed `apply()` (PRAGMA is connection-level, not transactional), and a string-literal-aware parser that stops CHECK constraints being mis-parsed. ([03-01](../../reports/weekly-report-2026-03-01.md))
- **C-only public API (v0.12.0)** — the public header became pure C with JSON interchange, C++ types confined to the implementation, and every test and document rewritten against it. ([03-08](../../reports/weekly-report-2026-03-08.md))
- **Strict-by-default apply policy with independent flag bits** — one overloaded boolean replaced by four atomic allow bits and themed combinations, with `BreakingChangeError` moved from diff time to apply time so policy lives with the caller, not the plan. ([05-10](../../reports/weekly-report-2026-05-10.md))
- **Virtual tables and standalone Go distribution** — fts5/fts3-4/rtree `CREATE VIRTUAL TABLE` support, C++ sources bundled in the Go module for cgo consumers, and the unconditional `-lsqlite3` dropped; the week's +29,472 lines are the vendored SQLite amalgamation, not authored code. ([05-24](../../reports/weekly-report-2026-05-24.md))
- **Adopted as mnemo's durability contract** — mnemo routed all schema change through sqlift under a strict additive-only policy, so an older binary can always read a newer database. ([05-24](../../reports/weekly-report-2026-05-24.md))
- **Richer apply diagnostics (v0.18.0)** — apply error messages expanded for on-device diagnosis. ([07-19](../../reports/weekly-report-2026-07-19.md))

## Standouts

- **Two implementations forced to agree byte-for-byte** — a fingerprinting tool whose C++ and Go ports disagree by one byte reports false-positive drift forever, so the Go port shipped with dedicated cross-language tests proving identical SHA-256 output for the same schema, which required getting field ordering, string encoding, and numeric serialisation to match exactly across the language boundary. ([03-01](../../reports/weekly-report-2026-03-01.md))
- **One boolean split into four independent bits** — `allow_destructive` had been carrying four unrelated concerns; v0.13.0/v0.14.0 replaced it with `SQLIFT_ALLOW_REBUILD`, `_DESTRUCTIVE`, `_LOOSEN`, and `_DATA_DEPENDENT`, and moved `BreakingChangeError` from diff time to apply time — a plan with `data_dependent: true` is still a valid plan, and whether it may run belongs to the caller's contract, not the plan's shape. ([05-10](../../reports/weekly-report-2026-05-10.md))
- **A failed `apply()` that left foreign keys switched off** — `PRAGMA foreign_keys` is connection-level, not transactional, so rolling back a migration did not restore it and the connection silently continued with FK enforcement disabled; found in audit and fixed alongside a string-literal-aware parser that stops CHECK constraints being mis-parsed. ([03-01](../../reports/weekly-report-2026-03-01.md))
- **Promoted to another project's durability contract** — [mnemo](mnemo.md) routed every schema change through sqlift under a strict additive-only policy, paired with pre-migration snapshots, so an older binary can always read a newer database. ([05-24](../../reports/weekly-report-2026-05-24.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 9 |
| Commits | 63 |
| Human attention | ~11–19 h |
| Traditional equivalent | ~1.6–2.7 months |
| Multiplier | ~18–95× |

## Weekly reports

[02-22](../../reports/weekly-report-2026-02-22.md), [03-01](../../reports/weekly-report-2026-03-01.md), [03-08](../../reports/weekly-report-2026-03-08.md), [04-19](../../reports/weekly-report-2026-04-19.md), [05-03](../../reports/weekly-report-2026-05-03.md), [05-10](../../reports/weekly-report-2026-05-10.md), [05-24](../../reports/weekly-report-2026-05-24.md), [06-14](../../reports/weekly-report-2026-06-14.md), [07-19](../../reports/weekly-report-2026-07-19.md)

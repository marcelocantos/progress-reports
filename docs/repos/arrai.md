# [arr-ai/arrai](https://github.com/arr-ai/arrai)

arr.ai, a Go-hosted relational data-transformation language. Across the series it is a maintenance and modernisation project: dependency-free generics, hot-path performance, CI and CVE custodianship, and occasional grammar corrections.

## The journey

arrai enters the series with a diagnosis rather than a change. A 161-line research document assessed the project's state — a peak of 182 commits in 2021, effectively dormant since 2024, 146 open issues — and set a direction: performance quick wins (object pooling, fast-path function application), medium-term work (bytecode compilation, lazy enumerators), and language evolution (gradual typing, deterministic parallelism), with the strategic recommendation to position arr.ai as an **embeddable data-transformation engine for Go**.

The heaviest week followed in early March and did two things at once. The **generics migration** moved all frozen types to `Set[T]`, `Map[K,V]` and `Key[T]` across 43 files, replaced `anz-bank/pkg/log` with stdlib `log/slog` and `anz-bank/pkg/mod` with a local `gomod.go` helper — eliminating the external `anz-bank/pkg` dependency entirely — and changed `multipleValues` to `Set[Value]` rather than `Set[any]` to stop panics on uncomparable types. In the same week hot-path caching landed: `GenericTuple.Names()` cached behind `sync.Once` where it had been rebuilding a `frozen.Set[string]` on every call despite immutability, and `Relation.attrMap` computed eagerly in `newRelation()`, for **−99% getBucket overhead**, −62% RelationAttrs, −44% `Relation.Enumerate` and −9–19% end-to-end on GenericSetJoin. Upstream dependencies moved with it: [frozen](frozen.md) to v1.9.0 for single-call H128 hashing, [wbnf](wbnf.md) to v0.38.0.

Custodianship dominated the rest. A 20-commit week modernised CI (Go 1.24, golangci-lint v1.64.8, a Node bump, a WASM CI path fix, goreleaser v2 config and a PAT for tag-triggered releases), picked up frozen v1.11.0's zero-alloc read optimisations with regenerated stdlib bundles, and cleared npm security advisories (svgo Billion Laughs DoS, serialize-javascript), alongside benchmark artefacts, a dict-union regression test, a `--help-agent` flag and a NOTICES file. April closed a lodash code-injection vulnerability (GHSA-r5fr-rjxr-66jc), switched docs CI from yarn to `npm ci`, and cut **v0.336.0**.

July brought the only language change in the window and its reversal: a one-token grammar correctness fix making the safe-accessor fallback `a?.b : c` bind a full expression rather than the restricted `@`, co-authored by Oliver Lade — reverted the following week alongside Dependabot crypto and docs vulnerability bumps and a Netlify docs-build fix.

## Highlights

- **State-of-the-language assessment** — a 161-line document diagnosing dormancy and proposing an embeddable-engine positioning with a staged performance and language roadmap. ([2026-02-15](../../reports/weekly-report-2026-02-15.md))
- **Generics migration across 43 files** — `Set[T]`/`Map[K,V]`/`Key[T]` throughout, with the entire `anz-bank/pkg` dependency eliminated in favour of stdlib `log/slog` and a local module helper. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **Hot-path caching** — `sync.Once`-cached `GenericTuple.Names()` and eager `Relation.attrMap` for −99% getBucket overhead and −9–19% end-to-end on GenericSetJoin. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **CI modernisation and a performance audit** — Go 1.24, golangci-lint v1.64.8, WASM path fix, goreleaser v2, benchmark artefacts and a dict-union regression test. ([2026-03-08](../../reports/weekly-report-2026-03-08.md))
- **CVE closure and v0.336.0** — the lodash code-injection advisory fixed, docs CI moved to `npm ci`, and a release cut with an audit log. ([2026-04-12](../../reports/weekly-report-2026-04-12.md))
- **Safe-accessor grammar fix** — `a?.b : c` made to bind a full expression rather than the restricted `@`, co-authored by Oliver Lade. ([2026-07-12](../../reports/weekly-report-2026-07-12.md))
- **Reverted the following week** — the safe-accessor `fall=expr` change was backed out alongside Dependabot crypto/docs bumps and a Netlify docs-build fix. ([2026-07-19](../../reports/weekly-report-2026-07-19.md))

## Standouts

- **−99% getBucket overhead from two caches** — `GenericTuple.Names()` had been rebuilding a `frozen.Set[string]` on every call despite immutability; caching it behind `sync.Once` and computing `Relation.attrMap` eagerly also gave −62% RelationAttrs, −44% `Relation.Enumerate` and −9–19% end-to-end on GenericSetJoin. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **A whole dependency deleted inside a type migration** — the `Set[T]`/`Map[K,V]`/`Key[T]` pass across 43 files also removed `anz-bank/pkg` entirely, swapping its log package for stdlib `log/slog` and its mod package for a local `gomod.go`. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **A dormancy diagnosis that set the direction** — 182 commits in 2021, effectively dormant since 2024, 146 open issues; the resulting 161-line assessment argued for positioning arr.ai as an embeddable data-transformation engine for Go. ([2026-02-15](../../reports/weekly-report-2026-02-15.md))
- **A grammar fix that lasted one week** — the one-token change making `a?.b : c` bind a full expression landed with an external co-author and was backed out the following week. ([2026-07-12](../../reports/weekly-report-2026-07-12.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 6 |
| Commits | 39 |
| Human attention | ~7.5–12 h |
| Traditional equivalent | ~0.7–1.2 months |
| Multiplier | ~25–90× |

## Weekly reports

[02-15](../../reports/weekly-report-2026-02-15.md), [03-01](../../reports/weekly-report-2026-03-01.md), [03-08](../../reports/weekly-report-2026-03-08.md), [04-12](../../reports/weekly-report-2026-04-12.md), [07-12](../../reports/weekly-report-2026-07-12.md), [07-19](../../reports/weekly-report-2026-07-19.md)

# [arr-ai/frozen](https://github.com/arr-ai/frozen)

Go persistent immutable collections built on HAMTs. Across three weeks in March it acquired a two-level hash architecture and a zero-allocation read path, and shipped v1.9.0 through v1.11.0.

## The journey

The March campaign was a hashing redesign with measurable consequences. **H128** replaced the old two-separately-seeded-call pattern with a single `func(T) H128` returning both halves of a 128-bit content hash, cached as `struct{lo, hi uintptr}` in every HAMT node, with an `EqArgs.fullHash` flag enabling O(1) equality short-circuit for Sets whose hash captures full content; [arr-ai/hash](https://github.com/arr-ai/hash) was internalised into `internal/pkg/hash` with cross-platform H128-AES assembly (amd64 and arm64 optimised, software fallback for 386/arm/mips/ppc64/s390x) for a geomean −3.3% in time. The companion idea is the sharper one: every node also caches **h0**, the XOR of all seed-0 element hashes, propagated upward by XOR of children, so `Equal()` compares h0 first and a mismatch means entire subtrees differ without traversal — **a 500x speedup on 1M-element set inequality detection**, 25 µs to 50 ns, with the builder deferring h0 to a single bottom-up `computeH0()` pass in `Finish()`. The two levels compose: h0 rejects instantly, H128 confirms instantly, and element-by-element comparison survives only for hash collisions. HAMT internals were reworked in the same 36-commit week — batched spine allocations (−60% GC objects at 1M elements), inlined branch copies, cached typed dispatch replacing per-operation `sync.Map` lookups (−75% SetBuilder allocations at 1M), and structural vetting behind a `frozen_vet` build tag — with `BenchmarkSetOps` covering Equal/Intersection/Difference/SubsetOf/Has at 1K and 1M across Same/Equal/Half/Disjoint/Near(99%)/Sparse(1%) overlap patterns and benchstat baselines. v1.9.0 shipped with an audit report carrying 34 findings (7 high, 2 medium).

The follow-on weeks eliminated allocations rather than adding capability. v1.10.0 refactored `EqArgs` to embed an `EqHash` interface into distinct concrete types carrying their hash and equality functions as struct fields — a pattern that gets polymorphic dispatch at the HAMT node level without the interface allocation Go generics would normally force — making `Map.Get`, `Map.Has`, `Set.Has` and `Map.Without` allocation-free and fixing a hash-consistency bug between the `EqHash` and default paths. v1.11.0 added no-op write elimination, so `Set.With` on an existing element and `Map.With` on an existing key with the same value return without allocating, detected by hash comparison before tree traversal, and a type-matrix correctness suite across int, string, float64, derived types, pointers, interfaces and structs, including independence tests proving `Set[int]` and `Set[ID]` do not collide in the HAMT. 🎯T2 was achieved, and [arrai](arrai.md) picked the work up downstream in both directions — v1.9.0 for H128, v1.11.0 for the zero-alloc reads.

## Highlights

- **H128 content hashing** — a single-call 128-bit hash cached per node with AES-accelerated assembly and a portable fallback, plus O(1) Set equality short-circuit. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **Recursive XOR h0 for 500x inequality detection** — 1M-element set inequality falls from 25 µs to 50 ns, with h0 computed bottom-up once in `Finish()`. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **HAMT internals overhaul** — batched spine allocations, inlined branch copies and cached typed dispatch for −60% GC objects and −75% SetBuilder allocations at 1M elements. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **Zero-alloc read path (v1.10.0/v1.11.0)** — `EqHash` embedded into distinct concrete types removes interface allocation from `Map.Get`, `Map.Has`, `Set.Has` and `Map.Without`. ([2026-03-08](../../reports/weekly-report-2026-03-08.md))
- **No-op write elimination and type-matrix tests** — redundant `With` calls return without allocating, and independence tests prove derived types do not collide in the HAMT; 🎯T2 achieved. ([2026-03-15](../../reports/weekly-report-2026-03-15.md))

## Standouts

- **500x faster inequality detection from an XOR** — every node caches h0, the XOR of all seed-0 element hashes propagated upward from its children, so a root mismatch means entire subtrees differ without traversal: 1M-element set inequality falls from 25 µs to 50 ns. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **Two hash levels that cover both ends of the distribution** — h0 rejects unequal sets instantly and H128 confirms equal ones instantly, leaving element-by-element comparison alive only for genuine hash collisions. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **Zero-allocation polymorphic dispatch in Go generics** — embedding `EqHash` into distinct concrete types that carry their hash and equality functions as struct fields gets node-level dispatch without the interface allocation generics would otherwise force, making `Map.Get`, `Map.Has`, `Set.Has` and `Map.Without` allocation-free. ([2026-03-08](../../reports/weekly-report-2026-03-08.md))
- **AES-accelerated hashing across six architecture targets** — `arr-ai/hash` was internalised with optimised amd64 and arm64 H128 assembly and a software fallback for 386/arm/mips/ppc64/s390x, for a geomean −3.3% in time. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 3 |
| Commits | 64 |
| Human attention | ~11–17 h |
| Traditional equivalent | 1.1–1.8 months |
| Multiplier | ~25–50× |

## Weekly reports

[03-01](../../reports/weekly-report-2026-03-01.md), [03-08](../../reports/weekly-report-2026-03-08.md), [03-15](../../reports/weekly-report-2026-03-15.md)

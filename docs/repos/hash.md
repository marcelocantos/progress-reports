# [arr-ai/hash](https://github.com/arr-ai/hash)

Hashing primitives behind [frozen](frozen.md). H128 AES assembly (amd64/arm64) with a portable fallback, later extracted as a seedless `hash128.Hashable` so nested values can cache a result.

## The journey

hash entered the series as the package frozen internalised during the March H128 campaign: a single `func(T) H128` returning both halves of a 128-bit content hash, with cross-platform AES assembly and a software fallback, for a geomean −3.3% in frozen's time. Frozen cached both halves per HAMT node and added the XOR-of-children h0 short-circuit that made 1M-element set inequality 500× faster.

In late August hash128 was extracted as a public, **seedless** `Hashable` interface. Composite values combine part hashes with Mix or Xor and can cache their result, which the seeded `hash.Hash64` interface makes impossible for nested values — every caller seeds differently. The amd64 32-bit routine places its lane at offset 4 so `Uint32(x)` and `Uint64(x)` no longer share an input block. Frozen v1.13.0 hashes elements through `hash128.Hashable` when they implement it; [arrai](arrai.md)'s interned-shape tuples consume the same path.

## Highlights

- **Internalised into frozen for H128** — AES-accelerated 128-bit hashing across six architecture targets, cached per HAMT node. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **hash128 extracted, seedless** — nested values can cache; Mix/Xor combine parts; `Uint32`/`Uint64` no longer share an input block. ([2026-08-30](../../reports/weekly-report-2026-08-30.md))

## Standouts

- **A seeded hash cannot be cached inside a nested value** — `hash.Hash64` takes a seed, so a composite cannot store "its" hash; hash128 is seedless so it can. ([2026-08-30](../../reports/weekly-report-2026-08-30.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 2 |
| Commits | ~2 |
| Human attention | ~1–2 h |
| Traditional equivalent | ~0.2–0.4 months |
| Multiplier | ~25–50× |

## Weekly reports

[03-01](../../reports/weekly-report-2026-03-01.md), [08-24](../../reports/weekly-report-2026-08-30.md)

# [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal)

A proposal to add [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754) decimal64 and decimal128 types to the Go standard library, backed by a working playground implementation.

## The journey

The proposal landed in a single +2,569-line commit in late February — not a design document alone, but a document with a working playground implementation and a CI pipeline behind it, which is what makes a stdlib proposal arguable rather than aspirational. It sits at #39 in the series' ranked [achievements](../achievements.md).

The following week's updates track the implementation's state rather than the proposal's prose: ABI, DWARF and BID128 exponent fixes recorded, and the math decimal tests made **blocking in CI** once a Linux bootstrap bug that had been holding them back was resolved. The headline statistics were restated at 129 files across 18+ packages with 3,500+ lines of tests.

## Highlights

- **Proposal plus playground implementation** — +2,569 lines covering decimal64/decimal128 for the Go stdlib, with CI, in one commit. ([2026-02-22](../../reports/weekly-report-2026-02-22.md))
- **Decimal tests made blocking in CI** — after a Linux bootstrap bug was cleared, the math decimal suite became a gate rather than an advisory. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **ABI, DWARF and BID128 exponent fixes** — status updated against an implementation spanning 129 files, 18+ packages and 3,500+ test lines. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 2 |
| Commits | 4 |
| Human attention | ~5–9 h |
| Traditional equivalent | 0.2–0.3 months |
| Multiplier | ~25–95× |

## Weekly reports

[02-22](../../reports/weekly-report-2026-02-22.md), [03-01](../../reports/weekly-report-2026-03-01.md)

# [arr-ai/wbnf](https://github.com/arr-ai/wbnf)

The grammar toolkit underpinning [arrai](arrai.md). Its appearances in the series are a research paper on where the notation should go, and a round of CI and security custodianship.

## The journey

wbnf's first appearance is a 717-line research paper, "Toward a Universal Grammar", arguing a position rather than shipping code. Its central claim is that notorious parsing difficulties — C's typedef ambiguity, C++'s template angle brackets — are **not parsing problems at all but semantic-analysis problems**, and dissolve once grammars are constrained to describe only surface syntax. The mechanisms proposed are concrete: regex/grammar unification with character classes as native grammar primitives, integrated tokenisation via labelled alternatives, generalised positional constraints (`@col`, `@line` predicates) for indentation-sensitive languages, and algebraic grammar composition for clean sublanguage embedding, with a related-work survey covering [SDF](https://www.syntax-definition.org/), Rascal, PEG/OMeta/Ohm and [LPEG](http://www.inf.puc-rio.br/~roberto/lpeg/) and an implementation roadmap.

Two months later the repo got a 19-commit maintenance pass: GitHub Actions bumped to Node-24-compatible versions with setup-go/checkout ordering fixed, golangci-lint pinned to v1.48 for reproducible CI, all outstanding lint warnings resolved (T1, T3), [logrus](https://github.com/sirupsen/logrus) bumped from v1.9.0 to v1.9.3 to close CVE-2025-65637, the GLL engine research document refined on auto-regular rules and filter semantics, and the bespoke generate-tag workflow retired in favour of the shared `/release` skill. arrai consumed the result via a v0.38.0 bump.

## Highlights

- **"Toward a Universal Grammar"** — a 717-line paper proposing regex/grammar unification, labelled-alternative tokenisation, positional constraints and algebraic composition. ([2026-02-15](../../reports/weekly-report-2026-02-15.md))
- **Hard parsing problems reframed** — C typedef ambiguity and C++ template brackets argued to be semantic-analysis problems that dissolve when grammars describe only surface syntax. ([2026-02-15](../../reports/weekly-report-2026-02-15.md))
- **CI modernisation and CVE-2025-65637** — Node-24 Actions, a pinned linter for reproducibility, a logrus bump closing the advisory, and the generate-tag workflow retired for `/release`. ([2026-04-12](../../reports/weekly-report-2026-04-12.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 2 |
| Commits | 20 |
| Human attention | 1–3 h |
| Traditional equivalent | ~0.5–1.0 months |
| Multiplier | ~30–90× |

## Weekly reports

[02-15](../../reports/weekly-report-2026-02-15.md), [04-12](../../reports/weekly-report-2026-04-12.md)

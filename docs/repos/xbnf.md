# [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf)

Scannerless CFG parser generator for Go. Grammars and regexes are the same notation. Regular fragments compile to DFAs; the rest run as GLL. It succeeds [wbnf](https://github.com/arr-ai/wbnf) as a new product, not a compatible upgrade: alternation is unordered, and ambiguity is a compile error unless the grammar says how to resolve it.

## The journey

xbnf was bootstrapped in the week of 31 August 2026: spec, plan, CLI stub, and an engine work graph, then a grammar IR for every construct, then the GLL engine with a DFA terminal layer (🎯T4/🎯T5). `|` has no source-order meaning; `|>` is ordered choice and must not mix with it; `#prefer` / `#longest` / `#wrap` / `/term/` are first-class. `fromwbnf` parses old `.wbnf` into an IR of meaning; leftover kinds are named gaps. The engine eats its own cooking: `docs/xbnf.xbnf` is parsed by xbnf.

The same week closed two gates that define the product. 🎯T22: seven live language tracks (SQL, XML, Go, Python, YAML, JavaScript, CommonMark) are Failed=0 against **present** oracles on pinned third-party corpora — pin lists were not shrunk after misses. 🎯T25: a pair-ratio KEEP/DISCARD/NOISY gate, golden-identical trees required, took nested JSON 64 KB from 11.78 ms to **4.06 ms** / 2.35 MB / 2 allocs (2.882×, 10/10) and the corpus aggregate to 3.043× with B/op 18.89 → 3.20 MB. H2 fusion, H3 predecessor-linked evidence, unit-production shortcut, DFA ASCII tables, Afroozeh-style callee sharing and a chart pool all KEEP; remaining profile candidates sit below the 3% bar. A capture-context correction (🎯T29/🎯T30) that fixed order-dependent reference matching was **not** reverted when the optimisation gate said DISCARD/NOISY.

The following week made xbnf a wbnf replacement for arr.ai (🎯T33): macros expand at compile, `%%` hooks and `#import` run on the product path, `\b` matches as in Go regexp, converted `arrai.wbnf` agrees with wbnf on a pinned accept/reject set. Parse output became an event stream (🎯T34) — open/close/leaf/skip events whose lengths tile `[0, End)`, 24 bytes each, `#wrap` visible as skip, `Tree()` a decode. Positions (🎯T23) and converted-grammar language parity (🎯T32) landed with it. The sandbox runs the committed T22 grammars as a tree viewer.

## Highlights

- **GLL+DFA engine, self-host, unordered `|`** — empty repo to a scannerless CFG engine that parses `xbnf.xbnf`; ambiguity is a compile error unless a disambiguator is declared. ([2026-09-06](../../reports/weekly-report-2026-09-06.md))
- **Seven languages Failed=0 against present oracles** — SQL/`pg_query`, XML/`xmllint`, Go/`go/parser`, Python/CPython, YAML/PyYAML events, JS/Acorn, CommonMark/cmark; pins not shrunk after misses. ([2026-09-06](../../reports/weekly-report-2026-09-06.md))
- **KEEP-gated 2.88× JSON / 3.04× corpus** — pair ratios, not medians; golden-identical trees; public tree is the API floor. ([2026-09-06](../../reports/weekly-report-2026-09-06.md))
- **Capture matching not reverted for speed** — order-dependent bindings fixed; DISCARD/NOISY is not a reason to restore the old semantics. ([2026-09-06](../../reports/weekly-report-2026-09-06.md))
- **Replace wbnf for arr.ai** — converted `arrai.wbnf` agrees with wbnf on a pinned accept/reject set (🎯T33). ([2026-09-13](../../reports/weekly-report-2026-09-13.md))
- **Event stream that tiles the input** — 24-byte events, wrap as skip, MEM WIN 2.88 → 1.30 MB, KEEP. ([2026-09-13](../../reports/weekly-report-2026-09-13.md))

## Standouts

- **Alternation that means nothing until you say how** — PEG ordered choice is control flow pretending to be a combinator; xbnf's `|` has no source-order meaning. ([2026-09-06](../../reports/weekly-report-2026-09-06.md))
- **Keep/discard is a pair ratio, not a median** — interleaved old/new at `GOMAXPROCS=1` after an idle wait; `NOISY` refuses to decide. ([2026-09-06](../../reports/weekly-report-2026-09-06.md))
- **An event stream that tiles the input** — leaf+skip lengths sum to `End`; positions are a prefix sum; `Node.Text` is a slice. ([2026-09-13](../../reports/weekly-report-2026-09-13.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 2 |
| Commits | 94 |
| Human attention | ~8–13 h |
| Traditional equivalent | ~1.1–1.8 months |
| Multiplier | ~40–70× |

## Weekly reports

[08-31](../../reports/weekly-report-2026-09-06.md), [09-07](../../reports/weekly-report-2026-09-13.md)

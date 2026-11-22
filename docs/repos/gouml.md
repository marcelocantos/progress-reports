# [marcelocantos/gouml](https://github.com/marcelocantos/gouml)

A Go port of [PlantUML](https://plantuml.com) produced by mechanically transpiling the Java source with tree-sitter, plus a runtime shim that supplies Java semantics for strings, numbers, collections, exceptions and dispatch.

## The journey

gouml began in the first week of November as a deliberate alternative to hand-porting. `j2go` parses the whole PlantUML tree, attributes types and emits one Go package with stubs for everything it does not yet include, while the `rt` shim carries Java's behaviour: operator precedence, class initialisation order, boxed attributes and aliasing collection views. The first week landed 39 commits and a transpiler that reached the runtime boundary across the whole of PlantUML's rendering layer.

The second landing week made it a measured port. 61 commits ported mindmap, WBS, JSON, YAML, Gantt, salt, network, timing, Wire, regex, EBNF, Git log, chart, board and legacy activity diagrams, and PlantUML's own command line. A `make parity` gate with name-level locks and a clock pin judges each integrator merge, and a ladder of audits files every remaining difference as a numbered target. Layout fidelity depends on Java's font metrics, so fallback advances are captured as tables rather than guessed.

## Highlights

- **Mechanical transpilation of PlantUML** — tree-sitter-driven `j2go` with a Java-semantics runtime. ([2026-11-08](../../reports/weekly-report-2026-11-08.md))
- **A dozen diagram families ported** — mindmap, WBS, JSON, YAML, Gantt, salt, network, timing, Wire, legacy activity and more. ([2026-11-22](../../reports/weekly-report-2026-11-22.md))
- **A parity gate** — `make parity` with name-level locks, a clock pin and integrator-by-integrator gates. ([2026-11-22](../../reports/weekly-report-2026-11-22.md))

## Standouts

- **Capturing Java's font advances** — format 2 and 3 fallback captures with 248 glyph rows, refused when whole-pixel, summed in float as Java does. ([2026-11-22](../../reports/weekly-report-2026-11-22.md))
- **Java runtime semantics in Go** — UTF-16 code units, ASCII regex classes, a DEFLATE reader and signed infinity on decimal overflow. ([2026-11-22](../../reports/weekly-report-2026-11-22.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 3 |
| Commits | 103 |
| Human attention | ~3–5 h in the latest week |
| Traditional equivalent | ~1.0–1.7 months in the latest week |
| Multiplier | not broken out beyond the weekly tables |

## Weekly reports

[11-02](../../reports/weekly-report-2026-11-08.md), [11-09](../../reports/weekly-report-2026-11-15.md), [11-16](../../reports/weekly-report-2026-11-22.md)

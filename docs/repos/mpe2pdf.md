# [marcelocantos/mpe2pdf](https://github.com/marcelocantos/mpe2pdf)

An npm-distributed Markdown-to-PDF converter, which gained an MCP server mode so agents can invoke conversions directly.

## The journey

mpe2pdf appears in the series as an existing tool being prepared for the outside world. A five-commit pass added Apache-2.0 licensing, a `STABILITY.md`, an agent guide behind `--help-agent`, and fixes to the npm publish configuration; a follow-up excluded `.db` files from the published tarball, which had been shipping in the package.

The substantive change came in April: an **MCP server mode** behind `--mcp`, exposing a `convert` tool so Markdown-to-PDF conversion can be driven programmatically from a Claude Code session rather than shelled out to, backed by smoke tests over the conversion pipeline and released as v0.4.0. The same week saw [vellum](vellum.md) created as a separate Go MCP server addressing the same conversion problem from a different toolchain.

## Highlights

- **Open-source release preparation** — Apache-2.0 licensing, `STABILITY.md`, an `--help-agent` guide and npm publish configuration fixes. ([2026-03-15](../../reports/weekly-report-2026-03-15.md))
- **Packaging fix** — `.db` files excluded from the published npm tarball. ([2026-03-29](../../reports/weekly-report-2026-03-29.md))
- **MCP server mode, v0.4.0** — a `--mcp` flag exposing a `convert` tool for agent-driven conversion, with smoke tests over the pipeline. ([2026-04-12](../../reports/weekly-report-2026-04-12.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 3 |
| Commits | ~13 |
| Human attention | not broken out in report tables |
| Traditional equivalent | ~0.4–0.7 months |
| Multiplier | ~28–65× |

## Weekly reports

[03-15](../../reports/weekly-report-2026-03-15.md), [03-29](../../reports/weekly-report-2026-03-29.md), [04-12](../../reports/weekly-report-2026-04-12.md)

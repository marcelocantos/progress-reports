# [marcelocantos/mcpsafe](https://github.com/marcelocantos/mcpsafe)

A Go reverse proxy that sits between an MCP server and its real backend, injecting credentials in transit so the MCP server never sees a secret. Per-backend request rewriting is scripted in Starlark.

## The journey

mcpsafe appears twice in the series, both times as an initial commit — first in March as a one-commit Go library for safe MCP tool execution patterns, then in May with the shape it kept. That second bootstrap reframed the idea as a **credential-injecting reverse proxy**: an MCP server such as `fogbugz-mcp` talks to mcpsafe, which reads credentials from the macOS Keychain via `security find-generic-password`, caches them in memory for the session, rewrites the host to the real backend and injects auth on the way through. The MCP server itself is never trusted with the secret.

The per-backend logic is deliberately data rather than code: a Starlark `transform(req)` function mutates a dict with `host`, `scheme`, `path` and `query` keys, so adding a backend means writing a script, not recompiling the proxy. The bootstrap shipped a working `examples/fogbugz.star`, a Darwin Keychain adapter, the listener, transform engine and driver script, with eight unit tests across roughly 830 lines.

## Highlights

- **Initial Go library for safe MCP tool execution patterns** — one commit, before the project settled on its proxy shape. ([03-08](../../reports/weekly-report-2026-03-08.md))
- **Credential-injecting reverse proxy** — Keychain-sourced secrets injected into MCP traffic in flight, with the host rewritten to the real backend, so the MCP server never holds a credential. ([05-03](../../reports/weekly-report-2026-05-03.md))
- **Starlark per-backend transforms** — `transform(req)` mutates `host`/`scheme`/`path`/`query`, making a new backend a script rather than a code change; ~830 lines with 8 unit tests. ([05-03](../../reports/weekly-report-2026-05-03.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 2 |
| Commits | 3 |
| Human attention | ~1 h |
| Traditional equivalent | ~0.1–0.2 months |
| Multiplier | ~25–50× |

## Weekly reports

[03-08](../../reports/weekly-report-2026-03-08.md), [05-03](../../reports/weekly-report-2026-05-03.md)

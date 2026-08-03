# [marcelocantos/cworkers](https://github.com/marcelocantos/cworkers)

An MCP server that dispatches Claude worker processes on demand, with a companion terminal dashboard. Two consecutive weeks took it from a socket-based CLI to a 35 KB stateless C broker.

## The journey

The first week produced **nine tagged releases (v0.1.0–v0.9.0)** and a wholesale protocol simplification: a Unix-socket CLI protocol with six subcommands was replaced by a single `cwork(task, cwd, model?)` [MCP](https://modelcontextprotocol.io/) tool over streamable HTTP on port 4242, built on [mcp-go](https://github.com/mark3labs/mcp-go). Callers stopped managing socket lifecycles and started making one tool call. Around that sat a self-warming worker pool — each dispatch triggers a replacement spawn, which is what fixed cold-pool bootstrapping where the first requests found no available worker — plus shadow auto-discovery locating the calling session's Claude transcript from its working directory so manual shadow/unshadow commands disappeared, content-driven progress that parses markdown headings out of worker output and forwards them as MCP progress notifications, and SQLite persistence behind a Svelte dashboard (~4,000 lines in a single commit) streaming logs over SSE with ANSI rendering via [xterm.js](https://xtermjs.org/).

The second week deleted most of it. Recognising that an MCP stdio frontend is essentially a JSON-to-process bridge — reading JSON-RPC from stdin, spawning a process, streaming the result back — the server was rewritten from Go to C: a **35 KB statically-linked binary replacing a 15 MB Go binary**, roughly 700 lines with a streaming JSON emitter, `.incbin`-embedded agent guide, pthread-per-call concurrent dispatch and structured JSONL logging. v0.14.0 went further and made the broker **stateless**, removing shadow context, the worker pool and transcript discovery entirely, because spawning a fresh Claude process per request turned out fast enough that pooling added complexity without measurable benefit. The Svelte dashboard was replaced by a `cdash` TUI written first in Rust with [ratatui](https://github.com/ratatui-org/ratatui) and then rewritten in Go with [bubbletea](https://github.com/charmbracelet/bubbletea) and [glamour](https://github.com/charmbracelet/glamour), showing worker IDs prefixed by model and rendering worker output as styled markdown under a file-watcher event loop. In net terms the 1,572-line Go server and 2,600-plus lines of Svelte became ~700 lines of C and ~440 of Go, across five releases (v0.11.0–v0.15.0).

## Highlights

- **Six socket subcommands collapse to one MCP tool** — `cwork(task, cwd, model?)` over streamable HTTP, ending caller-side socket lifecycle management. ([2026-03-15](../../reports/weekly-report-2026-03-15.md))
- **Self-warming pool with shadow auto-discovery** — each dispatch spawns its replacement, and the caller's transcript is found from its working directory rather than registered by hand. ([2026-03-15](../../reports/weekly-report-2026-03-15.md))
- **Svelte dashboard with live log streaming** — SSE-driven session tree, worker status and xterm.js ANSI rendering, landed in a single ~4,000-line commit. ([2026-03-15](../../reports/weekly-report-2026-03-15.md))
- **Go to C: 15 MB to 35 KB** — a streaming JSON emitter, `.incbin`-embedded guide and pthread dispatch in ~700 lines of C. ([2026-03-22](../../reports/weekly-report-2026-03-22.md))
- **Stateless broker (v0.14.0)** — shadow context, worker pool and transcript discovery deleted once fresh-spawn proved fast enough to make pooling unjustified. ([2026-03-22](../../reports/weekly-report-2026-03-22.md))

## Standouts

- **Protocol simplification as the whole feature** — going from a six-subcommand Unix-socket protocol to a single `cwork` tool call is the entire week's architectural argument, and it left callers with no lifecycle to manage. ([2026-03-15](../../reports/weekly-report-2026-03-15.md))
- **Self-warming beats pre-warming** — dispatching a worker spawns its own replacement, so pool depth is maintained with no external orchestration and no cold-start hole on the first request. ([2026-03-15](../../reports/weekly-report-2026-03-15.md))
- **An MCP stdio frontend is a JSON-to-process bridge** — that observation collapsed a 15 MB Go binary with a 1,572-line `main.go` into a 35 KB statically-linked C binary of ~700 lines, with no GC, no HTTP server and no module system. ([2026-03-22](../../reports/weekly-report-2026-03-22.md))
- **Deleting the pool once it proved unjustified** — v0.14.0 removed shadow context, worker pool and transcript discovery outright, because a fresh Claude process per request was fast enough that pooling bought only complexity. ([2026-03-22](../../reports/weekly-report-2026-03-22.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 2 |
| Commits | 72 |
| Human attention | 6–8 h |
| Traditional equivalent | 0.9–1.4 months |
| Multiplier | ~28–50× |

## Weekly reports

[03-15](../../reports/weekly-report-2026-03-15.md), [03-22](../../reports/weekly-report-2026-03-22.md)

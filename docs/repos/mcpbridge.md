# [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge)

A bimodal MCP framework: a thin C wrapper speaking stdio MCP to the agent, and a persistent Go daemon behind it over a Unix domain socket. It has since narrowed to a session-continuity proxy that keeps an agent's MCP session alive across upstream restarts and binary swaps.

## The journey

mcpbridge was created to resolve a structural tension in MCP servers — they must be light enough to sit on a stdio pipe to Claude Code, yet capable enough to watch files, run schedulers and talk HTTP. The answer splits the two: a **thin C wrapper** handling the stdio protocol with an FSM-based connection lifecycle and JSON-RPC dispatch, and a **long-lived Go daemon** carrying the scheduler, fsnotify watcher and source providers, with `list_changed` notifications on replay so the tool surface can change mid-session — impossible for a static stdio server. v0.1.0 and v0.2.0 shipped with a Homebrew formula, C unit tests, Go tests and an end-to-end reload test.

The next phase generalised the transport and then the front door. The fd-based transport vtable was replaced by a message-oriented one (`poll_fd`/`pump`/`send`) so each transport owns its framing, and `transport_http.c` implemented it against an MCP Streamable HTTP endpoint — POST-only, loopback-only, handling both `application/json` and chunked `text/event-stream` replies, single-threaded with a self-pipe as the stable poll fd. Wiring it through exposed a real structural bug: dispatch had been calling the sink twice per outbound message, harmless on stdio but fatal over HTTP where each call became a separate POST. v0.4.0 stabilised a **connection schema** carrying kind, command or URL, environment, working directory and allowed tools, and v0.5.0 collapsed the CLI tangle into a single **`mcpbridge connect <path>`** front door resolving a named connection from config, making stdio and HTTP orthogonal selections inside the schema rather than surface-level CLI variants. A launchd-visible brew bug from the same window produced a durable lesson: the fix belonged in the formula's service block (`EnvironmentVariables` for `PATH`), not in code.

Hardening followed, and its most interesting content is semantic rather than mechanical. v0.6.0 taught the wrapper to survive an upstream HTTP server forgetting its `MCP-Session-Id` — a stale session now drives `DRAINING → SWAPPING → perform_swap → replay handshake → RUNNING` with a queued replay, and the wrapper must never exit during any of it. v0.7.0 then split the replay path on **at-most-once delivery**: idempotent reads (`tools/list`, `resources/read`, `ping`) replay transparently, while side-effecting `tools/call` requests get a structured `-32002` so the agent decides whether to retry rather than having a mutation silently repeated. v0.8.0 narrowed the project to exactly that job — the daemon retired its brew and GitHub source backends and its polling scheduler, relying on the binary changing on disk to trigger a targeted fsnotify reload while the wrapper keeps the agent's session alive across the swap, with older config fields still loading for compatibility. Elsewhere in the fleet the pattern was adopted and, in one case, deliberately dropped: [mnemo](mnemo.md) vendored mcpbridge for its connection-identity pivot, while [spyder](spyder.md) moved to an HTTP-based MCP server and abandoned the stdio-proxy approach. mcpbridge was among the eight repositories swept by the Fable-5 deep audit, whose two-lens verification **set aside a false positive** against it rather than filing it.

## Highlights

- **Bimodal C wrapper plus Go daemon** — stdio MCP protocol in a thin C front end, business logic in a persistent daemon over a Unix socket, with `list_changed` notifications enabling dynamic tool discovery. ([04-12](../../reports/weekly-report-2026-04-12.md))
- **Message-oriented transport vtable and HTTP backend** — each transport owns its framing; `transport_http.c` speaks MCP Streamable HTTP to loopback with JSON and chunked SSE replies. ([04-26](../../reports/weekly-report-2026-04-26.md))
- **`mcpbridge connect <path>` as the single front door** — connection schema v2 makes stdio and HTTP orthogonal choices in config rather than CLI variants. ([04-26](../../reports/weekly-report-2026-04-26.md))
- **Upstream-restart recovery without exiting** — a stale session id drives drain, swap, handshake replay and queue drain while the agent's session stays alive. ([05-03](../../reports/weekly-report-2026-05-03.md))
- **Cycle-aware replay semantics** — idempotent reads replay transparently; side-effecting `tools/call` gets a structured `-32002` so at-most-once delivery is never violated silently. ([05-03](../../reports/weekly-report-2026-05-03.md))
- **v0.8.0 narrowed to a session-continuity proxy** — source backends and the polling scheduler retired in favour of fsnotify-driven reload on binary change, wire protocol unchanged. ([05-17](../../reports/weekly-report-2026-05-17.md))
- **Survived the Fable-5 audit clean** — the two-lens adversarial method refuted its one candidate finding, a self-unlinking listener, and set it aside rather than filing it. ([07-05](../../reports/weekly-report-2026-07-05.md))

## Standouts

- **A stdio micro-optimisation that had been wrong for years** — dispatch called the sink twice per outbound message, the bytes and then a bare newline. Pipes concatenate, so stdio never noticed; the HTTP backend maps each sink call to a separate POST, so the trailing newline became a one-byte POST rejected with 400. The fix was structural: one sink call per complete message, honouring the message-oriented vtable contract. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))
- **Surviving an upstream that forgets you exist** — when the upstream HTTP server restarts mid-session it loses the wrapper's `MCP-Session-Id` and rejects the next POST. v0.6.0 discriminates 4xx-with-active-session-id as `ESTALE`, queues the message bytes and runs `DRAINING → SWAPPING → perform_swap → replay handshake → RUNNING`, under the invariant that the wrapper must never exit during any of it — exiting is the exact friction it exists to remove. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **Replay split on at-most-once delivery** — v0.7.0 refused to make the recovery path uniformly convenient. Idempotent reads (`tools/list`, `resources/read`, `ping`) replay transparently, while a side-effecting `tools/call` gets a structured `-32002` so the agent decides whether to retry, rather than having a mutation silently repeated on its behalf. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 4 |
| Commits | 42 |
| Human attention | ~3–6 h |
| Traditional equivalent | ~1.0–1.6 months |
| Multiplier | ~25–95× |

## Weekly reports

[04-12](../../reports/weekly-report-2026-04-12.md), [04-19](../../reports/weekly-report-2026-04-19.md), [04-26](../../reports/weekly-report-2026-04-26.md), [05-03](../../reports/weekly-report-2026-05-03.md), [05-17](../../reports/weekly-report-2026-05-17.md), [06-21](../../reports/weekly-report-2026-06-21.md), [07-05](../../reports/weekly-report-2026-07-05.md)

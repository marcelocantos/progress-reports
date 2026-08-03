# Top Achievements

Ranked by meatiness — a combination of impact and degree of difficulty.

Commercial (HMS / minicades / non-`ge` Squz) achievements live in the private sibling: [docs/achievements.md](https://github.com/marcelocantos/progress-reports-private/blob/master/docs/achievements.md).

| # | Description | Meatiness |
|---|-------------|-----------|
| 1 | Built C++ CSP library with M:N scheduler + HTTP/1.1 server | [🥩🥩🥩🥩🥩](../reports/weekly-report-2026-02-22.md) |
| 2 | Built sqlpipe bidirectional replication with TLA+-verified protocol | [🥩🥩🥩🥩🥩](../reports/weekly-report-2026-02-22.md) |
| 3 | Created pigeon E2E-encrypted WebTransport relay (Go/Swift/Kotlin/TS/C) with protogen-driven wire-format codegen across all five languages | [🥩🥩🥩🥩🥩](../reports/weekly-report-2026-03-22.md) |
| 4 | Built rustuml — 18 diagram types matching Java PlantUML; faithful port of PlantUML's activity-layout engine (klimt compression + ftile geometry), Teoz sequence layout, and a second-generation swimlane engine (lane-tagging, per-lane MinMax columns, N-branch fork routing) | [🥩🥩🥩🥩🥩](../reports/weekly-report-2026-06-21.md) |
| 5 | Built sqldeep SQL transpiler with 4-language bindings (C++/Go/Swift/Kotlin); migrating to real LALR(1) parser via vendored deepparser | [🥩🥩🥩🥩🥩](../reports/weekly-report-2026-04-12.md) |
| 6 | Built sqlpipe relational algebra engine with bytecode VM | [🥩🥩🥩🥩🥩](../reports/weekly-report-2026-03-29.md) |
| 7 | Designed protogen generating Go/Swift/C/TLA+/PlantUML from YAML | [🥩🥩🥩🥩🥩](../reports/weekly-report-2026-03-22.md) |
| 8 | Built ge canonical 2D/UI surface + cross-platform IAP (StoreKit + Play Billing 7+) + ship substrate that took multimaze2 to both stores; eradicated bgfx for sokol_gfx as the sole renderer with render-on-demand + a TiltBuggy differential physics oracle; proven a reusable multi-title backend (esfera2, yourworld2); fourth direct-mode platform via Emscripten/WebGL2 (`make web`) with Asyncify-safe native run loop + location-transparent command stream (sensor authority, per-session instances); engine-owned ASTC/ETC2 texture cook-and-load with backend capability probing, and a zero-I/O per-instance frame-metrics ring | [🥩🥩🥩🥩](../reports/weekly-report-2026-07-19.md) |
| 9 | Built csp demand-paged microthread stacks with guard pages; channel hot-path overhaul flattening rendezvous to ~146 ns across processor counts after measuring 16× negative scaling (formal models + papers 33–34), then steal-to-local scheduling worth ~3× on multi-writer alt | [🥩🥩🥩🥩](../reports/weekly-report-2026-07-19.md) |
| 10 | Built csp QUIC transport on ngtcp2 + PicoTLS minicrypto (server, client, FIN, multiplexing) | [🥩🥩🥩🥩](../reports/weekly-report-2026-05-03.md) |
| 11 | Completed csp 5-phase Windows port (kqueue/epoll/IOCP) | [🥩🥩🥩🥩](../reports/weekly-report-2026-03-01.md) |
| 12 | Built cv build tool (formerly mk): content-hash graph + discovered-dependencies model (hard/soft edges, scan/trace, strace) | [🥩🥩🥩🥩](../reports/weekly-report-2026-05-31.md) |
| 13 | Built den dev environment manager with native formula parser; reached v1.0.0 release candidate (trust model, SAT-solver resolution, source-build + taps, perf benchmarks) | [🥩🥩🥩🥩](../reports/weekly-report-2026-06-28.md) |
| 14 | Built jevons fleet cockpit: durable Butler/CEO thread model (process-as-cache) + live token-spend governance with a runaway kill-switch; then fail-closed conversation durability (jevons-owned fsync chat log), ACP MCP attach past Grok's silent trust-gate (`mcp.claudia.json` + toolless-boot oracle), loopback-only bind, embedded web UI for stranger installs, and a chat UI bounded at the materialisation layer (15–20 s to ~1.5 s on a real 4,707-line history) with the journal left intact | [🥩🥩🥩🥩](../reports/weekly-report-2026-07-19.md) |
| 15 | Migrated frozen to 128-bit content hashing, 500x speedup | [🥩🥩🥩🥩](../reports/weekly-report-2026-03-01.md) |
| 16 | Built writ — declared-intent execution: a JSON manifest of what a command will read/write/fetch/exec compiled into a macOS seatbelt profile + manifest-keyed egress proxy + filtered env, with an eslogger drift audit whose declared-vs-actual diff doubles as a prompt-injection detector; hardened by a red-team harness (~18 path-construction escapes) promoted into the standing suite | [🥩🥩🥩🥩](../reports/weekly-report-2026-07-26.md) |
| 17 | Built doit three-level capability broker with audit log + threat model | [🥩🥩🥩🥩](../reports/weekly-report-2026-04-26.md) |
| 18 | Created sqlift C/Go schema migration with cross-language verification + strict-by-default flag bitmask | [🥩🥩🥩🥩](../reports/weekly-report-2026-05-10.md) |
| 19 | Built pigeon LAN upgrade with TLA+ cutover + path-switching + chaos tests | [🥩🥩🥩🥩](../reports/weekly-report-2026-04-19.md) |
| 20 | Built pigeon pure C client library with ngtcp2 QUIC + cross-language crypto vectors | [🥩🥩🥩🥩](../reports/weekly-report-2026-04-19.md) |
| 21 | Built pigeon multi-channel mux relay (N clients on one backend, 4-byte clientTag, AEAD-channel-id) | [🥩🥩🥩🥩](../reports/weekly-report-2026-05-03.md) |
| 22 | Built pageflip meeting-capture with compile-time egress gate + 5 claudia specialists | [🥩🥩🥩🥩](../reports/weekly-report-2026-04-19.md) |
| 23 | Built spyder cross-platform mobile MCP server (go-ios direct binding, self-healing tunnel, MessagePack-RPC app channel); became the sole game-fleet control plane (ged retired); command-stream browser player (same C++ tree → wasm, ~55–60 fps SP2S glass), headless/scripted glass, six-state daemon/device health plane, durable host Starlark explore/collect/regress scripts, and semantic hit-target addressing (id/role, never label) with a per-instance app metrics proxy | [🥩🥩🥩🥩](../reports/weekly-report-2026-07-19.md) |
| 24 | Built mnemo transcript indexer: image+CLIP, live compaction, mTLS federation, Windows MSI; macOS menu-bar navigator, Codex + Grok transcript ingest, SQLite-authorizer read guard, connection-preserving self-upgrade; vault wing MVP (decisions/memories) + in-process plugin system (launch/proxy/facets/MCP bridge) | [🥩🥩🥩🥩](../reports/weekly-report-2026-07-19.md) |
| 25 | Built sawmill Go MCP server: AST git index + semantic blame/bisect + equivalence closure + AST-aware merge + scope classification + AST-anchored concept search; 18-language adapter matrix (parse→rename→add_field MCP smoke with no skip hatch) + `languages` capability cards | [🥩🥩🥩🥩](../reports/weekly-report-2026-07-19.md) |
| 26 | Built bullseye MCP server: portfolio WSJF, git-history ID allocator, GitHub issue mirror; collapsed to a four-tool ledger API with structured envelopes, release-surface + ownership governance, and server-minted (TOCTOU-safe) IDs | [🥩🥩🥩🥩](../reports/weekly-report-2026-07-12.md) |
| 27 | Migrated arrai frozen types to generics across 43 files | [🥩🥩🥩🥩](../reports/weekly-report-2026-03-01.md) |
| 28 | Built sqlpipe changeset filtering with predicate pushdown | [🥩🥩🥩🥩](../reports/weekly-report-2026-03-29.md) |
| 29 | Compiled sqlpipe to WebAssembly via Emscripten | [🥩🥩🥩🥩](../reports/weekly-report-2026-03-15.md) |
| 30 | Wrote IEEE 754 decimal64/128 proposal for Go stdlib | [🥩🥩🥩🥩](../reports/weekly-report-2026-02-22.md) |
| 31 | Built csp dynamic-scoped variables backed by persistent HAMT | [🥩🥩🥩🥩](../reports/weekly-report-2026-02-22.md) |
| 32 | Split ge engine into engine/render/bridge subsystems + v0.1.0 | [🥩🥩🥩🥩](../reports/weekly-report-2026-04-19.md) |
| 33 | Ran a fleet-wide adversarial "Fable-5" security audit (two-lens reachability + invariant verification, default-refuted) across 8 repos, fixing real criticals verify-first — AES-GCM nonce reuse, a SQL read-guard bypass, a file-mutation root-escape | [🥩🥩🥩🥩](../reports/weekly-report-2026-07-05.md) |
| 34 | Built blurter spool-first notification daemon, created and released the same day: durable atomic spool, delivery recorded only on sink confirmation, transient/permanent retry taxonomy, and an MCP surface that keeps no LLM in the delivery path | [🥩🥩🥩](../reports/weekly-report-2026-07-26.md) |
| 35 | Built crosshair Rust convergence-executor daemon with stateless tick loop + Homebrew release CI | [🥩🥩🥩](../reports/weekly-report-2026-05-10.md) |
| 36 | Built cworkers Svelte dashboard with SSE and xterm.js | [🥩🥩🥩](../reports/weekly-report-2026-03-15.md) |
| 37 | Rewrote cworkers from Go to C (15MB to 35KB binary) | [🥩🥩🥩](../reports/weekly-report-2026-03-22.md) |

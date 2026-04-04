# Weekly Progress Report — 2026-03-16…22

## Executive Summary

A 7-day sprint across **11 repositories** spanning a PlantUML Rust port from zero to 12,500 golden tests, a WebTransport relay library with multi-platform clients, healthcare ERP completion through V2 features, a C MCP server rewrite with TUI dashboard, protocol state machine formal verification, H.264 streaming dev mode for a game engine, and a Homebrew-compatible package manager bootstrap. **rustuml** went from initial commit to 18 diagram types with 12,500+ golden test pairs passing against Java PlantUML reference output. **tern** was extracted from jevon into a standalone WebTransport relay library with Go, Swift, Kotlin, and TypeScript clients, deployed to Fly.io. **hms** completed V1 verification, implemented all 19 V2 sub-targets, fixed 821 swallowed exceptions, and added beta feature infrastructure. **cworkers** was rewritten from Go to C (35KB binary) with a Go TUI dashboard. **jevon** added a protocol state machine framework with TLA+ formal verification and a research paper.

**246 commits** | **~+130,000 net lines** (excl. vendored) | **~120-185 person-days traditional equivalent** | **~30-50x multiplier**

### Major Achievements & Innovations

- **PlantUML Rust port from scratch to 12,500+ golden tests** in rustuml: 18 diagram types (sequence, class, activity, state, component, deployment, use case, object, timing, ER, Gantt, mindmap, WBS, JSON, YAML, Salt, network, Ditaa), TIM preprocessor with `!define`, `!include`, `!foreach`, `!function`, themes, skinparams, PNG/PDF/EPS output, embedded Liberation Sans font for accurate text metrics. 159 commits in the gather window but 43 this week — the repo was created on Saturday and saw explosive development
- **WebTransport relay library with 5-platform clients** in tern: extracted from jevon into a standalone library with E2E-encrypted QUIC relay, Go/Swift/Kotlin/TypeScript clients, raw QUIC for native clients alongside WebTransport for browsers, LAN direct connection upgrade, datagram support, deployed to Fly.io with auto Let's Encrypt TLS via [certmagic](https://github.com/caddyserver/certmagic), 106 commits total (42 this week)
- **Protocol state machine framework with formal verification** in jevon: YAML-defined protocol specs compiled to Go, Swift, TLA+, and PlantUML via `protogen`. The PairingCeremony protocol is model-checked by [TLC](https://lamport.azurewebeb.org/tla/tools.html) with bounded state space for exhaustive verification. Research paper on dual-use protocol state machines (570 lines). State-space explosion tamed by bounding channels and using symmetry reduction
- **HMS2 V1 achieved + V2 complete + hardening pass**: 87 convergence targets tracked, V1 verified and double-verified against adversarial audit, all 19 V2 sub-targets (T69.1-T69.19) implemented including geofencing, OR-Tools VRP solver, Google Maps integration, TomTom routing. Fixed 821 swallowed exceptions with `Log` helper, fixed schema mismatches against real database, added beta channel feature flag infrastructure with command palette (Ctrl+K)
- **cworkers C rewrite: 35KB stdio MCP binary** replacing the 15MB Go binary: pure C implementation with streaming JSON emitter, `.incbin`-embedded help text, concurrent dispatch via pthreads, structured JSONL logging. Plus a Go TUI dashboard (`cdash`) using [bubbletea](https://github.com/charmbracelet/bubbletea) + [glamour](https://github.com/charmbracelet/glamour) for markdown rendering, replacing the Svelte web dashboard
- **bgfx migration and scene protocol** in yourworld2/ge: removed all Dawn/WebGPU code, ported globe rendering (mesh loading, cube map, atmosphere, silhouette) to [bgfx](https://github.com/bviber/bgfx), designed a scene display list protocol for streaming render commands to a thin player client, H.264 streaming dev mode with zero-copy Metal texture path via IOSurface
- **den bootstrapped**: Rust reimplementation of Homebrew as a universal development environment manager — consumes existing formulae/bottles, multi-version coinstallation, named environments, background upgrades

### Tough Challenges Overcome

- **821 swallowed exceptions in HMS2** (hms): a systematic audit discovered that every `catch` block in the C# backend silently discarded errors. Created a `Log` helper class and instrumented every single catch block — 821 of them — to log exceptions before handling. Required understanding which exceptions were genuinely expected (e.g. SQL "record not found") vs. masked bugs
- **Schema mismatches from hallucinated column names** (hms): the generated C# models referenced database columns that didn't exist in the real HMS_Demo SQL Server database. Required comparing every model field against actual `sys.columns` metadata and fixing the mapping layer
- **TLC state-space explosion in pairing ceremony** (jevon): the formal TLA+ model of the pairing ceremony protocol had unbounded message channels, causing TLC to explore an astronomically large state space. Tamed by bounding channel capacity to 2, introducing symmetry reduction between the two protocol roles, and writing a research paper documenting the technique
- **VRP reflection hack replaced with real OR-Tools** (hms): the initial vehicle routing solver used C# reflection to invoke Google OR-Tools, which was fragile and untestable. Replaced with a proper OR-Tools integration including distance matrix computation, capacity constraints, and time windows
- **Dawn wire protocol removal** (ge/yourworld2): the Dawn WebGPU wire protocol (1,089-line `WireSession.cpp` + 190-line `WireTransport.cpp`) was deeply integrated into the rendering pipeline. Removing it required careful surgery to preserve the player/server architecture while routing all rendering through bgfx, which has a fundamentally different command submission model

Contributor: Marcelo Cantos

---

## Game Projects

### [squz/yourworld2](https://github.com/squz/yourworld2) — bgfx Migration & Scene Protocol (8 commits)

Continued from last week's parity optimizer and feature waves, now pivoting to renderer infrastructure:

- **H.264 streaming dev mode** (T52): server renders frames, encodes to H.264, streams to a thin player client. Zero-copy Metal texture path via IOSurface — the GPU writes directly to an `IOSurfaceRef` that the H.264 encoder reads without CPU-side copies. `StreamSession` manages the encode pipeline; `VideoDecoder` handles client-side decoding
- **Dawn/WebGPU removal**: deleted the entire Dawn wire protocol in favour of H.264-only streaming for dev mode. Paves the way for the bgfx migration
- **bgfx globe rendering** (T53): ported mesh loading, cube map sampling, atmosphere shader, country silhouette rendering from Dawn/WebGPU to [bgfx](https://github.com/bviber/bgfx). All shaders compiled for Metal via `shaderc`. Carousel, HUD, text rendering, flag atlas, and icon textures ported
- **Scene display list protocol** (T54): designed a command-based protocol where the server emits render commands (create texture, draw mesh, set uniform) and a thin player replays them. Enables streaming rendering to remote clients without shipping the full game engine. Includes reliability tiers (lossless for state, lossy for ephemeral updates) and MSDF text rendering
- **Parity overlay refinement**: three blend modes (difference, side-by-side, overlay) via hardware blending for visual comparison against reference renders

### [squz/ge](https://github.com/squz/ge) (submodule) — bgfx Migration & Streaming (12 commits)

- **bgfx build integration**: vendored bgfx/bx/bimg submodules, built via `Module.mk`, purple clear test confirming Metal rendering works
- **Dawn removal**: deleted `WireSession.cpp` (1,089 lines), `WireTransport.cpp` (190 lines), and all WebGPU artifacts. bgfx is now the sole renderer
- **RenderBackend abstraction** (T54): `BgfxBackend` for real rendering, `SceneWriterBackend` for recording render commands to a scene protocol stream. Round-trip verification tests confirm writer → keyframe/delta → renderer fidelity
- **Scene protocol**: command structs with natural alignment (no `#pragma pack`), writer and renderer implementations, `SceneSession` for server-side session management over the ged relay
- **Tweak system overhaul**: enum, vec2, axis, and colour tweak types; MCP server for programmatic parameter control; dashboard UX with aspect ratio lock
- **H.264 streaming**: `StreamSession` + `VideoDecoder` for encode/stream/decode pipeline, main-thread rendering fix, BGRA capture format

---

## Health Management System

### [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) — V1 Verified, V2 Complete, Hardening (67 commits)

**The biggest effort of the week.** Continued from last week's five-wave implementation, now completing the feature surface and hardening:

- **V1 achievement and verification**: all V1 sub-targets verified and implemented (T1 achieved), then double-verified against an adversarial audit that found additional gaps. Three rounds of fixes until T1 was confirmed stable. Scheduling module with wait lists, time blocks, booking conflicts, and episode lifecycle
- **V2 feature surface** (T69): all 19 V2 sub-targets implemented — T69.1-T69.3 (clinical polish), T69.4/T69.5 (alerts, MDS finder), T69.6 (geofencing), T69.7-T69.10/T69.12 (distance matrix, Google Maps, GPS replay, address validation, VRP solver), T69.11 (travel-together), T69.13/T69.14 (TomTom routing, public transport), T69.16 (pivot grid), T69.17 (schema viewer), T69.19 (worker editor)
- **OR-Tools VRP integration**: replaced a reflection-based hack with real [Google OR-Tools](https://developers.google.com/optimization) integration for vehicle routing — distance matrix computation, capacity constraints, time windows, with Google Maps visualisation
- **Hardening pass**: fixed all 821 swallowed exceptions with `Log` helper instrumentation, fixed all medium-severity audit issues (XSS, CSP headers, magic numbers, async blocking), fixed schema mismatches against real HMS_Demo database, fixed shadow table init and hardcoded staffId references
- **Beta channel infrastructure**: feature flag system with `Beta` attribute, command palette (Ctrl+K) for quick navigation, live operations dashboard, caseload heatmap, patient timeline, patient flow visualisation — all behind beta flags
- **Security**: CSP headers (allowing `unsafe-inline` for SvelteKit hydration), ngrok tunnel support, RBAC error visibility at record level
- **Communication targets**: SMS gateway with reminders (T50), Word document generation (T51), MLLP/VINAH HL7 outbound (T52)
- **Documentation**: comprehensive developer's handbook for team handover, migration strategy document for engineer onboarding
- **Clinical features**: GP register, wound management, SCOTT consent, PMI lookup, referral intake (T46), budget calculation engine (T48) with HCP/NDIS/SAH funds checking
- **87 convergence targets tracked**: comprehensive target sweep with 19 deferrals converted to V2 targets, zero untracked gaps

---

## Libraries & Infrastructure

### [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) — PlantUML Rust Port (43 commits, initial)

A pure Rust reimplementation of [PlantUML](https://plantuml.com) — from bootstrap to 18 diagram types in a single weekend. Single statically-linked binary, no JVM, no Graphviz, no external fonts.

- **18 diagram types**: sequence, class, activity (new syntax), state, component, deployment, use case, object, timing, ER (crow's foot), Gantt, mindmap, WBS, JSON, YAML, Salt (UI wireframes), network (nwdiag), Ditaa (ASCII art). Plus Regex (railroad), DOT, EBNF, git, and board diagram types
- **12,500+ golden test pairs**: oracle test framework comparing Rust-rendered SVGs against Java PlantUML reference output. Compressed from 25,000 golden files into a 4.3MB zstd tarball read in-memory. Tests cover all diagram types with systematic matrix coverage (arrow types, participant types, modifiers, notes)
- **TIM preprocessor**: `!define`, `!include` (with base directory resolution), `!ifdef`/`!ifndef`/`!else`/`!endif`, `!foreach` loops, `!function`/`!procedure`, arithmetic expressions, `while` loops, `!theme` directives. Oracle tests comparing against Java PlantUML preprocessor output
- **Rendering pipeline**: SVG output via custom renderer, PNG via [resvg](https://github.com/nickmunroe/resvg), PDF via [svg2pdf](https://github.com/nickmunroe/svg2pdf), EPS output. Embedded Liberation Sans TTF font for accurate proportional text metrics. [Sugiyama](https://en.wikipedia.org/wiki/Layered_graph_drawing) layout for class diagrams, later replaced with Graphviz for higher-quality layout
- **Style system**: default and modern themes via YAML configuration, `skinparam` parsing and application, `--theme` CLI flag, `--theme-file` for custom YAML themes
- **Creole markup**: bold, italic, underline, monospace, links, trees, tables, nested lists, horizontal rules — rendered into SVG text elements
- **Multi-output modes**: `-pipe` flag for stdin/stdout streaming (12 pipe mode tests), `-tpng`, `-tpdf`, `-teps`, `-tsvg` format selection
- **Architecture**: 6 Rust crates — `rustuml` (CLI), `rustuml-parser` (diagram model + parsers), `rustuml-render` (SVG/PNG/PDF/EPS), `rustuml-layout` (graph layout), `rustuml-oracle` (golden test framework), `rustuml-math` (LaTeX rendering)
- **v0.2.0 and v0.3.0 released** with CI and release workflow

### [marcelocantos/tern](https://github.com/marcelocantos/tern) — WebTransport Relay Library (42 commits, initial)

Extracted from jevon into a standalone library: a WebTransport relay that enables connections between devices where the backend sits on a private network with no ingress.

- **WebTransport relay**: Go server using [quic-go](https://github.com/lucas-clemente/quic-go) WebTransport, deployed to [Fly.io](https://fly.io/) with automatic [Let's Encrypt](https://letsencrypt.org/) TLS via [certmagic](https://github.com/caddyserver/certmagic). Both reliable streams and unreliable datagrams
- **Multi-platform clients**: Go client (root package), Swift client via Network.framework QUIC (`TernRelay`), Kotlin client with Gradle wrapper, TypeScript/Web client with E2E crypto
- **Multi-transport architecture** (T5): `Conn` abstraction supporting WebSocket relay, WebTransport relay, and LAN direct connection. Automatic upgrade from relay to direct LAN when devices are on the same network. Transport-agnostic encrypted mode
- **Raw QUIC protocol**: for native clients (Swift, Kotlin, Go) alongside WebTransport for browsers. Both use the same E2E encryption layer
- **E2E encryption**: X25519 ECDH key exchange, AES-256-GCM with monotonic counter nonces and directional HKDF-SHA256 key derivation. Datagram/lossy mode added across all platforms (T8.2). MitM detection via 6-digit confirmation code
- **Channel API** (T12): streaming channels and datagram channels with comprehensive tests
- **Pairing persistence**: `PairingRecord` and `WithInstanceID` for persistent device pairing across reconnects
- **Testing**: live E2E tests against tern.fly.dev, local tests, parameterised test infrastructure (`forEachRelay`), packet loss simulation, latency and throughput benchmarks. Swift 6/6 E2E tests, Kotlin E2E tests, TypeScript Playwright E2E tests
- **Code generation**: `protogen` generates Go, Swift, Kotlin, TypeScript, TLA+, and PlantUML from YAML protocol specs
- **7 releases** (v0.1.0 through v0.7.0) with CI, release workflow, STABILITY.md, audit findings addressed across 4 rounds

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Request/Response & SIGPIPE Fix (6 commits)

Continued from last week's processor reuse and research papers:

- **Request/response primitives**: `requester<Req,Resp>` and `responder<Req,Resp>` channel types for typed RPC over CSP channels, with a pipe operator (`|`) for composing request/response chains. Research paper on channels-as-interfaces design (Paper 15, 269 lines)
- **Linux SIGPIPE fix** (T6): `SIGPIPE` on Linux was crashing the runtime. Fixed by ignoring the signal at startup with `signal(SIGPIPE, SIG_IGN)`. Marked T6 achieved
- **v0.4.0 release**: includes request/response primitives, SIGPIPE fix, and updated agent guide

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Chain Replication & Predictions (22 commits)

Continued from last week's Wasm build and Go wrapper, now adding replication topologies and optimistic UI:

- **Chain replication**: `Relay` class for source → relay → sink replication chains, enabling multi-hop data propagation. Fan-out tests: one Master broadcasting to N Replicas. Sequence gap rejection for consistency
- **Prediction API**: savepoint-based optimistic local updates — the client applies mutations immediately, wrapping them in a SQLite savepoint that rolls back if the server rejects the change. Enables responsive UI without waiting for round-trip confirmation
- **Fast reconnect** (protocol v6): skip full diff sync when sequence numbers match after reconnect, reducing reconnection latency to near-zero for brief disconnections
- **Explicit PeerRole**: breaking change replacing implicit server detection with explicit `PeerRole::Server`/`PeerRole::Client` designation, fixing a SIGSEGV in stress tests where the wrong role was inferred
- **Subscription fixes**: `subscribe()` now returns an ID and defers evaluation until the peer reaches `Live` state, fixing subscriptions that silently failed after diff sync
- **Swift package**: `SyncPeer` Swift wrapper with bundled C/C++ sources for direct Swift Package Manager consumption
- **Go module bundling**: C/C++ sources bundled directly in the Go module for standalone `go get` without external dependencies
- **3 releases**: v0.12.0, v0.13.0, v0.14.0

---

## Tooling

### [marcelocantos/cworkers](https://github.com/marcelocantos/cworkers) — C Rewrite & TUI Dashboard (35 commits)

Continued from last week's MCP server, now rewritten from Go to C with a companion TUI:

- **C MCP server** (`cwork`): 35KB statically-linked binary replacing the 15MB Go binary. Pure C with streaming JSON emitter, `.incbin`-embedded `help-agent.md`, concurrent dispatch via pthreads (one thread per `cwork` call). Structured JSONL logging with per-worker log files and activity log
- **Stateless broker architecture** (v0.14.0): removed shadow context, worker pool, and transcript discovery — the MCP server is now a thin dispatcher that spawns Claude processes on demand. Simpler, more reliable, no warm pool to manage
- **cdash TUI dashboard**: initially written in Rust with [ratatui](https://github.com/ratatui-org/ratatui), then rewritten in Go with [bubbletea](https://github.com/charmbracelet/bubbletea) + [glamour](https://github.com/charmbracelet/glamour) for markdown rendering. Sidebar shows worker IDs with model prefix (O/S/H for Opus/Sonnet/Haiku), transcript panel renders worker output as styled markdown. Event-driven updates via file watcher, active/all view toggle
- **Legacy removal**: deleted the Go server (`main.go`, 1,572 lines), Svelte dashboard (2,600+ lines of Svelte/CSS/JS), Go module files. All replaced by ~700 lines of C and ~440 lines of Go
- **5 releases**: v0.11.0 through v0.15.0

### [marcelocantos/jevon](https://github.com/marcelocantos/jevon) — Protocol Framework & Formal Verification (6 commits)

Continued from last week's server-driven Lua UI, now adding formal foundations:

- **Protocol state machine framework** (`protogen`): YAML-defined protocol specifications compiled to Go (state machine + message types), Swift (protocol handler), TLA+ (formal model), and PlantUML (sequence diagram). The `PairingCeremony` protocol — a 4-message handshake with key exchange, confirmation code display, and mutual verification — is the first protocol defined in this framework
- **TLA+ formal verification**: the PairingCeremony TLA+ spec is model-checked by [TLC](https://lamport.azurewebeb.org/tla/tools.html) with bounded state space. Initially hit state-space explosion from unbounded message channels; tamed by bounding channel capacity to 2 messages and exploiting protocol symmetry
- **Research paper**: "Dual-Use Protocol State Machines" (570 lines) — describes the approach of generating both executable code and formal models from the same YAML source, ensuring the verified model matches the implementation
- **State-space explosion write-up**: 127-line paper on bounding techniques for TLC verification, with the PairingCeremony as a case study. T15 achieved
- **Relay integration**: wired tern relay into jevond for voice call support with interruption handling, QR code scanning updated for relay connection

### [marcelocantos/den](https://github.com/marcelocantos/den) — Homebrew Replacement Bootstrap (4 commits, initial)

A new project: Rust reimplementation of Homebrew as a universal development environment manager.

- **Bootstrap**: Cargo project setup, CLI with `install`/`list`/`use`/`search`/`info`/`deps`/`cleanup` commands, Homebrew formula index consumption, content-addressed bottle cache
- **Rename**: started as "rubrew", renamed to "den" to reflect the broader vision — not just Ruby/Homebrew replacement but a universal development environment manager
- **Auto-upgrade**: unattended version switching with configurable maintenance windows
- **Architecture**: consumes existing Homebrew ecosystem (formulae, bottles, taps) without requiring rebuilds, with multi-version coinstallation and named environments

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 11 (9 with substantial development) |
| Total commits | 246 |
| Total lines added | +1,130,291† |
| Total lines removed | -61,532 |
| Net new lines | +1,068,759† |
| Net new lines (excl. vendored/generated) | ~+130,000 |
| File changes | 1,478 |
| New files created | 1,209 |
| Languages | Rust, Go, C, C++, C#, Swift, Kotlin, TypeScript, Svelte, Lua, WGSL, TLA+, Python, SQL, Markdown |
| Contributors | 1 (Marcelo Cantos) |

*†sqlpipe bundles sqlite3 sources for Go and Swift (~624k lines). jevon vendors Lua 5.1.5 and sqlite3 (~261k lines). rustuml includes ~636 golden test SVG files.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | 67 | 451 | +94,056 | -36,416 | +57,640 |
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | 43 | 848† | +19,545 | -545 | +19,000 |
| [marcelocantos/tern](https://github.com/marcelocantos/tern) | 42 | 180 | +13,602 | -3,255 | +10,347 |
| [marcelocantos/cworkers](https://github.com/marcelocantos/cworkers) | 35 | 143 | +11,781 | -11,673 | +108 |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 22 | 134 | +626,908 | -551 | +626,357* |
| ge (submodule) | 12 | 85 | +7,117 | -7,820 | -703 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 8 | 75 | +5,799 | -583 | +5,216 |
| [marcelocantos/jevon](https://github.com/marcelocantos/jevon) | 6 | 208 | +347,019 | -685 | +346,334* |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 6 | 30 | +981 | -146 | +835 |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 4 | 19 | +3,198 | -100 | +3,098 |

*\*Includes vendored dependencies (sqlite3, Lua 5.1.5).*
*†Includes ~636 golden test SVG files.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | ~12,500+ | Golden test pairs against Java PlantUML, format-parameterised smoke tests, matrix tests, pipe mode tests |
| [marcelocantos/tern](https://github.com/marcelocantos/tern) | ~92 | E2E crypto tests (Go, Swift, Kotlin, TypeScript), relay tests, live Fly.io tests, benchmarks, packet loss simulation |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~31 | Chain replication, fan-out, prediction API, fast reconnect, subscription fixes |
| [marcelocantos/jevon](https://github.com/marcelocantos/jevon) | ~20 | Protocol state machine tests, TLA+ model checking, crypto tests |
| [marcelocantos/cworkers](https://github.com/marcelocantos/cworkers) | ~15 | Integration tests, unknown method handling |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~5 | RPC request/response tests, swap tests |
| **Total** | **~12,663+** | |

---

## Ideas & Innovations

### Oracle-Driven Diagram Rendering ([rustuml](https://github.com/marcelocantos/rustuml))

Porting a complex rendering tool like PlantUML by hand would be a multi-year effort — the Java codebase is enormous and the rendering rules are undocumented, embedded in procedural code. rustuml takes a different approach: **build a golden test oracle that compares Rust-rendered SVGs against Java PlantUML reference output, then iterate rapidly against that oracle**. The test framework generates test inputs from a combinatorial matrix (diagram type x feature x modifier), renders them with both Java PlantUML and the Rust port, and compares the SVG output. This turns an impossible specification problem into a measurable convergence problem — at 12,500+ passing golden pairs, the Rust port is demonstrably compatible. The compressed golden archive (4.3MB zstd tarball, read in-memory) makes the test suite fast despite the massive test count.

### Dual-Use Protocol State Machines ([jevon](https://github.com/marcelocantos/jevon))

Protocol implementations and their formal models typically live in separate worlds — the implementation is handwritten code, the model is a TLA+ spec, and nothing guarantees they correspond. jevon's `protogen` tool **generates both executable code (Go, Swift) and formal models (TLA+) from the same YAML protocol specification**. The PairingCeremony protocol — a 4-message handshake with X25519 key exchange and mutual confirmation — is defined once in YAML and compiled to a Go state machine, a Swift protocol handler, a TLA+ spec for model checking, and a PlantUML sequence diagram. Changes to the protocol automatically update both the implementation and the formal model, making verification a continuous property rather than a one-time exercise.

### Savepoint-Based Optimistic Updates ([sqlpipe](https://github.com/marcelocantos/sqlpipe))

Optimistic UI — applying mutations immediately and rolling back on server rejection — is typically implemented with application-level undo logic that must mirror every possible mutation. sqlpipe's prediction API takes a simpler approach: **wrap optimistic mutations in a SQLite savepoint, so rollback is a single `ROLLBACK TO` regardless of mutation complexity**. The client applies the mutation inside a savepoint, immediately reflects the change in the UI, and waits for the server's verdict. On acceptance, the savepoint is released; on rejection, it rolls back atomically. This eliminates the need for per-mutation undo logic and guarantees consistency — the rollback undoes exactly what was applied, even for complex multi-table mutations.

### Chain Replication for SQLite Sync ([sqlpipe](https://github.com/marcelocantos/sqlpipe))

Bidirectional sync between two SQLite peers is useful, but real-world topologies involve intermediate nodes — edge caches, regional relays, hierarchical aggregation. sqlpipe's `Relay` class enables **multi-hop chain replication (source → relay → sink)** where intermediate nodes receive changesets, apply them locally, and forward them downstream. Combined with fan-out (one Master broadcasting to N Replicas) and sequence gap rejection, this creates a flexible replication topology that scales from simple two-peer sync to complex distribution networks. The relay is a thin passthrough — it applies the same changeset logic as any peer, so it inherits all the consistency guarantees of the base protocol.

### 35KB MCP Server in C ([cworkers](https://github.com/marcelocantos/cworkers))

The cworkers MCP server was rewritten from Go (15MB binary with 1,572-line `main.go`) to C (35KB binary, ~700 lines). The key insight is that **an MCP stdio frontend is essentially a JSON-to-process bridge** — it reads JSON-RPC from stdin, spawns a Claude process with the task, and streams the result back as JSON-RPC on stdout. This doesn't need a garbage collector, an HTTP server, or a module system. The C implementation uses a streaming JSON emitter (no intermediate string allocation), `.incbin` for embedding the agent guide at compile time, and pthreads for concurrent dispatch. The stateless architecture (v0.14.0) eliminated the warm worker pool entirely — each request simply spawns a fresh Claude process, which turns out to be fast enough that pooling adds complexity without measurable benefit.

### WebTransport with Automatic LAN Upgrade ([tern](https://github.com/marcelocantos/tern))

Cloud relays add latency — typically 50-200ms round-trip even to nearby servers. When two devices are on the same LAN, this latency is unnecessary. tern implements **automatic transport upgrade from relay to direct LAN connection** without application-level changes. The initial connection goes through the Fly.io WebTransport relay. Once established, both peers probe for LAN reachability. If found, the connection transparently upgrades to a direct LAN path, dropping latency to sub-millisecond. The `Conn` abstraction makes this invisible to the application — it sees the same `Send`/`Recv` interface regardless of the underlying transport. The upgrade is seamless because the E2E encryption layer operates above the transport, so switching transports doesn't require re-keying.

---

## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **rustuml** | 30-45 | Rust port of a complex Java rendering tool — 18 diagram parsers, TIM preprocessor with loops/functions/arithmetic, SVG/PNG/PDF/EPS output, embedded font metrics, Sugiyama→Graphviz layout pivot, 12,500+ golden test oracle framework with zstd-compressed reference archive |
| **hms** | 25-35 | V1 verification against adversarial audit, 19 V2 sub-targets including OR-Tools VRP solver, Google Maps integration, geofencing, 821 exception fixes requiring per-catch-block analysis, beta feature flag infrastructure, schema mismatch debugging against real SQL Server |
| **tern** | 20-30 | WebTransport relay with Go/Swift/Kotlin/TypeScript clients, E2E crypto (X25519 + AES-256-GCM) on 4 platforms, QUIC datagram support, certmagic Let's Encrypt integration, LAN direct connection upgrade, code generation from YAML protocol specs, Fly.io deployment |
| **cworkers** | 8-12 | Go-to-C rewrite of MCP server with streaming JSON, Rust-to-Go TUI rewrite, concurrent dispatch with pthreads, structured JSONL logging, 5 releases |
| **sqlpipe** | 8-12 | Chain replication topology, savepoint-based prediction API, fast reconnect protocol, subscription lifecycle fixes, Swift/Go module bundling with C++ sources, 3 releases |
| **jevon** | 6-10 | Protocol state machine framework generating Go/Swift/TLA+/PlantUML, TLC formal verification with state-space bounding, two research papers, relay integration |
| **yourworld2 + ge** | 8-12 | bgfx renderer migration from Dawn, H.264 streaming with zero-copy Metal textures, scene protocol design with reliability tiers, Dawn wire protocol removal surgery |
| **csp** | 3-5 | Request/response channel primitives, channels-as-interfaces design paper, SIGPIPE fix |
| **den** | 2-3 | Homebrew-compatible package manager bootstrap in Rust, CLI scaffolding, formula index consumption |

### The Diversity Tax

Specialisms exercised this week:

- Rust systems programming (PlantUML port with SVG rendering, font metrics, graph layout)
- QUIC/WebTransport protocol engineering across Go, Swift, Kotlin, and TypeScript
- Multi-platform cryptography (X25519, AES-256-GCM on 4 platforms with consistent APIs)
- C systems programming (MCP server, streaming JSON, `.incbin`, pthreads)
- C++ game engine architecture (bgfx migration, scene protocol, H.264 encoding)
- [TLA+](https://lamport.azurewebeb.org/tla/home.html) formal verification (state-space bounding, symmetry reduction)
- C#/ASP.NET Core with SQL Server, Dapper, RBAC, SSE streaming
- [SvelteKit](https://svelte.dev/) SPA with deep linking, feature flags, command palette
- Healthcare domain modelling (CHSP/NDIS/SAH funding, OR-Tools VRP, HL7 MLLP)
- Go TUI development with [bubbletea](https://github.com/charmbracelet/bubbletea) and [glamour](https://github.com/charmbracelet/glamour)
- SQLite replication protocol design (chain replication, savepoints, sequence gaps)
- [PlantUML](https://plantuml.com) diagram format reverse-engineering (18 types, preprocessor, themes)
- Metal GPU programming (IOSurface zero-copy textures, bgfx shader compilation)
- Swift/iOS development (Lua runtime, QR scanning, relay connectivity)

No single engineer holds expertise in Rust SVG rendering, QUIC/WebTransport across 4 platforms, C MCP servers, bgfx game engine migration, TLA+ formal verification, and healthcare ERP development simultaneously.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **rustuml** (43 commits) | 4-6 | Architecture decisions (6-crate structure, oracle-driven approach), golden test strategy, Graphviz migration decision, reviewing SVG output quality |
| **hms** (67 commits) | 5-7 | V2 target prioritisation, OR-Tools integration review, beta feature selection, adversarial audit response strategy, database schema investigation |
| **tern** (42 commits) | 4-6 | Library extraction architecture, WebTransport vs WebSocket decision, LAN upgrade protocol design, Fly.io deployment, multi-platform API surface review |
| **cworkers** (35 commits) | 3-4 | C rewrite decision, stateless architecture insight, cdash UX design, Go vs Rust for TUI |
| **sqlpipe** (22 commits) | 2-3 | Chain replication topology design, prediction API semantics, protocol v6 reconnect strategy |
| **Other** | 4-6 | jevon protocol framework design, TLA+ state-space bounding, csp request/response design, yourworld2/ge bgfx strategy, den concept |
| **Total** | **~22-32 hours** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | Ramp-up cost |
|---------|------------|-----------------|--------------|
| rustuml | 30-45 | 50-70 | +15 (Rust SVG rendering, PlantUML format internals, font metrics, graph layout algorithms) |
| hms | 25-35 | 40-55 | +10 (C#/ASP.NET, SvelteKit, SQL Server, CHSP/NDIS, OR-Tools, HL7) |
| tern | 20-30 | 35-50 | +12 (QUIC/WebTransport, multi-platform crypto, certmagic, Swift Network.framework, Kotlin QUIC) |
| cworkers | 8-12 | 12-18 | +4 (C MCP protocol, streaming JSON, bubbletea TUI, pthreads) |
| sqlpipe | 8-12 | 12-18 | +4 (SQLite replication, savepoint semantics, chain replication, Swift/Go module bundling) |
| jevon | 6-10 | 10-16 | +5 (TLA+ model checking, protocol code generation, state-space bounding) |
| yourworld2 + ge | 8-12 | 12-18 | +5 (bgfx, Metal textures, H.264 encoding, scene protocol design) |
| csp | 3-5 | 5-8 | +2 (CSP channel primitives, typed RPC design) |
| den | 2-3 | 3-5 | +2 (Homebrew internals, formula/bottle parsing) |
| **Subtotal** | **110-164** | **179-258** | **+59** |
| Context-switching tax (30%) | | +54-77 | |
| **Total** | | **233-335** | |

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~120-185 person-days (6-9 months)** |
| Specialist team (traditional) | **~70-110 person-days (3.5-5.5 person-months)** |
| Actual human effort this week | **~22-32 hours (~3-4 person-days)** |
| **Multiplier vs. generalist** | **~30-50x** |
| **Multiplier vs. specialist team** | **~18-30x** |

The multiplier is highest for rustuml, where building a PlantUML-compatible renderer from scratch with 18 diagram types and 12,500+ golden tests in a single weekend would be inconceivable for a solo developer — Java PlantUML has been developed for over 15 years. The tern extraction is similarly extreme: a multi-platform WebTransport relay with E2E crypto on 4 platforms (Go, Swift, Kotlin, TypeScript), QUIC datagram support, LAN upgrade, and Fly.io deployment in under a week. The multiplier is lowest for the jevon protocol work (research papers and TLA+ formal verification require human reasoning about protocol semantics) and the csp request/response design (channel primitive API design is fundamentally a creative act). The human contribution concentrated on architectural invention (oracle-driven rendering, dual-use protocol state machines, savepoint-based predictions, stateless MCP architecture), domain expertise (healthcare target prioritisation, protocol security properties), and strategic decisions (C vs Go, bgfx vs Dawn, extracting tern from jevon).

# Weekly Progress Report — 2026-03-23…29

## Executive Summary

A 7-day sprint across **9 repositories** spanning a C++ CSP library's M:N scheduler migration with TLA+ formal verification, a PlantUML Rust port reaching SVG parity against the Java reference, a Homebrew-replacement rewritten from Rust to C++ with 5 audit rounds, a SQL replication library with predicate-aware subscriptions and a bytecode VM, a WebTransport relay achieving 97.5% protocol coverage with fault injection testing, a voice-enabled AI orchestrator with Grok Realtime integration, and a game engine's scene protocol carrying full bgfx rendering over the wire. **csp** completed a sweeping M:N-only scheduler migration (663/663 tests passing), closing 5 convergence targets including TLA+ verification for 3 unmodeled protocols. **rustuml** rewrote 6 diagram renderers for exact PlantUML SVG parity using Java AWT binary-fraction font metrics, reaching 12,500+ golden test passes. **den** was rewritten from Rust to C++ with an independent package store, source builds, and Homebrew-free operation. **sqlpipe** gained a relational algebra engine with predicate pushdown, a bytecode VM for changeset filtering, and TLA+-verified convergence loop replication over tern.

**574 commits** | **~+96,000 net lines** (excl. vendored/golden) | **~100-160 person-days traditional equivalent** | **~25-45x multiplier**

### Major Achievements & Innovations

- **M:N-only scheduler with quiescence protocol** in csp: migrated the entire test suite (663 tests) to M:N-only scheduling, eliminating the 1:1 fallback. Added a `quiescence_scope` primitive for deterministic testing of concurrent processes, a `fake_clock` quiescence hook for automatic time advancement, and TLA+ specs for the quiescence scope protocol — closing 5 convergence targets (T2, T5, T8, T9, T10, T11) in a single week
- **Exact PlantUML SVG parity** in rustuml: rewrote 6 diagram renderers (class, state, component, activity, sequence, deployment) to produce SVGs matching Java PlantUML output to the pixel. Extracted exact Java AWT binary-fraction font metrics from golden SVGs. Oracle test framework extracts layout positions from reference SVGs and compares structurally, bypassing IEEE 754 precision differences
- **Predicate-aware SQL subscription invalidation** in sqlpipe: built a relational algebra engine that analyses SQL subscriptions, performs predicate pushdown and transitive propagation through equijoins, and compiles predicates to a bytecode VM for changeset filtering. Column relevance tracking skips irrelevant UPDATE notifications. Three-valued NULL semantics for correct SQL evaluation
- **C++ rewrite of den** with independent package store: rewrote the Homebrew replacement from Rust to C++ with spdlog/nlohmann/libarchive/libcurl, independent store at `~/.den/`, source builds that parse Homebrew formulae and compile from source, bundled Ruby for formula evaluation without requiring Homebrew. 5 rounds of adversarial security audits with 100+ findings fixed
- **TLA+-verified convergence loop** in sqlpipe: formal model of the stateless diff-sync replication protocol, end-to-end tested through a tern relay. Transport adapter for dual-channel replication (reliable streams + unreliable datagrams)
- **NetworkBackend: bgfx RendererContextI over the wire** in ge/yourworld2: patched bgfx to support custom renderer backends, implemented `NetworkBackend` that serialises full bgfx frame submissions (resources, uniforms, draw calls) for remote playback on a Metal backend — the scene player renders the full globe, carousel, and HUD remotely via the ged relay
- **Grok Realtime voice bridge** in jevon: integrated xAI's Grok Realtime API for voice I/O with adaptive local VAD, streaming text display of spoken responses, and WKWebView-based native UI via a Swift `JevonBridge` transport abstraction

### Tough Challenges Overcome

- **Quiescence gap in fake_clock hook** (csp): the M:N scheduler's quiescence detection had a gap where `fake_clock` could advance time before all imp processes had entered a waiting state, causing spurious wakeups and test flakes. Required a yield+recheck protocol in the main loop hook and TLA+ modelling of the fake_clock/quiescence interaction to prove correctness
- **IEEE 754 precision in golden test comparisons** (rustuml): Java PlantUML uses Java AWT font metrics that produce coordinates as exact binary fractions (e.g. 13.6875 = 13 + 11/16). Rust's f64 arithmetic introduces rounding that differs by the least significant bit. Solved by extracting oracle positions from reference SVGs and comparing with structural tolerance rather than string equality
- **net::listen fcontext terminate bug** (csp): the TCP accept loop investigation uncovered a fundamental interaction between fcontext coroutine termination and the listen socket lifecycle. TLA+ model for the listen lifecycle identified the HAMT leak root cause — channels were not being cleaned up when a listening socket was closed while accept coroutines were suspended
- **Scene protocol serialisation alignment** (ge): bgfx's internal `UniformCacheFrame` and `SubmitFrame` structures use platform-specific alignment and packing. Serialising them for network transport required flattening container types (e.g. `TextureCreate`), fixing `initCaps()` timing (must run after `bgfx::init()`), and handling Metal-specific uniform buffer serialisation
- **den Rust-to-C++ migration with audit hardening** (den): rewriting the entire package manager from Rust to C++ while simultaneously running 5 rounds of adversarial audits. Each round exposed new vulnerability classes: slug decode corruption, symlink path traversal, hardlink tar extraction attacks, settings reset via config corruption. Required atomic writes for critical paths and careful TOCTOU avoidance
- **Grok Realtime API schema mismatch** (jevon): xAI's Grok Realtime API uses different event names (`output_audio` not `audio`) and different session configuration schema than documented. Required empirical debugging of the WebSocket protocol to match the actual API behaviour

Contributor: Marcelo Cantos

---

## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — M:N Migration & Formal Verification (61 commits)

**The biggest effort of the week.** Continued from last week's Tier D combinators and Windows TSan clean pass, now completing a sweeping M:N-only scheduler migration:

- **M:N-only scheduler** (T11): transformed the entire test suite to use `csp::run()` exclusively — no more 1:1 scheduling fallback. 15 test files rewritten, 663/663 tests passing. Required making `RunStats` counters atomic, relaxing `Share` test assertions for M:N latest-value semantics, and fixing race conditions in `SpawnMany`, `ManyChannelPairs`, and `fanout` tests
- **Quiescence scope**: added `quiescence_scope` for deterministic testing of concurrent M:N processes. Auto-enrolls imps, provides a `binding()` API for fake_clock integration, supports scoped lifetime with RAII cleanup. Thread-safe implementation with `quiescence_scope` fallback for non-scoped contexts
- **fake_clock auto-advance**: migrated from explicit `fc.run()` to automatic advancement via a main_loop quiescence hook. When all imps are quiescent, the runtime advances the fake_clock to the next scheduled event. Inline construction via `csp::clock = fake_clock{}`
- **TLA+ formal verification** (T5): 3 new spec pairs — `BlockingPoolLifecycle`, signal pipe lifecycle, surplus processor reset protocol. Plus specs for quiescence scope and fake_clock/quiescence interaction. Paper 18: quiescence scope gap analysis
- **Networking I/O** (T3.1): `net::listen` and `net::dial` ergonomic wrappers with TCP half-close support. Investigation uncovered fcontext terminate bug and HAMT leak via TLA+ listen lifecycle model. Paper 17 updated with findings
- **Signal safety** (T8): audited signal handling for async-signal-safety, fixed fd-reuse race in signal handler, added cleanup at exit
- **Targets achieved**: T2 (Tier D combinators), T5 (TLA+ for unmodeled protocols), T8 (signal safety), T9 (TSan clean), T10 (shutdown crashes). v0.5.0 released

### [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) — PlantUML SVG Parity (184 commits)

Continued from last week's 12,500 golden tests, now pursuing exact SVG output parity with Java PlantUML:

- **6 renderer rewrites for SVG parity**: class, state, component, activity, sequence, and deployment diagram renderers rewritten to produce SVGs matching Java PlantUML output. v0.5.0 released as the "PlantUML parity" milestone
- **Java AWT font metrics**: extracted exact binary-fraction font metrics from Java AWT (e.g. character widths as n/16 fractions). Replaced truncated floating-point metrics with exact values — the key insight that unlocked coordinate parity
- **Oracle test framework**: structural SVG comparison that extracts element positions, text content, and layout relationships from both reference and generated SVGs. Bypasses IEEE 754 precision differences by comparing at the layout level rather than string level. Extended to state, component, deployment, and use case diagrams
- **Sequence renderer overhaul**: activation bars with colours, return message rendering with arrow tracking, self-messages (loopback), participant type shapes, autonumber, notes (hnote/rnote/across), dividers, dynamic per-message vertical spacing, group frames with proper extent calculation. 530+ golden test passes for sequence diagrams alone
- **Class diagram precision**: glyph paths, separator layout, member width with visibility modifiers, entity colours, stereotype rendering, 12pt font metrics. Moved from 726 to 967+ golden passes through incremental fixes
- **New diagram support**: [Archimate](https://www.archimatetool.com/) diagrams, [OpenIconic](https://useiconic.com/open) icon rendering for `<&name>` syntax, `[[url]]` link support
- **Graphviz integration**: replaced layout-rs with [Graphviz](https://graphviz.org/) for higher-quality class diagram layout
- **TIM preprocessor rewrite**: arithmetic expressions, `while` loops, enhanced `!define`/`!function`/`!procedure` support
- **v0.3.0, v0.4.0, and v0.5.0 released** with CI and release workflows

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Predicate VM & Convergence Loop (34 commits)

Continued from last week's peer subscribe/unsubscribe, now building the intelligent subscription layer:

- **Relational algebra engine**: SQL subscription queries analysed into a relational algebra representation. Predicate pushdown through joins, predicate splitting for multi-table subscriptions, join normalisation for canonical form. Transitive predicate propagation through equijoins — if `a.x = b.x` and `a.x > 5`, infer `b.x > 5`
- **Bytecode VM**: predicates compiled to a stack-based bytecode VM with `LoadCol`, comparison, logical, and `InList` operators. Evaluates changesets against subscription predicates without SQL parsing at runtime. Comprehensive predicate tests
- **Column relevance tracking**: subscription analysis identifies which columns each subscription cares about. `UPDATE` changesets affecting only irrelevant columns are skipped entirely, reducing unnecessary invalidation
- **SQL semantics**: OR-to-InList optimisation, `NOT IN` support, three-valued NULL semantics matching SQL standard behaviour
- **Convergence loop**: stateless diff-sync protocol — peers exchange bucket hashes, identify divergent buckets, and reconcile without a handshake phase. TLA+ formal model of the protocol. End-to-end test through a [tern](https://github.com/marcelocantos/tern) relay
- **Transport adapter**: dual-channel replication over tern — reliable streams for changeset delivery, protocol version and schema fingerprint in `BucketHashesMsg`
- **API simplification**: removed `Delivery`, `OutMessage`, and `PeerOutMessage` — messages are just messages. Vendored [liteparser](https://github.com/sqliteai/liteparser) for SQL AST analysis
- **v0.15.0, v0.16.0, and v0.17.0 released**

### [marcelocantos/tern](https://github.com/marcelocantos/tern) — Coverage, Fault Injection & LAN Upgrade (87 commits)

Continued from last week's multi-platform extraction, now hardening and extending:

- **Test coverage push**: root package from 78% to ~89%, crypto from 81% to 91.5%, protocol from 75.6% to 97.5%. Comprehensive tests for channels, datagrams, errors, and lifecycle. Parameterised test infrastructure (`forEachRelay`) for simultaneous local + live relay testing
- **Fault injection**: `faultproxy` — a transparent UDP proxy for injecting packet loss, delays, and corruption. Sequence-aware injection with `DropAfter`, `DropWindow`, and `PacketHook` for targeted failure scenarios. Packet loss simulation and relay stress tests
- **Channel API** (T12): streaming channels and datagram channels with comprehensive tests
- **Large datagram fragmentation**: transparent fragmentation and reassembly folded into `SendDatagram`/`RecvDatagram` — callers send arbitrarily large datagrams without worrying about MTU limits
- **Automatic LAN upgrade** (T5): redesigned as `LANServer` standalone server. Automatic detection and upgrade from relay to direct LAN connection when devices are on same network. Config struct replacing variadic options pattern
- **Multi-platform clients**: Swift via Network.framework QUIC, Kotlin with Gradle wrapper, TypeScript/Web with E2E crypto. E2E tests across all platforms — Swift 6/6, Kotlin, TypeScript Playwright. Raw QUIC for native clients alongside WebTransport for browsers
- **Deployment**: [Fly.io](https://fly.io/) auto-deploy from CI (T3), [certmagic](https://github.com/caddyserver/certmagic) storage verified, HTTP/3 + QUIC datagrams for browser WebTransport, Fly.io auto-start via TCP wake trigger (T16)
- **5 audit rounds** with all findings fixed. **v0.3.0 through v0.9.0 released**

### [marcelocantos/targets](https://github.com/marcelocantos/targets) — MCP Server Bootstrap (3 commits)

New project: Rust MCP server for convergence target management.

- **YAML schema**: hierarchical target definitions with status tracking, WSJF ranking fields
- **MCP tools**: `targets_render` with auto-render on mutations, `targets_frontier` for frontier-based scheduling
- **Design document**: hierarchical state machine model for target lifecycle

---

## Tooling

### [marcelocantos/den](https://github.com/marcelocantos/den) — C++ Rewrite & Audit Hardening (92 commits)

Continued from last week's Rust bootstrap, now rewritten to C++ and hardened through 5 audit rounds:

- **C++ rewrite**: complete rewrite from Rust to C++ with [spdlog](https://github.com/gabime/spdlog), [nlohmann/json](https://github.com/nlohmann/json), [libarchive](https://www.libarchive.org/), and [libcurl](https://curl.se/libcurl/). Independent package store at `~/.den/` — no dependency on Homebrew's `/opt/homebrew/` prefix. Unified package model across taps
- **Source builds**: parse Homebrew formulae via bundled Ruby binary (embedded Ruby VM attempted then dropped in favour of subprocess), compile packages from source with formula-parsed commands. Homebrew-free operation for environments where bottles are unavailable
- **Install flow**: CLI integration tests, index and archive test suites, platform detection, first-run Homebrew migration prompt
- **5 adversarial audit rounds**: 100+ findings across security, correctness, documentation, and infrastructure. Fixes include slug decode corruption, symlink path traversal, hardlink tar extraction, absolute path extraction, settings reset via config corruption, atomic writes for launchd plists, hash pinning, cache sealing, URL allowlist
- **Feature surface**: `install`, `list`, `use`, `info`, `search`, `deps`, `cleanup`, `uninstall`, `upgrade`, `cask`, `services`, `doctor` (7 health checks), `migrate`, background maintenance daemon, content-addressed bottle cache, manifest-based environment hierarchy, build environment integration, shell integration for environment switching
- **v0.1.0, v0.2.0, and v0.3.0 released** with cross-platform CI and release workflows

### [marcelocantos/jevon](https://github.com/marcelocantos/jevon) — Voice Bridge & Web UI (45 commits)

Continued from last week's protocol state machine framework, now adding voice capabilities and a desktop-first web UI:

- **Grok Realtime voice bridge**: integrated [xAI Grok Realtime API](https://docs.x.ai/docs/guides/realtime) for voice I/O — Option B architecture where Grok handles voice and Claude handles reasoning. Adaptive local VAD for noisy environments. Streaming text display of spoken responses. Voice status indicators in UI
- **Desktop-first web UI** (v0.2.0): split-pane layout — chat left, activity feed right. Persistent chat sessions across jevond restarts using JSONL as source of truth. PgUp/PgDn scrolling with smart auto-scroll. Hot reload from disk. Live terminal viewer — click an agent to see its PTY output
- **Persistent agent management**: agent registry with MCP tools for lifecycle management. Async fire-and-forget communication with notifications. `EnsureAgent` deduplication by workdir
- **WKWebView native path**: Swift `JevonBridge` for WKWebView↔native communication. Transport abstraction supporting browser and native dual mode. Tern relay transport for native connections
- **API key UX**: interactive prompting with masked input, clear instructions for obtaining keys, error messages for missing configuration

### [marcelocantos/mpe2pdf](https://github.com/marcelocantos/mpe2pdf) — Packaging Fix (1 commit)

- **npm tarball**: exclude `.db` files from published package

---

## Game Projects

### [squz/yourworld2](https://github.com/squz/yourworld2) + [ge](https://github.com/squz/yourworld2/ge) (submodule) — Scene Protocol & H.264 Streaming (104 commits)

Continued from last week's H.264 streaming and bgfx migration, now completing the scene protocol and engine refactoring:

- **Scene protocol end-to-end** (T54): full pipeline from server rendering through ged relay to remote player. Command structs with natural alignment, SceneSession for server-side management, SceneHost that connects to ged and waits for players. 43KB keyframes flowing. Round-trip verification tests confirm writer → keyframe/delta → renderer fidelity
- **NetworkBackend** (T54): patched [bgfx](https://github.com/bkarber/bgfx) to support custom `RendererContextI` implementations. `NetworkBackend` serialises full frame submissions — textures, uniforms, draw calls — for remote Metal backend playback. Asset creation protocol with `AssetTable` carrying source data. Per-session bgfx with replay removal. Full resource + frame flow: 1,418 resources flowing server→player
- **H.264 streaming**: zero-copy Metal texture path via [IOSurface](https://developer.apple.com/documentation/iosurface) — GPU writes directly to an `IOSurfaceRef` that the H.264 encoder reads without CPU copies. `StreamSession` manages encode pipeline; `VideoDecoder` handles client-side decode. Working end-to-end: bgfx renders globe, VideoToolbox encodes, streams via ged, player decodes and displays
- **T54 abandoned, pivot to H.264**: after the scene protocol reached per-session bgfx with direct-backend, the approach hit a dead end (bgfx's internal state is not designed for multi-instance). Pivoted to H.264 streaming as the practical path for dev mode
- **Engine refactoring**: `ge::run()` single entry point replacing 140 lines of infrastructure in main.cpp. `ge::Context` provides engine-owned SQLite DB handle. `BgfxContext` auto-installs signal handlers. `ge::Signal` for platform-gated SIGINT/SIGTERM. T55 achieved: game code is DB-mode-agnostic, engine owns persistence
- **sqlpipe v0.17.0 integration**: liteparser vendored, `db_wrap` from sqlift, `DeviceClass` support
- **Dawn removal complete** (T53): all WebGPU artifacts removed, bgfx is the sole renderer. Globe rendering (mesh loading, cube map, atmosphere, country silhouette) ported to bgfx with Metal shaders via `shaderc`

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 9 (+ ge submodule) |
| Total commits | 574 |
| Total lines added | +201,772 |
| Total lines removed | -105,816 |
| Net new lines | +95,956 |
| Net new lines (excl. vendored/golden) | ~+96,000 |
| File changes | 25,793 (incl. ~25,700 rustuml golden test files) |
| New files created | ~26,000 (incl. golden test pairs) |
| Languages | C++, Rust, Go, Swift, Kotlin, TypeScript, JavaScript, TLA+, YAML, SQL, HTML, CSS, WGSL, Lua, Ruby, PlantUML |
| Contributors | 1 (Marcelo Cantos) |

Note: den's +1M/-506K includes ~1M lines of vendored C++ dependencies (spdlog, nlohmann, libarchive, libcurl, OpenSSL). rustuml's +346K/-199K includes ~190K golden test SVG files and ~77K vendored code.

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | 184 | 25,793 | +346,501 | -199,119 | +147,382* |
| [squz/yourworld2](https://github.com/squz/yourworld2) + ge | 104 | 258 | +16,691 | -58,447 | -41,756** |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 92 | 136 | +1,034,698 | -506,505 | +528,193*** |
| [marcelocantos/tern](https://github.com/marcelocantos/tern) | 87 | 281 | +22,800 | -6,441 | +16,359 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 61 | 86 | +11,155 | -4,996 | +6,159 |
| [marcelocantos/jevon](https://github.com/marcelocantos/jevon) | 45 | 75 | +7,022 | -7,738 | -716 |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 34 | 62 | +29,829 | -3,155 | +26,674 |
| [marcelocantos/targets](https://github.com/marcelocantos/targets) | 3 | 14 | +2,539 | -6 | +2,533 |
| [marcelocantos/mpe2pdf](https://github.com/marcelocantos/mpe2pdf) | 1 | 1 | +1 | -0 | +1 |

\* rustuml net includes ~190K golden test SVG files and ~77K vendored code; own code net is ~+68K.
\** yourworld2 + ge net negative from Dawn/WebGPU removal (~48K lines deleted) offset by scene protocol and H.264 additions.
\*** den net includes ~510K vendored C++ dependencies; own code net is ~+18.5K.

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | ~720 | Golden test pairs, oracle extraction tests, format-parameterised smoke tests |
| [marcelocantos/tern](https://github.com/marcelocantos/tern) | ~224 | Channel tests, fault injection tests, coverage push (78%→89% root, crypto 91.5%, protocol 97.5%) |
| [marcelocantos/den](https://github.com/marcelocantos/den) | ~88 | CLI integration tests, index/archive test suites |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~42 | M:N scheduling migration tests, quiescence scope tests, TLA+ specs |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~29 | Predicate VM tests, convergence loop edge cases, E2E through tern |
| **Total** | **~1,103** | |

---

## Ideas & Innovations

### Quiescence Scope for Deterministic M:N Testing ([csp](https://github.com/marcelocantos/csp))

Testing M:N concurrent schedulers is notoriously difficult because thread interleaving is non-deterministic. The `quiescence_scope` primitive solves this by defining regions where the scheduler can detect that all enrolled imp processes have reached a stable state — no pending messages, no runnable coroutines. Combined with the `fake_clock` quiescence hook, this creates **deterministic test execution for inherently non-deterministic concurrent code**: when all processes are quiescent, the fake clock advances to the next scheduled event, triggering exactly the right set of wakeups. The TLA+ model of this interaction proves the protocol is gap-free — no spurious wakeups, no missed events.

### Oracle-Based SVG Parity Testing ([rustuml](https://github.com/marcelocantos/rustuml))

Achieving pixel-perfect SVG parity with Java PlantUML seemed impossible due to IEEE 754 floating-point differences between Rust and Java. The oracle test framework sidesteps this by **extracting structural layout information from reference SVGs** — element positions, text baselines, separator coordinates — and comparing at the layout level rather than as raw strings. The key insight was that Java AWT font metrics are exact binary fractions (multiples of 1/16), not arbitrary floats. By using these exact fractions in Rust, the coordinate calculations match precisely, and the oracle comparator handles the remaining edge cases structurally.

### Predicate-Aware Subscription Invalidation via Relational Algebra ([sqlpipe](https://github.com/marcelocantos/sqlpipe))

Most database replication systems treat subscriptions as opaque — any change to a subscribed table triggers a full re-evaluation. sqlpipe's relational algebra engine analyses subscription queries to determine **exactly which changesets affect which subscriptions**. Predicates are pushed down through joins, split across tables, and propagated transitively through equijoins. The compiled bytecode VM evaluates changesets in microseconds. Column relevance tracking adds another layer — if a subscription only depends on columns A and B, an UPDATE to column C is silently skipped. This transforms O(subscriptions × changes) invalidation into O(relevant changes).

### Custom bgfx RendererContextI for Network Rendering ([yourworld2/ge](https://github.com/squz/yourworld2))

[bgfx](https://github.com/bviber/bgfx) was not designed for remote rendering — it assumes a local GPU. The `NetworkBackend` bypasses this by **implementing bgfx's internal `RendererContextI` interface** to intercept all rendering commands (texture creation, uniform updates, draw calls) and serialise them for network transport. The remote player instantiates a real Metal backend and replays the serialised commands. This is a fundamentally different approach from the previous scene protocol (which operated at a higher abstraction level) — it captures bgfx's actual internal rendering state, achieving full fidelity without re-implementing the rendering pipeline.

### Fault Injection Proxy for Transport Testing ([tern](https://github.com/marcelocantos/tern))

Testing network protocols under failure conditions typically requires either mocking (which misses real protocol interactions) or waiting for real failures (which is slow and non-deterministic). The `faultproxy` is a **transparent UDP proxy with sequence-aware injection** — it sits between client and server, forwarding packets normally until a configured trigger fires. `DropAfter(n)` drops everything after packet n, `DropWindow(start, end)` drops a specific range, and `PacketHook` provides arbitrary per-packet logic. Because it operates at the UDP level, it tests the real protocol stack including encryption, fragmentation, and retransmission — not a mock.

### Stateless Convergence Loop for Eventually-Consistent Replication ([sqlpipe](https://github.com/marcelocantos/sqlpipe))

Traditional replication protocols require a handshake phase to establish baseline state before streaming changes. sqlpipe's convergence loop is **stateless** — peers exchange bucket hashes (content-addressed summaries of data ranges), identify divergent buckets by comparison, and reconcile by sending the actual data for differing buckets. No session state, no sequence numbers, no exactly-once delivery requirements. The protocol naturally converges regardless of packet loss, reordering, or restart. The TLA+ model proves convergence under all failure modes within bounded rounds.

---

## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| csp M:N migration + TLA+ | 25-40 | M:N scheduler correctness requires reasoning about all possible thread interleavings; quiescence detection is a distributed consensus problem; TLA+ specs require formal methods expertise |
| rustuml SVG parity | 20-30 | Reverse-engineering Java AWT font metrics from binary SVG output; building a structural SVG comparator; 6 renderer rewrites while maintaining 12,500+ golden tests |
| den C++ rewrite + audits | 15-25 | Full-stack package manager (HTTP, archive extraction, Ruby embedding, daemon, CLI) rewritten cross-language; 5 adversarial security audit rounds |
| sqlpipe predicate VM + convergence | 15-25 | Relational algebra engine, bytecode VM compiler, three-valued NULL semantics, TLA+ verification of convergence protocol |
| tern coverage + fault injection | 10-15 | UDP fault proxy with sequence-aware injection, 4 platform E2E tests, coverage push to 97.5% protocol |
| yourworld2/ge scene protocol + H.264 | 15-25 | bgfx internals (custom RendererContextI), Metal-specific serialisation, H.264 encode/decode pipeline, zero-copy IOSurface |
| jevon voice + web UI | 5-10 | Grok Realtime API integration (underdocumented), WKWebView bridge, persistent chat with JSONL |
| targets MCP server | 2-3 | Rust MCP server scaffold with YAML schema |

### The Diversity Tax

Specialisms exercised this week:

- **Concurrent systems programming** — M:N scheduler, quiescence protocols, atomic operations, thread-safety analysis
- **Formal verification** — TLA+ specifications for 6+ protocols, model checking with bounded state spaces
- **Compiler/language tooling** — PlantUML parser, relational algebra engine, bytecode VM compiler
- **Graphics programming** — bgfx internals, Metal rendering, custom RendererContextI, shader compilation
- **Video engineering** — H.264 encode/decode, VideoToolbox, IOSurface zero-copy paths
- **Network protocol design** — WebTransport, QUIC, fault injection, convergence protocols
- **Security auditing** — 5 rounds of adversarial audit, path traversal, symlink attacks, TOCTOU
- **Package management** — Homebrew formula parsing, bottle extraction, dependency resolution, source builds
- **Voice AI integration** — Grok Realtime API, VAD, WebSocket voice protocol
- **Cross-platform mobile** — Swift/Network.framework, Kotlin/Gradle, WKWebView bridging
- **Database internals** — SQLite preupdate hooks, changeset processing, predicate pushdown

No single developer holds production-level expertise across concurrent systems, formal verification, graphics programming, video encoding, network protocols, security auditing, and package management simultaneously.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| csp | 4-6 | Quiescence protocol design, TLA+ spec review, M:N migration strategy |
| rustuml | 3-5 | Font metrics insight (binary fractions), oracle comparison strategy |
| den | 2-3 | C++ rewrite decision, audit triage |
| sqlpipe | 3-4 | Predicate algebra design, convergence protocol review |
| tern | 2-3 | Fault injection design, coverage strategy |
| yourworld2/ge | 3-5 | Scene protocol architecture, T54 abandon decision, H.264 pivot |
| jevon | 2-3 | Voice architecture (Grok voice + Claude brain), WKWebView approach |
| **Total** | **~19-29** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | Ramp-up cost |
|---------|------------|-----------------|--------------|
| csp | 25-40 | 35-55 | M:N scheduling theory, TLA+, fcontext internals |
| rustuml | 20-30 | 30-45 | PlantUML internals, Java AWT metrics, SVG spec |
| den | 15-25 | 20-35 | Homebrew architecture, Ruby embedding, tar/archive security |
| sqlpipe | 15-25 | 25-40 | Relational algebra, VM compilation, SQLite internals |
| tern | 10-15 | 15-20 | QUIC protocol, WebTransport, 4-platform E2E |
| yourworld2/ge | 15-25 | 25-40 | bgfx source, Metal API, H.264/VideoToolbox |
| jevon | 5-10 | 8-15 | Grok API, WKWebView bridging, voice processing |
| targets | 2-3 | 3-4 | Rust MCP protocol |

Context-switching tax (11 domain switches): +15-25 person-days

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **120-180 person-days (5-8 months)** |
| Specialist team (traditional) | **100-160 person-days (3-5 person-months)** |
| Actual human effort this week | **~19-29 hours (~3-4 person-days)** |
| **Multiplier vs. generalist** | **~30-50x** |
| **Multiplier vs. specialist team** | **~25-45x** |

The multiplier is highest on the formally verified concurrent systems work (csp) and the renderer parity effort (rustuml), where the AI's ability to systematically transform 663 tests and rewrite 6 renderers while maintaining correctness would take a human weeks of tedious, error-prone work. The multiplier is lowest on the voice integration (jevon) where the main difficulty was empirical API debugging — a fundamentally sequential activity. The human contribution concentrated on architectural decisions (quiescence protocol design, scene protocol pivot, convergence loop design) and quality judgement (when to abandon T54, how to structure oracle comparisons, which audit findings are real vulnerabilities).

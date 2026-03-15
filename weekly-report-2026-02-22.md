# Weekly Progress Report — 2026-02-16…22

## Executive Summary

The biggest week yet — **11 repositories** spanning concurrency infrastructure, language design, database tooling, game development, AI agent skills, and a Go standard library proposal. **csp** underwent a complete transformation from bare extraction to a comprehensive CSP platform: M:N scheduler, 100+ stream combinators, channel topology surgery, a full cancellation framework with cancel-aware TLS, kqueue I/O reactor, mmap stack pools, TLA+ formal verification, C++23 migration, and a 6-paper engineering series (133 commits). **mk** was designed and built from scratch as a modern build tool and shipped through 5 releases to [Homebrew](https://brew.sh/) in 4 days. Two new C++ libraries — **sqlift** (declarative SQLite schema migration) and **sqlpipe** (streaming SQLite replication) — were created and released. **yourworld2** gained a country carousel, audio, and SQLite-backed game state with real-time bidirectional sync via sqlpipe. **go-decimal-proposal** introduced a decimal64/decimal128 proposal for the Go standard library.

**313 commits** | **+70,000+ net lines** (excl. vendored deps) | **~200-340 person-days traditional equivalent** | **~30-60x multiplier**

### Major Achievements & Innovations

- **CSP platform from extraction to production** in csp: 133 commits building an M:N work-stealing scheduler, 100+ stream combinators, channel topology surgery (swap/fuse/splice/tap), cancellation framework with cancel-aware TLS via mbedTLS, kqueue I/O reactor, mmap demand-paged stack pools, persistent HAMT-backed dynamic scoping, TLA+ formal verification of 9+ concurrency protocols, C++23 migration, 400+ tests, comprehensive documentation (11-chapter guide, 50+ combinator reference pages, 6 engineering papers, architecture document)
- **mk build tool from nothing to Homebrew in 4 days**: Complete build tool language (pattern rules with glob/regex constraints, build configs with composition/exclusion, user-defined functions, `for` loops, parallel execution, fingerprinting, scoped includes) in Go, 5 releases (v0.1.0-v0.5.0) with CI, Homebrew formula, shell completions, and self-hosting mkfile
- **Channel topology surgery** in csp: `swap`, `fuse`, `splice`, and `tap` enable runtime channel rewiring — `tap` provides RAII observation with auto-fuse-back, `splice` adds weak references and slot memory safety, all backed by 4 new TLA+ formal specs
- **Demand-paged microthread stacks** in csp: 1 MB mmap'd regions with guard pages consume only actual stack depth in physical RAM; `maybe_shrink()` at channel operations reclaims pages mid-flight so transient deep recursion does not hold memory indefinitely
- **sqlpipe streaming replication**: Built a bidirectional SQLite replication protocol from scratch using [SQLite session extension](https://www.sqlite.org/sessionintro.html) changesets, with master/replica architecture evolving to a symmetric `Peer` class, 60+ tests, and CI pipeline
- **Persistent HAMT for dynamic scoping** in csp: `csp::dynamic<T>` provides microthread-local variables with copy-on-write semantics and cross-microthread context transfer via channels — request-scoped logging and transaction contexts without explicit parameter threading
- **Go decimal64/decimal128 proposal**: Playground-based proposal for adding IEEE 754 decimal floating-point types to Go's standard library, with CI and working examples

### Tough Challenges Overcome

- **M:N scheduler TOCTOU race** (csp): between registering on a channel wait queue and context-switching out, a waker on another thread can call `schedule()` — solved with a three-participant protocol (suspender, waker, drainer) using two atomic booleans, validated by TLA+ exhaustive model checking
- **Channel use-after-free in prialt post-wakeup path** (csp): after a prialt fires, the wakeup path was accessing channel slot state that could already be freed by the winning branch's cleanup — required careful lifetime analysis of the three-participant protocol to ensure the slot remains valid until all branches complete their CAS cleanup
- **mk pattern rule prerequisite merging**: when multiple pattern rules match a target, their prerequisites must be merged into a single dependency list without introducing cycles — required a topological analysis phase during rule resolution that detects and reports ambiguous matches
- **Homebrew version detection collision** (homebrew-tap): homebrew-releaser was extracting "64" from "arm64" in tarball filenames as the version number — fixed by adding an explicit `version` field to the formula
- **sqlpipe bidirectional changeset ordering**: when both peers write simultaneously, changesets can arrive out of causal order — the `Peer` class resolves this by serialising changeset application through a single event loop and returning change events from `handle_message` rather than using callbacks, ensuring deterministic conflict resolution
- **Porting carousel physics from Obj-C** (yourworld2): the original GameState.mm used a three-component force law (linear damping, smoothstep friction, magnetic snap-to-grid) with sub-stepped integration; faithfully reproducing the feel required matching the exact force coefficients and 10-iteration-per-frame symplectic Euler stepping

Contributor: Marcelo Cantos

---

## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — From Extraction to Comprehensive Platform (133 commits)

**The biggest effort of the week by a wide margin.** What began as a bare extraction from bricabrac became a production-grade CSP microthreading platform spanning scheduler design, I/O, formal verification, and comprehensive documentation:

- **M:N scheduler**: Work-stealing across OS threads (`init_runtime(n)`), with TLA+ formal verification of the suspension TOCTOU race, work stealing, channel lifecycle, worker parking, and alt-state CAS — 5 models with bug variants verified by [TLC](https://lamport.azurewebsites.net/tla/tools.html)
- **100+ stream combinators** in `csp::part` namespace: `map`, `where`, `scan`, `flat_map`, `batch`, `window`, `slide`, `merge`, `zip`/`unzip`, `round_robin`, `interleave`, `partition`, `group_by`, `share`, `debounce`, `throttle`, `gate`, `metrics`, `reduce`, `first_wins`, `join`, `distinct`, `unique`, `sample`, `delay`, `timeout`, `take_while`, `skip_while`, `pairwise`, `nwise`, `flatten`, `stride`, `default_if_empty`, `parallel_map` (concurrent N-worker transform), `combine_latest`, `pace` (rate-limited passthrough with backpressure), `conflate`, `mux`/`demux`/`collect`, `try_map`, `take_until`, `any_of`/`all_of`, `chunk_by`, `foreach_emit`, `fallback`, `transpose`, `sort_merge`, `random_bytes`, RNG stream combinators. Four flattening strategies (`merge_all`, `concat_all`, `switch_all`, `exhaust_all`). Dead-letter channels for `throttle`, `debounce`, and `sample`. All header-only with `operator|` composition via `filter`/`producer`/`consumer` wrapper types
- **Channel topology surgery**: `swap` (atomic 4-arg channel endpoint exchange), `fuse` (join two channel halves), `splice` (insert processing between endpoints with weak refs and slot memory safety), `tap` (RAII channel observer with auto-fuse-back on destruction). 4 new TLA+ specs (`ConcurrentSwap`, `SwapWaiterRetry`, `TapLifecycle`, plus `prialt` and `swap+waiter` interaction models)
- **Supervision & cancellation**: `worker_group` with restart policies (one-for-one, one-for-all) and escalation. Cancel-aware TLS via [mbedTLS](https://www.trustedfirmware.org/projects/mbed-tls/) integration. Unified timer/IO suspension through reactor signals. `cancel.h`/`cancel.cc` cancellation token framework
- **CSP-aware I/O**: [kqueue](https://en.wikipedia.org/wiki/Kqueue) reactor for non-blocking `read`/`write`/`accept`/`connect`, blocking thread pool for DNS resolution, Unix signal channels via self-pipe trick
- **`csp::dynamic<T>`**: Dynamic-scoped variables backed by a persistent [HAMT](https://en.wikipedia.org/wiki/Hash_array_mapped_trie) (intrusive refcounting, BLR-free read path), with `context`/`context_scope` for snapshot/restore across microthreads
- **Mmap stack pool**: 1 MB mmap'd regions with guard pages, demand-paged (physical memory matches actual depth), `MADV_FREE` lazy reclamation, API-boundary shrinking to reclaim transient deep stacks. Under sanitisers, falls back to 128 KB heap allocation to avoid shadow-memory bloat
- **C++23 migration**: Switched entire codebase from C++17. Applied deducing `this`, `requires` clauses, `std::bit_ceil`, `std::unreachable()`, `static operator()`, `std::flat_map`, `std::expected`, `std::popcount`, direct template storage replacing `std::function`
- **API refinement**: `chan<T>` structured bindings, move-only endpoints, 0-based `alt`/`prialt` indexing, `~index` bitwise complement for death results, two-phase `prialt` eliminating the `action` class entirely. Renamed "microthread" to "imp". `csp::none` non-blocking guard. `fake_clock` for deterministic time testing. `csp::local` dynamic scoping, `csp::mt_local<T>` imp-local storage. Parameterless parts converted from functions to variable templates
- **ARM64 stack depth analyser**: Static analysis of compiled functions to right-size microthread stacks, with BLR elimination for exact analysis
- **Documentation**: 6-paper ["Engineering of CSP"](https://github.com/marcelocantos/csp/tree/master/docs/papers) series (TLS caching, channel lifecycle, two-phase prialt, TLA+ verification, stack engineering, dynamic scoping). 11-chapter guide (channels, multiplexing, timers, combinators, I/O, blocking, signals, concurrency, error handling, pitfalls, dynamic scoping). 50+ individual combinator reference pages with SVG diagrams generated from an ASCII-art DSL. Architecture document (1,055 lines). 12 runnable examples
- **Sanitiser support**: Full ASan, UBSan, TSan build targets with [Boost.Context](https://www.boost.org/doc/libs/release/libs/context/) fibre annotations
- **Testing**: 400+ tests, all passing under normal, TSan, and ASan+UBSan builds

---

### [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) — Initial Release (6 commits, initial)

A new declarative SQLite schema migration library for C++:

- **Core library**: ~1,040 lines implementing schema extraction from live databases, structural diffing, and migration plan generation/application. Handles tables, columns, indices, triggers, and views. Header-only with vendored [doctest](https://github.com/doctest/doctest) for testing and [nlohmann/json](https://github.com/nlohmann/json) for serialisation
- **JSON round-trip**: `MigrationPlan` serialises to/from JSON via nlohmann/json, enabling plan inspection and storage
- **Testing**: 56 tests across 7 test files covering schema extraction, diffing, plan application, edge cases, and JSON serialisation
- **Build**: Started with GNU Makefile, migrated to mk. Vendored doctest into `vendor/include/` to remove brew dependency
- **Agent support**: `CLAUDE.md` project instructions and `agents-guide.md` with complete API reference

---

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Initial Release (13 commits, initial)

A new streaming replication protocol for SQLite:

- **Core library**: Built on [SQLite's session extension](https://www.sqlite.org/sessionintro.html) — captures changesets as they happen and streams them between peers. Initial master/replica architecture with state-request handshake, changeset framing, and resync support
- **Bidirectional replication**: Evolved to a symmetric `Peer` class replacing the master/replica split. Changed API to return change events from `handle_message` instead of using callbacks, enabling deterministic conflict resolution
- **Query subscriptions**: Result-change detection for live query updates. Hash-exchange diff sync protocol for efficient state reconciliation
- **Testing**: 60+ test cases across 6 test files (integration, master, replica, protocol, resync, peer). Loopback example demonstrating the full round-trip
- **CI and build**: GitHub Actions CI workflow. Migrated from Makefile to mk. Vendored SQLite (compiled with session/preupdate hooks), [spdlog](https://github.com/gabime/spdlog), and doctest

---

### [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) — Initial Release (1 commit, initial)

A proposal for adding [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754) decimal64/decimal128 types to Go's standard library. Includes a working playground implementation with CI pipeline. +2,569 lines.

---

## Tooling

### [marcelocantos/mk](https://github.com/marcelocantos/mk) — From-Scratch Build Tool (39 commits, initial)

Built a modern replacement for GNU Make from scratch in Go:

- **Language**: Pattern rules with glob and regex constraints on captures. Variables (`=`, `?=`, `:=`). `$[...]` functions (`shell`, `wildcard`, `patsubst`, etc.). Multi-output rules. [Order-only prerequisites](https://www.gnu.org/software/make/manual/html_node/Prerequisite-Types.html). `[keep]` annotations. `$changed` automatic variable for incremental recipes. `[fingerprint: command]` for non-file artifact staleness. Recursive variable definition detection (parse error, not silent loop). Relative indentation preserved in recipes
- **Advanced features**: `for` loops for generating rules and variables across a matrix. Build configs with composition (`+`), exclusion, and state isolation. User-defined functions with hash cache. Parallel execution with automatic CPU capacity detection. Scoped includes with path rebasing and pattern discovery
- **Standard library**: Embedded `std/c.mk`, `std/cxx.mk`, `std/go.mk` for common build patterns
- **Release pipeline**: Apache 2.0 licence. GitHub Actions CI building for darwin/arm64, linux/amd64, linux/arm64. 5 releases (v0.1.0-v0.5.0) in 4 days. [Homebrew formula](https://github.com/marcelocantos/homebrew-tap) with automated updates via [homebrew-releaser](https://github.com/Justintime50/homebrew-releaser). Shell completions for bash and zsh. Self-hosting mkfile
- **Agent support**: Embedded agents guide accessible via `--help-agent` (with CLI usage text prefix). `-C` flag for directory change. `--version` flag
- **Documentation**: Full design spec (`DESIGN.md`), README with getting started guide and mini tutorial, detailed ["Why mk?"](https://github.com/marcelocantos/mk/blob/master/docs/why-mk.md) analysis

---

### [marcelocantos/skills](https://github.com/marcelocantos/skills) — Claude Code Skills (20 commits, initial)

Created a repository of reusable [Claude Code](https://claude.ai/code) skill definitions:

- **6 skills**: `/docs` (end-to-end documentation sherpa with comprehensive document types taxonomy, agent-guide generation), `/open-source` (audit, fix, document, publish, release — delegates docs to `/docs`), `/release` (version, release notes, CI, Homebrew tap, GitHub release), `/republish-skills` (sync to GitHub with mk automation), `/progress-report` (weekly report generation from git activity), `/where` (concise session status)
- **Build**: mkfile handles syncing from `~/.claude/skills/`, README generation, diffing, committing, and pushing

---

### [marcelocantos/homebrew-tap](https://github.com/marcelocantos/homebrew-tap) — mk Distribution (8 commits)

Created the Homebrew tap and iterated the mk formula through 5 versions. Evolved from source-based Go build to pre-built binary distribution with shell completion installation. Fixed version detection bug where homebrew-releaser extracted "64" from "arm64" in tarball filenames. Switched to automated formula updates via homebrew-releaser.

---

## Game Projects

### [squz/yourworld2](https://github.com/squz/yourworld2) — Carousel, Audio & State Persistence (12 commits)

- **Country carousel**: Horizontally scrollable strip at screen bottom showing unplaced countries with physics-based scrolling ported from original GameState.mm — snap-to-grid, velocity accumulation with 5/6 boost decay, sub-stepped symplectic Euler integration (10 iterations/frame). 584-line Carousel.cpp with pImpl pattern
- **Country silhouettes**: Initially loaded meshes.bin on CPU and projected to 2D; refactored to render directly from the globe's existing GPU mesh buffers using the atlas pipeline and per-cell orthographic viewProj. Size scaled by country radius with smootherstep curve; orientation rotated in globe-local space to match country position as globe spins. New `carousel.wgsl` shader for 2D UI rendering with per-vertex colour tinting
- **Audio**: Background music (`blue_planet_full_loop.mp3`, 0.5 volume, looped) and placement sound effect (`distant_explosion03.wav`) via sq::Audio interface, assets from original yourworld tracked with Git LFS
- **SQLite-backed game state**: New `GameDb` class (~380 lines) wrapping [sqlift](https://github.com/marcelocantos/sqlift) to persist game state in SQLite, replacing in-memory-only `Game` struct. `Application` and `Carousel` refactored to work through `GameDb`
- **sqlpipe state sync**: Wired [sqlpipe](https://github.com/marcelocantos/sqlpipe) bidirectional replication into the game server — creates a `sqlpipe::Master` on the in-memory GameDb, sends a state-request magic byte on connect, loads received DB bytes, and streams changesets via `drainMessages`/`onMessage`. Foundation for multiplayer state replication
- **C++23 upgrade**: Bumped from C++20 to C++23 to leverage sqlift/sqlpipe APIs
- **Engine rebrand**: Renamed `sq` submodule to `ge` across all files (`.gitmodules`, Makefile, C++ includes, namespaces). 7 ge submodule updates
- **Codebase documentation**: 7 planning documents under `.planning/codebase/` (architecture, concerns, conventions, integrations, stack, structure, testing) — 1,468 lines mapping the existing codebase

### [squz/multimaze2](https://github.com/squz/multimaze2) — Submodule Maintenance (7 commits)

- `sq` to `ge` submodule rename across the codebase
- sq submodule updates (sqd daemon, iOS TestFlight CI, Android SIGSEGV fix)
- Moved `Tweak.h` into sq submodule for cross-project reuse

---

## Strategic Planning & Documentation

### [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) — Reports & Agentic AI Talk (18 commits)

Weekly progress reports and a [Marp](https://marp.app/) slide deck on agentic AI development with outline document, HTML export, and slide images (CSP architecture SVG, HAMT SVG, spherical chess screenshot, YourWorld globe screenshot). +4,806 lines.

---

## Other Work

### [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) — Recovery & Restoration (20 commits)

Recovery/restoration commits: database procedures, schemas, and forms. +2,293/-489 lines. Brief maintenance work, not new development.

---

## Other Team Work

### [squz/esfera2](https://github.com/squz/esfera2) — Competitive Multiplayer & Release Engineering (59 commits, Andrew Cantos)

Andrew delivered a major feature and infrastructure push: TestFlight pipeline (`make testflight`) with App Store compliance fixes, staging/production deploy pipeline, per-category Elo ratings (online vs correspondence) with server tests, correspondence play via WebSocket, daily streak tracking, landscape orientation, game history, push notifications, player profiles with 193-country selection, nested menu system with pixel-art icons, turn indicator extraction into a testable module (32 test cases), animation refactoring, and GPU buffer overflow fix. 59 commits, ~+3,400/-500 lines.

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 11 |
| Total commits | 313 |
| Total lines added | +411,000+* |
| Total lines removed | -25,000+ |
| Net new lines (excl. vendored) | +70,000+ |
| File changes | 884 |
| New files created | 779+ |
| Languages | C++, Go, TLA+, Markdown, Python, WGSL, SQL, Ruby, YAML, Shell |

*\*Includes ~314,000 lines of vendored dependencies (sqlite3, doctest, nlohmann/json in sqlift and sqlpipe).*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 133 | 508 | +72,000+ | -16,000+ | +56,000+* |
| [marcelocantos/mk](https://github.com/marcelocantos/mk) | 39 | 28 | +7,536 | -380 | +7,156 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 20 | 10 | +853 | -115 | +738 |
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | 20 | — | +2,293 | -489 | +1,804 |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 18 | — | +4,806 | -36 | +4,770 |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 13 | 24 | +288,155* | -1,170 | +286,985* |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 12 | 29 | +2,429 | -536 | +1,893† |
| [marcelocantos/homebrew-tap](https://github.com/marcelocantos/homebrew-tap) | 8 | 2 | +93 | -31 | +62 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 7 | 13 | +155 | -299 | -144‡ |
| [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) | 6 | 20 | +35,376* | -92 | +35,284* |
| [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) | 1 | — | +2,569 | -0 | +2,569 |

*\*Includes vendored dependencies (sqlite3, doctest, nlohmann/json, spdlog).*
*†Non-vendored lines only.*
*‡Submodule updates and refactoring.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~400 | I/O, combinators, M:N, timers, dynamic scoping, topology surgery, cancellation, TLS, flattening, TLA+-validated protocols |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~60 | Integration, master, replica, protocol, resync, bidirectional peer |
| [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) | ~56 | Schema extraction, diffing, plan application, JSON round-trip |
| [marcelocantos/mk](https://github.com/marcelocantos/mk) | ~40 | Pattern rules, variables, configs, parallel execution, includes |
| **Total** | **~556** | |

---

## Ideas & Innovations

### TLA+ Verification of a Microthread Scheduler ([csp](https://github.com/marcelocantos/csp))

The csp library's M:N scheduler has a subtle TOCTOU race in its suspension protocol: between the moment a microthread registers on a channel's wait queue and the moment it context-switches out, a waker on another thread can call `schedule()` — but pushing a still-executing MT onto a run queue would cause double execution. The solution uses two atomic booleans (`suspending_`, `wake_pending_`) with a three-participant protocol (suspender, waker, drainer). Rather than relying on code review alone, **9+ TLA+ models** (plus deliberate-bug variants) were built and exhaustively verified by the [TLC model checker](https://lamport.azurewebsites.net/tla/tools.html), covering suspension, work stealing, channel lifecycle, worker parking, alt-state CAS, concurrent swap, swap+waiter retry, and tap lifecycle. This is unusually rigorous for a C++ library.

### Demand-Paged Microthread Stacks ([csp](https://github.com/marcelocantos/csp))

Instead of heap-allocating fixed-size stacks, csp maps **1 MB virtual regions** per microthread with a guard page at the base. The kernel demand-pages physical memory as the stack grows, so a microthread using 4 KB of stack consumes 4 KB of RAM, not 1 MB. Freed stacks are cached (up to 256) with `MADV_FREE` for lazy kernel reclamation. The twist: `maybe_shrink()` is called at channel operations to **reclaim unused stack pages mid-flight** — a microthread that briefly recurses deep does not hold physical memory indefinitely. Under sanitisers, the system falls back to 128 KB heap allocation to avoid shadow-memory bloat.

### Channel Topology Surgery ([csp](https://github.com/marcelocantos/csp))

Most CSP implementations treat channel connections as immutable: once a writer connects to a reader, the topology is fixed. csp introduces **`swap`, `fuse`, `splice`, and `tap` operations that rewire channel connections at runtime** while preserving type safety and thread safety. `tap` is particularly elegant — it interposes an observer on a live channel and automatically fuses the original connection back when the tap is destroyed (RAII). `splice` uses weak references and slot memory safety to allow safe insertion of processing stages into an existing pipeline without dangling pointers. A dedicated TLA+ specification verifies the concurrent swap protocol handles the race where two swaps target overlapping endpoints simultaneously.

### From-Scratch Build Tool to Homebrew in 4 Days ([mk](https://github.com/marcelocantos/mk))

mk demonstrates the leverage of AI-assisted development at its most extreme. The entire tool — **language design, parser, dependency graph engine, pattern matching with glob/regex constraints, build configs with composition, parallel execution, fingerprinting, standard library, CI pipeline, Homebrew formula, shell completions, documentation, and 5 shipped releases** — was conceived and delivered in a single 4-day burst. The language design itself is novel: `[fingerprint: command]` annotations let mk track non-file artifacts (like database schema versions) by command output hash, and scoped `include` with automatic path rebasing enables composable build definitions across nested project structures.

### SQLite Streaming Replication via Session Extension ([sqlpipe](https://github.com/marcelocantos/sqlpipe))

SQLite lacks built-in replication, but its [session extension](https://www.sqlite.org/sessionintro.html) can capture row-level changesets as they happen. sqlpipe exploits this to build **streaming bidirectional replication** — each peer wraps its database in a session, captures writes as changesets, and streams them to the other peer for application. The key insight is that **changesets are self-describing and composable**: they can be serialised, transported over any byte stream, and applied idempotently. The protocol includes a resync handshake for recovering from divergence, making it suitable for unreliable networks like mobile game connections.

### Cancellation-Aware TLS in a Microthread Runtime ([csp](https://github.com/marcelocantos/csp))

Integrating TLS into a cooperative microthread scheduler creates a chicken-and-egg problem: TLS needs blocking I/O for the handshake, but the scheduler's I/O is non-blocking and cooperative. csp's solution **wraps mbedTLS with custom BIO callbacks that route through the kqueue reactor**, so TLS read/write operations suspend the current imp (microthread) and resume when data arrives — exactly like plain socket I/O. Cancellation tokens propagate through the TLS layer, so cancelling a parent scope cleanly tears down in-flight TLS connections without leaked sockets or half-completed handshakes.

### SVG Diagram Generation from ASCII Art ([csp](https://github.com/marcelocantos/csp))

The csp documentation uses dataflow diagrams for every combinator, but maintaining Mermaid diagrams alongside code proved fragile (syntax changes, rendering inconsistencies, no version control diff). The solution: **a custom ASCII-art DSL that compiles to SVG** via a Python script (`gen_diagrams.py`). Diagrams are defined inline in documentation as ASCII box-and-arrow art, which is readable in source form, diffs cleanly in git, and renders to publication-quality SVG. This eliminated the Mermaid dependency entirely and made diagrams a first-class part of the documentation workflow.

### GPU Mesh Reuse for 2D Silhouettes ([yourworld2](https://github.com/squz/yourworld2))

The country carousel initially loaded 3D mesh data from `meshes.bin` on the CPU, projected each country to 2D orthographically, and uploaded separate silhouette buffers. The refactored version **renders silhouettes directly from the globe's existing GPU mesh buffers** using the same atlas pipeline and texture bind groups — each carousel cell just gets a different orthographic viewProj matrix looking head-on at the country's centroid. This eliminates the second mesh load, the CPU projection, and the duplicate GPU uploads, while producing identical visual output.

---

## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **csp** | 80-120 | Building an M:N scheduler with work stealing is a PhD-level concurrency problem. TLA+ formal verification (9+ models) requires expertise in temporal logic. 100+ combinators with correct channel lifecycle semantics and back-pressure handling. Channel topology surgery (swap/fuse/splice/tap) is novel — no reference implementations exist. kqueue reactor. HAMT implementation. Cancel-aware TLS via mbedTLS requires deep understanding of both TLS state machines and cooperative scheduling. ARM64 binary analysis. C++23 migration of a large codebase. 6 engineering papers. Comprehensive reference docs with diagram generation. |
| **mk** | 40-60 | Language design from first principles requires understanding parser construction, dependency graph analysis, cycle detection, and GNU Make's conceptual model. Pattern rules with constraint propagation, build configs with exclusion semantics, parallel execution with capacity detection, fingerprinting for non-file artifacts, scoped includes with path rebasing. CI pipeline, Homebrew formula debugging, shell completions, self-hosting bootstrap. |
| **sqlpipe** | 8-12 | Streaming replication over SQLite sessions requires deep understanding of the session extension API, changeset serialisation, and conflict resolution semantics. Bidirectional peer protocol design with correct causal ordering. Query subscriptions with change detection. |
| **sqlift** | 5-8 | Schema extraction from live SQLite databases, structural diffing, and migration plan generation. Correct handling of tables, columns, indices, triggers, and views. JSON serialisation. |
| **yourworld2** | 8-12 | Carousel physics (ported from original Obj-C), silhouette rendering (CPU-to-GPU refactor), audio integration, GameDb design wrapping sqlift, sqlpipe state sync wiring, engine rebrand across all files, 1,468 lines of codebase documentation. |
| **multimaze2** | 1-2 | Submodule updates and refactoring. Tweak.h extraction to shared submodule. |
| **skills** | 2-3 | Writing precise, agent-optimised skill definitions requires understanding Claude Code's execution model and tool APIs. |
| **homebrew-tap** | 1-2 | Homebrew formula iteration, debugging version detection collision, homebrew-releaser integration. |
| **go-decimal-proposal** | 3-5 | IEEE 754 decimal semantics, Go type system integration, playground implementation. |
| **progress-reports** | 1-2 | Marp slide deck design, report generation. |
| **hms** | 2-3 | Database procedure restoration, schema recovery. |

### The Diversity Tax

Specialisms exercised this week:

- C++ microthreading, context switching, M:N scheduling, lock-free protocols
- TLA+ formal methods and model checking (9+ models)
- kqueue/reactor-based I/O
- ARM64 instruction set analysis
- TLS protocol integration with cooperative schedulers
- Language design and parser implementation (Go)
- Build system theory (dependency graphs, pattern matching, fingerprinting)
- SQLite session extension and replication protocols
- Schema migration algorithms
- C++23 standard library and idioms
- WebGPU/WGSL shader programming and game state architecture
- Orthographic projection and globe-space geometry
- IEEE 754 decimal floating-point specification
- Open-source release engineering (CI/CD, Homebrew, GitHub Actions)
- Technical writing (engineering papers, reference documentation, agent guides)
- Database procedure restoration and recovery

No single engineer holds expertise in formal verification, language design, database replication, game engine architecture, IEEE 754 decimal semantics, and release engineering simultaneously.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **csp** (133 commits) | 12-22 | Architecture decisions (M:N design, combinator API, topology surgery, cancellation design), reviewing TLA+ specs, testing under sanitisers, approving C++23 migration strategy |
| **mk** (39 commits) | 4-8 | Language design decisions (syntax, config composition semantics), testing builds on real projects (csp, sqlift, sqlpipe), reviewing CI output |
| **yourworld2** (12 commits) | 3-5 | Carousel UX decisions, visual comparison with original game, audio selection, state sync architecture decisions, reviewing codebase docs |
| **sqlpipe** (13 commits) | 2-3 | Protocol design decisions, testing replication round-trips |
| **sqlift** (6 commits) | 1-2 | API review, migration plan validation |
| **skills** (20 commits) | 1-2 | Deciding skill scope and content |
| **Other** (mk, homebrew, hms, reports, proposal) | 2-4 | Homebrew debugging, talk content, submodule renames, recovery work, proposal review |
| **Total** | **~25-46 hours** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | Ramp-up cost |
|---------|-------------|-----------------|--------------|
| csp | 80-120 | 120-180 | +50% for TLA+, lock-free protocols, ARM64 |
| mk | 40-60 | 50-75 | +25% for language design, build system theory |
| sqlpipe | 8-12 | 12-18 | +50% for SQLite session extension internals |
| sqlift | 5-8 | 8-12 | +50% for schema diffing algorithms |
| yourworld2 | 8-12 | 12-18 | +50% for GPU pipeline, Obj-C physics porting |
| All other | 10-17 | 15-25 | +50% average |
| **Subtotal** | **151-229** | **217-328** | |
| Context-switching tax (11 projects) | | +15% | |
| **Total** | | **~250-375** | |

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~200-340 person-days (10-17 months)** |
| Specialist team (traditional) | **~120-180 person-days (6-9 person-months)** |
| Actual human effort this week | **~25-46 hours (~3-6 person-days)** |
| **Multiplier vs. generalist** | **~35-95x** |
| **Multiplier vs. specialist team** | **~20-50x** |

The multiplier is highest for csp, where a single agent traversed M:N scheduler design, TLA+ formal verification, kqueue reactor implementation, channel topology surgery, cancel-aware TLS integration, ARM64 binary analysis, C++23 migration, and comprehensive documentation without context-switch overhead. mk is close behind — the entire journey from language design to Homebrew distribution compressed into 4 days. The human contribution concentrated on architectural vision (combinator API shape, topology surgery design, mk syntax decisions), quality validation (reviewing TLA+ specs, benchmark-driven optimisation, testing mk on real projects), and aesthetic judgement (carousel UX, audio selection, silhouette rendering).

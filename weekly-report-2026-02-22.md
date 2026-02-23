# Weekly Progress Report — 2026-02-19…22 (4 days)

## Executive Summary

A prolific 4-day sprint across **8 repositories** spanning library engineering, language design, database tooling, game development, and AI agent infrastructure. **mk** was designed and built from scratch as a modern build tool — pattern rules, parallel execution, embedded standard library — and shipped through 5 releases to [Homebrew](https://brew.sh/). **csp** added ~20 more stream combinators, channel topology surgery (swap/fuse/splice/tap), a full cancellation framework with cancel-aware TLS, and a 6-paper engineering series. Two new C++ libraries — **sqlift** (declarative SQLite schema migration) and **sqlpipe** (streaming SQLite replication) — were created and released. **yourworld2** gained SQLite-backed game state with real-time bidirectional sync via sqlpipe.

**159 commits** | **+45,428 net lines** (excl. vendored deps) | **~95-150 person-days traditional equivalent** | **~25-50x multiplier**

### Major Achievements & Innovations

- **mk build tool from nothing to Homebrew in 4 days**: Designed and implemented a complete build tool language (pattern rules with glob/regex constraints, build configs with composition/exclusion, user-defined functions, `for` loops, parallel execution, fingerprinting, scoped includes) in Go, open-sourced under Apache 2.0, shipped 5 releases (v0.1.0–v0.5.0) with CI, Homebrew formula, shell completions, and self-hosting mkfile
- **Channel topology surgery** in csp: `swap`, `fuse`, `splice`, and `tap` enable runtime channel rewiring — `tap` provides RAII observation with auto-fuse-back, `splice` adds weak references and slot memory safety for safe channel graph mutation, all backed by 4 new TLA+ formal specs
- **Cancellation framework** in csp: cancel-aware [TLS via mbedTLS](https://www.trustedfirmware.org/projects/mbed-tls/), unified timer/IO suspension via reactor signals, `worker_group` supervision with restart policies and escalation — a complete structured-concurrency story
- **sqlpipe streaming replication**: Built a bidirectional SQLite replication protocol from scratch using [SQLite session extension](https://www.sqlite.org/sessionintro.html) changesets, with master/replica architecture evolving to a symmetric `Peer` class, full test suite (60+ cases), and CI pipeline
- **C++23 migration** of the entire csp codebase: deducing `this`, `requires` clauses, `std::bit_ceil`, `std::unreachable()`, `static operator()`, `std::flat_map`, `std::expected`, direct template storage replacing type-erased `std::function`
- **"The Engineering of CSP" paper series**: 6 technical papers covering TLS caching, channel lifecycle, two-phase prialt, TLA+ verification, stack engineering, and dynamic scoping — comprehensive design rationale for a novel C++ concurrency library

### Tough Challenges Overcome

- **Channel use-after-free in prialt post-wakeup path** (csp): after a prialt fires, the wakeup path was accessing channel slot state that could already be freed by the winning branch's cleanup — required careful lifetime analysis of the three-participant protocol to ensure the slot remains valid until all branches complete their CAS cleanup
- **mk pattern rule prerequisite merging**: when multiple pattern rules match a target, their prerequisites must be merged into a single dependency list without introducing cycles — required a topological analysis phase during rule resolution that detects and reports ambiguous matches
- **Homebrew version detection collision** (homebrew-tap): homebrew-releaser was extracting "64" from "arm64" in tarball filenames as the version number, causing formula generation to fail — fixed by adding an explicit `version` field to the formula
- **sqlpipe bidirectional changeset ordering**: when both peers write simultaneously, changesets can arrive out of causal order — the `Peer` class resolves this by serialising changeset application through a single event loop and returning change events from `handle_message` rather than using callbacks, ensuring deterministic conflict resolution

Contributor: Marcelo Cantos

---

## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Combinators, Topology Surgery & Cancellation (61 commits)

**The biggest effort of the week.** Continued from last week's platform build, adding major new subsystems:

- **~20 new combinators**: `parallel_map` (concurrent N-worker transform), `combine_latest` (emit tuple on any input update), `pace` (rate-limited passthrough with backpressure), `conflate` (drop intermediate values), `mux`/`demux`/`collect`, `try_map` (error-handling map), `take_until`, `any_of`/`all_of`, `chunk_by`, `foreach_emit`, `fallback`, `transpose`, `sort_merge`, `random_bytes`, RNG stream combinators in `csp::part::rand`. Four flattening strategies (`merge_all`, `concat_all`, `switch_all`, `exhaust_all`). Dead-letter channels added to `throttle`, `debounce`, and `sample`. Existing combinators refactored to accept external trigger channels and `required<T>` config structs
- **Channel topology surgery**: `swap` (atomic 4-arg channel endpoint exchange), `fuse` (join two channel halves), `splice` (insert processing between endpoints with weak refs and slot memory safety), `tap` (RAII channel observer with auto-fuse-back on destruction). Published a dedicated engineering paper on the design. 4 new TLA+ specs (`ConcurrentSwap`, `SwapWaiterRetry`, `TapLifecycle`, plus `prialt` and `swap+waiter` interaction models)
- **Supervision & cancellation**: `worker_group` with restart policies (one-for-one, one-for-all) and escalation. Cancel-aware TLS via [mbedTLS](https://www.trustedfirmware.org/projects/mbed-tls/) integration. Unified timer/IO suspension through reactor signals. `cancel.h`/`cancel.cc` cancellation token framework
- **C++23 migration**: Switched entire codebase from C++17. Applied deducing `this`, `requires` clauses, `std::bit_ceil`, `std::unreachable()`, `static operator()`, `std::flat_map`, `std::expected`, `std::popcount`, direct template storage replacing `std::function`
- **Documentation**: 6-paper ["Engineering of CSP"](https://github.com/marcelocantos/csp/tree/master/docs/papers) series (TLS caching, channel lifecycle, two-phase prialt, TLA+ verification, stack engineering, dynamic scoping). Comprehensive [reference documentation](https://github.com/marcelocantos/csp/tree/master/docs/reference) for every combinator with SVG diagrams generated from an ASCII-art DSL (replacing Mermaid). Transition-rules reference. Stack depth analyser future directions document
- **API refinements**: Renamed "microthread" to "imp" across the codebase. `csp::none` non-blocking guard for `alt`/`prialt`. `fake_clock` for deterministic time testing. `csp::local` dynamic scoping, `csp::mt_local<T>` imp-local storage. `reduce` redesigned as composable filter with `reader::single()`. Parameterless parts converted from functions to variable templates. `*_map` shims removed in favour of `map | *_all` composition. `lines()` → `split_lines()`, `fixed()` → `fixed_frames()`
- **Bug fixes**: Channel use-after-free in prialt post-wakeup path. Flaky `sample` dead-letter tests fixed with deterministic channel control. Flaky `AltManyChannels` test fixed

---

### [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) — Initial Release (5 commits, initial)

A new declarative SQLite schema migration library for C++:

- **Core library**: ~1,040 lines implementing schema extraction from live databases, structural diffing, and migration plan generation/application. Handles tables, columns, indices, triggers, and views. Header-only with vendored [doctest](https://github.com/doctest/doctest) for testing and [nlohmann/json](https://github.com/nlohmann/json) for serialization
- **JSON round-trip**: `MigrationPlan` serialises to/from JSON via nlohmann/json, enabling plan inspection and storage
- **Testing**: 56 tests across 7 test files covering schema extraction, diffing, plan application, edge cases, and JSON serialization
- **Build**: Started with GNU Makefile, migrated to mk. Vendored doctest into `vendor/include/` to remove brew dependency
- **Agent support**: `CLAUDE.md` project instructions and `agents-guide.md` with complete API reference

---

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Initial Release (12 commits, initial)

A new streaming replication protocol for SQLite:

- **Core library**: Built on [SQLite's session extension](https://www.sqlite.org/sessionintro.html) — captures changesets as they happen and streams them between peers. Initial master/replica architecture with state-request handshake, changeset framing, and resync support
- **Bidirectional replication**: Evolved to a symmetric `Peer` class replacing the master/replica split. Changed API to return change events from `handle_message` instead of using callbacks, enabling deterministic conflict resolution
- **Testing**: 60+ test cases across 6 test files (integration, master, replica, protocol, resync, peer). Loopback example demonstrating the full round-trip
- **CI and build**: GitHub Actions CI workflow. Migrated from Makefile to mk. Vendored SQLite (compiled with session/preupdate hooks), [spdlog](https://github.com/gabime/spdlog), and doctest
- **Documentation**: `CLAUDE.md`, `agents-guide.md`, comprehensive API documentation with resync diagrams and error handling docs

---

## Tooling

### [marcelocantos/mk](https://github.com/marcelocantos/mk) — From-Scratch Build Tool (39 commits, initial)

Built a modern replacement for GNU Make from scratch in Go:

- **Language**: Pattern rules with glob and regex constraints on captures. Variables (`=`, `?=`, `:=`). `$[...]` functions (`shell`, `wildcard`, `patsubst`, etc.). Multi-output rules. [Order-only prerequisites](https://www.gnu.org/software/make/manual/html_node/Prerequisite-Types.html). `[keep]` annotations. `$changed` automatic variable for incremental recipes. `[fingerprint: command]` for non-file artifact staleness. Recursive variable definition detection (parse error, not silent loop). Relative indentation preserved in recipes
- **Advanced features**: `for` loops for generating rules and variables across a matrix. Build configs with composition (`+`), exclusion, and state isolation. User-defined functions with hash cache. Parallel execution with automatic CPU capacity detection. Scoped includes with path rebasing and pattern discovery
- **Standard library**: Embedded `std/c.mk`, `std/cxx.mk`, `std/go.mk` for common build patterns
- **Release pipeline**: Apache 2.0 license. GitHub Actions CI building for darwin/arm64, linux/amd64, linux/arm64. 5 releases (v0.1.0–v0.5.0) in 4 days. [Homebrew formula](https://github.com/marcelocantos/homebrew-tap) with automated updates via [homebrew-releaser](https://github.com/Justintime50/homebrew-releaser). Shell completions for bash and zsh. Self-hosting mkfile
- **Agent support**: Embedded agents guide accessible via `--help-agent` (with CLI usage text prefix). `-C` flag for directory change. `--version` flag
- **Documentation**: Full design spec (`DESIGN.md`), README with getting started guide and mini tutorial, detailed ["Why mk?"](https://github.com/marcelocantos/mk/blob/master/docs/why-mk.md) analysis

---

### [marcelocantos/skills](https://github.com/marcelocantos/skills) — Claude Code Skills (19 commits, initial)

Created a repository of reusable [Claude Code](https://claude.ai/code) skill definitions:

- **6 skills**: `/docs` (end-to-end documentation sherpa with comprehensive document types taxonomy, agent-guide generation), `/open-source` (audit, fix, document, publish, release — delegates docs to `/docs`), `/release` (version, release notes, CI, Homebrew tap, GitHub release), `/republish-skills` (sync to GitHub with mk automation), `/progress-report` (weekly report generation from git activity), `/where` (concise session status)
- **Build**: mkfile handles syncing from `~/.claude/skills/`, README generation, diffing, committing, and pushing

---

### [marcelocantos/homebrew-tap](https://github.com/marcelocantos/homebrew-tap) — mk Distribution (6 commits, initial)

Created the Homebrew tap and iterated the mk formula through 5 versions. Evolved from source-based Go build to pre-built binary distribution with shell completion installation. Fixed version detection bug where homebrew-releaser extracted "64" from "arm64" in tarball filenames. Switched to automated formula updates via homebrew-releaser.

---

## Game Projects

### [squz/yourworld2](https://github.com/squz/yourworld2) — State Persistence & Engine Rebrand (11 commits)

- **SQLite-backed game state**: New `GameDb` class (~380 lines) wrapping [sqlift](https://github.com/marcelocantos/sqlift) to persist game state in SQLite, replacing in-memory-only `Game` struct. `Application` and `Carousel` refactored to work through `GameDb`
- **sqlpipe state sync**: Wired [sqlpipe](https://github.com/marcelocantos/sqlpipe) bidirectional replication into the game server — creates a `sqlpipe::Master` on the in-memory GameDb, sends a state-request magic byte on connect, loads received DB bytes, and streams changesets via `drainMessages`/`onMessage`. Foundation for multiplayer state replication
- **C++23 upgrade**: Bumped from C++20 to C++23 to leverage sqlift/sqlpipe APIs
- **Engine rebrand**: Renamed `sq` submodule to `ge` across all files (`.gitmodules`, Makefile, C++ includes, namespaces). 7 ge submodule updates bringing SessionHost/ged daemon architecture, sqlite3 in libge.a, parallel make, wire protocol changes
- **Codebase documentation**: 7 planning documents under `.planning/codebase/` (architecture, concerns, conventions, integrations, stack, structure, testing) — 1,468 lines mapping the existing codebase

---

## Strategic Planning & Documentation

### [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) — Agentic AI Talk (3 commits)

Created a [Marp](https://marp.app/) slide deck on agentic AI development with outline document, HTML export, and slide images (CSP architecture SVG, HAMT SVG, spherical chess screenshot, YourWorld globe screenshot). Iterated on layout (two-column spherical chess slide with repositioned screenshot).

---

## Other Team Work

### [squz/esfera2](https://github.com/squz/esfera2) — Feature Delivery & Release Engineering (18 commits, Andrew Cantos)

Andrew delivered a major feature push: TestFlight pipeline (`make testflight`) with App Store compliance fixes (privacy manifest, encryption flags), staging/production deploy pipeline with blue-green promotions, per-category Elo ratings (online vs correspondence) with server tests (~1,200 lines), WebSocket-based correspondence updates replacing REST polling, daily streak tracking with rewarded ads, landscape orientation for iPad/iPhone, online game reconnection with rejoin/forfeit, and multiple bug fixes (sphere rotation double-sensitivity, username text flicker, stale highlights). 18 commits, ~+3,400/-500 lines.

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 10 |
| Total commits | 159 |
| Total lines added | +371,092† |
| Total lines removed | -11,967 |
| Net new lines | +359,125† |
| Net new lines (excl. vendored) | +45,428 |
| File changes | 543 |
| New files created | 344 |
| Languages | C++, Go, TLA+, Python, WGSL, Ruby, YAML, Shell |

*†sqlpipe vendors sqlite3.c/sqlite3.h (+274,664 lines) and doctest.h (+7,134 lines). sqlift vendors nlohmann/json.hpp (+24,765 lines) and doctest.h (+7,134 lines). Total vendored: +313,697 lines.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 61 | 408 | +35,562 | -9,411 | +26,151 |
| [marcelocantos/mk](https://github.com/marcelocantos/mk) | 39 | 28 | +8,512 | -696 | +7,816 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 19 | 10 | +846 | -111 | +735 |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 12 | 24 | +287,694* | -1,146 | +286,548* |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 11 | 26 | +2,298 | -333 | +1,965 |
| [marcelocantos/homebrew-tap](https://github.com/marcelocantos/homebrew-tap) | 6 | 2 | +61 | -10 | +51 |
| [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) | 5 | 20 | +35,378* | -60 | +35,318* |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 3 | 3 | +529 | -17 | +512 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 2 | 13 | +85 | -85 | 0† |
| [squz/esfera2](https://github.com/squz/esfera2) | 1 | 9 | +127 | -98 | +29† |

*\*Includes vendored dependencies (see aggregate footnote).*
*†ge submodule rename only.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~200 | Topology surgery, cancellation, TLS, flattening, combinators, clock, RNG |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~60 | Integration, master, replica, protocol, resync, bidirectional peer |
| [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) | ~56 | Schema extraction, diffing, plan application, JSON round-trip |
| [marcelocantos/mk](https://github.com/marcelocantos/mk) | ~40 | Pattern rules, variables, configs, parallel execution, includes |
| **Total** | **~356** | |

---

## Ideas & Innovations

### Channel Topology Surgery ([csp](https://github.com/marcelocantos/csp))

Most CSP implementations treat channel connections as immutable: once a writer connects to a reader, the topology is fixed. csp introduces **`swap`, `fuse`, `splice`, and `tap` operations that rewire channel connections at runtime** while preserving type safety and thread safety. `tap` is particularly elegant — it interposes an observer on a live channel and automatically fuses the original connection back when the tap is destroyed (RAII). `splice` uses weak references and slot memory safety to allow safe insertion of processing stages into an existing pipeline without dangling pointers. A dedicated TLA+ specification verifies the concurrent swap protocol handles the race where two swaps target overlapping endpoints simultaneously.

### From-Scratch Build Tool to Homebrew in 4 Days ([mk](https://github.com/marcelocantos/mk))

mk demonstrates the leverage of AI-assisted development at its most extreme. The entire tool — **language design, parser, dependency graph engine, pattern matching with glob/regex constraints, build configs with composition, parallel execution, fingerprinting, standard library, CI pipeline, Homebrew formula, shell completions, documentation, and 5 shipped releases** — was conceived and delivered in a single 4-day burst. The language design itself is novel: `[fingerprint: command]` annotations let mk track non-file artifacts (like database schema versions) by command output hash, and scoped `include` with automatic path rebasing enables composable build definitions across nested project structures.

### Declarative SQLite Schema Migration ([sqlift](https://github.com/marcelocantos/sqlift))

Rather than the traditional approach of hand-writing numbered migration scripts, sqlift takes the **declarative diff approach**: you describe the desired schema, and sqlift extracts the current schema from the live database, diffs them structurally, and generates a migration plan. This eliminates the error-prone process of writing ALTER TABLE sequences by hand and ensures migrations are always correct relative to the actual database state. The plan is serialisable to JSON for inspection and approval before application.

### SQLite Streaming Replication via Session Extension ([sqlpipe](https://github.com/marcelocantos/sqlpipe))

SQLite lacks built-in replication, but its [session extension](https://www.sqlite.org/sessionintro.html) can capture row-level changesets as they happen. sqlpipe exploits this to build **streaming bidirectional replication** — each peer wraps its database in a session, captures writes as changesets, and streams them to the other peer for application. The key insight is that **changesets are self-describing and composable**: they can be serialised, transported over any byte stream, and applied idempotently. The protocol includes a resync handshake for recovering from divergence, making it suitable for unreliable networks like mobile game connections.

### Cancellation-Aware TLS in a Microthread Runtime ([csp](https://github.com/marcelocantos/csp))

Integrating TLS into a cooperative microthread scheduler creates a chicken-and-egg problem: TLS needs blocking I/O for the handshake, but the scheduler's I/O is non-blocking and cooperative. csp's solution **wraps mbedTLS with custom BIO callbacks that route through the kqueue reactor**, so TLS read/write operations suspend the current imp (microthread) and resume when data arrives — exactly like plain socket I/O. Cancellation tokens propagate through the TLS layer, so cancelling a parent scope cleanly tears down in-flight TLS connections without leaked sockets or half-completed handshakes.

### SVG Diagram Generation from ASCII Art ([csp](https://github.com/marcelocantos/csp))

The csp documentation uses dataflow diagrams for every combinator, but maintaining Mermaid diagrams alongside code proved fragile (syntax changes, rendering inconsistencies, no version control diff). The solution: **a custom ASCII-art DSL that compiles to SVG** via a Python script (`gen_diagrams.py`). Diagrams are defined inline in documentation as ASCII box-and-arrow art, which is readable in source form, diffs cleanly in git, and renders to publication-quality SVG. This eliminated the Mermaid dependency entirely and made diagrams a first-class part of the documentation workflow.

---

## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **mk** | 40-60 | Language design from first principles requires understanding parser construction, dependency graph analysis, cycle detection, and GNU Make's conceptual model. Pattern rules with constraint propagation, build configs with exclusion semantics, parallel execution with capacity detection, fingerprinting for non-file artifacts, scoped includes with path rebasing. Then: CI pipeline, Homebrew formula debugging, shell completions, self-hosting bootstrap. |
| **csp** | 30-50 | ~20 new combinators each requiring correct channel lifecycle semantics and back-pressure handling. Channel topology surgery (swap/fuse/splice/tap) is novel — no reference implementations exist. Supervision with restart policies. Cancel-aware TLS via mbedTLS requires deep understanding of both TLS state machines and cooperative scheduling. C++23 migration of a large codebase. 4 TLA+ formal specs. 6 engineering papers. Comprehensive reference docs with diagram generation. |
| **sqlpipe** | 8-12 | Streaming replication over SQLite sessions requires deep understanding of the session extension API, changeset serialisation, and conflict resolution semantics. Bidirectional peer protocol design with correct causal ordering. |
| **sqlift** | 5-8 | Schema extraction from live SQLite databases, structural diffing, and migration plan generation. Correct handling of tables, columns, indices, triggers, and views. JSON serialisation. |
| **yourworld2** | 5-8 | Wiring sqlpipe state sync into a game server requires understanding both the replication protocol and the game loop's threading model. GameDb design. Engine rebrand across all files. 1,468 lines of codebase documentation. |
| **skills** | 2-3 | Writing precise, agent-optimised skill definitions requires understanding Claude Code's execution model and tool APIs. |
| **homebrew-tap** | 1-2 | Homebrew formula iteration, debugging version detection collision, homebrew-releaser integration. |
| **progress-reports** | 1-2 | Marp slide deck design and iteration. |

### The Diversity Tax

Specialisms exercised this week:

- Language design and parser implementation (Go)
- Build system theory (dependency graphs, pattern matching, fingerprinting)
- C++ microthreading, topology surgery, supervision, cancellation
- TLA+ formal methods and model checking
- TLS protocol integration with cooperative schedulers
- SQLite session extension and replication protocols
- Schema migration algorithms
- C++23 standard library and idioms
- WebGPU/WGSL shader programming and game state architecture
- Open-source release engineering (CI/CD, Homebrew, GitHub Actions)
- Technical writing (engineering papers, reference documentation, agent guides)

No single engineer holds expertise in language design, formal verification, database replication, game engine architecture, and release engineering simultaneously.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **mk** (39 commits) | 4-8 | Language design decisions (syntax, config composition semantics), testing builds on real projects (csp, sqlift, sqlpipe), reviewing CI output |
| **csp** (61 commits) | 5-10 | Architecture decisions (cancellation design, topology surgery API), reviewing TLA+ specs, approving C++23 migration strategy |
| **sqlpipe** (12 commits) | 2-3 | Protocol design decisions, testing replication round-trips |
| **sqlift** (5 commits) | 1-2 | API review, migration plan validation |
| **yourworld2** (11 commits) | 2-3 | State sync architecture decisions, reviewing codebase docs |
| **skills** (19 commits) | 1-2 | Deciding skill scope and content |
| **Other** | 1-2 | Homebrew debugging, talk content, submodule renames |
| **Total** | **~16-30 hours** | |

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~95-150 person-days (5-8 months)** |
| Specialist team (traditional) | **~55-85 person-days (3-5 person-months)** |
| Actual human effort this week | **~16-30 hours (~2-4 person-days)** |
| **Multiplier vs. generalist** | **~25-50x** |
| **Multiplier vs. specialist team** | **~15-35x** |

The multiplier is highest for mk, where the entire journey from language design to Homebrew distribution was compressed into 4 days — a project that would typically take a single developer 2-3 months. The human contribution concentrated on design taste (mk's syntax decisions, csp's topology surgery API shape) and quality validation (testing mk on real projects, reviewing TLA+ specs, verifying sqlpipe replication semantics).

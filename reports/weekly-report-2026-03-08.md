# Weekly Progress Report — 2026-03-02…08

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Vendor omitted this week: **+43,074/−41** (marcelocantos/sqlpipe +28,228, marcelocantos/sqldeep +14,806). Excl-vendor landed lines: **+53,740/−18,144** (net **+35,596**).

## Executive Summary

A 7-day sprint across **15 repositories** spanning C++ concurrency, mobile game development, health management systems, HAMT data structures, AI agent infrastructure, SQL tooling, and game engine architecture. **csp** completed its Windows port with CI flake fixes, buffered channels, and a channel use-after-free concurrency bug fix. **jevon** (renamed from dais) was redesigned with filesystem-based session discovery, a trust model, an iOS mobile app, and QR-based server discovery. **frozen** achieved zero-allocation read paths and shipped v1.10.0 and v1.11.0. Commercial project detail: [private week 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md).

**305 commits** | **~+53,740 / ~−18,144** (excl. vendor) | **~100-165 person-days traditional equivalent** | **~25-45x multiplier**

### Major Achievements & Innovations

- **HMS2 full-stack rewrite** — detail in [private week 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md)
- **yourworld2 wave-based feature buildout** — detail in [private week 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md)
- **csp channel use-after-free fix**: diagnosed and fixed a concurrency bug where a `chan_op` destructor called `prialt_begin` on a freed `Channel` after the last endpoint was dropped on another thread — a real M:N scheduling race requiring careful lifetime analysis across OS thread boundaries
- **frozen zero-allocation read path** (v1.11.0): eliminated all allocations in `Map.Get`, `Map.Has`, `Set.Has`, `Map.Without`, and no-op `Set.With`/`Map.With` operations through `EqArgs` refactoring with embedded `EqHash` interface and distinct concrete types — benchmarked and verified with convergence targets
- **jevon iOS mobile app**: built a native [Swift](https://developer.apple.com/swift/)/[SwiftUI](https://developer.apple.com/xcode/swiftui/) iOS app with WebSocket connectivity, QR-based server discovery via camera scanning, ATS exception handling, and auto-connect on simulator — from zero to functional mobile client
- **ge protocol v4**: device identity with iOS Keychain persistence, orientation-aware sessions, safe area pipeline, serialiser discard mode for reconnect corruption, and multi-session thread safety — a substantial engine revision supporting mobile-first game deployment
- **sqldeep PostgreSQL backend**: extended the SQL transpiler from SQLite-only to dual SQLite/PostgreSQL support with backend-specific function mapping, enabling the same ergonomic FROM-first syntax against production PostgreSQL databases

### Tough Challenges Overcome

- **Channel use-after-free in M:N mode** (csp): a `Channel` object was destroyed while another imp on a different OS thread still held a live `chan_op` referencing its mutex. The `chan_op` destructor called `prialt_begin` on freed memory. Manifested as a flaky TSan/ASan failure on ARM64 CI (~50% reproduction rate). Required audit of channel destruction vs `chan_op` lifetime across the M:N scheduler
- **Reconnect wire corruption** — detail in [private week 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md)
- **Orientation rendering pipeline** — detail in [private week 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md)
- **HMS2 Go-to-C# backend migration** — detail in [private week 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md)
- **Frozen EqArgs refactoring for zero-alloc reads** (frozen): eliminating allocations in `Map.Get`/`Has` required restructuring `EqArgs` to use an embedded `EqHash` interface with distinct concrete types, fixing a hash consistency bug between `EqHash` and the default path, and ensuring the refactoring preserved correctness across all HAMT operations

Contributor: Marcelo Cantos

---

## Game Projects

### [squz/yourworld2](https://github.com/squz/yourworld2) — Wave-Based Feature Buildout (44 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md).*
### [squz/ge](https://github.com/squz/ge) (submodule) — Protocol v4 & Orientation Pipeline (19 commits)

The game engine powering yourworld2, esfera2, and multimaze2:

- **Protocol v4**: Device identity via unique per-device addresses, orientation lock removed, mDNS discovery removed in favour of explicit connection. iOS [Keychain](https://developer.apple.com/documentation/security/keychain_services) persistence for device address across app reinstalls
- **Orientation-aware sessions**: `Session::orientationRot()` for clip-space counter-rotation, `Session::width()`/`height()` for portrait-space dimensions, `Session::orientation()` accessor. Went through portrait-lock → clipRot → surface-coordinate rendering iterations before settling on clean architecture
- **Safe area pipeline**: Proper safe area insets flowing through the rendering pipeline, fixed corruption on orientation round-trips
- **Reconnect reliability**: Serialiser discard mode prevents stale buffer from corrupting wire responses on reconnect. Fixed `WebSocket` over-read race in `connectWebSocket`
- **Multi-session thread safety**: Fixed crashes with multiple concurrent players by protecting shared session state
- **Connect timeout**: Configurable connection timeout with player address persistence

### [squz/esfera2](https://github.com/squz/esfera2) — Status Bar Config (2 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md).*
### [squz/multimaze2](https://github.com/squz/multimaze2) — Crash Fix (2 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md).*
### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) — Build Automation & Visual Regression (6 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md).*
### [minicadesmobile/kart-stars](https://github.com/minicadesmobile/kart-stars) — Targets & Tracking (2 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md).*
### [minicadesmobile/dragster-mayhem](https://github.com/minicadesmobile/dragster-mayhem) — Codebase Audit (1 commit)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md).*
## Health Management System

*Commercial detail for this section is in the private sibling: [week ending 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md).*

## Other Team Work

Primarily ticket-driven work on the production Delphi application (tickets #6233, #6390, #6397, #6408). Commercial project detail: [private week 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md).

---

## Libraries & Infrastructure

### [arr-ai/frozen](https://github.com/arr-ai/frozen) — Zero-Alloc Read Path (23 commits)

Continued from last week's H128/h0 hash innovations with allocation elimination:

- **Zero-alloc read operations** (v1.11.0): Eliminated all allocations in `Map.Get`, `Map.Has`, `Set.Has` by refactoring `EqArgs` to use an embedded `EqHash` interface with distinct concrete types. Fixed hash consistency bug between `EqHash` and default path. `Map.Without` also made allocation-free
- **No-op write elimination**: `Set.With` on an existing element and `Map.With` on an existing key with same value now return without allocating, detected by hash comparison before tree traversal
- **Type-matrix correctness tests**: Comprehensive test suite exercising `Set` and `Map` across diverse key/value types (int, string, struct, pointer, interface) to verify generic specialisation correctness
- **Releases**: v1.10.0 (EqArgs refactor, allocation elimination), v1.11.0 (zero-alloc reads, type-matrix tests). Convergence target 🎯T2 achieved

### [arr-ai/arrai](https://github.com/arr-ai/arrai) — CI Modernisation & Perf Audit (20 commits)

- **CI modernisation**: Go 1.24, golangci-lint v1.64.8, Node version bump. Fixed deprecated lint config, gofmt double blank lines, errcheck failures, Dockerfile Go version. WASM CI path fix for Go 1.24+
- **Frozen v1.11.0**: Updated to pick up zero-alloc read optimisations, regenerated stdlib bundles
- **Performance audit**: Benchmark artifacts, dict union regression test, npm security fixes (svgo Billion Laughs DoS, serialize-javascript vulnerability)
- **Agent guide**: Added `--help-agent` flag with agent guide symlink, NOTICES file for third-party attribution
- **goreleaser v2**: Fixed deprecated config fields, PAT for tag-triggered releases

---

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — CI Stabilisation & Buffered Channels (62 commits)

Continued from last week's Windows port with stabilisation and new features:

- **Channel use-after-free fix**: Diagnosed and fixed `prialt_begin_impl` crash where `chan_op` destructor accessed freed `Channel` mutex. A real M:N scheduling race — the last endpoint dropped on thread A while thread B's `chan_op` destructor hadn't fired. Required careful lifetime analysis of channel vs `chan_op` across OS thread boundaries
- **CI flake fixes**: LSan memory leak in `context.test.cc` (heap-allocated `std::function` bypassing destructor via non-local fcontext jump — switched to caller-managed storage). Throttle budget reset flake (migrated to `fake_clock`). Watchdog timing flake (widened threshold under TSan). Swap storm race (barrier ensures swaps complete before writes). Multiple MN timer/thread flakes (use `csp::yield()` instead of busy loops)
- **Buffered channels**: Full buffered channel implementation with configurable capacity, integrated into the existing channel infrastructure
- **Windows port completion**: Fixed MSVC compilation errors (`__has_feature`, MASM assembly, `%lu` format for `size_t`, 64-bit pointer truncation via `~15UL`). POSIX header guards (`#ifndef _WIN32`). Demand-commit stacks with VEH handler for `MEM_RESERVE` pages. Exception dispatch fix — separate trampoline/finish PROCs for MSVC x64 unwind. Console signal tests using `win::signal::raise()`. `maybe_shrink` disabled on Windows to prevent double-fault during exception dispatch
- **CI improvements**: Windows CI with crash diagnostics, `workflow_dispatch` trigger, test exclusions for isolation. Run `test-dist` with both `TLS=1` and `TLS=0`. mbedTLS sanitiser false positive suppression
- **Documentation**: Imp exit/supervision documentation. Namespace-prefixed reference doc headers. Normalised header references to distribution header `csp.h`. Stopped generating `AGENTS-CSP.md`, maintaining it directly in `dist/`
- **Release**: v0.3.0 with stability tracking, completed Windows port

---

### [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) — PostgreSQL Backend (7 commits)

Continued from last week's SQLite-focused transpiler:

- **PostgreSQL backend**: Extended the transpiler to generate [PostgreSQL](https://www.postgresql.org/)-compatible SQL alongside SQLite. Backend-specific function mapping (e.g. `json_group_array` → `json_agg`, `json_object` → `json_build_object`). Shared test infrastructure with YAML test data for both backends
- **C public API**: Made `C` the sole public API entry point, moved distribution files to `dist/`
- **JSON path extraction tests**: Expanded test coverage for JSON path operations
- **Release**: v0.5.0

### [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) — C-Only Public API (5 commits)

- **API consolidation**: Merged `sqlift_c.h`/`sqlift_c.cpp` into `sqlift.h`/`sqlift.cpp` — the public header is now pure C with `extern "C"` linkage and JSON data interchange. C++ types remain implementation-internal. All tests rewritten against the C API. Go CGo includes updated. All documentation (reference, guide, getting-started, agents-guide) rewritten from C++ to C
- **Release**: v0.12.0

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Go Wrapper & Callback Logging (5 commits)

- **Go wrapper**: Added Go bindings via CGo for the sqlpipe C API, enabling Go applications to use streaming SQLite replication
- **Callback logging**: Replaced [spdlog](https://github.com/gabime/spdlog) dependency with user-provided callback logging, eliminating the compiled dependency
- **Schema hashing**: Integrated sqlift v0.12.0 for schema fingerprinting, enabling drift detection across replicas
- **Distribution layout**: Reorganised with `dist/` directory structure
- **Release**: v0.7.0

---

## Tooling

### [marcelocantos/jevon](https://github.com/marcelocantos/jevon) — Rename, iOS App & Security Model (24 commits)

Renamed from dais (multi-session Claude Code orchestrator), with major architectural changes:

- **Rename**: Full project rename from dais to jevon, shepherd to Jevon, across all code, docs, and configuration
- **Session discovery rewrite**: Replaced `workers` database table with filesystem-based session discovery. Active sessions detected by scanning Claude Code session directories, eliminating stale-state issues. Relevance-ranked session selection replaces fixed age filter
- **Trust model**: Formal security architecture with defined trust boundaries, capability restrictions, and tool filtering. Jevon instructed to ask questions as plain conversational text, inappropriate tools disabled
- **iOS mobile app**: Native [Swift](https://developer.apple.com/swift/)/[SwiftUI](https://developer.apple.com/xcode/swiftui/) client with [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) connectivity to the jevon daemon. ATS exception for local network access. Simulator auto-connect at app level (not transport level, fixing reconnect storm)
- **QR-based server discovery**: Camera-based QR code scanning to discover the jevon server address and port, eliminating manual configuration
- **Test coverage**: 61 tests across 7 packages covering jevon, db, mcpserver, and server. Convergence targets 🎯T1, 🎯T2, 🎯T3 achieved

### [marcelocantos/doit](https://github.com/marcelocantos/doit) — MCP Integration & Test Coverage (16 commits)

Continued from last week's three-level capability broker:

- **MCP integration**: Public `engine` and `mcptools` packages exposing doit's policy engine as [MCP](https://modelcontextprotocol.io/) tools. New `doit-mcp` binary for direct MCP server usage. `sh -c` execution path in engine, bypassing the pipeline parser for `Command` requests
- **Test coverage**: Comprehensive test suites for `internal/cap`, `internal/cap/builtin`, `internal/config`, `internal/cli`, and `cmd/doit` packages. MCP integration tests with daemon testdata. Convergence targets 🎯T4 (per-project policy) and 🎯T5 (test coverage) achieved
- **Per-project policy**: Configuration support for project-specific policy overrides, allowing different policy profiles per repository

### [marcelocantos/solarmon](https://github.com/marcelocantos/solarmon) — Solar Inverter Monitor (1 commit, initial)

- **Initial release**: Go application monitoring [GoodWe](https://www.goodwe.com/) solar inverters via ping + [SEMS API](https://www.semsportal.com/). Tracks inverter online status and energy production

### [marcelocantos/mcpsafe](https://github.com/marcelocantos/mcpsafe) — MCP Safety Library (1 commit, initial)

- **Initial commit**: Go library for safe MCP tool execution patterns

### [marcelocantos/skills](https://github.com/marcelocantos/skills) — Skill Syncs (31 commits)

- **Automated syncs**: 31 skill publishes reflecting ongoing workflow refinements — convergence system improvements, `/wrap` skill creation, context compression handling, parallel fan-out support in `/cv`

### [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) — Journey Narrative (2 commits)

- **"The Journey So Far"**: Added narrative section to README contextualising the 25-day, 746-commit, 1.9-3.3 year equivalent body of work

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 20 (15 with substantial development) |
| Total commits | 305 |
| Total lines added | +228,566† |
| Total lines removed | −18,144 |
| Net new lines | +187,982† |
| Net new lines (excl. vendored/generated) | ~+96,000 |
| File changes | 2,286 |
| Languages | C++, Go, C#, Svelte, Swift, SQL, TLA+, Shell, YAML, HTML, JavaScript |
| Contributors | 1 (Marcelo Cantos) |

*†sqlpipe vendors sqlift + sqlite3_impl.c (~57k lines). sqldeep vendors fkYAML + dist files (~33k). hms includes package-lock.json (~1.5k).*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 62 | 526 | +17,372 | -6,408 | +10,964 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 44 | 238 | +13,169 | -2,033 | +11,136 |
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | 34 | 643 | +59,869 | -14,700 | +45,169* |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 31 | 111 | +4,877 | -352 | +4,525† |
| [marcelocantos/jevon](https://github.com/marcelocantos/jevon) | 24 | 137 | +6,394 | -2,897 | +3,497 |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | 23 | 99 | +2,593 | -581 | +2,012 |
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | 20 | 61 | +3,862 | -673 | +3,189 |
| ge (submodule) | 19 | 135 | +6,132 | -4,480 | +1,652 |
| [marcelocantos/doit](https://github.com/marcelocantos/doit) | 16 | 58 | +7,508 | -406 | +7,102 |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | 7 | 62 | +33,828 | -2,050 | +31,778* |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 6 | 42 | +1,404 | -61 | +1,343 |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 5 | 79 | +64,873 | -522 | +64,351* |
| [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) | 5 | 63 | +5,601 | -5,404 | +197 |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 2 | 2 | +36 | 0 | +36† |
| [squz/esfera2](https://github.com/squz/esfera2) | 2 | 2 | +2 | -2 | 0‡ |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 2 | 2 | +6 | -7 | -1‡ |
| [minicadesmobile/kart-stars](https://github.com/minicadesmobile/kart-stars) | 2 | 6 | +94 | -8 | +86§ |
| [marcelocantos/solarmon](https://github.com/marcelocantos/solarmon) | 1 | 3 | +336 | 0 | +336 |
| [marcelocantos/mcpsafe](https://github.com/marcelocantos/mcpsafe) | 1 | 1 | +201 | 0 | +201 |
| [minicadesmobile/dragster-mayhem](https://github.com/minicadesmobile/dragster-mayhem) | 1 | 3 | +389 | 0 | +389§ |

*\*Includes vendored dependencies or generated content.*
*†Automated skill syncs / meta.*
*‡ge submodule updates only.*
*§Audit/targets only.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/doit](https://github.com/marcelocantos/doit) | ~230 | MCP integration, cap/builtin/config/cli packages, smoke tests (all new) |
| [marcelocantos/jevon](https://github.com/marcelocantos/jevon) | ~76 | 61 tests across 7 packages: jevon, db, mcpserver, server |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~52 | Buffered channels, CI flake fixes, Windows signal, swap storm barrier |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | ~34 | Type-matrix correctness tests, Map.Get/Without benchmarks |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | ~28 | PostgreSQL backend, JSON path extraction |
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | ~2 | Dict union regression test |
| **Total** | **~422** | |

---

### Daily Activity

![Daily active repositories](daily-activity-2026-03-08.svg)

## Ideas & Innovations

### Wave-Based Parallel Feature Delivery ([yourworld2](https://github.com/squz/yourworld2))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md).*
### Serialiser Discard Mode for Reconnect Safety ([ge](https://github.com/squz/ge))

Wire-based remote rendering faces a subtle problem on client reconnect: the server-side serialiser may hold buffered state from the previous session (partial messages, stale sequence numbers, accumulated deltas). Sending a fresh game state through a **serialiser with stale buffer state corrupts the wire protocol**. ge solves this by introducing a discard mode that clears all serialiser state upon detecting a reconnect, ensuring the fresh session starts with a clean serialisation context. Combined with inferring device orientation from surface dimensions (rather than round-tripping through the wire protocol), this eliminated a class of reconnect corruption bugs.

### Filesystem-Based Session Discovery ([jevon](https://github.com/marcelocantos/jevon))

The original dais design used a `workers` database table to track Claude Code sessions, but this created stale-state problems — sessions that crashed or were killed left orphan records. jevon replaces this with **filesystem-based discovery**, scanning Claude Code's session directories directly. A session is "active" if its directory exists and was recently modified. This eliminates the entire category of stale-record bugs and adds **relevance-ranked selection** — sessions are scored by recency and activity rather than filtered by a fixed age threshold, naturally surfacing the most contextually useful sessions.

### EqHash Interface Embedding for Zero-Alloc Generics ([frozen](https://github.com/arr-ai/frozen))

Go's generics with type constraints don't naturally support zero-allocation polymorphism — interface dispatch typically requires heap allocation for the receiver. frozen's `EqArgs` refactoring solves this by **embedding the `EqHash` interface into concrete types** that carry their hash/equality functions as struct fields rather than interface values. The distinct concrete types (`eqArgsDefault`, `eqArgsCustom`) avoid the interface allocation while still supporting polymorphic dispatch at the HAMT node level. This architectural pattern — concrete types embedding interfaces for zero-alloc generic dispatch — is broadly applicable to performance-critical Go generics code.

### QR-Based Cross-Device Session Transfer ([hms](https://github.com/Health-Management-Systems/hms))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-03-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-08.md).*
## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **yourworld2** | 20-30 | Complete game feature buildout from globe renderer — 5 game modes, tutorial system, achievement persistence, menu/overlay architecture, audio integration, orientation-aware rendering pipeline with multiple failed approaches before convergence |
| **hms** | 20-30 | Full-stack rewrite spanning C#/ASP.NET backend, SvelteKit SPA, SQL Server stored procedures, TOTP MFA, QR session transfer with trampoline pages, MDI workspace with deep linking — 30+ screens across 16 API domains |
| **csp** | 15-25 | Channel use-after-free diagnosis across M:N scheduler thread boundaries, multiple CI flake root-cause analyses (fcontext destructor bypass, timing sensitivity under TSan, swap race), MSVC x64 exception unwind debugging, demand-commit VEH handler |
| **jevon** | 10-15 | Project rename (full codebase), filesystem-based session discovery replacing database, formal trust model, native Swift/SwiftUI iOS app with WebSocket and QR scanning, reconnect storm debugging |
| **ge** | 8-12 | Protocol revision (v4), orientation rendering pipeline with multiple iterations, serialiser discard mode, Keychain persistence, multi-session thread safety across C++ game engine |
| **frozen** | 5-8 | Zero-allocation read path through EqArgs/EqHash refactoring, hash consistency fix, type-matrix test design, two releases |
| **doit** | 5-8 | MCP tool integration, sh -c execution bypass, comprehensive test suites across 5 packages, per-project policy configuration |
| **arrai** | 3-5 | CI modernisation across Go/Node/lint/Docker/WASM, security vulnerability fixes, goreleaser v2 migration |
| **SQL stack** (sqldeep/sqlift/sqlpipe) | 5-8 | PostgreSQL backend transpilation, C-only API consolidation with full test/doc rewrite, Go CGo wrapper, callback logging replacing compiled dependency |
| **stock-car-racing** | 2-3 | Build automation extraction, visual regression testing system |
| **Other** | 2-3 | solarmon initial, mcpsafe initial, dragster-mayhem audit, kart-stars targets |

### The Diversity Tax

Specialisms exercised this week:

- C++ M:N scheduler debugging and channel lifetime analysis
- MSVC x64 exception dispatch and VEH demand-commit handlers
- Game engine architecture (orientation pipelines, serialiser state machines, wire protocols)
- Mobile game design (wave-based feature delivery, tutorial systems, achievement persistence)
- C#/ASP.NET Core backend with SQL Server stored procedures
- [SvelteKit](https://svelte.dev/) SPA with Svelte 5 components and deep linking
- TOTP multi-factor authentication and QR-based session transfer
- Swift/SwiftUI iOS app development with WebSocket and camera APIs
- HAMT data structure optimisation with zero-allocation generics patterns
- SQL transpiler construction with multi-backend code generation
- [MCP](https://modelcontextprotocol.io/) tool integration and policy engine architecture
- Go test infrastructure and convergence-target-driven development
- CI/CD across GitHub Actions (Go, C++, Node, WASM, Windows MSVC)
- Unity build automation and visual regression testing
- Solar inverter monitoring APIs

No single engineer holds expertise in C++ M:N schedulers, game engine orientation pipelines, SvelteKit SPAs, TOTP authentication, Swift/SwiftUI, HAMT zero-alloc optimisation, SQL transpiler backends, and MCP tool integration simultaneously.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **yourworld2** (44 commits) | 5-8 | Game design decisions (mode selection, tutorial flow, achievement criteria), play-testing on iPad, orientation rendering approach iteration, aesthetic judgement on carousel placement |
| **hms** (34 commits) | 4-6 | Architecture decisions (Go→C# migration, SvelteKit over vanilla JS), QR transfer security design, MDI UX review, screen layout approval |
| **csp** (62 commits) | 3-5 | Channel lifetime debugging direction, CI flake triage priorities, Windows port review |
| **jevon** (24 commits) | 3-4 | Session discovery architecture, trust model design, iOS app UX review |
| **ge** (19 commits) | 2-3 | Protocol v4 design, orientation pipeline iterations |
| **Other** | 4-6 | frozen API design, doit MCP architecture, SQL stack release coordination, arrai CI review |
| **Total** | **~21-32 hours** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | Ramp-up cost |
|---------|------------|-----------------|--------------|
| yourworld2 | 20-30 | 30-45 | +8 (game design, orientation math, overlay architecture) |
| hms | 20-30 | 30-45 | +10 (C#/ASP.NET, SvelteKit, SQL Server, TOTP, QR security) |
| csp | 15-25 | 25-40 | +8 (M:N schedulers, MSVC exception dispatch, VEH handlers) |
| jevon | 10-15 | 15-22 | +5 (Swift/SwiftUI, WebSocket, QR scanning) |
| ge | 8-12 | 12-18 | +4 (wire protocol, orientation rendering, Keychain) |
| frozen | 5-8 | 8-12 | +3 (HAMT internals, Go generics performance) |
| doit | 5-8 | 8-12 | +3 (MCP protocol, policy engines) |
| arrai | 3-5 | 5-8 | +2 (golangci-lint migration, WASM CI) |
| SQL stack | 5-8 | 8-12 | +3 (SQL transpilation, CGo, multi-backend) |
| Other | 4-6 | 6-10 | +3 |
| **Subtotal** | **95-147** | **147-224** | **+49** |
| Context-switching tax (30%) | | +44-67 | |
| **Total** | | **191-291** | |

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~100-165 person-days (5-9 months)** |
| Specialist team (traditional) | **~60-100 person-days (3-5 person-months)** |
| Actual human effort this week | **~21-32 hours (~3-4 person-days)** |
| **Multiplier vs. generalist** | **~25-45x** |
| **Multiplier vs. specialist team** | **~15-30x** |

The multiplier is highest for the HMS2 rewrite, where delivering 30+ screens across a C#/SvelteKit/SQL Server stack with MFA, QR transfer, and deep linking in one week would be extraordinary even for a dedicated team. It's also high for yourworld2's wave-based game buildout, where the ability to fan out parallel agents on independent feature waves (menu, tutorial, achievements, encyclopedia) compressed what would normally be weeks of sequential game development into a day. The multiplier is lowest for the orientation pipeline work in ge/yourworld2, where multiple failed approaches (portrait-lock, clipRot, surface rendering) required human iteration and judgement to converge on the right architecture. The human contribution concentrated on architectural taste (Go→C# migration decision, session discovery redesign, protocol v4 design), game design (mode selection, tutorial flow, carousel aesthetics), and debugging direction (channel use-after-free triage, orientation rendering iteration).

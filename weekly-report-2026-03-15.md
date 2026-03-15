# Weekly Progress Report — 2026-03-09…15

## Executive Summary

A 7-day sprint across **13 repositories** spanning GPU compute shader optimisation, healthcare ERP buildout, iOS Lua runtime construction, C++ concurrency research, SQL transpiler evolution, Go iterator library modernisation, HAMT allocation tuning, MCP server architecture, and Wasm compilation. **yourworld2** delivered a GPU-accelerated visual parity optimizer using Jump Flood Algorithm compute shaders and differential evolution, plus three waves of game features (hints, magnification, menus, tutorials, achievements, encyclopedia). **hms** completed a five-wave HMS2 implementation covering 50 convergence targets across C#/SvelteKit/SQL Server. **cworkers** went from initial commit to v0.9.0 with MCP server, SQLite persistence, and a Svelte real-time dashboard in one week. **jevon** built a server-driven iOS app with an embedded Lua 5.1.5 runtime rendering SwiftUI from server-pushed scripts. **sqldeep** shipped three releases including recursive tree construction via SQL-only bracket injection.

**228 commits** | **~+130,000 net lines** (excl. vendored) | **~110-175 person-days traditional equivalent** | **~25-45x multiplier**

### Major Achievements & Innovations

- **GPU-accelerated visual parity optimizer** in yourworld2: a full compute shader pipeline — [Sobel](https://en.wikipedia.org/wiki/Sobel_operator) edge detection, [JFA](https://en.wikipedia.org/wiki/Jump_flooding_algorithm) init/step/distance, [Chamfer distance](https://en.wikipedia.org/wiki/Chamfer_distance) reduction with overflow-safe atomics — feeding a [differential evolution](https://en.wikipedia.org/wiki/Differential_evolution) optimizer that tunes ~17 rendering parameters at ~50 evaluations/sec on M4 Max. Zero-copy GPU pipeline renders directly into compute textures. Live web dashboard with score charts and edge-diff overlays
- **Server-driven iOS UI with embedded Lua** in jevon: the server pushes Lua scripts over WebSocket, the iOS client embeds Lua 5.1.5 and executes them locally to build native SwiftUI views. `LuaRuntime.swift` (782 lines) exposes 26 SwiftUI builder functions and 15 modifier properties. Server retains all business logic; the client is a pure renderer
- **cworkers MCP server from scratch to v0.9.0 in one week**: 9 tagged releases replacing a Unix socket CLI protocol with a single `cwork(task, cwd, model?)` MCP tool over streamable HTTP, self-warming worker pool, shadow auto-discovery of Claude transcripts, SQLite persistence, and a Svelte real-time dashboard (~4,000 lines) with SSE-driven session trees and ANSI log rendering via [xterm.js](https://xtermjs.org/)
- **HMS2 five-wave implementation** in hms: 50 convergence targets achieved — recurrence engine with CHSP/DVA budget-aware scheduling (451 lines), SSE multiplexer for streaming search (542 lines), RBAC enforcement with field-level security, transport route optimisation with GPS live map ([Leaflet](https://leafletjs.com/)), GL tree, equipment tracking, group attendance, 18 deep-linkable pages
- **Recursive tree construction in SQL** in sqldeep (v0.8.0): `RECURSE ON (parent_id)` transpiles to a 3-CTE bracket-injection template — recursive DFS, row numbering with JSON, opening/closing bracket fragments sorted by path — producing nested JSON entirely within SQL via `group_concat`. Works on both SQLite and PostgreSQL
- **linqgo/linq v2 with `iter.Seq` API**: merged the range-func branch replacing channel-based iteration with Go 1.23 [iter.Seq](https://pkg.go.dev/iter), eliminating goroutine overhead across 150 files (+3,720/-2,706 lines)
- **sqlpipe Wasm build**: compiled to [WebAssembly](https://webassembly.org/) via [Emscripten](https://emscripten.org/), with TypeScript wrapper and live browser demo — bidirectional SQLite sync running entirely client-side

### Tough Challenges Overcome

- **TSan race in processor slot reuse** (csp): `set_maxprocs` reused dead processor slots by resetting `unique_ptr` contents, but `steal_work` on another thread could race on the pointer. Root cause: teardown of the old processor object while another thread reads its `alive` flag. Fixed by resetting processor state in-place with `memory_order_release` barrier instead of reallocating
- **golangci-lint v2 crashes on complex generics** (linq): the linter crashed repeatedly on linq's heavily generic codebase. Nine commits of investigation before pinning golangci-lint v1.62 with Go 1.23 as the working combination — a pragmatic decision after exhausting v2 compatibility options
- **Cube map orientation iterations** (yourworld2): equirectangular-to-cube-map conversion required multiple rounds of orientation correction — the generated faces were flipped, rotated, or had incorrect winding. Converged by building `gen_cubemap.py` with [Natural Earth](https://www.naturalearthdata.com/) shapefile water detection to validate orientation (blue ocean tinting confirms face identity)
- **sqlpipe bidirectional sync wire format** (jevon/sqlpipe): integrating sqlpipe state sync into the jevon iOS app required a C API wrapper (824 lines) and Swift `SyncPeer` wrapper (504 lines) with multiple wire format iterations to handle the Go sync manager, C layer, and Swift layer all speaking the same protocol
- **HMS SSE multiplexer design** (hms): streaming search results with infinite scroll over [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) required `MultiplexSession.cs` (542 lines) to manage concurrent query streams, backpressure, and client disconnection without leaking server resources

Contributor: Marcelo Cantos

---

## Game Projects

### [squz/yourworld2](https://github.com/squz/yourworld2) — Parity Optimizer & Feature Waves (49 commits)

**The biggest effort of the week.** Continued from last week's wave-based feature buildout, now adding GPU compute and three more feature waves:

- **GPU-accelerated parity optimizer** (`bin/parity`): a full compute shader pipeline measuring visual distance between the new renderer and the original app. Five [WGSL](https://www.w3.org/TR/WGSL/) compute shaders: Sobel edge detection, JFA initialisation, JFA step (log-time distance field), distance transform, and Chamfer reduction with overflow-safe atomics. [Differential evolution](https://en.wikipedia.org/wiki/Differential_evolution) optimizer (`DiffEvolution.h`) with adaptive mutation and population restart, tuning ~17 rendering parameters (atmosphere density, lighting angles, colour curves). Zero-copy GPU pipeline renders directly into compute textures — no readback. ~50 evaluations/sec on M4 Max. Live web dashboard (`ParityServer`) with score history charts and edge-diff overlays
- **Cube map rendering pipeline**: `gen_cubemap.py` converts equirectangular textures to cube maps with [Natural Earth](https://www.naturalearthdata.com/) shapefile-based water detection for blue ocean tinting and land gamma/saturation adjustment. `atlas_2d.wgsl` for carousel rendering, `texture_cube` sampling for globe. Multiple orientation-fix iterations
- **Wave 2 — Gameplay depth**: auto-zoom via critically damped harmonic oscillator (`HarmonicValue.h`), hint system with compass bearing, magnification lens via screen-space vertex shader distortion, country flags from sprite atlas, audio integration (SFX + music), HUD overlay
- **Wave 3 — Polish systems**: menu system with overlay stack, level completion ceremony (Card overlay), tutorial system with contextual positioned bubbles and SQLite-persisted progress flags, local achievements with SQLite persistence, encyclopedia with Wikipedia deep links
- **Atmosphere rendering**: dedicated `atmosphere.wgsl` shader with premultiplied alpha blending, directional lighting, glow effects. Globe blend modes matching original app
- **GameDb rewrite**: migrated from sqlift ORM to raw SQLite via RAII `SqliteDb` wrapper for simpler state management
- **Asset preparation**: ~4,800 lines of JSON data (cities, landmarks, flags, Wikipedia URLs) converted from original app data
- **ge submodule**: 18 pointer updates (wire filter for cube maps, reconnect corruption fix, safe area fixes, `Tweak<vector<string>>`)

### [squz/esfera2](https://github.com/squz/esfera2) — ge Submodule Update (2 commits)

- **Submodule**: ge repointing to squz/ge org

### [squz/multimaze2](https://github.com/squz/multimaze2) — ge Submodule Update (2 commits)

- **Submodule**: ge repointing to squz/ge org

### [squz/ge](https://github.com/squz/ge) (submodule) — Wire Fixes & Safe Area (3 commits)

- **Wire serialiser corruption fix**: stale buffer state cleared on reconnect
- **Safe area pipeline**: proper inset flow with orientation inference from surface dimensions
- **Tweak extension**: `Tweak<vector<string>>` support for configurable string lists

---

## Health Management System

### [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) — Five-Wave HMS2 Implementation (33 commits)

Continued from last week's full-stack rewrite with five implementation waves completing the HMS2 feature surface:

- **Wave 3 — Clinical core**: patient and episode detail views, budget management with CHSP/DVA funding model awareness, scheduling engine, dynamic episode layouts varying by program type. 10 deep-linkable pages
- **Wave 4 — Operational systems**: healthcare extracts, [HL7](https://www.hl7.org/) integration, staff management with RBAC enforcement (middleware-based, field-level security, permission-aware menus), transport route optimisation with GPS live map via [Leaflet](https://leafletjs.com/) and driver tracking, meal planning
- **Wave 5 — Administrative breadth**: GL tree, equipment tracking, group attendance, reporting engine, data explorer, campaigns, contracts, checklists, correspondence, todo management, org chart, external monitoring, document viewer
- **SSE multiplexer**: `MultiplexSession.cs` (542 lines) for streaming search results with infinite scroll over [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events), managing concurrent query streams and backpressure
- **Recurrence engine**: `RecurrenceEngine.cs` (451 lines) with budget-aware scheduling — tracks CHSP and DVA funding allocations, generates recurring appointments respecting budget limits
- **URL state tracking**: 18 pages with deep-linkable URLs, full back/forward/refresh support
- **50 convergence targets achieved** across all 6 waves (including last week's Waves 1-2)

---

## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Processor Reuse & Research Papers (12 commits)

Continued from last week's Windows port and channel fixes:

- **Processor slot reuse**: dead surplus processor slots now reset in-place via `Processor::reset()` rather than reallocating, avoiding a race with `steal_work` on `unique_ptr`. `set_maxprocs` replaces `init_runtime` with a runtime-adjustable API for dynamic processor pool sizing
- **TSan race fix**: root cause — processor reuse tearing down the object while another thread reads the `alive` flag on a stale pointer. Fixed with in-place reset and `memory_order_release` fence
- **Multi-room chat server**: worked CSP example (622 lines) demonstrating channel-based actor patterns for concurrent connection handling
- **Research papers**: Paper 12 (Verification Architecture), Paper 13 (Formal Foundations — 4-axiom system deriving race-freedom, orphan-block freedom, and cleanup freedom), Paper 14 (Mutex-to-Channel Migration)

### [arr-ai/frozen](https://github.com/arr-ai/frozen) — No-Op Allocation Elimination (5 commits)

Continued from last week's zero-alloc read path:

- **No-op write elimination** (v1.11.0): `Set.With` on an existing element and `Map.With` on an existing key with the same value now return the original node without allocating. Detection by hash comparison before tree traversal
- **Type-matrix correctness tests**: parametric tests across int, string, float64, derived types, and structs. Independence tests verify that `Set[int]` and `Set[ID]` (where `ID` is `type ID int`) do not collide in the HAMT

### [linqgo/linq](https://github.com/linqgo/linq) — v2 iter.Seq Migration (16 commits)

- **v2 release**: merged range-func branch — all `Query[T]` now wraps [iter.Seq[T]](https://pkg.go.dev/iter) instead of channels, eliminating goroutine overhead. 150 files changed, +3,720/-2,706 lines. A fundamental API shift aligning with Go 1.23's iterator protocol
- **golangci-lint CI battle**: 9 commits fighting golangci-lint v2 crashes on heavily generic code. Eventually pinned v1.62 with Go 1.23 as the stable combination
- **Benchmarks and documentation**: new benchmarks for iterator-based paths, examples updated, README rewritten for v2

### [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) — Recursive Trees & Dialect Compat (19 commits)

Three releases continuing from last week's PostgreSQL backend:

- **Recursive tree construction** (v0.8.0): `SELECT/1 { id, name, children: * } FROM categories RECURSE ON (parent_id)` transpiles to a 3-CTE bracket-injection template — `_sdq_dfs` (recursive DFS with cycle detection), `_sdq_ranked` (row numbering + JSON column generation), `_sdq_events` (opening/closing bracket fragments sorted by DFS path). `group_concat` assembles nested JSON entirely within SQL. Supports both SQLite and PostgreSQL
- **SQL dialect compatibility** (v0.7.0): `--` comment support, context-sensitive `->` / `->>` JSON operators (parsed as comparison/shift in non-JSON contexts, as JSON extraction in JSON contexts)
- **Aggregate fields and computed keys** (v0.6.0): aggregate expressions in field lists, computed join keys for non-FK relationships
- **Fixed-point comprehensions paper**: 744-line theoretical foundations document on the algebraic semantics underlying sqldeep's query model

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Wasm Build & Go Wrapper (6 commits)

- **Wasm build**: compiled to [WebAssembly](https://webassembly.org/) via [Emscripten](https://emscripten.org/), with TypeScript wrapper class and live browser demo for bidirectional SQLite sync running entirely client-side
- **Self-contained Go wrapper**: dropped `mattn/go-sqlite3` dependency, owns raw `sqlite3*` handle directly. CGo trampoline for callbacks. Zero external dependencies. 33 tests
- **Auto schema migration + one-shot query API**: simplified integration surface for Go consumers
- **QueryWatch extraction**: standalone query subscription engine for reactive UI patterns

---

## Tooling

### [marcelocantos/cworkers](https://github.com/marcelocantos/cworkers) — MCP Server & Dashboard (37 commits)

Nine tagged releases (v0.1.0 through v0.9.0) in one week, transforming a socket-based CLI tool into a production MCP server:

- **MCP server rewrite**: replaced Unix socket CLI protocol (6 subcommands) with a single `cwork(task, cwd, model?)` [MCP](https://modelcontextprotocol.io/) tool over streamable HTTP on port 4242, using [mcp-go](https://github.com/mark3labs/mcp-go). Fundamental protocol simplification — callers invoke one tool instead of managing socket lifecycle
- **Self-warming worker pool**: each dispatch triggers replacement spawn to maintain pool depth. Fixed cold-pool bootstrapping where initial requests saw no available workers
- **Shadow auto-discovery**: locates the Claude transcript from the caller's working directory, eliminating manual shadow/unshadow commands. Supports multiple concurrent sessions
- **Content-driven progress**: parses worker output for markdown headings, forwards them as MCP progress notifications for real-time status visibility
- **SQLite persistence + Svelte dashboard**: real-time monitoring UI (~4,000 lines in a single commit) — sessions grouped by working directory, worker status indicators, log streaming with ANSI rendering via [xterm.js](https://xtermjs.org/), session tree visualisation. [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) for live updates
- **Session-scoped workers**: workers tied to session lifecycle with queryable status

### [marcelocantos/jevon](https://github.com/marcelocantos/jevon) — Server-Driven Lua UI & State Sync (30 commits)

Continued from last week's iOS app and trust model with a radical UI architecture:

- **Server-driven UI with Lua**: the jevon daemon sends Lua scripts over WebSocket; the iOS client embeds [Lua 5.1.5](https://www.lua.org/manual/5.1/) and executes them locally to construct native SwiftUI views. `LuaRuntime.swift` (782 lines) registers 26 SwiftUI builder functions (`text`, `vstack`, `hstack`, `button`, `textfield`, `list`, `image`, `toggle`, `picker`, `scrollview`, etc.) and 15 modifier properties (`font`, `padding`, `frame`, `background`, `cornerRadius`, `opacity`, `foregroundColor`, etc.) into the Lua environment
- **Lua action handling**: server-side callbacks (`on_submit`, `on_tap`) invoked over WebSocket. Transcript management, file I/O, timer, and notification primitives exposed from Lua
- **sqlpipe state sync (T10)**: bidirectional SQLite synchronisation — Go sync manager, C API wrapper (824 lines), Swift `SyncPeer` wrapper (504 lines). Vendored sqlpipe with all dependencies. Multiple wire format iterations to align Go, C, and Swift layers
- **sqldeep integration**: vendored the sqldeep transpiler into the iOS query pipeline for ergonomic FROM-first queries
- **QR code scanning**: camera-based server discovery for zero-configuration device pairing
- **MCP tools**: transcript read/rewind for external agent inspection of jevon sessions

### [marcelocantos/mpe2pdf](https://github.com/marcelocantos/mpe2pdf) — Open-Source Release Prep (5 commits)

- **Release preparation**: Apache-2.0 licensing, `STABILITY.md`, agent guide (`--help-agent`), npm publish configuration fixes

### [marcelocantos/skills](https://github.com/marcelocantos/skills) — Skill Syncs (6 commits)

- **Automated syncs**: `/cv` updates, CLAUDE.md restructuring, convergence system refinements

### [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) — Report Maintenance (3 commits)

- **Period realignment**: all reports aligned to Mon-Sun boundaries, backfill for Jan 20-Feb 4 gap

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 15 (13 with substantial development) |
| Total commits | 228 |
| Total lines added | +479,564† |
| Total lines removed | -26,349 |
| Net new lines | +453,215† |
| Net new lines (excl. vendored/generated) | ~+130,000 |
| File changes | 1,680 |
| Languages | C++, WGSL, Go, C#, Svelte, Swift, Lua, Python, SQL, JavaScript/TypeScript, Markdown |
| Contributors | 1 (Marcelo Cantos) |

*†jevon vendors Lua 5.1.5, sqlpipe, and sqlite3 (~330k lines). hms includes package-lock.json and generated assets.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [squz/yourworld2](https://github.com/squz/yourworld2) | 49 | 266 | +17,003 | -1,811 | +15,192 |
| [marcelocantos/cworkers](https://github.com/marcelocantos/cworkers) | 37 | 144 | +10,157 | -2,904 | +7,253 |
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | 33 | 645 | +90,954 | -17,356 | +73,598* |
| [marcelocantos/jevon](https://github.com/marcelocantos/jevon) | 30 | 191 | +337,941 | -618 | +337,323* |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | 19 | 62 | +2,267 | -268 | +1,999 |
| [linqgo/linq](https://github.com/linqgo/linq) | 16 | 133 | +2,355 | -1,232 | +1,123 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 12 | 119 | +6,255 | -1,643 | +4,612 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 6 | 14 | +971 | -288 | +683† |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 6 | 67 | +4,620 | -331 | +4,289 |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | 5 | 31 | +1,212 | -152 | +1,060 |
| [marcelocantos/mpe2pdf](https://github.com/marcelocantos/mpe2pdf) | 5 | 16 | +4,966 | -3 | +4,963 |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 3 | 8 | +1,728 | -946 | +782† |
| ge (submodule) | 3 | 12 | +298 | -47 | +251 |
| [squz/esfera2](https://github.com/squz/esfera2) | 2 | 2 | +2 | -2 | 0‡ |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 2 | 2 | +2 | -2 | 0‡ |

*\*Includes vendored dependencies or generated content.*
*†Automated syncs / meta.*
*‡ge submodule pointer updates only.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/cworkers](https://github.com/marcelocantos/cworkers) | ~29 | Worker pool, MCP protocol, session management |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~33 | Go wrapper, sync protocol, query watch |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | ~25 | Recursive tree construction, dialect compatibility, aggregate fields |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | ~12 | Type-matrix correctness, no-op allocation tests |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~8 | Processor reuse, set_maxprocs, chat server example |
| **Total** | **~107** | |

---

## Ideas & Innovations

### GPU-Accelerated Visual Parity via Chamfer Distance ([yourworld2](https://github.com/squz/yourworld2))

Tuning a renderer to match a reference image is typically a manual process — tweak a parameter, render, compare side-by-side, repeat. yourworld2's parity optimizer replaces this with **automated parameter search using GPU-computed Chamfer distance as the objective function**. The pipeline chains five WGSL compute shaders: Sobel edge extraction on both images, JFA initialisation seeding edge pixels, iterative JFA steps building the distance field in O(log n) passes, distance lookup, and finally a Chamfer reduction using overflow-safe atomics to produce a single scalar. Differential evolution explores the ~17-dimensional parameter space (atmosphere density, lighting angles, colour curves, glow intensity) at ~50 evaluations/sec by rendering directly into compute textures with no GPU-CPU readback. The result is a principled, repeatable visual matching process that would otherwise depend entirely on human aesthetic judgement.

### Server-Driven Native UI via Embedded Lua ([jevon](https://github.com/marcelocantos/jevon))

Mobile apps traditionally require redeployment to change UI. Web views avoid this but sacrifice native performance and feel. jevon takes a third path: **the server sends Lua scripts that the iOS client executes locally to construct native SwiftUI views**. The Lua runtime registers 26 builder functions and 15 modifier properties, giving the server full control over layout, styling, and interaction without any HTML/CSS/JS layer. Actions like `on_submit` and `on_tap` call back to the server over WebSocket, keeping business logic server-side. This architecture means the iOS app never needs updating for UI changes — it is a generic SwiftUI renderer driven by whatever Lua the server sends. The ~782-line `LuaRuntime.swift` is the entire bridge between two languages and two paradigms.

### Recursive Tree Construction in Pure SQL ([sqldeep](https://github.com/marcelocantos/sqldeep))

Producing nested JSON from a recursive SQL relationship (e.g. category trees) normally requires application-level recursion or multiple queries. sqldeep's `RECURSE ON` clause transpiles the intent into **a 3-CTE bracket-injection template that assembles nested JSON entirely within SQL**. The first CTE (`_sdq_dfs`) performs recursive DFS with cycle detection, producing a path column. The second (`_sdq_ranked`) assigns row numbers and generates per-row JSON fragments. The third (`_sdq_events`) emits opening and closing bracket characters positioned by DFS path, so that a final `group_concat` over the sorted events produces correctly nested JSON. No temporary tables, no cursors, no application code — the entire tree materialises in a single SQL statement. The same template works on both SQLite and PostgreSQL.

### Self-Warming Worker Pool with Shadow Discovery ([cworkers](https://github.com/marcelocantos/cworkers))

Pre-spawned worker pools face a cold-start problem: the first request arrives before any worker is ready. cworkers solves this with **self-warming** — each time a worker is dispatched, a replacement is immediately spawned, maintaining pool depth without external orchestration. Combined with shadow auto-discovery (finding the calling Claude session's transcript from the working directory rather than requiring manual registration), this means callers simply invoke the `cwork` MCP tool and get a warm worker with full session context. The progression from 6-subcommand Unix socket protocol to single MCP tool call is a case study in protocol simplification.

### iter.Seq as Query Foundation ([linq](https://github.com/linqgo/linq))

Go's channel-based iterators carry goroutine overhead per element — allocation, scheduling, and synchronisation costs that accumulate across chained operations. linq v2's migration to **`iter.Seq[T]` replaces channels with simple function values**, eliminating all goroutine overhead. The change touched 150 files because `Query[T]` is the foundational type — every combinator, every test, every example flows through it. The result is a LINQ-style query library that composes without hidden concurrency costs, aligning with Go 1.23's native iterator protocol rather than fighting it.

### SSE Multiplexer for Streaming Search ([hms](https://github.com/Health-Management-Systems/hms))

Traditional paginated search returns a fixed page, requiring a new request for each page. HMS2's `MultiplexSession.cs` (542 lines) implements **multiplexed Server-Sent Events streams** where a single SSE connection carries results from multiple concurrent queries, each independently scrollable. The multiplexer manages backpressure (pausing database reads when the client falls behind), handles client disconnection without leaking database cursors, and supports infinite scroll by streaming additional results on demand. This gives the clinical user interface the responsiveness of a local database while querying SQL Server.

---

## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **yourworld2** | 25-35 | GPU compute shader pipeline (5 WGSL shaders, JFA, Chamfer distance with atomics), differential evolution optimizer, equirectangular-to-cube-map with shapefile water detection, critically damped harmonic oscillator for auto-zoom, screen-space vertex shader distortion for magnification lens, SQLite game state, menu/tutorial/achievement overlay systems |
| **hms** | 25-35 | Healthcare ERP across 5 waves — recurrence engine with CHSP/DVA budget models, SSE multiplexer with backpressure, RBAC middleware with field-level security, transport route optimisation with GPS live map, HL7 integration, 50 convergence targets spanning C#/Svelte/SQL Server |
| **cworkers** | 10-15 | MCP server architecture with streamable HTTP, self-warming worker pool with cold-start mitigation, shadow auto-discovery of Claude transcripts, SQLite persistence, real-time Svelte dashboard with SSE and xterm.js ANSI rendering, 9 releases in 7 days |
| **jevon** | 15-20 | Embedded Lua 5.1.5 runtime in Swift with 26 SwiftUI builder bindings, bidirectional SQLite sync (Go sync manager + C wrapper + Swift wrapper across 3 languages), WebSocket protocol for script push and action callbacks, QR scanning, MCP tool exposure |
| **sqldeep** | 8-12 | Recursive tree transpilation with 3-CTE bracket-injection (DFS + ranking + event generation), context-sensitive operator parsing (`->` as JSON vs comparison), aggregate field expressions, dual SQLite/PostgreSQL codegen, 744-line theory paper |
| **csp** | 5-8 | TSan race diagnosis in M:N processor slot reuse, in-place reset with release semantics, 3 research papers (formal foundations axiom system, verification architecture, mutex migration), 622-line chat server example |
| **linq** | 5-8 | iter.Seq migration touching 150 files across the entire combinator library, golangci-lint v2 crash investigation and workaround, benchmark suite, README rewrite |
| **sqlpipe** | 4-6 | Emscripten Wasm compilation of C++ SQLite sync library, TypeScript wrapper API, self-contained Go wrapper dropping external SQLite dependency, QueryWatch reactive subscription engine |
| **frozen** | 2-3 | No-op allocation elimination with hash-based detection, type-matrix parametric tests across 5 key types with independence verification |
| **mpe2pdf** | 2-3 | Open-source release preparation: Apache-2.0 licensing, stability documentation, agent guide, npm publish pipeline |
| **Other** | 2-3 | ge wire fixes, esfera2/multimaze2 submodule updates, skills syncs, report maintenance |

### The Diversity Tax

Specialisms exercised this week:

- GPU compute shader programming (WGSL, JFA, atomics, Chamfer distance)
- [Differential evolution](https://en.wikipedia.org/wiki/Differential_evolution) metaheuristic optimisation
- Equirectangular projection and cube map geometry with shapefile processing
- C++ M:N scheduler internals and memory ordering semantics
- Formal methods research (axiom systems, verification architecture)
- Swift/SwiftUI with embedded Lua FFI and 26-function binding layer
- Bidirectional SQLite replication across Go/C/Swift language boundaries
- C#/ASP.NET Core with Dapper, SQL Server stored procedures, SSE streaming
- [SvelteKit](https://svelte.dev/) SPA with Svelte 5, deep linking, RBAC-aware menus
- Healthcare domain modelling (CHSP/DVA funding, recurrence scheduling, HL7)
- [MCP](https://modelcontextprotocol.io/) server architecture with streamable HTTP transport
- Go iterator protocol migration (channels to iter.Seq)
- SQL transpiler construction with recursive CTE generation
- WebAssembly compilation via Emscripten with TypeScript bindings
- Critically damped harmonic oscillators for animation

No single engineer holds expertise in GPU compute shader optimisation, embedded Lua runtimes on iOS, healthcare recurrence engines, M:N scheduler memory ordering, SQL transpiler CTE generation, and differential evolution simultaneously.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **yourworld2** (49 commits) | 6-8 | Parity optimizer concept and parameter selection, cube map orientation debugging, game mode design, play-testing on device, aesthetic judgement on atmosphere/lighting |
| **hms** (33 commits) | 4-6 | Wave planning and prioritisation, RBAC model design, recurrence engine business rules (CHSP/DVA), SSE architecture review, screen layout approval |
| **jevon** (30 commits) | 4-6 | Lua-over-WebSocket architecture decision, SwiftUI builder API surface design, sqlpipe sync integration strategy, wire format iteration review |
| **cworkers** (37 commits) | 3-4 | MCP tool design, self-warming pool concept, shadow discovery approach, dashboard UX review |
| **csp** (12 commits) | 2-3 | TSan race diagnosis direction, paper review, processor reuse strategy |
| **Other** | 4-6 | sqldeep RECURSE ON design, linq v2 migration strategy, sqlpipe Wasm target decision, frozen allocation detection approach |
| **Total** | **~23-33 hours** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | Ramp-up cost |
|---------|------------|-----------------|--------------|
| yourworld2 | 25-35 | 40-55 | +12 (GPU compute shaders, JFA, differential evolution, cube map geometry, harmonic oscillators) |
| hms | 25-35 | 40-55 | +10 (C#/ASP.NET, SvelteKit, SQL Server SPs, CHSP/DVA models, SSE multiplexing, HL7) |
| jevon | 15-20 | 25-35 | +8 (Swift FFI, Lua embedding, bidirectional sync across 3 languages, WebSocket protocol) |
| cworkers | 10-15 | 15-22 | +4 (MCP protocol, SSE, xterm.js, worker pool patterns) |
| sqldeep | 8-12 | 12-18 | +4 (recursive CTE generation, SQL parser, dual-backend codegen) |
| csp | 5-8 | 8-12 | +3 (M:N schedulers, memory ordering, formal methods) |
| linq | 5-8 | 8-12 | +3 (Go generics, iter.Seq internals, linter compatibility) |
| sqlpipe | 4-6 | 6-10 | +3 (Emscripten, CGo, SQLite internals) |
| Other | 4-6 | 6-10 | +3 |
| **Subtotal** | **101-145** | **160-229** | **+50** |
| Context-switching tax (30%) | | +48-69 | |
| **Total** | | **208-298** | |

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~110-175 person-days (5.5-9 months)** |
| Specialist team (traditional) | **~65-100 person-days (3-5 person-months)** |
| Actual human effort this week | **~23-33 hours (~3-4 person-days)** |
| **Multiplier vs. generalist** | **~28-45x** |
| **Multiplier vs. specialist team** | **~16-30x** |

The multiplier is highest for the yourworld2 parity optimizer, where building a GPU compute shader pipeline (5 WGSL shaders, JFA distance fields, Chamfer reduction with atomics) feeding a differential evolution optimizer would be a multi-week research project for a graphics specialist — here it was one workstream among several in a single week. The HMS2 five-wave buildout is similarly extreme: 50 convergence targets spanning a healthcare ERP with budget-aware scheduling, SSE streaming, RBAC, and transport optimisation. The multiplier is lowest for the csp research papers and the linq linter battle, where human reasoning time (axiom system construction, debugging linter crashes) dominated over code volume. The human contribution concentrated on architectural invention (Lua-over-WebSocket for native UI, self-warming worker pools, Chamfer distance as visual objective function), domain expertise (CHSP/DVA funding models, HL7 integration points), and aesthetic judgement (globe atmosphere rendering, game mode design, dashboard UX).

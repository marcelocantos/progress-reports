# Weekly Progress Report — 2026-02-02…08

## Executive Summary

A heavily concentrated week across **2 repositories** dominated by **yourworld2**, which underwent two major architectural transformations: completing the engine extraction into the shared sq submodule, and building a wire-based remote rendering architecture that sends WebGPU commands from a headless server to mobile clients. Progressive mipmapped texture streaming with ASTC compression capped the week with a high-performance mobile delivery pipeline.

**77 commits** | **-1,785 net lines** | **~55-100 person-days traditional equivalent** | **~25-50x multiplier**

### Major Achievements & Innovations

- **Wire-based remote rendering architecture** (yourworld2): headless server emits [WebGPU wire protocol](https://dawn.googlesource.com/dawn) commands to iOS/Android clients, achieving native rendering quality with server-driven game logic — a thin-client model that sidesteps video streaming entirely
- **Progressive mipmapped texture streaming with ASTC compression** (yourworld2): deferred mip delivery with priority queues, wire-level mip truncation, and [ASTC](https://en.wikipedia.org/wiki/Adaptive_scalable_texture_compression) compression for 4x faster wire startup, with a mip cache probe protocol to avoid redundant transfers
- **Engine extraction completion** (yourworld2): sq submodule fully separated with `Module.mk` namespaced variables, `libsq.a` static linking, `#include <sq/...>` angle-bracket includes, relocated unit tests and test shaders — enabling code sharing with esfera2 and future projects
- **bgfx to Dawn/WebGPU migration** (yourworld2): complete rendering backend replacement including shader rewrites to [WGSL](https://www.w3.org/TR/WGSL/), `dawnProcSetProcs` initialisation, and removal of all bgfx references — the prerequisite that made wire rendering possible
- **RAII EventWatchHandle for macOS live resize** (yourworld2): SDL3's modal resize event loop on macOS freezes rendering; solved by installing an event watcher callback that renders during resize, wrapped in RAII for safe cleanup across threads

### Tough Challenges Overcome

- **Wire protocol design with progressive texture delivery** (yourworld2): the wire rendering receiver needed robust reconnection with exponential backoff, deferred mip streaming with priority queues to deliver visible textures first, wire-level mip truncation to reduce initial payload, and idle disconnect detection — each of these is a distinct networking concern layered on top of the WebGPU wire format
- **bgfx-to-Dawn shader and API translation** (yourworld2): two fundamentally different GPU abstraction models — bgfx's submit-based batching vs. Dawn's command encoder pipeline — required rewriting every rendering call and every shader, not just mechanical substitution but rethinking render pass structure
- **Cross-platform mobile receiver** (yourworld2): the wire receiver needed to work on iOS (with landscape orientation handling and resize events) and Android simultaneously, each with platform-specific texture format support (ASTC primary, ETC2 fallback) and touch input coordinate mapping
- **Live resize rendering on macOS** (yourworld2): SDL3 blocks the event loop during window resize on macOS, which is a platform-specific behaviour that cannot be worked around within SDL's normal event pump — the event watcher callback runs on the OS event thread, creating thread-safety concerns that the RAII wrapper addresses

Contributor: Marcelo Cantos

---

## Game Projects

### [squz/yourworld2](https://github.com/squz/yourworld2) — Wire Rendering & Engine Extraction (77 commits)

**The dominant effort of the week.** Two massive parallel themes: completing the engine extraction begun in the previous period, and building an entirely new wire-based remote rendering architecture. Non-vendored diff: +4,594/-6,379 (net -1,785 — the negative net reflects heavy refactoring and dead code removal). 87 files changed, 22 new files.

- **Engine extraction completion** (Feb 2-3): extracted `sq/` into a standalone submodule ([squz/sq](https://github.com/squz/sq)), refactored Makefile rules into `sq/Module.mk` with namespaced variables (`sq/` prefixes for all targets/sources/flags), linked against `libsq.a` instead of individual object files, moved unit tests and test shaders into the sq module. Merged `render_app` into `render_test` for in-process rendering. Multiple submodule updates integrated `BgfxResource` rename, CLAUDE.md, and a dependency graph tool
- **bgfx to Dawn migration** (Feb 3): complete replacement of the [bgfx](https://github.com/bkaradzic/bgfx) rendering backend with [Dawn](https://dawn.googlesource.com/dawn) (WebGPU). Initialised `dawnProcSetProcs` for switchable backends, removed unused shaders (`simple`, `line`, `diff`), updated application to `sq::render` API, switched to `#include <sq/...>` angle-bracket style, added METRICS.md with include dependency graph
- **Architecture improvements** (Feb 3): simplified `Application` constructor using sq helpers, implemented 1:1 aspect ratio viewport with centred globe, fixed live resize on macOS via `SDL_AddEventWatch` with RAII `EventWatchHandle`, optimised render loop to reduce redundant GPU state calls, moved generic build infrastructure into `sq/Module.mk`
- **Wire-based remote rendering** (Feb 6-8): added wire rendering receiver and headless server mode (`YOURWORLD_WIRE=1`), robust reconnection with exponential backoff, moved receiver and protocol into sq submodule, simplified `main.cpp` to wire-only mode with `sq::WireSession`, reduced main to pure game logic. Added touch/mouse input from receiver to drive globe rotation, handled receiver resize events and disconnect/reconnect. Multiple sq submodule updates for iOS receiver build, QR scanner, receiver split, Android receiver, Android emulator support, iOS Dawn libs, iOS Simulator libs, LFS migration for macOS Dawn libs, touch input fixes, and platform abstraction
- **Texture pipeline** (Feb 8): mipmapped `.sqtex` textures for progressive wire delivery, [ASTC](https://en.wikipedia.org/wiki/Adaptive_scalable_texture_compression) texture compression for 4x faster wire startup, wire-level mip truncation, deferred mip streaming with priority queues, mip cache probe protocol, idle disconnect detection. Removed all remaining bgfx references
- **Mobile support** (Feb 7-8): iOS landscape rendering fix, wire drag inertia fix (accumulate deltas per frame), direct rendering mode (`make direct`), mobile receiver documentation

Languages: C++, WGSL, Makefile, Markdown

---

## Other Team Work

### [squz/esfera2](https://github.com/squz/esfera2) — Spherical Chess (37 commits, Andrew Cantos)

Massive progress from M3 through to a complete, playable game with online multiplayer. Andrew delivered M3 (game logic port with `GamePosition`, 160-bit `BitBoard`, minimax bot, 12 tests), M4 (62 piece meshes rendered on the sphere), M5 (click-to-select with legal move highlights), M6 (threaded AI opponent with game mode menu), and M7 (move animation, undo, persistence, last-move highlight). Platform migration from bgfx/GLFW/CMake to sq/SDL3/Make. Pawn promotion, endgame overlay, alpha-beta pruning, touch support, standalone iOS app with full feature parity, Go backend server with REST API + WebSocket game relay, interactive tutorial with 10 guided lessons, and online multiplayer with matchmaking lobby. 37 commits, +5,098/-2,403 lines, 29 files changed, 28 new files.

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 1 |
| Total commits | 77 |
| Total lines added | +4,594 |
| Total lines removed | -6,379 |
| Net new lines | -1,785 |
| File changes | 87 |
| New files created | 22 |
| Languages | C++, WGSL, Makefile, Markdown |

*The negative net reflects heavy refactoring — engine extraction, bgfx removal, and code consolidation into the sq submodule removed more lines than the new wire rendering architecture added.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [squz/yourworld2](https://github.com/squz/yourworld2) | 77 | 87 | +4,594 | -6,379 | -1,785 |

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [squz/yourworld2](https://github.com/squz/yourworld2) | — | Regression test framework maintained; render_app merged into render_test |
| **Total** | **—** | Focus was on architecture and protocol, not new test functions |

---

## Ideas & Innovations

### Wire-Based Remote Rendering via WebGPU Wire Protocol ([yourworld2](https://github.com/squz/yourworld2))

Rather than streaming compressed video (high latency, lossy) or replicating game state to clients (complex synchronisation), yourworld2 sends **raw WebGPU wire protocol commands** from a headless server to mobile receivers. The client device runs a real GPU-backed WebGPU implementation that executes these commands natively, producing pixel-perfect rendering without video compression artefacts. This is possible because Dawn's wire protocol was designed for Chrome's GPU process isolation — it serialises the entire WebGPU API surface. Repurposing it for network transport turns every mobile device into a thin rendering terminal with native GPU quality.

### Progressive Mipmapped Texture Streaming ([yourworld2](https://github.com/squz/yourworld2))

The wire protocol's biggest bandwidth challenge is texture data. The solution uses **mipmapped `.sqtex` files with wire-level mip truncation**: the server sends only the smallest mip levels initially (enough for a visible but blurry globe), then streams higher-resolution mips in priority order based on what the camera is looking at. A **mip cache probe protocol** lets the server skip mips the client already has from a previous session. Combined with ASTC compression (which reduces texture size ~4x compared to raw RGBA), this achieves a 4x faster startup while the full-resolution textures arrive progressively in the background.

### Engine Extraction via Module.mk Namespacing ([yourworld2](https://github.com/squz/yourworld2))

Extracting a rendering engine from a working application into a reusable submodule is normally disruptive surgery. The approach here used **`Module.mk` with systematically namespaced variables** — every target, source list, and compiler flag prefixed with `sq/` — so the submodule's build rules compose cleanly with any host project's Makefile without variable collisions. The host links against `libsq.a` as a single static library, and includes use `#include <sq/...>` angle-bracket style, making the boundary explicit in source code. This means esfera2, multimaze2, and future projects share the engine by adding one submodule and one `include` line.

### RAII Event Watcher for macOS Live Resize ([yourworld2](https://github.com/squz/yourworld2))

macOS's window manager runs a **modal event loop during resize**, blocking SDL3's normal event pump and freezing the render loop. The fix installs an SDL event watcher callback via `SDL_AddEventWatch` that renders frames in response to resize events, bypassing the blocked main loop. Wrapping the registration in an RAII `EventWatchHandle` ensures the callback is removed on destruction — a subtle correctness concern since SDL event watchers run on the OS event thread, not the application thread, and a dangling callback after application teardown would be a use-after-free bug.

### Exponential Backoff Reconnection for Wire Receivers ([yourworld2](https://github.com/squz/yourworld2))

The wire receiver must handle server restarts, network interruptions, and idle timeouts gracefully. The reconnection strategy uses **exponential backoff with idle disconnect detection**: the receiver monitors wire activity and disconnects proactively when the server goes quiet (distinguishing "server crashed" from "nothing to render"), then reconnects with increasing delays to avoid thundering-herd problems when multiple mobile clients reconnect simultaneously after a server restart.

---

## Effort Estimate: Traditional vs. AI-Assisted

A single-project week, but the work spans an unusually wide range of disciplines — from GPU rendering pipelines to network protocol design to mobile platform integration.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **yourworld2** (engine extraction) | 8-15 | Submodule extraction requires deep understanding of Make's evaluation model, C++ include/link semantics, and careful variable namespacing to avoid collisions. Merging render_app into render_test changes the test harness architecture. |
| **yourworld2** (Dawn migration) | 10-15 | bgfx and Dawn have fundamentally different rendering models. Every shader must be rewritten from bgfx's `sc` format to WGSL. Every rendering call changes. The dawnProcSetProcs switchable backend adds another layer. |
| **yourworld2** (wire rendering) | 15-25 | Novel architecture — not off-the-shelf. Headless server mode, wire protocol integration, receiver with reconnection, input forwarding from client to server, resize event propagation. Two mobile platforms with different texture format requirements. |
| **yourworld2** (texture pipeline) | 10-15 | Mipmapped progressive streaming with priority queues is networking/graphics crossover. ASTC compression pipeline. Wire-level mip truncation. Cache probe protocol. Idle disconnect detection. Each is a distinct sub-problem. |
| **yourworld2** (mobile/platform) | 5-10 | iOS landscape rendering, Android receiver, touch input coordinate mapping, drag inertia accumulation, platform-specific texture format selection. |

### The Diversity Tax

The specialisms exercised within this single project:

- [WebGPU](https://www.w3.org/TR/webgpu/)/[Dawn](https://dawn.googlesource.com/dawn) rendering pipeline and [WGSL](https://www.w3.org/TR/WGSL/) shader authoring
- [bgfx](https://github.com/bkaradzic/bgfx) internals (to migrate away from)
- Dawn wire protocol internals (serialisation, command buffering)
- Make build system engineering (`Module.mk`, namespaced variables, static library linking)
- Network protocol design (reconnection, backoff, idle detection, cache probing)
- [ASTC](https://en.wikipedia.org/wiki/Adaptive_scalable_texture_compression) and ETC2 texture compression formats
- iOS platform integration (landscape orientation, touch coordinates, Dawn libs)
- Android platform integration (emulator, receiver, touch input)
- [SDL3](https://github.com/libsdl-org/SDL) event system internals (event watchers, modal event loops)
- Mipmap streaming and progressive delivery algorithms

A single developer expert in all of these is exceptionally rare. In a traditional team, this would involve a graphics programmer, a networking engineer, a build engineer, and mobile platform specialists — at minimum 3-4 people with coordination overhead.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **yourworld2** (77 commits) | 8-15 | Architecture decisions (wire protocol design, texture streaming strategy), testing on iOS/Android devices, debugging mobile-specific rendering issues, visual verification of globe rendering, interaction feel tuning |
| **Total** | **~8-15 hours** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | The ramp-up cost |
|---------|------------|-----------------|------------------|
| **yourworld2** (engine extraction) | 8-15 | 12-20 | Make evaluation model subtleties, C++ include path conventions, submodule workflow |
| **yourworld2** (Dawn migration) | 10-15 | 18-25 | WebGPU spec is large. WGSL is new. Understanding dawnProcSetProcs requires reading Dawn internals. |
| **yourworld2** (wire rendering) | 15-25 | 25-40 | Wire protocol is Dawn-internal API — no tutorials exist. Reconnection strategy is protocol design from scratch. |
| **yourworld2** (texture pipeline) | 10-15 | 15-25 | ASTC format spec, mipmap math, priority queue design for streaming, cache protocol design |
| **yourworld2** (mobile/platform) | 5-10 | 10-15 | Two mobile platforms, each with their own build toolchains, texture format support, and touch input models |
| **Subtotal** | **48-80** | **~80-125** | |

Adding a ~15% context-switching tax for thrashing between GPU rendering, network protocols, build systems, and mobile platforms within a single codebase brings the realistic single-person estimate to **~55-100 person-days, or roughly 3-5 months**.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **55-100 person-days (3-5 months)** |
| Specialist team (traditional) | **48-80 person-days (2-4 person-months)** |
| Actual human effort this week | **~8-15 hours (~1-2 person-days)** |
| **Multiplier vs. generalist** | **~25-50x** |
| **Multiplier vs. specialist team** | **~25-40x** |

The multiplier is highest on the wire rendering architecture — a novel design that required synthesising knowledge of Dawn's wire protocol internals, network reconnection strategies, and progressive texture streaming into a coherent system. No existing tutorial or library covers this combination; it is pure architectural invention. The human contribution concentrated on the key design decisions: choosing the wire protocol approach over video streaming, deciding on progressive mip delivery over all-or-nothing texture transfer, and specifying the reconnection behaviour. These decisions took minutes but determined the entire week's technical direction.

# Weekly Progress Report — 2026-01-27…02-04 (9 days)

## Executive Summary

An intensely focused period on **1 repository**, devoted entirely to evolving **yourworld2** from a prototype globe renderer into a properly architected application. The work spans engine extraction into a shared submodule, a full rendering backend migration from bgfx to Dawn/WebGPU, a new asset pipeline with JSON manifests and binary mesh packs, interactive globe controls with damped rotation, and a comprehensive build system overhaul.

**79 commits** | **+719 net application lines** | **~45-77 person-days traditional equivalent** | **~30-50x multiplier**

### Major Achievements & Innovations

- **Engine extraction into shared submodule** (yourworld2): the rendering engine, resource abstractions, and test framework were extracted into [squz/sq](https://github.com/squz/sq) as a standalone submodule with its own `Module.mk`, `libsq.a` static library, and `#include <sq/...>` paths — enabling code sharing across future game projects (such as esfera2)
- **bgfx to Dawn/WebGPU migration** (yourworld2): complete rendering backend replacement — all shaders rewritten from bgfx's `sc` format to [WGSL](https://www.w3.org/TR/WGSL/), bgfx API calls replaced with WebGPU equivalents, `dawnProcSetProcs` introduced for runtime backend switching. [Dawn](https://dawn.googlesource.com/dawn) is Google's WebGPU implementation, whose wire protocol later enables remote rendering
- **JSON manifest + binary mesh pack** (yourworld2): replaced a monolithic binary country data file with a split architecture — human-readable JSON manifest for metadata plus a compact binary mesh pack for precomputed triangle data, making country definitions diff-friendly without sacrificing load performance
- **Damped rotation with inertia** (yourworld2): `DampedRotation` and `DampedValue` abstractions provide physically plausible deceleration using exponential decay applied per-frame, making the interaction frame-rate independent
- **Translucent bathymetry ocean sphere** (yourworld2): a second-pass translucent sphere textured with [bathymetry](https://en.wikipedia.org/wiki/Bathymetry) data, requiring careful blend state management and render order control in the Dawn pipeline

### Tough Challenges Overcome

- **Live resize on macOS** (yourworld2): SDL3's event loop blocks during window resize on macOS, freezing rendering. Solved with an SDL event watcher callback (`SDL_AddEventWatch`) wrapped in an RAII `EventWatchHandle` that renders during the resize event itself, sidestepping the blocking event loop
- **Prime meridian triangle winding** (yourworld2): splitting mesh triangles at the prime meridian for hemisphere rendering introduced reversed winding order, causing backface culling to discard visible geometry. Required careful vertex ordering logic in the mesh splitter
- **Build system extraction** (yourworld2): splitting a working application's build into a host `Makefile` and a submodule `sq/Module.mk` with properly namespaced variables (`sq/...` prefixes) without breaking incremental builds, test discovery, or `compile_commands.json` generation demanded precise understanding of Make's evaluation model

Contributor: Marcelo Cantos

---

## Game Projects

### [squz/yourworld2](https://github.com/squz/yourworld2) — Engine Extraction & Dawn Migration (79 commits)

**The sole focus of the period.** Continued development of the globe-based world game, transforming the previous week's prototype into a properly layered application with a shared engine, modern rendering backend, and production-quality asset pipeline.

- **Engine extraction** ([sq](https://github.com/squz/sq) **submodule**): moved engine code, vendor dependencies, and build infrastructure into `sq/` and extracted it as a standalone submodule ([squz/sq](https://github.com/squz/sq)). Refactored build rules into `sq/Module.mk` with namespaced variables, linked against `libsq.a` instead of individual object files, relocated unit tests and test shaders. Multiple subsequent submodule updates integrated `BgfxResource` rename, CLAUDE.md, a dependency graph tool, and Dawn Wire transport
- **bgfx to Dawn migration**: full replacement of the [bgfx](https://github.com/bkaradzic/bgfx) rendering backend with [Dawn](https://dawn.googlesource.com/dawn) (WebGPU). All shaders rewritten to [WGSL](https://www.w3.org/TR/WGSL/), `dawnProcSetProcs` initialised for switchable backends. Removed unused shaders (`simple`, `line`, `diff`)
- **Asset pipeline**: replaced monolithic binary with JSON manifest + binary mesh pack. Added country binary format, replaced [stb_image](https://github.com/nothings/stb) with [SDL3_image](https://github.com/libsdl-org/SDL_image), migrated world texture and shapefiles into the repo, split world texture into hemispheres for meridian rendering
- **Rendering features**: translucent ocean sphere with [bathymetry](https://en.wikipedia.org/wiki/Bathymetry) texture, batched mesh parts by country to reduce draw calls, 1:1 aspect ratio viewport with centred globe, optimised render loop reducing redundant GPU state calls
- **Interactive controls**: mouse drag with `DampedRotation` and `DampedValue` — damped inertia using per-frame exponential decay for frame-rate-independent deceleration
- **Architecture**: `BgfxResource` RAII wrappers replacing raw handles, `std::format` and decontextualised error reporting in resource loaders, manifest loader throws on errors, `SPDLOG_` macros throughout, `sq::loadProgram` helper, `DeltaTimer`, decoupled `CaptureTarget` from `Application` (RAII), fixed live resize on macOS via `SDL_AddEventWatch` with RAII `EventWatchHandle`
- **Build system**: incremental builds, `compile_commands.json` generation for LSP, `make init` for automated development environment setup
- **Testing**: consolidated rendering pipeline with regression tests, merged `render_app` into `render_test` for in-process rendering
- **Documentation**: comprehensive planning docs (`feature-parity-analysis.md`, `implementation-plan.md`), integrated user feedback, CLAUDE.md, METRICS.md with include dependency graph

Application code: +8,390/-7,671 lines (net +719 — the modest net reflects heavy refactoring, not low output). Total lines including extraction: +66,388/-343,506 (the large deletion is vendored code moving into the sq submodule). 121 files changed, 63 new files.

---

## Other Team Work

### [squz/esfera2](https://github.com/squz/esfera2) — Spherical Chess (7 commits, Andrew Cantos)

A new project: a rewrite of [esfera](https://github.com/squz/esfera), a chess variant played on a [geodesic sphere](https://en.wikipedia.org/wiki/Geodesic_polyhedron). Andrew built M1 (project scaffolding with bgfx + GLFW on macOS/Metal, CMake build system), M2 (geodesic sphere rendering with interactive mouse rotation, bgfx shaders for cell colouring), and M3 (full chess game logic port — `GamePosition`, `BitBoard` at 160 bits, `GameAnalysis`, [minimax](https://en.wikipedia.org/wiki/Minimax) bot with [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning), check/checkmate/stalemate detection, 12 tests passing). +2,523/-64 lines, 20 files.

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 1 |
| Total commits | 79 |
| Total lines added | +8,390 |
| Total lines removed | -7,671 |
| Net new lines | +719 |
| File changes | 121 |
| New files created | 63 |
| Languages | C++, WGSL, Makefile, Markdown |

*The +66,388/-343,506 total diff includes the sq submodule extraction (moving vendored code out of the main repo). The application code figures above exclude this bulk movement.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [squz/yourworld2](https://github.com/squz/yourworld2) | 79 | 121 | +8,390 | -7,671 | +719* |

*\*Application code only. Including vendored code extraction: +66,388/-343,506.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [squz/yourworld2](https://github.com/squz/yourworld2) | — | Regression test framework established; render_app merged into render_test |
| **Total** | **—** | Test infrastructure built; specific test counts not separated from pre-existing suite |

---

## Ideas & Innovations

### Engine Extraction via Module.mk Namespacing ([yourworld2](https://github.com/squz/yourworld2))

Extracting a rendering engine from a working application into a reusable submodule is normally a disruptive multi-day surgery. The approach here used **`Module.mk` with systematically namespaced variables** (`sq/` prefixes for all targets, sources, and flags) so the submodule's build rules compose cleanly with any host project's Makefile without variable collisions. The host links against `libsq.a` as a single static library, and includes shift to `#include <sq/...>` angle-bracket style, making the boundary explicit in source code. This means any future project — [esfera2](https://github.com/squz/esfera2), [multimaze2](https://github.com/squz/multimaze2) — can share the engine by adding one submodule and one `include` line in its Makefile.

### bgfx to Dawn as a WebGPU Wire Protocol Enabler ([yourworld2](https://github.com/squz/yourworld2))

The migration from [bgfx](https://github.com/bkaradzic/bgfx) to [Dawn](https://dawn.googlesource.com/dawn) was not simply swapping one rendering API for another. bgfx is a multi-backend abstraction layer (Metal, D3D, OpenGL, Vulkan behind a single API) designed for local rendering. Dawn implements the [WebGPU](https://www.w3.org/TR/webgpu/) standard, which includes a **wire protocol** — a serialisation format for GPU commands that can be sent over a network. By migrating to Dawn now, the architecture is positioned for remote rendering: a headless server can execute game logic and emit WebGPU wire commands to thin mobile clients, which became the central architecture in subsequent weeks.

### JSON Manifest + Binary Mesh Pack Split ([yourworld2](https://github.com/squz/yourworld2))

The previous monolithic binary country data file was opaque, unauditable, and required recompilation for any metadata change. The replacement splits the data into two concerns: a **JSON manifest** describing countries, mesh references, and texture coordinates (human-readable, version-controllable, diff-friendly) and a **binary mesh pack** containing precomputed triangle strips (compact, fast to memory-map). This separation of concerns means artists or designers can edit country metadata without touching binary geometry, and the geometry pipeline can be optimised independently.

### Frame-Rate-Independent Damped Rotation ([yourworld2](https://github.com/squz/yourworld2))

Globe rotation with inertia sounds simple, but naive implementations produce frame-rate-dependent behaviour — the globe spins faster on a 120 Hz display than on a 60 Hz one. The `DampedValue` abstraction uses **exponential decay scaled by delta-time**: `value *= pow(damping, dt)`. This gives frame-rate independence by construction, not by accident. The `DampedRotation` wrapper applies this to quaternion-space globe orientation, producing physically plausible deceleration after mouse release regardless of frame timing.

### RAII Event Watcher for macOS Live Resize ([yourworld2](https://github.com/squz/yourworld2))

macOS's window manager runs a **modal event loop during resize**, blocking SDL3's normal event pump and freezing the render loop. The fix installs an SDL event watcher callback via `SDL_AddEventWatch` that renders frames in response to resize events, bypassing the blocked main loop. Wrapping the watcher registration in an RAII `EventWatchHandle` ensures the callback is removed when the application exits, preventing dangling function pointers — a subtle correctness concern since SDL event watchers run on the OS event thread, not the application thread.

---

## Effort Estimate: Traditional vs. AI-Assisted

This period is a deep dive into a single project, but the work spans an unusually wide range of engineering disciplines for one codebase.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **yourworld2** | 25-45 | Engine extraction requires deep understanding of Make's evaluation model and C++ include/link semantics. bgfx-to-Dawn migration means rewriting every shader and every rendering call — two very different GPU APIs. Asset pipeline design (manifest + mesh pack split) is systems architecture. macOS live resize fix requires knowledge of SDL3 internals and platform-specific event loop behaviour. Damped rotation needs correct quaternion math with frame-rate independence. Bathymetry ocean sphere requires blend state and render order management. |

### The Diversity Tax

Even within a single project, the specialisms exercised are remarkably diverse:

- [WebGPU](https://www.w3.org/TR/webgpu/)/[Dawn](https://dawn.googlesource.com/dawn) rendering pipeline and [WGSL](https://www.w3.org/TR/WGSL/) shader authoring
- [bgfx](https://github.com/bkaradzic/bgfx) internals (to migrate away from)
- Make build system engineering (`Module.mk`, namespaced variables, `compile_commands.json` generation)
- C++ library architecture (submodule extraction, `libsq.a` static linking, include path conventions)
- JSON/binary asset pipeline design
- [SDL3](https://github.com/libsdl-org/SDL) platform integration (event watchers, live resize, image loading)
- Computational geometry (meridian splitting, triangle winding order)
- Interactive physics (quaternion rotation, exponential damping)
- macOS platform quirks (modal resize event loops)

A single developer expert in *all* of these is rare. More commonly, this work would involve a graphics programmer, a build engineer, and a platform integration specialist.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **yourworld2** (79 commits) | 6-12 | Architecture decisions (engine boundary, asset pipeline format, Dawn migration rationale), visual inspection of rendering output, testing globe interaction feel, debugging macOS resize behaviour |
| **Total** | **~6-12 hours** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | The ramp-up cost |
|---------|------------|-----------------|------------------|
| **yourworld2** | 25-45 | 40-70 | Dawn/WebGPU pipeline setup requires reading the spec and understanding device/queue/surface/swapchain lifecycle. bgfx migration requires understanding both APIs in parallel. Module.mk namespacing requires Make expertise that most C++ developers lack. SDL3 is new (not SDL2), so even experienced SDL developers face API differences. Quaternion rotation math has well-known gimbal-lock pitfalls. |

Adding a ~10% context-switching tax (lower than usual — single project, but many sub-domains) brings the realistic single-person estimate to **~45-77 person-days, or roughly 2-4 months**.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **45-77 person-days (2-4 months)** |
| Specialist team (traditional) | **25-45 person-days (1-2 person-months)** |
| Actual human effort this week | **~6-12 hours (~1-1.5 person-days)** |
| **Multiplier vs. generalist** | **~30-50x** |
| **Multiplier vs. specialist team** | **~17-30x** |

The multiplier is highest on the rendering backend migration — the AI can translate between bgfx and Dawn APIs methodically, rewriting every call site and shader, where a human would spend days reading documentation and debugging subtle differences. The human contribution concentrated on the architectural decisions that shaped the entire period: choosing to extract the engine now (enabling code sharing with esfera2), choosing Dawn over sticking with bgfx (enabling wire-based remote rendering in subsequent weeks), and choosing the manifest + mesh pack split (enabling the asset pipeline to evolve independently). These decisions took minutes but determined weeks of downstream work.

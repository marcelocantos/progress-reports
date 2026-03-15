# Weekly Progress Report — 2026-01-26...02-01

## Executive Summary

An explosive week across **2 repositories** dominated by game development. The headline: **yourworld2** went from last week's 8-commit globe prototype to a 60-commit application with GPU texture atlases, RAII resource architecture, constrained Delaunay triangulation, interactive globe controls with damped inertia, a translucent bathymetry ocean, and the first steps of engine extraction into a shared library. A new project appeared: **esfera2**, a geodesic chess game built by Andrew Cantos.

**61 commits** | **+5,422 net lines** | **~40-70 person-days traditional equivalent** | **~25-50x multiplier**

### Major Achievements & Innovations

- **GPU-based texture atlas generation** in yourworld2 -- a two-pass bgfx render pipeline composites country textures for arbitrary polygon shapes including antimeridian-crossing territories, with per-polygon-part processing for disjoint islands and exclaves
- **ESRI shapefile to binary mesh pipeline** in yourworld2 -- raw shapefiles parsed, triangulated via the [Triangle](https://www.cs.cmu.edu/~quake/triangle.html) library with [constrained Delaunay triangulation](https://en.wikipedia.org/wiki/Constrained_Delaunay_triangulation), then serialised to a JSON manifest + binary mesh pack replacing a monolithic binary format
- **RAII architecture for GPU resources** in yourworld2 -- `BgfxContext`, `SdlContext`, `BgfxResource` wrappers, `Texture`/`Mesh`/`Model` abstractions, eliminating manual resource cleanup and enabling clean composition
- **Damped rotation with frame-rate-independent exponential decay** in yourworld2 -- mouse drag control with inertia using `DampedRotation` and `DampedValue` classes, producing smooth deceleration regardless of frame timing
- **JSON manifest + binary mesh pack** in yourworld2 -- replaced a monolithic binary with a structured two-file format separating metadata from geometry, enabling incremental builds and selective loading

### Tough Challenges Overcome

- **Triangle library replacing earcut for quality mesh generation** (yourworld2): [earcut.hpp](https://github.com/mapbox/earcut.hpp) produced degenerate triangulations on complex country polygons with holes; switching to Jonathan Shewchuk's [Triangle](https://www.cs.cmu.edu/~quake/triangle.html) with constrained Delaunay triangulation and quality refinement eliminated the artefacts
- **Antimeridian-crossing territories** (yourworld2): countries like Russia and Fiji span the [antimeridian](https://en.wikipedia.org/wiki/180th_meridian) -- the texture atlas generator uses a two-pass approach, rendering the main hemisphere and the wrapped portion separately, to correctly composite these disjoint regions
- **Triangle winding order when splitting at prime meridian** (yourworld2): splitting country polygons at the prime meridian for hemisphere texture rendering inverted triangle winding, producing inside-out meshes -- required careful winding correction after the split
- **bgfx Metal uniform passing** (yourworld2): fragment shader uniforms were silently ignored on the Metal backend due to a bgfx-specific registration ordering requirement not present on OpenGL -- tracked down through render debugging on macOS

Contributor: Marcelo Cantos

---

## Game Projects

### [squz/yourworld2](https://github.com/squz/yourworld2) -- Globe Application Buildout (60 commits)

**The biggest effort of the week.** The globe prototype introduced last week (8 commits) exploded into a full application. Non-vendored: +9,021/-3,677 (net +5,344) across 124 files (82 new).

- **GPU texture atlas & country rendering**: Two-pass [bgfx](https://github.com/bkaradzic/bgfx) render pipeline compositing atlas tiles for arbitrary polygon shapes with antimeridian handling, per-polygon-part processing for disjoint territories. Added [earcut.hpp](https://github.com/mapbox/earcut.hpp), [stb_image_write](https://github.com/nothings/stb), [spdlog](https://github.com/gabime/spdlog). `--validate` flag and `ImageDiff` module (GPU + CPU comparison paths) for atlas verification
- **Triangulation pipeline**: Replaced earcut with [Triangle](https://www.cs.cmu.edu/~quake/triangle.html) for [constrained Delaunay triangulation](https://en.wikipedia.org/wiki/Constrained_Delaunay_triangulation) with quality refinement. Implemented then removed [Douglas-Peucker](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm) mesh simplification in favour of Triangle's built-in quality mesh refinement
- **RAII architecture & resource abstractions**: `BgfxContext`, `SdlContext` [RAII](https://en.wikipedia.org/wiki/Resource_acquisition_is_initialization) wrappers. `Texture`, `Mesh`, `Model` classes for GPU resources. `BgfxResource` generic wrapper. `State` simplified to plain struct. `CountryData` replaced with `CountryLoader`. Fragment shader uniform fix for bgfx [Metal](https://developer.apple.com/metal/) backend. Shader files renamed to `*_vs`/`*_fs` convention
- **Rendering features**: Per-country saturation control. Batched mesh parts by country to reduce draw calls. Translucent ocean sphere with [bathymetry](https://en.wikipedia.org/wiki/Bathymetry) texture. World texture split into hemispheres for meridian rendering. Triangle winding order fix for prime meridian splits
- **Interactive controls**: Mouse drag rotation with damped inertia via `DampedRotation` and `DampedValue` classes -- frame-rate-independent exponential decay for smooth deceleration
- **Asset pipeline**: JSON manifest + binary mesh pack replacing monolithic binary format. Incremental builds. Split ocean texture. Country binary format. Replaced stb with [SDL3_image](https://github.com/libsdl-org/SDL_image). `compiledb` integration for clangd
- **Test infrastructure**: [doctest](https://github.com/doctest/doctest) unit test framework. Visual regression tests with golden images in [Git LFS](https://git-lfs.com/). Standalone `render_app` for headless capture
- **Engine extraction**: Moved engine code, vendor dependencies, and build infrastructure into `sq/` directory as the first step toward a shared library. Unified globe radius. Pure alpha blending
- **Build & documentation**: `CLAUDE.md` with project documentation. Reorganised README with quick start and developer setup. `make init` for automated dev environment setup. Migrated shapefiles and world texture to repo assets. Comprehensive planning documentation

Languages: C++, GLSL, Makefile, Markdown

### [squz/yourworld](https://github.com/squz/yourworld) -- Scheme Addition (1 commit)

Added `YourWorldFree.xcscheme` to shared Xcode data. +78/-0, 1 file. Trivial infrastructure commit.

---

## Other Team Work

### [squz/esfera2](https://github.com/squz/esfera2) -- Geodesic Chess (6 commits, Andrew Cantos)

New project: a rewrite of [esfera](https://github.com/squz/esfera), a chess game played on a [geodesic sphere](https://en.wikipedia.org/wiki/Geodesic_polyhedron) with pentagons and hexagons. Andrew set up the project from scratch this week: initial README with codebase assessment and roadmap, M1 project scaffolding (bgfx + [GLFW](https://www.glfw.org/) on macOS/Metal, [CMake](https://cmake.org/) build), M2 geodesic sphere rendering with interactive mouse rotation, and Phase 1 milestone documentation. 6 commits, +1,117/-63 lines, 13 files (all new).

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 2 |
| Total commits | 61 |
| Total lines added | +9,099 |
| Total lines removed | -3,677 |
| Net new lines | +5,422 |
| File changes | 125 |
| New files created | 82 |
| Languages | C++, GLSL, Makefile, Markdown |
| Contributors | 1 (Marcelo Cantos) |

*yourworld2 line counts exclude vendored dependencies. yourworld is a trivial scheme file addition only.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [squz/yourworld2](https://github.com/squz/yourworld2) | 60 | 124 | +9,021 | -3,677 | +5,344 |
| [squz/yourworld](https://github.com/squz/yourworld) | 1 | 1 | +78 | -0 | +78 |

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [squz/yourworld2](https://github.com/squz/yourworld2) | ~10 | Visual regression tests, ImageDiff module, doctest unit tests |
| **Total** | **~10** | |

---

## Ideas & Innovations

### GPU-Based Texture Atlas Generation ([yourworld2](https://github.com/squz/yourworld2))

Country texture atlases are traditionally composited on CPU by sampling and copying pixel rectangles -- a slow process that struggles with irregular polygon shapes and territories spanning the [antimeridian](https://en.wikipedia.org/wiki/180th_meridian). The yourworld2 atlas generator instead **renders each country's texture region as a GPU draw call via bgfx**, using the country's triangulated mesh as the render geometry with the world map as a source texture. A two-pass approach handles antimeridian-crossing territories: the first pass renders the main hemisphere, the second wraps longitude coordinates and renders the overflow. This produces correctly composited atlases for arbitrary polygon shapes -- including Russia's 11-timezone span and Fiji's dateline straddle -- at GPU speed.

### JSON Manifest + Binary Mesh Pack ([yourworld2](https://github.com/squz/yourworld2))

The original asset format was a monolithic binary blob containing all country geometry. This made incremental builds impossible -- any change to one country's mesh required regenerating the entire file. The replacement architecture **separates metadata from geometry**: a JSON manifest lists countries with their mesh offsets, vertex counts, and atlas coordinates, while a companion binary file contains the raw mesh data as packed vertex/index buffers. This enables selective loading (fetch one country's mesh by seeking to its offset), incremental rebuilds (reprocess only changed countries), and human-readable inspection of the manifest for debugging.

### Damped Rotation with Exponential Decay ([yourworld2](https://github.com/squz/yourworld2))

Globe rotation with mouse-drag inertia typically uses linear velocity damping, which produces frame-rate-dependent deceleration and feels different at 30fps versus 60fps. The `DampedValue` class implements **frame-rate-independent exponential decay**: velocity is multiplied by `pow(dampingFactor, deltaTime)` each frame, producing identical deceleration curves regardless of frame timing. The `DampedRotation` variant extends this to 3D rotation using quaternion slerp, giving the globe a natural "spin and settle" feel that is consistent across hardware.

### Visual Regression Testing for GPU Output ([yourworld2](https://github.com/squz/yourworld2))

Pixel-perfect image comparison breaks across GPU vendors, driver versions, and floating-point rounding differences. The `ImageDiff` module provides **threshold-based comparison with both GPU-accelerated and CPU paths**, comparing rendered output against golden images stored in Git LFS. The GPU path runs a diff shader to produce a difference image; the CPU path computes per-pixel distance metrics. A standalone `render_app` binary enables headless capture, decoupling visual regression testing from the interactive application.

### Constrained Delaunay Replacing Ear Clipping ([yourworld2](https://github.com/squz/yourworld2))

[Ear clipping](https://en.wikipedia.org/wiki/Ear_clipping) (via earcut.hpp) is the standard fast-path for polygon triangulation, but it produces degenerate triangles on complex geopolitical boundaries -- coastlines with thousands of vertices, polygons with multiple holes (lakes within countries), and multi-part territories. Switching to [constrained Delaunay triangulation](https://en.wikipedia.org/wiki/Constrained_Delaunay_triangulation) via the Triangle library **maximises minimum triangle angles**, producing meshes that render cleanly and deform well under projection. Triangle's built-in quality refinement (minimum angle constraints) superseded a manual Douglas-Peucker simplification step, eliminating an entire processing stage while producing better results.

---

## Effort Estimate: Traditional vs. AI-Assisted

A single-repo-dominated week -- 60 of 61 commits landed in yourworld2. But those 60 commits span GPU rendering, computational geometry, resource architecture, interactive controls, asset pipeline design, test infrastructure, and engine extraction. The breadth within one project is as demanding as breadth across many.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **yourworld2** | 25-40 | GPU atlas generation is a non-standard rendering technique requiring bgfx pipeline expertise. Constrained Delaunay triangulation with quality refinement is research-grade computational geometry. The asset pipeline redesign (monolithic binary to JSON manifest + binary mesh pack) is systems design work. RAII resource architecture in C++ requires careful lifetime reasoning. Damped rotation with frame-rate-independent decay straddles physics and UX. 60 commits of iteration implies substantial debugging and rework. |
| **yourworld** | 0.1 | Trivial scheme file addition. |

### The Diversity Tax

Despite concentrating on one repository, the specialisms exercised are diverse:

- [bgfx](https://github.com/bkaradzic/bgfx) cross-platform rendering (OpenGL + [Metal](https://developer.apple.com/metal/)) and GLSL shader authoring
- GPU-based texture compositing (non-standard atlas generation pipeline)
- [Computational geometry](https://en.wikipedia.org/wiki/Computational_geometry): constrained Delaunay triangulation, polygon-with-holes processing, mesh quality refinement
- [ESRI shapefile](https://en.wikipedia.org/wiki/Shapefile) parsing and geographic coordinate systems (antimeridian handling, hemisphere splitting)
- C++ RAII/pImpl architecture and resource lifetime management
- Physics-style interpolation (exponential decay, quaternion slerp for rotation damping)
- Asset pipeline design (binary formats, JSON manifests, incremental builds)
- Visual regression testing methodology (GPU/CPU image comparison, golden images, Git LFS)

A single developer proficient in all of these would be exceptional. Computational geometry and GPU rendering are each deep specialisms; combining them with asset pipeline design and physics-based interaction in a single week of work would typically require 2-3 people.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **yourworld2** (60 commits) | 8-15 | Architecture decisions (Triangle over earcut, JSON manifest format, RAII pattern choices), visual review of rendered globe quality, directing the engine extraction strategy, testing interactive controls |
| **yourworld** (1 commit) | 0.1 | Quick scheme file addition |
| **Total** | **~8-15 hours** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | The ramp-up cost |
|---------|------------|-----------------|------------------|
| **yourworld2** | 25-40 | 35-60 | bgfx rendering pipeline and Metal backend quirks. Triangle library API and constrained Delaunay theory. Geographic coordinate systems and antimeridian geometry. Asset pipeline design with binary format versioning. Frame-rate-independent physics. All in C++ with manual memory management. |
| **yourworld** | 0.1 | 0.1 | Trivial. |
| **Subtotal** | **25-40** | **~35-60** | |

Adding a ~10-15% context-switching tax for moving between rendering, computational geometry, asset pipeline, physics, and test infrastructure -- even within one project -- brings the realistic single-person estimate to **~40-70 person-days, or roughly 2-4 months**.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **40-70 person-days (2-4 months)** |
| Specialist team (traditional) | **25-40 person-days (1-2 person-months)** |
| Actual human effort this week | **~8-15 hours (~1-2 person-days)** |
| **Multiplier vs. generalist** | **~25-50x** |
| **Multiplier vs. specialist team** | **~15-25x** |

The multiplier is highest for the computational geometry and GPU rendering work, where the AI's ability to handle Triangle library integration, antimeridian edge cases, and bgfx Metal quirks simultaneously eliminated what would traditionally be days of documentation reading and trial-and-error debugging. The human contribution concentrated on architectural judgement -- choosing the right triangulation library, designing the manifest format, directing the engine extraction -- and visual assessment of rendered output that requires seeing the globe and knowing what "correct" looks like.

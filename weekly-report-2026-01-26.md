# Weekly Progress Report — 2026-01-20…26 (7 days)

## Executive Summary

A high-intensity first week of AI-assisted development across **3 repositories** spanning Android build engineering, iOS rendering fixes, and a from-scratch globe rendering prototype. The headline items: **yourworld2** built from zero to a fully rendered globe with country meshes, texture atlases, and visual regression tests in two days; **stock-car-racing** stabilised for Google Play with 16KB page alignment and Firebase SDK upgrade; **yourworld** fixed resolution scaling for modern iPhones.

**44 commits** | **+5,081 net app lines** | **~45-80 person-days traditional equivalent** | **~25-50x multiplier**

### Major Achievements & Innovations

- **GPU-based texture atlas generation** in yourworld2 — rather than stitching country textures on CPU, a two-pass [bgfx](https://github.com/bkaradzic/bgfx) render pipeline composites atlas tiles for arbitrary polygon shapes including antimeridian-crossing territories
- **ESRI shapefile-to-binary mesh pipeline** in yourworld2 — raw [ESRI shapefiles](https://en.wikipedia.org/wiki/Shapefile) parsed, triangulated via the [Triangle](https://www.cs.cmu.edu/~quake/triangle.html) library ([constrained Delaunay triangulation](https://en.wikipedia.org/wiki/Constrained_Delaunay_triangulation) with quality refinement), and serialised to a compact binary format, separating expensive geometry from runtime
- **Full globe prototype in two days** — yourworld2 went from an empty repository to sphere rendering, country outlines, texture atlases, per-country saturation control, visual regression tests, and a clean RAII/pImpl architecture
- **Android 16KB page compliance via CMake post-processor** in stock-car-racing — injected `-Wl,-z,max-page-size=16384` into IL2CPP's generated build files, a surgical fix working across Unity versions without engine modification
- **Visual regression testing for GPU output** in yourworld2 — [ImageDiff](https://en.wikipedia.org/wiki/Image_differencing) module with both GPU-accelerated and CPU comparison paths, configurable thresholds, and golden images in [Git LFS](https://git-lfs.com/)

### Tough Challenges Overcome

- **Split Application Binary causing `Resources.Load` failures on Android 13+** (stock-car-racing): APK Expansion Files (OBB) are broken on modern Android; disabling Split Application Binary and bundling resources directly into the APK/AAB resolved silent asset loading failures that produced no useful error messages
- **Corrupted Gradle caches masquerading as adapter bugs** (stock-car-racing): Facebook and MyTarget ad adapters were disabled after D8 dex failures and `StackOverflowError` during R file generation — root cause was corrupted Gradle caches, not the adapters themselves. Re-enabling them after cache cleanup revealed a genuine secondary bug: Facebook Audience Network SDK 6.21.0 has a D8 [NullPointerException](https://developer.android.com/reference/java/lang/NullPointerException) on AAB bundle builds, requiring a downgrade to 6.20.0.0
- **Triangle library replacing earcut for quality mesh generation** (yourworld2): [earcut.hpp](https://github.com/mapbox/earcut.hpp) produced degenerate triangulations on complex country polygons with holes; switching to Jonathan Shewchuk's [Triangle](https://www.cs.cmu.edu/~quake/triangle.html) with constrained Delaunay triangulation and quality refinement eliminated the artefacts
- **Antimeridian-crossing territories** (yourworld2): countries like Russia and Fiji span the [antimeridian](https://en.wikipedia.org/wiki/180th_meridian) — the texture atlas generator uses a two-pass approach, rendering the main hemisphere and the wrapped portion separately, to correctly composite these disjoint regions

Contributor: Marcelo Cantos

---

## Game Projects

### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) — Android Build Stabilisation (5 commits)

A [Unity](https://unity.com/)-based racing game targeting [Google Play](https://play.google.com/). This week focused entirely on getting Android builds passing and meeting current Google Play compliance requirements.

- **Build fixes**: Disabled then re-enabled Facebook and [MyTarget](https://mytarget.my.com/) ad adapters (root cause: corrupted [Gradle](https://gradle.org/) caches, not the adapters), fixed `AndroidManifest` namespace attribute, added launcher template gradle, increased Gradle JVM memory to handle AAB bundling
- **Facebook SDK regression**: Downgraded Facebook Audience Network adapter from 6.21.0.0 to 6.20.0.0 — the newer version triggers a [D8](https://developer.android.com/tools/d8) `NullPointerException` during AAB dex merging
- **Android 13+ asset loading**: Disabled Split Application Binary ([APK Expansion Files](https://developer.android.com/google/play/expansion-files)) — `Resources.Load` silently fails on Android 13+ with OBB-based asset delivery, returning null for assets that load fine in the editor
- **16KB page size compliance**: Google Play now requires [16KB page alignment](https://developer.android.com/guide/practices/page-sizes) for native libraries. Upgraded [Firebase](https://firebase.google.com/) Unity SDK 12.4.1 to 13.7.0 for native 16KB support, added an [IL2CPP](https://docs.unity3d.com/Manual/IL2CPP.html) CMake post-processor injecting `-Wl,-z,max-page-size=16384`, enabled [R8](https://developer.android.com/build/shrink-code) minification for smaller AAB, added [ProGuard](https://www.guardsquare.com/proguard) rules to protect Unity `PlayerPrefs` and `SharedPreferences`
- **Build infrastructure**: Post-build script for `symbols.zip` and `mapping.txt` generation, version code bump to 209, copied TMP Default Style Sheet to active Resources folder

### [squz/yourworld](https://github.com/squz/yourworld) — iOS Resolution Fix (3 commits)

A geography quiz game built in [Objective-C++](https://en.wikipedia.org/wiki/Objective-C#Objective-C++) with [OpenGL ES](https://en.wikipedia.org/wiki/OpenGL_ES), originally targeting older iPhones.

- **Resolution scaling fix** (#30): Replaced hardcoded resolution tables with dynamic `UIScreen`-based scaling, swapped legacy launch images for a `LaunchScreen.storyboard` — confirmed working on iPhone 16 Pro simulator. 20 files, +290/-258
- **Project documentation**: Added `CLAUDE.md` (189 lines) and `README.md` (298 lines) documenting the legacy codebase architecture, build process, and known issues
- **Xcode scheme**: Added `YourWorldFree.xcscheme` to shared data for consistent IDE configuration

### [squz/yourworld2](https://github.com/squz/yourworld2) — Globe Prototype (36 commits, initial)

**The biggest effort of the week.** A brand-new globe rendering application built from scratch in two days, using [bgfx](https://github.com/bkaradzic/bgfx) for cross-platform rendering (OpenGL/[Metal](https://developer.apple.com/metal/)), [SDL3](https://github.com/libsdl-org/SDL) for windowing, and C++17.

- **Globe rendering**: Sphere mesh generation with configurable subdivision, high-resolution 21600x10800 world texture (stored in [Git LFS](https://git-lfs.com/)), [Gouraud shading](https://en.wikipedia.org/wiki/Gouraud_shading) with specular reflection, per-country saturation control
- **Country rendering pipeline**: [ESRI shapefile](https://en.wikipedia.org/wiki/Shapefile) parser, precompute tool converting shapefiles to compact binary, `CountryData`/`CountryLoader` modules, country outlines as line strips, GPU-based texture atlas generator with two-pass antimeridian handling, per-polygon-part processing for disjoint territories (islands, exclaves)
- **Triangulation**: Started with [earcut.hpp](https://github.com/mapbox/earcut.hpp), replaced with [Triangle](https://www.cs.cmu.edu/~quake/triangle.html) for [constrained Delaunay triangulation](https://en.wikipedia.org/wiki/Constrained_Delaunay_triangulation) with quality refinement. Implemented [Douglas-Peucker](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm) mesh simplification (added then removed in favour of Triangle's built-in quality refinement)
- **Architecture**: [pImpl](https://en.cppreference.com/w/cpp/language/pimpl) pattern (`Application`/`State` separation), [RAII](https://en.wikipedia.org/wiki/Resource_acquisition_is_initialization) wrappers (`BgfxContext`, `SdlContext`, `BgfxResource`), resource abstractions (`Texture`, `Mesh`, `Model`), `State` simplified to plain struct
- **Visual testing**: Golden-image regression tests with [Git LFS](https://git-lfs.com/) storage, `ImageDiff` module (GPU-accelerated and CPU comparison with configurable thresholds), standalone `render_app` for headless capture, [doctest](https://github.com/doctest/doctest) unit test framework
- **Shader pipeline**: 12 shader files (atlas, diff, line, simple, test variants) compiled via [bgfx shader toolchain](https://bkaradzic.github.io/bgfx/tools.html#shader-compiler-shaderc)
- **Build system**: Makefile with pattern rules for shader compilation, `bin/` directory for all binaries, vendored dependencies ([spdlog](https://github.com/gabime/spdlog), [linalg.h](https://github.com/sgorsten/linalg), [stb_image_write](https://github.com/nothings/stb), [doctest](https://github.com/doctest/doctest), [earcut.hpp](https://github.com/mapbox/earcut.hpp), [Triangle](https://www.cs.cmu.edu/~quake/triangle.html), [SQLite3](https://sqlite.org/), bgfx/bimg/bx submodules)

Application code: +5,343/-1,383 (net +3,960) across 83 files. Total including vendored libraries: +313,987/-8,611 (sqlite3.c 261K, triangle.c 16K, doctest.h 7K, plus header-only libraries and bgfx submodules).

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 3 |
| Total commits | 44 |
| Total lines added | +7,423 |
| Total lines removed | -2,342 |
| Net new lines | +5,081 |
| File changes | ~107 |
| New files created | 81 |
| Languages | C++, GLSL, C#, Objective-C++, Makefile, Gradle, XML, Markdown |
| Contributors | 1 (Marcelo Cantos) |

*yourworld2 line counts exclude vendored dependencies (sqlite3.c, triangle.c, doctest.h, header-only libraries, bgfx/bimg/bx submodules). Total including vendor: +316,067/-9,570.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [squz/yourworld2](https://github.com/squz/yourworld2) | 36 | ~83 | +5,343 | -1,383 | +3,960* |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 5 | ~24 | +1,224 | -701 | +523 |
| [squz/yourworld](https://github.com/squz/yourworld) | 3 | ~24 | +856 | -258 | +598 |

*\*Application code only; excludes vendored libraries. With vendor: +313,987/-8,611.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [squz/yourworld2](https://github.com/squz/yourworld2) | ~8 | Visual regression tests, ImageDiff module, doctest framework |
| **Total** | **~8** | |

---

## Ideas & Innovations

### GPU-Based Texture Atlas Generation ([yourworld2](https://github.com/squz/yourworld2))

Country texture atlases are traditionally composited on CPU by sampling and copying pixel rectangles — a slow process that struggles with irregular polygon shapes and territories spanning the [antimeridian](https://en.wikipedia.org/wiki/180th_meridian). The yourworld2 atlas generator instead **renders each country's texture region as a GPU draw call via bgfx**, using the country's triangulated mesh as the render geometry. A two-pass approach handles antimeridian-crossing territories: the first pass renders the main hemisphere, the second pass wraps the longitude coordinates and renders the overflow. This produces correctly composited atlases for arbitrary polygon shapes — including Russia's 11-timezone span and Fiji's dateline straddle — at GPU speed.

### ESRI Shapefile to Binary Mesh Pipeline ([yourworld2](https://github.com/squz/yourworld2))

The geometry processing pipeline separates expensive computational geometry from runtime startup. Raw [ESRI shapefiles](https://en.wikipedia.org/wiki/Shapefile) (the de facto standard for geopolitical boundary data) are parsed, then each country's polygon parts are **triangulated using constrained Delaunay triangulation with quality refinement** via Jonathan Shewchuk's [Triangle](https://www.cs.cmu.edu/~quake/triangle.html) library, and serialised to a compact binary format. The precompute step handles the hard cases — polygons with holes, multi-part territories (islands, exclaves), degenerate input geometries — so the runtime application loads pre-triangulated meshes and starts rendering immediately.

### Visual Regression Testing for Rendering ([yourworld2](https://github.com/squz/yourworld2))

Pixel-perfect image comparison breaks across GPU vendors, driver versions, and floating-point rounding differences. The `ImageDiff` module provides **threshold-based comparison with both GPU-accelerated and CPU paths**, comparing rendered output against golden images stored in Git LFS. The GPU path runs a diff shader to produce a difference image; the CPU path computes per-pixel distance metrics. Configurable thresholds allow tests to tolerate minor rounding differences while catching genuine rendering regressions. A standalone `render_app` binary enables headless capture for CI integration.

### CMake Post-Processor for 16KB Page Alignment ([stock-car-racing](https://github.com/minicadesmobile/stock-car-racing))

Google Play's [16KB page size requirement](https://developer.android.com/guide/practices/page-sizes) demands that native libraries be linked with 16KB-aligned segments. Unity's [IL2CPP](https://docs.unity3d.com/Manual/IL2CPP.html) backend generates CMake build files that the developer cannot directly control. Rather than patching or rebuilding the IL2CPP toolchain, **a CMake post-processor script injects the `-Wl,-z,max-page-size=16384` linker flag** into IL2CPP's generated `CMakeLists.txt` after Unity produces it but before the native build runs. This surgical approach works across Unity versions without modifying the engine and is trivially removable once Unity adds native 16KB support.

---

## Effort Estimate: Traditional vs. AI-Assisted

This is the first week of AI-assisted development. The work is notable for its breadth across very different domains — Unity/Android build engineering, iOS/Objective-C++ rendering, and from-scratch C++ application architecture with computational geometry.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **yourworld2** | 15-25 | From-scratch globe renderer in two days. [Constrained Delaunay triangulation](https://en.wikipedia.org/wiki/Constrained_Delaunay_triangulation) is research-grade computational geometry. The shapefile-to-mesh pipeline handles degenerate polygons, holes, multi-part territories, and antimeridian wrapping. GPU-based atlas generation is a non-standard rendering technique. RAII/pImpl architecture, visual regression testing with threshold-based image comparison, 12 shader files. The breadth of the stack — C++, bgfx, SDL3, GLSL, computational geometry, geographic data formats — demands rare cross-domain fluency. |
| **stock-car-racing** | 5-10 | Unity/Android build engineering is notoriously opaque. Debugging D8 dex failures, Gradle cache corruption, APK Expansion File breakage on Android 13+, and IL2CPP CMake post-processing requires deep knowledge of the Unity-to-Android build pipeline. Firebase SDK major upgrade (12.4.1 to 13.7.0) across a mature project with ad mediation. ProGuard rule authoring to protect Unity internals. |
| **yourworld** | 3-5 | Legacy Objective-C++/OpenGL ES codebase with no documentation. Resolution scaling fix requires understanding `UIScreen` APIs, launch image history, and OpenGL ES viewport configuration across iPhone generations. |

### The Diversity Tax

The specialisms exercised in a single week:

- [bgfx](https://github.com/bkaradzic/bgfx) cross-platform rendering (OpenGL + Metal) and GLSL shader authoring
- [Computational geometry](https://en.wikipedia.org/wiki/Computational_geometry): constrained Delaunay triangulation, Douglas-Peucker simplification, polygon-with-holes processing
- [ESRI shapefile](https://en.wikipedia.org/wiki/Shapefile) parsing and geographic coordinate systems
- Unity/Android build pipeline: Gradle, D8/R8, IL2CPP, ProGuard, APK Expansion Files
- [Firebase](https://firebase.google.com/) SDK upgrade and ad mediation integration
- iOS/Objective-C++ rendering with OpenGL ES
- C++ RAII/pImpl architecture and resource management patterns
- Visual regression testing methodology

No single person holds expert-level knowledge in all of these. The Unity/Android build engineering alone is a specialism that teams dedicate full-time resources to; computational geometry with geographic data formats is another; bgfx rendering is a third. In a traditional team, this would involve 2-3 specialists with coordination overhead.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **yourworld2** (36 commits) | 5-10 | Architecture decisions (bgfx vs. other renderers, Triangle vs. earcut), visual review of rendered output, testing country boundary quality, directing the atlas approach |
| **stock-car-racing** (5 commits) | 3-5 | Debugging on physical Android devices, Google Play console interaction, identifying the Facebook SDK version regression through binary search |
| **yourworld** (3 commits) | 1-2 | Testing on iPhone simulator, visual comparison of old vs. new rendering |
| **Total** | **~9-17 hours** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | The ramp-up cost |
|---------|------------|-----------------|------------------|
| **yourworld2** | 15-25 | 25-40 | Computational geometry (Triangle library API, constrained Delaunay theory, polygon winding). bgfx rendering pipeline if unfamiliar. Geographic data formats and coordinate systems. Two-pass antimeridian handling requires domain insight. |
| **stock-car-racing** | 5-10 | 10-20 | Unity-to-Android build pipeline is poorly documented. Each layer (Gradle, D8, IL2CPP, ProGuard) has its own failure modes. The APK Expansion File breakage on Android 13+ is not well-known. Firebase SDK upgrade compatibility matrix. |
| **yourworld** | 3-5 | 5-10 | Legacy Objective-C++/OpenGL ES codebase with no prior documentation. iPhone resolution history and `UIScreen` API evolution. |
| **Subtotal** | **23-40** | **~40-70** | |

Adding a ~10-15% context-switching tax for moving between Unity/Gradle/Android, Objective-C++/iOS, and C++/bgfx/computational geometry in a single week brings the realistic single-person estimate to **~45-80 person-days, or roughly 2-4 months**.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **45-80 person-days (2-4 months)** |
| Specialist team (traditional) | **23-40 person-days (1-2 person-months)** |
| Actual human effort this week | **~9-17 hours (~1-2 person-days)** |
| **Multiplier vs. generalist** | **~25-50x** |
| **Multiplier vs. specialist team** | **~12-25x** |

The multiplier is highest for yourworld2, where the AI seamlessly handled computational geometry, rendering pipeline setup, shader authoring, geographic data parsing, and visual testing methodology — domains that would require at least two specialists traditionally. The human contribution concentrated on architectural direction (choosing bgfx, choosing Triangle over earcut), visual quality assessment, and device-specific debugging that requires physical hardware interaction.

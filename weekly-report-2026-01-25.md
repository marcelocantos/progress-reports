# Weekly Progress Report — 2026-01-19…25

## Executive Summary

The first week of AI-assisted development, spanning **3 repositories** across Android build engineering, iOS rendering, and a from-scratch globe rendering prototype. The headline items: **stock-car-racing** stabilised for Google Play after a succession of Android build failures; **yourworld** fixed resolution scaling for modern iPhones and received its first documentation; **yourworld2** was born — from empty repository to rendered globe with country outlines, ESRI shapefile parsing, and RAII architecture in a matter of days.

**15 commits** | **+3,060 net app lines** | **~20-35 person-days traditional equivalent** | **~10-25x multiplier**

### Major Achievements & Innovations

- **ESRI shapefile-to-mesh pipeline** in yourworld2 — raw [ESRI shapefiles](https://en.wikipedia.org/wiki/Shapefile) parsed, country boundaries extracted, triangulated, and rendered as line strips on a textured globe, with a precomputation step separating expensive geometry processing from runtime
- **Full globe prototype from zero** — yourworld2 went from initial commit to sphere rendering with a 21600x10800 world texture, [Gouraud shading](https://en.wikipedia.org/wiki/Gouraud_shading), country outlines, [pImpl](https://en.cppreference.com/w/cpp/language/pimpl)/[RAII](https://en.wikipedia.org/wiki/Resource_acquisition_is_initialization) architecture, and shader compilation pipeline, all using [bgfx](https://github.com/bkaradzic/bgfx)/[SDL3](https://github.com/libsdl-org/SDL)
- **Android build triage across multiple failure modes** in stock-car-racing — five distinct issues (D8 dex failures, R file generation overflow, manifest namespace, Gradle memory, APK Expansion File breakage on Android 13+) diagnosed and resolved, including the discovery that corrupted Gradle caches were masquerading as adapter bugs
- **Dynamic resolution scaling for modern iPhones** in yourworld — replaced hardcoded resolution tables with `UIScreen`-based scaling and a `LaunchScreen.storyboard`, confirmed on iPhone 16 Pro simulator

### Tough Challenges Overcome

- **Split Application Binary causing silent `Resources.Load` failures on Android 13+** (stock-car-racing): [APK Expansion Files](https://developer.android.com/google/play/expansion-files) (OBB) are broken on modern Android — `Resources.Load` returns null with no error. Disabling Split Application Binary and bundling resources directly into the APK/AAB resolved the issue.
- **Corrupted Gradle caches masquerading as adapter bugs** (stock-car-racing): Facebook and MyTarget ad adapters were initially disabled after D8 dex failures and `StackOverflowError` during R file generation. Root cause was corrupted Gradle caches, not the adapters. Re-enabling them after cache cleanup revealed a genuine secondary bug: Facebook Audience Network SDK 6.21.0 has a D8 [NullPointerException](https://developer.android.com/reference/java/lang/NullPointerException) on AAB builds, requiring a downgrade to 6.20.0.0.
- **Legacy Objective-C++/OpenGL ES codebase with no documentation** (yourworld): fixing resolution scaling required understanding the historical progression of iPhone screen sizes, `UIScreen` API evolution, and OpenGL ES viewport configuration — in a codebase that had no README, no CLAUDE.md, and no comments explaining the rendering pipeline.

Contributor: Marcelo Cantos

---

## Game Projects

### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) — Android Build Stabilisation (4 commits)

A [Unity](https://unity.com/)-based racing game targeting [Google Play](https://play.google.com/). The game had accumulated several Android build and runtime issues that prevented publishing. This week resolved them in sequence.

- **Ad adapter triage**: Disabled Facebook adapter (D8 `NullPointerException`) and [MyTarget](https://mytarget.my.com/) adapter (`StackOverflowError` during R file generation), then re-enabled both after discovering the root cause was corrupted [Gradle](https://gradle.org/) caches. Subsequently downgraded Facebook Audience Network adapter from 6.21.0.0 to 6.20.0.0 — the newer version has a genuine D8 bug on AAB builds.
- **Build configuration**: Fixed `AndroidManifest` namespace attribute, added launcher template gradle, increased Gradle JVM memory to handle AAB bundling
- **Android 13+ asset loading**: Disabled Split Application Binary ([APK Expansion Files](https://developer.android.com/google/play/expansion-files)) — `Resources.Load` silently fails on Android 13+ with OBB-based asset delivery. Copied TMP Default Style Sheet to active Resources folder.
- **Infrastructure**: Added `CLAUDE.md` for AI-assisted development, bumped `versionCode` to 209

### [squz/yourworld](https://github.com/squz/yourworld) — iOS Resolution Fix (3 commits)

A geography quiz game built in [Objective-C++](https://en.wikipedia.org/wiki/Objective-C#Objective-C++) with [OpenGL ES](https://en.wikipedia.org/wiki/OpenGL_ES), originally targeting older iPhones. The game rendered at incorrect resolutions on modern devices due to hardcoded screen size tables.

- **Resolution scaling fix** (#30): Replaced hardcoded resolution tables with dynamic `UIScreen`-based scaling, swapped legacy launch images for a `LaunchScreen.storyboard` — confirmed working on iPhone 16 Pro simulator. 20 files, +290/-258
- **Project documentation**: Added `CLAUDE.md` (189 lines) and `README.md` (298 lines) documenting the legacy codebase architecture, build process, and known issues (#32)
- **Xcode scheme**: Added `YourWorldFree.xcscheme` to shared data for consistent IDE configuration

### [squz/yourworld2](https://github.com/squz/yourworld2) — Globe Prototype (8 commits, initial)

**The biggest effort of the week.** A brand-new globe rendering application, the seed of what becomes a major project. Built from scratch in C++17 using [bgfx](https://github.com/bkaradzic/bgfx) for cross-platform rendering (OpenGL/[Metal](https://developer.apple.com/metal/)) and [SDL3](https://github.com/libsdl-org/SDL) for windowing.

- **Globe rendering**: Sphere mesh generation, high-resolution 21600x10800 world texture (stored in [Git LFS](https://git-lfs.com/)), [Gouraud shading](https://en.wikipedia.org/wiki/Gouraud_shading) with specular reflection
- **Country outline pipeline**: [ESRI shapefile](https://en.wikipedia.org/wiki/Shapefile) parser, precompute tool converting raw shapefiles to a compact binary format, `CountryData` module, country outlines rendered as yellow line strips on the globe
- **Architecture**: [pImpl](https://en.cppreference.com/w/cpp/language/pimpl) pattern from day one (`Application`/`State` separation), [RAII](https://en.wikipedia.org/wiki/Resource_acquisition_is_initialization) resource management, clean separation of concerns
- **Build system**: Makefile with pattern rules for [bgfx shader compilation](https://bkaradzic.github.io/bgfx/tools.html#shader-compiler-shaderc), vendored dependencies ([spdlog](https://github.com/gabime/spdlog), [linalg.h](https://github.com/sgorsten/linalg), [SQLite3](https://sqlite.org/)), bgfx/bimg/bx as Git submodules
- **Vendor dependencies**: sqlite3.c (261K lines), linalg.h, and other header-only libraries vendored into the repository

Non-vendored application code: +1,720/-147 lines across 32 files (31 new).

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 3 |
| Total commits | 15 |
| Total lines added | +3,060 |
| Total lines removed | -478 |
| Net new lines | +2,582 |
| File changes | ~57 |
| New files created | ~44 |
| Languages | C++, GLSL, C#, Objective-C++, Makefile, Gradle, XML, Markdown |
| Contributors | 1 (Marcelo Cantos) |

*yourworld2 line counts exclude vendored dependencies (sqlite3.c, linalg.h, bgfx/bimg/bx submodules). stock-car-racing line counts include generated Gradle configuration files.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [squz/yourworld2](https://github.com/squz/yourworld2) | 8 | ~32 | +1,720 | -147 | +1,573* |
| [squz/yourworld](https://github.com/squz/yourworld) | 3 | ~24 | +856 | -258 | +598 |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 4 | ~24 | +484 | -73 | +411 |

*\*Application code only; excludes vendored libraries.*

### Testing

No new automated tests were added this week. The yourworld2 visual regression testing infrastructure arrives in the following week.

---

## Ideas & Innovations

### ESRI Shapefile to Country Outline Pipeline ([yourworld2](https://github.com/squz/yourworld2))

Rendering political boundaries on a globe requires converting geopolitical boundary data from [ESRI shapefiles](https://en.wikipedia.org/wiki/Shapefile) — the de facto standard for this kind of geographic data — into GPU-renderable geometry. The yourworld2 pipeline **separates expensive parsing from runtime** by running a precompute tool that reads raw shapefiles, extracts polygon boundaries, and serialises them to a compact binary format. The runtime application then loads pre-processed data and renders country outlines as line strips. This two-stage approach keeps the application startup fast and the rendering code clean, while the precompute step can be re-run whenever the source data changes.

### pImpl/RAII Architecture from Day One ([yourworld2](https://github.com/squz/yourworld2))

Many rendering prototypes start with global state and refactor later — if ever. The yourworld2 prototype adopted the **pImpl pattern with RAII resource management from the first commit**, separating `Application` from `State` and wrapping bgfx/SDL3 resources in scope-guarded objects. This is a deliberate architectural bet: the upfront cost is small, but it pays dividends as the codebase grows, because resource lifetimes are always well-defined and the public API surface remains stable even as internals are restructured. The fact that the project later undergoes a full rendering backend migration (bgfx to Dawn/WebGPU) without rewriting the application layer validates this early investment.

### Gradle Cache Corruption as a Red Herring ([stock-car-racing](https://github.com/minicadesmobile/stock-car-racing))

The initial diagnosis — that Facebook and MyTarget ad adapters were causing D8 dex failures and R file generation overflows — was wrong. The real problem was **corrupted Gradle caches producing misleading error messages** that pointed at the adapters. This is a good example of a common trap in build engineering: the error message names a component, but the fault lies in the build system's cached state. The fix was to clean the cache and re-enable the adapters, which then revealed a genuine but different bug (Facebook SDK 6.21.0 D8 NullPointerException on AAB builds). The debugging sequence — disable, identify root cause elsewhere, re-enable, discover real secondary issue — is worth documenting because the layered failure mode is easy to misdiagnose.

---

## Effort Estimate: Traditional vs. AI-Assisted

This is the first week of AI-assisted development. The work is modest in volume — 15 commits across 3 repos — but spans three very different domains: Unity/Android build engineering, iOS/Objective-C++ rendering, and from-scratch C++ application architecture with geographic data processing.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **yourworld2** | 8-12 | From-scratch rendering application with bgfx, SDL3, GLSL shaders, sphere geometry, ESRI shapefile parsing, precomputation pipeline, and pImpl/RAII architecture. The shapefile parser alone requires understanding a binary geographic data format. Not yet at the computational geometry stage (triangulation comes later), but the rendering pipeline setup, shader compilation toolchain, and build system are non-trivial. |
| **stock-car-racing** | 5-10 | Unity/Android build engineering is notoriously opaque. Four distinct failure modes (D8 dex, R file generation, APK Expansion Files on Android 13+, Gradle cache corruption) each requiring different diagnostic approaches. The layered failure — cache corruption masking a genuine SDK bug — is the kind of issue that burns days. |
| **yourworld** | 3-5 | Legacy Objective-C++/OpenGL ES codebase with no documentation. Resolution scaling fix requires understanding `UIScreen` API evolution, launch image history, and OpenGL ES viewport configuration across iPhone generations. Writing 487 lines of documentation for an undocumented codebase requires reading and understanding the entire project. |

### The Diversity Tax

The specialisms exercised in a single week:

- Unity/Android build pipeline: Gradle, D8, APK Expansion Files, AndroidManifest configuration
- Ad mediation SDKs: Facebook Audience Network, MyTarget
- iOS/Objective-C++ rendering with OpenGL ES and `UIScreen` APIs
- [bgfx](https://github.com/bkaradzic/bgfx) cross-platform rendering (OpenGL + Metal) and GLSL shader authoring
- [ESRI shapefile](https://en.wikipedia.org/wiki/Shapefile) parsing and geographic data formats
- C++ RAII/pImpl architecture and resource management patterns
- Build system engineering (Makefile pattern rules, Gradle configuration)

No single person holds expert-level knowledge in all of these. The Unity/Android build engineering alone is a specialism that teams dedicate full-time resources to; bgfx rendering is another; geographic data formats a third.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **yourworld2** (8 commits) | 3-5 | Architecture decisions (bgfx, SDL3, pImpl from day one), directing the shapefile pipeline approach, visual review of rendered globe |
| **stock-car-racing** (4 commits) | 2-4 | Debugging on physical Android devices, Google Play console interaction, identifying cache corruption as root cause |
| **yourworld** (3 commits) | 1-2 | Testing on iPhone simulator, visual comparison of old vs. new rendering |
| **Total** | **~6-11 hours** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | The ramp-up cost |
|---------|------------|-----------------|------------------|
| **yourworld2** | 8-12 | 12-18 | bgfx rendering pipeline if unfamiliar. GLSL shader authoring. ESRI shapefile binary format. Geographic coordinate systems. The pImpl/RAII architecture decisions require C++ design experience. |
| **stock-car-racing** | 5-10 | 8-15 | Unity-to-Android build pipeline is poorly documented. Each layer (Gradle, D8, IL2CPP) has its own failure modes. The APK Expansion File breakage on Android 13+ is not well-known. |
| **yourworld** | 3-5 | 5-8 | Legacy Objective-C++/OpenGL ES codebase with no prior documentation. iPhone resolution history and `UIScreen` API evolution. |
| **Subtotal** | **16-27** | **~25-41** | |

Adding a ~10% context-switching tax for moving between Unity/Gradle/Android, Objective-C++/iOS, and C++/bgfx in a single week brings the realistic single-person estimate to **~20-35 person-days, or roughly 1-2 months**.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **20-35 person-days (1-2 months)** |
| Specialist team (traditional) | **16-27 person-days (1-1.5 person-months)** |
| Actual human effort this week | **~6-11 hours (~1-1.5 person-days)** |
| **Multiplier vs. generalist** | **~15-25x** |
| **Multiplier vs. specialist team** | **~10-20x** |

The multiplier is moderate compared to later weeks — this is a lighter week with 15 commits, and much of the stock-car-racing work involved device-specific debugging that the human had to participate in directly. The yourworld2 prototype shows the higher end of the multiplier: the AI handled shapefile parsing, shader pipeline setup, and build system engineering while the human focused on architectural direction. The multiplier will climb sharply in subsequent weeks as the projects move from setup into sustained feature development.

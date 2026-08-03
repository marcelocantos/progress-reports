# Weekly Progress Report — 2026-01-19…25

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Excl-vendor landed lines: **+1,749/−494** (net **+1,255**).

## Executive Summary

The first week of AI-assisted development, spanning **3 repositories** across Android build engineering, iOS rendering, and a from-scratch globe rendering prototype. Commercial project detail: [private week 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md).

**15 commits** | **~+1,749 / ~−494** (excl. vendor) | **~20-35 person-days traditional equivalent** | **~10-25x multiplier**

### Major Achievements & Innovations

- **ESRI shapefile-to-mesh pipeline** — detail in [private week 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md)
- **Full globe prototype from zero** — detail in [private week 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md)
- **Android build triage across multiple failure modes** — detail in [private week 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md)
- **Dynamic resolution scaling for modern iPhones** — detail in [private week 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md)
### Tough Challenges Overcome

- **Split Application Binary causing silent `Resources.Load` failures on Android 13+** — detail in [private week 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md)
- **Corrupted Gradle caches masquerading as adapter bugs** — detail in [private week 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md)
- **Legacy Objective-C++/OpenGL ES codebase with no documentation** — detail in [private week 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md)
---

## Game Projects

### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) — Android Build Stabilisation (4 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md).*
### [squz/yourworld](https://github.com/squz/yourworld) — iOS Resolution Fix (3 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md).*
### [squz/yourworld2](https://github.com/squz/yourworld2) — Globe Prototype (8 commits, initial)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md).*
## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 3 |
| Total commits | 15 |
| Total lines added | +1,749 |
| Total lines removed | −494 |
| Net new lines | +1,255 |
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

### Daily Activity

![Daily active repositories](daily-activity-2026-01-25.svg)

## Ideas & Innovations

### ESRI Shapefile to Country Outline Pipeline ([yourworld2](https://github.com/squz/yourworld2))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md).*
### pImpl/RAII Architecture from Day One ([yourworld2](https://github.com/squz/yourworld2))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md).*
### Gradle Cache Corruption as a Red Herring ([stock-car-racing](https://github.com/minicadesmobile/stock-car-racing))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-01-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-01-25.md).*
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

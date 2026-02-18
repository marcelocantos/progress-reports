# Weekly Progress Report — 2026-02-13…18 (6 days)

## Executive Summary

Another high-output week across **6 repositories**. The headline: the **csp** library exploded from a bare extraction into a fully-featured CSP microthreading platform (63 commits, 50+ combinators, M:N scheduling, kqueue I/O, TLA+ formal verification). **frozen** underwent a focused allocation-elimination campaign with benchmark-driven results. **multimaze2** swapped its hand-rolled physics for [Box2D v3](https://box2d.org/) and added live-tunable parameter tweaking. **yourworld2** built a country carousel UI with silhouette rendering and audio.

**108 commits** | **+26,573 net lines** | **~100-180 person-days traditional equivalent** | **~30-75x multiplier**

### Major Achievements & Innovations

- **TLA+ formal verification** of 5 concurrency protocols in csp (suspension TOCTOU, work stealing, channel lifecycle, worker parking, alt-state CAS) — unusually rigorous for a C++ library, with deliberate-bug variants to validate the model checker catches violations
- **Demand-paged microthread stacks** in csp: 1 MB mmap'd regions with guard pages consume only actual stack depth in physical RAM; `maybe_shrink()` at channel operations reclaims pages mid-flight so transient deep recursion doesn't hold memory indefinitely
- **Persistent HAMT for dynamic scoping** in csp: `csp::dynamic<T>` provides microthread-local variables with copy-on-write semantics and cross-microthread context transfer via channels — request-scoped logging and transaction contexts without explicit parameter threading
- **Batched spine allocation** for frozen's HAMT: `withFastBatched()` walks the tree iteratively and allocates all spine branches in a single contiguous slice, cutting allocations by 60% and speeding With operations by 39% at 1M-element scale
- **Live-tunable physics** in multimaze2: all physics constants converted to self-registering, atomically-read, SQLite-persisted `tweak::Float` variables adjustable via dashboard UI while the game runs, then extracted to sq submodule for cross-project reuse
- **GPU mesh reuse for silhouettes** in yourworld2: carousel renders country silhouettes directly from the globe's existing GPU buffers with per-cell orthographic viewProj, eliminating duplicate mesh loads, CPU projection, and GPU uploads

### Tough Challenges Overcome

- **M:N scheduler TOCTOU race** (csp): between registering on a channel wait queue and context-switching out, a waker on another thread can call `schedule()` — solved with a three-participant protocol (suspender, waker, drainer) using two atomic booleans, validated by TLA+ exhaustive model checking
- **sync.Map overhead exceeding caching benefit** (frozen): profiling revealed `reflect.TypeOf` keys cost ~26ns per lookup, making the hash/equality cache slower than direct dispatch; required selective reversion of caching and replacing reflect keys with `uintptr` type descriptors to recover 53% of a regression
- **Porting carousel physics from Obj-C** (yourworld2): the original GameState.mm used a three-component force law (linear damping, smoothstep friction, magnetic snap-to-grid) with sub-stepped integration; faithfully reproducing the feel required matching the exact force coefficients and 10-iteration-per-frame symplectic Euler stepping
- **Box2D v3 collision geometry alignment** (multimaze2): balls were intruding into walls by one radius because `kBallRadius` was set to 0.15 instead of 16/47 (half the sprite size) — a subtle mismatch between physics and visual geometry

Contributor: Marcelo Cantos

---

## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — From Extraction to Platform (63 commits)
**The biggest effort of the week.** Last week's bare extraction from bricabrac became a production-grade microthreading library:
- **M:N scheduler**: Work-stealing across OS threads (`init_runtime(n)`), with TLA+ formal verification of the suspension TOCTOU race, work stealing, channel lifecycle, worker parking, and alt-state CAS — 5 models with bug variants verified by [TLC](https://lamport.azurewebsites.net/tla/tools.html)
- **50+ stream combinators** in `csp::part` namespace: `map`, `where`, `scan`, `flat_map`, `batch`, `window`, `slide`, `merge`, `zip`/`unzip`, `round_robin`, `interleave`, `partition`, `group_by`, `share`, `debounce`, `throttle`, `gate`, `metrics`, `reduce`, `first_wins`, `join`, `distinct`, `unique`, `sample`, `delay`, `timeout`, `take_while`, `skip_while`, `pairwise`, `nwise`, `flatten`, `stride`, `default_if_empty` — all header-only with `operator|` composition via `filter`/`producer`/`consumer` wrapper types
- **CSP-aware I/O**: [kqueue](https://en.wikipedia.org/wiki/Kqueue) reactor for non-blocking `read`/`write`/`accept`/`connect`, blocking thread pool for DNS resolution, Unix signal channels via self-pipe trick
- **`csp::dynamic<T>`**: Dynamic-scoped variables backed by a persistent [HAMT](https://en.wikipedia.org/wiki/Hash_array_mapped_trie) (intrusive refcounting, BLR-free read path), with `context`/`context_scope` for snapshot/restore across microthreads
- **Mmap stack pool**: 1 MB mmap'd regions with guard pages, demand-paged (physical memory matches actual depth), `MADV_FREE` lazy reclamation, API-boundary shrinking to reclaim transient deep stacks
- **API refinement**: `chan<T>` structured bindings, move-only endpoints, 0-based `alt`/`prialt` indexing, `~index` bitwise complement for death results, two-phase `prialt` eliminating the `action` class entirely
- **ARM64 stack depth analyzer**: Static analysis of compiled functions to right-size microthread stacks, with BLR elimination for exact analysis
- **Sanitizer support**: Full ASan, UBSan, TSan build targets with [Boost.Context](https://www.boost.org/doc/libs/release/libs/context/) fiber annotations
- **Microbenchmarking**: [nanobench](https://nanobench.ankerl.com/) infrastructure for channel throughput baselines
- **Documentation**: 11-chapter guide (channels, multiplexing, timers, combinators, I/O, blocking, signals, concurrency, error handling, pitfalls, dynamic scoping), 50+ individual part reference pages, architecture document (1,055 lines), 12 runnable examples
- **210 new tests** (298 total), all passing under normal, TSan, and ASan+UBSan builds

### [arr-ai/frozen](https://github.com/arr-ai/frozen) — Allocation Elimination (8 commits)
Benchmark-driven performance campaign following last week's multi-round hashing refactor:
- **Reintroduced `leaf2[T]`** with inline `[2]T` array — the most common collision case now costs 1 heap allocation instead of 2 (struct + slice). IntSet/With **-17-20%**, allocs **-7-20%**
- **Batched spine allocation**: `withFastBatched()` walks the tree iteratively and allocates all spine branches in a single contiguous slice. **~60% fewer allocations** for 1M-element sets (8→3), **~39% faster** With at scale
- **Inlined branch copies**: Direct `ret := *b` struct copy with inline mutation replaces intermediate packer allocation — **halved allocs per level**
- **Boxing elimination**: Per-type dispatch caching for hash/equality hot paths, replacing `any`-boxing of scalars and `hash.Hashable` types. **75% fewer allocations** at 1Mi scale
- **sync.Map overhead reduction**: Replaced `reflect.TypeOf` keys (~26ns lookup) with `uintptr` type-descriptor keys; reverted `value.Equal` to direct type-switch where cache overhead exceeded dispatch savings. IntSet/With recovered **53% of regression** (125.8→105.2 ns/op)
- **Structural vetting**: `frozen_vet` build tag enables tree invariant checking after every operation; `TestPathologicalCollision` exercises 42-level deep trees with constant-hash types

### [arr-ai/hash](https://github.com/arr-ai/hash) — Benchmarking (2 commits)
- Added CLAUDE.md with project guidance
- **Comprehensive hash function benchmarks**: 21 benchmark cases covering all supported types (int8-64, uint8-64, float32/64, string, byte slices, struct, pointer, slice, map, Hashable interface)

### [squz/bricabrac](https://github.com/squz/bricabrac) — Thread Module Retirement (1 commit)
Replaced the entire Thread module with a `csp` git submodule dependency. Thin adapter headers now forward `brac::Thread::*` to `csp::*`. Net **-5,556 lines** as ~5,700 lines of channel, microthread, and combinator code are now consumed from csp.

---

## Game Projects

### [squz/multimaze2](https://github.com/squz/multimaze2) — Box2D & Live Tuning (18 commits)
- **[Box2D v3](https://box2d.org/) integration**: Replaced hand-rolled Euler integration and single-pass collision solver with Box2D's iterative constraint solver. Walls as capsule shapes, balls as dynamic circles, bonds as rigid distance joints, repulsion as pre-step force application. Ball radius corrected from 0.15 to 16/47 (exact sprite boundary match)
- **Live-tunable tweaks system**: All physics constants (`kBallRadius`, `kGravityScale`, `kBallDensity`, `kBallFriction`, `kBallRestitution`, `kBallDamping`, `kWallFriction`, `kBondLength`, `kRepulsionForce`, etc.) converted from `constexpr` to `tweak::Float` with SQLite persistence (`tweaks.db`), atomic values, and self-registering registry. Dashboard integration via GET/POST `/api/tweaks`. Box2D world auto-rebuilds when tweak generation advances
- **Tweak.h extraction**: Moved to sq submodule (`<sq/Tweak.h>`) for cross-project reuse
- **Server lifecycle**: Fix player crash on disconnect, stop server when dashboard tab closes, clean exit on dashboard disconnect
- **sq submodule evolution**: 11 updates bringing sqd daemon mode, iOS TestFlight CI, shared mobile playerLoop, live 3D phone preview in dashboard, Android SIGSEGV fix, background lifecycle handling, Homebrew tap

### [squz/yourworld2](https://github.com/squz/yourworld2) — Country Carousel & Audio (10 commits)
- **Carousel country selector**: Horizontally scrollable strip at screen bottom showing unplaced countries with physics-based scrolling ported from original GameState.mm — snap-to-grid, velocity accumulation with 5/6 boost decay, sub-stepped symplectic Euler integration (10 iterations/frame). 584-line Carousel.cpp with pImpl pattern
- **Country silhouettes**: Initially loaded meshes.bin on CPU and projected to 2D; refactored to render directly from the globe's existing GPU mesh buffers using the atlas pipeline and per-cell orthographic viewProj. Size scaled by country radius with smootherstep curve; orientation rotated in globe-local space to match country position as globe spins
- **Audio**: Background music (`blue_planet_full_loop.mp3`, 0.5 volume, looped) and placement sound effect (`distant_explosion03.wav`) via sq::Audio interface, assets from original yourworld tracked with Git LFS
- **Carousel shader**: New `carousel.wgsl` for 2D UI rendering with per-vertex colour tinting

---

## Other Team Work

### [squz/esfera2](https://github.com/squz/esfera2) — Competitive Multiplayer & Polish (31 commits, Andrew Cantos)
Andrew matured esfera2 from playable to shippable: cinematic intro sequence with phased animations (title, taglines, sphere build, piece placement), bot-vs-bot background gameplay during menus, ELO rating system with variable K-factors (Go backend, Postgres), global and country-specific leaderboards with pagination, player profiles with 193-country selection, nested menu system with pixel-art icons and scrollable rules screen, turn indicator extraction into a testable module (32 test cases), App Store automation (`make testflight`), animation refactoring (4 extracted helpers replacing 3x duplication), and GPU buffer overflow fix for bitmap font rendering. 31 commits, +7,600/-724 lines.

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 6 |
| Total commits | 108 |
| Total lines added | +40,454 |
| Total lines removed | -13,881 |
| Net new lines | +26,573 |
| File changes | 341 |
| Languages | C++, Go, Markdown, WGSL, TLA+, SQL, Python, Shell |

*The bricabrac removal (-5,556 lines) mirrors code now consumed from the csp submodule. The csp line counts exclude last week's initial extraction.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 63 | 241 | +37,241 | -6,838 | +30,403 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 18 | 11 | +643 | -592 | +51 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 10 | 19 | +1,096 | -277 | +819 |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | 8 | 17 | +1,133 | -481 | +652 |
| [squz/esfera2](https://github.com/squz/esfera2) | 6 | 3 | +41 | -42 | -1† |
| [arr-ai/hash](https://github.com/arr-ai/hash) | 2 | 2 | +214 | -9 | +205 |
| [squz/bricabrac](https://github.com/squz/bricabrac) | 1 | 48 | +86 | -5,642 | -5,556* |

*\*Thread module replaced by csp submodule dependency.*
*†sq submodule pointer updates only.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 210 | 298 total; I/O, combinators, M:N, timers, dynamic scoping, TLA+-validated protocols |
| [arr-ai/hash](https://github.com/arr-ai/hash) | 21 | Benchmark suite covering all hashable types |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | 1 | Pathological collision test (42-level deep trees) |
| **Total** | **232** | |

---

## Ideas & Innovations

### TLA+ Verification of a Microthread Scheduler ([csp](https://github.com/marcelocantos/csp))
The csp library's M:N scheduler has a subtle TOCTOU race in its suspension protocol: between the moment a microthread registers on a channel's wait queue and the moment it context-switches out, a waker on another thread can call `schedule()` — but pushing a still-executing MT onto a run queue would cause double execution. The solution uses two atomic booleans (`suspending_`, `wake_pending_`) with a three-participant protocol (suspender, waker, drainer). Rather than relying on code review alone, **5 TLA+ models** (plus 5 deliberate-bug variants) were built and exhaustively verified by the [TLC model checker](https://lamport.azurewebsites.net/tla/tools.html), covering suspension, work stealing, channel lifecycle, worker parking, and alt-state CAS. This is unusually rigorous for a C++ library.

### Demand-Paged Microthread Stacks ([csp](https://github.com/marcelocantos/csp))
Instead of heap-allocating fixed-size stacks, csp maps **1 MB virtual regions** per microthread with a guard page at the base. The kernel demand-pages physical memory as the stack grows, so a microthread using 4 KB of stack consumes 4 KB of RAM, not 1 MB. Freed stacks are cached (up to 256) with `MADV_FREE` for lazy kernel reclamation. The twist: `maybe_shrink()` is called at channel operations to **reclaim unused stack pages mid-flight** — a microthread that briefly recurses deep doesn't hold physical memory indefinitely. Under sanitizers, the system falls back to 128 KB heap allocation to avoid shadow-memory bloat.

### Persistent HAMT for Dynamic Scoping ([csp](https://github.com/marcelocantos/csp))
`csp::dynamic<T>` provides microthread-local variables with copy-on-write semantics, backed by a persistent [HAMT](https://en.wikipedia.org/wiki/Hash_array_mapped_trie) (intrusive refcounting, tagged pointers, BLR-free read path). Child microthreads **inherit the parent's context on spawn**; writes path-copy the HAMT for isolation. Context handles are copyable and sendable over channels, enabling patterns like request-scoped logging or transaction contexts that propagate through microthread topologies without explicit parameter threading.

### Batched Spine Allocation for HAMTs ([frozen](https://github.com/arr-ai/frozen))
The standard HAMT update path allocates one branch copy per tree level during immutable `With` — for a 1M-element set, that's ~8 separate heap allocations walking down the spine. `withFastBatched()` instead **walks down iteratively, then allocates all spine branches in a single contiguous slice**. This trades 3-6% more bytes-per-operation (from slice retention) for **60% fewer GC-tracked objects** and 39% faster operations at scale. Combined with inlined branch copies (eliminating intermediate packer allocations) and the reintroduced `leaf2[T]` (inline `[2]T` array for the common two-element collision case), the week's optimisations cut allocations by up to 75% on key benchmarks.

### GPU Mesh Reuse for 2D Silhouettes ([yourworld2](https://github.com/squz/yourworld2))
The country carousel initially loaded 3D mesh data from `meshes.bin` on the CPU, projected each country to 2D orthographically, and uploaded separate silhouette buffers. The refactored version **renders silhouettes directly from the globe's existing GPU mesh buffers** using the same atlas pipeline and texture bind groups — each carousel cell just gets a different orthographic viewProj matrix looking head-on at the country's centroid. This eliminates the second mesh load, the CPU projection, and the duplicate GPU uploads, while producing identical visual output.

### Live-Tunable Physics via Dashboard ([multimaze2](https://github.com/squz/multimaze2))
All of multimaze2's physics constants (gravity, ball density, friction, restitution, damping, bond parameters, repulsion forces) were converted from `constexpr` to `tweak::Float` — **self-registering, atomically read, SQLite-persisted, and adjustable via the dashboard UI** while the game runs. When the tweak generation counter advances, the Box2D world auto-rebuilds with new parameters. The Tweak.h system was then extracted to the sq submodule for cross-project reuse, so yourworld2 and esfera2 can adopt the same live-tuning workflow.

---

## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **csp** | 40-60 | Building an M:N scheduler with work stealing is a PhD-level concurrency problem. The TLA+ formal verification alone requires expertise in temporal logic. 50+ combinators with correct channel lifecycle semantics. kqueue reactor. HAMT implementation. ARM64 binary analysis. Sanitizer integration with fiber annotations. 1,055 lines of architecture docs. |
| **frozen** | 5-8 | Benchmark-driven allocation elimination requires deep understanding of Go's memory model, GC behaviour, and the HAMT's invariants. Each optimisation (spine batching, leaf2 reintroduction, boxing elimination) needs to preserve correctness across Combine/Difference/Intersection/With/Without while improving benchmarks. |
| **multimaze2** | 5-8 | Box2D v3 integration requires understanding constraint solvers, shape types, and tuning parameters. The tweaks system (self-registering, atomic, SQLite-persisted, dashboard-integrated, auto-rebuilding Box2D world) is non-trivial plumbing. |
| **yourworld2** | 4-6 | Carousel physics (ported from original Obj-C), silhouette rendering (CPU→GPU refactor), audio integration. The orthographic projection per carousel cell, matching globe orientation, requires spatial reasoning. |
| **hash** | 0.5 | Benchmark scaffolding. |
| **bricabrac** | 0.5-1 | Mechanical replacement with adapter headers, but requires understanding both the old Thread API and the new csp API to get the forwarding right. |

### The Diversity Tax

Specialisms exercised this week:

- C++ microthreading, context switching, M:N scheduling, lock-free protocols
- TLA+ formal methods and model checking
- kqueue/reactor-based I/O
- ARM64 instruction set analysis
- HAMT algorithm design and allocation profiling (Go)
- Box2D physics engine integration
- WebGPU/Dawn rendering pipelines and WGSL shaders
- Orthographic projection and globe-space geometry
- SQLite-backed live parameter tuning
- Audio integration (LFS, wire protocol)

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **csp** (63 commits) | 8-15 | Architecture decisions (M:N design, combinator API), reviewing TLA+ specs, testing under sanitizers |
| **frozen** (8 commits) | 2-4 | Benchmark analysis, deciding which allocations to target, reviewing correctness |
| **multimaze2** (18 commits) | 2-4 | Choosing Box2D, tuning physics parameters via the new tweaks UI, testing on devices |
| **yourworld2** (10 commits) | 2-4 | Carousel UX decisions, visual comparison with original game, audio selection |
| **hash** (2 commits) | 0.25 | Quick benchmark pass |
| **bricabrac** (1 commit) | 0.25 | Reviewing the submodule switch |
| **Total** | **~15-28 hours** | |

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~100-180 person-days (5-9 months)** |
| Specialist team (traditional) | **~55-85 person-days (3-5 person-months)** |
| Actual human effort this week | **~15-28 hours (~2-4 person-days)** |
| **Multiplier vs. generalist** | **~30-75x** |
| **Multiplier vs. specialist team** | **~15-35x** |

The multiplier is highest for the csp work, where a single agent traversed M:N scheduler design, TLA+ formal verification, kqueue reactor implementation, ARM64 binary analysis, and comprehensive documentation without context-switch overhead. The human contribution concentrated on architectural vision (the combinator API shape, the decision to formally verify) and quality judgement (reviewing TLA+ specs, benchmark-driven optimisation targets).

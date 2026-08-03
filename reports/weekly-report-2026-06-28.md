# Weekly Progress Report — 2026-06-22…28

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Vendor omitted this week: **+1,494/−2,215** (marcelocantos/sqlpipe +1,494). Excl-vendor landed lines: **+333,602/−20,191** (net **+313,411**).

## Executive Summary

**Eleven repositories** saw substantive landed work this week (sixteen touched in total), spanning MCP developer tooling, dev-environment release engineering, PlantUML layout reverse-engineering, mobile game engineering, and C++ streaming infrastructure. The week's centre of gravity was a **v1.0.0 push in [marcelocantos/den](https://github.com/marcelocantos/den)** (4 commits, +7,848 lines): five v1 **frontier checkpoints** (multi-provider, SAT-solver dependency resolution, migration, deferred upgrades, host detection), the v1 blockers cleared (a trust model, source-build-plus-taps, perf benchmarks), and 🎯T74 RC prep (capability matrix, v1 smoke set, version bump) with a portable-SHA256 fix to the macOS RC pipeline — reaching the **v1.0.0 release candidate**. **[marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)** was again the highest-volume effort (36 commits, +4,050 Rust lines), continuing last week's swimlane-v2 engine into **real-world golden lock-down** — restaurant, shopping-cart, onboarding, approval and expense swimlane parity, partition if-sequence and ETL fork geometry, nested-swimlane if-connector routing, and merge-sort/binary-search while-fork geometry against the Java reference. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** landed the **elimination of daemon idle-CPU burn** (🎯T91/T92) and stopped the open usage-analytics dashboard from burning CPU on its own (🎯T93). **[marcelocantos/csp](https://github.com/marcelocantos/csp)** landed a **prebuilt-library release pipeline** plus a pull-based `io::source` streaming refinement and a TLS `close_notify` fix (🎯T24/T17.3/T17.4/T3.10; the v0.19.0 tag itself falls on 06-29, next window). Significant work sits **in-flight, unmerged** (reported separately): csp's v0.19.0 tag, sawmill's FTS5-plus-vector-plus-RRF discovery/retrieval tier, ge's bgfx-submodule purge and render-on-demand, esfera2's WebGPU→ge rendering port, and HMS's transpiler corpus — all dated 06-29/30, next window. Commercial project detail: [private week 2026-06-28](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-28.md).

**74 commits** | **~+0.33M added / ~−20k removed** (excl. vendor) | **~18-28 person-days traditional equivalent** | **~20-40x multiplier**

> Honesty note: the raw +440,947/−31,807 line figure (net +409,140) is badly distorted by non-authored content. Commercial project detail: [private week 2026-06-28](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-28.md).

### Major Achievements & Innovations

- **den v1.0.0 release candidate** ([marcelocantos/den](https://github.com/marcelocantos/den)) — the dev-environment manager reached its v1 RC across four merges (+7,848 lines): five v1 **frontier checkpoints** (multi-provider, **SAT-solver dependency resolution**, migration, deferred upgrades, host detection, #47), the v1 blockers cleared (a **trust model**, source-build-plus-taps, perf benchmarks, #48), and 🎯T74 RC prep — a capability matrix, a v1 smoke set, and the version bump (#49) — plus a portable-SHA256 fix to the macOS RC pipeline (#50) so the Package binary hashes identically across platforms.
- **ge headless render-to-PNG + camera-basis GlobeController + v0.65 IAP prune** ([squz/ge](https://github.com/squz/ge)) — 🎯T124 turns the GPU pipeline into a deterministic offline renderer (`ge::renderToPng`/`renderBatch`, a `tiltbuggy render` CLI, golden-image fixtures); 🎯T122/T123 make `GlobeController` camera-orientation-agnostic by deriving motion from an explicit camera basis rather than world axes; 🎯T126 prunes revoked IAP entitlements from the cache and shipped in v0.65, consumed downstream by multimaze2 the same week.
- **bullseye v0.36.0 — invariants-hook timeout fix** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)) — 🎯T38 adds a timeout to the invariants hook that had been hanging esfera2 outright, restoring the target-validation path for a downstream repo.
- **sqldeep v0.23.0 — positional-parameter-order safety** ([marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep)) — hardens positional parameter handling so a reordering is detected and fails loudly rather than silently mis-binding arguments (#24).

### Significant Progress

- **rustuml — real-world swimlane golden lock-down (36 commits, on master)** ([marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)) — the week's highest-volume effort: +4,050 Rust lines, −399, continuing last week's second-generation swimlane layout engine into **real-world diagram parity**. Locked restaurant, shopping-cart, onboarding, approval and expense swimlane goldens; matched partition if-sequence and ETL partition fork geometry, replicated swimlane group frames, routed **nested-swimlane if-connectors**, packed switch while-case columns, modelled recursive terminal if-fork branches, aligned nested terminating if-down corridors, and matched merge-sort/binary-search while-fork geometry — plus repeat terminal-survivor and break-survivor corridor routing. Develops on master with no PR ceremony, validated golden-by-golden against the Java PlantUML reference.
- **mnemo — daemon idle-CPU elimination (2 commits)** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)) — 🎯T91/T92 trace and eliminate idle-CPU burn in the mnemo daemon (#128), and 🎯T93 stops the open usage-analytics dashboard from burning CPU on its own (#129); +1,273 lines across 24 files. The cost of getting this wrong is a background tool quietly heating the laptop while doing nothing useful.
- **csp — prebuilt-library release pipeline + pull-based streaming refinement (3 commits)** ([marcelocantos/csp](https://github.com/marcelocantos/csp)) — 🎯T24/T17.3/T3/T17.4/T3.10 land a prebuilt-library release pipeline that ships pre-built artefacts, a TLS `close_notify` fix, an umbrella-header retire, and two design papers (#78); a follow-up refines pull-based `io::source` streaming and the pre-built artefacts (#79); and a `build-libs.sh` fix targets stock macOS bash 3.2 (#80). +2,668 C++ lines. The v0.19.0 release tag is dated 06-29 (next window) — the pipeline work landed here, the tag did not.
- **multimaze2 — StoreKit launch surface (5 commits)** — detail in [private week 2026-06-28](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-28.md)
### Tough Challenges Overcome

- **A daemon that burned CPU while doing nothing** (mnemo) — 🎯T91/T92 traced and eliminated idle-CPU burn in the daemon, and 🎯T93 stopped the open usage-analytics dashboard from polling hot on its own. Idle-liveness tooling that costs CPU when nothing is happening is a subtle, always-on drain rather than a one-off failure.
- **An invariants hook that hung a downstream repo** (bullseye) — 🎯T38 fixes an invariants-hook timeout that had been hanging esfera2's target validation; the fix ships in v0.36.0 and unblocks a repo that could not otherwise run its convergence checks.
- **A globe controller that assumed world-axis orientation** (ge) — 🎯T122/T123 make `GlobeController` camera-orientation-agnostic by driving rotation from an explicit **camera basis** rather than fixed world axes, so globe input behaves correctly regardless of how the camera is oriented — a correctness fix whose absence produces subtly wrong drag directions.
- **An RC pipeline that hashed differently across platforms** (den) — 🎯T74's RC pipeline failed on the macOS build because SHA256 was computed non-portably in the Package binary (#50); the fix makes the hash identical across platforms so the release-candidate artefacts verify consistently.

### Contributors

- Marcelo Cantos

---

## Tooling & Workflow

### [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) — Real-World Swimlane Parity (36 commits)

**The highest-volume effort of the week.** As described in Significant Progress — continuing the swimlane-v2 activity-layout engine into real-world golden lock-down: restaurant/shopping-cart/onboarding/approval/expense swimlane parity, partition if-sequence and ETL fork geometry, nested-swimlane if-connector routing, switch while-case column packing, recursive terminal if-fork branches, nested terminating if-down corridors, merge-sort/binary-search while-fork geometry, and repeat terminal-survivor/break-survivor corridor routing. +4,050 Rust / −399, validated golden-by-golden against the Java PlantUML reference; develops on master with no PR ceremony.

### [marcelocantos/den](https://github.com/marcelocantos/den) — v1.0.0 Release Candidate (4 commits)

- **🎯T74 v1 RC**: as in Major Achievements — five v1 frontier checkpoints (multi-provider, SAT-solver dependency resolution, migration, deferred upgrades, host detection), v1 blockers cleared (trust model, source-build + taps, perf benchmarks), RC prep (capability matrix, v1 smoke set, version bump), and a portable-SHA256 macOS RC-pipeline fix. +7,848 lines across 84 files.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Idle-CPU Elimination (2 commits)

- **🎯T91/T92/T93 CPU-burn elimination**: as in Major Achievements and Tough Challenges — idle-daemon CPU burn traced and eliminated (#128), and the open usage-analytics dashboard no longer burns CPU on its own (#129). +1,273 lines across 24 files.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Invariants-Hook Timeout (1 commit, v0.36.0)

- **🎯T38 invariants-hook timeout**: adds a timeout to the invariants hook that had been hanging esfera2; shipped in v0.36.0 (#115). +203/−8.
### [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) — Tree-Sitter Hygiene (1 commit)

- **🎯T37**: skip oversized and minified files before tree-sitter parsing (#29), avoiding pathological parse cost and memory on generated blobs. +185/−0. (The larger discovery/retrieval tier — FTS5 + vector embeddings + RRF fusion — landed 06-29, next window.)

### [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) — Parameter-Order Safety (1 commit, v0.23.0)

- **Preserve positional parameter order, or fail (#24)**: hardens positional-parameter handling so a reordering is detected rather than silently mis-bound. +339/−8.

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) · [marcelocantos/skills](https://github.com/marcelocantos/skills) — Re-Vendor + Auto-Sync

- **sqlpipe** (1 commit, v0.24.0): bundled sqldeep v0.23.0 + restored `OutMessage`/`Delivery` API (#15) — largely re-vendored amalgamation churn (+15,397/−16,031, footnoted). **skills** (3 commits): automated `Update skills from ~/.claude/skills` syncs (+71/−15).

---

## Game Projects

### [squz/ge](https://github.com/squz/ge) — Headless Render + Camera-Basis GlobeController (3 commits)

- **The biggest engine effort of the week.** — detail in [private week 2026-06-28](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-28.md)

### [squz/multimaze2](https://github.com/squz/multimaze2) — StoreKit Launch Surface (5 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-28](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-28.md).*
### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) — USA Car Pack (5 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-28](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-28.md).*
### [minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit) — Headless Resolve + DebugBridge (4 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-28](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-28.md).*
### [minicadesmobile/dragster-mayhem](https://github.com/minicadesmobile/dragster-mayhem) · [kart-stars](https://github.com/minicadesmobile/kart-stars) · [mopar-drag-n-brag](https://github.com/minicadesmobile/mopar-drag-n-brag) — Fleet Unity 6 / 16KB Compliance

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-28](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-28.md).*
## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Prebuilt-Library Pipeline + Streaming (3 commits)

- **🎯T24/T17.3/T17.4/T3.10 prebuilt-lib pipeline**: as in Significant Progress — a prebuilt-library release pipeline shipping pre-built artefacts, a TLS `close_notify` fix, an umbrella-header retire, and two design papers (#78); a pull-based `io::source` streaming refinement plus the pre-built artefacts (#79); and a `build-libs.sh` fix for stock macOS bash 3.2 (#80). +2,668 C++ / −55. The v0.19.0 tag lands 06-29 (next window).

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

Reported as a forward signal; deliberately excluded from shipped metrics to avoid cross-report double-counting.

- **Health-Management-Systems/hms** — detail in [private week 2026-06-28](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-28.md)
- **squz/esfera2** — detail in [private week 2026-06-28](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-28.md)
- **marcelocantos/csp** — 4 commits in-flight (+1,830/−27): the v0.19.0 release tag lands 06-29, next window.
- **marcelocantos/sawmill** — 3 commits in-flight (+199/−5): the discovery/retrieval tier (FTS5 + vector embeddings + RRF fusion) landed 06-29, next window.
- **squz/ge** — the bgfx-submodule purge and render-on-demand work landed 06-29/30 and falls in next week's window.
- **squz/yourworld2** — detail in [private week 2026-06-28](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-28.md)
---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-06-22…28. In-flight branch work is excluded by design (see the section above).*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | 16 total; **11** with substantive work† |
| Total landed commits | 74 |
| Total in-flight commits (excluded) | 40 |
| Total lines added (landed) | +333,602‡ |
| Total lines removed (landed) | −20,191‡ |
| Net new lines (landed) | +313,411‡ |
| Authored net lines (estimate) | ~+18k (den, rustuml, csp, stock-car-racing, mnemo leading) |
| Languages | Go, Rust, C++, Objective-C++, C, GLSL, C#, Python, Markdown, YAML, JSON, shell |
| Contributors | 1 (Marcelo Cantos) |

†*The other 5 landed repos had trivial or mechanical work: sqlpipe's re-vendor, skills auto-sync, and the dragster-mayhem/kart-stars/mopar-drag-n-brag Unity-6/16KB fleet bumps.*
‡*Line totals are dominated by non-authored content: **dragster-mayhem +405,058/−12,819 is Unity-regenerated** (2 commits, 3,548 files) and **sqlpipe +15,397/−16,031 is a re-vendored sqldeep amalgamation**. Hand-authored merged source is ~+20k added / ~+18k net.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | 36 | 42 | +4,050 | −399 | +3,651 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 5 | 17 | +504 | −191 | +313 |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 5 | 17 | +2,233 | −934 | +1,299 |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 4 | 84 | +7,848 | −1,062 | +6,786 |
| [minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit) | 4 | 6 | +145 | −19 | +126 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 3 | 28 | +2,668 | −55 | +2,613 |
| [squz/ge](https://github.com/squz/ge) | 3 | 54 | +966 | −124 | +842 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 3 | 5 | +71 | −15 | +56* |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 2 | 24 | +1,273 | −29 | +1,244 |
| [minicadesmobile/dragster-mayhem](https://github.com/minicadesmobile/dragster-mayhem) | 2 | 3,548 | +405,058 | −12,819 | +392,239† |
| [minicadesmobile/kart-stars](https://github.com/minicadesmobile/kart-stars) | 2 | 8 | +6 | −112 | −106 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 1 | 5 | +203 | −8 | +195 |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 1 | 5 | +185 | −0 | +185 |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | 1 | 12 | +339 | −8 | +331 |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 1 | 50 | +15,397 | −16,031 | −634‡ |
| [minicadesmobile/mopar-drag-n-brag](https://github.com/minicadesmobile/mopar-drag-n-brag) | 1 | 1 | +1 | −1 | +0 |

\* *skills: auto-sync of `~/.claude/skills`.*
† *dragster-mayhem: +405,058 is almost entirely Unity-regenerated (Unity 6 upgrade + IAP-SDK migration + 16KB compliance).*
‡ *sqlpipe: re-vendored sqldeep amalgamation churn.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [squz/ge](https://github.com/squz/ge) | ~6-8 | render-to-PNG golden-image fixtures + GlobeController camera-basis doctests |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~5 | pull-based `io::source` streaming + prebuilt-lib pipeline doctests |
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | ≈8 goldens | real-world swimlane parity (restaurant, shopping-cart, onboarding, approval, expense) + geometry |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~2 | idle-CPU-burn regression coverage |
| [marcelocantos/den](https://github.com/marcelocantos/den) | qualitative | v1 smoke set + capability matrix (RC harness) |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | 1 | positional-parameter-order safety |
| **Total** | **~22 (+≈8 goldens)** | landed only; conservative diff-grep estimates, in-flight tests not counted |

### Daily Activity

![Daily active repositories](daily-activity-2026-06-28.svg)

*(All-repo active-repository counts per day across the week, from the timeline cache — a broad activity signal counting all authors and all branches, so it runs higher than landed Marcelo-only work and spikes on branch-merge days. Plotted: Mon 06-22 12, Tue 06-23 1, then a quiet 06-24…27, Sun 06-28 17. Landed Marcelo-only work clustered on Mon 06-22; the Sun 06-28 spike is branch/merge activity — much of it the 06-29/30 tranches, in-flight this window.)*

---

## Ideas & Innovations

### Idle Liveness Tooling That Costs Nothing When Idle ([mnemo](https://github.com/marcelocantos/mnemo))
A background daemon and an open analytics dashboard are supposed to sit quietly until something happens — yet mnemo's did the opposite, burning CPU while doing nothing useful and warming the laptop. 🎯T91/T92 trace and eliminate the idle-loop burn in the daemon, and 🎯T93 stops the open usage-analytics dashboard polling hot on its own. The lesson, restated: **liveness tooling must cost nothing when nothing is happening** — an always-on tool's idle cost is paid every second it runs, so it is worth far more scrutiny than a one-off hot path.

### Headless Rendering as a Deterministic Test Surface ([ge](https://github.com/squz/ge))
GPU output is notoriously hard to test because it normally requires a window, a device, and a human eye. 🎯T124 turns ge's pipeline into a **deterministic offline renderer** — `ge::renderToPng`/`renderBatch` plus a `tiltbuggy render` CLI that emits PNGs into a golden-image fixture harness. Rendering becomes a pure function from scene to bytes, comparable in CI. The elegance is that the same surface that ships frames now also grades them, so a rendering regression fails a test instead of surviving to a device.

### SAT-Solver Dependency Resolution Behind a Trust Model ([den](https://github.com/marcelocantos/den))
Reaching v1.0.0 for a dev-environment manager means the dependency resolver can no longer be a best-effort walk — conflicting version constraints must be resolved soundly or rejected. den's v1 checkpoint frames **dependency resolution as a SAT problem** (multi-provider, with migration and deferred upgrades as first-class states) rather than an ad-hoc graph traversal, so "is this environment satisfiable?" becomes a decision procedure with a definite answer. Pairing it with an explicit **trust model** and source-build-plus-taps as gating v1 blockers means the resolver's inputs are as principled as its algorithm — the two together are what make a v1 RC defensible.

### A Globe Controller Anchored to the Camera, Not the World ([ge](https://github.com/squz/ge))
A globe drag that maps screen motion to fixed world axes feels correct only while the camera happens to be upright; tilt or roll the camera and the drag direction quietly diverges from the pointer. 🎯T122/T123 make `GlobeController` **camera-orientation-agnostic by deriving rotation from an explicit camera basis** rather than world axes, so a horizontal drag always rotates the globe horizontally *as the viewer sees it*. The insight is that the natural frame for an input gesture is the camera's, not the scene's — resolving the gesture in camera space and only then projecting onto the globe removes a whole class of orientation-dependent bugs.

### Real-World Diagrams as the Parity Oracle ([rustuml](https://github.com/marcelocantos/rustuml))
Byte-exact reproduction of an undocumented layout engine is easy to overfit: pass a hand-picked set of synthetic goldens and still mislay a real diagram. This week's rustuml work **locks parity against real-world swimlane diagrams** — restaurant, shopping-cart, onboarding, approval and expense workflows — rather than only minimal reproductions. Driving the port from realistic diagrams exercises the combinatorial corners (nested-swimlane if-connectors, partition fork geometry, while-fork survivor corridors) that synthetic cases rarely hit, so the golden that fails is the one a user would actually draw. The oracle is the messy real diagram, not the tidy unit fixture.

### A Prebuilt-Library Release Pipeline for a Compiled Language ([csp](https://github.com/marcelocantos/csp))
Distributing a C++ library normally forces every consumer to build from source — slow, toolchain-sensitive, and a barrier to adoption. csp's 🎯T24 pipeline **ships pre-built artefacts** alongside the source, so downstream projects can link a known-good binary instead of recompiling the world, with `build-libs.sh` hardened down to stock macOS bash 3.2 for portability. Coupled with the pull-based `io::source` streaming model and a TLS `close_notify` fix, the release now carries both a cleaner streaming abstraction and a friendlier distribution story — the kind of packaging work that turns a library from usable into adoptable.

---

## Effort Estimate: Traditional vs. AI-Assisted

A moderate week by commit volume (74 landed) but high in value: a v1.0.0 release-candidate push (den), a deterministic headless-render test surface plus a camera-basis controller (ge), the elimination of daemon idle-CPU burn (mnemo), real-world swimlane parity lock-down (rustuml), a prebuilt-library release pipeline (csp), and a StoreKit launch surface (multimaze2) — polish-and-hardening in character rather than greenfield.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| den v1.0.0 RC | 4-6 | A v1 release-candidate gate: SAT-solver dependency resolution, a trust model, source-build + taps, perf benchmarks, capability matrix, v1 smoke set, and a portable-SHA256 macOS RC-pipeline fix — release engineering across a wide correctness surface. |
| rustuml real-world swimlane parity | 3-5 | Byte-exact reverse-engineering of PlantUML's undocumented swimlane/activity layout (partition fork geometry, nested-swimlane if-connectors, while-fork survivor corridors) against a Java reference, locked golden-by-golden on realistic diagrams. |
| ge headless render + GlobeController | 2-3 | A deterministic offline GPU renderer with golden-image fixtures, a camera-basis input-frame correctness fix, and IAP entitlement-cache pruning — GPU-pipeline and input-geometry depth. |
| mnemo idle-CPU elimination | 2-3 | Diagnosing and eliminating idle-daemon and open-dashboard CPU burn — an always-on observability regression where the failure is silent heat rather than a crash. |
| csp prebuilt pipeline + streaming | 2-3 | A prebuilt-library release pipeline (portable down to bash 3.2), pull-based `io::source` streaming, a TLS `close_notify` fix, and two design papers — packaging plus streaming/TLS silent-wrongness risk. |
| multimaze2 launch surface | 1-2 | StoreKit restore/entitlement flows, legacy "allpacks" migration, paid-pack gating, and a paywall-to-buy-prompt swap — App-Store-review-sensitive correctness. |
| stock-car-racing + Minicades fleet | 1-2 | Designer car-pack integration, headless EDM4U `make resolve-android`, DebugBridge re-filing, and Unity-6/16KB fleet compliance across three shipping games. |
| bullseye / sawmill / sqldeep | 2-3 | An invariants-hook timeout fix (unblocking esfera2), a tree-sitter oversized/minified-file guard, and positional-parameter-order safety. |

### The Diversity Tax

This week spans Go (den's SAT-solver-backed resolver, mnemo's daemon, sqldeep), Rust (rustuml's layout engine), C++ and GLSL (ge, csp), Objective-C++ and Metal (ge's render-to-PNG), C# and Unity lifecycle (stock-car-racing, the Minicades fleet), plus StoreKit IAP, TLS streaming, PlantUML reverse-engineering, and cross-platform release engineering. No single engineer holds SAT-solver-backed package management, PlantUML-layout reverse-engineering, GPU headless-render test design, concurrent-daemon observability, and StoreKit launch flows at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| den | 2-4 | v1 RC review and release-candidate approvals, judging the trust model and dependency-resolution scope. |
| rustuml | 2-3 | Steering the real-world parity push, judging golden diffs, deciding replicate-vs-approximate on undocumented layout behaviour. |
| ge / multimaze2 | 2-4 | Render-to-PNG golden validation, camera-basis input feel checks, IAP/paywall play-testing on device. |
| mnemo / csp / bullseye | 2-3 | Diagnosing idle-CPU burn on the live daemon, streaming-I/O and release-pipeline review, target-graph triage. |
| Everything else | 1-3 | PR review, release approvals (bullseye, sqldeep, sqlpipe), Unity fleet builds, convergence triage. |

### What If It Were One Person?

A single generalist would not merely do the work serially — they would pay a ramp-up cost re-entering each domain (Go release engineering, Rust layout reverse-engineering, GPU render testing, Unity lifecycle, StoreKit) and a context-switching tax bouncing between eight-plus repos in a week. The expert-days estimate above (~18-28) understates the generalist total once those costs are added, which is why the generalist band sits meaningfully higher than a specialist team's.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~18-28 person-days (~0.9-1.4 months)** |
| Specialist team (traditional) | **~11-18 person-days (~0.55-0.9 person-months)** |
| Actual human effort this week | **~9-15 hours (~1.5-2.5 person-days)** |
| **Multiplier vs. generalist** | **~20-40x** |
| **Multiplier vs. specialist team** | **~10-20x** |

The multiplier runs highest on rustuml — reverse-engineering an undocumented Java swimlane-layout engine into Rust golden-by-golden is exactly the cross-domain-recall-and-search task where the AI dominates — and on den's v1 RC hardening, where the breadth of the correctness surface (SAT-solver resolution, trust model, cross-platform RC pipeline) would strand a generalist in unfamiliar territory. It runs lowest on the release/plumbing tail (skills auto-sync, the sqlpipe re-vendor, Unity fleet resolve-android bumps). The human contribution concentrated on judgement a specification can't reach: the v1-RC trust model and scope, which PlantUML behaviours to replicate on real diagrams, the render-to-PNG oracle design, the camera-frame input insight, and on-device ship validation.

# Weekly Progress Report — 2026-06-08…14

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Excl-vendor landed lines: **+24,814/−3,891** (net **+20,923**).

## Executive Summary

**Eight repositories** saw substantive landed work this week (fifteen touched in total), spanning PlantUML layout reverse-engineering, iOS device automation, MCP developer tooling, and mobile game engineering. The dominant effort was **[marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)** (46 commits, +4,794 Rust), which ported the `klimt/compress` **whole-diagram ON_X compression engine** and wired it into the activity renderer, then drove a long tail of faithful golden parity across break/repeat/switch/fork/elseif geometry and Teoz sequence diagrams — the compression-and-parity groundwork beneath the next-generation swimlane engine. Five versioned releases shipped: **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** v0.54/v0.56/v0.57 (**iOS ≤16 deploy/launch/screenshot over lockdown** with no tunneld, plus app-channel state slices and **server-side jq filtering**), **[squz/ge](https://github.com/squz/ge)** v0.57.0 (a **SpriteBatch overflow buffer-pool** with per-frame autorelease drain, a `ge::Metrics` callback, the app-channel state-slice telemetry pipe, and an IDE-free iOS build lane), **[marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)** v0.30.0 (a **git-history target-ID allocator**), **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** v0.48.0 (**token-volume compaction convergence** and status ingest-freshness diagnostics), and **[marcelocantos/vellum](https://github.com/marcelocantos/vellum)** v0.5.0 (a rich-text→Markdown importer). Significant work sits in-flight, unmerged, and is reported as a forward signal: rustuml's next tranche is the swimlane-v2 layout engine (79 commits on worktree branches), landing next week. Commercial project detail: [private week 2026-06-14](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-14.md).

**75 commits** | **~+24,814 / ~−3,891** (excl. vendor) | **~24-38 person-days traditional equivalent** | **~18-30x multiplier**

> Honesty note: the raw +24,951/−4,100 figure carries modest non-authored inflation. **progress-reports' +2,792/−970 is this repo's own output** (the 2026-06-01…07 report-publishing commit), and **multimaze2's +7,047 and ge's line counts include committed binaries** (`.png` sprites and `prebuilt/*.a` static libraries) that distort `git`'s accounting. Genuinely hand-authored, merged source is on the order of **+16-19k lines** — led by multimaze2 (+6.5k C++/GLSL incl. assets), rustuml (+4.2k Rust), spyder (+3.1k Go), mnemo (+1.5k Go), csp (+1.5k C++), and ge (+1.5k C++/Objective-C++).

### Major Achievements & Innovations

- **spyder v0.54/v0.56/v0.57 — iOS ≤16 via lockdown + app-channel state slices** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — v0.54.0 (🎯T78) deploys, launches, and screenshots **iOS ≤16 devices over the lockdown protocol with no tunneld** — no Developer-mode tunnel required — and a follow-up fixes those same devices being silently filtered out by the `devicectl` gate, restoring a whole class of older test hardware. v0.56.0/v0.57.0 (🎯T80/T81) make app-channel state slices agent-consumable with **server-side `jq` filtering** and an `app_state_describe` tool. 32 new Go tests.
- **ge v0.57.0 — SpriteBatch overflow pooling, metrics callback, app-channel telemetry** ([squz/ge](https://github.com/squz/ge)) — 🎯T113/T114 add a **SpriteBatch overflow buffer-pool plus a per-frame autorelease-pool drain** to bound transient GPU allocation under sprite-heavy frames; 🎯T111 exposes a `ge::Metrics` engine performance-metrics callback via `RunConfig::onMetrics`; 🎯T115/T116/T117 bless the app-channel state-slice telemetry pipe as documented, add volunteered example payloads, and ship a header-only `ge::box2d::worldGeometry` convenience; 🎯T110 adds an IDE-free iOS build/deploy lane. 25 new doctest cases.
- **bullseye v0.30.0 — git-history target-ID allocator** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)) — 🎯T28 allocates target IDs from git history rather than from the working file, so parallel worktrees and agents never mint the same 🎯T-id twice. 7 new Rust tests.
- **mnemo v0.48.0 — token-volume compaction convergence + ingest-freshness diagnostics** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)) — 🎯T72 makes transcript compaction converge on token volume (addenda treated as a tail, a precise recursion guard); 🎯T75 exposes transcript-ingest freshness and per-source lag diagnostics through `mnemo_status`. 17 new Go tests.
- **vellum v0.5.0 — rich-text import to Markdown** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum)) — adds an importer converting rich-text formats (RTF/DOCX/HTML/ODT/EPUB and friends) to Markdown, with new MCP tools and 4 Go tests.

### Significant Progress

- **rustuml — whole-diagram compression engine port + golden parity (46 commits, on master)** ([marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)) — +4,794 Rust / −612, developing directly on master against the Java PlantUML reference. The centrepiece is a **faithful port of `klimt/compress`'s whole-diagram ON_X compression engine** (`26868030`), wired into the activity renderer (`f3c7a7da`) with connector polygons/paths counted as ON_X occupancy exactly as PlantUML's `SlotFinder` would (`d3d02572`). Around it, a long tail of byte-exact golden parity: break-corridor stretch and break-if loop-back fusion, nested-repeat tail expansion and asymmetric `FtileRepeat` spine/arm, switch ON_X compression and in-while switch merge bands, `FtileForkInner` and mixed-asymmetry fork spines, `FtileIfLongHorizontal` elseif geometry, and extensive Teoz sequence work (group-frame geometry, livebox constraints, named-box footers, note-frame margins). 11 new `#[test]` plus wide golden-fixture parity updates.
- **csp — pull-based `io::source` streaming (2 commits)** ([marcelocantos/csp](https://github.com/marcelocantos/csp)) — 🎯T17 introduces a **pull-based `io::source`** threaded through `tls::stream` and `http::fetch` streaming bodies, replacing the push-based `net::connection.input`; 🎯T17.1 then makes `http::serve`'s `handle_connection` read through the same `fd_source` (dup-and-drop before the WebSocket hijack handoff so the upgrade handler reads the original fd cleanly). Unreleased this week (the v0.19.0 tag falls in a later window). 4 new doctest cases.
- **multimaze2 — iOS v1 readiness (1 commit)** — detail in [private week 2026-06-14](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-14.md)
### Tough Challenges Overcome

- **iOS ≤16 automation without a Developer-mode tunnel** (spyder) — modern iOS device automation assumes a tunneld/Developer-mode tunnel that iOS ≤16 devices don't provide; 🎯T78 reaches deploy/launch/screenshot over the **lockdown protocol** directly, and a follow-up fixes those same devices being silently filtered out by the `devicectl` gate. The capability was present all along; the modern gatekeeper simply assumed it wasn't.
- **SpriteBatch overflow under Metal driver pressure** (ge) — 🎯T113/T114 add an overflow buffer-pool to `SpriteBatch` plus a per-frame autorelease-pool drain, bounding unbounded transient GPU allocation in sprite-heavy frames — a real driver-pressure failure mode, not a theoretical one.
- **An iOS jetsam kill under memory pressure** — detail in [private week 2026-06-14](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-14.md)
- **Byte-exact whole-diagram compression parity** (rustuml) — porting PlantUML's `klimt/compress` engine faithfully means replicating undocumented ON_X occupancy accounting (counting connector polygons/paths and inter-diamond arrowheads exactly as `SlotFinder` does) so that compressed activity diagrams match the Java reference golden-by-golden.

### Contributors

- Marcelo Cantos

---

## Tooling & Workflow

### [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) — Compression Engine + Golden Parity (46 commits)

**The biggest effort of the week.** As described in Significant Progress — the `klimt/compress` whole-diagram ON_X compression engine ported and wired into the activity renderer, then a long tail of faithful golden parity.

- **The biggest effort of the week.** **Compression engine**: a faithful port of `klimt/compress`'s whole-diagram compression (`26868030`), wired into the activity renderer (`f3c7a7da`), counting connector polygons/paths as ON_X occupancy like PlantUML's `SlotFinder` (`d3d02572`).
- **Activity parity**: break-corridor stretch and last-flow break-if loop-back fusion in while loops, nested-repeat tail expansion, switch ON_X compression, in-while switch merge bands and loop-back anchors, `FtileForkInner` and mixed-asymmetry fork spines, `FtileIfLongHorizontal`/`FtileIfLong` elseif branch placement and diamond-row spacing, and single-survivor-if spine reconvergence under redirect.
- **Teoz sequence parity**: faithful Teoz group-frame geometry, livebox constraints and foot layout, named-box-frame footers, nested-group left floor and note-frame margins, guillemets and open-group area reservation.
- **Metrics**: +4,794 Rust / −612; 11 new `#[test]`, plus wide golden-fixture parity updates (existing fixtures brought to parity, not new files). Develops on master with no PR ceremony.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Compaction Convergence (3 commits, v0.48.0)

- **🎯T72 token-volume compaction convergence**: compaction converges on token volume with addenda treated as a tail and a precise recursion guard.
- **🎯T75 ingest-freshness diagnostics**: `mnemo_status` exposes transcript-ingest freshness and per-source lag diagnostics. 17 new Go tests.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Git-History ID Allocator (1 commit, v0.30.0)

- **🎯T28 git-history ID allocator**: as in Major Achievements — target IDs allocated from git history so parallel worktrees never collide on a 🎯T-id. 7 new Rust tests.

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — Rich-Text Import (1 commit, v0.5.0)

- **Rich-text→Markdown importer**: converts RTF/DOCX/HTML/ODT/EPUB and related formats to Markdown; new MCP tools, 4 Go tests.

### [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) · [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) · [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) · [marcelocantos/skills](https://github.com/marcelocantos/skills) · [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Routine Maintenance

- **`mk`→`cv` migration**: sqldeep (#22), sqlift (#18), and sqlpipe (#13) each land the `mk`→`cv` rename. **skills** (2): the `mk`→`cv` migration plus stale-doc removal. **claudia** (2): `bullseye.yaml` update and stale `docs/targets.{yaml,md}` removal.

---

## Libraries & Infrastructure

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — iOS ≤16 Lockdown + App-Channel Slices (4 commits, 3 releases)

- **🎯T78/T80/T81**: as in Major Achievements — iOS ≤16 deploy/launch/screenshot over lockdown (no tunneld), the `devicectl`-gate filtering fix, agent consumption of app-channel state slices with server-side `jq` filtering, and `app_state_describe`. 32 new Go tests.

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Pull-Based Streaming I/O (2 commits)

- **🎯T17 pull-based `io::source`**: as in Significant Progress — a pull-based `io::source` threaded through `tls::stream` and `http::fetch` streaming bodies, with `http::serve`'s `handle_connection` reading via `fd_source` (🎯T17.1). 4 new doctest cases.

---

## Game Projects

### [squz/ge](https://github.com/squz/ge) — Buffer-Pool + Telemetry Pipe (7 commits, v0.57.0)

- **🎯T113/T114/T111/T115/T116/T117/T110**: as in Major Achievements — a SpriteBatch overflow buffer-pool plus per-frame autorelease drain, a `ge::Metrics` callback (`RunConfig::onMetrics`), the app-channel state-slice telemetry pipe blessed as documented with example payloads and a `ge::box2d::worldGeometry` convenience, and an IDE-free iOS build/deploy lane. 25 new doctest cases.

### [squz/multimaze2](https://github.com/squz/multimaze2) — iOS v1 Readiness (1 commit)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-14](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-14.md).*
### [squz/yourworld2](https://github.com/squz/yourworld2) — Housekeeping (2 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-14](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-14.md).*
## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

Reported as a forward signal; deliberately excluded from shipped metrics to avoid cross-report double-counting.

- **marcelocantos/rustuml** — 79 commits in-flight (+6,324/−1,025): the **second-generation swimlane layout engine** (swimlane-v2), landing next week.
- **Health-Management-Systems/hms** — detail in [private week 2026-06-14](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-14.md)
- **marcelocantos/mnemo** — 14 commits in-flight (+2,031/−118) beyond the merged v0.48.0.
- **Smaller in-flight tails across jevons (7), multimaze2 (4), s…** — detail in [private week 2026-06-14](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-14.md)
---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-06-08…14. In-flight branch work is excluded by design (see the section above).*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | 15 total; **8** with substantive work† |
| Total landed commits | 75 |
| Total lines added (landed) | +24,814‡ |
| Total lines removed (landed) | −3,891 |
| Net new lines (landed) | +20,923‡ |
| Authored net lines (estimate) | ~+16-19k (multimaze2, rustuml, spyder, mnemo, csp, ge leading) |
| File changes (landed) | 395 (sum of per-repo change events) |
| New files created | 107‡ |
| Languages | Rust, C++, Objective-C++, Swift, GLSL, Go, Ruby, Markdown, YAML, JSON, SQL, shell |
| Contributors | 1 (Marcelo Cantos) |

†*The other 7 touched repos had trivial or mechanical work: `mk`→`cv` renames (sqldeep, sqlift, sqlpipe, skills), `bullseye.yaml`/stale-doc removal (claudia, yourworld2), and the report-publishing commit (progress-reports).*

‡*Line and new-file totals carry modest non-authored inflation: **progress-reports' +2,792/−970 is this repo's own report-publishing output**, and **multimaze2 and ge include committed binaries** (`.png` sprites, `prebuilt/*.a` static libraries) that distort `git`'s accounting — hence 40 of the new files are `.png`. Hand-authored merged source is ~+16-19k.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | 46 | 54 | +4,794 | −612 | +4,182 |
| [squz/ge](https://github.com/squz/ge) | 7 | 80 | +1,711 | −253 | +1,458‡ |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 4 | 51 | +3,159 | −102 | +3,057 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 3 | 30 | +2,066 | −554 | +1,512 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 2 | 20 | +1,648 | −171 | +1,477 |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 2 | 3 | +149 | −467 | −318 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 2 | 9 | +31 | −148 | −117 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 2 | 6 | +77 | −155 | −78 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 1 | 99 | +7,047 | −531 | +6,516† |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 1 | 6 | +2,792 | −970 | +1,822* |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 1 | 10 | +745 | −30 | +715 |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 1 | 13 | +641 | −34 | +607 |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 1 | 5 | +44 | −26 | +18 |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | 1 | 5 | +25 | −25 | +0 |
| [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) | 1 | 4 | +22 | −22 | +0 |

\* *progress-reports: the report-publishing commit for the previous week (this repo's own output), not development work.*
† *multimaze2: line/file counts include committed `.png` sprite binaries and regenerated assets.*
‡ *ge: line counts include committed `prebuilt/*.a` static libraries.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 32 | iOS ≤16 lockdown path, app-channel state slices, jq filtering |
| [squz/ge](https://github.com/squz/ge) | 25 | SpriteBatch buffer-pool, `ge::Metrics` callback, slice descriptors |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 17 | token-volume compaction convergence, ingest-freshness diagnostics |
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | 11 (+ golden parity) | `#[test]` plus extensive golden-fixture parity updates |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 7 | git-history ID allocator |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 4 | pull-based `io::source` / `tls::stream` streaming |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 4 | rich-text import |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 1 | physics/telemetry |
| **Total** | **~101 (+ golden parity)** | landed only; in-flight tests not counted |

*Test counts are landed-only diff-grep figures (added `+` lines matching test markers) within the strict 7-day window.*

### Daily Activity

![Daily active repositories](daily-activity-2026-06-14.svg)

*(All-repo active-repository counts per day, from the timeline cache — a broad activity signal counting all authors and all branches, so it runs higher than landed Marcelo-only work and spikes on branch-merge days. Plotted: Mon 06-08 4, Tue 4, Wed 06-10 6, Thu 5, Fri 0, Sat 0, Sun 06-14 25. The Sunday spike reflects a broad cross-repo landing/merge burst.)*

---

## Ideas & Innovations

### iOS Automation Below the Tunnel ([spyder](https://github.com/marcelocantos/spyder))
Contemporary iOS device automation is built on the Developer-mode tunnel (tunneld/CoreDevice), which simply does not exist on iOS ≤16 — stranding a fleet of older test devices. 🎯T78's insight is that **deploy, launch, and screenshot don't actually need the tunnel** — they can be driven over the older **lockdown protocol** directly. Reaching beneath the modern abstraction to the still-present lockdown services restores a whole device class, and the follow-up fix (the `devicectl` gate silently filtering ≤16 devices) shows the same theme: the capability was there, the modern gatekeeper just assumed it wasn't.

### Pull Beats Push for Streaming I/O ([csp](https://github.com/marcelocantos/csp))
csp's networking originally exposed a push-based `net::connection.input` — bytes arrive and the connection shoves them at you — which forces awkward buffering when a consumer (a TLS record reassembler, an HTTP body reader) wants to pull at its own pace. 🎯T17 inverts this to a **pull-based `io::source`** threaded uniformly through `tls::stream`, `http::fetch`, and `http::serve`. The consumer asks for the next chunk, the source supplies it, and back-pressure falls out for free — even the server's `handle_connection` now reads through an `fd_source`, dup-ing and dropping the fd before the WebSocket hijack so the upgrade handler still sees a clean original.

### Allocating Target IDs From Git History ([bullseye](https://github.com/marcelocantos/bullseye))
When several worktrees and agents file convergence targets in parallel, a naive "next integer" allocator collides — two branches both mint 🎯T29. bullseye's 🎯T28 derives the **next ID from git history** rather than from the working file, so the allocator reads the union of what every branch has ever assigned and never reissues a number, even across concurrent worktrees. The source of truth stays `bullseye.yaml`, but the *namespace* is reconstructed from history so distributed authorship can't clash.

### A Buffer-Pool That Bounds a Driver-Pressure Failure ([ge](https://github.com/squz/ge))
Sprite-heavy frames can push a `SpriteBatch` past its buffer capacity, and the naive response — allocate a fresh transient buffer whenever you overflow — leaks pressure straight into the Metal driver, which is a real on-device failure mode rather than a theoretical one. 🎯T113/T114 answer with an **overflow buffer-pool paired with a per-frame autorelease-pool drain**: overflow buffers are recycled rather than reallocated, and the autorelease drain caps how much transient allocation any single frame can accumulate. Transient GPU memory becomes *bounded* instead of proportional to the worst frame.

### Porting a Whole-Diagram Compression Engine Faithfully ([rustuml](https://github.com/marcelocantos/rustuml))
PlantUML compresses activity diagrams by counting how much each row is occupied along an axis (ON_X/ON_Y) and sliding tiles into the slack — an undocumented pass whose correctness lives in exactly *what* counts as occupancy. rustuml's port reproduces `klimt/compress`'s whole-diagram compression so that **connector polygons and paths are counted as ON_X occupancy precisely as PlantUML's `SlotFinder` would**, then wires the pass into the activity renderer. The payoff is that compressed diagrams match the Java reference golden-by-golden — the compression isn't approximated, it's replicated, which is what makes the downstream swimlane engine's geometry trustworthy.

### Two Liveness Signals for Ingest Freshness ([mnemo](https://github.com/marcelocantos/mnemo))
A transcript indexer that silently falls behind is worse than one that's obviously down — the data looks live but isn't. 🎯T75 makes `mnemo_status` **surface transcript-ingest freshness and per-source lag** as first-class diagnostics, so a stale source is visible rather than inferred, and 🎯T72's token-volume compaction convergence (addenda-as-tail with a precise recursion guard) keeps the backlog from thrashing. Together they make the ingest pipeline observable and self-limiting instead of a black box that occasionally wedges.

---

## Effort Estimate: Traditional vs. AI-Assisted

A single week spanning PlantUML compression-engine reverse-engineering (rustuml), platform-deep iOS automation (spyder's lockdown path), GPU buffer-pool robustness (ge), MCP-tooling reliability (mnemo, bullseye), a streaming-I/O model inversion (csp), and a mobile-game iOS-readiness landing (multimaze2).

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| rustuml compression engine + parity | 4-7 | Byte-exact reverse-engineering of PlantUML's undocumented `klimt/compress` whole-diagram ON_X compression (SlotFinder occupancy accounting) against a Java reference, validated golden-by-golden across activity and Teoz sequence geometry. |
| multimaze2 iOS v1 readiness | 2-4 | An App-Store-facing IAP surface plus an iOS jetsam memory-pressure fix and geometry/physics telemetry — on-device, review-sensitive correctness where a memory kill has no crash log. |
| ge v0.57.0 | 2-4 | A SpriteBatch overflow buffer-pool with per-frame autorelease drain (Metal driver-pressure depth), an engine metrics callback, the app-channel telemetry pipe, and an IDE-free iOS build lane. |
| spyder iOS ≤16 lockdown + app-channel | 2-4 | Driving deploy/launch/screenshot over the lockdown protocol beneath the modern tunnel, plus app-channel state slices with server-side jq filtering — iOS platform-protocol depth. |
| mnemo compaction convergence + diagnostics | 1-3 | Token-volume compaction convergence with a precise recursion guard, and ingest-freshness/per-source lag diagnostics — observability and convergence correctness. |
| csp pull-based streaming I/O | 2-3 | Inverting connection I/O from push to a pull-based `io::source` across TLS and HTTP body paths with correct back-pressure and a clean WebSocket-hijack handoff — silent-wrongness risk on the streaming/TLS surface. |
| bullseye git-history ID allocator | 1-2 | A concurrency-safe target-ID allocator that reconstructs the ID namespace from git history so parallel worktrees never collide. |
| vellum rich-text importer | 1 | A multi-format rich-text→Markdown importer (RTF/DOCX/HTML/ODT/EPUB). |
| maintenance tail (sqldeep/sqlift/sqlpipe/skills/claudia/yourworld2) | 1-2 | `mk`→`cv` migrations, `bullseye.yaml`/stale-doc cleanup, and a Makefile refactor. |

### The Diversity Tax

This week alone spans Rust (rustuml's compression engine, bullseye), C++ and GLSL (ge, multimaze2, csp), Objective-C++ and Metal (ge's SpriteBatch pooling), Swift and StoreKit (multimaze2's IAP surface), Go (spyder, mnemo, vellum), the iOS lockdown protocol and jetsam lifecycle, TLS/HTTP streaming, and PlantUML layout reverse-engineering. No single engineer holds PlantUML-compression reverse-engineering, iOS lockdown-protocol automation, Metal buffer-pool robustness, pull-based streaming-I/O design, and concurrency-safe tooling at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| rustuml | 2-4 | Steering the compression-engine port, judging golden diffs, deciding replicate-vs-approximate on undocumented layout behaviour. |
| ge / multimaze2 | 3-5 | On-device + simulator validation, jetsam/memory-pressure checks, IAP play-testing, buffer-pool spot checks. |
| spyder / csp | 2-4 | iOS ≤16 device testing, lockdown-path validation, streaming-I/O design review. |
| mnemo / bullseye / everything else | 2-3 | The five release approvals, diagnostics review, target-graph triage, and the maintenance tail. |

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~24-38 person-days (~1.2-1.9 months)** |
| Specialist team (traditional) | **~14-22 person-days (~0.7-1.1 person-months)** |
| Actual human effort this week | **~9-15 hours (~1.5-2.5 person-days)** |
| **Multiplier vs. generalist** | **~18-30x** |
| **Multiplier vs. specialist team** | **~10-16x** |

The multiplier runs highest on rustuml — faithfully porting an undocumented Java compression engine into Rust, golden-by-golden, is exactly the cross-domain-recall-and-search task where the AI dominates — and on spyder's iOS-below-the-tunnel work. It runs lowest on the release/maintenance tail (the `mk`→`cv` renames, stale-doc cleanup). The human contribution concentrated on judgement a specification can't reach: which PlantUML behaviours to replicate, the iOS-below-the-tunnel insight, the buffer-pool driver-pressure diagnosis, and on-device ship validation.
</content>
</invoke>

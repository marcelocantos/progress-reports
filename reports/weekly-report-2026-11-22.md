# Weekly Progress Report — 2026-11-16…11-22

## Executive Summary

**Twenty-nine repositories** landed **298 commits** across a Java-to-Go transpiler, editor plugins, agent-fleet tooling, defect-hunted libraries and commercial products. **[marcelocantos/gouml](https://github.com/marcelocantos/gouml)**, the mechanical PlantUML port, landed 61 commits that port a dozen more diagram families and gate every merge on a parity battery. **[marcelocantos/t3code](https://github.com/marcelocantos/t3code)** shipped fork releases v0.6.0 and v0.7.0 with plugin panels that replace built-in items and a repeatable upstream-merge process, and **[marcelocantos/t3-plugins](https://github.com/marcelocantos/t3-plugins)** gave plugins a home and an authoring guide. **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** v0.111.0 reports device power and lock health and supervises the adb server. **[marcelocantos/den](https://github.com/marcelocantos/den)** now installs Go module paths and reads formula dependencies natively against a Homebrew oracle. **[marcelocantos/vellum](https://github.com/marcelocantos/vellum)** hardened its viewer so that nothing a document names is fetched, and nine daemons across the fleet left supervisord.

**298 commits** | **<span style="color:#1a7f37">+133,946</span> net lines** | **~90-143 person-days traditional equivalent** | **~19-52x multiplier**

### Major Achievements & Innovations

- **Fork releases and a repeatable upstream merge** ([marcelocantos/t3code](https://github.com/marcelocantos/t3code) v0.6.0, v0.7.0). Plugin panels can replace built-in items and collapse, plugin cards stay on screen, links hand clicks to plugins, and web surfaces and link cards set their own size (#5, #6, #8). Plugin copy goes through i18n and decision counts translate on web and mobile. The fork now merges upstream v0.1.10 and v0.1.11 by a written process with a friction ledger, and CI checks the fork's own footprint on Linux rather than all of upstream (#9). Published releases must carry the stapled DMG's checksum.
- **Plugins get a home** ([marcelocantos/t3-plugins](https://github.com/marcelocantos/t3-plugins), [marcelocantos/t3-open-with](https://github.com/marcelocantos/t3-open-with)). The open-with plugin opens Markdown file links with the default application and now runs only as a T3-managed sidecar. It moved into a collection of T3 Code plugins with an agent-focused authoring guide that records that panel config is re-read without reopening the sidebar and that thread panels can supersede built-in items.
- **Spyder reads device health** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) v0.111.0). `device_state` and `devices` report power and lock health (🎯T194.1), lease admission, drain step-in, idle stop and adb server supervision follow (🎯T194.2–T194.5), Android network reachability gates admission (🎯T194.8), and a restarting daemon's tunnel is taken over when the outgoing one goes away (🎯T193). A heap guard protects the daemon and its tests run the go-ios browse regressions (🎯T195).
- **Vellum v0.41.0 and v0.42.0** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum)). The editor closes on one Escape even with text selected, and wide tables no longer scroll the viewer sideways in Firefox. Scoop manifests followed each release.
- **Native Go module and formula-dependency installs** ([marcelocantos/den](https://github.com/marcelocantos/den), 🎯T77, 🎯T58). `den install --provider go` accepts a full module path with an optional `@version` (`honnef.co/go/tools/cmd/staticcheck@latest`), stored under a key that cannot collide with a sibling path. The native formula parser extracts `depends_on` into its five phases and `uses_from_macos` with tags and `since:` bounds, resolves platform guards, and marks anything it cannot read as complex so the Ruby path keeps it.

### Significant Progress

- **PlantUML, transpiled and measured** ([marcelocantos/gouml](https://github.com/marcelocantos/gouml)). 61 commits ported mindmap, WBS, JSON, YAML, Gantt, salt, network, timing, Wire, regex, EBNF, Git log, chart, board, DOT, legacy activity, and math and LaTeX diagrams, plus SVG and pixel sprites, the standard library includes, Archimate icons, the SURL shim and PlantUML's own command line for SVG and preprocessed output. A `make parity` gate with name-level locks and a clock pin judges every integrator merge, and a ladder of audits (G14a–d, G15, G33) files each remaining difference as a numbered target.
- **A viewer that fetches nothing a document names** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum)). Document HTML is sanitised, a Content-Security-Policy is sent, only opened folders are served and every route is guarded (🎯T57). The PDF and clipboard converters and the Mermaid renderer's browser load nothing a document or diagram names (🎯T66, 🎯T68).
- **Defect hunts that close** ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf), [marcelocantos/ytt](https://github.com/marcelocantos/ytt), [marcelocantos/vendep](https://github.com/marcelocantos/vendep), [marcelocantos/threedee](https://github.com/marcelocantos/threedee), [marcelocantos/sysinfo-mcp](https://github.com/marcelocantos/sysinfo-mcp)). Each repository took a frontier or defect-hunt pass and landed the findings as numbered targets with tests. xbnf bounds the recursion a user grammar can trigger (🎯T112–T114), and ytt moved ingest orchestration into Go so that a stop kills the worker tree (🎯T20, 🎯T40).
- **Daemons off supervisord.** blurter, bullseye, claudia, loadmon, mcpbridge, spyder, vellum and xbnf-sandbox now run under launchd, and mnemo runs under `brew services` with a 25-second stop timeout so that shutdown can drain.

### Tough Challenges Overcome

- **Layout that matches Java's text measurement** ([marcelocantos/gouml](https://github.com/marcelocantos/gouml), 🎯T1.2.4). PlantUML positions text by Java's font metrics, which a Go port cannot call. The port installs captured fallback-advance tables (format 2 with 248 glyph rows, then format 3), refuses a whole-pixel fallback capture, sums advances in float as Java does, and generates SansSerif space advances.
- **Java runtime semantics in Go** ([marcelocantos/gouml](https://github.com/marcelocantos/gouml), 🎯T1.6, 🎯T6). UTF-16 code units, Java's ASCII regex classes, the DEFLATE reader, signed infinity on decimal overflow, JDK 21 zone display names, `LinkageError` in catch clauses and Java `Writer` dispatch through generated subclasses all had to be reproduced in the runtime shim.
- **Replication across schema change** ([marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe), 🎯T42–T60). Rows survive schema changes, resends and stale resyncs, decoders refuse malformed frames, REAL conflicts are compared by bits rather than by value, diffs stage without foreign keys, and only writable columns replicate.
- **A prune that held every write** ([marcelocantos/loadmon](https://github.com/marcelocantos/loadmon), T13, T21). The hourly prune's lookups were unindexed, so one run could hold the database against every sampler write. Both prunes now use indexes, a hung volume can no longer stop sampling (T12), and a late sample is charged to its own interval (T14–T19).
- **Ingest that fails honestly** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo), T209). Mutation testing of the recent ingest fixes found three faults the tests missed. Partial lines are indexed once, rows are kept when a source changes, and unchanged files are skipped at startup.

### Contributors

- Marcelo Cantos (AI co-authors — Claude, Grok, Cursor, Codex — on trailers throughout).

---

## Editor Plugins & Drawing Surfaces

### [marcelocantos/t3code](https://github.com/marcelocantos/t3code) — Fork Releases (15 commits, v0.6.0–v0.7.0)

- **Plugins**: panels replace built-in items and collapse, plugin cards stay on screen (#6); links hand clicks to plugins and builds sign with a Developer ID (#5); web surfaces and link cards set their own size (#8); UI copy goes through i18n and decision counts translate on web and mobile.
- **Merge process**: a repeatable upstream-merge process with a friction ledger, a reviewer's starting commands, and an agent-context label that starts its own run and is applied to upstream-only increases on merge PRs. Upstream v0.1.10 and v0.1.11 merged through it (#7, #10).
- **CI and releases**: upstream-merge PRs check the fork's footprint, not all of upstream (#9), on Linux where upstream's tests are written to run; published releases must carry the stapled DMG's checksum; the fork reports 0.7.0 (#11). About 7 new tests.

### [marcelocantos/t3-plugins](https://github.com/marcelocantos/t3-plugins) and [marcelocantos/t3-open-with](https://github.com/marcelocantos/t3-open-with) — Plugin Collection (13 commits)

- **Open with**: Markdown file links open with the default application; `--sidecar` runs the plugin as a T3-managed sidecar and a breaking change makes that the only mode. The plugin moved into the collection repository.
- **Authoring**: an agent-focused plugin authoring guide, with the per-build config path corrected, config re-read without reopening the sidebar, and thread panels that supersede built-in items. About 8 new tests.

### [canticode/orthograph](https://github.com/canticode/orthograph) — Agent Dispatcher Plan (4 commits)

- **Dispatcher**: a tracked plan replaces the T3 Code dependency with an agent dispatcher (🎯T68), with a TypeScript Agent SDK sidecar chosen (🎯T68.1).
- **Surface**: T3's thread panel is sized to a gridless picture of the drawing (🎯T67.1), and the daemon and tunnel are described as LaunchAgents.

---

## Agent & Fleet Infrastructure

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Device Health (15 commits, v0.111.0)

- **Released**: device power and lock health, lease admission, drain step-in, idle stop and adb server supervision (🎯T194.1–T194.5, T194.8), tunnel takeover (🎯T193), a heap guard (🎯T195), and restarts that wait for the Pueue lab group.
- **Since the release**: an Android app installs as a unit, APK plus OBB files, tested through the MCP surface (🎯T197), every daemon verb runs from the CLI from the schema MCP uses (🎯T198), and Unity's adb-kill EditorPrefs are recorded and held (🎯T194.6). Wireless-debugging devices by alias were filed as 🎯T196. About 52 new tests.

### [marcelocantos/loadmon](https://github.com/marcelocantos/loadmon) — Audit Hardening (11 commits)

- **Accounting**: free-space accounting counts the measured change in swap allocation and says so plainly when it is unavailable (T10); a five-minute disk burst is projected beside the hour's line and the volume is walked when the disk level worsens (T11).
- **Robustness**: the fold's project lookup is bounded (T12), both prunes are indexed (T13, T21), late samples are charged to their own interval and processes survive a failed listing (T14–T19), and mutation-audit gaps closed with eleven hunt findings (T20).
- **Daemon**: runs under launchd, waiting up to 30 seconds for the old instance to exit before bootstrapping. About 53 new tests.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Ingest Hardening (4 commits)

- **Ingest**: partial lines indexed once, rows kept on source changes, unchanged files skipped at startup, and three faults found by mutation testing fixed (T209).
- **Service**: the shared daemon runs under `brew services` with a 25-second stop timeout. About 99 new tests.

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — Viewer Hardening (11 commits, v0.41.0–v0.42.0)

- **Releases**: one Escape closes the editor even with text selected (v0.41.0); wide tables no longer scroll the viewer sideways in Firefox (v0.42.0).
- **Security**: sanitised document HTML, a Content-Security-Policy, folders served only when opened, every route guarded, RTF through pandoc, one PDF writer and a viewer homepage (🎯T57, 🎯T30); converters and the Mermaid renderer fetch nothing a document names (🎯T66, 🎯T68). About 96 new tests.

### [marcelocantos/den](https://github.com/marcelocantos/den) — Native Installs (1 commit)

- **Go modules**: full module paths with an optional `@version` install under keys that end in `@`, so `a/b` and `a/b/c` cannot share a directory and two versions of one module are stored apart; uninstall and materialise walk nested linked records, and the smoke step fails when a tracked Go package is not linked (🎯T77).
- **Formula dependencies**: the native parser extracts `depends_on` into the five published phases plus `no_linkage`, and `uses_from_macos` with tags and bounds, resolving `on_linux`, `on_macos`, `on_arm`, `on_intel` and release guards for a bottle tag. Against the unmodified Homebrew API snapshot it matches exactly on 397 of 400 seeded formulae and 9 of 9 supplemental ones, and the three misses are classified complex (🎯T58). About 17 new tests.

### Smaller landings

**[marcelocantos/blurter](https://github.com/marcelocantos/blurter)**, **[marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)**, **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** (the dev-host broker and native sidecar helpers) and **[marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge)** (1 each): daemons under launchd. **[marcelocantos/skills](https://github.com/marcelocantos/skills)** (1): synced skill refresh. **[squz/ge](https://github.com/squz/ge)** (1): the iOS simulator matrix leases its simulator from spyder instead of booting it.

---

## Parsers, Data & Libraries

### [marcelocantos/gouml](https://github.com/marcelocantos/gouml) — PlantUML Parity (61 commits)

A Go port of [PlantUML](https://plantuml.com) produced by mechanically transpiling the Java source with tree-sitter, plus a runtime shim for Java semantics.

**The biggest effort of the week.**

- **Diagram families**: mindmap and WBS (G1), JSON and YAML (G2), Gantt (G3), salt (G4), network (G5), regex, EBNF, Git log, chart, board and direct DOT (G6), timing (G7), legacy activity (G16), Wire (G21), and math and LaTeX text fallback (G20).
- **Resources**: SVG and pixel sprites, stdlib includes and Archimate icons (G13, G10), 8-bit RGBA PNG sprites, the SURL shim up to the connection and the source compressor classes (G24), and PlantUML's command line for SVG and preprocessed output (G17).
- **Fidelity**: Java's `TextLayout` measurement of shaped controls and derived italics (G8), format 2 and 3 fallback advance captures with 248 glyph rows, JDK 21 zone names, float width sums, an `end note` that prints "Syntax Error?" as the original does (G32), and a Graphviz rank-list reallocation fix through the owning pointer (G9).
- **Gate**: `make parity` with name-level locks, a clock pin and rules; integrators 6 to 14 each record their gate on the target ledger, and audits G14a–d, G15, G22, G26 and G33 triage the remaining mismatches into 🎯T1.6.x and 🎯T6.x targets. About 210 new tests.

### [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) — Defect Hunts (6 commits)

- **Hunts**: frontier-2 parser and corpus defects (🎯T39–T51), the 2026-11-20 hunt findings (🎯T101–T111), and bounded recursion for user grammars (🎯T112–T114).
- **Corpus**: tree-class fixtures compare by structure and large real corpora are pinned (🎯T26, 🎯T27); a bare `go test` passes on a fresh clone. About 116 new tests.

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Replication Correctness (3 commits)

- **Replication**: rows survive schema changes, resends and stale resyncs, and decoders refuse malformed frames (🎯T42–T49).
- **Conflicts**: REAL conflicts compare by bits, diffs stage without foreign keys, and only writable columns replicate (🎯T55–T57). The T30 audit closed and `EXPLAIN` of a sqldeep query no longer aborts (T38). About 32 new tests.

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt), [marcelocantos/vendep](https://github.com/marcelocantos/vendep), [marcelocantos/sysinfo-mcp](https://github.com/marcelocantos/sysinfo-mcp) — Tooling Hunts (8 commits)

- **ytt**: ingest orchestration moves to Go and stop kills the worker tree (🎯T20, 🎯T40, 🎯T41); hunt findings fixed (🎯T42–T51); the crosshair retirement is recorded (🎯T7).
- **vendep**: vendors prefixed tags, removes a package and finds `vendor/` from any subdirectory (🎯T3–T5); the 2026-11-20 hunt findings are fixed (🎯T6–T14).
- **sysinfo-mcp**: audit findings fixed (🎯T4) and readings that are incomplete or not exactly representable are omitted (🎯T7).

### [marcelocantos/threedee](https://github.com/marcelocantos/threedee) — CAD Hardening (4 commits)

- **Toolchain**: the CAD toolchain is pinned and the export block shared (🎯T1).
- **Checks**: exact overlap, sweep and containment checks, As-Cut staging, and STL, preset and preflight guards (🎯T12–T23); fuzzy 3MF includes, printer exit codes, monitor zone and concave half-turn clearance (🎯T24–T27); deterministic scale-rail fillets (🎯T29).

### [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) and [marcelocantos/csp](https://github.com/marcelocantos/csp) — Submission and Transport (3 commits)

- **Decimal**: the design document is prepared for submission with the fork pin moved to `5032fd7754` (#36), and the kernel probe is published with the README pointing at the design document (#37).
- **csp**: QUIC listen shares its certificate and key, the TLA+ jar is pinned, a private borrow door is added and the part examples compile (🎯T64–T67).

---

## Commercial

**[minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing)** — 121 commits. **[Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms)** — 5 commits, <span style="color:#1a7f37">+2,542</span>/<span style="color:#cf222e">−35</span> after the `hms2/tools` evidence and generated-file excludes. **[canticode/dropship](https://github.com/canticode/dropship)** — 4 commits. Full narrative: [private week 2026-11-22](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-11-22.md).

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **[marcelocantos/gouml](https://github.com/marcelocantos/gouml)**: 224 commits on branches. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)**: 68. **[marcelocantos/xbnf](https://github.com/marcelocantos/xbnf)**: 67. **[marcelocantos/doit](https://github.com/marcelocantos/doit)**: 66. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)**: 63. **[linqgo/linq](https://github.com/linqgo/linq)**: 57. **[marcelocantos/den](https://github.com/marcelocantos/den)**: 52. The Go decimal fork ([golang/go](https://github.com/golang/go)): 5. Commercial in-flight work is in the private companion.

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **29** |
| Total landed commits | **298** |
| Total lines added (landed, filtered) | <span style="color:#1a7f37">+159,707</span>‡ |
| Total lines removed (landed, filtered) | <span style="color:#cf222e">−25,761</span>‡ |
| Net new lines (landed, filtered) | <span style="color:#1a7f37">+133,946</span>‡ |
| File changes | 2,183 (summed per commit; a path touched twice counts twice) |
| Bulk paths excluded from ☲ | <span style="color:#1a7f37">+128,613</span>/<span style="color:#cf222e">−5,820</span> on counted repos, dominated by gouml's lifted PlantUML tree and test diagrams and the xbnf, threedee and den fixtures |
| Releases published | **5** (spyder v0.111.0; vellum v0.41.0–v0.42.0; t3code v0.6.0–v0.7.0) |
| Languages | Go, TypeScript, Swift, Java, C, C++, Python, Delphi/Pascal, Shell, Markdown, YAML |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. **New this run:** den `tests/corpus/**` (the pinned Homebrew formula oracle).*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 121 | 414 | <span style="color:#1a7f37">+12,243</span> | <span style="color:#cf222e">−1,936</span> | <span style="color:#1a7f37">+10,307</span> |
| [marcelocantos/gouml](https://github.com/marcelocantos/gouml) | 61 | 680 | <span style="color:#1a7f37">+80,482</span> | <span style="color:#cf222e">−4,608</span> | <span style="color:#1a7f37">+75,874</span> |
| [marcelocantos/t3code](https://github.com/marcelocantos/t3code) | 15 | 147 | <span style="color:#1a7f37">+3,983</span> | <span style="color:#cf222e">−542</span> | <span style="color:#1a7f37">+3,441</span> |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 15 | 94 | <span style="color:#1a7f37">+4,721</span> | <span style="color:#cf222e">−276</span> | <span style="color:#1a7f37">+4,445</span> |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 11 | 131 | <span style="color:#1a7f37">+8,607</span> | <span style="color:#cf222e">−1,114</span> | <span style="color:#1a7f37">+7,493</span> |
| [marcelocantos/loadmon](https://github.com/marcelocantos/loadmon) | 11 | 80 | <span style="color:#1a7f37">+2,221</span> | <span style="color:#cf222e">−392</span> | <span style="color:#1a7f37">+1,829</span> |
| [marcelocantos/t3-plugins](https://github.com/marcelocantos/t3-plugins) | 9 | 31 | <span style="color:#1a7f37">+1,228</span> | <span style="color:#cf222e">−173</span> | <span style="color:#1a7f37">+1,055</span> |
| [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) | 6 | 88 | <span style="color:#1a7f37">+5,718</span> | <span style="color:#cf222e">−814</span> | <span style="color:#1a7f37">+4,904</span> |
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | 5 | 35 | <span style="color:#1a7f37">+2,542</span> | <span style="color:#cf222e">−35</span> | <span style="color:#1a7f37">+2,507</span> |
| [marcelocantos/threedee](https://github.com/marcelocantos/threedee) | 4 | 57 | <span style="color:#1a7f37">+5,346</span> | <span style="color:#cf222e">−389</span> | <span style="color:#1a7f37">+4,957</span> |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 4 | 52 | <span style="color:#1a7f37">+7,672</span> | <span style="color:#cf222e">−819</span> | <span style="color:#1a7f37">+6,853</span> |
| [canticode/dropship](https://github.com/canticode/dropship) | 4 | 19 | <span style="color:#1a7f37">+2,290</span> | <span style="color:#cf222e">−21</span> | <span style="color:#1a7f37">+2,269</span> |
| [marcelocantos/t3-open-with](https://github.com/marcelocantos/t3-open-with) | 4 | 19 | <span style="color:#1a7f37">+1,001</span> | <span style="color:#cf222e">−163</span> | <span style="color:#1a7f37">+838</span> |
| [canticode/orthograph](https://github.com/canticode/orthograph) | 4 | 10 | <span style="color:#1a7f37">+316</span> | <span style="color:#cf222e">−81</span> | <span style="color:#1a7f37">+235</span> |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 3 | 85 | <span style="color:#1a7f37">+5,896</span> | <span style="color:#cf222e">−7,693</span> | <span style="color:#cf222e">−1,797</span> |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 3 | 45 | <span style="color:#1a7f37">+4,049</span> | <span style="color:#cf222e">−1,689</span> | <span style="color:#1a7f37">+2,360</span> |
| [marcelocantos/vendep](https://github.com/marcelocantos/vendep) | 3 | 40 | <span style="color:#1a7f37">+3,337</span> | <span style="color:#cf222e">−272</span> | <span style="color:#1a7f37">+3,065</span> |
| [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) | 2 | 23 | <span style="color:#1a7f37">+2,059</span> | <span style="color:#cf222e">−1,035</span> | <span style="color:#1a7f37">+1,024</span> |
| [marcelocantos/sysinfo-mcp](https://github.com/marcelocantos/sysinfo-mcp) | 2 | 17 | <span style="color:#1a7f37">+2,102</span> | <span style="color:#cf222e">−627</span> | <span style="color:#1a7f37">+1,475</span> |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 2 | 9 | <span style="color:#1a7f37">+1,169</span> | <span style="color:#cf222e">−11</span> | <span style="color:#1a7f37">+1,158</span> |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 1 | 22 | <span style="color:#1a7f37">+447</span> | <span style="color:#cf222e">−241</span> | <span style="color:#1a7f37">+206</span> |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 1 | 21 | <span style="color:#1a7f37">+555</span> | <span style="color:#cf222e">−72</span> | <span style="color:#1a7f37">+483</span> |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 1 | 18 | <span style="color:#1a7f37">+1,179</span> | <span style="color:#cf222e">−101</span> | <span style="color:#1a7f37">+1,078</span> |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 1 | 14 | <span style="color:#1a7f37">+1</span> | <span style="color:#cf222e">−2,302</span> | <span style="color:#cf222e">−2,301</span> |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 1 | 13 | <span style="color:#1a7f37">+224</span> | <span style="color:#cf222e">−153</span> | <span style="color:#1a7f37">+71</span> |
| [marcelocantos/blurter](https://github.com/marcelocantos/blurter) | 1 | 8 | <span style="color:#1a7f37">+144</span> | <span style="color:#cf222e">−113</span> | <span style="color:#1a7f37">+31</span> |
| [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) | 1 | 8 | <span style="color:#1a7f37">+129</span> | <span style="color:#cf222e">−76</span> | <span style="color:#1a7f37">+53</span> |
| [squz/ge](https://github.com/squz/ge) | 1 | 2 | <span style="color:#1a7f37">+44</span> | <span style="color:#cf222e">−13</span> | <span style="color:#1a7f37">+31</span> |
| [marcelocantos/progress-reports-private](https://github.com/marcelocantos/progress-reports-private) | 1 | 1 | <span style="color:#1a7f37">+2</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+2</span> |

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | ~188 | Commercial; see private companion |
| [marcelocantos/gouml](https://github.com/marcelocantos/gouml) | ~210 | Diagram families, parity locks, runtime semantics |
| [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) | ~116 | Hunt regressions, recursion bounds, corpora |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~99 | Ingest mutation tests |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | ~96 | Viewer sanitising, route guards, converters |
| [marcelocantos/loadmon](https://github.com/marcelocantos/loadmon) | ~53 | Swap accounting, prunes, late samples |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~52 | Device health, leases, OBB install |
| [marcelocantos/vendep](https://github.com/marcelocantos/vendep) | ~44 | Prefixed tags, hunt findings |
| [marcelocantos/threedee](https://github.com/marcelocantos/threedee) | ~35 | Overlap, sweep and preflight checks |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | ~35 | Ingest orchestration, hunt findings |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~32 | Replication across schema change |
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | ~19 | Commercial; see private companion |
| [marcelocantos/den](https://github.com/marcelocantos/den) | ~17 | Go module paths, formula dependency oracle |
| [canticode/dropship](https://github.com/canticode/dropship) | ~8 | Commercial; see private companion |
| [marcelocantos/t3code](https://github.com/marcelocantos/t3code) | ~7 | Plugin link cards |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~7 | Broker helpers |
| [marcelocantos/sysinfo-mcp](https://github.com/marcelocantos/sysinfo-mcp) | ~5 | Audit findings |
| [marcelocantos/t3-plugins](https://github.com/marcelocantos/t3-plugins), [marcelocantos/t3-open-with](https://github.com/marcelocantos/t3-open-with) | ~8 | Sidecar mode |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~4 | Part examples |
| [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) | ~2 | Pin checks |
| [canticode/orthograph](https://github.com/canticode/orthograph) | ~1 | Thread panel |
| **Total** | **~1,038** | |

### Daily Activity

![Daily active repositories](daily-activity-2026-11-22.svg)

---

## Ideas & Innovations

### Transpile the Source, Then Measure the Port ([gouml](https://github.com/marcelocantos/gouml))

Hand-porting a large Java program invites silent drift. **gouml transpiles PlantUML mechanically and lets a parity gate with name-level locks and a clock pin decide every merge**: a family of diagrams either matches the reference render or its difference is filed as a numbered target. Progress is then a ledger of measured gaps rather than a feeling.

### Capture the Host's Font Advances ([gouml](https://github.com/marcelocantos/gouml))

PlantUML places text with Java's font metrics, and a Go port has no JVM to ask. The fix was to **capture the reference host's fallback advances as tables and refuse any capture that rounds to whole pixels**, summing them in float exactly as Java does. Layout then agrees with the original without reimplementing its font stack.

### Parse What You Can, Mark the Rest Complex ([den](https://github.com/marcelocantos/den))

Homebrew formulae are Ruby, and a faithful parser would be a Ruby interpreter. Den's native parser **extracts only the declarations it fully understands and marks any condition, dynamic call or inheritance as complex, which keeps the old path**. An unmodified API snapshot is the oracle, and a baseline locks the result in both directions, so coverage can grow without ever silently misreading a formula.

### A Fork That Merges Itself ([t3code](https://github.com/marcelocantos/t3code))

A fork that tracks a fast upstream spends its life merging. Rather than treat each merge as an event, **the fork keeps a written process, a friction ledger and a CI check of the fork's own footprint**, so a merge reviewer starts from commands and a known shape and the cost of each merge is recorded for the next.

### A Viewer That Fetches Nothing a Document Names ([vellum](https://github.com/marcelocantos/vellum))

A document viewer that renders HTML, PDF and diagrams will follow whatever links the document names. Vellum **treats every document as hostile: sanitised HTML, a Content-Security-Policy, only opened folders served, and converters and the Mermaid browser that load nothing a document names**. The viewer's trust boundary becomes the file, not the network.

### Compare Floating Point by Bits ([sqlpipe](https://github.com/marcelocantos/sqlpipe))

Two replicas disagree about a REAL column when equal-looking values differ in the last place, or when NaN is involved. **Conflicts are compared by their bits**, so a conflict is real exactly when the stored values are, and diffs stage without foreign keys so ordering cannot hide one.

---

## Effort Estimate: Traditional vs. AI-Assisted

The week mixed a mechanical-transpilation campaign, a release train for a commercial product and an editor-plugin fork with fleet tooling, defect-hunted libraries and a daemon migration. The difficulty sat in reproducing another language's runtime exactly and in hardening many small tools at once.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| Commercial work (Stock Cars, HMS, dropship) | 20-30 | Detail in the private companion. |
| gouml | 22-36 | Tree-sitter-driven Java-to-Go transpilation, Java runtime semantics, font-metric fidelity and a parity gate across dozens of diagram families. |
| t3code, t3-plugins, t3-open-with | 8-12 | A plugin host across web, desktop and mobile, signed releases and a repeatable upstream merge. |
| spyder, loadmon | 12-19 | Android device power, lock and adb supervision; SQLite prune contention and swap and disk accounting in a Swift daemon. |
| vellum, mnemo | 10-16 | A hostile-document viewer with CSP and converters, and mutation-tested ingest. |
| xbnf, ytt, vendep, sqlpipe, sysinfo-mcp | 12-20 | Parser recursion bounds, ingest orchestration, vendoring semantics and replication across schema change. |
| den, orthograph | 6-10 | A native formula-dependency parser checked against a Homebrew oracle, and an agent-dispatcher plan. |
| threedee, csp, go-decimal-proposal, ge, others | 5-8 | CAD overlap and sweep checks, QUIC certificate sharing, a decimal design submission. |

### The Diversity Tax

Java and Go runtime semantics, tree-sitter transpilation, font metrics and SVG layout, Graphviz internals, Android device and adb internals, SQLite concurrency, Swift daemon engineering, macOS launchd and code signing, plugin hosts for web and mobile, parser theory, replication protocols, CAD geometry, and the commercial products' own specialisms. No single specialist holds that range.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| Commercial work | 6-10 | Detail in the private companion. |
| gouml | 3-5 | Setting the parity gate and judging which differences matter. |
| t3code, t3-plugins | 3-5 | Plugin behaviour review and release sign-off. |
| spyder, loadmon, vellum, mnemo | 3-6 | Device checks, rule choices and release sign-off. |
| xbnf, ytt, vendep, sqlpipe, sysinfo-mcp | 3-5 | Choosing which hunt findings to fix first. |
| den, orthograph and others | 4-7 | Native-install design calls, dispatcher choice, and fitting and printing parts. |

### What If It Were One Person?

The specialist band sums to roughly 62-98 person-days. A generalist would also need ramp-up on PlantUML's Java internals, Android device tooling and the T3 Code plugin host. Landed activity ran on six of the seven days.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~90-143 person-days (~4.1-6.6 months)** |
| Specialist team (traditional) | **~62-98 person-days (~2.9-4.5 person-months)** |
| Actual human effort this week | **~22-38 hours (~2.75-4.75 person-days)** |
| **Multiplier vs. generalist** | **~19-52x** |
| **Multiplier vs. specialist team** | **~13-36x** |

The multiplier is highest on the transpilation and hardening work, where an oracle and a gate absorb most of the cost. It is lowest on the commercial products, where device checks and store processes set the pace. The human contribution concentrated on deciding what counts as proof: a port must match its reference by measurement, a viewer must trust nothing it opens, and a replica must agree to the last bit.

# Progress Reports

Weekly progress reports for Marcelo Cantos's AI-assisted development work.

Commercial project detail (HMS, minicades, and non-`ge` Squz titles) lives in the private sibling [progress-reports-private](https://github.com/marcelocantos/progress-reports-private). This public series keeps names, rolled-up metrics, and stubs; open-source `squz/ge` remains fully documented here.

## At a Glance

*32 weeks · 19 January – 30 August 2026*

- **~7,662 commits** landed to default branches across **40+ repositories** in **20+ languages**
- **~502–833 hours** of total human attention — the direction, review, and on-device testing a specification can't reach
- **~9.9–16.8 years** of a single talented generalist's full-time work, produced at a **20–95× multiplier**
- **~+3.57M net lines** of tracked change (excl. `vendor/` / `node_modules/` and the fleet `data/line-excludes.yaml` globs) — an activity signal, not hand-authored source

## The Journey So Far

Thirty-two weeks of AI-assisted development, from 19 January to 30 August 2026. Around **7,660 commits** have landed to default branches across more than forty repositories and twenty-odd languages — a body of work a single talented generalist would need **ten to seventeen years** to match, produced on one to three hours of human attention a day.

The numbers describe a *mode of production*, not a portfolio.

**Breadth held at once rather than in turn.** Concurrent systems, GPU and mobile bring-up, applied cryptography, sandbox policy, compiler reverse-engineering, formal verification, stylus input, language-runtime representation, and full-stack fleet tooling sit in a single working set. Crossing between them stopped being expensive months ago, which is why a week can found a product or spend two hundred commits on the fleet's own survival without queuing behind specialists.

**A system that has to survive operating itself.** The latest phase is not writing more agents but keeping a running fleet from destroying the machine it lives on, then making its behaviour interpretable. Failures are workshop failures: leftover windows rematerialising until a 128 GB host sat at load 267; a ceiling that could not see one provider's cached reads; a connect-replay that pinned to a slot instead of a person; a status-bar wedge diagnosed in the transcript, so the diagnosis became the wedge. The fixes are contractual: upgrade adopts leftovers, ordinary start does not reap, Exclusive MCP subtracts rather than inherits, CloseGoal is a host fact, an exhausted model falls down its ladder, and the tmux anchor pane is what holds the server open.

**Economics and correctness as the same surface.** Spend is decomposed along the axes the levers act on; a tool surface is weighed in bytes, not counted in entries; unknown remaining is not 100% headroom. The same instinct is a field a provider cannot honour being refused, a backup retain-count that was 4.3× the data it protected, and a corpus forbidden from being produced by the tool it tests. An oracle is a loop, not an artefact.

**A standing suspicion of silent success.** The consistent theme is making failure visible. A pipeline that exits zero while ingesting nothing, a watcher that reloads because it just reloaded, a summariser that took its input as instructions, a supervisor whose plist still looks healthy after launchd has dropped the job — each surfaced only when something asked "is this still producing anything?" rather than "did this step fail?".

**Things that ship.** Libraries cut releases with CI and Homebrew taps published from a codesigned binary rather than a CI secret; games reached both stores; an engine extracted from one title now runs the others on four platforms. Finish lines are store submissions, version tags, and an install that works for a stranger.

**An inverted human role.** Volume comes from the system. What remains is architecture, on-device judgement no agent can supply, and deciding what a tool must *refuse* to do: that a secret is never a tool argument, that an unknown measurement must not trigger an action, that ordinary start must not reap, that the destructive branch is never the default under ambiguity.

The multiplier, typically 20× to 95×, has held across the series, highest on platform-deep and silent-wrongness work and lowest on mechanical consolidation. Headline figures count landed commits only; line counts exclude vendored trees, generated mirrors, lockfiles, ledger churn and amalgamations, and remain an activity signal rather than hand-authored output.

For the specifics — which projects, which releases, which week — see **Greatest Hits**, the [per-repository pages](docs/repos/README.md), and the weekly reports below.

![Daily active repositories — full timeline](reports/timeline.svg)

## Greatest Hits

The [top 50 achievements](docs/achievements.md) across all projects, ranked by meatiness.

## By Project

One page per repository, summarising its whole arc across the series: [docs/repos](docs/repos/README.md). Commercial (HMS / minicades / non-`ge` Squz) journeys: [progress-reports-private](https://github.com/marcelocantos/progress-reports-private).

## Reports

<details>
<summary><a href="reports/weekly-report-2026-08-30.md"><b>2026-08-24…30</b></a> React daily cockpit, model ladder fallback, mnemo compressed and weighed, interned arr.ai shapes, tapper ships the tap</summary>

<b>jevons</b> made the React cockpit the daily UI, persisted coalesced transcripts in SQLite, and taught an exhausted model to fall down its ladder rather than be re-briefed; the tmux anchor pane is what holds the fleet server open. <b>mnemo</b> compressed hot fields, cut backup retain from seven to one, and weighed the tool surface in bytes. <b>arr.ai</b> rebuilt tuples as interned shapes; <b>orthograph</b> became a Canticode product published through a new <b>tapper</b> rather than a CI secret; <b>finance</b> is a statement-transcript oracle with no data in the repo. 183 commits across 18 repos, ~3.0-4.8 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-08-23.md"><b>2026-08-17…23</b></a> host-owned MCP and a host-closed Session Goal, Exclusive MCP, bullseye stopped auto-commit, ytt split clocks, USB speed ratchet</summary>

<b>jevons</b> made the fleet interpretable — host-owned MCP, a Session Goal the host can close, Codex Session over app-server — and <b>claudia</b> cut five releases that are that substrate: an HTTP MCP proxy that never stores tokens, Exclusive mode, and host CloseGoal. <b>bullseye</b> stopped auto-committing the ledger; <b>ytt</b> split paced download from unthrottled analysis; <b>spyder</b> reports USB link speed as a ratchet. A Saturday entropy-audit documentation pass then touched sixty-eight other repositories. 411 commits across 78 repos (10 product), ~2.8-4.3 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-08-16.md"><b>2026-08-10…16</b></a> ghost Claude fleet recovered, mutual daemon/watchdog supervision, Claude cache-read ceiling, Codex provider, bullseye hang and SHA stability</summary>

<b>jevons</b> spent the week surviving a host-down incident: leftover Claude tmux windows rematerialised on every bounce until a 128 GB machine sat at load 267. Upgrade now adopts leftovers; the daemon and a launchd watchdog supervise each other. Last week's context ceiling started working once Claude's cached reads counted as context, then needed hysteresis so it would not become a treadmill. <b>claudia</b> v0.21.0 added Codex and a capability matrix that refuses fields a path cannot honour. <b>bullseye</b> v0.45.0 ended a UTF-8 hang. 263 commits across 8 repos, ~2.4-3.8 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-08-09.md"><b>2026-08-03…09</b></a> orthograph shared sketch surface built and shipped, jevons fleet spend oracle and context ceiling, worker write and commit guards, slacker browser OAuth, mnemo 70→18 tools</summary>

<b>orthograph</b> went from an empty repository to a <code>brew install</code>-able product in six days: a Pencil-first iPad sketch surface whose vector document lives on the Mac, readable and writable by agents over MCP. <b>jevons</b> landed 80 commits largely by supervising itself — a spend oracle decomposing cost as turns × calls × context, a hard context ceiling, wake coalescing after over half its costliest agent's prompts proved to be machine noise, a compare-and-swap write guard, and a <code>GIT_INDEX_FILE</code> commit gate. <b>slacker</b> replaced paste-a-token with browser OAuth over a TLS loopback callback; <b>mnemo</b> cut 70 MCP tools to 18; <b>mcpbridge</b> ended a self-feeding reload loop. 297 commits across 19 repos, ~2.3-3.8 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-08-02.md"><b>2026-07-27…08-02</b></a> summariser containment after a 4.3-billion-token runaway, ge gesture-hint service and tile pyramid, csp ARM64 stack analyser, mnemo cost engine, 40 releases</summary>

<b>mnemo</b> had its largest week of the series — fourteen releases — carrying streaming topic segmentation, a token-cost engine derived from published pricing, and the fix for a real incident: a summariser obeyed an instruction inside a transcript and spawned roughly 33,000 subagents. Closing it needed <b>claudia</b> v0.20.0 first, whose Task mode had never applied the tool restrictions the package documented. <b>ge</b> cut eight tags including a gesture-hint service where one timeline both draws an SDF hand and injects real touch events, and a tile-pyramid format whose coarse packs are byte prefixes of the fine ones. <b>csp</b> shipped an ARM64 stack analyser; <b>ytt</b> was ported to Go and lost a dependency doing it. 115 commits, 19 repos, 40 releases, ~1.1-1.8 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-07-26.md"><b>2026-07-20…26</b></a> writ declared-intent execution sandbox, blurter spool-first daemon released same-day, ge compressed textures + metrics ring, csp ~3× scheduler fix + Windows gate, ytt 16-day silent outage closed</summary>

<b>writ</b> went from empty repo to working MVP in four days: a declared intent manifest compiled into a macOS seatbelt profile, a manifest-keyed egress proxy, and a drift audit whose declared-versus-actual diff doubles as a prompt-injection detector — then hardened against its own red team. <b>blurter</b> was created and released the same day, inverting notification durability so delivery is recorded only once a sink confirms. <b>ge</b> cut four tags (engine-owned ASTC/ETC2 texture cook-and-load, a zero-I/O frame-metrics ring, SDL3 3.4.12), exposed through <b>spyder</b> as semantic hit-target and metrics tools. <b>csp</b> shipped a ~3× scheduler-thrash fix and a two-tier Windows gate; <b>ytt</b> ended a sixteen-day silent outage; <b>jevons</b> cut chat load from 15–20 s to ~1.5 s. 63 commits across 16 repos, ~0.8-1.3 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-07-19.md"><b>2026-07-13…19</b></a> ge Emscripten/WebGL2 browser platform, spyder wasm command-stream player, jevons MCP attach + fail-closed durability, csp ~146 ns channel hot-path, mnemo vault/plugins, sawmill 18-language matrix</summary>

<b>ge</b> shipped a fourth direct-mode platform (Emscripten/WebGL2, Asyncify-safe run loop) and a location-transparent command stream; <b>spyder</b> compiled the same player tree to a browser glass at ~55–60 fps SP2S plus health monitoring and host Starlark scripts. <b>jevons</b>/<b>claudia</b> closed silent toolless-overseer boots (session-scoped MCP attach, fail-closed resume, embedded web UI). <b>csp</b> flattened channel rendezvous to ~146 ns after measuring 16× negative scaling; <b>mnemo</b> vault wing + plugin system; <b>sawmill</b> 18-language matrix; <b>yourworld</b>/<b>yourworld2</b>/<b>esfera2</b> oracle density, gameplay recovery, and tilt parallax. 96 commits across 18 repos, ~0.7-1.2 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-07-12.md"><b>2026-07-06…12</b></a> MultiMaze 2 v1 store launch, pigeon crypto remediation, jevons v0.5.0 cockpit + live cost governance, ged→spyder control-plane migration, Grok provider rollout, bullseye four-tool ledger API</summary>

<b>multimaze2</b> reached v1 on both stores (Play Billing AAB + App Store submission). <b>pigeon</b> shipped six releases fixing a confirmed AES-GCM nonce-reuse race and re-architecting per-flow AEAD channels with a ZRTP-style SAS commit-reveal round. <b>jevons</b> v0.5.0 became a real fleet cockpit — a durable Butler/CEO thread model and a token-spend clamp-down born from a live money-loss incident. "Plateau P" retired the entire <b>ged</b> daemon and console and made <b>spyder</b> the sole control plane, streaming H.264 dev video end-to-end; <b>claudia</b> gained a Grok Task+Session provider (v0.15→v0.17) consumed by jevons and <b>mnemo</b>; <b>bullseye</b> collapsed to a four-tool ledger API; <b>esfera2</b> and <b>yourworld2</b> converged onto ge's sokol_gfx backend. 120 commits across ~20 substantive repos, ~0.8-1.4 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-07-05.md"><b>2026-06-29…07-05</b></a> fleet-wide Fable-5 security audit + same-week remediation, ge bgfx eradication + TiltBuggy differential oracle, rustuml parity honesty ratchet, mnemo menu-bar navigator, sawmill discovery/retrieval tier</summary>

An AI-driven security and correctness audit swept eight repos, surfacing genuine criticals (a pigeon nonce-reuse race, a mnemo read-guard bypass, a sawmill root-escape) and shipping verify-first fixes the same week. <b>ge</b> finished eradicating bgfx (sokol_gfx the sole renderer, a −42.7k purge) and built a differential oracle harness making the revived 2013 <b>TiltBuggy</b> the executable ground truth for its box2d port. <b>rustuml</b> added a no-oracle parity ratchet that fails on unrecorded improvement; <b>mnemo</b> shipped a macOS menu-bar navigator and Codex ingest; <b>sawmill</b> landed an FTS5+PageRank+vector discovery tier; <b>claudia</b> shipped session rewind; <b>multimaze2</b> cleared its iOS release blockers. 169 commits across 19 repos, ~0.7-1.2 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-06-28.md"><b>2026-06-22…28</b></a> den v1.0.0 release candidate, ge headless render-to-PNG + camera-basis GlobeController, rustuml real-world swimlane parity lock-down, mnemo daemon idle-CPU elimination, multimaze2 IAP restore + paywall</summary>

<b>den</b> reached its v1.0.0 release candidate — trust model, SAT-solver dependency resolution, source-build plus taps, and perf benchmarks clearing the v1 blockers. <b>ge</b> turned its GPU pipeline into a deterministic offline renderer (<code>ge::renderToPng</code> + <code>tiltbuggy render</code>, golden-image fixtures) and made <code>GlobeController</code> camera-orientation-agnostic; <b>rustuml</b> locked real-world swimlane parity (restaurant, shopping-cart, onboarding, approval, expense) atop last week's engine; <b>mnemo</b> eliminated daemon idle-CPU burn; <b>multimaze2</b> landed IAP restore, legacy entitlement, and the paid-pack paywall; <b>bullseye</b> v0.36 fixed the invariants-hook timeout hanging esfera2. 74 commits across 11 substantive repos, ~0.9-1.4 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-06-21.md"><b>2026-06-15…21</b></a> rustuml second-generation swimlane layout engine, mnemo reliability suite (compaction healing, three-tier tests), bullseye five releases + GitHub issue mirror, multimaze2 level-survivability solver, stock-car Unity testing harness</summary>

The biggest week of the series. <b>rustuml</b> built its second-generation swimlane activity-layout engine — connector lane-tagging, per-lane MinMax columns, a cross-lane router, and N-branch fork-lane routing from simple through six-branch. <b>mnemo</b> healed the compaction-failure ratio and added a three-tier test architecture and a self-diagnostics suite; <b>bullseye</b> cut five releases including a GitHub issue mirror and CLI/MCP parity; <b>multimaze2</b> built a 2,527-line headless level-survivability solver; <b>den</b> stood up its RC harness and publishing pipeline; <b>stock-car-racing</b> gained a Unity Test Framework harness with asmdef isolation and a Unity 6.4 CVE hotfix; <b>csp</b> completed the pull-based streaming cutover. 217 commits across 12 substantive repos, ~1.6-2.6 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-06-14.md"><b>2026-06-08…14</b></a> spyder iOS ≤16 automation over lockdown, csp pull-based io::source streaming, bullseye git-history ID allocator, ge SpriteBatch buffer-pool + app-channel telemetry, rustuml whole-diagram compression engine, vellum rich-text import</summary>

<b>spyder</b> shipped deploy, launch, and screenshot for iOS ≤16 devices over the lockdown protocol — no Developer-mode tunnel required — plus agent-consumable app-channel state slices with server-side jq filtering. <b>csp</b> inverted its networking to a pull-based <code>io::source</code> threaded through TLS and HTTP bodies; <b>bullseye</b> v0.30 derived target IDs from git history so parallel worktrees never collide; <b>ge</b> added a SpriteBatch overflow buffer-pool and blessed its app-channel telemetry pipe; <b>rustuml</b> ported PlantUML's whole-diagram ON_X compression engine and locked a long tail of golden parity; <b>vellum</b> v0.5.0 imports rich-text formats to Markdown. 75 commits across 8 substantive repos, ~1.2-1.9 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-06-07.md"><b>2026-06-01…07</b></a> rustuml PlantUML activity-diagram layout parity, ge eleven-release diagnostics + RPC-channel sprint, multimaze2 per-ball soft-shadow lighting and IAP launch surface, spyder bidirectional RPC channel, mnemo stuck-watcher fix</summary>

An authoring-heavy week led by <b>rustuml</b>, which committed fresh PlantUML activity-diagram layout parity straight to master — whole-diagram compression, branch/loop/switch tile geometry, sequence layout, swimlane lane-widths, and an ArchiMate rewrite, with 173 new tests. <b>ge</b> ran an eleven-release sprint adding a diagnostic render overlay, the app side of spyder's MessagePack-RPC channel, presentation-tilt, a simulator command-buffer-leak fix, and Android Vulkan/GLES backend selection. <b>multimaze2</b>, one release from the App Store, landed per-ball soft-shadow lighting and its IAP launch surface; <b>spyder</b> shipped the bidirectional RPC channel and per-session log listener; <b>mnemo</b> killed a false stuck-watcher warning; <b>pigeon</b> landed a real-QUIC JNI transport. 432 commits across 11 repos, ~1.1-1.9 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-05-31.md"><b>2026-05-25…31</b></a> rustuml v0.7.0 strict-XML-parity merge (last week's in-flight work lands), ge bgfx→sokol_gfx renderer migration + prebuilt-vendor-lib cutover, cv v0.9.0 discovered-dependencies build model, mnemo compactor data-plane hardening</summary>

A consolidation-and-hardening week; the methodology now counts landed commits only, with in-flight work reported separately. Much of the raw total is <b>rustuml</b>'s v0.7.0 merge of the strict-XML-parity work previewed last week — the shipping event, not fresh authorship. <b>ge</b> migrated its renderer from bgfx to sokol_gfx, cut the iOS/Android build over to prebuilt vendor static libraries, moved the iOS build onto the xcodeproj-gem builder, and added simulator Metal-shader support. <b>cv</b> (renamed from mk) shipped v0.9.0 with a discovered-dependencies build model. <b>mnemo</b> hardened the compaction data plane, including a covering index taking a candidate query from ~30 min to 142 ms. Smaller landings across spyder, pigeon, multimaze2, csp, and kart-stars. 332 commits across 10 repos, ~0.7-1.3 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-05-24.md"><b>2026-05-18…24</b></a> mnemo eight releases (backup primitive + additive-only schema + daemon-boot workers), spyder self-healing tunnel + log-capture, ge sixteen-blocker mega-PR + IAP preps, pigeon seven-target cross-language fan-out, den PackageProvider abstraction</summary>

Twenty-one repositories landed work across library infrastructure, game-engine ship plumbing, and mobile release engineering. <b>mnemo</b> shipped eight releases building a backup primitive, an additive-only schema, eager daemon-boot workers, and a sweep of compactor/store hardening. <b>spyder</b> culminated in a tunnel daemon that self-heals on device-lifeline death, plus managed log-capture and usbmuxd wedge auto-recovery. <b>ge</b> landed a mega-PR closing sixteen multimaze2-blocker targets at once, plus IAP release preps with a StoreKit 2 Swift bridge. <b>den</b> shipped a PackageProvider abstraction making Homebrew one provider among many. <b>pigeon</b> ran a seven-target fan-out exercising its wire format across five language runtimes. Releases also landed for csp, sqlift, sqldeep, bullseye, and claudia. 124 commits across 21 repos, ~3.5-5 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-05-17.md"><b>2026-05-11…17</b></a> bullseye second schema simplification in two weeks (kind enum removed), ge::iap cross-platform module (StoreKit + Play Billing), HMS2 patient-view V1 fidelity fan-out, pigeon five-language wire-format codegen, csp per-protocol dist split</summary>

<b>bullseye</b> shipped its second schema simplification in two weeks, retiring the kind enum, its edges, budgets, and tools in favour of fanout ordering — the conceptual shift being bullseye-the-tool as minimal substrate. <b>ge</b> added a cross-platform IAP module with StoreKit and Play Billing backends, a debug panel, and tiltbuggy as a real consumer. <b>HMS2</b> landed a patient-view V1 fidelity rewrite across one fan-out PR plus inline episode-detail. <b>pigeon</b> drove session activation through the generated state machine and shipped protogen wire-format codegen across Go/C/Swift/Kotlin/TypeScript with verified-identical byte vectors. <b>csp</b> split the dist amalgamation into six per-protocol drop-ins backed by linker dead-code elimination. Further landings across rustuml, mnemo, vellum, sawmill, sqldeep, and den. 142 commits across 18 repos, ~4.5-7.5 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-05-10.md"><b>2026-05-04…10</b></a> ge eighteen-release sprint building the canonical 2D/UI surface in five days, spyder pmd3-bridge wholesale deletion for direct go-ios binding, multimaze2 faithful-to-2010 physics, crosshair v0.1.0 public release, HMS oracle parity closes</summary>

An eighteen-release sprint for <b>ge</b> built out the canonical 2D/UI surface in five days: physical-size sizing, device-tilt parallax, a canonical Activity, an SVG rasteriser, and the asset/sprite pipeline, with a compile-time public-surface audit. <b>spyder</b> shipped the architectural inversion — pmd3-bridge and devicectl decommissioned wholesale in favour of go-ios bound directly into the daemon with a device cache. <b>HMS oracle</b> closed the cool_jessie parity loop end-to-end. <b>multimaze2</b> landed the faithful-to-2010 physics rewrite (doors that are walls at rest), raw SDL3 audio, and an auto-scrolling level picker. <b>crosshair</b> shipped v0.1.0 as a public release — a Rust convergence-executor daemon for bullseye targets. Further work across sawmill, bullseye, sqlift, mnemo, pigeon, and csp. 158 commits across 16 repos, ~4-7 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-05-03.md"><b>2026-04-27…05-03</b></a> spyder eleven releases (transport recoverable/fatal split + pool redesign), csp QUIC transport on ngtcp2, ge v0.2-v0.4 Android lifecycle + iOS orientation lock, pigeon multi-client mux relay, sawmill AST-aware three-way merge</summary>

An eleven-release run for <b>spyder</b>: a bridge-transport recoverable-vs-fatal split killing the periodic daemon-panic wedge, autoawake opt-out, and a SQLite-ledger-backed adopt-from-live pool. <b>csp</b> v0.13.0 landed a working QUIC transport on ngtcp2 + PicoTLS with integration tests and six runnable example apps. <b>ge</b> shipped v0.2-v0.4 with Android background/foreground swap-chain survival, a dual renderer, and iOS orientation lock. <b>pigeon</b> landed the multi-channel API and multi-client mux relay; <b>sawmill</b> shipped an AST-aware three-way merge engine; <b>bullseye</b> cut three releases. <b>rustuml</b> extracted PlantUML font metrics from 125,710 text elements. New repos: <b>crosshair</b> and <b>mcpsafe</b>. 253 commits across 31 repos, ~5-8 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-04-26.md"><b>2026-04-20…26</b></a> mnemo eleven releases (Windows MSI + ARM64 + mTLS federation + four MCP tools), spyder ten releases completing the pmd3-bridge migration, bullseye six releases, HMS oracle validation toolchain</summary>

An eleven-release week for <b>mnemo</b>: a Windows double-click installer, llvm-mingw ARM64, per-user Windows Service registration, mTLS federation across linked instances, an idempotent indexer, and four new MCP tools. <b>spyder</b> completed the KeepAwake-to-bundled-pmd3-bridge migration across ten releases. <b>bullseye</b> shipped the envelope-leak validation guard, the set-aside status, and the validate split. <b>HMS</b> opened a brand-new Mac-side validation harness — a C# SendInput daemon, a Delphi DFM parser handling 1,282 of 1,307 files with Apple Vision OCR, and a tunnelled pymssql baseline/snapshot path. <b>sawmill</b> shipped a SQLite-backed git AST index, semantic blame and bisect, the pattern-equivalence pillar, and an auto-fix loop. Further releases across csp, pigeon, mcpbridge, doit, ytt, vellum, and stock-car-racing. 355 commits across 20 repos, ~5-8 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-04-19.md"><b>2026-04-13…19</b></a> pageflip + spyder launched (2 new brew-installable products), mnemo v0.16-v0.21 (image/OCR/CLIP indexing + live compaction + connection identity + HTTP transport collapse + Windows), pigeon TLA+-verified cutover + ngtcp2 QUIC C + multi-client pairing, ge v0.1.0 with engine/render/bridge split, bullseye per-repo storage redesign</summary>

Greenfield-plus-depth week: <b>pageflip</b> shipped v0.1.0 as a Rust+Go meeting-capture pipeline with macOS Vision face-blur, OCR PII redaction, ScreenCaptureKit audio with compile-time egress gate via sealed types, WhisperX+pyannote diarisation, and a Go meetcat shell spawning 5 claudia-backed specialist agents (skeptic/constructive/neutral/dejargoniser/contradictions) with artefact writer. <b>spyder</b> shipped v0.1.0→v0.5.0 in 3 days as an HTTP MCP server for cross-platform mobile orchestration with iOS (pymobiledevice3+CoreDevice) and Android (adb) adapters, reservation system, screen recording, crash collection, network shaping, and run artefacts. <b>mnemo</b> climbed v0.16→v0.21 (6 releases) adding image/OCR/CLIP indexing via Anthropic vision API, a live compaction lifecycle with claudia.Task LLM summariser, a connection-identity pivot that re-keyed session chains around daemon connections, HTTP MCP transport collapse, and native Windows support. <b>pigeon</b> v0.17.0 added a TLA+-verified (159K states) drain-window cutover protocol, ngtcp2 QUIC C transport vtable, one-time-token multi-client pairing. <b>squz/ge</b> v0.1.0 with engine/render/bridge subsystem split, Android text rendering (SDL_ttf vendored), GPU YUV colour-space conversion, physical-device matrix cells passing on iOS+Android. <b>bullseye</b> v0.15→v0.17 redesigned storage from machine-wide to per-repo path-driven discovery. <b>doit</b> v0.6.0 added shell-script SHA-256 approval gate, process-group timeouts, and audit-log-driven duration anomaly detection. <b>jevons</b> v0.4.0 added mTLS CA + device provisioning + cross-repo active-work dashboard. <b>esfera2</b> ported sphere+pieces from Dawn/WebGPU to bgfx atop ge v0.1.0. 391 commits across 21 repos. ~5.5-9 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-04-12.md"><b>2026-04-06…12</b></a> bullseye v0.5-v0.14 (portfolio WSJF, cross-repo convergence), mnemo v0.4-v0.15 (11 new tools, session chains), pigeon pure C client library, claudia bootstrap to tmux agent pool, HMS 7-round de-identification hardening, sawmill git history indexing</summary>

MCP ecosystem maturation week: <b>bullseye</b> reached v0.14.0 with portfolio-level WSJF ranking, cross-repo dependency edges, and convergence gap analysis (75 commits, 10 releases). <b>mnemo</b> climbed from v0.4.0 to v0.15.0 with 11 new tools including session chains, CI indexing, and self-healing streams (81 commits). <b>pigeon</b> gained a pure C client library with amalgamated distribution and cross-language crypto vector tests (v0.16.0). <b>claudia</b> went from bootstrap to tmux-backed agent pool with warm spawning and session chains (v0.6.0). <b>hms</b> de-identification tool hardened through 7 red-team audits with exhaustive PII coverage manifest. <b>sawmill</b> added git history AST indexing, 7 new MCP tools, and global daemon (v0.9.0). 646 commits across 28 repos. ~6-9 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-04-05.md"><b>2026-03-30…04-05</b></a> sawmill Rust-to-Go rewrite + open-source (11 frontier milestones), pigeon session protocol with generated state machines (Go/Swift/Kotlin/TS) + TLA+, sqldeep XML literals through 10 releases, nostalgia TUI git browser, csp v0.6-v0.8</summary>

<b>sawmill</b> complete Rust-to-Go rewrite with daemon architecture, open-sourced with 11 frontier milestones (Phases 2-6, Frontiers A-E, K), binary hash handshake, zero-project-footprint state, v0.2.0-v0.6.0. <b>pigeon</b> (renamed from tern) unified session protocol in YAML with code generators producing typed state machines in Go/Swift/Kotlin/TypeScript, TLA+ generator rewritten to pure TLA+ with channel elimination (121 states, &lt;1s), path-switching with chaos tests, v0.9.0-v0.14.0. <b>sqldeep</b> XML/HTML literal syntax, BLOB protocol, JSONML, JSX, boolean semantics, interactive CLI, v0.9.0-v0.18.0. <b>nostalgia</b> new TUI git file history browser with DAG graph, syntax highlighting, go-git. <b>csp</b> fd_t, file I/O, 3 example apps, v0.6.0-v0.8.0. <b>yourworld2/ge</b> H.264 pivot, engine ownership. 432 commits across 15 repos. ~5-7 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-03-29.md"><b>2026-03-23…29</b></a> csp M:N-only scheduler (663/663 tests, quiescence scope, TLA+), rustuml 6 renderer rewrites for exact SVG parity, den Rust-to-C++ rewrite with 5 audit rounds, sqlpipe predicate VM + convergence loop, tern 97.5% protocol coverage + fault injection, ge NetworkBackend + H.264 streaming</summary>

<b>csp</b> M:N-only scheduler migration complete — 663/663 tests, quiescence scope primitive, fake_clock auto-advance, 6 TLA+ specs, 5 targets achieved, v0.5.0. <b>rustuml</b> 6 renderer rewrites for exact PlantUML SVG parity using Java AWT binary-fraction font metrics, oracle test framework, Graphviz integration, v0.3.0–v0.5.0. <b>den</b> complete Rust-to-C++ rewrite with independent package store, source builds via bundled Ruby, 5 adversarial audit rounds (100+ findings), v0.1.0–v0.3.0. <b>sqlpipe</b> relational algebra engine with predicate pushdown, bytecode VM, TLA+-verified convergence loop, v0.15.0–v0.17.0. <b>tern</b> coverage push to 97.5% protocol, faultproxy UDP fault injection, channel API, large datagram fragmentation, v0.3.0–v0.9.0. <b>yourworld2/ge</b> scene protocol E2E, NetworkBackend (bgfx RendererContextI over the wire), H.264 streaming with zero-copy IOSurface. <b>jevon</b> Grok Realtime voice bridge, desktop web UI, WKWebView native path. 574 commits across 9 repos. ~5-8 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-03-22.md"><b>2026-03-16…22</b></a> rustuml from zero to 12,500 golden tests (18 diagram types), tern extracted as standalone WebTransport relay (5-platform clients, Fly.io), HMS2 V1+V2 complete (821 swallowed exceptions fixed), cworkers C rewrite (35KB), jevon protocol state machine + TLA+, den bootstrapped</summary>

<b>rustuml</b> from initial commit to 18 diagram types with 12,500+ golden test pairs against Java PlantUML reference, TIM preprocessor, PNG/PDF/EPS output. <b>tern</b> extracted from jevon into standalone WebTransport relay with Go/Swift/Kotlin/TypeScript clients, raw QUIC + WebTransport, LAN direct upgrade, deployed to Fly.io. <b>hms</b> V1 verified + all 19 V2 sub-targets, 821 swallowed exceptions fixed, beta feature infrastructure. <b>cworkers</b> rewritten from Go to C (35KB binary) with Go TUI dashboard. <b>jevon</b> protocol state machine framework with TLA+ formal verification, research paper. <b>yourworld2/ge</b> Dawn removal complete, bgfx globe rendering, scene display list protocol, H.264 dev mode. <b>den</b> bootstrapped as Rust Homebrew reimplementation. 246 commits across 11 repos. ~6-9 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-03-15.md"><b>2026-03-09…15</b></a> GPU parity optimizer (JFA + differential evolution), server-driven iOS Lua runtime, cworkers v0.1-v0.9 in one week, HMS2 five-wave completion (50 targets), sqldeep recursive tree construction, linq v2 iter.Seq migration</summary>

<b>yourworld2</b> GPU-accelerated visual parity optimizer — 5 WGSL compute shaders (Sobel, JFA, Chamfer distance), differential evolution tuning ~17 parameters at ~50 eval/sec. Three feature waves: hints, magnification, menus, tutorials, achievements, encyclopedia. Cube map pipeline with shapefile water detection. <b>hms</b> five-wave HMS2 completion: recurrence engine, SSE multiplexer, RBAC, transport, 50 convergence targets. <b>cworkers</b> from initial commit to MCP server + Svelte dashboard across 9 releases. <b>jevon</b> server-driven Lua UI on iOS (26 SwiftUI builders, sqlpipe sync). <b>sqldeep</b> recursive tree construction via 3-CTE bracket injection (v0.6-v0.8). <b>linq</b> v2 iter.Seq migration. <b>csp</b> processor reuse fix + 3 research papers. 228 commits across 13 repos. ~5.5-9 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-03-08.md"><b>2026-03-02…08</b></a> HMS2 full-stack rewrite (C#/SvelteKit/30+ screens/MFA/QR transfer), yourworld2 wave-based game buildout, csp channel use-after-free fix + buffered channels, jevon iOS app + QR discovery, frozen zero-alloc reads</summary>

<b>hms</b> HMS2 full-stack rewrite: Go-to-C# backend migration, SvelteKit SPA, 30+ screens across 16 API domains, TOTP MFA, QR session transfer. <b>yourworld2</b> wave-based feature buildout — 5 game modes, menu/tutorial/achievement systems, audio, zoom, HUD — from globe renderer to complete game in one day. <b>csp</b> channel use-after-free fix, buffered channels, CI flake resolution, Windows port completion (v0.3.0). <b>jevon</b> renamed from dais with iOS app, QR server discovery, filesystem session discovery, trust model. <b>frozen</b> zero-alloc read path (v1.10.0, v1.11.0). <b>ge</b> protocol v4 with orientation pipeline and reconnect reliability. SQL stack: sqldeep PostgreSQL backend, sqlift C-only API, sqlpipe Go wrapper. 305 commits across 15 repos. ~5-9 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-03-01.md"><b>2026-02-23…03-01</b></a> csp 5-phase Windows port + TLA+ verification, frozen H128 500x equality speedup, sqldeep transpiler from scratch, dais + doit new Claude Code tools, stock-car-racing Unity 6 + null-ref audit</summary>

<b>csp</b> completed a full 5-phase Windows port (kqueue/epoll/Windows thread pool reactors), TLA+ formal verification for 4 concurrent protocols, and ARM64 thread-local corruption fix. <b>frozen</b> H128 128-bit content hash + recursive XOR hash (h0) delivering 500x set inequality speedup. <b>sqldeep</b> built from scratch as SQL transpiler with FK-guided join path algebra (4 releases). <b>dais</b> multi-session Claude Code orchestrator and <b>doit</b> three-level capability broker both designed and shipped. <b>sqlift</b> Go port with cross-language hash verification (6 releases). <b>stock-car-racing</b> Unity 6 upgrade with 61-finding null-ref audit. 364 commits across 13 repos. ~6-10 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-02-22.md"><b>2026-02-16…22</b></a> csp extraction-to-platform (133 commits, 100+ combinators, topology surgery, TLA+, C++23), mk build tool from scratch to Homebrew, sqlift + sqlpipe new libraries, yourworld2 state sync</summary>

<b>csp</b> went from M:N scheduler to full platform: 100+ stream combinators, channel topology surgery (swap/fuse/splice/tap), cancellation framework with cancel-aware TLS, kqueue I/O, TLA+ verification (9+ models), C++23 migration, demand-paged stacks, dynamic scoping, 6-paper engineering series. <b>mk</b> built from scratch as a modern build tool (pattern rules, parallel execution, stdlib) and shipped 5 releases to Homebrew. Two new C++ libraries: <b>sqlift</b> (declarative SQLite migration) and <b>sqlpipe</b> (streaming SQLite replication). <b>yourworld2</b> gained SQLite-backed game state with bidirectional sync via sqlpipe, carousel GPU silhouettes, and engine rebrand (sq to ge). 313 commits across 11 repos. ~10-17 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-02-15.md"><b>2026-02-09…15</b></a> csp library born (M:N threading, timers, sanitizers), multimaze2 from scratch to Box2D + live-tunable physics, gg CLI overhaul, yourworld2 carousel + audio, universal grammar research</summary>

<b>csp</b> extracted from bricabrac and rapidly expanded with timer channels, M:N scheduling, sanitizer support, and microbenchmarking. <b>multimaze2</b> built from scratch (custom physics, 72 ASCII-art levels, WebGPU renderer) then swapped to Box2D v3 with live-tunable SQLite-persisted physics. <b>gg</b> comprehensive CLI overhaul (interactive installer, shell injection elimination, 27 integration tests, CI). <b>yourworld2</b> country carousel with GPU silhouette rendering, placement mechanics, and audio. <b>wbnf</b> universal grammar research paper. <b>arrai</b> strategic analysis. 129 commits across 10 repos. ~6-11 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-02-08.md"><b>2026-02-02…08</b></a> wire-based remote rendering architecture, engine extraction completion, bgfx-to-Dawn migration, progressive mip streaming with ASTC compression, RAII live resize</summary>

<b>yourworld2</b> dominated: completed engine extraction into sq submodule, migrated from bgfx to Dawn/WebGPU, built wire-based remote rendering with headless server and mobile receivers, progressive mipmapped texture streaming with ASTC compression (4x faster startup), mip cache probe protocol. iOS and Android receiver support. 77 commits across 1 repo. ~3-5 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-02-01.md"><b>2026-01-26…02-01</b></a> yourworld2 60-commit explosion (GPU atlas, RAII architecture, constrained Delaunay, damped rotation, engine extraction begins), esfera2 geodesic chess launched</summary>

<b>yourworld2</b> exploded from 8-commit prototype to full application: GPU texture atlas generation with two-pass antimeridian handling, RAII resource architecture, Triangle-based constrained Delaunay triangulation replacing earcut, JSON manifest + binary mesh pack asset pipeline, damped globe rotation with frame-rate-independent decay, translucent bathymetry ocean, visual regression tests, and engine extraction into sq/ directory. <b>esfera2</b> launched as new geodesic chess project (Andrew Cantos). 61 commits across 2 repos. ~2-4 months traditional equivalent.

</details>

<details>
<summary><a href="reports/weekly-report-2026-01-25.md"><b>2026-01-19…25</b></a> first week of AI-assisted development, yourworld2 globe prototype born, Android 16KB page compliance, iOS resolution fix</summary>

First week of AI-assisted development. <b>yourworld2</b> born as a globe rendering prototype with bgfx/SDL3, ESRI shapefile parsing, country outline rendering, and pImpl architecture from day one. <b>stock-car-racing</b> Android build stabilisation: Gradle cache debugging, Facebook SDK regression workaround, version code bump. <b>yourworld</b> iPhone resolution scaling fix and project documentation. 15 commits across 3 repos. ~1-2 months traditional equivalent.

</details>

## Metrics

Figures come from qualitative per-repository reads of the actual commits, scored on four axes (impact, platform depth, correctness surface, scope) and converted into traditional-development equivalents under both a single-generalist and specialist-team model. Every number is a range. See [docs/methodology.md](docs/methodology.md) for the full derivation.

Each row packs the period stats into one cell — commits (ℂ), lines added/removed in kloc (☲), actual human hours (**AI**), single-generalist months-equivalent (**H**), and gain multiplier (×).

| Week&nbsp;ℂommits&nbsp;☲±kloc<br>AI&nbsp;Human&nbsp;boost× | Highlights |
|--------|------------|
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-08-30.md">08-24</a>&nbsp;ℂ183&nbsp;☲+116-8\*<br><b>AI</b>18-30h&nbsp;<b>H</b>3.0-4.8mo&nbsp;40-70× | React daily + statedb, ladder fallback, mnemo retain=1, interned arr.ai shapes, tapper. \*new globs: mnemo zstd, housekeeping snapshots; orthograph +41k conversion squash |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-08-23.md">08-17</a>&nbsp;ℂ411&nbsp;☲+99-63\*<br><b>AI</b>16-26h&nbsp;<b>H</b>2.8-4.3mo&nbsp;40-70× | host-owned MCP + CloseGoal, Exclusive MCP, bullseye dirty-ledger, ytt split clocks. \*sawmill wipe +1/−55k; no new globs; +8.0k/−2.1k lockfile and ledger omitted |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-08-16.md">08-10</a>&nbsp;ℂ263&nbsp;☲+83-10\*<br><b>AI</b>14-24h&nbsp;<b>H</b>2.4-3.8mo&nbsp;40-70× | ghost-fleet adopt + mutual supervision, Claude cache-read ceiling, Codex refusal matrix, bullseye SHA. \*no new exclude globs; +5.3k/−0.6k lockfile and ledger omitted |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-08-09.md">08-03</a>&nbsp;ℂ297&nbsp;☲+252-14\*<br><b>AI</b>18-30h&nbsp;<b>H</b>2.3-3.8mo&nbsp;60-95× | orthograph 0→brew in six days, jevons spend oracle + context ceiling + worker write/commit guards, slacker TLS OAuth, mnemo 70→18 tools. \*three new exclude globs: orthograph SPM build tree, both report repos' `reports/`+`docs/` (history rewrite re-added the back-catalogue) — +72k/−4.9k omitted |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-08-02.md">07-27</a>&nbsp;ℂ115&nbsp;☲+82-9\*<br><b>AI</b>14-24h&nbsp;<b>H</b>1.1-1.8mo&nbsp;35-60× | summariser containment after a 4.3B-token runaway, ge gesture hints + tile pyramid, csp ARM64 stack analyser, mnemo cost engine, ytt Go port. 40 releases. \*+8.2k/−2.8k bulk omitted; no new globs |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-07-26.md">07-20</a>&nbsp;ℂ63&nbsp;☲+27-7\*<br><b>AI</b>12-20h&nbsp;<b>H</b>0.8-1.3mo&nbsp;30-50× | writ declared-intent sandbox, blurter released same-day, ge textures + metrics ring (4 tags), csp ~3× scheduler fix + Windows gate, ytt 16-day outage closed. \*six new exclude globs this week: ge `headers/`+`prebuilt/`, csp `dist/`, lockfiles, `bullseye.yaml` (+2.9k/−1.2k omitted) |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-07-19.md">07-13</a>&nbsp;ℂ96&nbsp;☲+132-13\*<br><b>AI</b>11-18h&nbsp;<b>H</b>0.7-1.2mo&nbsp;30-55× | ge web platform (Emscripten/WebGL2), spyder wasm command-stream glass, jevons MCP attach + fail-closed durability, csp ~146 ns hot-path, mnemo vault/plugins, sawmill 18-language matrix. \*+770k vendor omitted (spyder +731k, ge +38k); yourworld2 goldens + ge verdicts still in ☲ |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-07-12.md">07-06</a>&nbsp;ℂ120&nbsp;☲+93-33\*<br><b>AI</b>14-24h&nbsp;<b>H</b>0.8-1.4mo&nbsp;35-60× | MultiMaze 2 v1 store launch, pigeon crypto remediation (AES-GCM nonce-reuse), jevons v0.5.0 cockpit + cost governance, ged→spyder Plateau P, Grok provider rollout, bullseye four-tool API. \*+35k vendor omitted (bullseye +29k, yourworld2 +5k) |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-07-05.md">06-29</a>&nbsp;ℂ169&nbsp;☲+55-50<br><b>AI</b>13-23h&nbsp;<b>H</b>0.7-1.2mo&nbsp;30-55× | fleet-wide Fable-5 security audit + remediation (8 repos), ge bgfx eradication + TiltBuggy differential oracle, rustuml parity honesty ratchet, mnemo menu-bar navigator, sawmill discovery/retrieval tier. |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-06-28.md">06-22</a>&nbsp;ℂ74&nbsp;☲+334-20\*<br><b>AI</b>9-15h&nbsp;<b>H</b>0.9-1.4mo&nbsp;20-40× | den v1.0.0 RC (trust model, SAT solver), ge headless render-to-PNG + GlobeController, rustuml real-world swimlane parity, mnemo idle-CPU elimination. \*Unity-regenerated assets still in ☲ |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-06-21.md">06-15</a>&nbsp;ℂ217&nbsp;☲+40-10<br><b>AI</b>14-24h&nbsp;<b>H</b>1.6-2.6mo&nbsp;28-46× | rustuml swimlane-v2 engine, mnemo reliability suite (compaction/three-tier), bullseye five releases + issue mirror, multimaze2 level solver, stock-car Unity test harness. |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-06-14.md">06-08</a>&nbsp;ℂ75&nbsp;☲+25-4<br><b>AI</b>9-15h&nbsp;<b>H</b>1.2-1.9mo&nbsp;18-30× | spyder iOS ≤16 lockdown, csp pull-based io::source, bullseye git-history ID allocator, ge SpriteBatch pooling, rustuml compression-engine port, vellum rich-text import. |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-06-07.md">06-01</a>&nbsp;ℂ432&nbsp;☲+54-11<br><b>AI</b>9-15h&nbsp;<b>H</b>1.1-1.9mo&nbsp;25-45× | rustuml PlantUML activity-diagram layout parity, ge eleven-release diagnostics/RPC sprint, multimaze2 soft-shadow lighting + IAP, spyder bidirectional RPC channel. |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-05-31.md">05-25</a>&nbsp;ℂ332\*&nbsp;☲+445-16\*<br><b>AI</b>6-10h&nbsp;<b>H</b>0.7-1.3mo&nbsp;20-35× | rustuml v0.7.0 XML-parity merge, ge bgfx→sokol_gfx migration + prebuilt-vendor cutover, cv discovered-dependencies build model, mnemo compactor data-plane hardening. \*landed-only; 269 are rustuml's previewed-last-week merge; +27k vendor omitted (ge +27k); ge prebuilt/header bulk outside vendor/ still in ☲ |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-05-24.md">05-18</a>&nbsp;ℂ124&nbsp;☲+121-31<br><b>AI</b>18-28h&nbsp;<b>H</b>3.5-5mo&nbsp;30-50× | mnemo eight releases (backup + schema + workers), spyder self-healing tunnel, ge sixteen-blocker mega-PR, pigeon five-runtime fan-out, den PackageProvider. |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-05-17.md">05-11</a>&nbsp;ℂ142&nbsp;☲+40-16<br><b>AI</b>13-25h&nbsp;<b>H</b>4.5-7.5mo&nbsp;30-65× | bullseye kind-enum removal (second schema cut in two weeks), ge::iap cross-platform module, HMS2 patient-view fidelity fan-out, pigeon five-language wire-format codegen. |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-05-10.md">05-04</a>&nbsp;ℂ158&nbsp;☲+28-18<br><b>AI</b>19-33h&nbsp;<b>H</b>4-7mo&nbsp;30-55× | ge eighteen-release canonical 2D/UI surface in five days, spyder pmd3-bridge deletion for direct go-ios, multimaze2 faithful-to-2010 physics, crosshair v0.1.0 release. |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-05-03.md">04-27</a>&nbsp;ℂ253&nbsp;☲+87-39<br><b>AI</b>22-36h&nbsp;<b>H</b>5-8mo&nbsp;25-50× | spyder eleven releases (transport split), csp QUIC on ngtcp2, ge Android lifecycle + iOS orientation, sawmill AST-aware merge. |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-04-26.md">04-20</a>&nbsp;ℂ355&nbsp;☲+91-19<br><b>AI</b>20-32h&nbsp;<b>H</b>5-8mo&nbsp;30-50× | mnemo eleven releases (Windows + ARM64 + mTLS federation + four tools), spyder pmd3-bridge migration complete, HMS oracle validation toolchain. |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-04-19.md">04-13</a>&nbsp;ℂ391&nbsp;☲+98-16<br><b>AI</b>18-28h&nbsp;<b>H</b>5.5-9mo&nbsp;35-55× | pageflip + spyder launched, mnemo v0.16-v0.21 (images/CLIP/compaction/connection identity/HTTP), pigeon TLA+ cutover + ngtcp2 QUIC C, ge v0.1.0 engine split, bullseye per-repo storage. |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-04-12.md">04-06</a>&nbsp;ℂ646&nbsp;☲+206-83\*<br><b>AI</b>21-32h&nbsp;<b>H</b>6-9mo&nbsp;30-55× | bullseye 10 releases (portfolio WSJF, cross-repo convergence), mnemo 12 releases (11 tools, session chains), pigeon pure C client, claudia tmux pool, HMS 7 audits. \*+29k vendor omitted (csp +11k, ge +9k) |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-04-05.md">03-30</a>&nbsp;ℂ432&nbsp;☲+1050-521\*<br><b>AI</b>21-31h&nbsp;<b>H</b>5-7mo&nbsp;25-45× | sawmill Rust→Go + open-source (11 frontiers), pigeon session state machines (4 langs + TLA+), sqldeep XML literals (10 releases), nostalgia TUI. \*+56k vendor omitted (sqldeep +33k, ge +19k); den/sqldeep non-vendor bulk still in ☲ |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-03-29.md">03-23</a>&nbsp;ℂ574&nbsp;☲+119-59\*<br><b>AI</b>19-29h&nbsp;<b>H</b>5-8mo&nbsp;25-45× | csp M:N-only (663 tests, quiescence, TLA+), rustuml SVG parity (6 renderers), den C++ rewrite + 5 audits, sqlpipe predicate VM, tern 97.5% coverage. \*+122k vendor omitted (rustuml +76k, den +45k) |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-03-22.md">03-16</a>&nbsp;ℂ246&nbsp;☲+718-9\*<br><b>AI</b>22-32h&nbsp;<b>H</b>6-9mo&nbsp;30-50× | rustuml 12,500 golden tests, tern 5-platform relay, HMS2 V1+V2 (821 exceptions), cworkers C rewrite, jevon TLA+. \*+307k vendor omitted (jevons +306k); goldens/HMS2 bulk still in ☲ |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-03-15.md">03-09</a>&nbsp;ℂ228&nbsp;☲+30-4\*<br><b>AI</b>23-33h&nbsp;<b>H</b>5.5-9mo&nbsp;28-45× | GPU parity optimizer (JFA + Chamfer), Lua iOS runtime, cworkers v0.1-v0.9, HMS2 50 targets, sqldeep RECURSE ON, linq v2. \*+7k vendor omitted (ge +7k) |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-03-08.md">03-02</a>&nbsp;ℂ305&nbsp;☲+54-18\*<br><b>AI</b>21-32h&nbsp;<b>H</b>5-9mo&nbsp;25-45× | HMS2 full rewrite, yourworld2 game buildout, csp channel fix + buffered channels, jevon iOS app, frozen zero-alloc. \*+43k vendor omitted (sqlpipe +28k, sqldeep +14k) |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-03-01.md">02-23</a>&nbsp;ℂ364&nbsp;☲+79-15\*<br><b>AI</b>24-42h&nbsp;<b>H</b>6-10mo&nbsp;25-50× | csp Windows port + TLA+, frozen H128 500x speedup, sqldeep transpiler, dais + doit, Unity 6 audit. \*+296k vendor omitted (sqldeep +281k, sqlift +10k) |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-02-22.md">02-16</a>&nbsp;ℂ313&nbsp;☲+108-25\*<br><b>AI</b>25-46h&nbsp;<b>H</b>10-17mo&nbsp;30-60× | csp 133 commits (100+ combinators, topology surgery, TLA+, C++23), mk to Homebrew, sqlift + sqlpipe. \*+310k vendor omitted (sqlpipe +281k, sqlift +24k) |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-02-15.md">02-09</a>&nbsp;ℂ129&nbsp;☲+50-14\*<br><b>AI</b>17-35h&nbsp;<b>H</b>6-11mo&nbsp;30-90× | csp born (M:N + timers + sanitizers), multimaze2 from scratch to Box2D, gg CLI overhaul, carousel + audio. \*+266k vendor omitted (ge +266k) |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-02-08.md">02-02</a>&nbsp;ℂ77&nbsp;☲+14-9\*<br><b>AI</b>8-15h&nbsp;<b>H</b>3-5mo&nbsp;25-50× | Wire rendering architecture, engine extraction, bgfx-to-Dawn, progressive mip streaming + ASTC. \*+402k vendor omitted (ge +367k, yourworld2 +34k) |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-02-01.md">01-26</a>&nbsp;ℂ61&nbsp;☲+8-3\*<br><b>AI</b>8-15h&nbsp;<b>H</b>2-4mo&nbsp;25-50× | yourworld2 60-commit explosion (GPU atlas, RAII, Delaunay, damped rotation), esfera2 launched. \*+309k vendor omitted (yourworld2 +308k) |
| <a href="/marcelocantos/progress-reports/blob/master/reports/weekly-report-2026-01-25.md">01-19</a>&nbsp;ℂ15&nbsp;☲+2-1<br><b>AI</b>6-11h&nbsp;<b>H</b>1-2mo&nbsp;10-25× | yourworld2 globe prototype born, Android 16KB compliance, iOS resolution fix. |
| **Totals**&nbsp;ℂ**~7,662**\*&nbsp;**☲+4737-1168**<br><b>AI</b>**502-833h**&nbsp;<b>H</b>**9.9-16.8y** | \*landed commits only; ☲ excludes `**/vendor/**` and `**/node_modules/**` across the whole series (~+2985k vendor omitted), plus the fleet `data/line-excludes.yaml` globs from 07-20 onward (earlier weeks not restamped for those). Remaining activity-signal inflation: Unity-regenerated assets, goldens/fixtures, prebuilts outside vendor/, HMS2 codegen, committed sprites. |


## Guide

See [docs/guide.md](docs/guide.md) for detailed instructions on generating these reports. Project-level directives are in [CLAUDE.md](CLAUDE.md).

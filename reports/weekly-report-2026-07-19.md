# Weekly Progress Report — 2026-07-13…19

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Vendor omitted this week: **+770,255/−2,630** (marcelocantos/spyder +731,220, squz/ge +38,776). Excl-vendor landed lines: **+132,039/−13,348** (net **+118,691**).

## Executive Summary

**Eighteen repositories** landed work this week, centred on making the game stack *location-transparent* and the agent fleet *stranger-safe*. The headline shipping event is a **browser lane for the whole ge/spyder path**: **[squz/ge](https://github.com/squz/ge)** gained an [Emscripten](https://emscripten.org/)/WebGL2 direct-mode platform (🎯T157, v0.75→v0.79) so an unmodified consumer `main.cpp` builds to `.html/.js/.wasm`, and **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** shipped a **command-stream browser player** — the same C++ player tree compiled to wasm, served at `/player/`, replaying SP2S at ~55–60 fps in Chrome, WebKit, and Firefox (v0.68→v0.71). Alongside it, ge's **location-transparent stream** (🎯T156/T158/T159/T163) established sensor authority, per-session game instances, and live telemetry so a glass (native player, headless, or browser) can sit anywhere. On the agent side, **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** (v0.6→v0.7) closed the silent toolless-overseer week with ACP MCP attach via **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** v0.18–v0.19 (fail-closed `session/load`, `mcp.claudia.json` to dodge Grok's trust gate), plus a jevons-owned chat log, loopback-only bind, and an embedded web UI so brew installs no longer 404. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** shipped a vault wing MVP and an in-process plugin system (v0.63→v0.68); **[marcelocantos/csp](https://github.com/marcelocantos/csp)** flattened channel rendezvous to **~146 ns across processor counts** (v0.24.0) after a measured 16× negative-scaling root-cause; **[marcelocantos/sawmill](https://github.com/marcelocantos/sawmill)** grew from ~5 to **18 language adapters** with a full MCP smoke matrix (v0.17.0). Commercial project detail: [private week 2026-07-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-19.md).

**96 commits** | **~+132k added / ~−13k removed** (excl. vendor) | **~14–24 person-days traditional equivalent** | **~30–55x multiplier**

> Honesty note: Line stats exclude `**/vendor/**` (and `node_modules/`). Under that policy, **spyder is +22.5k/−1.1k** for authored daemon + player; **~+731k** under `player/vendor/` (ge vendor snapshot — sqlite amalgamation, asio, headers, …) is recorded only as excluded bulk. **ge is +41.2k/−3.9k** excl. vendor (~+39k more under `vendor/`); the remaining ge total still carries T156.6 verdict traces (~+29k). Hand-authored leaders excl. those: mnemo (~+8.5k), csp (~+6.6k), sawmill (~+4.4k), jevons (~+3.9k). Commercial project detail: [private week 2026-07-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-19.md).

### Major Achievements & Innovations

- **ge browser platform (Emscripten/WebGL2)** ([squz/ge](https://github.com/squz/ge), 🎯T157, v0.75→v0.79) — fourth direct-mode platform: unmodified `ge::run(Factory)` builds to wasm via `make web`, sokol GLES3 over WebGL2, Asyncify-preserving native run loop (RAF-aligned, no exception-unwound main loop), IDBFS-backed sqlite, single-threaded (no COOP/COEP). A deepparser arena default-align abort that killed every web app at startup was fixed same-week.
- **spyder browser player + command-stream glass** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder), v0.68→v0.71) — the player C++ tree builds with Emscripten (SDL3 via submodule + prebuilts), attaches over browser WebSocket, and replays SP2S at ~55–60 fps across browsers; protocol-only (no ge sources). Protocol v9 pacing, headless mode (`--headless`/`--script`/`--trace`), and a 32-bit wasm `HashKeyHash` shift-width UB fix (divergent bucket hashes at -O2 had made the first frame never decode).
- **Location-transparent stream** ([squz/ge](https://github.com/squz/ge) 🎯T156/T158/T159/T163 + spyder glass) — sensor authority, seat promotion, per-session game instances, live telemetry; glass declares `kCapHasAccelerometer` and re-answers mid-session `SessionConfig` so a promoted seat re-establishes authority exactly as at connect. Headless AccelSynth reduced to delivery plumbing so arm policy can't drift between glass and server.
- **jevons MCP attach + conversation durability + stranger-safe install** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons), v0.6→v0.7) — root-caused Grok's silent skip of ACP `mcpServers` matching cwd `.mcp.json` in untrusted folders; `mcp.claudia.json` + claudia v0.19 attach proven end-to-end; toolless-boot oracle screams if zero `tools/list` in 45s; jevons-owned fsync chat log + fail-closed resume (claudia v0.18); loopback-only default bind; `go:embed` web UI so brew installs serve `/`.
- **csp channel hot-path flat ~146 ns** ([marcelocantos/csp](https://github.com/marcelocantos/csp), v0.24.0) — measured 16× negative scaling (321 ns at 2 procs → 5,081 ns at 16) root-caused to unconditional `global_mu` on every context switch and wake; channel-owned buffered ring + suite teardown abort; TLA+ models (`OptimisticAlt`, `BufferedChanRing`, `ParkGate`, …) and papers 33–34.
- **mnemo vault wing + plugin system** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo), v0.63→v0.68) — `_mnemo/` namespace + vault layout (decisions/memories + quiet v2); in-process plugin system (config, launch, proxy, facets, signals, MCP bridge) with proof tests; Codex transcript fidelity (model, usage, parent chains).
- **sawmill 18-language adapter matrix** ([marcelocantos/sawmill](https://github.com/marcelocantos/sawmill), v0.17.0) — Java, C#, JS, Ruby, PHP, Kotlin, Swift, C, then Lua/Protobuf/Zig/Bash/SQL; MCP `TestLanguageMatrixSmoke` (parse→find→rename→apply→add_field for every language, no skip hatch); `languages` MCP tool for capability cards.

### Significant Progress

- **yourworld oracle as live layout ground truth** — detail in [private week 2026-07-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-19.md)
- **yourworld2 gameplay recovery + dual-oracle + parallax + web** — detail in [private week 2026-07-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-19.md)
- **spyder self-monitoring health plane** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder), 🎯T89/T90) — stale-tunnel re-establish, usbmux attach/detach grooming, per-entity health state machine (daemon/subprocess/device×layer), durable host Starlark scripts for explore/collect/dynamic regression (🎯T108).
- **claudia fail-closed resume + ACP MCP pass-through** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia), v0.18→v0.19) — `session/load` never silently mints a replacement for a materialized conversation; ACP `mcpServers` from `Config.MCPConfig`; prefers `mcp.claudia.json` over `.mcp.json`.

### Tough Challenges Overcome

- **A CLI that silently drops MCP servers in untrusted folders** (jevons/claudia) — Grok classifies ACP `mcpServers` matching cwd `.mcp.json` as repo-local and skips them without error; weeks of toolless overseer boots. Fix: session-scoped `mcp.claudia.json` (no trust gate), mint-fresh sessions (load ignores `mcpServers`), plus a 45s toolless-boot oracle that fails loud.
- **wasm32 shift-width UB in the command-stream hash** (spyder player) — `HashKeyHash` put/get compiled divergent bucket hashes on wasm32 at -O2, so every blob lookup missed and the first frame never decoded; fixed the 32-bit shift contract.
- **Asyncify `postRun` treated as exit** (spyder player) — under ASYNCIFY, `main()` suspends at first yield so `postRun` fires seconds after startup and the page reloaded healthy sessions on backoff (1/2/4/8s flicker); switched reload trigger to `onExit`.
- **deepparser arena default align aborting every web app** (ge) — wasm startup died before first frame; fixed align and recooked `libliteparser` across prebuilds.
- **Channel rendezvous that got slower with more processors** (csp) — serial two-imp workload went 16× worse from 2→16 procs because `drain_suspended` and `Imp::schedule` took `global_mu` on every switch/wake; hot-path overhaul flattened to ~146 ns across counts.

### Contributors

- **Marcelo Cantos (Andrew Cantos co-authored two esfera2 planni…** — detail in [private week 2026-07-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-19.md)
---

## Tooling & Workflow

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — MCP Attach + Durability + Stranger-Safe (13 commits, v0.6.0→v0.7.0)

**The biggest tooling effort of the week.** Overseer MCP tools attach via claudia v0.19: concrete bind-addr `.mcp.json`/`mcp.claudia.json`, session rotation every boot (CLI ignores `mcpServers` on load; continuity via `chatlog.Recap`), persona announces the MCP namespace, and a toolless-boot oracle (🎯T50). Conversation durability (🎯T30.1): append-only fsync JSONL at `~/.jevons/chatlog/`, replay before liveness so a dead overseer can't blank history, fail-closed resume through claudia v0.18. Security floor (🎯T6): loopback-only default bind. T48 campaign: prune ge submodule/C++ app/remote TUI, docs truth-pass, delete legacy `internal/manager` + REST session surface, CEO-loop hermetic oracle, structured config with no owner identity in code. T39 chat coalesce (one bubble per turn, not per token) + Playwright UI oracle. T53 embed web via `go:embed`. T54 stranger first-run legibility. +3,947/−2,288, ~17 new `func Test`.

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Browser Player + Health + Starlark (9 commits, v0.68→v0.71)

- **Browser player** (🎯T101/T106): Emscripten wasm glass at `/player/`, WebSocketClient_web (Asyncify-yielding recv), main-loop RAF + 250ms hidden-page fallback, HashKeyHash wasm32 fix, non-finite sensor filter, onExit reload semantics.
- **Command-stream glass** (🎯T97/T156.7): protocol v9, magic-agnostic streamrelay, headless mode, InputScript, QR-less iOS launch via Documents/`stream_addr`, soft-fail sqlpipe to `:memory:`.
- **Health plane** (🎯T89/T90): `ReestablishTunnel`, usbmux attach/detach listener, health Model with six states and recovery-exhaustion escalation only.
- **Durable host Starlark** (🎯T108): explore/collect/dynamic-regress recipes, `run_script`/`list_scripts`. +22,528/−1,058 (excl. `player/vendor/`; +731,220 vendor excluded), ~100 new `func Test` + ~70 TEST-related C++ lines.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Vault + Plugins + Codex Fidelity (10 commits, v0.63→v0.68)

- **Vault wing MVP** (🎯T64.2–T64.4): `_mnemo/` namespace, `vault_layout` config, decisions/memories + quiet v2.
- **Plugin system** (🎯T102): in-process manager, launch, proxy, facets, signals, MCP bridge — complete with proof suite.
- **Codex transcript fidelity** (🎯T112): model, usage, parent chains folded into the search spine.
- Auto-upgrade hot-reload, 5m idle default, Windows flake fix. +8,457/−275, ~61 new `func Test`.

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Fail-Closed Load + ACP MCP (5 commits, v0.18→v0.19)

- **Fail-closed `session/load`** (v0.18.0): `RequireResume` / `Materialized` — never silently mint a replacement session or overwrite the registry id.
- **ACP `mcpServers` pass-through** (v0.19.0): convert Claude-style MCP config to ACP entries; prefer `mcp.claudia.json` so Grok does not reclassify servers as repo-local; debug request logging on the ACP wire. +236/−32, ~3 new tests (small surface; hermetic coverage rides prior fixtures).

### [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) — 18-Language Matrix (4 commits, v0.17.0)

- Eight then five more language adapters (Java/C#/JS/Ruby/PHP/Kotlin/Swift/C + Lua/Protobuf/Zig/Bash/SQL); full `LanguageAdapter` query surface; language-matrix MCP smoke with no skip hatch; Ruby `add_field` end-keyword body fix; `languages` MCP capability cards; THIRD_PARTY_NOTICES for binary releases. +4,442/−74, ~41 new `func Test`.

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) · [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) · [marcelocantos/issuepipe](https://github.com/marcelocantos/issuepipe) — Diagnostics

- **sqlpipe** (2 commits, v0.29→v0.30): preserve `_sqlpipe_meta` on Database reopen; richer migration diagnostics + dual-channel transport tests (authored ≈1.3k triplicated across C++/Go/Swift mirrors). +1,306/−264 excl. vendor.
- **sqlift** (2 commits, v0.18.0): richer apply error messages for on-device diagnosis. +115/−53.
- **issuepipe** (1 commit): document T31 transport (repo webhooks; App deferred to T32). +10/−5.

---

## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Channel Hot-Path Overhaul (3 commits, v0.23→v0.24)

- **Hot-path**: flat ~146 ns rendezvous across processor counts after root-causing negative scaling (paper 33: profiles, `global_mu` on every switch/wake).
- **Channel-owned buffered ring** + suite teardown abort fix (paper 34); formal models `OptimisticAlt`, `BufferedChanRing`, `ParkGate`, `DrainSuspended`, `PlacementClaim` with bug variants. +6,577/−1,639 (includes dist amalgamation + formal + papers).

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) · [arr-ai/arrai](https://github.com/arr-ai/arrai) · [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)

- **pigeon** (1 commit): `DatagramPart` interop fix in csdke2e mixed tests. +8/−9.
- **arrai** (3 commits): Dependabot crypto/docs vulns + Netlify docs build; revert safe-accessor fall=expr. +599/−424.
- **bullseye** (1 commit): ledger update only. +37/−3.

---

## Game Projects

### [squz/ge](https://github.com/squz/ge) — Web Platform + Location-Transparent Stream (8 commits, v0.75→v0.79)

- **Browser platform** (🎯T157): as in Major Achievements — `cmake/web-wasm.cmake`, `SokolContext_web`, `FontLoader_web`, web-template CMake, prebuilt `web-wasm/` cook, Asyncify contract documented in `docs/web-platform.md`.
- **Location-transparent stream** (🎯T156/T158/T159/T163): `CmdStream`, `StreamHostPolicy`, `SeatPolicy`, `ViewerMetrics`, sensor authority, per-session instances, live telemetry; T156.6 verdict traces.
- **T128 MVP**: pass-through + cache for command-stream (progressive optimisations parked).
- **`ge::drawSolid`**: unlit solid-color mesh fill. +41,165/−3,885 excl. vendor (+38,776/−2,590 under `vendor/` excluded); remaining bulk is mostly T156.6 verdict traces, ~57 TEST-related C++ additions.

### [squz/yourworld](https://github.com/squz/yourworld) — Oracle Density (26 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-19.md).*
### [squz/yourworld2](https://github.com/squz/yourworld2) · [squz/esfera2](https://github.com/squz/esfera2) · [squz/multimaze2](https://github.com/squz/multimaze2) — Parity, Parallax, ge Bumps

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-19.md).*
## Strategic Planning & Documentation

### [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) — Series Catch-Up (1 commit)

Published the 2026-07-05 and 2026-07-12 weekly reports (prior period's catch-up land). +6,095/−2,122 (report markdown + SVGs).

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **Health-Management-Systems/hms** — detail in [private week 2026-07-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-19.md)
- **minicadesmobile/stock-car-racing** — detail in [private week 2026-07-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-19.md)
---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-07-13…19. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **18** |
| Total landed commits | 96 |
| Total lines added (landed, excl. vendor) | +132,039‡ |
| Total lines removed (landed, excl. vendor) | −13,348‡ |
| Net new lines (landed, excl. vendor) | +118,691‡ |
| Vendor paths excluded from ☲ | +770,255 / −2,630 (spyder `player/vendor/` + ge `vendor/` + sqlpipe) |
| Languages | Go, C++, Objective-C++, C, GLSL, Starlark, JavaScript, Python, TLA+, Emscripten/Wasm, Markdown, YAML, shell |
| Contributors | 1 primary (Marcelo Cantos); Andrew Cantos co-authored two esfera2 planning commits (excluded from metrics) |

‡*Headline line stats exclude `**/vendor/**` and `**/node_modules/**` (see methodology). Remaining non-vendor bulk: **yourworld2 +34.6k** (goldens/assets), **ge verdict traces ~+29k**. Authored work excl. those is on the order of +50–75k.*

### Per-Repository Breakdown

*Files / ±lines exclude `vendor/` and `node_modules/`. Vendor bulk (if any) is in the last column.*

| Repo | Commits | Files | Lines added | Lines removed | Net | Vendor excluded |
|------|---------|-------|-------------|---------------|-----|-----------------|
| [squz/ge](https://github.com/squz/ge) | 8 | — | +41,165 | −3,885 | +37,280‡ | +38,776 / −2,590 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 1 | — | +34,629 | −535 | +34,094‡ | — |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 9 | — | +22,528 | −1,058 | +21,470 | +731,220 / −0 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 10 | — | +8,457 | −275 | +8,182 | — |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 3 | — | +6,577 | −1,639 | +4,938 | — |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 1 | — | +6,095 | −2,122 | +3,973 | — |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 4 | — | +4,442 | −74 | +4,368 | — |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 13 | — | +3,947 | −2,288 | +1,659 | — |
| [squz/yourworld](https://github.com/squz/yourworld) | 26 | — | +1,777 | −618 | +1,159 | — |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 2 | — | +1,306 | −264 | +1,042 | +259 / −40 |
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | 3 | — | +599 | −424 | +175 | — |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 5 | — | +236 | −32 | +204 | — |
| [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) | 2 | — | +115 | −53 | +62 | — |
| [squz/esfera2](https://github.com/squz/esfera2) | 5 | — | +109 | −64 | +45 | — |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 1 | — | +37 | −3 | +34 | — |
| [marcelocantos/issuepipe](https://github.com/marcelocantos/issuepipe) | 1 | — | +10 | −5 | +5 | — |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 1 | — | +8 | −9 | −1 | — |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 1 | — | +2 | −0 | +2 | — |

‡ *yourworld2 net is mostly golden fixtures/assets; ge net still carries verdict traces outside `vendor/`.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~100 | health/tunnel recovery oracles + player/glass unit tests |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~61 | plugin system + vault layout + Codex fidelity |
| [squz/ge](https://github.com/squz/ge) | ~57 | CmdStream / stream policy / solid-fill (TEST* additions) |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | ~41 | 18-language matrix + adapter capture assertions |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~17 | CEO-loop, chatlog, config, Playwright UI oracles |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) · [marcelocantos/csp](https://github.com/marcelocantos/csp) · [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~5 | meta-preserve, formal/bench suite, fail-closed load |
| **Total** | **~280** | landed only; conservative diff-grep estimates |

### Daily Activity

![Daily active repositories](daily-activity-2026-07-19.svg)

*(All-repo active-repository counts per day. Plotted: Mon 07-13 8, Tue 07-14 3, Wed 07-15 2, Thu 07-16 4, Fri 07-17 5, Sat 07-18 16, Sun 07-19 10. Saturday–Sunday are the centre of gravity: jevons MCP/durability, ge web+stream, spyder player, mnemo plugins, csp hot-path, and the game parallax landings all cluster there.)*

---

## Ideas & Innovations

### A Browser That Is Just Another Glass ([marcelocantos/spyder](https://github.com/marcelocantos/spyder), [squz/ge](https://github.com/squz/ge))
Once H.264 was the stream and the browser was a decoder, the glass and the game were different codepaths. This week's cut is structural: **the same command-stream protocol drives a native player, a headless glass, and a wasm player**, and ge's direct-mode platform builds the *game* itself to the browser with Asyncify rather than a rewritten main loop. Hard ge↔spyder decoupling holds (protocol-only; no ge sources in the player). The insight is that location transparency is a *protocol + seat-authority* problem, not a transport problem — when the glass declares accelerometer capability and re-answers mid-session `SessionConfig` on seat promotion, a browser tab and a phone become interchangeable seats.

### MCP Attach That Survives an Untrusted Folder ([marcelocantos/jevons](https://github.com/marcelocantos/jevons), [marcelocantos/claudia](https://github.com/marcelocantos/claudia))
Grok's ACP path loads MCP servers from the session parameter, but **silently reclassifies any server whose name matches cwd `.mcp.json` as repo-local and drops it in untrusted folders** — no error, just a toolless agent. The fix is a session-scoped filename the CLI does not scan (`mcp.claudia.json`), mint-fresh sessions on every boot (because load ignores `mcpServers`), and a regression oracle that treats zero `tools/list` within 45s as a loud failure. The elegance is making the silent failure *observable* and then unrepresentable: an overseer that boots without tools cannot look healthy.

### Fail-Closed Resume as Conversation Integrity ([marcelocantos/claudia](https://github.com/marcelocantos/claudia), [marcelocantos/jevons](https://github.com/marcelocantos/jevons))
A provider that "helpfully" mints a new session when load fails is a data-loss bug wearing a recovery mask. claudia v0.18 makes **`session/load` fail closed for materialized conversations** (`RequireResume` / `Materialized`), and jevons owns the durable log separately from the provider store — every chat line is fsynced first, replay happens before the liveness check, and a dead overseer can no longer blank history. The conversation is the durable artefact; the process and the provider session are caches of it.

### Measuring Negative Scaling Before Optimising ([marcelocantos/csp](https://github.com/marcelocantos/csp))
csp's channel hot-path work started from a bench that showed the *wrong* shape: a serial two-imp rendezvous got **16× slower** as processors rose from 2 to 16, and a large buffer was slower than unbuffered. Profiling pinned unconditional `global_mu` on every context switch and wake; the fix flattened rendezvous to ~146 ns across counts. The method essay is the point: **measure the scaling curve first**, so "faster" is defined against a structural defect rather than a local micro-optimisation.

### An 18-Language Smoke Matrix with No Skip Hatch ([marcelocantos/sawmill](https://github.com/marcelocantos/sawmill))
Language adapters are usually demoed on the happy path. sawmill's `TestLanguageMatrixSmoke` drives parse→find_symbol→rename→apply→add_field through the MCP handler for **every supported language with no skip escape**, and writing it found a real bug (Ruby `add_field` assumed brace-delimited bodies). The matrix is the product: support that is not exercised end-to-end on disk is not support.

### The Legacy App as a Denser Layout Oracle ([squz/yourworld](https://github.com/squz/yourworld))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-19.md).*
### Asyncify as a Contract, Not a Flag ([squz/ge](https://github.com/squz/ge))
ge's web run loop keeps the native blocking loop and suspends via RAF-aligned Asyncify. The hard rule is that **Asyncify cannot suspend beneath a JS frame**: `ge::run` is `noexcept`, SessionHost compiles without exceptions on web, sqlite fsync is compiled out, and indirect-call suspends abort. Documenting that contract (and the failed alternative — `emscripten_set_main_loop` exception-unwinding C++ cleanups) is what makes the fourth platform maintainable rather than a one-off demo.

---

## Effort Estimate: Traditional vs. AI-Assisted

Shipping density remains high (many version bumps across ge/spyder/mnemo/jevons/csp/claudia/sawmill/sqlpipe). Commercial project detail: [private week 2026-07-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-19.md).

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| ge web platform + location-transparent stream | 4-6 | Emscripten/WebGL2 direct-mode with an Asyncify-safe native run loop, prebuilt wasm cook, sensor authority and per-session instances across native/headless/browser glasses — platform work that spans C++/ObjC++/cmake/wasm. |
| spyder browser player + health + Starlark | 3-5 | Same player tree to wasm (SDL3 submodule/prebuilts, WebSocket glass, wasm32 UB), headless/scripted glass, tunnel self-heal, and a six-state health model with recovery-exhaustion escalation. |
| jevons MCP attach + durability + stranger-safe | 2-4 | Live forensics against a silent CLI trust gate, fail-closed conversation integrity, embedded UI, loopback security floor, CEO-loop and Playwright oracles. |
| csp channel hot-path | 2-3 | Profile-driven concurrency overhaul with formal models and measured flat scaling — scheduler mutex discipline is easy to get subtly wrong. |
| mnemo vault + plugins + Codex | 2-3 | In-process plugin lifecycle with MCP bridge and proof suite; vault layout as a durable personal-knowledge wing. |
| sawmill 18-language matrix | 1-2 | Tree-sitter adapter surface across 18 languages with an end-to-end MCP smoke that admits no skips. |
| yourworld oracle + yourworld2 recovery/parallax | 2-3 | Layout residual compression against a live legacy app; gameplay recovery on sokol; device-tilt parallax on two titles. |
| claudia fail-closed + ACP MCP | 1-2 | Session integrity contract and MCP pass-through that embedders (jevons) depend on. |

### The Diversity Tax

This week spans Go (jevons, mnemo, spyder, claudia, sawmill), C++/ObjC++/Metal (ge, player, yourworld, esfera2), Emscripten/Wasm/WebGL2, Starlark, tree-sitter multi-language CST work, TLA+ (csp formal), Playwright, and mobile device tunnels. No single engineer holds wasm Asyncify contracts, M:N channel schedulers, ACP MCP attach forensics, and geodesic layout oracles at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| ge web + stream / spyder player | 4-6 | Blessing the Asyncify contract, live browser fps soaks, seat-authority design, on-device player attach. |
| jevons / claudia MCP + durability | 3-5 | Live forensics on toolless boots, trust-gate root-cause, kill/resume drills, stranger-install judgement. |
| csp hot-path | 1-2 | Interpreting scaling curves, accepting the mutex redesign, release judgement. |
| mnemo / sawmill / games | 3-5 | Plugin/vault shape review, language-matrix scope, yourworld/esfera2 tilt feel, parity residual judgement. |

### What If It Were One Person?

A single generalist would pay ramp-up across wasm, mobile tunnels, ACP session semantics, CSP scheduling, and globe-layout residual math, then a heavy context-switch tax as the same week ships a browser platform, a fleet MCP fix, and a concurrency hot-path. The expert-days band (~14–24) understates the calendar time once those costs are added; the multi-release shipping cadence is what keeps the multiplier elevated.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~14-24 person-days (~0.7-1.2 months)** |
| Specialist team (traditional) | **~9-16 person-days (~0.45-0.8 person-months)** |
| Actual human effort this week | **~11-18 hours (~1.5-2.5 person-days)** |
| **Multiplier vs. generalist** | **~30-55x** |
| **Multiplier vs. specialist team** | **~18-35x** |

The multiplier runs highest on the ge/spyder location-transparent browser lane — four platforms plus a protocol-only glass with wasm UB and Asyncify contracts is deep platform work a lone generalist would take weeks to land safely — and on the jevons/claudia MCP attach forensics, where a silent CLI behaviour had to be made observable before it could be fixed. It runs lowest on ge/version bumps in consumer games and the issuepipe doc commit. Human contribution concentrated on contracts a specification cannot taste: whether Asyncify is safe, whether a toolless boot is allowed to look healthy, how aggressive residual compression should be against a live oracle, and on-device/browser soaks no agent can perform.

# Weekly Progress Report — 2026-07-06…12

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Excl-vendor landed lines: **+92,767/−33,291** (net **+59,476**). Commercial project detail: [private week 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md).

## Executive Summary

Around it, three large arcs ran in parallel. First, the **Fable-5 audit remediation** shipped — most consequentially in **[marcelocantos/pigeon](https://github.com/marcelocantos/pigeon)** (six releases, v0.26→v0.31), which fixed a confirmed **AES-GCM nonce-reuse race** (16,384 concurrent encrypts had produced 1,964 colliding nonce prefixes), added independent per-stream/per-datagram AEAD counters via HKDF diversification, and closed a relay-MitM hole with a ZRTP-style SAS commit-reveal round — plus remediation in mnemo (v0.60→v0.62), csp (v0.22.0), den, and crosshair, each verify-first. Second, a **Grok provider rollout** threaded the fleet: **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** gained a Grok Task provider then a Grok Session provider over the [Agent Client Protocol](https://agentclientprotocol.com/) (v0.15→v0.17), and **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** and **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** consumed it (a Grok-only harness; Grok transcript ingest). Third, a control-plane consolidation — **"Plateau P"** — **retired the entire `ged` daemon and its React console** across **[squz/ge](https://github.com/squz/ge)** (a −14,211-line deletion) and made **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** the sole control plane, with ge and yourworld now streaming H.264 dev video through spyder end-to-end (verified in headless Chrome). A fleet-wide `targets.yaml → bullseye.yaml` migration swept ~15 further repos mechanically. Commercial project detail: [private week 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md).

**120 commits** | **~+92,767 / ~−33,291** (excl. vendor) | **~16–28 person-days traditional equivalent** | **~35–60x multiplier**

> Honesty note: the raw line totals carry large vendored/generated content. Hand-authored source is led by jevons (~+10k Go), mnemo (~+7k Go), spyder (~+7k Go), pigeon (~+5.8k), and claudia (~+5.3k). Commercial project detail: [private week 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md).

### Major Achievements & Innovations

- **MultiMaze 2 reaches v1 on both stores** — detail in [private week 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md)
- **pigeon crypto remediation** ([marcelocantos/pigeon](https://github.com/marcelocantos/pigeon), v0.26→v0.31, six releases) — 🎯T49 fixes the AES-GCM nonce-reuse race (a `sync.Mutex` in Encrypt/Decrypt makes 16,384 concurrent nonces all-distinct); 🎯T53 gives each named stream a `ModeStrict` channel and datagrams a `ModeDatagrams` channel forked via HKDF diversify labels so a lost datagram can't desync a shared counter; 🎯T52 adds a ZRTP-style commit-reveal SAS round (a relay MitM that could grind a colliding key in 305,883 tries/3.2s no longer can); 🎯T54/T56 fix a ceremony goroutine/handle leak and a last-writer-wins hub-ID hijack. Each ships a failing-then-passing repro under `-race`.
- **jevons v0.5.0 — fleet cockpit + live cost governance** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)) — a durable Butler/CEO thread model (transcript + metadata decoupled from a live process, so a stopped worker transparently `--resume`s — "process-as-cache", 🎯T30) and a whole `internal/cost` package born from a 2026-07-06 token-runaway post-mortem: real-time usage collected from *every* session JSONL (the incident fleet was invisible), a burn-rate monitor with decidable runaway signals, and a warn→throttle→pause→kill enforcer whose `TmuxKillSwitch` reaches the launchd-detached fleet tmux (🎯T36). Plus Origin-validated WebSockets and CSRF guards (🎯T38).
- **ged retired; spyder the sole control plane ("Plateau P")** ([squz/ge](https://github.com/squz/ge), v0.72→v0.74; [marcelocantos/spyder](https://github.com/marcelocantos/spyder), v0.64→v0.67) — spyder absorbed ged's entire control plane onto its MessagePack app-channel (tweaks, logs, state, screenshot, a `/dashboard` SPA) plus H.264 dev-streaming proven live game→spyder→browser (WebCodecs decode, browser→`SDL_Event` input round-trip verified in headless Chrome), across four launch media (device, sim/emu, desktop, server-spawned instance). ge then *deleted* the `ged/` daemon and `web/` console outright (−12,630 lines) and streams its server mode directly through spyder.
- **claudia Grok provider (Task + Session over ACP)** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia), v0.15→v0.17) — `ProviderGrok` through the task seam (resolves the grok binary, maps headless streaming-JSON into `TaskEvent`), then persistent Grok sessions over the Agent Client Protocol (`session/new|load|prompt|update|cancel`, auto-approve permissions), then registry wiring so `Registry.Launch` honours `AgentDef.Provider` instead of always starting Claude. A Codex provider seam landed alongside.
- **mnemo v0.60 — audit hardening + connection-preserving self-upgrade** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo), v0.60→v0.62) — 🎯T109 replaces the client-resettable read guard with a dedicated read driver whose `ConnectHook` authorizer denies ATTACH/query_only-off; 🎯T97 adds a session-affinity edge proxy that upgrades mnemo without invalidating live Claude Code clients, and a graceful SIGTERM drain ending in `wal_checkpoint(TRUNCATE)`; plus Grok transcript ingest (🎯T110/T111).
- **bullseye four-tool ledger API** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye), v0.37→v0.39) — the agent surface collapses to `bullseye_open`/`bullseye_query`/`bullseye_commit`/`bullseye_plan_checks` (legacy tools demoted to shims), mutations return a structured `ids/changed/frontier` envelope with stable error codes, and `release_surface`/`owned_by`/server-minted child IDs add release governance and close a TOCTOU in ID allocation.
- **csp CI deadlock root-cause** ([marcelocantos/csp](https://github.com/marcelocantos/csp), v0.22.0) — a coin-flip third-pairing self-deadlock plus a watchdog storm root-caused and fixed, with the stack-analysis ASan fix.

### Significant Progress

- **esfera2 WebGPU→ge sokol_gfx port lands (1 commit, on master)** — detail in [private week 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md)
- **yourworld2 sokol migration + dual-oracle harness (on master)** — detail in [private week 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md)
- **spyder control-plane migration (9 commits, v0.64→v0.67)** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — beyond Plateau P, a `DesktopAdapter` (a game as a local host process, same interface as iOS/Android) and a server-medium factory model (`spawn_instance`, `InstancePool` acquire/GC), plus iOS tunnel self-heal (🎯T89) that rebuilds stale tunnels on empty tunnel-info.

### Tough Challenges Overcome

- **A nonce counter shared across every pump** (pigeon) — the production `cwire.Channel` counter was shared across all stream pumps and the datagram pump and advanced by a non-atomic C read-modify-write, so concurrent encrypts reused AES-GCM nonces (1,964 collisions in 16,384). The fix serialises the counter and, structurally, forks per-stream and per-datagram channels via HKDF so they can never share a sequence in the first place.
- **A cost monitor that couldn't see the fleet that was burning** (jevons) — the 2026-07-06 runaway was invisible because usage collection only watched *registered* workers, while the detached `claudia-anchor` fleet tmux burned tokens off-book. The fix tails every session JSONL regardless of registration, scopes the kill-switch to fleet-plus-orphan (so the owner's own heavy sessions don't trip it), and adds thin-rate and sustained-breach guards so a single $11 re-cache message can't auto-fire the nuke.
- **A daemon drain that was dead code** (mnemo) — the graceful-drain path existed but ran with `context.Background()`, so `brew services restart` hard-killed mnemo mid-request; the fix wires a real cancelable context through SIGTERM/SIGINT into an ordered, deadline-bounded drain that ends in a WAL checkpoint.
- **A launch that renders on a backend the game had never used** — detail in [private week 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md)
### Contributors

- Marcelo Cantos (with Oliver Lade co-authoring one [arr-ai/arrai](https://github.com/arr-ai/arrai) grammar fix; AI co-authors — Grok 4.5, Codex CLI, and Claude models — appear on `Co-authored-by` trailers throughout).

---

## Tooling & Workflow

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Fleet Cockpit + Cost Governance (11 commits, v0.5.0)

**The biggest tooling effort of the week.** As in Major Achievements — the Butler/CEO thread model (`internal/thread` atomic store + `internal/butler` orchestrator: adopt-observe, spawn, direct-with-rehydrate, idle-GC) and the `internal/cost` clamp-down (L1 real-time usage into SQLite tailing every session JSONL, L2 burn-rate runaway signals, L3 warn→throttle→pause→kill with a `TmuxKillSwitch`, dead-man's switch, and a hard daily ceiling). Later hardened live: global burn made informational-only, fleet+orphan scope drives the kill-switch, a synthetic-runaway drill auto-detects and kills detached burners within 30s. Plus Origin-safe WebSockets, CSRF guards, unbounded history replay, the Grok-only harness pivot, and iOS collapsed to artifact-driven pigeon connect (🎯T14.1). +10,022/−1,568, ~92 new test decls (fakeFleet e2e + cost-ladder oracles).

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Grok Provider (5 commits, v0.15→v0.17)

- **Grok Task provider** (v0.15.0): `ProviderGrok` resolves the grok binary (`GROK_BIN`/PATH/`~/.grok/bin`) and maps headless streaming-JSON into `TaskEvent`, failing closed on Session/rewind until the ACP contract is proven.
- **Grok Session over ACP** (v0.16.0): persistent sessions via the Agent Client Protocol with a hermetic fake ACP server; a `CLAUDIA_GROK_LIVE`-gated live smoke.
- **Registry wiring** (v0.17.0): persists `Provider` on `AgentDef` so `Registry.Launch` stops always starting Claude. A Codex provider seam and hermetic Task-spawn tests (shell fakes replaying golden stream fixtures for all three providers) landed alongside. +5,263/−300, ~58 new test decls.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Audit Hardening + Self-Upgrade (6 commits, v0.60→v0.62)

- **🎯T109 audit hardening**: a dedicated read driver with a `ConnectHook` authorizer denying ATTACH/DETACH and query_only-off; ingest durability fixed (a `bufio.Scanner` token-cap silently dropped oversized lines — switched to `ReadBytes` so the offset is always a true line boundary).
- **🎯T97 connection-preserving upgrade**: a session-affinity MCP edge proxy (pins by `Mcp-Session-Id`) with release detection, an opt-in Homebrew auto-apply state machine, and an affinity-drain that keeps pins on the old backend until the count hits zero.
- **🎯T97.1 graceful drain**: SIGTERM/SIGINT drives an ordered, 10s-deadline drain ending in `wal_checkpoint(TRUNCATE)`; the realtime watcher moves ahead of cold catch-up ingest.
- **🎯T110/T111 Grok ingest**: `~/.grok/sessions` ACP transcripts folded into the search spine with model/usage/session-type fidelity. +7,332/−344, ~69 new test decls.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Four-Tool Ledger API (4 commits, v0.37→v0.39)

- **🎯T45 four-tool API**: `bullseye_open`/`bullseye_query`/`bullseye_commit`/`bullseye_plan_checks`, legacy tools demoted to shims, mutations returning a structured envelope with stable error codes.
- **Release governance** (🎯T42/T43/T44/T46): `release_surface` prefixes filter which unreleased fix commits block a release; `owned_by` excludes a target from the frontier without unblocking dependents; server-minted child IDs close a TOCTOU.
- **Build-perf** (🎯T47–T49): vendored the MCP SDK with a stdio-sized tokio feature set and feature-gated `rusqlite` so `--no-default-features` skips bundled libsqlite3-sys. +32,938/−412 (≈29.5k vendored SDK; authored ≈2.5–3k Rust), ~40 new `#[test]`. Co-authored with Grok 4.5.

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Sole Control Plane (9 commits, v0.64→v0.67)

- As in Major Achievements — ged's control plane ported onto spyder's app-channel with a `/dashboard` SPA, the four-media launch model (`DesktopAdapter` + server-medium factory), H.264 dev-streaming proven live end-to-end in headless Chrome, and Plateau P declared (the ged differential harness and vocabulary deleted). Plus iOS tunnel self-heal (🎯T89). +7,032/−2,009, ~59 new test decls (`SPYDER_GE_TILTBUGGY`-gated live e2e).

### [marcelocantos/den](https://github.com/marcelocantos/den) · [marcelocantos/issuepipe](https://github.com/marcelocantos/issuepipe) · [marcelocantos/crosshair](https://github.com/marcelocantos/crosshair) — Soak, Ingest, Executor

- **den** (1 commit): a remote conviction-loop harness — `soak.sh` over live `~/.den` scenarios driven by SSH against a physical `den-test-mac` (harness 21 PASS/0, soak 14/0/1), plus Fable F1–F5 remediation (archive-symlink escapes, env-slug `..` percent-encoding, fail-closed self-update checksum) and a Mach-O bottle-relocation fix (poured arm64 binaries were SIGKILLed on invalid codesign until `install_name_tool` rewrote the load commands). +1,600/−111.
- **issuepipe** (5 commits, **new repo**): stage 1 of the bullseye GitHub-issues integration — a GitHub App webhook → per-repo sqlpipe Master (`repo_<id>.db`, HMAC-verified, idempotent upserts, cold-start backfill), deployable as a hardened Ubuntu-24.04 C++23 Docker build. +1,769/−17, ~14 new test decls.
- **crosshair** (1 commit): the bullseye convergence executor hardened — 5-field `cron:`/`every:`/`manual` triggers honoured, each attempt in its own process group so a backgrounded descendant can't wedge later ticks, WAL-persisted attempt state, and a 30m→24h backoff ladder (🎯T2 + Fable F4). +948/−75, ~21 new test decls.

---

## Libraries & Infrastructure

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) — Crypto Remediation (10 commits, v0.26→v0.31)

- As in Major Achievements — the AES-GCM nonce-reuse fix (🎯T49), independent per-stream/per-datagram AEAD counters forked via HKDF diversify labels (🎯T53), the ZRTP-style SAS commit-reveal round (🎯T52), per-session salt on artifact reconnect (🎯T50), automatic LAN upgrade (🎯T48), deterministic ceremony teardown (🎯T57), progressive datagram fragmentation with metadata (🎯T59), and a hub-ID ownership fix (🎯T56). Bound per-stream AEAD across the Go/Swift/Kotlin accept paths.
- **Two method essays**: `docs/formal-state-machines.md` (TLA+ in CI, deterministic multi-language codegen, model-implementation fidelity) and `docs/adversarial-modeling.md` (adversary-as-transitions, Dolev-Yao, residual-power properties). +5,779/−770, ~49 new test decls (new `channel_race_test.go`, `hub_ownership_test.go`, `t53_channel_isolation_test.go`, all green under `-race`).

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Structural Fingerprint + Swift Build (4 commits, v0.26→v0.28)

- **Full structural schema fingerprint**: replaces a lossy 32-bit fold with the full structural hash across the C++ core and all three binding mirrors, cutting false schema-equality collisions.
- **Swift package build fix**: vendored the `deepparser` Lemon parser into `CSqlpipe` so the Swift package builds standalone; plus Go `Database` parity in `wrapper.go`, `sqlift` header sync, and lossy dual-channel transport tests (the obsolete `terntest` module removed). +19,289/−867 (≈16.8k vendored parser; authored ≈1.2–1.6k, triplicated across mirrors), ~51 new test decls.

### [marcelocantos/csp](https://github.com/marcelocantos/csp) · [arr-ai/hash](https://github.com/arr-ai/hash) · [arr-ai/arrai](https://github.com/arr-ai/arrai) — Deadlock Fix, Benchmarks, Grammar

- **csp** (3 commits, v0.22.0): the coin-flip third-pairing self-deadlock and watchdog-storm root-cause + ASan fix. +731/−57.
- **arr-ai/hash** (1 commit): ~35 benchmarks comparing interface-boxed hashing against typed fast paths, establishing a perf baseline. +205.
- **arr-ai/arrai** (2 commits): a one-token grammar correctness fix — the safe-accessor fallback `a?.b : c` now binds a full expression rather than the restricted `@` (co-authored by Oliver Lade). +46/−80.

---

## Game Projects

### [squz/ge](https://github.com/squz/ge) — Plateau P: ged Removed (11 commits, v0.72→v0.74)

- **Plateau P** (🎯T145): deletes the entire `ged/` Go daemon (daemon/server/stream/mcp/dashboard) *and* the whole React tweak console (`TweakPanel.tsx`, `PhonePreview`, package-lock) — −12,630 lines, the bulk of the week's −14,211. spyder is now the only control plane.
- **Direct server session**: replaces the brokered session path with a direct one (`ServerSession.mm`, `DirectRenderHost.mm`; `ServerWireBridge`/`SessionHost_brokered` deleted), streaming ge server mode through spyder.
- **Audit remediation** (🎯T140–T143): a null-safe dispatch shim + wire bounds checks in the sokol-dispatch codegen; headless iOS device enrollment (🎯T110); hygiene close-out (README/STABILITY/release-surface). +2,467/−14,211, 2 new tests (a video encode→decode roundtrip + a null-safe dispatch test).

### [squz/esfera2](https://github.com/squz/esfera2) · [squz/yourworld2](https://github.com/squz/yourworld2) · [squz/yourworld](https://github.com/squz/yourworld) — sokol_gfx Convergence

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md).*
### [squz/multimaze2](https://github.com/squz/multimaze2) — Store Launch (3 commits, v3.0.0)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md).*
### [minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit) · [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) — Release Ledger + DebugBridge

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md).*
## Strategic Planning & Documentation

### [marcelocantos/threedee](https://github.com/marcelocantos/threedee) · [marcelocantos.com](https://github.com/marcelocantos/marcelocantos.com) — CAD Import + Blog Fixes

- **threedee** (1 commit, **new repo**): a parametric 3D-printing/CAD project — OpenSCAD `.scad` models generated from Python (`projects/*.py`) with exported `.3mf`/`.stl`/`.step`/`.gcode`, for a range of physical parts (a baby-gate latch, a cat-flap RPi mount, a router-bit rack, Starlock holders). Tracked as a convergence project with a Makefile and `bullseye.yaml`. +1,053.
- **marcelocantos.com** (3 commits): three real deploy fixes — pinned Hugo 0.163.3 in `netlify.toml` (a checksum mismatch on the 2019-pinned 0.53 had broken all deploys) and modernised two theme partials using removed APIs; fixed a corrupted `baseURL` (`$DEPLOY_PRIME_URL` isn't interpolated in `netlify.toml`, so every absolute URL 404'd); added RSS feed autodiscovery. +45/−8.

### Fleet-wide `targets.yaml → bullseye.yaml` migration

A single mechanical migration to bullseye's new ownership model swept ~15 further repos with one commit each — arr-ai/frozen, arr-ai/wbnf, goeezi/check, goeezi/gopkgdep, marcelocantos/{sqldeep, protocol-app, mpe2pdf, pageflip, gg}, minicadesmobile/{drag-n-brag-2, kart-stars, mopar-drag-n-brag, dragster-mayhem}, and squz/bricabrac — no behavioural change. Counted in totals but not narrated individually.

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **Health-Management-Systems/hms** — detail in [private week 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md)
- **squz/ge** — 21 in-flight (+10,867/−7,559); **squz/yourworld2** — 29 in-flight; **marcelocantos/crosshair** — 16 in-flight; **marcelocantos/{spyder, pigeon, mnemo}** — 8–9 each; smaller tranches across den, doit, sawmill, rustuml (36 in-flight — last week's swimlane work continuing).

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-07-06…12. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | 45 total; **~20** with substantive work† |
| Total landed commits | 120 |
| Total lines added (landed) | +92,767‡ |
| Total lines removed (landed) | −33,291‡ |
| Net new lines (landed) | +59,476‡ |
| Authored net lines (estimate) | ~+30–40k (jevons, mnemo, spyder, pigeon, claudia leading) |
| Languages | Go, C++, Objective-C++, Rust, C, GLSL, C#, Swift, Kotlin, TypeScript, Python, OpenSCAD, TLA+, Markdown, YAML, shell |
| Contributors | 1 primary (Marcelo Cantos); Oliver Lade co-authored one arrai commit |

†*~15 repos had a single mechanical `targets.yaml → bullseye.yaml` or MinicadesKit-bump commit (see the fleet-migration note).*
‡*Line totals carry heavy vendored content: **bullseye +32,938 (~29.5k vendored MCP SDK)**, **sqlpipe +19,289 (~16.8k vendored parser)**, **yourworld2 +18,323 (~15.6k vendored MP3 decoder + shapefiles)**, and ge's −14,211 is a ged-daemon/web-console deletion. Hand-authored net is ~+30–40k.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 11 | 134 | +10,022 | −1,568 | +8,454 |
| [squz/ge](https://github.com/squz/ge) | 11 | 139 | +2,467 | −14,211 | −11,744† |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 10 | 113 | +5,779 | −770 | +5,009 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 9 | 91 | +7,032 | −2,009 | +5,023 |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 7 | 13 | +200 | −33 | +167 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 6 | 60 | +7,332 | −344 | +6,988 |
| [minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit) | 6 | 13 | +998 | −41 | +957 |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 5 | 55 | +5,263 | −300 | +4,963 |
| [marcelocantos/issuepipe](https://github.com/marcelocantos/issuepipe) | 5 | 29 | +1,769 | −17 | +1,752 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 4 | 184 | +32,938 | −412 | +32,526‡ |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 4 | 84 | +19,289 | −867 | +18,422‡ |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 3 | 51 | +1,802 | −281 | +1,521 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 3 | 21 | +731 | −57 | +674 |
| [marcelocantos/marcelocantos.com](https://github.com/marcelocantos/marcelocantos.com) | 3 | 8 | +45 | −8 | +37 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 1 | 60 | +18,323 | −1,693 | +16,630‡ |
| [squz/esfera2](https://github.com/squz/esfera2) | 1 | 50 | +6,293 | −9,706 | −3,413 |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 1 | 21 | +1,600 | −111 | +1,489 |
| [marcelocantos/threedee](https://github.com/marcelocantos/threedee) | 1 | 16 | +1,053 | −0 | +1,053 |
| [squz/yourworld](https://github.com/squz/yourworld) | 2 | 17 | +1,494 | −251 | +1,243 |
| [marcelocantos/crosshair](https://github.com/marcelocantos/crosshair) | 1 | 11 | +948 | −75 | +873 |
| [arr-ai/hash](https://github.com/arr-ai/hash) | 1 | 2 | +205 | −0 | +205 |
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | 2 | 5 | +46 | −80 | −34 |
| *~17 mechanical-only repos* | ~19 | — | — | — | — |

† *ge: net is dominated by the −14,211 ged-daemon/web-console deletion.*
‡ *bullseye/sqlpipe/yourworld2: nets dominated by vendored SDK/parser/decoder+geodata — authored ≈2.5–3k, 1.2–1.6k, and 2k respectively.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~92 | Butler/cost-ladder oracles + fakeFleet e2e |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~69 | audit regressions + ingest-boundary + Grok ingest |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~59 | live e2e + headless-Chrome streaming oracles |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~58 | hermetic fake-CLI/fake-ACP + golden fixtures |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | ~49 | crypto race regressions (green under `-race`) |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~51 | transport + fingerprint + diff-sync |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | ~40 | ledger-API core tests |
| [arr-ai/hash](https://github.com/arr-ai/hash) | ~35 (benchmarks) | boxed-vs-typed hashing baseline |
| [marcelocantos/crosshair](https://github.com/marcelocantos/crosshair) | ~21 | trigger/backoff + F4 regression |
| [marcelocantos/issuepipe](https://github.com/marcelocantos/issuepipe) | ~14 | HMAC + idempotent upsert + backfill |
| [squz/multimaze2](https://github.com/squz/multimaze2) · [squz/ge](https://github.com/squz/ge) | ~3 | lighting-quality + video roundtrip/null-safe dispatch |
| **Total** | **~490** | landed only; conservative diff-grep estimates |

### Daily Activity

![Daily active repositories](daily-activity-2026-07-12.svg)

*(All-repo active-repository counts per day. Plotted: Mon 07-06 8, Tue 07-07 2, Wed 07-08 2, Thu 07-09 0, Fri 07-10 1, Sat 07-11 36, Sun 07-12 2. The Saturday 07-11 spike of 36 is the week's centre of gravity: the Fable-5 remediation ships across pigeon/csp/mnemo/spyder/bullseye/claudia plus the fleet-wide `bullseye.yaml` migration all landed that day.)*

---

## Ideas & Innovations

### A Cost Monitor That Watches the Fleet It Doesn't Manage ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
The 2026-07-06 token runaway was expensive precisely because it was invisible: usage collection only watched *registered* workers, while a detached `claudia-anchor` fleet tmux burned tokens off the books. jevons' clamp-down inverts the assumption — **it tails every session JSONL on disk regardless of whether jevons started it**, so an orphaned or adopted session can't hide. The subtlety is in *not over-killing*: the kill-switch is scoped to fleet-plus-orphan so the owner's own heavy interactive sessions don't trip it, and thin-rate and sustained-breach guards stop a single expensive re-cache message from auto-firing the nuke. A governor that can see spend it doesn't control, and distinguish it from spend it should, is the hard part of an automated kill-switch.

### Forking Nonce Streams So They Can Never Collide ([marcelocantos/pigeon](https://github.com/marcelocantos/pigeon))
The nonce-reuse bug had an obvious point fix — serialise the shared counter — but the deeper remediation is structural. 🎯T53 gives **every named stream and the datagram path its own AEAD channel, forked from the session key via HKDF diversify labels** (`pigeon/v1/stream:<name>`, `pigeon/v1/datagram`), so two flows never share a sequence space to begin with. The elegance is that a whole class of desync bugs — a lost datagram advancing a shared counter, a second stream racing the first — becomes unrepresentable rather than merely guarded, and the SAS commit-reveal round applies the same instinct to key agreement: commit before reveal so a relay can't grind after seeing the peer's public key.

### Process-as-Cache: Threads That Outlive Their Workers ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
A fleet orchestrator usually conflates a conversation with the process running it, so killing the process loses the thread. jevons' Butler model separates them: a **thread is a durable transcript plus metadata, and the worker process is treated as a cache of it**. A stopped or aged worker is transparently `--resume`d from the thread when it's next directed, and an idle-GC ticker can reclaim the process without losing the conversation. The inversion — the durable thing is the record, the process is the disposable accelerator — is what lets a cockpit "adopt-observe" a live session it didn't spawn and later take it over without a handoff.

### Migrating a Control Plane by Deleting It ([squz/ge](https://github.com/squz/ge), [marcelocantos/spyder](https://github.com/marcelocantos/spyder))
Retiring a subsystem is usually deferred indefinitely because the replacement is never *quite* proven. "Plateau P" gated the deletion on a decidable contract: each ged capability — tweaks, logs, state, screenshot, H.264 streaming — was re-implemented on spyder's app-channel and proven live against a real ge app across four launch media, with the streaming path verified end-to-end in headless Chrome (455K canvas pixels changing under injected input). Only then was the entire `ged/` daemon and React console **deleted outright** (−12,630 lines). The lesson is that a migration finishes when the old code is gone, not when the new code works — and the way to make deletion safe is to make each capability's parity a test that must pass first.

### A Renderer Backend Proven Reusable by a Second Title ([squz/esfera2](https://github.com/squz/esfera2))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md).*
### The Original App as a Live Oracle, Over UDP ([squz/yourworld](https://github.com/squz/yourworld))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md).*
### An Audit-Log You Can Reconstruct After the Fact ([marcelocantos/den](https://github.com/marcelocantos/den), and others)
Several repos gained a `docs/audit-log.md` this week — but the interesting move is that they were **reconstructed forensically from git history** rather than kept live from day one. This backfills the same governance surface (what security-relevant decisions were made, and when) onto repos that predate the practice, so the fleet's audit posture is uniform even for its older members. It is a small instance of a recurring pattern this period: making a practice retroactive so the whole fleet can be held to one standard rather than only its newest additions.

---

## Effort Estimate: Traditional vs. AI-Assisted

Breadth and shipping both unusually high. Commercial project detail: [private week 2026-07-12](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-12.md).

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| pigeon crypto remediation | 3-5 | Fixing an AES-GCM nonce-reuse race that lives in C (invisible to Go's race detector), then re-architecting per-flow AEAD channels via HKDF and adding a ZRTP-style commit-reveal — applied cryptography across Go/C/Swift/Kotlin with failing-then-passing repros. |
| jevons v0.5.0 cockpit + cost governance | 3-5 | A durable thread/process-as-cache orchestrator plus a real-time cost governor that must see off-book fleet spend, distinguish it from the owner's own, and kill runaways without false positives — born from a live money-loss incident. |
| ged→spyder Plateau P | 3-4 | Re-implementing an entire control plane (tweaks/logs/state/streaming) on a new transport, proving H.264 dev-video end-to-end in a browser, across four launch media, then deleting 12.6k lines of the predecessor safely. |
| Grok provider rollout (claudia + consumers) | 2-3 | A Task provider and a persistent Session provider over the Agent Client Protocol, hermetic fakes, registry wiring, and downstream adoption in jevons and mnemo. |
| bullseye four-tool API + governance | 2-3 | Collapsing a public MCP surface to four tools with structured envelopes and stable error codes, release-surface/ownership governance, and a TOCTOU-safe ID allocator, plus a tokio/SQLite build-perf rework. |
| esfera2 + yourworld2 sokol migration + oracle | 2-4 | Two renderer ports onto a shared backend at feature parity, validated by a UDP-mirror differential oracle spanning the legacy and ported apps. |
| multimaze2 store launch | 2-3 | A dual-store first launch — Play Billing + AAB signing + App Store submission assets — in one push. |
| mnemo hardening + issuepipe + den + crosshair | 2-4 | Audit hardening with a SQLite authorizer, a connection-preserving self-upgrade proxy, a new webhook-ingest service, a Mach-O bottle-relocation fix, and a hardened convergence executor. |

### The Diversity Tax

This week spans Go (jevons, mnemo, spyder, pigeon, claudia daemons), C/C++ (pigeon's libpigeon, sqlpipe, csp, ge), Objective-C++/Metal (ge, esfera2, yourworld), Rust (bullseye, crosshair), Swift/Kotlin/TypeScript SDKs (pigeon), C#/Unity (multimaze2, Minicades), OpenSCAD/Python (threedee), TLA+ (pigeon's method essays), plus applied cryptography, the Agent Client Protocol, StoreKit/Play Billing, WebCodecs H.264, SQLite internals, and cross-platform release engineering. No single engineer holds crypto remediation, ACP provider integration, control-plane migration, live cost-governance, and dual-store launch at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| pigeon / mnemo / crypto | 3-5 | Judging which audit findings are real, reviewing the AEAD re-architecture and SAS design, approving six pigeon releases. |
| jevons cost governance | 3-5 | Diagnosing the live token runaway, tuning kill-switch scope and guards so it doesn't over-kill, approving v0.5.0. |
| ged→spyder / ge / streaming | 3-5 | Validating H.264 streaming and input round-trip on real devices, blessing the ged deletion, control-plane review. |
| multimaze2 store launch | 2-4 | Store-submission judgement, screenshot/asset review, on-device Billing and launch testing. |
| Grok rollout / bullseye / games | 3-5 | Provider-integration review, API-shape decisions, esfera2/yourworld2 parity feel checks, convergence triage. |

### What If It Were One Person?

A single generalist would face both a ramp-up cost re-entering each domain — applied crypto, ACP, Metal rendering, StoreKit, Rust, Unity — and an unusually severe context-switching tax across a week that touched a store launch, a crypto campaign, a control-plane migration, and a provider rollout more or less simultaneously. The expert-days band (~16–28) understates the generalist total once those costs are added; the shipping density in particular (roughly a dozen releases plus a store submission) is what pushes the multiplier toward the top of its range.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~16-28 person-days (~0.8-1.4 months)** |
| Specialist team (traditional) | **~10-18 person-days (~0.5-0.9 person-months)** |
| Actual human effort this week | **~14-24 hours (~2-3.5 person-days)** |
| **Multiplier vs. generalist** | **~35-60x** |
| **Multiplier vs. specialist team** | **~20-35x** |

The multiplier runs highest on the pigeon crypto remediation — re-architecting per-flow AEAD channels and a commit-reveal SAS with verify-first repros is deep, silent-wrongness-sensitive work a lone generalist would take weeks to do safely — and on the jevons cost-governance package, where a live incident was turned into a decidable governor within days. It runs lowest on the fleet-wide bullseye.yaml migration and the MinicadesKit bumps. The human contribution concentrated on judgement a specification can't reach: which audit findings are real, how to scope a kill-switch so it fires on runaways but not on the owner, when a control plane is proven enough to delete, and the on-device store-launch and streaming verification no agent can perform.

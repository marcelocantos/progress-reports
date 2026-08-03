# Weekly Progress Report — 2026-05-18…24

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Excl-vendor landed lines: **+120,755/−30,812** (net **+89,943**).

## Executive Summary

Twenty-one repositories landed work this week across library infrastructure, game-engine ship plumbing, mobile device tooling, and mobile-game release engineering. The headline landed efforts are **marcelocantos/mnemo**, which shipped eight releases (v0.36.0–v0.43.0) building out a backup primitive plus periodic worker (🎯T61), an sqlift-mediated strict additive-only schema (🎯T49), eager-start workers at daemon boot (🎯T62), and a sweep of compactor/store hardening targets (🎯T53/T56/T59/T60/T63); **marcelocantos/spyder**, which shipped v0.35.0–v0.48.0 culminating in a tunnel daemon that self-heals on device-lifeline death (consuming an upstream go-ios fix), plus managed log-capture sessions with a math/big-free oslog parser (🎯T60), removal of the autoawake/KeepAwake supervisor (🎯T63), usbmuxd third-party-table wedge auto-recovery, and an observability pass; **squz/ge**, which lands the ship substrate's 🎯T64.2 fastlane/preflight followups (REPO_ROOT-as-superproject when consumed as a submodule, Homebrew-PATH preservation, source-vs-execute guards, app-identifier + API-key threading) and a mega-PR closing sixteen multimaze2-blocker targets at once (🎯T69 — audio pause/resume, per-edge safe-area accessors, lunasvg fingertip-tolerance hit testing, point-native `*InPts()` layout, IAP LocalStore mode, a long-press gesture detector), bracketed by IAP release preps v0.28.0–v0.30.0 (StoreKit 2 backend via a Swift bridge); and **marcelocantos/den**, which ships v0.11.0 with a `PackageProvider` abstraction making Homebrew one provider among many (🎯T23.1–T23.6) and a built-in process supervisor replacing launchctl (🎯T33). **marcelocantos/pigeon** lands a seven-target `/cv` fan-out (🎯T23/T25/T33/T35/T36/T37/T41) — macOS Keychain-backed identity, a Swift pairing-ceremony driver with Go↔Swift cross-language tests, Go↔C wire interop through a Go relay, an Android NDK build matrix for the Kotlin JNI AAR, a JVM-callback transport (C invokes Kotlin via JNI), a real ngtcp2 QUIC `PigeonTransport` for Swift, and a Unix-socket local backchannel — plus the 🎯T34 C-SDK foldings onto `cwire` and a 🎯T39.7 generic candidate-pair sub-FSM. **marcelocantos/csp** ships v0.15.0 + v0.16.0 prep with 🎯T3.4 context-aware stack-depth analysis, 🎯T23 per-protocol dist drop-ins (Phase A + B), and a convergence batch closing six targets and retiring four. **marcelocantos/sqlift** ships v0.15.0–v0.17.0 (`CREATE VIRTUAL TABLE` for fts5/fts3-4/rtree, bundled C++ source for cgo consumers, dropped unconditional `-lsqlite3`); **marcelocantos/sqldeep** ships v0.22.0 replacing the hand-written parser with the deepparser AST pipeline; **marcelocantos/bullseye** ships v0.29.0 (`bullseye_subdivide`); **marcelocantos/claudia** ships v0.12.0 (Grok PTT controls, system notes, history replay); **marcelocantos/jevons** lands voice-bridge hardening (claudia v0.12.0, FSM recovery, transcript-failure surfacing); **marcelocantos/go-ios** lands the upstream tunnel self-heal + DTX dispatch fix that spyder consumes. Commercial project detail: [private week 2026-05-24](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-05-24.md).

*Commercial executive-summary detail is in [private week 2026-05-24](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-05-24.md).*

**124 landed commits** | **+79,538 net landed lines**\* | **~7-10 person-days traditional equivalent** | **~30-50x multiplier**

\* *Landed lines are inflated by sqlift's +29,472 vendored SQLite C++ amalgamation. Hand-authored, merged source is on the order of +45-50k lines. In-flight work (rustuml's 203 commits, hms's 37) is excluded by design — see the In-Flight section and Metrics footnotes.*

### Major Achievements & Innovations

- **mnemo v0.36.0–v0.43.0 — backup primitive, additive-only schema, daemon-boot workers** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)) — eight releases land the data-durability and lifecycle layer: 🎯T49 an sqlift-mediated strict additive-only schema policy; 🎯T61 a backup primitive with a pre-migration snapshot (Phase 1) and a periodic backup worker + config + MCP tools (Phase 2); 🎯T62 eager-start of the default user's workers at daemon boot; 🎯T53 trees-of-interest references for parent-child overlap; 🎯T56 dropping the sqldeep dispatch from `Store.Query`; 🎯T59 driving the compactor off session activity rather than connections; 🎯T60 a stale `daemon_connections` sweep; 🎯T63 opt-in cost reconciliation; and 🎯T64.1 a vault-indexing-scope + `.mnemoignore` consent fix. The sqldeep dependency is bumped v0.19.0 → v0.22.0 to pick up the new parser.
- **spyder v0.48.0 — self-healing userspace tunnel** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — across v0.35.0–v0.48.0, the userspace tunnel daemon now self-heals when the device's RSD lifeline dies (consuming the upstream go-ios fix), preceded by 🎯T60 managed log-capture sessions backed by a `math/big`-free oslog parser, 🎯T63 ripping out the autoawake/KeepAwake supervisor (a go-ios upstream leak), usbmuxd third-party-table wedge auto-recovery, a `spyder doctor` + connection pool + DTX upstream fix, and an observability pass (wedge snapshots + MCP dispatch lifecycle + log-level audit). A sudoers entry bypasses PAM so the daemon's `sudo -n` succeeds.
- **ge 🎯T69 mega-PR — sixteen multimaze2 blockers + ship-substrate followups** ([squz/ge](https://github.com/squz/ge)) — one PR resolves sixteen multimaze2-blocker targets at once: audio engine-driven pause/resume for SDL audio devices, per-edge safe-area accessors, `hitTestSvgAt` lunasvg fingertip-tolerance hit testing, point-native layout renaming Context rect accessors to `*InPts()`, IAP LocalStore mode (`GE_IAP_MODE=local`), a Keychain entitlement cache for warm-start `owned()`, a `LongPressWatcher` hold-to-fire gesture detector, `RefreshRateBoost` during press, `Button` drift-in capture, `SkuMapping` per-product override, and `SessionConfig.orientation` honouring specific `kOrientation*` constants. The 🎯T64.2 ship-substrate gains a long tail of preflight/fastlane fixes (REPO_ROOT = superproject when consumed as a submodule, Homebrew-PATH-first, source-vs-execute guards, app-identifier + API-key env threading, `exportOptions.plist` written directly to override gym's export method, `setup_ci` for a non-interactive CI keychain). IAP release preps v0.28.0–v0.30.0 land the Apple StoreKit 2 backend via a Swift bridge (🎯T68), `SkuMapping` per-product override (🎯T67), and iOS/Android device log sinks (🎯T65/T66).
- **den v0.11.0 — PackageProvider abstraction + process supervisor** ([marcelocantos/den](https://github.com/marcelocantos/den)) — 🎯T23.1–T23.6 land the multi-provider package layer: a `PackageProvider` abstract interface, the Homebrew install/uninstall/list refactored to implement it, provider-resolution dispatch routing installs to the right provider, a manifest schema accepting provider-scoped entries, environment composition treating provider binaries uniformly with Homebrew kegs, and a stub non-Homebrew provider proving the seams are usable (T23 retired). 🎯T33 replaces the launchctl dependency with a built-in process supervisor.
- **csp v0.15.0 + v0.16.0 — context-aware stack analysis + per-protocol dist** ([marcelocantos/csp](https://github.com/marcelocantos/csp)) — v0.15.0 ships 🎯T3.4 context-aware stack-depth analysis (retired) + 🎯T23 Phase A per-protocol dist; the week then lands 🎯T23 Phase B (factory API + lint + CI subset matrix), a `scripts/vendor-deps.sh` for dist drop-in users, and a convergence batch closing T2/T5/T8/T25/T27/T28 and retiring T11/T12/T15/T16, with 🎯T26 narrowed to the scheduler wake race and Linux build portability fixes ahead of the v0.16.0 prep.
- **sqlift v0.15.0–v0.17.0 — virtual tables + cgo-friendly distribution** ([marcelocantos/sqlift](https://github.com/marcelocantos/sqlift)) — v0.15.0 adds `CREATE VIRTUAL TABLE` support (fts5, fts3/4, rtree); v0.16.0 bundles the C++ source inside the Go module so cgo consumers build without an external checkout; v0.17.0 drops the unconditional `-lsqlite3` from cgo LDFLAGS so consumers control their own SQLite link.
- **sqldeep v0.22.0 — deepparser AST pipeline replaces hand-written parser** ([marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep)) — the hand-rolled partial-parser is replaced by the vendored deepparser (Lemon LALR(1) grammar + visitable AST) pipeline, closing the latent-bug class where plain-SQL forms the old scanner didn't understand produced spurious errors.
- **bullseye v0.29.0 — `bullseye_subdivide`** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)) — 🎯T27.1 adds a `bullseye_subdivide` MCP tool for decomposing a target into sub-targets in one call, then retires the target shipped in the release.
- **claudia v0.12.0 — Grok PTT, system notes, history replay** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — push-to-talk controls, system-note injection, and conversation history replay land in the Grok client, with a STABILITY doc and the merge-commit hash recorded in the audit log.

### Significant Progress

- **pigeon seven-target /cv fan-out — cross-language transport + crypto** ([marcelocantos/pigeon](https://github.com/marcelocantos/pigeon)) — a single fan-out PR lands 🎯T23 (macOS Keychain-backed `crypto.Identity` for the echo backend), 🎯T25 (Swift pairing-ceremony driver + Go↔Swift cross-language test), 🎯T33 (Go-peer↔C-peer wire interop through a Go relay), 🎯T35 (Android NDK build matrix for the Kotlin JNI AAR), 🎯T36 (JVM-callback transport — C invokes a Kotlin `JniQuicTransport` via JNI), 🎯T37 (`Ngtcp2Transport` — a real QUIC `PigeonTransport` for Swift), and 🎯T41 (local Unix-socket backchannel between CLI and daemon). The 🎯T34 C-SDK foldings precede it — the pairing package folded onto `cwire.RunAcceptor`/`RunInitiator`, Stream/Datagram AEAD folded onto `cwire.Channel`, `api.go` activation onto libpigeon (T34 retired), cgo Connect + Listener wrappers in `cwire/`, libsodium vendored, and the C test loopback BSS shrunk — followed by 🎯T39.7's generic candidate-pair sub-FSM in `protocol/session.yaml`. The cgo amalgamation accounts for much of the repo's +17k landed lines.

### Tough Challenges Overcome

- **Self-healing a userspace tunnel whose device lifeline dies** (spyder / go-ios) — when the device's RSD lifeline drops, the userspace tunnel previously wedged; the fix detects the dead lifeline and tears down + re-establishes the tunnel daemon-side (landed upstream in go-ios, then consumed in spyder v0.48.0), plus a `dtx_codec` fix dispatching `ReadMessage` on `PayloadHeader.MessageType`. Pinned go-ios fork SHAs are tagged so rebases can't orphan them (🎯T70).
- **A write lock that survived a five-hour compactor silence — pre-emptive hardening** (mnemo) — the week's compactor/store work (🎯T59 driving the compactor off session activity, 🎯T56 dropping the sqldeep dispatch from `Store.Query`, 🎯T60 sweeping stale `daemon_connections`) tightened the read/write surface that, the following week, was traced to a write-lock held across a subprocess. The additive-only schema policy (🎯T49) and the backup primitive (🎯T61) make the whole store recoverable rather than fragile.
- **Cross-language transport parity across five runtimes** (pigeon) — the fan-out had to keep the wire format byte-identical while spanning C↔Kotlin (JNI callbacks both directions), Swift (ngtcp2 QUIC), and Go↔C (relay interop). Each binding is its own toolchain (Android NDK, JNI, ngtcp2, Keychain), and the only guarantee against silent divergence is the cross-language test corpus exercising the generated codecs end-to-end.
- **A clean seam for non-Homebrew package providers** (den) — making Homebrew one provider among many required lifting a `PackageProvider` interface with documented install/uninstall/list/binary-path contracts and a resolution dispatch that routes each install to the right backend — validated by a stub non-Homebrew provider so the abstraction is proven real before any second concrete provider exists.

### Contributors

- Marcelo Cantos

---

## Libraries & Infrastructure

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Backup + Schema + Lifecycle (21 commits)

- **The biggest effort of the week.** **Eight releases (v0.36.0–v0.43.0)**: as described in Major Achievements — 🎯T49 sqlift-mediated strict additive-only schema, 🎯T61 backup primitive + pre-migration snapshot (Phase 1) + periodic backup worker + config + MCP tools (Phase 2), 🎯T62 eager-start of the default user's workers at daemon boot, 🎯T53 trees-of-interest references for parent-child overlap, 🎯T56 sqldeep dispatch dropped from `Store.Query`, 🎯T59 compactor driven off session activity not connections, 🎯T60 stale `daemon_connections` sweep, 🎯T63 opt-in cost reconciliation, and 🎯T64.1 vault-indexing-scope + `.mnemoignore` consent fix.
- **Dependency + target maintenance**: sqldeep bumped v0.19.0 → v0.22.0; a 🎯T65 cross-session agent-to-agent messaging target filed; `bullseye.yaml` reconciled so T64.* parses (quoted acceptance lines). (The bitemporal two-law reconciliation rebuild — 🎯T68 — is in-flight this week and lands the following week; see the In-Flight section.)

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — v0.48.0 Self-Healing Tunnel (16 commits)

- **The biggest effort of the week.** **Self-healing tunnel + log capture (v0.35.0–v0.48.0)**: as described in Major Achievements and Tough Challenges — v0.48.0 self-heals the userspace tunnel on device-lifeline death (consuming the go-ios upstream fix), 🎯T60 managed log-capture sessions + a `math/big`-free oslog parser, 🎯T63 autoawake/KeepAwake supervisor removed, usbmuxd third-party-table wedge auto-recovery, a `spyder doctor` + connection pool + DTX upstream fix, an observability pass (wedge snapshots + MCP dispatch lifecycle + log-level audit), and a sudoers entry that bypasses PAM so `sudo -n` succeeds.
- **In-flight**: a devicectl/CoreDevice migration is on unmerged branches this week (12 in-flight commits) and is set aside the following week, superseded by the self-heal — see the In-Flight section.

### [marcelocantos/den](https://github.com/marcelocantos/den) — v0.11.0 PackageProvider (9 commits)

- **The biggest effort of the week.** **🎯T23 multi-provider package management**: as described in Major Achievements — `PackageProvider` abstract interface (🎯T23.1), Homebrew refactored to implement it (🎯T23.2), provider-resolution dispatch (🎯T23.3), provider-scoped manifest entries (🎯T23.4), uniform environment composition (🎯T23.5), and a stub non-Homebrew provider proving the seams (🎯T23.6, T23 retired).
- **🎯T33 process supervisor**: a built-in process supervisor replaces launchctl. v0.11.0 ships. Repo-state cleanup: bullseye Makefile, `.gitignore`, format pass.

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — v0.15.0 + v0.16.0 prep (8 commits)

- **The biggest effort of the week.** **Stack analysis + per-protocol dist + convergence batch**: as described in Major Achievements — 🎯T3.4 context-aware stack-depth analysis (retired) + 🎯T23 Phase A (v0.15.0), then 🎯T23 Phase B (factory API + lint + CI subset matrix), `scripts/vendor-deps.sh` for dist drop-in users, and a convergence batch closing T2/T5/T8/T25/T27/T28 + retiring T11/T12/T15/T16.
- **Targets + portability**: 🎯T26 narrowed to the scheduler wake race; 🎯T14 set aside; Linux build portability fixes; 🎯T3.10 (walker register provenance) and 🎯T28 (csp-flow SVG hygiene) filed; v0.16.0 release prep.

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) — Cross-Language Transport Fan-Out (8 commits)

- **The biggest effort of the week.** **Seven-target /cv fan-out 🎯T23/T25/T33/T35/T36/T37/T41**: as described in Significant Progress — Keychain-backed identity, a Swift pairing-ceremony driver, Go↔C wire interop via a Go relay, an Android NDK build matrix, a JVM-callback transport, a real ngtcp2 QUIC transport for Swift, and a Unix-socket local backchannel.
- **C-SDK foldings (🎯T34) + 🎯T39.7**: the pairing package folded onto `cwire.RunAcceptor`/`RunInitiator`; Stream/Datagram AEAD folded onto `cwire.Channel`; `api.go` activation onto libpigeon (T34 retired); cgo Connect + Listener wrappers in `cwire/`; libsodium vendored and the C test loopback BSS shrunk; a generic candidate-pair sub-FSM in `protocol/session.yaml`; live C SDK round-trips with protogen-driven wire formats.

### [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) — v0.15.0–v0.17.0 (6 commits)

- **Virtual tables + distribution**: `CREATE VIRTUAL TABLE` for fts5/fts3-4/rtree (v0.15.0); C++ source bundled in the Go module for cgo consumers (v0.16.0); unconditional `-lsqlite3` dropped from cgo LDFLAGS (v0.17.0). The bundled SQLite C++ amalgamation accounts for the repo's +29,472 lines — vendored, not authored.

### [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) — v0.22.0 deepparser Pipeline (3 commits)

- **AST pipeline cutover**: the hand-written parser is replaced with the deepparser AST pipeline (v0.22.0); deepparser bumped to a cleaned-up tip.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — v0.29.0 (2 commits)

- **🎯T27.1 `bullseye_subdivide`**: a one-call target-decomposition MCP tool ships in v0.29.0 and the target is retired.

### [marcelocantos/go-ios](https://github.com/marcelocantos/go-ios) — Tunnel Self-Heal (1 commit)

- **Upstream fix consumed by spyder**: `dtx_codec` dispatches `ReadMessage` on `PayloadHeader.MessageType` (the tunnel self-heal change is consumed by spyder v0.48.0).

---

## Game Projects

### [squz/ge](https://github.com/squz/ge) — T69 Mega-PR + Ship Followups (15 commits)

- **The biggest effort of the week.** **🎯T69 sixteen-blocker mega-PR + 🎯T64.2 ship followups + IAP release preps**: as described in Major Achievements — audio pause/resume, per-edge safe-area accessors, lunasvg fingertip-tolerance hit testing, point-native `*InPts()` layout, IAP LocalStore mode, a long-press gesture detector, `RefreshRateBoost`, `SkuMapping`, and `kOrientation*`-honouring orientation (🎯T36); a long tail of preflight/fastlane fixes (REPO_ROOT-as-superproject, Homebrew-PATH-first, source-vs-execute guards, app-identifier + API-key threading, direct `exportOptions.plist`, `setup_ci`); and IAP release preps v0.28.0–v0.30.0 (StoreKit 2 Swift bridge, per-product `SkuMapping`, iOS/Android device log sinks).
- **In-flight**: the CMake→Ruby-xcodeproj iOS builder (🎯T35) lands the following week (05-25); ge's prebuilt-vendor-header cutover is on worktree branches this week.

### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) — Unity Test Framework (8 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-05-24](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-05-24.md).*
### [minicadesmobile/kart-stars](https://github.com/minicadesmobile/kart-stars) — Ads + Gradle Migration (5 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-05-24](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-05-24.md).*
### [minicadesmobile/mopar-drag-n-brag](https://github.com/minicadesmobile/mopar-drag-n-brag) — 16 KB Page Size (5 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-05-24](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-05-24.md).*
### [squz/multimaze2](https://github.com/squz/multimaze2) — Pre-Ship Plumbing (5 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-05-24](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-05-24.md).*
## Tooling & Workflow

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — v0.12.0 Grok Controls (3 commits)

- **Grok PTT + system notes + history replay**: push-to-talk controls, system-note injection, and conversation history replay (plus a STABILITY doc) ship in v0.12.0; the merge-commit hash is recorded in the audit log.

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Voice-Bridge Hardening (3 commits)

- **Voice bridge hardening**: claudia v0.12.0 bump, FSM recovery, worker-note UI, transcript-failure surfacing; a voice overseer + FSM cleanup with an iOS / pigeon / auth backlog. (A `voicelab` desktop CLI is in-flight on an unmerged branch — see the In-Flight section.)

### [marcelocantos/skills](https://github.com/marcelocantos/skills) — Sync (2 commits)

- **Update skills from `~/.claude/skills`**: routine sync pushes.

### [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) — Weekly Report (1 commit)

- **Add weekly report 2026-05-11…17**: the previous period's main artefact.

---

## Other Game / Engine Repos

- **[squz/esfera2](https://github.com/squz/esfera2)** — detail in [private week 2026-05-24](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-05-24.md)
- **[minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit)** — detail in [private week 2026-05-24](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-05-24.md)
---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

This work exists only on feature/worktree-agent branches and has **not** merged to a default branch. It is reported here as a forward signal, deliberately kept out of the shipped metrics to avoid the cross-report double-counting that previously inflated totals (dev commits counted now, the eventual squash-merge counted again later).

- **rustuml** — 0 landed, ~203 commits in-flight on `strict-xml-parity-renderers` and ~18 `worktree-agent-*` branches: a strict-XML-parity push adopting verbatim oracle-replay across the diagram corpus (capturing and replaying the PlantUML oracle's root `<g>` body where the renderer can't yet reproduce byte-exact geometry), an embedded PlantUML `!theme` bundle, a grammatical SVG-path bounding-box parser, per-kind sequence/skinparam overrides, and a Latin-1/CJK width fallback. **This is exactly the work that merges the following week as rustuml v0.7.0** (~266 landed commits) — see the 05-25…31 report. Reported here as in-flight so it is counted once, on merge.
- **Health-Management-Systems/hms** — detail in [private week 2026-05-24](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-05-24.md)
- **spyder** — 12 commits in-flight: a devicectl/CoreDevice migration (typed CoreDevice wrappers, devicectl-primary enumeration with usbmuxd as a guarded supplement) that is **set aside the following week, superseded by the v0.48.0 self-heal** rather than merged.
- **squz/ge** — 7 commits in-flight on prebuilt-vendor and worktree-agent branches: the prebuilt-vendor-header cutover (lifted third-party headers), which lands the following week.
- **marcelocantos/pigeon** — 8 commits in-flight beyond the merged fan-out.
- **marcelocantos/csp** — 5 commits in-flight.
- **marcelocantos/mnemo** — 2 commits in-flight (the start of the 🎯T68 bitemporal reconciliation rebuild that lands next week).
- **marcelocantos/jevons** — 1 commit in-flight: a `voicelab` desktop CLI for iterating on Grok Realtime voice.
- **marcelocantos/ytt** — 1 commit in-flight: a `--json` output mode persisting the full API payload at ingest.

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits only. In-flight branch work is excluded by design (see the section above).*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | 21 |
| Total landed commits | 124 |
| Total in-flight commits (excluded) | 277 |
| Total lines added (landed) | +120,755\* |
| Total lines removed (landed) | −30,812 |
| Net new lines (landed) | +89,943\* |
| Authored net lines (estimate) | ~+45-50k |
| Languages | C++, Go, C, Swift, Kotlin, Objective-C++, Java, Ruby, C#, Markdown, YAML, SQL, shell |
| Contributors | 1 (Marcelo Cantos) |

\* *Landed line totals are inflated by sqlift's +29,472 vendored SQLite C++ amalgamation (bundled into the Go module, not authored) and a large share of pigeon's +17k (vendored libsodium + the cgo amalgamation). Hand-authored, merged source is on the order of +45-50k lines. The two largest in-flight efforts — rustuml (203 commits) and HMS2 (663-form transpiler output) — are excluded entirely.*

### Per-Repository Breakdown

| Repo | Commits (landed) | Files changed | Lines added | Lines removed | Net |
|------|------------------|---------------|-------------|---------------|-----|
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 21 | 86 | +5,839 | -1,940 | +3,899 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 16 | 220 | +8,999 | -4,880 | +4,119 |
| [squz/ge](https://github.com/squz/ge) | 15 | 117 | +8,789 | -699 | +8,090 |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 9 | 113 | +4,160 | -1,226 | +2,934 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 8 | 97 | +12,364 | -565 | +11,799 |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 8 | 142 | +17,055‡ | -6,342 | +10,713‡ |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 8 | 35 | +574 | -24 | +550 |
| [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) | 6 | 21 | +29,472† | -43 | +29,429† |
| [minicadesmobile/kart-stars](https://github.com/minicadesmobile/kart-stars) | 5 | 176 | +2,957 | -440 | +2,517 |
| [minicadesmobile/mopar-drag-n-brag](https://github.com/minicadesmobile/mopar-drag-n-brag) | 5 | 147 | +1,111 | -385 | +726 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 5 | 12 | +416 | -37 | +379 |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 3 | 8 | +263 | -29 | +234 |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 3 | 66 | +5,716 | -4,326 | +1,390 |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | 3 | 16 | +1,634 | -2,348 | -714 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 2 | 11 | +1,094 | -7 | +1,087 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 2 | 5 | +350 | -7 | +343 |
| [marcelocantos/go-ios](https://github.com/marcelocantos/go-ios) | 1 | 1 | +28 | -4 | +24 |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 1 | 22 | +3,262 | -1,303 | +1,959 |
| [squz/esfera2](https://github.com/squz/esfera2) | 1 | 1 | +20 | 0 | +20 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 1 | 1 | +24 | -4 | +20 |
| [minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit) | 1 | 1 | +24 | -4 | +20 |

†*sqlift +29,472 is the bundled SQLite C++ amalgamation, vendored not authored.*
‡*A large share of pigeon's +17k is vendored libsodium + the cgo amalgamation, not hand-authored.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [squz/ge](https://github.com/squz/ge) | ~120 | doctest cases across IAP, audio, layout, hit-test (landed only) |
| [marcelocantos/den](https://github.com/marcelocantos/den) | ~82 | doctest cases across PackageProvider seams |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~58 | Go tests incl. log-capture + connection pool |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~40 | Go tests for backup/worker/schema |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | ~40 | Go/Swift tests incl. cross-language interop |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~18 | per-protocol dist + convergence-batch cases |
| **Total** | **~358** | landed only; rustuml's worktree-branch tests are in-flight, not counted |

*Test counts are landed-only diff-grep estimates (added `+` lines matching test markers); they overstate where a test block was moved or reformatted.*

### Daily Activity

![Daily active repositories](daily-activity-2026-05-24.svg)

*(Daily landed-active-repo counts: Mon 5, Tue 12, Wed 11, Thu 5, Fri 7, Sat 2, Sun 8.)*

---

## Ideas & Innovations

### PackageProvider: Homebrew as One Provider Among Many ([den](https://github.com/marcelocantos/den))

den's environment manager was Homebrew-shaped throughout. The refactor lifts a `PackageProvider` abstract interface (install/uninstall/list/is-installed/binary-paths) and makes Homebrew just one implementation, with provider-resolution dispatch routing each install to the right backend and environment composition treating all provider binaries uniformly with Homebrew kegs. **The seam is validated by a stub non-Homebrew provider** — proving the abstraction is real before any second concrete provider is written.

### Additive-Only Schema as a Durability Contract ([mnemo](https://github.com/marcelocantos/mnemo))

mnemo's store had migrated schema freely, which makes rollback and backup semantics fuzzy. 🎯T49 routes all schema change through sqlift under a **strict additive-only policy** — columns and tables may be added but never dropped or narrowed — so an older binary can always read a newer database. Paired with the 🎯T61 backup primitive (a pre-migration snapshot plus a periodic worker), the store becomes recoverable by construction: every migration is forward-compatible, and every migration is preceded by a snapshot. The insight is that **a schema you can only extend is a schema you can always restore from**.

### JVM-Callback QUIC Transport via JNI ([pigeon](https://github.com/marcelocantos/pigeon))

Pigeon's transport abstraction now spans the C↔Kotlin boundary in both directions: a C peer can invoke a Kotlin `JniQuicTransport` via JNI callbacks (🎯T36), so the same protocol state machine drives a transport implemented in the JVM. Combined with a real ngtcp2 QUIC transport for Swift (🎯T37) and Go↔C wire interop through a Go relay (🎯T33), **the wire format is now exercised end-to-end across five language runtimes in cross-language tests** — the strongest possible guarantee that the generated codecs agree.

### Self-Healing a Tunnel Instead of Restarting It ([spyder](https://github.com/marcelocantos/spyder))

When a device's RSD lifeline dies, the naive response is to restart the whole daemon — losing every other device's session in the process. spyder v0.48.0 instead **detects the dead lifeline and tears down + re-establishes only the affected tunnel, daemon-side**, leaving the rest of the device pool untouched. The broader lesson the week reinforced (and that motivated setting aside the in-flight devicectl migration) is that a precise, scoped recovery beats a coarse rebuild: the self-heal made a wholesale adapter rewrite unnecessary.

### deepparser: A Real Grammar Beats a Hand-Written Partial Parser ([sqldeep](https://github.com/marcelocantos/sqldeep))

sqldeep had carried a hand-rolled partial-SQL scanner that silently mis-parsed any construct it hadn't been taught. v0.22.0 cuts the whole pipeline over to the vendored **deepparser** (a Lemon LALR(1) grammar with a visitable AST). The elegance is that the entire class of "the scanner didn't understand this valid SQL" bugs disappears at once — not patched case by case, but eliminated by adopting a grammar that parses the language properly. The transpiler now walks a real AST rather than guessing at token shapes.

---

## Effort Estimate: Traditional vs. AI-Assisted

*Commercial executive-summary detail is in [private week 2026-05-24](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-05-24.md).*

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| mnemo backup + schema + lifecycle | 3-5 | Additive-only schema policy, a backup/snapshot primitive, and compactor/store hardening are correctness-sensitive data-engineering with silent-wrongness risk. |
| ge T69 mega-PR + ship followups | 3-5 | Sixteen blocker targets spanning audio, hit-testing, layout, IAP, and gestures; fastlane + gym + App Store Connect + submodule-as-superproject path resolution is a notorious integration swamp. |
| pigeon transport fan-out | 3-5 | Five-language transport + crypto (Keychain, JNI, ngtcp2, NDK) with cross-language byte parity; each binding is its own toolchain. |
| spyder self-healing tunnel + log capture | 2-4 | Userspace-tunnel lifecycle recovery and a math/big-free oslog parser require deep iOS-device-protocol knowledge. |
| den PackageProvider + supervisor | 2-4 | A clean abstraction over package managers plus a process supervisor; moderate but careful. |
| csp stack analysis + per-protocol dist | 2-3 | Context-aware stack-depth analysis and linker-DCE per-protocol distribution; correctness-sensitive. |
| Releases (sqlift/sqldeep/bullseye/claudia) | 2-3 | Virtual-table support, an LALR(1) parser cutover, MCP tooling, Grok client controls. |
| Mobile game release plumbing | 1-2 | Unity gradle/ads/page-size compliance + a first Unity Test Framework harness. |

### The Diversity Tax

This week alone exercised: Go (mnemo, pigeon, spyder, sqldeep, den), C++ (ge, csp), C (pigeon SDK, libsodium, sqlift), Swift (pigeon transport, StoreKit bridge), Kotlin/JNI (Android transport), Objective-C++ (StoreKit), Java (JVM-callback transport), Ruby (ge ship scripts), C# (Unity games), plus fastlane/GHA/code-signing, SQLite virtual tables, LALR(1) grammar work, and Unity build engineering. No single engineer holds device-protocol recovery, five-language crypto bindings, App Store ship automation, and SQL grammar engineering simultaneously.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| ge / mobile ship | 5-8 | Release approvals, App Store Connect setup, on-device IAP and gesture checks. |
| spyder | 3-5 | Device-wedge reproduction, tunnel-recovery validation, the call to set aside the devicectl migration. |
| mnemo / den / csp | 4-6 | Architecture decisions on the schema policy and provider seam, PR review, convergence triage. |
| Everything else | 3-5 | Release approvals, parser-cutover sanity checks, cross-language test review. |

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~70-100 person-days (~3.5-5 months)** |
| Specialist team (traditional) | **~35-50 person-days (~1.8-2.5 person-months)** |
| Actual human effort this week | **~18-28 hours (~2.5-3.5 person-days)** |
| **Multiplier vs. generalist** | **~30-50x** |
| **Multiplier vs. specialist team** | **~15-25x** |

The multiplier is highest where the work is integration-heavy and well-specified (ship automation, release packaging, the package-provider seam) and lowest where it demands hardware-in-the-loop validation (spyder device wedges, on-device IAP testing) or strategic taste (the call to set aside the devicectl migration in favour of a scoped self-heal). The human contribution concentrates on architecture, on-device verification, and the calls that can't be derived from a spec. Note that the week's heaviest design work — rustuml's strict-XML parity and the HMS2 transpiler — sat in-flight and is not counted here; it lands the following week.

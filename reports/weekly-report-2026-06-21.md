# Weekly Progress Report — 2026-06-15…21

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Excl-vendor landed lines: **+39,558/−10,333** (net **+29,225**).

## Executive Summary

The heaviest week of the mid-June span: **twelve repositories** saw substantive landed work — spanning PlantUML layout reverse-engineering, MCP developer tooling, mobile-game engineering, iOS device automation, and C++ streaming concurrency — across **217 landed commits** with no Unity-regenerated inflation to discount. The dominant effort by a wide margin was **[marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)** (73 commits, +9,406 Rust), which stood up the *second-generation swimlane layout engine* ("swimlane-v2") for activity diagrams — connector lane-tagging infrastructure as the foundation, a `LaneMark` node variant with `lane_spans` emit-tracking, a port of the compress `shift_x/shift_y/x_bounds/y_max` transforms, if-class layout with per-lane `getMinMax` columns and `ON_X`, an if-branch cross-lane connector router, and N-branch fork-lane routing scaling from simple through six-branch (plus lane-delimited combos and nested swimlane fork workflows) — behind the new 🎯T4 release-freeze gate, alongside a long golden-parity tail across break/repeat/switch/elseif/fork geometry and Teoz. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** cut **v0.49.0 and v0.50.0** (12 commits, +7,737 Go): compaction-failure-ratio healing (🎯T77), a queryable TODO/Obsidian-Tasks ingestion index (🎯T78), a three-tier test architecture (🎯T73), a self-diagnostics suite with circuit-breaker, cross-session agent-to-agent inbox notes, and e2e de-flaking. **[marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)** cut **five releases (v0.31–v0.35)**: a GitHub issue mirror via `bullseye github sync` (🎯T34), CLI/MCP surface parity (🎯T36), a shape vocabulary and tail-aware subdivide (🎯T26/T27), `bullseye_resolve` with release-freeze awareness (🎯T29), and a self-documenting header (🎯T30). **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** shipped **v0.58.0/v0.59.0** — retiring `log_collect_*` so the app-channel is the only logging path and renaming `LOG_TARGET`→`SPYDER_APP_CHANNEL` — plus per-`(device, bundle_id)` app-channel listener auto-management with a `Session.Close` deadlock fix (🎯T83) and iOS-17+ tunnel-pending device supervision (🎯T84). **[marcelocantos/den](https://github.com/marcelocantos/den)** built its **v1.0.0 RC harness and publishing pipeline** with three bug fixes (🎯T73). **[marcelocantos/csp](https://github.com/marcelocantos/csp)** completed the **pull-based `io::source` streaming migration** — streaming HTTP/1.1 bodies through `io::source` and removing push-based `net::connection.input` outright (🎯T17.2/T17.5). Significant work sits **in-flight, unmerged** (reported separately): rustuml's next tranche (40 commits), mnemo (46), esfera2's WebGPU→ge reference-frame port (39), and HMS's transpiler corpus (68 commits, zero landed). Commercial project detail: [private week 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md).

**217 commits** | **~+39,558 / ~−10,333** (excl. vendor) | **~32-52 person-days traditional equivalent** | **~28-46x multiplier**

> Honesty note: unlike the fortnight before it, this week carries **no Unity-regenerated inflation** — the +43,898/−11,214 raw figure is close to genuine authorship. The only non-development deltas are **skills's +1,143/−329**, which is six automated `Update skills from ~/.claude/skills` syncs, and **progress-reports's +66/−43**, this repo's own output; **pigeon's +3,336/−4,699 (net −1,363)** is a real API rewrite whose churn on both sides is authored work, not blob noise. A tail of mechanical `ci: bump GitHub Actions to Node 24 majors` commits landed across mnemo, spyder, ge, csp, den, sawmill, sqldeep, sqlpipe, and others. Commercial project detail: [private week 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md).

### Major Achievements & Innovations

- **mnemo v0.49.0/v0.50.0 — compaction healing, TODO ingestion, three-tier tests** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)) — two releases. 🎯T77 heals the compaction failure ratio (JSON framing, deferred non-payloads, durable quarantine); 🎯T78 lands a queryable, manipulable Obsidian-Tasks TODO ingestion index and 🎯T80 extends TODO discovery to all known roots, not just git repos; 🎯T73 introduces a three-tier test architecture (`MNEMO_HOME`, an e2e harness, a snapshot helper); 🎯T79 makes the vault/compactor MCP tools fall back to the default user. Around them: a self-diagnostics suite with a circuit-breaker (and a summariser-cwd fix), cross-session agent-to-agent inbox notes, and e2e de-flaking (env-gated out of blocking CI, nightly coverage, race hardening).
- **bullseye v0.31–v0.35 — GitHub issue mirror + CLI/MCP parity** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)) — five releases. 🎯T34 mirrors targets to GitHub issues via `bullseye github sync` (🎯T37 renames the mirror IDs `GHI-<n>`→`GH<n>`); 🎯T36 brings the CLI and MCP surfaces to parity (github-sync and sync-priorities exposed as MCP tools); 🎯T26/T27 add a shape vocabulary and tail-aware subdivide; 🎯T29 adds `bullseye_resolve` and release-freeze awareness; 🎯T30 puts a self-documenting header on `bullseye.yaml`.
- **spyder v0.58.0/v0.59.0 — app-channel as the sole logging path + deadlock fix** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — v0.58.0 removes `log_collect_*` so the app-channel is the only logging path, and v0.59.0 renames `LOG_TARGET`→`SPYDER_APP_CHANNEL` to match. 🎯T83 auto-manages app-channel listeners per `(device, bundle_id)` and fixes a `Session.Close` deadlock; 🎯T84 surfaces tunnel-pending iOS-17+ devices, supervises the tunnel registry, and retries `TunnelInfoForDevice`.

### Significant Progress

- **rustuml — swimlane-v2 activity-layout engine + golden parity (73 commits, on master)** ([marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)) — the week's dominant effort: +9,406 Rust lines, −1,587, against the Java PlantUML reference, developing directly on master (no PR ceremony). This is where the **second-generation swimlane layout engine** lands: connector lane-tagging infrastructure as the foundation, a `LaneMark` node variant with `lane_spans` emit-tracking, a port of the compress `shift_x/shift_y/x_bounds/y_max` transforms plus `CompressionTransform::translate`, if-class layout (predicate routing + per-lane `getMinMax` columns + `ON_X`), an if-branch **cross-lane connector router**, title-overflow lane centring, and **N-branch fork-lane routing** scaling from simple through six-branch forks — with lane-delimited fork combos and nested swimlane fork workflows on top. Around it, a long tail of faithful golden parity across break corridors, repeat backward/break-body redistribution, switch `ON_Y` compression, `FtileForkInner` fork layout, elseif geometry, and Teoz named-box frames — roughly 60 goldens locked this week. A new 🎯T4 release-freeze gate blocks `/release` until zero golden failures; the oracle test-diagram generators were expanded and renamed.
- **multimaze2 — level-survivability solver + launch navigation (14 commits)** — detail in [private week 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md)
- **den — v1.0.0 RC harness + publishing pipeline (4 commits)** ([marcelocantos/den](https://github.com/marcelocantos/den)) — 🎯T73 builds the release-candidate harness and publishing pipeline for the dev-environment manager, together with three den bug fixes (+2,644 lines). A follow-up gates the supervisor shutdown-ordering test on service readiness, removing a startup race. (The v1 frontier checkpoints and blockers land in the following week's window — not claimed here.)
- **csp — completing the pull-based `io::source` streaming migration (5 commits)** ([marcelocantos/csp](https://github.com/marcelocantos/csp)) — 🎯T17.2/T17.5 stream the HTTP/1.1 body through the pull-based `io::source` abstraction and **remove push-based `net::connection.input` outright**, finishing the migration begun the prior week (+2,641/−885). Also lands a repo hygiene posture (a `hygiene.yaml` schema, a drift validator, and a fleet aggregator), archives the abandoned T3.7 HTTP/2 follow-up WIP, and bumps CI to Node 24.
- **stock-car-racing — Unity testing harness + Unity 6.4 CVE hotfix (61 commits)** — detail in [private week 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md)
### Tough Challenges Overcome

- **Proving every level still solvable after an engine rewrite** — detail in [private week 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md)
- **A Session.Close deadlock under per-device listener management** (spyder) — 🎯T83 auto-manages app-channel listeners keyed on `(device, bundle_id)` and, in doing so, resolves a `Session.Close` deadlock in the listener lifecycle — a concurrency hazard where the cost of silent wrongness is a hung session that takes the whole device automation path down.
- **A compaction pipeline that quietly lost payloads** (mnemo) — 🎯T77 heals the compaction failure ratio by fixing JSON framing, deferring non-payload records, and quarantining bad inputs durably rather than dropping them — turning a class of silent data loss in the transcript compactor into a recoverable, observable condition.
- **Byte-exact cross-lane connector routing against an undocumented Java engine** (rustuml) — reproducing PlantUML's swimlane connector geometry means routing arrows that cross lane boundaries while respecting each lane's independent `getMinMax` column extents; the if-branch cross-lane router and N-branch fork-lane routing (through six-branch) had to match the Java reference golden-by-golden with no specification to consult.

### Contributors

- Marcelo Cantos

---

## Tooling & Workflow

### [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) — Swimlane-v2 Layout Engine (73 commits)

**The biggest effort of the week, by a wide margin.** As described in Significant Progress — the second-generation swimlane activity-layout engine (lane-tagging foundation, `LaneMark` + `lane_spans` tracking, the compress transform port, per-lane `getMinMax` columns + `ON_X`, the if-branch cross-lane connector router, title-overflow lane centring, and N-branch fork-lane routing from simple through six-branch plus lane-delimited combos and nested swimlane forks), plus faithful golden parity across break/repeat/switch/elseif/fork geometry and Teoz named-box frames (≈60 goldens this week), the 🎯T4 release-freeze gate, and the oracle generator expand-and-rename. +9,406 Rust / −1,587. Develops on master with no PR ceremony.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Reliability Suite + TODO Ingestion (12 commits, 2 releases)

- **🎯T77/T78/T80/T79 healing + ingestion**: as in Major Achievements — compaction-failure-ratio healing (JSON framing, deferred non-payloads, durable quarantine), a queryable Obsidian-Tasks TODO index with discovery across all known roots, and default-user fallback for the vault/compactor MCP tools.
- **Reliability + tests**: a three-tier test architecture (🎯T73 — `MNEMO_HOME`, e2e harness, snapshot helper), a self-diagnostics suite with a circuit-breaker plus a summariser-cwd fix, and e2e de-flaking (env-gated out of blocking CI, nightly coverage, race hardening).
- **Collaboration**: cross-session agent-to-agent inbox notes for passing context between concurrent sessions.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Issue Mirror + Surface Parity (8 commits, 5 releases)

- **🎯T34/T36/T37**: as in Major Achievements — GitHub issue mirror via `bullseye github sync`, CLI/MCP surface parity (github-sync + sync-priorities exposed as MCP tools), and the `GHI-<n>`→`GH<n>` mirror-ID rename.
- **🎯T26/T27/T29/T30**: shape vocabulary + tail-aware subdivide, `bullseye_resolve` + release-freeze awareness, and a self-documenting header on `bullseye.yaml`. +3,893 Rust / −390.

### [marcelocantos/den](https://github.com/marcelocantos/den) — v1.0.0 RC Harness (4 commits)

- **🎯T73 RC harness**: as in Significant Progress — the release-candidate harness and publishing pipeline plus three bug fixes (+2,644), and a supervisor shutdown-ordering test gated on service readiness. (v1 frontier checkpoints and blockers land next window.)

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — Ingest Hardening (3 commits)

- **Robust playlist/channel ingest**: `--json` payloads, paced fetching, newest-first ordering, a spend-limit abort, and full-transcript JSON persistence; CI Node-24 bump.

### [marcelocantos/skills](https://github.com/marcelocantos/skills) · [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) · [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) · [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Routine Maintenance

- **skills** (6 commits): six automated `Update skills from ~/.claude/skills` syncs (+1,143/−329, auto-sync, footnoted). **sawmill / sqldeep / sqlpipe** (1 each): `ci: bump GitHub Actions to Node 24 majors` only.

### [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) — Report Tooling (3 commits)

- **Journey recast + length budgets**: recast the Journey section as an overview rather than an enumeration, add a sub-linear length budget for it, and cap report-entry lengths (re-compressing seven bloated weeks). This repo's own output, footnoted.

---

## Game Projects

### [squz/multimaze2](https://github.com/squz/multimaze2) — Survivability Solver + Launch Nav (14 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md).*
### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) — Testing Harness + Unity 6.4 Hotfix (61 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md).*
### [minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit) — Asmdef Isolation (6 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md).*
### [squz/ge](https://github.com/squz/ge) — App-Channel Logging Unification (3 commits)

- **🎯T119 fold dev logging into `SPYDER_APP_CHANNEL`**: iOS/Android parity with the ge lifecycle JNI exported; `appchannel` logs errno and applies a bounded retry around the spyder dial; CI Node-24 bump. +355 / −321.

### [minicadesmobile/mopar-drag-n-brag](https://github.com/minicadesmobile/mopar-drag-n-brag) · [minicadesmobile/kart-stars](https://github.com/minicadesmobile/kart-stars) — Fleet Plumbing

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md).*
### [squz/yourworld2](https://github.com/squz/yourworld2) · [squz/yourworld](https://github.com/squz/yourworld) — Housekeeping

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md).*
## Libraries & Infrastructure

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — App-Channel Logging + Deadlock Fix (5 commits, 2 releases)

- **🎯T83/T84 + v0.58.0/v0.59.0**: as in Major Achievements — `log_collect_*` retired so the app-channel is the only logging path, `LOG_TARGET`→`SPYDER_APP_CHANNEL`, per-`(device, bundle_id)` listener auto-management with a `Session.Close` deadlock fix, and iOS-17+ tunnel-pending device supervision (registry supervision + `TunnelInfoForDevice` retry). +1,408 Go / −1,218.

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Pull-Based Streaming Completion (5 commits)

- **🎯T17.2/T17.5**: as in Significant Progress — HTTP/1.1 body streamed through `io::source` with push-based `net::connection.input` removed outright, plus a repo hygiene posture (`hygiene.yaml` + drift validator + fleet aggregator), the archived T3.7 HTTP/2 WIP, and a Node-24 CI bump. +2,641 C++ / −885.

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) — Remote-Listen Relay Model (3 commits)

- **T45 relay collapse**: the relay L1 collapses to a remote-Listen model (`register`/`listen`/`connect`, per-client QUIC pipes), with the README, agent guide, and NOTICES realigned to the post-T45 API; CI Node-24 bump. +3,336/−4,699 (net −1,363, an API rewrite).

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

Reported as a forward signal; deliberately excluded from shipped metrics to avoid cross-report double-counting. The gather scan counts **217 in-flight commits** on unmerged branches this week — coincidentally matching the landed total.

- **Health-Management-Systems/hms** — detail in [private week 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md)
- **squz/esfera2** — detail in [private week 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md)
- **marcelocantos/mnemo** — 46 commits in-flight (+8,555/−764) beyond the merged releases.
- **marcelocantos/rustuml** — 40 commits in-flight (+3,804/−329): the next swimlane/parity tranche on worktree branches.
- **marcelocantos/pigeon** — 5 commits in-flight (+2,538/−3,766) beyond the merged T45 work.
- **Smaller in-flight tails across yourworld (9), bullseye (1), …** — detail in [private week 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md)
---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within the strict window 2026-06-15…21. In-flight branch work is excluded by design (see the section above).*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | 21; **12** with substantive work† |
| Total landed commits | 217 |
| Total in-flight commits (excluded) | 217 |
| Total lines added (landed) | +39,558 |
| Total lines removed (landed) | −10,333 |
| Net new lines (landed) | +29,225 |
| Authored net lines (estimate) | ~+31k (rustuml, mnemo, multimaze2, bullseye, stock-car, den, csp leading) |
| Languages | Rust, C++, Objective-C++, C, GLSL, Go, C#, Kotlin, Python, Markdown, YAML, JSON, shell |
| Contributors | 1 (Marcelo Cantos) |

†*The other 9 repos with landed commits had trivial or mechanical work: `Node 24` CI bumps (sawmill, sqldeep, sqlpipe), skills auto-sync, submodule-pointer / include-path bumps (kart-stars, mopar-drag-n-brag), `bullseye.yaml`-only or build-artifact-only touches (yourworld, yourworld2), and this repo's own report-tooling commits.*

*No Unity-regenerated inflation this week. The only non-development deltas in the line totals are **skills's +1,143/−329 auto-sync** and **progress-reports's +66/−43 self-output**; **pigeon's net −1,363** is a genuine relay API rewrite. Hand-authored merged source is ~+31k.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | 73 | 81 | +9,406 | −1,587 | +7,819 |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 61 | 192 | +4,123 | −930 | +3,193 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 14 | 62 | +6,073 | −340 | +5,733 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 12 | 107 | +7,737 | −273 | +7,464 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 8 | 55 | +3,893 | −390 | +3,503 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 6 | 23 | +1,143 | −329 | +814* |
| [minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit) | 6 | 27 | +267 | −38 | +229 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 5 | 28 | +2,641 | −885 | +1,756 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 5 | 40 | +1,408 | −1,218 | +190 |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 4 | 31 | +2,644 | −39 | +2,605 |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 3 | 67 | +3,336 | −4,699 | −1,363* |
| [squz/ge](https://github.com/squz/ge) | 3 | 23 | +355 | −321 | +34 |
| [minicadesmobile/mopar-drag-n-brag](https://github.com/minicadesmobile/mopar-drag-n-brag) | 3 | 8 | +351 | −33 | +318 |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 3 | 15 | +351 | −55 | +296 |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 3 | 5 | +66 | −43 | +23* |
| [minicadesmobile/kart-stars](https://github.com/minicadesmobile/kart-stars) | 2 | 5 | +8 | −6 | +2 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 2 | 3 | +8 | −21 | −13 |
| [squz/yourworld](https://github.com/squz/yourworld) | 1 | 1 | +81 | −0 | +81 |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 1 | 2 | +4 | −4 | +0 |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | 1 | 2 | +2 | −2 | +0 |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 1 | 1 | +1 | −1 | +0 |

\* *skills: auto-sync of `~/.claude/skills`; progress-reports: this repo's own report-tooling output; pigeon: net-negative because T45 is a relay API rewrite. (Files column is per-repo changed-file count.)*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | ≈60 goldens | golden-fixture parity across break/repeat/switch/elseif/fork + swimlane-v2 routing |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~40 (est.) | three-tier harness, self-diagnostics + circuit-breaker, compaction/TODO-ingest, e2e de-flake |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | ~25 (est.) | issue mirror, CLI/MCP parity, shape vocabulary + subdivide |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~12 (est.) | app-channel listener management, `Session.Close` deadlock regression, tunnel supervision |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | ~7 | Unity Test Framework + visual regression |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~5 (est.) | pull-based `io::source` streaming doctests |
| [marcelocantos/den](https://github.com/marcelocantos/den) | ~4 (est.) | RC harness + supervisor readiness-gated shutdown test |
| [squz/multimaze2](https://github.com/squz/multimaze2) | ~2 | solver / survivability |
| **Total** | **~95 tests (+≈60 goldens)** | landed only; estimates are conservative diff-grep counts; in-flight tests not counted |

### Daily Activity

![Daily active repositories](daily-activity-2026-06-21.svg)

*(All-repo active-repository counts per day across the week, from the timeline cache — a broad activity signal counting all authors and all branches, so it runs higher than landed Marcelo-only work and spikes on branch-merge days. Plotted: Mon 06-15 5, Tue 2, Wed 1, Thu 6, Fri 5, Sat 06-20 13, Sun 06-21 24. Landed Marcelo-only work concentrated on the 06-20/21 weekend, when rustuml's swimlane-v2 tranche and the mnemo/bullseye release stretch merged.)*

---

## Ideas & Innovations

### A Solver as a Level-Survivability Oracle ([multimaze2](https://github.com/squz/multimaze2))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md).*
### Mirroring the Target Graph to GitHub Issues ([bullseye](https://github.com/marcelocantos/bullseye))
Convergence targets live in `bullseye.yaml`, which is legible to the agent but invisible to collaborators who work out of GitHub issues. bullseye's 🎯T34 adds `bullseye github sync`, which **mirrors the target graph into issues while keeping `bullseye.yaml` the single source of truth** — the issues are a projection, not a second master, so there is no bidirectional-sync ambiguity to resolve. 🎯T36 then brings the CLI and MCP surfaces to parity (exposing github-sync and sync-priorities as MCP tools), so an agent and a human driving the same workflow reach for the same operations. The insight is that a planning tool earns adoption by *meeting people where they already look*, without surrendering its authoritative store.

### Lane-Tagging as the Foundation for Cross-Lane Routing ([rustuml](https://github.com/marcelocantos/rustuml))
PlantUML's swimlane activity layout is an undocumented Java engine, and connectors that cross lane boundaries are its hardest geometry — each lane computes its own `getMinMax` column extents, yet arrows must thread between them faithfully. swimlane-v2's design move is to **tag every connector with its lane provenance first** (the `LaneMark` node variant and `lane_spans` emit-tracking) and only then route: predicate-routed if-class layout builds per-lane MinMax columns with `ON_X` occupancy, and the cross-lane connector router consumes the tags to place arrows that respect each lane's independent extents. With that foundation in place, N-branch fork-lane routing scales cleanly from simple through six-branch forks and lane-delimited combos — the same tagging machinery carrying every fork width without special cases per branch count.

### Finishing the Job: Deleting the Push Path ([csp](https://github.com/marcelocantos/csp))
The prior week introduced a pull-based `io::source` alongside the existing push-based `net::connection.input`; running both is where subtle bugs breed, because two flow-control models coexist and every layer must decide which it speaks. 🎯T17.2/T17.5 close this out by streaming the HTTP/1.1 body through `io::source` and then **removing `net::connection.input` outright** — the push path is gone, not merely deprecated. The discipline is worth naming: a migration is only safe once the old mechanism is *deleted*, so no code can silently fall back to it and no reviewer has to remember which model a given call site uses. Back-pressure now falls out of one abstraction rather than being reconciled between two.

### Isolating Game Code So Tests Can Reach It ([stock-car-racing](https://github.com/minicadesmobile/stock-car-racing))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md).*
### Healing a Failure Ratio Instead of Dropping Payloads ([mnemo](https://github.com/marcelocantos/mnemo))
mnemo's transcript compactor was losing a measurable fraction of records to malformed framing — a silent data-loss condition that only surfaces as a degraded failure ratio. 🎯T77's fix is threefold and worth distinguishing: correct **JSON framing** so well-formed records parse, **deferral of non-payload records** so metadata doesn't masquerade as content, and **durable quarantine** of genuinely bad inputs so they are set aside rather than discarded. The last point is the key idea — a pipeline that quarantines is recoverable and observable, whereas one that drops is neither; you can re-examine a quarantine, but a dropped payload is gone.

---

## Effort Estimate: Traditional vs. AI-Assisted

*Commercial executive-summary detail is in [private week 2026-06-21](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-06-21.md).*

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| rustuml swimlane-v2 + parity | 8-12 | Byte-exact reverse-engineering of PlantUML's undocumented swimlane/activity layout algorithm (lane MinMax columns, cross-lane connector routing, N-branch fork lanes through six-branch) against a Java reference, validated golden-by-golden. |
| mnemo reliability suite + ingestion | 5-7 | Compaction-failure healing with durable quarantine, a queryable Obsidian-Tasks index, a three-tier test architecture, a self-diagnostics circuit-breaker, and e2e de-flaking — concurrency and observability depth where silent regressions lose data or heat the machine. |
| multimaze2 solver + launch nav | 4-6 | A from-scratch 2,527-line headless geometric solver as an independent survivability oracle, plus packs→levels navigation, slide transitions, and procedural-SVG menu chrome — App-Store-review-sensitive correctness. |
| bullseye five-release run | 3-4 | A GitHub issue mirror as a one-way projection of the target graph, CLI/MCP surface parity, a shape vocabulary with tail-aware subdivide, and release-freeze-aware resolution. |
| stock-car testing harness + Unity 6.4 hotfix | 3-5 | An asmdef-isolation refactor that makes a shipping Unity game testable without breaking it, a visual-regression system, a CVE hotfix upgrade, and an ad-SDK/plugin-meta migration. |
| csp pull-based streaming completion | 2-4 | Streaming the HTTP/1.1 body through `io::source` and deleting the push-based `net::connection.input` entirely — silent-wrongness risk on the streaming/TLS surface, resolved by removing the fallback. |
| spyder app-channel + deadlock fix | 2-4 | Unifying logging onto the app-channel, per-`(device, bundle_id)` listener auto-management with a `Session.Close` deadlock fix, and iOS-17+ tunnel-registry supervision — iOS platform-protocol depth and concurrency. |
| den v1.0.0 RC harness | 2-3 | A release-candidate harness and publishing pipeline with three bug fixes and a readiness-gated supervisor-shutdown test — release engineering with a wide correctness surface. |
| pigeon relay collapse | 2-3 | Collapsing the relay L1 to a remote-Listen model (`register`/`listen`/`connect`, per-client QUIC pipes) — a net-negative API rewrite with doc/NOTICES realignment. |
| ge / ytt / minicades fleet | 2-4 | App-channel logging unification with lifecycle JNI export, ingest hardening, asmdef isolation, and Unity fleet plumbing. |

### The Diversity Tax

This week alone spans Rust (rustuml's layout engine, bullseye), C++ and GLSL (multimaze2's solver, csp streaming), Objective-C++ and C (ge app-channel), Go (mnemo, spyder, den, pigeon, ytt), C# and Unity lifecycle (stock-car-racing, Minicadeskit), plus the iOS lockdown/app-channel surface, QUIC relay design, PlantUML reverse-engineering, and StoreKit-adjacent launch correctness. No single engineer holds PlantUML-layout reverse-engineering, concurrent-daemon observability, iOS device-automation protocol work, geometric puzzle-solving, and Unity test-harness bring-up at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| rustuml | 4-7 | Steering the swimlane-v2 port, judging golden diffs, deciding replicate-vs-approximate on undocumented lane/fork layout behaviour. |
| mnemo / bullseye / den | 4-6 | Diagnosing the compaction failure ratio on live data, release review and approvals (mnemo two, bullseye five), target-graph and issue-mirror triage, RC-harness review. |
| multimaze2 / stock-car | 3-5 | Level-solver spot checks, on-device play-testing, Unity 6.4 upgrade validation, visual-regression baseline judgement. |
| spyder / csp / pigeon | 3-6 | iOS device testing, the deadlock reproduction, streaming-migration design review, relay-model API decisions. |

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~32-52 person-days (~1.6-2.6 months)** |
| Specialist team (traditional) | **~18-30 person-days (~0.9-1.5 person-months)** |
| Actual human effort this week | **~14-24 hours (~2.5-4 person-days)** |
| **Multiplier vs. generalist** | **~28-46x** |
| **Multiplier vs. specialist team** | **~14-22x** |

The multiplier runs highest on rustuml — reverse-engineering an undocumented Java swimlane-layout engine into Rust golden-by-golden is exactly the cross-domain-recall-and-search task where the AI dominates — and on mnemo's reliability suite, where the fix surface (compaction framing, quarantine, three-tier tests) is broad and fiddly. It runs lowest on the Node-24 CI bumps, the skills auto-sync, and the Unity version-code churn. The human contribution concentrated on judgement a specification can't reach: which PlantUML behaviours to replicate, the solver-as-oracle split, the migrate-by-deletion discipline in csp, the deadlock reproduction in spyder, and on-device ship validation across the mobile fleet.

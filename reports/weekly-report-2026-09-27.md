# Weekly Progress Report — 2026-09-21…27

## Executive Summary

**Fourteen repositories** landed **354 commits** — the heaviest landed week of the series by commit count. Almost everything else orbits **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** (197 commits, v0.42.0–v0.44.0): an **OMP sidecar** for subscription providers, **broker-admitted Task runs**, plan credentials sealed out of Keychain argv, and **Claudia-owned seat migration** with per-seat provider policy. **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** (37 commits, v0.88–v0.95) shipped **`spyder verify`** — daemon-wide DAG workflows with live dashboard gates and unattended owner replay. **[marcelocantos/sentinel](https://github.com/marcelocantos/sentinel)** (27 commits, initial) is a never-ending host-health loop that runs each check as a broker-admitted restricted task. **[marcelocantos/serviceboard](https://github.com/marcelocantos/serviceboard)** (10 commits, initial) is a loopback Supervisor/Homebrew dashboard. **[marcelocantos/finance](https://github.com/marcelocantos/finance)** landed a dual-stream mid-cycle ledger with persistent transfer identification. **[squz/ge](https://github.com/squz/ge)** finished source-only cook and ledger-enforcement gates. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** made `/health` answer in ~2 ms from the scheduler snapshot (🎯T181). **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** landed **zero** this week — the migration/OMP consumer work is a large in-flight train. **[squz/multimaze2](https://github.com/squz/multimaze2)** (21 commits, Classic key) plus HMS/stock-car in-flight: [private week 2026-09-27](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-09-27.md).

**354 commits** | **+48,347 net lines** | **~70-110 person-days traditional equivalent** | **~30-55x multiplier**

> Honesty note: **new `data/line-excludes.yaml` globs this run** — `marcelocantos/skills` `skills/synced/**` (third-party Anthropic/office skill trees and ISO OOXML XSDs copied by skill sync; ~+79k this week). Headline ☲ is gather `landed:` after that glob (**+54,770/−6,423**). Excluded bulk this week **+83,171/−469**.

### Major Achievements & Innovations

- **OMP sidecar + sealed plan credentials** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.42–v0.44) — subscription providers route through pinned pi-agent-core; Bash/Read/Write/Glob/Grep advertised on OMP seats; plan blob in an encrypted file not Keychain argv; one Keychain read/write per process; ACL sealed to the product broker; login refresh when xAI rejects the access token.
- **Broker-admitted Task runs** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — restricted tasks for Sentinel; background admission against published model capacity; model selection reported in the task stream; failures streamed to unattended callers; tasks can require the standalone broker.
- **Claudia-owned seat migration** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) 🎯T691) — live and stopped-seat handover with retained successor session identity; per-seat provider placement policy; refuse stale-provider adoption; preserve active sidecar turn on a busy prompt; jevons delegates destination handover (in-flight consumer).
- **`spyder verify`** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) v0.88–v0.95) — daemon-wide DAG workflows, live WebSocket dashboard with data-URI screenshots, model-reviewed Verify runs with retained definitions, unattended preparation and owner replay, fleet battery history tab.
- **Sentinel** ([marcelocantos/sentinel](https://github.com/marcelocantos/sentinel), initial) — five-minute host-health loop; each turn is a broker-admitted restricted task; bounded Supervisor/health-port probes; Jevons API+Playwright layers; blurter alerts only after two distinct failed observations plus an intervening review.
- **mnemo `/health` in ~2 ms** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) 🎯T181, v0.101–v0.106) — serve from the scheduler snapshot; compression status on indexes; no live `compress.backfill` query on the health path.
- **finance dual-stream ledger** ([marcelocantos/finance](https://github.com/marcelocantos/finance)) — mid-cycle history load, persistent transfer identification, controlled journal categories; parsers/reconcile/migrate with a real fixture corpus.

### Significant Progress

- **ge source-only cook closed** ([squz/ge](https://github.com/squz/ge) 🎯T190–🎯T201) — vendor SDL cook on demand; AccelSynth parity oracles are functions of their input; refuse bullseye filings that never reach master; killed SDL cook wedges filed.
- **serviceboard** ([marcelocantos/serviceboard](https://github.com/marcelocantos/serviceboard), initial) — loopback Supervisor/Homebrew dashboard with search keyboard nav, official logos, focused live updates.
- **vellum viewer polish** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum) v0.20–v0.23) — parchment favicon; checkbox click-target only; focus preserved across reload via toggle stamp; one kqueue machine per viewed path.
- **ytt requires the broker** ([marcelocantos/ytt](https://github.com/marcelocantos/ytt) v0.15–v0.17) — analyze path requires jevons-broker; background Resolve for synopses; exhausted capacity is a quiet deferral.
- **csp subset-link / move-only sends** ([marcelocantos/csp](https://github.com/marcelocantos/csp)) — deferred move-only sends; macOS subset-link arm that actually tests DCE (🎯T63).
- **bullseye incremental ID-history** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) v0.57.0) — on-disk cache for git ID-history scans (🎯T92).

### Tough Challenges Overcome

- **Plan tokens in process argv** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — Keychain items and sidecar env were leaking plan material into inspectable surfaces; encrypted file store, argv scrub, ACL sealed to the product broker, one read/write per process.
- **Migration that orphans the successor** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) / jevons in-flight) — adopting a stale source after broker migration, or parking when destination health is incomplete, left seats on the wrong provider; handover is Claudia-owned with retained session identity and per-seat policy.
- **`/health` that waited on the packer** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) 🎯T181) — the query was 0.12 s; the wait was the problem. Snapshot serve + indexed compression status → ~2 ms; full pass runs when startup finishes, not on every GET.
- **Verify that sampled the app into the dashboard** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — dashboard frames were stealing app frames; Verify keeps the dashboard off the sample path; apps stop on every exit and idle timeout.

### Contributors

- Marcelo Cantos (AI co-authors — Claude, Grok, Cursor, Codex — on trailers throughout; claudia OMP/migration and spyder verify were largely the supervised fleet).

---

## Agent & Fleet Infrastructure

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — OMP, Task, Migration (197 commits, v0.42.0–v0.44.0)

**The biggest effort of the week — and of most weeks.** 599 file changes, **+23,772/−2,317**. **~364 new `func Test` additions** (gross).

- **OMP sidecar**: route subscription providers through pinned pi-agent-core; tool advertise; seat workdir for tools; dated spool without HFS compression; Bun process kept across bounces; provider-local model before sidecar start; plan startup returned to Claudia.
- **Credentials**: plan blob encrypted file; Keychain ACL; no tokens in argv; refresh expired logins; update item in place; disposable Keychain in recovery tests.
- **Broker Task**: restricted runs for Sentinel; background capacity admission; stream model selection and failures; require standalone broker; Codex tasks in non-Git workdirs; Grok tool-call relay for host audit.
- **Migration (🎯T691)**: live/stopped handover; per-seat provider policy; retain OMP successor identity; refuse stale-provider adoption; preserve busy sidecar turn; migration permissions persisted.
- **Judge / intel**: typed Judge mode answered by Jev with full distributions (🎯T127); held-out citation discipline.
- **Operator**: re-claim after detach; grant ownership in status; force-release (🎯T124).

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Verify Workflows (37 commits, v0.88.0–v0.95.0)

171 file changes, **+9,414/−668**. **~80 new tests**.

- **`spyder verify`**: daemon-wide DAG; WebSocket live dashboard; data-URI screenshots; reports for completed runs; model-reviewed runs with retained definitions; unattended prep + owner replay; PATH-shadowing version check; graceful iOS terminate before kill.
- **Battery**: fleet history + Battery tab; short names; stable plot width; charge icons from native diagnostics.
- **Device**: hybrid smoke transport for LLM-driven release checks; reachable app-channel host for physical devices; deploy descendants on verification resume.

### [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) — Host Health Loop (27 commits, initial)

131 file changes, **+4,475/−1,221**. **~48 new tests**.

- `sen --serve` / `--check`; personal `~/.local/share/sen/` with MEMORY.md addendum; broker-admitted restricted tasks; bounded Supervisor + health-port probes; Jevons API probe + Playwright UI smoke; blurter alert after two failed observations + review; LaunchAgent install path.

### [marcelocantos/serviceboard](https://github.com/marcelocantos/serviceboard) — Local Service Dashboard (10 commits, initial)

- Loopback-only Supervisor/Homebrew dashboard; search keyboard nav; official logos; focused live Supervisor events + Homebrew poll; registration protocol for per-service origins.

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — Broker-Required Analyze (12 commits, v0.15.0–v0.17.0)

- Speak the running daemon; Resolve picks the model; refuse overspent synopsis providers; background resolution; analyze requires jevons-broker (🎯T33); exhausted capacity is quiet deferral.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Health Snapshot (13 commits, v0.101.0–v0.106.0)

- 🎯T181: `/health` from scheduler snapshot (~2 ms); compression aggregates indexed; packer/source_state follow-ups filed; `~/.jevons/spool` indexed older-first with ditto of closed days after drain+checkpoint.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — ID-History Cache (5 commits, v0.57.0)

- Incremental git ID-history scans with on-disk cache (🎯T92); refused writes on achieved rows must not report no-change; `commit --op assign` accepts documented `--owner`.

### [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) — Supervisor (1 commit)

- Run mcpbridge daemon under Supervisor.

### [marcelocantos/skills](https://github.com/marcelocantos/skills) — Sync Hygiene (3 commits)

- Update from `~/.claude/skills` (synced office trees excluded from ☲); remove retired `target` and `vcheck` skills. **+45/−871** after exclude.

---

## Libraries & Infrastructure

### [marcelocantos/finance](https://github.com/marcelocantos/finance) — Dual-Stream Ledger (2 commits)

**New personal ledger.** 56 file changes, **+5,651/−63**.

- Dual-stream mid-cycle history; persistent transfer identification; controlled categories for journal postings; parsers/reconcile/migrate/audit; statement fixtures across ANZ/CBA/NAB; docs/dual-stream.md.

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Subset-Link / Move-Only (1 commit)

- Deferred move-only sends; NOTICE/part-doc oracles; macOS subset-link arm that tests dead-code elimination (🎯T63). **+1,181/−39**.

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — Viewer Focus (10 commits, v0.20.0–v0.23.0)

- Parchment-and-ink favicon; toggle only when the checkbox is clicked; focus preserved via toggle stamp after reload; one kqueue watch machine per viewed path.

---

## Game Engine

### [squz/ge](https://github.com/squz/ge) — Cook + Ledger Gates (15 commits)

- Source-only cook (🎯T190); NDK glob (🎯T191); AccelSynth parity oracles as functions of input (🎯T198); refuse filings that never reach master (🎯T200); fail standing invariants when master's unit suite is red; killed SDL cook wedge filed (🎯T201).


## Commercial

**[squz/multimaze2](https://github.com/squz/multimaze2)** (21 commits) closed Classic key/door solvability under a physics oracle — full narrative in [private week 2026-09-27](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-09-27.md). HMS2 checkpoint-history / layout-parity and stock-car 3.26 Verify/smoke trains: same private companion.

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **marcelocantos/jevons** — large in-flight migration/OMP consumer train (gather ~383); Claudia-owned handover, retire Jevons-owned broker executable, fleet policy controls. Detail belongs with next land.
- **Health-Management-Systems/hms** — heavy in-flight (gather inflated by a checkpoint-history branch of ~500 semantic oracles); layout-parity continues. Private companion.
- **minicadesmobile/stock-car-racing** — 3.26 Verify/smoke/repair/Derby owner gates; private companion.
- **squz/yourworld2** — ~20 in-flight; **marcelocantos/finance** — 34 in-flight beyond the two landed; **marcelocantos/claudia** — 14 in-flight; **arr-ai/arrai** corpus programme still branched.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-09-21…27. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **14** |
| Total landed commits | **354** |
| Total lines added (landed, filtered) | +54,770‡ |
| Total lines removed (landed, filtered) | −6,423‡ |
| Net new lines (landed, filtered) | +48,347‡ |
| File changes | 1,279 |
| New files created | ~1,004 |
| Bulk paths excluded from ☲ | +83,171 / −469 (skills/synced OOXML + lockfiles/bullseye.yaml + standing globs) |
| Releases published | **~25** (claudia v0.42–v0.44, spyder v0.88–v0.95, mnemo v0.101–v0.106, vellum v0.20–v0.23, ytt v0.15–v0.17, bullseye v0.57.0) |
| Languages | Go, Python, C++, JavaScript, HTML, CSS, YAML, Markdown, Shell, SQL |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. **New this run:** `marcelocantos/skills` `skills/synced/**`.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 197 | 599 | +23,772 | −2,317 | +21,455 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 37 | 171 | +9,414 | −668 | +8,746 |
| [marcelocantos/finance](https://github.com/marcelocantos/finance) | 2 | 56 | +5,651 | −63 | +5,588 |
| [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) | 27 | 131 | +4,475 | −1,221 | +3,254 |
| [marcelocantos/serviceboard](https://github.com/marcelocantos/serviceboard) | 10 | 42 | +2,917 | −104 | +2,813 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 21 | 55 | +2,046 | −543 | +1,503 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 13 | 44 | +1,488 | −138 | +1,350 |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 10 | 55 | +1,467 | −142 | +1,325 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 1 | 21 | +1,181 | −39 | +1,142 |
| [squz/ge](https://github.com/squz/ge) | 15 | 30 | +1,051 | −78 | +973 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 5 | 10 | +651 | −93 | +558 |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 12 | 48 | +489 | −146 | +343 |
| [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) | 1 | 6 | +123 | −0 | +123 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 3 | 11 | +45 | −871 | −826* |

\* *After excluding `skills/synced/**` (+79,029 excluded); net negative from removing retired target/vcheck skills.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~364 gross | OMP, Task, migration, Keychain ACL, Judge |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~80 | Verify DAG, dashboard, release gates |
| [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) | ~48 | broker admission, probes, alert state |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~35 | T181 health snapshot / indexes |
| [marcelocantos/finance](https://github.com/marcelocantos/finance) | parsers/reconcile/transfers | fixture corpus |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | ~13 | checkbox focus / kqueue |
| [squz/multimaze2](https://github.com/squz/multimaze2) | physics oracle | Classic key solvability |
| [squz/ge](https://github.com/squz/ge) | cook/parity oracles | AccelSynth input-function |
| **Total** | **~540+ gross** | landed only |

### Daily Activity

![Daily active repositories](daily-activity-2026-09-27.svg)

*(Active repositories per day: Mon 09-21 8, Tue 09-22 4, Wed 09-23 5, Thu 09-24 3, Fri 09-25 5, Sat 09-26 4, Sun 09-27 6.)*

---

## Ideas & Innovations

### The Sidecar Owns the Subscription ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
Direct provider processes and Keychain argv made plan material inspectable and login refresh a host ritual. **OMP seats run through a pinned sidecar with advertised host tools; the plan blob is an encrypted file; Keychain is sealed to the product broker with one read/write per process.** Refresh is a login verb, not a second writer race.

### A Task Is an Admitted Turn ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) / [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel))
Unattended health checks that mint their own seats fight the fleet for capacity. **Broker Task admits against published remaining; restricted tool surfaces; failures stream to the caller; exhausted capacity defers without a noisy fake green.** Sentinel's five-minute loop is a consumer of admission, not a second broker.

### Migration Is a Grant Handover ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
Provider switches that stop the seat and rewrite the registry row orphan context. **Claudia owns the handover: retain successor session identity, honour per-seat provider policy, refuse stale-provider adoption, preserve a busy sidecar turn.** The consumer reports pending failures; it does not invent a cold start.

### Verify Is a DAG, Not a Script ([marcelocantos/spyder](https://github.com/marcelocantos/spyder))
Release smoke that samples the dashboard into the app under test lies. **`spyder verify` is a daemon-wide DAG with retained model-reviewed definitions, live WebSocket gates, and unattended owner replay** — apps stop on exit; the dashboard does not steal frames.

### Health Is a Snapshot ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo))
A correct aggregate that waits on the packer is still an unavailable health endpoint. **Serve `/health` from the scheduler's last snapshot; index the aggregates; run the full pass when startup finishes.** ~2 ms is the contract; 0.12 s queries that block behind a writer are not.

---

## Effort Estimate: Traditional vs. AI-Assisted

An infrastructure week with three new products (sentinel, serviceboard, finance ledger) under a 197-commit claudia OMP/migration train — the diversity tax is the story.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| claudia OMP/Task/migration/credentials (v0.42–v0.44) | 20-32 | Sidecar lifecycle; Keychain ACL; broker Task protocol; live+stopped migration with retained identity; Judge distributions. |
| spyder verify + battery (v0.88–v0.95) | 8-12 | Daemon DAG; device/WebSocket dashboard; unattended replay; iOS terminate races. |
| sentinel host-health loop | 5-8 | Broker-admitted restricted tasks; Jevons probe layers; blurter incident hysteresis. |
| finance dual-stream ledger | 4-7 | Mid-cycle/transfer identity across banks; reconcile correctness. |
| ge source-only cook (+ commercial multimaze2 Classic key — private) | 4-7 | Source-only cook friction; Classic key detail private. |
| mnemo T181 health snapshot | 2-4 | Snapshot serve without lying; indexed aggregates. |
| serviceboard + vellum + ytt + csp + bullseye + mcpbridge + skills | 4-7 | Loopback dashboard; kqueue viewer; broker-required analyze; subset-link DCE. |

### The Diversity Tax

Broker sidecar credentials, device Verify DAGs, host-health supervision, personal double-entry mid-cycle transfers, game-engine cook doctrine, and SQLite health snapshots in one week. No single engineer holds OMP Keychain ACL, Spyder iOS terminate races, and ANZ/CBA transfer fingerprinting at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| claudia OMP / migration doctrine | 8-12 | Sidecar-not-argv; Claudia-owned handover; Task admission for unattended loops. |
| spyder verify product shape | 4-7 | DAG not script; dashboard must not sample the app; owner replay. |
| sentinel alert hysteresis | 2-4 | Two failures + review before blurter; capacity pressure is not Slack. |
| finance transfer identity | 2-4 | Persistent IDs across mid-cycle streams. |
| ge / mnemo | 3-5 | Cook doctrine; health snapshot. |

### What If It Were One Person?

The expert band sums to roughly 47-77 person-days. Ramp-up alone on OMP sidecar credentials, device Verify, and bank reconcile would dominate a generalist's month. Activity was spread across every weekday (3–8 active repos/day) with no zero day.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~70-110 person-days (~3.5-5.5 months)** |
| Specialist team (traditional) | **~50-78 person-days (~2.5-3.9 person-months)** |
| Actual human effort this week | **~19-32 hours (~2.4-4.0 person-days)** |
| **Multiplier vs. generalist** | **~30-55x** |
| **Multiplier vs. specialist team** | **~22-40x** |

The multiplier peaks on claudia OMP/migration (the expensive step is sealing credentials and owning handover, not "add Bun") and on spyder verify (DAG + device truth). It runs lowest on skills sync hygiene. The human contribution concentrated on refusals: plan tokens never in argv, migration never a consumer-invented cold start, Verify never sampling itself, `/health` never waiting on the packer, and Slack never firing on ordinary capacity pressure.

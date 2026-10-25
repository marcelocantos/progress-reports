# Weekly Progress Report — 2026-10-19…25

## Executive Summary

**Thirteen repositories** landed **292 commits**. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** reached what its squash merge calls a usable state (#74): seats on bare pi-agent-core, a two-database control plane after a shared-file defect lost a run of journeys, fleet runaway fixes, and 45 of 45 journeys green. **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** ran eight releases (v0.58.0–v0.65.0, 115 commits): sidecar seats that survive a broker restart, a restart that relaunches only the seats someone wants, Cursor seats that can be steered, and a broker that falls back to the Homebrew binary when a pinned one breaks. **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** v0.98.0–v0.102.0 (74) keeps a resident iOS automation agent per tethered device and stops hung device calls from restarting the daemon. **[marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)** (38) can now write ledgers as git commits with ref compare-and-swap. **loadmon** is new: a macOS menu-bar load monitor with a seven-day logarithmic history. **[marcelocantos/vellum](https://github.com/marcelocantos/vellum)** shipped seven releases and the first `make verify-release`. HMS, Stock Cars, and yourworld2 moved only on branches: [private week 2026-10-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-10-25.md).

**292 commits** | **<span style="color:#1a7f37">+70,116</span> net lines** | **~58-90 person-days traditional equivalent** | **~20-55x multiplier**

> Honesty notes. **(1) The draft was written directly in the Colossus shell.** `claudia broker task --pick remaining` still fails with "Task CLI transport removed; no OMP Task replacement is available (T192; T190)". **(2) Six full jevons clones are left out.** They sit under `.jevons-worktrees-jevons/`, and each re-counts about 950 jevons commits as a separate repo. Gather's raw totals (27 repos, 6,018 commits) and its daily repo counts include them, so every figure here was recounted per commit without them. The README timeline was regenerated with that directory skipped. **(3) claudia and jevons are counted as the union of local `master` and `origin/master`.** Both had diverged again: claudia was 34 ahead and 3 behind, and all 34 local-only commits are unique. Most of them are weekend ledger commits, and they are counted, along with the three origin-only commits (v0.65.0 and `make verify-release`). jevons has **5** commits: squash #74 on origin, plus four unpushed local `master` commits (T1054, T393). #74's body lists 242 squashed items, many of them written on the branch in earlier weeks that reported it as in-flight; it is counted once, here, and dominates ☲ (<span style="color:#1a7f37">+51,136</span>/<span style="color:#cf222e">−11,445</span>). **(4) Several local `master` branches are ahead of GitHub**: bullseye (78), sentinel (59), spyder (9), orthograph (8), and threedee (2). loadmon has no remote. These are counted under the skill's local-default-branch rule. **(5) HMS has no local `master`**, so gather fell back to the checked-out branch and called 31 branch commits "landed". `origin/master` has none in the window, so HMS counts as in-flight. **(6) New exclude:** `canticode/certs` `profiles/**` and `certs/**` (fastlane match-encrypted signing blobs). `marcelocantos/think` had no commits this week and stays out of the headline. Excluded bulk on the counted repos: <span style="color:#1a7f37">+8,122</span>/<span style="color:#cf222e">−2,295</span>. That covers lockfiles, `bullseye.yaml` ledgers, jevons `docs/audits/**/*.json`, the certs blobs, and the report repos' own `reports/**` and `docs/**`.

### Major Achievements & Innovations

- **jevons reaches a usable state** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) #74). Every seat runs on bare pi-agent-core, and the coding-agent SDK that had been adopted beside it is dropped (T1074.12). The control plane splits into two databases with one writer each, after a shared broker file was found to have lost J44, J39, and about 22 journeys behind them. Fleet reconcile passes are serialised, and a handoff with an unknown receipt reports `delivered_unconfirmed`, not "sent". The journey suite runs 45/45, and a topology oracle guards the shared-file defect.
- **The broker restarts without losing the fleet** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.62.0–v0.64.0). A sidecar seat survives a broker restart, and Cursor messages persist during an open streaming request (🎯T206). A restart relaunches only the seats that are wanted and honours the consumer's fleet intent at boot (🎯T207). A restored tool call that never finished is answered as interrupted (🎯T213), and the restart nudge goes only to seats that were mid-turn (🎯T214). A `-state-dir` broker isolates its sidecar socket (T208). Sidecar file tools honour host protected paths and refuse to write back a truncated read (🎯T209).
- **A broken pin no longer takes the broker down** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.64.0–v0.65.0). A 16:00 outage on 22 Oct was filed as a target the same day. A broken `CLAUDIA_BIN` pin now falls back to the Homebrew broker, and `install.sh` stops carrying an earlier pin forward (🎯T212). v0.65.0 adds `make verify-release`, which runs end-to-end tests against the Homebrew install.
- **A resident iOS automation agent per device** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) v0.100.0–v0.102.0). The main daemon supervises a DeviceKit runner for each tethered iPhone (🎯T175). The runner gets a fresh budget on each boot, offers an attended Retry, and stays owned while consent is pending. Sessions come back after a reboot or replug (🎯T167). `ensure_session` can launch an app again after it was terminated (🎯T176).
- **Commit-mode ledgers** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)). The T100 chain writes the ledger through a private `GIT_INDEX_FILE` and `update-ref` compare-and-swap on an integration ref. It refreshes the worktree after each write and is opt-in through `BULLSEYE_COMMIT`/`--commit-mode`. A concurrency oracle proves that simultaneous writes land without silent loss. Achieve and retire became CAS-aware (T96), and a malformed target now degrades on its own instead of failing the whole read (T99).
- **loadmon** (new, local repo). A menu-bar monitor shows CPU, GPU, network, and disk as four meters. Its graph has a logarithmic time axis from 5 seconds to 7 days, backed by five-second SQLite samples kept for eight days. Processes get a pid-and-start-time identity and are ranked as trees by cumulative load. A `loadmond` LaunchDaemon handles root-only sampling, and a local API serves the samples to agents under supervisor.

### Significant Progress

- **vellum v0.29.0–v0.35.0** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum)). The Windows bookkeeping is closed out (T36, T23), and converters fail fast in one shared path for the CLI and MCP (🎯T30.5). `make verify-release` runs an end-to-end battery against the Homebrew install. Same-page anchors resolve to the document, wide PDF artifacts fit the viewer, and a download menu offers PDF or Source. v0.35.0 was rebuilt with Go 1.27.3.
- **Hung device calls no longer restart the spyder daemon** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)). Device listings are coalesced and bounded (T168–T170). A hung adb process is killed at its dispatch deadline (T171). The CLI no longer starts a competing daemon when `:3030` is already listening (T132.8, T173). Run archives replace deletion on retention (🎯T166). Eight entropy-audit findings closed, and `govulncheck` joined the test report.
- **claudia accounting and failure causes** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.58.0–v0.61.0). A broker refusal carries a provider-failure cause (auth, rate limit, backend, client bug), and a billing error is stamped as a spend wall. Grok and Codex overage spend is mapped from their billing caps (T967.2, T967.3). Placement ranks near-ties and draws exact ties at random (T203). Every target is built with cgo, with Linux via zig. Every test binary runs on a private HOME.
- **Orthograph moves to the Canticode Apple team** ([canticode/orthograph](https://github.com/canticode/orthograph), [canticode/certs](https://github.com/canticode/certs)). iOS signing now uses the Canticode team and fastlane match certificates from a new match repo. The App Store Connect record was created and its IDs documented.
- **sqlpipe v0.33.0** ([marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe)). A write committed mid-handshake crosses the link exactly once, and claudia now requires this release.

### Tough Challenges Overcome

- **A shared file that ate journeys** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)). One broker file shared across journey isolates let an earlier journey's state break later ones, and commit 4c638044 lost J44, J39, and about 22 journeys behind them. The fix is structural, not a retry: journey isolates no longer pre-create or symlink the broker file, the control plane has one writer per file, and a topology oracle records how the defect was missed.
- **History scans starved under load** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)). `bullseye serve` writes failed with `id_history_scan_failed` while the CLI succeeded. The cause was a cache wipe combined with a daemon-priority git scan that starved under load (T101). Serve-time history scans are now bounded.
- **An outage from a pinned binary** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)). After the 22 Oct production-broker outage, the fix was to make a broken pin fall back instead of failing, and to stop the installer carrying the pin forward.
- **A daemon that restarted itself to escape slow devices** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)). Concurrent installs, unbounded `devicectl` listings, and temp-directory calls inside the iOS listing could all stall cheap calls long enough to trigger a self-restart. The self-restart in turn left an orphaned `serve` holding the iOS tunnel port. Each case got its own target: coalescing, bounds, deadline kills, and refusing a second auto-start.

### Contributors

- Marcelo Cantos (AI co-authors — Claude, Grok, Cursor, Codex — on trailers throughout).

---

## Agent & Fleet Infrastructure

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Usable State (5 commits: squash #74 plus 4 unpushed)

842 file changes, <span style="color:#1a7f37">+51,136</span>/<span style="color:#cf222e">−11,445</span> after the standing `ios/Vendor/**` and `docs/audits/**/*.json` excludes. **~525 added test declarations**, most of them inside #74. No tag. The squash carries 242 items, many of them reported as in-flight in earlier weeks.

- **Seat engine (T1074.12)**: seats stay on bare pi-agent-core. The decision is documented, and the coding-agent SDK adopted beside it is gone.
- **Control plane (T1074.9)**: two databases with one writer each, and a topology oracle. T1074.9 and T1074.10 were recorded as achieved late in the branch, after the live seat-lifecycle and SDK-seat journeys.
- **Receipts, not transcripts**: a settled handoff, a capable opening brief, a caller-owned interrupt, and a queue drain all answer from the structured receipt, not from the transcript watch. An unknown escalation receipt is not reported as a steer.
- **Fleet runaway fixes**: reconcile passes hold one lock; a parked hold stays queued across twenty simulated minutes, with each stall alert journalled once; the published pin's cost guard fails closed.
- **OCT audit map**: OCT-01 to OCT-10 are mapped to production call sites, regressions, and open residuals, without being declared closed.
- **Unpushed (local `master`)**: a server-side routine-noise classifier for sealed-text owner surfaces, plus `ClassifyLive`, which is bounded and not yet wired (T1054), with a precision report over 20 real session samples.

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Restart-Safe Broker, Eight Releases (115 commits, v0.58.0–v0.65.0)

272 file changes, <span style="color:#1a7f37">+9,321</span>/<span style="color:#cf222e">−2,587</span>. **~117 added test declarations**. Eight releases, plus a `v0.63.1-t861` tag that is not counted as a release. Counted as the union of local and origin `master`; see the honesty note.

- **Restart safety (T206, T207, T208, T213, T214)**: covered under Major Achievements.
- **Sidecar policy (T209, T886)**: protected paths and a truncated-read write guard, ratcheted in the seat's coding-tools wiring. Ledger `protected_paths` persist across a seat reload.
- **Cursor (T118, T204)**: Cursor seats run in the OMP sidecar and are steerable. Cursor plan usage is read in-process again from the IDE session token.
- **Live switching (T612)**: host MCP tools refresh on a live provider switch. Fleet pause and resume are wired to `agentPauseGate` (jevons T966).
- **Failure causes and spend (v0.58.0, T967)**: failure causes are stamped on broker refusals, a billing error is a spend wall, and Grok and Codex on-demand spend are mapped.
- **Control plane (v0.59.0)**: one writer per file, with consumers syncing over a socket. An exit never rewrites a usage fact. A write at any handshake step crosses the link once (requires sqlpipe v0.33.0).
- **Release (v0.60.0, v0.65.0)**: cgo on every target, Linux via zig, never under a `go.work`. The sidecar is staged with its tree layout. `make verify-release` was added.
- **Weekend ledger (unpushed)**: about 30 commits filing and withholding T218–T226 targets: per-seat child environments, seat-owned teardown of command process groups, and spawn-wire attribution. Plus T215, a mid-stream persist that updates one entry instead of chaining snapshots.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Commit Mode and Ledger Repair (38 commits)

80 file changes, <span style="color:#1a7f37">+4,141</span>/<span style="color:#cf222e">−251</span>. **~39 added tests** (Rust). No tag. Local `master` is 78 commits ahead of GitHub.

- **T100.1–T100.5**: covered under Major Achievements.
- **T96–T99**: CAS-protected achieve and retire with concurrent-write retries, and per-target schema parse failures tolerated on read.
- **T101–T103**: bounded serve history scans, a sentinel oracle for thread-local override propagation, and `commit --help` flag parity ratcheted.
- **T104–T106**: `context_append` with a safe context replace; restoring absent targets from a pinned git revision; repairing dedented context literal blocks in ledgers that would not load (the same defect was hand-repaired in claudia this week).

### [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) — FSEvents Gaps (2 commits)

Only directories the FSEvents journal could not name are walked. 🎯T9 (oversized memory degrades the review) and 🎯T10 (Jevons fault classes) were filed. <span style="color:#1a7f37">+824</span>/<span style="color:#cf222e">−47</span>, ~8 tests.

---

## Devices

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Resident iOS Agent, Bounded Daemon (74 commits, v0.98.0–v0.102.0)

163 file changes, <span style="color:#1a7f37">+9,853</span>/<span style="color:#cf222e">−808</span>. **~100 added test declarations**. Five tags.

- **Resident DeviceKit runner (🎯T175)**: per-device backend of the agent supervisor; supervisor env rendered from install-time UDIDs; AlertRunner hold sessions without a one-hour lifetime.
- **Sessions (T167, T176)**: a live `runwda` session comes back when its device reappears; `ensure_session` launches after terminate and alias routing.
- **Daemon bounds (T168–T171, T173, T132.8)**: covered under Significant Progress.
- **Run archives (🎯T166)**: archive rather than delete on retention, verified before removal and created `0600`, with source versions recorded per run.
- **Entropy audit**: ENT-002, 003, 005, 006, 009, 010, 011, and 012 closed. That includes hermetic log capture, an MCP deadline ratchet, a player-wire suite attestation, and a `govulncheck` suite.
- **Signing (T134)**: `codesign-spyder` reads the certificate OU for macOS openssl and comma-separated subjects. The Developer ID certificate is still pending.

### loadmon — Menu-Bar Load Monitor (18 commits, new)

A new Swift package with no GitHub remote. 113 file changes, <span style="color:#1a7f37">+8,007</span>/<span style="color:#cf222e">−482</span>, **~42 tests**.

- Four meters plus a popover graph whose time axis is logarithmic from 5 s to 7 d, with labelled 15 s, 30 s, 5 m, and 10 m steps. CPU, network, and disk are counter deltas over a five-second step; GPU is a per-second gauge averaged into that step.
- Per-process identity is the pid plus the kernel start time. Process scores are `sqrt(cpu²+gpu²+net²)/√3`, accumulated over each process tree.
- A `loadmond` root helper, plus directory I/O trees that cover 60% of each level and a disk-use tree ranked by bytes stored. The local API is served to agents under supervisor. The menu-bar app stops sampling while `loadmond` is alive.

---

## Libraries, Documents & Apps

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — Seven Releases and verify-release (21 commits, v0.29.0–v0.35.0)

70 file changes, <span style="color:#1a7f37">+1,755</span>/<span style="color:#cf222e">−130</span>, ~10 tests. Each release has a Scoop manifest. T36 is achieved with the Colossus `cv gate` plus a zero-skip hms-vm suite as its oracle, T7.1 is superseded, and T23 is achieved. `docs/HANDOVER.md` is marked historical (T30.3). Converters fail fast in `convert.Run` (T30.5). `make verify-release` was added. Anchor links, wide PDF fitting, and the download menu followed.

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — v0.33.0 (4 commits)

Exactly-once crossing for a write committed during the handshake; the lossy-link test now always exercises recovery.

### [canticode/orthograph](https://github.com/canticode/orthograph) and [canticode/certs](https://github.com/canticode/certs) — Apple Cutover (5 + 6 commits)

Signing cut over to the Canticode team (T27.3), with an App Store Connect record created. `canticode/certs` is a new fastlane match repo. Its encrypted profiles and certificates are excluded from ☲, so only the README and the match version file count.

### [marcelocantos/threedee](https://github.com/marcelocantos/threedee) — Print Plates (2 commits)

A ten-key print plate for an X1 Carbon, and the shopping-trolley key source grouped into one project.

---

## Commercial

Nothing commercial landed on a default branch.

**[Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms)** — 31 commits on a branch, gather ☲ <span style="color:#1a7f37">+15,569</span>/<span style="color:#cf222e">−714</span>. **[minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing)** — 222 in-flight commits, <span style="color:#1a7f37">+173,144</span>/<span style="color:#cf222e">−6,878</span> after the standing `Assets/Tracks/**` exclude. **[squz/yourworld2](https://github.com/squz/yourworld2)** — 3 in-flight. Full narrative: [private week 2026-10-25](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-10-25.md).

**[squz/ge](https://github.com/squz/ge)** and **[squz/multimaze2](https://github.com/squz/multimaze2)** had no activity.

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **minicadesmobile/stock-car-racing**: 222 in-flight. See Commercial.
- **Health-Management-Systems/hms**: 31 on a branch. See Commercial.
- **marcelocantos/mnemo**: 13 in-flight, <span style="color:#1a7f37">+4,025</span>/<span style="color:#cf222e">−1,039</span>.
- **marcelocantos/den**: 3 in-flight, <span style="color:#1a7f37">+2,142</span>/<span style="color:#cf222e">−70</span>.
- **arr-ai/arrai**: 3 in-flight, <span style="color:#1a7f37">+1,055</span>/<span style="color:#cf222e">−35</span>.
- **squz/yourworld2**: 3 in-flight (see Commercial). **marcelocantos/spyder**: 6 on side branches. **marcelocantos/cv** and **go-ios**: 1 each.
- **marcelocantos/jevons**: the checked-out `steer-modes-stop-guards-seat-stops` branch is 1,879 commits ahead of `origin/master`. Gather's in-flight figures for jevons and claudia are not used, because with local `master` diverged they mostly re-count commits that are already on origin or inside #74.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** commits within 2026-10-19…25 by commit date. That means the local default branch for most repos, and the union of local and `origin/master` for claudia and jevons. The `.jevons-worktrees-jevons/` clones and HMS's branch are excluded (see the honesty notes). In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **13** |
| Total landed commits | **292** |
| Total lines added (landed, filtered) | <span style="color:#1a7f37">+86,088</span>‡ |
| Total lines removed (landed, filtered) | <span style="color:#cf222e">−15,972</span>‡ |
| Net new lines (landed, filtered) | <span style="color:#1a7f37">+70,116</span>‡ |
| File changes | 1,599 (summed per commit; a path touched twice counts twice) |
| New files created | 525 unique paths after the same excludes |
| Bulk paths excluded from ☲ | <span style="color:#1a7f37">+8,122</span>/<span style="color:#cf222e">−2,295</span> on counted repos |
| Releases published | **21** (claudia v0.58.0–v0.65.0; vellum v0.29.0–v0.35.0; spyder v0.98.0–v0.102.0; sqlpipe v0.33.0) |
| Languages | Go, TypeScript, Rust, Swift, Python, Shell, Markdown, YAML |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. Every repo was recounted per commit with the same pathspecs gather uses. **New this run:** `canticode/certs` `profiles/**` and `certs/**`.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 115 | 272 | <span style="color:#1a7f37">+9,321</span> | <span style="color:#cf222e">−2,587</span> | <span style="color:#1a7f37">+6,734</span>* |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 74 | 163 | <span style="color:#1a7f37">+9,853</span> | <span style="color:#cf222e">−808</span> | <span style="color:#1a7f37">+9,045</span> |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 38 | 80 | <span style="color:#1a7f37">+4,141</span> | <span style="color:#cf222e">−251</span> | <span style="color:#1a7f37">+3,890</span> |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 21 | 70 | <span style="color:#1a7f37">+1,755</span> | <span style="color:#cf222e">−130</span> | <span style="color:#1a7f37">+1,625</span> |
| loadmon (local) | 18 | 113 | <span style="color:#1a7f37">+8,007</span> | <span style="color:#cf222e">−482</span> | <span style="color:#1a7f37">+7,525</span> |
| [canticode/certs](https://github.com/canticode/certs) | 6 | 4 | <span style="color:#1a7f37">+80</span> | <span style="color:#cf222e">−52</span> | <span style="color:#1a7f37">+28</span> |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 5 | 843 | <span style="color:#1a7f37">+51,136</span> | <span style="color:#cf222e">−11,445</span> | <span style="color:#1a7f37">+39,691</span>† |
| [canticode/orthograph](https://github.com/canticode/orthograph) | 5 | 10 | <span style="color:#1a7f37">+195</span> | <span style="color:#cf222e">−61</span> | <span style="color:#1a7f37">+134</span> |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 4 | 21 | <span style="color:#1a7f37">+658</span> | <span style="color:#cf222e">−86</span> | <span style="color:#1a7f37">+572</span> |
| [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) | 2 | 12 | <span style="color:#1a7f37">+824</span> | <span style="color:#cf222e">−47</span> | <span style="color:#1a7f37">+777</span> |
| [marcelocantos/threedee](https://github.com/marcelocantos/threedee) | 2 | 7 | <span style="color:#1a7f37">+82</span> | <span style="color:#cf222e">−9</span> | <span style="color:#1a7f37">+73</span> |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 1 | 3 | <span style="color:#1a7f37">+35</span> | <span style="color:#cf222e">−14</span> | <span style="color:#1a7f37">+21</span> |
| [marcelocantos/progress-reports-private](https://github.com/marcelocantos/progress-reports-private) | 1 | 1 | <span style="color:#1a7f37">+1</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+1</span> |

\* *The union of local and `origin/master`: 81 origin commits plus 34 unpushed local commits. Two of the 81 were authored on 14 and 18 Oct but committed in this window.*

† *Squash #74 (242 items, many previously reported as in-flight) plus four unpushed local commits.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~525 | Journeys, receipts, reconcile, control-plane topology, classifiers |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~117 | Restart and resume, sidecar policy, planusage, controlplane links |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~100 | DeviceKit runner, archives, deadline ratchets, listings |
| loadmon | ~42 | Sampler, store, policy, process series |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | ~39 | Commit-mode CAS and concurrency, restore, repair |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | ~10 | Fail-fast converters, anchors, verify-release |
| [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) | ~8 | FSEvents gap walk |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~1 | Mid-handshake write |
| **Total** | **~842** | Gross added `func Test` / `#[test]` / `@Test` / `test(` / `it(` lines in the landed diff. jevons' figure spans the whole squash. |

### Daily Activity

![Daily active repositories](daily-activity-2026-10-25.svg)

*(Active repositories per day, landed commits by commit date, with the clones excluded: Mon 10-19 4, Tue 10-20 2, Wed 10-21 5, Thu 10-22 6, Fri 10-23 4, Sat 10-24 6, Sun 10-25 6. The README timeline counts all-branch activity by author date, so its days for this week are higher.)*

---

## Ideas & Innovations

### Survive the Restart, Relaunch Only What Is Wanted ([claudia](https://github.com/marcelocantos/claudia))

Restarting a broker used to be a choice between losing seats and resurrecting every seat it had ever run. **What is persisted is intent as well as state.** The canonical messages are written before each model call, the consumer's fleet intent is honoured at boot, and only wanted seats come back. A tool call cut off mid-flight is answered as interrupted, so the model does not wait for a result that will never arrive.

### A Pin Should Fail Toward the Known-Good Binary ([claudia](https://github.com/marcelocantos/claudia))

A `CLAUDIA_BIN` pin exists so a dev build can run the fleet, which means a bad dev build can take the fleet down. **A broken pin now falls back to the Homebrew broker**, and the installer stops carrying an old pin forward. `make verify-release` then checks the Homebrew path end to end, the same pattern vellum adopted the same week.

### One Writer per File ([jevons](https://github.com/marcelocantos/jevons), [claudia](https://github.com/marcelocantos/claudia))

A shared control file let one journey's state poison the next and silently lost two dozen journeys. **Each file now has a single writer, and consumers sync over a socket.** The fix landed on both sides of the jevons/claudia boundary in the same week, and a topology oracle keeps the shared file from creeping back.

### Ledger Writes as Commits ([bullseye](https://github.com/marcelocantos/bullseye))

When many agents update one YAML ledger, the hard part is concurrency, not the format. **A private git index plus `update-ref` compare-and-swap turns each write into an atomic commit on an integration ref.** A loser retries instead of overwriting, and a concurrency oracle proves that nothing is lost.

### A Log-Time Axis for Machine Load ([loadmon](#loadmon--menu-bar-load-monitor-18-commits-new))

The last few seconds and the last week matter for different reasons. **A logarithmic age axis puts 5 s and 7 d on one graph**, and every stored value stays a raw five-second sample. Any coarsened copy is a cache that can be rebuilt, never the source of truth.

### Kill the Call, Not the Daemon ([spyder](https://github.com/marcelocantos/spyder))

The daemon had been restarting itself whenever a device call outlived its budget. That restart dropped every healthy session and could leave an orphaned server on the tunnel port. **The deadline now kills the hung adb or `devicectl` call, and listings are coalesced and bounded**, so one slow phone cannot evict the others.

---

## Effort Estimate: Traditional vs. AI-Assisted

A week of operational hardening, with the fleet back on after the 21 Oct unblock. jevons' usable-state squash is estimated on what it carries, since none of it was counted while in-flight. claudia's work centred on making a broker restart and a bad pin survivable, which follows directly from running the fleet on dev builds.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| jevons usable state (#74) | 12-18 | Seat-engine decision and SDK removal; a two-database control plane after a cross-journey state defect; receipt-based handoff status; fleet runaway fixes; a full 45-journey suite green. |
| claudia v0.58–v0.65 | 10-15 | Restart-safe sidecar seats and intent-only relaunch; protected-path and truncated-read guards; billing and failure-cause mapping; cgo/zig release; pin fallback after an outage. |
| spyder v0.98–v0.102 | 7-11 | Per-device resident DeviceKit runner under supervision; reboot and replug recovery; bounding devicectl, adb, and listings; archive-not-delete retention; eight audit closures. |
| bullseye commit mode + T96–T106 | 5-8 | Git ref CAS writer with a private index; concurrency oracles; bounded history scans under load; restore and repair of unloadable ledgers. |
| loadmon | 4-6 | New macOS app: IOKit/GPU counters, a log-time renderer, SQLite five-second storage, process identity and trees, a root LaunchDaemon helper, a local API. |
| vellum, sqlpipe, sentinel, orthograph/certs, threedee | 3-6 | Seven releases and the verify-release battery; exactly-once handshake writes; FSEvents gap walk; Apple team cutover; print plates. |

### The Diversity Tax

Agent-runtime restart semantics, a fleet control plane and journey harness, iOS and Android device automation, git plumbing for concurrent ledgers, macOS system telemetry and LaunchDaemons, Apple signing, and CAD print parts. Few engineers move between `update-ref` CAS and IOKit GPU counters in the same week.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| jevons | 2-4 | Unblocking the fleet (21 Oct), the seat-engine decision, signing off the usable-state merge. |
| claudia | 4-7 | Outage triage on 22 Oct, eight release cuts, the verify-release pattern, the fleet-restart rules. |
| spyder | 2-4 | Physical device runs, consent prompts, deciding what counts as a device failure versus a daemon failure. |
| bullseye | 1-2 | Commit-mode design and ledger repair calls. |
| loadmon | 2-4 | Product design of the meters, axis, and process scoring; on-machine iteration on the menu bar. |
| vellum, orthograph/certs, others | 2-3 | Release path, Apple developer account and App Store Connect steps, print checks. |

### What If It Were One Person?

The expert band sums to roughly 41-64 person-days. A generalist would add ramp-up on pi-agent-core and the broker wire, DeviceKit and `devicectl`, git plumbing, and macOS telemetry APIs. Landed activity ran every day (2–6 repos), with the heaviest days on Thursday and the weekend.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~58-90 person-days (~2.9-4.5 months)** |
| Specialist team (traditional) | **~41-64 person-days (~2.1-3.2 person-months)** |
| Actual human effort this week | **~13-24 hours (~1.6-3.0 person-days)** |
| **Multiplier vs. generalist** | **~20-55x** |
| **Multiplier vs. specialist team** | **~15-40x** |

The multiplier is highest on jevons' squash and claudia's restart work, where the cost is the volume of carefully tested change, and lowest on loadmon and the Apple cutover, where on-machine judgement and account steps dominate. The human contribution was operational: turn the fleet back on, find out why a restart lost seats and a pin broke production, and require the release path to be proven rather than assumed.

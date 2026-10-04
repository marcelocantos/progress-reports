# Weekly Progress Report — 2026-09-28…10-04

## Executive Summary

**Fifteen repositories** landed **562 commits** — the heaviest landed week of the series by commit count. Last week's jevons in-flight train reached master as **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** v0.14.0–v0.15.0 (304 commits): one `seatstate.Authority`, worktree isolation with a merge-tree integrator, rename-proof mission bounds, and reap-not-park. **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** (156 commits, v0.45.0–v0.48.0) sealed the OMP sidecar's lifetime to the broker that started it, put one access token per plan under a broker-owned refresh lock, and made host MCP a real session. **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** (39 commits, v0.96–v0.97) turned Verify into an owner-review product — in-place findings, restage-without-reassess, iOS Local Network alerts. Two new public products: **[marcelocantos/memento](https://github.com/marcelocantos/memento)** (lossless tile screen history) and **[marcelocantos/jevons-mobile](https://github.com/marcelocantos/jevons-mobile)** (chrome-free Flutter cockpit on iPad and Pixel Fold). **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** v0.107.0 repairs schema drift from a half-applied sqlift plan. **[marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)** refuses an achieve whose cited gate does not hold. Stock Cars 3.26 went live on both stores; HMS remains unmerged: [private week 2026-10-04](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-10-04.md).

**562 commits** | **+86,185 net lines** | **~90-140 person-days traditional equivalent** | **~30-50x multiplier**

> Honesty note: **new `data/line-excludes.yaml` globs this run** — `**/pubspec.lock` in defaults (Flutter lockfile; jevons-mobile ~+370); `minicadesmobile/stock-car-racing` `Assets/Tracks/**` (4,020 Unity track files, ~+209k/−11k in the 3.26 squash). Headline ☲ is gather `landed:` after those globs plus the origin/main Stock Cars squash counted by hand (local `main` lagged origin). **+99,267/−13,082**. Excluded bulk this week **~+220k/−14k**. Remaining Unity garage/UI/scenes in stock-car still sit in ☲.

### Major Achievements & Innovations

- **Control-plane land** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) v0.14.0–v0.15.0) — last week's ~383-commit in-flight train reached master. One `internal/seatstate.Authority` with explicit unknowns; same-repo workers in private git worktrees landed via `git merge-tree` + git-dir flock; `missionbound` caps starts per *target* so a rename cannot reset the meter; finished workers are reaped, not parked. Pins claudia v0.45–v0.48.
- **Sidecar lifetime sealed** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.45–v0.48) — Bun is a child whose stdin is a lifeline pipe; SIGKILL of the broker kills it. One access token per plan; refresh lock is the broker's; unattended recover cannot pop a sign-in. Host MCP `tools/list` is a real session; a wedged stdio server is restarted. Homebrew ships the sidecar so a tap install can start plan seats.
- **Verify is a reviewable run** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) v0.96–v0.97) — finished runs stay until dismissed; the owner types findings in place (`in_game` / `other`); `verify_now` restages one step without reassessing; advisory preconditions tag evidence untrustworthy rather than blocking the gate. iOS Local Network alert is read via Accessibility Inspector and tapped via an in-process XCUITest runner.
- **Schema-drift repair** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) v0.107.0) — sqlift applied DDL in autocommit and stamped the hash only after the plan; a lost write lock left indexes committed and the hash unchanged. `BEGIN IMMEDIATE` around apply; additive drift is reconciled in place.
- **Stock Cars 3.26 live** ([minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing)) — Night and Derby tracks, Halloween cars, repair reminders, 3.25 save compatibility; App Store and Play production 2026-10-04. Detail: [private week 2026-10-04](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-10-04.md).

### Significant Progress

- **memento** ([marcelocantos/memento](https://github.com/marcelocantos/memento), initial) — rolling in-memory screen history: 64×64 LZ4 tiles, no GOP, any frame rebuilt from each tile's newest version at or before *t*. Live ScreenCaptureKit path still blocked on TCC.
- **jevons-mobile** ([marcelocantos/jevons-mobile](https://github.com/marcelocantos/jevons-mobile), initial) — chrome-free Flutter WebView shell for the cockpit; codesign via wildcard profile without registering a portal App ID; deployed to the Jevons iPad mini and Pixel Fold.
- **Achieve-time gate enforcement** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)) — refuse a write whose cited gate is not GREEN; persist accepted-risk as `UNVERIFIED — ACCEPTED RISK`; reserve IDs held uncommitted in any worktree. Still v0.57.0.
- **Keychain secrets + GoodWe SEMS+** ([marcelocantos/sentinel](https://github.com/marcelocantos/sentinel)) — AES-256-GCM store keyed in login Keychain; 1Password import never printed; SEMS+ JSON API with daylight gate and two-observation hysteresis. No tag.
- **finance category matcher** ([marcelocantos/finance](https://github.com/marcelocantos/finance)) — idempotent seed + substring/regex matcher writing `postings.category_id` aligned to Beancount chart paths.

### Tough Challenges Overcome

- **One Bash froze every seat** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — sidecar Bash/Glob/Grep were `spawnSync` in one Bun process; a 60 s command froze load/adopt/prompt for every other seat (205 silent ≥30 s gaps). Now async `runCommand`.
- **Orphan sidecar survived every restart** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — `Setsid` + never waited; the 08:04 sidecar outlived the broker, so token-per-plan and async tools never took effect. Stdin lifeline + `StopUnowned` SIGTERM/SIGKILL-replace.
- **Unattended recover popped a sign-in** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — `RecoverPlan` raced a seat refresh, presented a spent refresh token, got `invalid_grant`, and opened interactive login. Plan refresh lock; `Login.NoLogin`; only a turn's own error marks its token refused.
- **Wedged turn after a dead sidecar handle** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)) — reattach queued behind a turn that never ended; “accepted” was not motion. Lost-handle interrupt + 15-minute wedge, not “wait for in_flight”.
- **Census looked like done** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)) — retiring seat-state symbols dropped the needle count while controls still derived state. Done is a call-graph ratchet (`t766_seat_derivation_ratchet_test.go`), not `count.sh`.
- **SpringBoard buttons AX cannot press** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — Accessibility Inspector walks the Local Network alert and cannot Activate it. Read is inspector-only; tap is a 22-line XCUITest hosted by go-ios `testmanagerd`.
- **Half-applied DDL that looked like drift** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)) — autocommit plan, hash stamped at the end; restart refused a store that had already created indexes.

### Contributors

- Marcelo Cantos (AI co-authors — Claude, Grok, Cursor, Codex — on trailers throughout; some jevons/claudia commits authored as the `commitbase` worktree identity, excluded from ℂ by gather's `user.name` filter).

---

## Agent & Fleet Infrastructure

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Control-Plane Land (304 commits, v0.14.0–v0.15.0)

**The biggest effort of the week — and the land of last week's in-flight train.** 977 file changes, <span style="color:#1a7f37">+33,770</span>/<span style="color:#cf222e">−3,685</span>. **~366 net new `func Test`**. Pins claudia v0.45.0 → v0.48.0.

- **Seat authority (🎯T766.2)**: one `internal/seatstate.Authority` injected into HTTP, MCP and fleet. Alive / InFlight / Phase / BornStuck / QueueDepth / Provider / Model carry explicit unknowns; observation feeds are independent of actuators. Census needles retired 11→4 by folding call sites, then rebriefed when rename-counts looked like done.
- **Worktree isolation (🎯T254.2, T955, T888, T918)**: same-repo workers get private git worktrees; PO/integrator keep the shared clone. `worktree.Integrate` uses `git merge-tree` (no dirty tree), fast-forward as CAS, flock in the git dir — concurrent landings failed 6/6 without the lock because git rewrites the index before the ref swap. `DetectBranchCheckout` refuses a shared-clone `git checkout` off the integration branch.
- **Mission blowout (🎯T998, T784)**: a worker hit ~10σ context / 6σ starts among ~219 seats. `internal/missionbound` (JSON store, `DefaultMaxStarts=15` / 24h, **target-attributed so a rename cannot reset**); `internal/missionmeter` from spool+lifecycle bytes. A mid-work finish-report **retains** its seat instead of reaping.
- **Reap vs park (🎯T985, T972, T983, T984)**: finished/superseded workers are reaped (`stop+Remove`), not parked rows. Pre-reap scope-scan parks seats with uncommitted work. Parked intent survives restart. Sentinel `intent_violation` / `seat_divergence` via claudia `BrokerSeats` / `StopBrokerSeat`.
- **Busy-seat delivery (🎯T899/T902/T931)**: sender-class ladders (owner 60 s, overseer 120 s); mid-turn answers relay at the next tool event; non-steerable busy seats queue.
- **Cockpit**: plan-override colours and prohibition icon; Frontier follows the selected seat's repo; Workers/jwork strip unmounted; build-id hello auto-reload; dictation-safe empty composer.
- **Correctness substrate**: nested heavy-lease reuse (T997); T603 flock serialises concurrent `go test`; tests cannot grant seats on the owner's broker (T975); isolate brokers must not rotate the shared Anthropic refresh token (T940).

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Sidecar Lifetime (156 commits, v0.45.0–v0.48.0)

442 file changes, <span style="color:#1a7f37">+16,467</span>/<span style="color:#cf222e">−1,970</span>. **~192 new `func Test`**. Continuation of last week's OMP/credentials/migration train.

- **Sidecar is a child (🎯T145, T166, T157)**: `Ensure` starts Bun whose stdin is a lifeline pipe; EOF (including SIGKILL of the broker) kills it. Exclusive `flock` on `<socket>.lock`. Homebrew formula ships `PackagedSidecarDir`; sidecar `EnsureDeps` installs its own `node_modules` before Bun.
- **One access token per plan (🎯T159, T155, T165, T168)**: sidecar holds one token per plan; broker moves a whole plan with one token message. Every refresh is saved. `RecoverOMPPlan` takes the plan refresh lock so unattended `auth-recover` cannot race a seat refresh into `invalid_grant`. Broker ticks every minute, renews inside a 10-minute margin, never opens a sign-in. `CLAUDIA_OMP_NO_REFRESH`. `auth_status` reports login health without logging in.
- **Host MCP is a session (🎯T147, T149, T934)**: `tools/list` via a proper MCP session; concurrent launches share one fetch; stalled servers neither block launch nor fail silent. Pending host tool does not outlive its connection. Claude Code 2.1.284 `server/discover` before `initialize` had wedged stdio; wedged stdio MCP is restarted and bounded.
- **Conversation survives the process (🎯T150–T153, T148)**: per-seat JSONL store; compaction as Oh My Pi (`ContextPreserve` / `ContextPins`); compact before `thresholdTokens`; 400 “prompt is too long” after one retry is terminal `ContextOverflow`. Resume gate ignores sidecar bookkeeping as history.
- **Shared sidecar must not serialise the fleet (🎯T161–T164)**: Bash/Glob/Grep async; thinking-only Claude record is not a terminal stop; sidecar refusal on Grok/Cursor names the missing `PATH`; Bash tool refuses `git checkout`/`git switch` of the shared clone.
- **Consumer-visible broker**: `BrokerSeats` / `StopBrokerSeat`; deliberate broker stop says so to every host first; `TaskConfig.SessionID` is the provider-neutral resume handle; claudia never imports jevons (🎯T13).

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Verify Owner Review (39 commits, v0.96.0–v0.97.0)

174 file changes, <span style="color:#1a7f37">+6,909</span>/<span style="color:#cf222e">−612</span>. **~41 new `func Test`**.

- **Owner review (🎯T149)**: finished runs stay until `Hub.Dismiss`. `verify_review` saves finding/notes as typed; `verify_now` restages one entry without checks or cleanup; `GET /verify/runs/<id>/report.json` is the full outline. Universal findings: `in_game` (“Check in game”), `other` (notes required). Next-unassessed arrows; list and pane scroll independently.
- **Model appraisal**: `human_gate` with `judgment: static` is appraised unattended; the verdict never settles the gate. Model images resized to Claude's 1568 px long edge, JPEG ≤ 256 KiB (a 485 KiB iPad JPEG produced no Claudia final result against a 1 MiB JSONL line limit).
- **Advisory preconditions (🎯T145)**: `human_gate.precondition` is best-effort and never changes which steps run. Not met or unchecked tags the entry untrusted (`?` on the step).
- **iOS system alerts**: `system_alert` / `system_alert_tap` via Accessibility Inspector + XCUITest `AlertRunner`. Workflow `ios-fresh-install.yaml` uninstalls, deploys, taps **Allow** on Local Network, then waits for the app channel.
- **Device robustness**: CoreDevice graceful terminate before SIGKILL (Stock Cars on Jevons relaunched after go-ios kill); one retry of DTX process-list on a *fresh* connection; cull relay sessions on peer loss; ge `submit_release` / TestFlight `external:true` need `--confirm` before fastlane exec.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Achieve Gates That Refuse (24 commits)

52 file changes, <span style="color:#1a7f37">+2,932</span>/<span style="color:#cf222e">−141</span>. Still v0.57.0.

- **T94 write-path gate**: `apply_with_gate` runs before `with_locked_mutation` returns Ok. Verdicts Verified / Ungated / Marked / Refused. Refusals name the field: unknown id, not GREEN, `tree.clean:false`, misquoted verdict, not an ancestor. Byte-identical ledger on refuse.
- **`UNVERIFIED — ACCEPTED RISK`**: marked achieves persist behind that greppable marker (bytes shared with jevons `AchieveMarker`).
- **Worktree ID reserve**: `id_alloc` scans every `git worktree list` ledger so uncommitted rows on the main clone are not minted by a sibling.
- **GitHub adapter mutex**: one issue writer per ledger; `github sync` and `issues-poll` refuse the other adapter. Bounded default summary projection. T89 CLI `--owner` honouring.

### [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) — Keychain Secrets, SEMS+ (7 commits)

33 file changes, <span style="color:#1a7f37">+2,306</span>/<span style="color:#cf222e">−137</span>. Continuation of last week's host-health loop.

- **`secrets.enc`**: AES-256-GCM, 32-byte key in login Keychain (`com.marcelocantos.sen.secrets`). Daemon reads set `kSecUseAuthenticationUIFail` — missing approval is an error, never an unattended dialog.
- **1Password Go SDK**: `sen --secret-import` via desktop-app integration; value never printed. `--secret-import-login` fills account+password in one approval.
- **GoodWe SEMS+**: direct JSON API (`au-semsplus.goodwe.com`), request signing like the web client, daylight gate at 20° solar elevation, two fresh observations before blurter. Empty issue list is `[]` not null.

### [marcelocantos/jevons-mobile](https://github.com/marcelocantos/jevons-mobile) — Chrome-Free Cockpit Shell (8 commits, initial)

**New product.** 86 file changes, <span style="color:#1a7f37">+2,357</span>/<span style="color:#cf222e">−130</span> after `pubspec.lock` exclude. Flutter WebView shell for `https://jevons.canticode.com`. No URL bar, reload, or settings chrome; failed main-frame loads still offer Retry / Change URL. `scripts/sign-ios.sh` codesigns unsigned `Runner.app` with the existing wildcard development profile (team `SWA3H3N7TW`) so Xcode never registers a new App ID. Deployed via Spyder to the Jevons iPad mini and the Pixel Fold.

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — Synopsis Parser + Broker Pin (2 commits)

- Skip narrated slug replies (161 failed replies in two days had each re-raised a ytt alert). Pin Claudia v0.48.0 and `RequireBroker` so tasks never fall back to a direct provider spawn (`task_started.provider` was unknown to the v0.44 client).

### [marcelocantos/skills](https://github.com/marcelocantos/skills) — LOC Colouring (1 commit)

- progress-report skill requires green/red HTML spans on plus/minus line counts.

---

## Libraries & Infrastructure

### [marcelocantos/memento](https://github.com/marcelocantos/memento) — Tile Screen History (2 commits, initial)

**New product.** A rolling, in-memory screen history for macOS. `memento run` captures every display up to five times a second and keeps the last five minutes; `memento grab --ago 30s` writes a lossless sRGB PNG per display. Raw frames do not fit (Retina + 6K ≈ 132 MB/frame, ~199 GB for five minutes at 5 fps). Each display is 64×64 tiles; only tiles that changed since the previous frame are kept, LZ4-compressed. Any retained frame is rebuilt from each tile's newest version at or before that moment — no delta chains, no keyframes. A 2 GB byte budget drops the globally oldest frame so every display covers the same span. Displays keyed by UUID; frames stamped on the ScreenCaptureKit host clock. Live capture still unverified (TCC denied Screen Recording to the launching app). **11 Swift Testing `@Test`**.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Drift Repair (2 commits, v0.107.0)

- sqlift applied each DDL in autocommit and stamped the schema hash only after the whole plan. A `CREATE INDEX` that lost the write lock left earlier indexes committed and the hash unchanged; every later start refused with “Schema drift detected”. `applyMigration` wraps `BEGIN IMMEDIATE` / `COMMIT`; already-drifted stores whose remaining diff is additive are reconciled and re-stamped. Wedged schema is a health **failure**; throttled compress backfill is a **warning**.

### [marcelocantos/finance](https://github.com/marcelocantos/finance) — Category Matcher (2 commits)

- First-pass matcher: case-insensitive substring, `re:` prefix for regex, higher `priority` wins. Seeds are Beancount chart paths; winning path also writes `postings.account`. Coles Express outranks Coles; word-boundary `aldi` / `agl` so aldinga/eagle do not match. Dual-stream / mid-cycle tables untouched. **15** unittest methods.

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — First Paint (2 commits, v0.24.0)

- Two small mmdc diagrams were ~390 KB of inline SVG in a 10 KB document. Serve-time lift of every Mermaid SVG to `/_vellum/fragment`; fetch when they near the viewport. Images `loading="lazy"`. v0.25.0 (pptx sink) is in-flight on origin, not this clone's master.

### [marcelocantos/sysinfo-mcp](https://github.com/marcelocantos/sysinfo-mcp) — Battery Temp, Router (4 commits)

- `AppleSmartBattery` Temperature is deciKelvin (3050 → 31.85 °C). IPv4 router is `kSCPropNetIPv4Router` on the primary interface, not a key that is never present. JSON-RPC smoke for every `system_info` category.

---

## Game Engine

### [squz/ge](https://github.com/squz/ge) — Stale SDL Cook Lock (5 commits)

- **🎯T201**: waiter seeing a dead cook-lock pid reclaims immediately instead of 30 minutes; `clone_or_checkout` drops a half-written dir if `.git` exists but `rev-parse HEAD` fails.
- **🎯T198** achieved: unit-test GREEN **447/447**, **55,618/55,618** assertions (root cause was uncooked `vendor/sdl3` under source-only doctrine).
- **🎯T202** filed: versioned ship builds must use tagged worktree source.

---

## Commercial

**[minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing)** (1 commit on `origin/main`) — **3.26 live** on App Store and Play, 2026-10-04. Night/Derby tracks, Halloween cars, repair reminders, 3.25 save compatibility. Unity `Assets/Tracks/**` excluded from ☲. Full narrative: [private week 2026-10-04](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-10-04.md).

HMS2 C# VCL port, RenderStream, and native-web journeys remain unmerged (checkpoint-history corpus still inflates in-flight). **[squz/yourworld2](https://github.com/squz/yourworld2)** Spyder Verify YAML + music-resume still on `chore/hygiene-init`. **[squz/multimaze2](https://github.com/squz/multimaze2)** silent; Classic key still off origin. Same private companion.

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **Health-Management-Systems/hms** — 334 in-flight; ~2.25M of this week's insertions are generated retranslation. Semantic work is the `Hms.Vcl` runtime (~30k) plus local `native-web` / `renderstream` forks. Private companion.
- **marcelocantos/jevons** — ~56 in-flight tail (T766.3 action arbitration, T608 unpublished symbols).
- **marcelocantos/claudia** — ~24 in-flight (T164/T169–T171 after v0.48).
- **marcelocantos/vellum** — v0.25.0 pptx sink on origin, not this clone.
- **squz/yourworld2** — ~9 in-flight on chore (Verify YAML, music resume, ge pin).
- **minicadesmobile/stock-car-racing** — chore branch still carries pre-squash history vs main; T83 (save-compat vs live 3.26) filed.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-09-28…10-04. In-flight branch work is excluded by design. Stock Cars 3.26 is counted from `origin/main` (local `main` had not fast-forwarded).*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **15** |
| Total landed commits | **562** |
| Total lines added (landed, filtered) | <span style="color:#1a7f37">+99,267</span>‡ |
| Total lines removed (landed, filtered) | <span style="color:#cf222e">−13,082</span>‡ |
| Net new lines (landed, filtered) | <span style="color:#1a7f37">+86,185</span>‡ |
| File changes | ~2,200 |
| New files created | ~500 |
| Bulk paths excluded from ☲ | ~+220k / −14k (stock-car Tracks + lockfiles/bullseye.yaml + standing globs) |
| Releases published | **~12** (jevons v0.14–v0.15, claudia v0.45–v0.48, spyder v0.96–v0.97, mnemo v0.107.0, vellum v0.24.0, Stock Cars 3.26) |
| Languages | Go, TypeScript, Rust, Swift, Dart, Python, C, C++, YAML, Markdown, Shell, SQL, HTML, CSS, Kotlin, Starlark |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. **New this run:** `**/pubspec.lock`; `minicadesmobile/stock-car-racing` `Assets/Tracks/**`.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 304 | 977 | <span style="color:#1a7f37">+33,770</span> | <span style="color:#cf222e">−3,685</span> | <span style="color:#1a7f37">+30,085</span> |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 1 | ~353 | <span style="color:#1a7f37">+28,550</span> | <span style="color:#cf222e">−5,946</span> | <span style="color:#1a7f37">+22,604</span>* |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 156 | 442 | <span style="color:#1a7f37">+16,467</span> | <span style="color:#cf222e">−1,970</span> | <span style="color:#1a7f37">+14,497</span> |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 39 | 174 | <span style="color:#1a7f37">+6,909</span> | <span style="color:#cf222e">−612</span> | <span style="color:#1a7f37">+6,297</span> |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 24 | 52 | <span style="color:#1a7f37">+2,932</span> | <span style="color:#cf222e">−141</span> | <span style="color:#1a7f37">+2,791</span> |
| [marcelocantos/jevons-mobile](https://github.com/marcelocantos/jevons-mobile) | 8 | 86 | <span style="color:#1a7f37">+2,357</span> | <span style="color:#cf222e">−130</span> | <span style="color:#1a7f37">+2,227</span> |
| [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) | 7 | 33 | <span style="color:#1a7f37">+2,306</span> | <span style="color:#cf222e">−137</span> | <span style="color:#1a7f37">+2,169</span> |
| [marcelocantos/memento](https://github.com/marcelocantos/memento) | 2 | 23 | <span style="color:#1a7f37">+1,931</span> | <span style="color:#cf222e">−4</span> | <span style="color:#1a7f37">+1,927</span> |
| [marcelocantos/finance](https://github.com/marcelocantos/finance) | 2 | 14 | <span style="color:#1a7f37">+1,928</span> | <span style="color:#cf222e">−263</span> | <span style="color:#1a7f37">+1,665</span> |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 2 | 13 | <span style="color:#1a7f37">+1,062</span> | <span style="color:#cf222e">−36</span> | <span style="color:#1a7f37">+1,026</span> |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 2 | 9 | <span style="color:#1a7f37">+510</span> | <span style="color:#cf222e">−3</span> | <span style="color:#1a7f37">+507</span> |
| [marcelocantos/sysinfo-mcp](https://github.com/marcelocantos/sysinfo-mcp) | 4 | 8 | <span style="color:#1a7f37">+284</span> | <span style="color:#cf222e">−68</span> | <span style="color:#1a7f37">+216</span> |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 2 | 8 | <span style="color:#1a7f37">+131</span> | <span style="color:#cf222e">−30</span> | <span style="color:#1a7f37">+101</span> |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 2 | 4 | <span style="color:#1a7f37">+86</span> | <span style="color:#cf222e">−52</span> | <span style="color:#1a7f37">+34</span> |
| [squz/ge](https://github.com/squz/ge) | 5 | 2 | <span style="color:#1a7f37">+30</span> | <span style="color:#cf222e">−1</span> | <span style="color:#1a7f37">+29</span> |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 1 | 2 | <span style="color:#1a7f37">+14</span> | <span style="color:#cf222e">−4</span> | <span style="color:#1a7f37">+10</span> |

\* *After excluding `Assets/Tracks/**` (~+209k/−11k) and `bullseye.yaml`; remaining Unity garage/UI/scenes still in ☲. Squash on `origin/main`; local `main` had not fast-forwarded at gather time.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~366 net `func Test` | Authority, worktrees, missionbound, reap, journeys J14/J35–J38 |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~192 gross | sidecar lifetime, token lock, host MCP, compaction |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~41 | review, verify_now, preconditions, alerts, DTX retry |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | ~40 `#[test]` | gatecheck refuse-before-write, worktree alloc |
| [marcelocantos/finance](https://github.com/marcelocantos/finance) | 15 | matcher priority, regex, dual-stream isolation |
| [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) | 14 | secrets round-trip, SEMS sign/session/daylight |
| [marcelocantos/jevons-mobile](https://github.com/marcelocantos/jevons-mobile) | 11 | settings + chrome-free widget tests |
| [marcelocantos/memento](https://github.com/marcelocantos/memento) | 11 | tile rebuild, budget, unplug segment, PNG |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 7 | txn rollback, additive reconcile, ingest waits |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 5 | lazy lift + fragment identity |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 4 | narrated slug, RequireBroker |
| **Total** | **~700+ gross** | landed only |

### Daily Activity

![Daily active repositories](daily-activity-2026-10-04.svg)

*(Active repositories per day: Mon 09-28 10, Tue 09-29 6, Wed 09-30 6, Thu 10-01 3, Fri 10-02 5, Sat 10-03 8, Sun 10-04 3. Sunday was missing from gather's daily loop — Melbourne DST spring-forward on 2026-10-04 — and is filled from the same landed scan.)*

---

## Ideas & Innovations

### Observed Authority, Not Another Helper ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
Eleven independent seat-state derivations each “fixed” a symptom. **One `Authority` with explicit unknowns and per-signal freshness; controls only `Get`.** A blank pane cannot prove idle, a disconnected handle cannot prove the broker seat dead, and a queue write cannot refresh liveness.

### The Sidecar Dies With Its Broker ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
A `setsid` sidecar that is never waited becomes the process that outlives every restart, so later token and tool fixes never take effect. **Stdin is a lifeline pipe; kernel EOF on SIGKILL is the destructor; `flock` on `<socket>.lock` is held for process life.** Orphan replacement is SIGTERM then SIGKILL, not unlink-and-hope.

### One Plan Token, Refresh On The Broker ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
Per-seat tokens and sidecar-held refresh secrets made unattended recover a sign-in lottery. **The sidecar holds one access token per plan and never the refresh token; the broker's refresh lock is the only writer; `NoLogin` forbids an interactive prompt from a recover path.**

### Bound Targets, Not Worker Names ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
A remint cap keyed on seat name resets when the worker is renamed — the census cheat that produced a 10σ start spike. **`missionbound` attributes starts to the target id in a durable store, so a rename cannot reset the meter.**

### Untrustworthy, Not Blocked ([marcelocantos/spyder](https://github.com/marcelocantos/spyder))
A failed screen check used to be a gate. **It is now an advisory tag on the evidence: the run continues, the `?` travels with the model verdict, and the owner sees that the model may have judged the wrong screen.** Stock Cars 3.26 folded thirteen screen checks into preconditions on the back of that change.

### Tiles, Not A GOP ([marcelocantos/memento](https://github.com/marcelocantos/memento))
Five minutes of 6K+Retina at 5 fps is ~199 GB of raw frames; a video GOP would make “the screen 30 s ago” a decode. **64×64 tiles, LZ4, keep only what changed, rebuild any retained frame from each tile's newest version at or before *t*.** No delta chain, no keyframe, no I/O until `grab`.

---

## Effort Estimate: Traditional vs. AI-Assisted

A land week: jevons's deferred train, claudia's sidecar-lifetime seal, spyder owner-review, a store live, and two new products. The diversity tax is the story.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| jevons control plane (v0.14–v0.15) | 22-35 | Seat authority with explicit unknowns; git worktree/index CAS; rename-proof remint; reap-vs-park sentinel; claudia pin climb. |
| claudia sidecar lifetime/token/MCP (v0.45–v0.48) | 10-16 | Process-tree lifeline; Keychain vs path seals; OAuth refresh lock; MCP stdio unwedge; clock-seamed tests. |
| spyder Verify owner-review (v0.96–v0.97) | 6-10 | In-place review product; iOS AX vs XCUITest split; DTX retry; 256 KiB model-image budget. |
| Stock Cars 3.26 live (private) | 4-7 | Store path + save-compat vs 3.25; Unity track bulk excluded. |
| memento tile history | 5-8 | ScreenCaptureKit, LZ4 tiles, shared budget, UUID hotplug; live TCC residual. |
| bullseye T94 + worktree IDs | 4-7 | Refuse-before-write; ancestry; uncommitted sibling ledgers. |
| sentinel secrets + SEMS+ | 4-6 | Keychain silent-read; 1Password desktop auth; SEMS signed HTTP. |
| jevons-mobile + mnemo drift + finance + vellum + ytt + sysinfo + ge | 6-10 | Wildcard codesign; sqlift autocommit; chart-path matcher; lazy Mermaid; IOKit temp. |

### The Diversity Tax

Git worktree CAS, OAuth refresh races, iOS SpringBoard automation, ScreenCaptureKit tiling, Unity save compatibility, GoodWe session signing, and SQLite schema-hash repair in one week. No single engineer holds merge-tree flocking, Keychain ACLs, and Play save-key pinning at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| jevons control-plane doctrine | 8-14 | Reopen T766.2 on needle count; file T998 from the 10σ plot; reap-not-park; two `/release` cycles. |
| claudia sidecar lifetime | 6-10 | Stdin-not-setsid; no unattended sign-in; one token per plan. |
| spyder owner-review shape | 4-7 | Advisory not blocking; AX cannot press SpringBoard; owner journey on Stock Cars. |
| Stock Cars 3.26 store | 2-4 | Save-key pin vs 3.25; live on both stores. |
| memento / jevons-mobile / sentinel | 3-5 | Tiles not GOP; wildcard not portal; no Keychain UI from the daemon. |
| bullseye / mnemo | 2-4 | Refuse unless the cited gate holds; transaction around sqlift apply. |

### What If It Were One Person?

The expert band sums to roughly 61-99 person-days. Ramp-up alone on OMP sidecar credentials, git worktree CAS, and iOS alert tapping would dominate a generalist's month. Activity was spread across every weekday (3–10 active repos/day) with no zero day.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~90-140 person-days (~4.5-7.0 months)** |
| Specialist team (traditional) | **~65-105 person-days (~3.3-5.3 person-months)** |
| Actual human effort this week | **~24-40 hours (~3.0-5.0 person-days)** |
| **Multiplier vs. generalist** | **~30-50x** |
| **Multiplier vs. specialist team** | **~20-40x** |

The multiplier peaks on jevons authority/worktrees (the expensive step is refusing Goodhart and owning the integrator lock, not “add a struct”) and on claudia sidecar lifetime (stdin EOF is the destructor). It runs lowest on skills LOC-colouring. The human contribution concentrated on refusals: a census is not done, an orphan sidecar is not a running one, unattended recover is not a sign-in, Verify is not a gate that hides the wrong screen, and an achieve whose cited gate is red is not an achieve.

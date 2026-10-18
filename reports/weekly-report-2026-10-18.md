# Weekly Progress Report — 2026-10-12…18

## Executive Summary

**Twelve repositories** landed **173 commits**. **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** v0.53.0–v0.56.0 (115 commits) lets a seat switch provider or model in place, deletes the tmux backend, warm pool, and legacy CLI seat transport outright, persists request and execution receipts before dispatch, and journals every physical provider attempt — net <span style="color:#cf222e">−13,555</span> lines. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** finally landed its in-flight fleet train as two squash merges (#71, #72): owner-question routing, reap and admission fixes, jevons-mobile folded into `mobile/`, the claudia v0.53 pin, and the tmux pane census removed. **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** (18) supervises one reusable XCTest agent per tethered iPhone and adds leased USB development flags. **[marcelocantos/vellum](https://github.com/marcelocantos/vellum)** v0.27.0–v0.28.0 ships Windows. **[marcelocantos/serviceboard](https://github.com/marcelocantos/serviceboard)** cut v0.1.0. HMS, Stock Cars 3.27, and Minicadeskit moved only on branches: [private week 2026-10-18](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-10-18.md).

**173 commits** | **<span style="color:#1a7f37">+2,412</span> net lines** | **~58-88 person-days traditional equivalent** | **~25-55x multiplier**

> Honesty notes. **(1) claudia and jevons are counted from `origin/master`, not the local checkout.** Both local `master` branches had diverged (claudia 17 ahead / 91 behind; jevons 3 ahead / 68 behind). Sixteen of claudia's seventeen local-only commits are patch-identical to origin commits; the seventeenth (a ledger-only audit commit) is counted. Twenty-one claudia commits authored 10–11 Oct and rebased onto `master` on 13 Oct are **not** counted again — last week's report already covered them. jevons' three local-only commits are content already inside squash #71 and are not counted. **(2) jevons' ℂ is 2** because #71 and #72 are squash merges; #71's body lists 206 squashed items, most written in earlier weeks while the branch was in-flight. **(3) `marcelocantos/think` is left out of every headline figure.** It is a personal knowledge vault that was cloned under the scan root on 18 Oct for the first time; its 123 commits this week are automated YouTube-transcript ingestion (<span style="color:#1a7f37">+505,081</span> lines under `knowledge/youtube/`), not development, and earlier weeks never counted it. A `knowledge/youtube/**` glob is added to `data/line-excludes.yaml` so a future run cannot fold that bulk into ☲. Excluded bulk on the counted repos this week: <span style="color:#1a7f37">+2,586</span>/<span style="color:#cf222e">−136</span> (lockfiles, `bullseye.yaml` ledgers, jevons `docs/audits/**/*.json`, spyder `player/vendor`, xbnf corpora), plus the report series' own `reports/**` and `docs/**`.

### Major Achievements & Innovations

- **A seat switches provider in place** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.53.0) — `Agent.SwitchModel` / `Registry.SwitchModel` replace `SetModel`, `Migrate`, and `MigrateStopped`. A sidecar seat moves from Anthropic to `openai-codex` between turns and keeps its conversation; nothing is summarised and no successor seat starts. The context-transfer migration, its transfer seat, and the migrate wire ops are deleted (61 files, <span style="color:#1a7f37">+976</span>/<span style="color:#cf222e">−3,829</span>). Live tests prove the switched seat recalls an earlier tool result, not just a prompt.
- **The CLI seat era ends** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.53.0–v0.56.0) — every seat runs on the OMP agent core, so the tmux backend, warm pool, Claude tmux ops, and GHA workflows go on 14 Oct (<span style="color:#cf222e">−11,624</span>). About fifteen commits then turned each remaining CLI spawn path into a named refusal — attach, capture, paste, kill-server, the Codex schema probe, a nil Grok billing refresh that had been starting a headless CLI turn — before the legacy CLI seat transport itself was deleted (<span style="color:#cf222e">−8,079</span>).
- **Receipts before dispatch, and every physical attempt journalled** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.54.0–v0.56.0) — identified request and execution receipts persist in seat history before a provider is called, survive interrupted preparation and duplicate admission, and publish into sqlpipe. A pinned pi-ai patch observes Anthropic, Responses, Codex, and Cursor attempts at the request and parser seams, so a retry that vanishes from the final assistant message is still counted, and native compaction is attributed to the active turn.
- **The fleet train lands** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) #71, #72) — owner questions with typed intake, a durable per-question outbox, and a cross-repo open-questions view; reap that leaves blocked and in-progress workers alone; admission counting active process seats; `SIGUSR1` heap and goroutine profiles; jevons-mobile merged under `mobile/`; claudia v0.53.0 pinned and migration removed; tmux pane census and CLI-harness boot plumbing deleted (<span style="color:#cf222e">−8,149</span>).
- **Windows** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum) v0.27.0–v0.28.0) — a pure-Go Windows clipboard (CF_HTML, RTF, Unicode text, PDF, `CF_HDROP`), a Scheduled Task service, drive-letter `file://` URLs, a polling watcher that follows same-directory renames by file identity, and windows-arm64/amd64 zips with a Scoop manifest. v0.27.0 dropped Linux tarballs and releases darwin-arm64 only.
- **serviceboard v0.1.0** ([marcelocantos/serviceboard](https://github.com/marcelocantos/serviceboard)) — first tag: page-height inventory and detail panels, Page Up/Down scrolling with a keyboard journey test, an agent guide, and a root `NOTICE`.

### Significant Progress

- **One XCTest agent per tethered iPhone** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — a healthy runner is reused across authorised clients; idle stops the app under test; a failed lock query or a changed boot id is not "ready"; a detached device is hidden only after its tunnel `DELETE` succeeds. No tag.
- **Leased USB development flags** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — host-local global, group, and exact-app flags reconcile only while fresh physical USB proof and reservation ownership hold; development ad suppression rides renewable, owner- and run-bound leases.
- **Device operations isolated without blocking recovery** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — provider I/O leaves the global handler lock; pipelines serialise by canonical device identity; caller cancellation reaches process discovery, termination, and session setup without restarting a healthy daemon (a 90-second handshake wait cancels in 51 ms).
- **Desired seats reconciled from sqlpipe** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — desired seats, grants, and intents stay Jevons-owned and replicate both ways; the broker applies existing rows before the socket listens and binds only to a control file that already exists. T1074.9 is not achieved.

### Tough Challenges Overcome

- **A billing refresh that started a model turn** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — with no token rotator configured, a Grok 401 fell back to spawning a headless CLI turn, and a nil Cursor model refresh spawned the agent CLI. Both now name the refusal and touch nothing; the same sweep refused every other compiled path that could still start a subscription CLI.
- **Retries that disappear from the bill** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — the final assistant message reports one attempt even when the engine retried. Observation moves to the request and raw-parser seams, keeps invocation, physical attempt, and host delivery as distinct identities through broker replay, and does not count engine aggregates twice.
- **A reboot that never surfaced** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — an idle tick replaced `CondRebooted` with `CondIdle` after the new boot id had been stored. Rebooted now sticks until observed, and the usbmux detach edge hides a device only when `DropTunnel` returns nil.
- **A keyword guard compiled to nothing** ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf)) — the `(?!KEYWORD)` guard sat inside a regular block, where the DFA compiles lookaheads to epsilon, so `IDENT` matched `FROM` and `SELECT a, b, FROM;` parsed. The guard moved outside the block and `KEYWORD` consumes its boundary in-regex.
- **An oracle that crashed was read as a reject** ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf)) — `pyyaml_events.py` exited 1 on a missing PyYAML, so every YAML accept fixture failed as a disagreement. Oracles now exit 125 when they cannot judge, which is `oracle-error`, not `oracle-disagree`.

### Contributors

- Marcelo Cantos (AI co-authors — Claude, Grok, Cursor, Codex — on trailers throughout).

---

## Agent & Fleet Infrastructure

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — In-Place Switch, CLI Era Deleted (115 commits, v0.53.0–v0.56.0)

**The biggest landed effort of the week.** 968 file changes, <span style="color:#1a7f37">+23,961</span>/<span style="color:#cf222e">−37,516</span>. **~282 added test declarations** (Go `func Test` plus sidecar `test(`/`it(`), with many tmux-only tests deleted. Four tags. Counted from `origin/master`; see the honesty note.

- **In-place switch (🎯T195, v0.53.0)**: `SwitchModel` on `Agent` and `Registry`; `set_model` carries a provider. A broker-run seat this host has not attached is refused. A re-attach never fails a working seat over its model. Live: Anthropic → `openai-codex` in place, recalling an earlier tool result.
- **Deletion**: tmux backend, warm pool, Claude tmux ops/adopt, daemon pool grant (refused on the wire), `.github/workflows` (approved 8 Oct) — <span style="color:#cf222e">−11,624</span>. Then about fifteen commits refused each surviving CLI spawn path by name before the legacy CLI seat transport was deleted (<span style="color:#cf222e">−8,079</span>): attach, term-log writer, rewind, capture, paste, the control dial, window probes, `checkTmux`, the Task-surface lookup of subscription binaries, the Codex app-server schema probe. Every fleet provider is proven to launch through the sidecar.
- **Receipts**: identified request receipts persist in seat history and execution receipts persist before dispatch; acceptance is awaited and request state queryable across Go transports; obligations survive interrupted preparation and recovery; active turns survive duplicate and queued admission; a model switch carries no receipt. A closed or unbound turn's id never leaks onto the next send.
- **Usage accounting**: physical attempts observed for Anthropic and Responses, Codex HTTP/WebSocket, and Cursor Run (without inventing billed tokens). Native and mid-turn threshold compaction are attributed to the active turn. Historical generations are discovered through bounded header pages; journal replay is bounded; counters arriving after cancellation are kept. The SDK model cache lives outside the seat directory.
- **Broker and sqlpipe (v0.54.0–v0.56.0)**: desired seats reconciled from the shared sqlpipe pair (requires sqlpipe v0.32.0); broker binds only to an existing `claudia-control.db`; an isolated OMP session adapter keeps embedded credentials and restore under host control. Cursor's model-listed tools now run from the MCP exec frame instead of answering tool-not-found.
- **Plumbing**: Codex task and grant seats get workspace-write; `--workdir` resolves client-side and the daemon rejects a relative one; a spend-limit flag names an exhausted plan but is no veto on its own; `--mode queue` delivers its text. `THIRD_PARTY_NOTICES` is now `NOTICE`.

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Fleet Train Landed (2 squash commits, #71 and #72)

560 file changes, <span style="color:#1a7f37">+21,839</span>/<span style="color:#cf222e">−19,430</span> after the standing `ios/Vendor/**` and `docs/audits/**/*.json` excludes. **~286 added test declarations**. No tag. Previous reports carried this work as in-flight; it is counted once, now.

- **Owner questions (T1028, T404)**: explicit intake for blocked reports and owner gates, a durable per-question blurter outbox with a bounded digest, a cross-repo open-questions view joined to typed blocked reports, defaults and options on a question, answers routed to the asker.
- **Reap and admission (T844, T1024, T1034)**: a seat never reaps another registered seat's process; an active wait on a live external process is not a finish; explicit in-progress or blocked goal status keeps a worker from reap. Admission counts active process seats (default cap 100); durably parked or stopped seats leave the census after the liveness TTL; positive local or broker process evidence fails closed.
- **Stall work (🎯T1067, T1066)**: a restart under the frontier pause starts no auto-spawned workers; a seat's spool records are read without decoding the whole spool; each ledger parses once per content; `SIGUSR1` writes goroutine and heap profiles without stopping the daemon. Intent is re-read at the send-queue drain, not just at admission.
- **Review evidence and gates**: a scoped, versioned review evidence manifest; review detail pinned to metadata under concurrent revisions; CSRF denial distinguished from an answer that failed closed. Gate checks tell negative observations from failed attestations.
- **Integration**: jevons-mobile merged under `jevons/mobile/` (T995) with the native photo picker; claudia v0.53.0 pinned and the migrate tool replaced by `jevons_agent_switch_model`; the tmux pane census and orphan sweep deleted (it had held `agent_list` for 303 s); legacy CLI-harness boot and upgrade plumbing removed; `git reset --hard` / `clean -f` refused when the ledger is dirty (T1011); the restart rate limit removed outright.

### [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) — Jevons Probe Budget (6 commits)

12 file changes, <span style="color:#1a7f37">+278</span>/<span style="color:#cf222e">−42</span>. ~5 new `func Test`. Owner pause is honoured for Jevons monitoring; saturated fleet stalls alert; the cheap probe summarises agent stop reasons and keeps a growing agent feed bounded; failed reviews are budgeted per actionable incident.

### [marcelocantos/serviceboard](https://github.com/marcelocantos/serviceboard) — v0.1.0 (3 commits)

8 file changes, <span style="color:#1a7f37">+280</span>/<span style="color:#cf222e">−25</span>. Page-height panels, eased Page Up/Down that keeps the selection, a keyboard journey test, `agents-guide.md`, and `NOTICE` for the bundled marks.

---

## Devices

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — XCTest Agent, USB Leases (18 commits)

144 file changes, <span style="color:#1a7f37">+12,292</span>/<span style="color:#cf222e">−796</span>. **~115 added test declarations**. No tag.

- **Supervised XCTest agent**: one reusable runner per tethered iOS device, reused across authorised clients; idle stops the launched app and drops the host build session; a non-owner cannot mutate the device. iOS 17+ lock state comes from `devicectl`; an unknown lock is not ready.
- **USB development flags**: global, group, and exact-app flags with explicit acknowledgements, bounded writes, and expiring app leases; healthy peer ACKs publish without waiting on slower peers. `SPYDER_DATA_DIR` isolates state without changing device identity.
- **Cancellation**: process reads cancel without evicting a replacement service generation; session waits cancel without restarting a healthy daemon; a standing real-daemon desktop REST gate. The uncancellable go-ios RPC remains 🎯T160.2.
- **Diagnostics and honesty records**: one log schema across Android and iOS captures, with device time and host receipt as separate clocks. An unresolved physical test-runner startup outage (`RSD/XPC STREAM_CLOSED`) is recorded without claiming a repair, and XCTest biometric consent is kept distinct from runner readiness.

---

## Libraries & Documents

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — Windows (12 commits, v0.26.1, v0.27.0, v0.28.0)

73 file changes, <span style="color:#1a7f37">+1,724</span>/<span style="color:#cf222e">−213</span>. ~13 new `func Test`.

- **Windows core and platform layer**: build tags detached; `%APPDATA%` config; Explorer reveal; npm shim exec; drive-letter view paths and `file://` URLs; `filepath.IsAbs` checks; pure-Go clipboard (`clipboard_windows.go`, CF_HTML, RTF, Unicode text, PDF, `CF_HDROP`); `install-service` as a Scheduled Task; global KaTeX lookup.
- **Packaging**: windows-arm64/amd64 zips with checksums and a Scoop manifest (the repo is its own bucket); hygiene enforces release platforms. v0.27.0 releases darwin-arm64 only and drops Linux. v0.26.1 (13 Oct) bumped `yaml.v3` and `x/sys`.

### [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) — Reject Fixtures and Attestations (12 commits)

20 file changes, <span style="color:#1a7f37">+167</span>/<span style="color:#cf222e">−126</span>. No tag. T28, T37, and T38 achieved with attestations. SQL keywords reserved so `IDENT` rejects them, with trailing-comma and unbalanced-paren reject fixtures (`pg_query` agrees on the latter). An oracle that cannot run is `oracle-error`. The sandbox languages page sends non-UTF-8 fixtures as raw bytes. Staticcheck clean-ups; dead case-fold helpers dropped.

---

## Ledger-Only Commits

**[marcelocantos/finance](https://github.com/marcelocantos/finance)**, **[marcelocantos/tapper](https://github.com/marcelocantos/tapper)**, and **[marcelocantos/ytt](https://github.com/marcelocantos/ytt)** each landed one commit filing keychain and hardened-runtime targets from the 17 Oct audit (the same commit also landed in claudia, sentinel, and spyder). These touch only `bullseye.yaml`, so they count toward ℂ and not ☲. The two report repos each carry last week's publish.

---

## Commercial

Nothing commercial landed on a default branch.

**[Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms)** — 379 in-flight commits. Gather's in-flight ☲ is <span style="color:#1a7f37">+9,778,715</span>/<span style="color:#cf222e">−166,787</span>, dominated by generated retranslation; it is not a product size and was not split this run. Subjects cluster on `Hms.Vcl`, form census, navigation, and a browser deployment. Full narrative: [private week 2026-10-18](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-10-18.md).

**[minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing)** — 88 in-flight commits on a 3.27 release branch, <span style="color:#1a7f37">+81,129</span>/<span style="color:#cf222e">−1,171</span>. **[minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit)** — 14 in-flight. Same private companion.

**[squz/ge](https://github.com/squz/ge)**, **[squz/yourworld2](https://github.com/squz/yourworld2)**, and **[squz/multimaze2](https://github.com/squz/multimaze2)** had no landed or substantive in-flight work.

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **Health-Management-Systems/hms** — 379 in-flight. See Commercial.
- **minicadesmobile/stock-car-racing** — 88 in-flight. See Commercial.
- **marcelocantos/den** — 17 in-flight, <span style="color:#1a7f37">+6,674</span>/<span style="color:#cf222e">−699</span>. Continuation of last week's Linux bottle relocation.
- **minicadesmobile/Minicadeskit** — 14 in-flight. See Commercial.
- **marcelocantos/mnemo** — 8 in-flight, <span style="color:#1a7f37">+4,885</span>/<span style="color:#cf222e">−273</span>.
- **arr-ai/arrai** — 6 in-flight, <span style="color:#1a7f37">+1,353</span>/<span style="color:#cf222e">−15</span>.
- **marcelocantos/sqlpipe** — 5 in-flight; **marcelocantos/cv** — 2 in-flight (the PR behind v0.11.0); **marcelocantos/sqldeep**, **mcpsafe**, **slacker**, **squz/ge** — stash or zero-file entries only.
- Gather's in-flight lines for claudia (97) and jevons (230) are not used here: with local `master` diverged, they mostly re-count commits that are already on `origin/master`.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** commits within 2026-10-12…18 — local default branch for most repos, `origin/master` for claudia and jevons (see the honesty note). `marcelocantos/think` is excluded. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **12** |
| Total landed commits | **173** |
| Total lines added (landed, filtered) | <span style="color:#1a7f37">+60,578</span>‡ |
| Total lines removed (landed, filtered) | <span style="color:#cf222e">−58,166</span>‡ |
| Net new lines (landed, filtered) | <span style="color:#1a7f37">+2,412</span>‡ |
| File changes | 1,789 (summed per commit; a path touched twice counts twice) |
| New files created | 422 unique paths after the same excludes |
| Bulk paths excluded from ☲ | <span style="color:#1a7f37">+2,586</span>/<span style="color:#cf222e">−136</span> on counted repos (standing globs), plus `reports/**` and `docs/**` on the two report repos |
| Releases published | **8** (claudia v0.53.0, v0.54.0, v0.55.0, v0.56.0; vellum v0.26.1, v0.27.0, v0.28.0; serviceboard v0.1.0) |
| Languages | Go, TypeScript, Dart, Swift, Kotlin, Python, JavaScript, Shell, Markdown, YAML, JSON |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. claudia and jevons were recounted per commit with the same pathspecs gather uses; spyder's recount matched gather exactly. **New this run:** `marcelocantos/think` `knowledge/youtube/**`. The think repo is out of the headline regardless.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 115 | 968 | <span style="color:#1a7f37">+23,961</span> | <span style="color:#cf222e">−37,516</span> | <span style="color:#cf222e">−13,555</span>* |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 18 | 144 | <span style="color:#1a7f37">+12,292</span> | <span style="color:#cf222e">−796</span> | <span style="color:#1a7f37">+11,496</span> |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 12 | 73 | <span style="color:#1a7f37">+1,724</span> | <span style="color:#cf222e">−213</span> | <span style="color:#1a7f37">+1,511</span> |
| [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) | 12 | 20 | <span style="color:#1a7f37">+167</span> | <span style="color:#cf222e">−126</span> | <span style="color:#1a7f37">+41</span> |
| [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) | 6 | 12 | <span style="color:#1a7f37">+278</span> | <span style="color:#cf222e">−42</span> | <span style="color:#1a7f37">+236</span> |
| [marcelocantos/serviceboard](https://github.com/marcelocantos/serviceboard) | 3 | 8 | <span style="color:#1a7f37">+280</span> | <span style="color:#cf222e">−25</span> | <span style="color:#1a7f37">+255</span> |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 2 | 560 | <span style="color:#1a7f37">+21,839</span> | <span style="color:#cf222e">−19,430</span> | <span style="color:#1a7f37">+2,409</span>† |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 1 | 3 | <span style="color:#1a7f37">+33</span> | <span style="color:#cf222e">−18</span> | <span style="color:#1a7f37">+15</span> |
| [marcelocantos/progress-reports-private](https://github.com/marcelocantos/progress-reports-private) | 1 | 1 | <span style="color:#1a7f37">+4</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+4</span> |
| [marcelocantos/finance](https://github.com/marcelocantos/finance) | 1 | 0 | <span style="color:#1a7f37">+0</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+0</span> |
| [marcelocantos/tapper](https://github.com/marcelocantos/tapper) | 1 | 0 | <span style="color:#1a7f37">+0</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+0</span> |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 1 | 0 | <span style="color:#1a7f37">+0</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+0</span> |

\* *`origin/master`, commits authored 12–18 Oct, plus one unpushed ledger commit. 21 rebased commits authored 10–11 Oct are excluded as already reported.*

† *Two squash merges (#71, #72) carrying work previously reported as in-flight.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~286 | Owner questions, reap/admission, review evidence, gates, history anchoring |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~282 | Receipts, usage observation, in-place switch, sidecar policy; many tmux tests deleted |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~115 | XCTest supervision, USB leases, cancellation, diagnostics |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | ~13 | Windows clipboard, service, paths |
| [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) | ~5 | Probe budget and pause |
| [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) | ~1 | Oracle-error classification |
| **Total** | **~702** | Gross added `func Test` / `test(` / `it(` lines in the landed diff. jevons' figure spans the whole squashed train. |

### Daily Activity

![Daily active repositories](daily-activity-2026-10-18.svg)

*(Active repositories per day, landed commits by commit date: Mon 10-12 5, Tue 10-13 4, Wed 10-14 5, Thu 10-15 2, Fri 10-16 3, Sat 10-17 3, Sun 10-18 7. The README timeline counts all-branch activity by author date, so its days for this week are higher and include the `think` vault.)*

---

## Ideas & Innovations

### Switch the Model, Keep the Conversation ([claudia](https://github.com/marcelocantos/claudia))

Migration had meant a summary, a successor seat, and a transfer seat to carry the context between them. Once every seat runs on one agent core, **the provider is a property of the next turn, not of the process** — `SwitchModel` changes it between turns and the conversation stays where it is. The whole migration apparatus is deleted rather than kept as a fallback, and the live test asks the switched seat about an earlier tool result to prove it.

### Refuse First, Delete Second ([claudia](https://github.com/marcelocantos/claudia))

Removing a transport while callers still reach it turns a deletion into an outage hunt. **Each surviving CLI spawn path was first made to fail with a named refusal and a test**, one family per commit, until nothing reached the code; only then was the CLI transport removed. The refusals also surfaced the paths nobody listed — a billing refresh and a model refresh that each started a CLI turn.

### Count the Attempt, Not the Answer ([claudia](https://github.com/marcelocantos/claudia))

A provider's final message describes the answer, not how many requests produced it. **Observation sits at the request and raw-parser seams, with invocation, physical attempt, and host delivery kept as separate identities**, so a retry that disappears from the final message is still on the journal and an engine aggregate is never added on top.

### A Receipt Before the Call ([claudia](https://github.com/marcelocantos/claudia))

If a request is recorded after dispatch, a crash between the two leaves a provider call with no owner. **Request and execution receipts are persisted in seat history before dispatch**, and acceptance is awaited, so recovery can tell a request that never left from one that is still running.

### A Lease, Not a Setting ([spyder](https://github.com/marcelocantos/spyder))

Development switches — suppress ads, pin orientation — are dangerous when they outlive the session that wanted them. **Each flag is a lease bound to fresh physical USB proof and the reservation's owner**, renewed while the test runs and gone when the cable or the owner is.

### An Oracle That Cannot Run Has No Opinion ([xbnf](https://github.com/marcelocantos/xbnf))

A crashed oracle that exits 1 looks exactly like a reject. **Exit 125 means "cannot judge"**, which the harness reports as `oracle-error`, so an environment without PyYAML can no longer fail every YAML accept fixture as a parser disagreement.

---

## Effort Estimate: Traditional vs. AI-Assisted

A week of subtraction and landing. claudia removed more than it added; jevons' long branch reached `master`. The fleet was stopped on 14 Oct while token use was investigated, and much of the second half of claudia's week is accounting and refusal work that bears on that. jevons is estimated on what its squash merges carry, since none of it was counted while in-flight.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| claudia v0.53–v0.56 | 12-18 | In-place provider switch with conversation continuity; refusing then deleting a transport the fleet still touched; pre-dispatch receipts through recovery; attempt-level usage at parser seams; sqlpipe desired-seat reconcile. |
| jevons fleet train (#71, #72) | 13-20 | Owner-question lifecycle across repos; reap and admission classifiers that must not kill live work; stall diagnosis and profiling; mobile shell merge; removing tmux and CLI-harness plumbing from boot and upgrade. |
| spyder XCTest + USB leases | 8-12 | Reusable XCTest runner supervision; lock and reboot truth on iOS 17+; leased development flags tied to USB proof; cancellation through go-ios without evicting replacements. |
| vellum Windows | 4-6 | Win32 clipboard formats in pure Go; Scheduled Task service; drive-letter URLs; rename-following poll watcher; Scoop packaging. |
| xbnf, sentinel, serviceboard v0.1.0, audit ledgers | 3-6 | DFA lookahead placement; oracle exit semantics; probe budgeting; first release docs; filing keychain targets across repos. |

### The Diversity Tax

Agent-runtime internals (provider SDK seams, compaction, receipts), fleet scheduling and reap policy, iOS device automation (XCTest, `devicectl`, usbmux), Windows clipboard and service APIs, and parser-generator semantics. The skills that make a deletion of 20,000 lines safe are not the ones that make a Windows clipboard paste correctly.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| claudia | 5-8 | In-place switch over migration; delete rather than keep the CLI path; GHA removal; four releases; usage accounting during the fleet stop. |
| jevons | 3-5 | Merge-plan sign-offs (T995, T1020), owner-question design, landing the train. |
| spyder | 2-4 | Physical device runs; refusing to claim a startup repair; biometric consent kept separate. |
| vellum | 1-2 | Windows scope, Linux dropped, release cuts. |
| xbnf, sentinel, serviceboard, audit | 1-2 | Attestations, probe policy, first serviceboard tag, keychain audit. |

### What If It Were One Person?

The expert band sums to roughly 40-62 person-days. A generalist would add ramp-up on the OMP agent core and pi-ai internals, XCTest supervision, and Win32 clipboard formats, and pay a context-switching tax across four platforms. Landed activity ran every day (2–7 repos), heaviest on Sunday.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~58-88 person-days (~2.9-4.4 months)** |
| Specialist team (traditional) | **~40-62 person-days (~2.0-3.1 person-months)** |
| Actual human effort this week | **~12-21 hours (~1.5-2.6 person-days)** |
| **Multiplier vs. generalist** | **~25-55x** |
| **Multiplier vs. specialist team** | **~15-40x** |

The multiplier is highest on claudia's refusal sweep and on jevons' squashed train, where the expensive part is the volume of careful, tested change, and lowest on the Windows release, where on-machine judgement dominates. The human contribution concentrated on removal and restraint: a migration is not needed when the model can switch, a code path that can start a model turn from a billing refresh is refused, a startup outage is recorded rather than declared fixed, and a branch's work is counted once, when it lands.

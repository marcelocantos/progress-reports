# Weekly Progress Report — 2026-08-10…16

## Executive Summary

**Seven repositories** landed **263 commits** — the second-largest week of the series by commit count, almost entirely the fleet turning on its own survival. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** (158 commits) absorbed a real host-down incident: on 15 August a 128 GB machine sat at load **267** with **0.14 GB free**, not because the CPUs were busy but because the kernel was compressing ~2 GB/s of a **ghost Claude fleet**. Claudia's tmux windows survive the consumer; every jevonsd bounce rematerialised the roster into new processes and left the old ones running. The product contract is now three-valued — drain, start, upgrade — and only upgrade adopts leftovers. The daemon and a launchd watchdog then supervise **each other** from different process trees, after launchd quietly dropped the job fourteen minutes after install and nothing noticed for five days. Last week's context ceiling, which had shipped and done nothing on Claude, started working once cached reads were counted as context — and immediately revealed a treadmill, five rotations in 23 minutes, closed with hysteresis. **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** (48 commits, v0.21.0) added a Codex provider, a capability matrix that **refuses** fields a path cannot honour, leftover-window `Adopt`, and the start of a tiered runtime whose rule identity is a content hash. **[marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)** v0.45.0 ended a UTF-8 hang and stopped concurrent agents amending each other's ledger SHAs. **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** v0.79.0 added `wait_state` and an allowlisted `device_setting`. **[marcelocantos/vellum](https://github.com/marcelocantos/vellum)** found that AppKit's HTML importer is a per-user launchd agent, not a library, and falls back to pandoc when that agent is unreachable. Commercial project detail: [private week 2026-08-16](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-16.md).

**263 commits** | **+73,131 net lines** | **~48-76 person-days traditional equivalent** | **~40-70x multiplier**

> Honesty note: no new `data/line-excludes.yaml` entries this run. Headline ☲ is gather `landed:` after the existing globs. Excluded bulk this week is **+5,333/−614** (lockfiles, `bullseye.yaml`, and the standing per-repo trees). jevons +45,282 and claudia +28,966 were checked: authored Go, vanilla JS, Rust tests, and small JSON/JSONL fixtures — no new golden or generated corpus.

### Major Achievements & Innovations

- **Crash-survival is not recovery** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T40.1, [marcelocantos/claudia](https://github.com/marcelocantos/claudia) 🎯T34) — Claudia's tmux substrate keeps an agent alive if the consumer dies, which is true and was the entire problem: there was no `Adopt`, `Registry.Stop` was a silent no-op without an in-memory handle, and every bounce called `Launch`. One day's log held ~500 `agent started` events against ~24 live agents, 46 tmux windows and 65 `claude` processes. Containment (watchdog `bootout`) dropped compression from 1,136 MB/s to zero and freed 19 GB without touching Bitdefender, Parallels or ollama. The contract now distinguishes drain, cold start and upgrade: only an upgrade handoff carrying `TmuxWindowID` adopts; ordinary start leaves leftovers visible so an exit leak cannot hide behind the next boot.
- **The daemon and the watchdog supervise each other** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T405) — on 10 August a worker's restart killed the daemon, the daemon's shutdown killed every agent including that worker, and the restart script died five seconds before starting the replacement. A launchd watchdog now probes the port from outside every process tree a restart tears down; the daemon then supervises the watchdog, because launchd dropped the job fourteen minutes after install, the plist still looked healthy, and five days of daemon bounces produced not one alarm. Loaded is not running; a late probe is not a gap; a reinstatement carries the installed plist's `PATH` rather than the detached daemon's environment.
- **A ceiling that could not see Claude's cache** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T392.1) — Grok reports `inputTokens` inclusive of cached reads; Claude reports `input_tokens` fresh-only. Both call sites read `Usage.Input` directly, so last week's ceiling shipped at 22:55 on 9 August and did nothing: mean context *rose* to 205k under a 100k cap, the overseer at 346k per call. The new test uses a real Claude frame (12 fresh, 300k cached, 5k created → 305,012 and a compact verdict). The moment it started working, the overseer rotated five times in 23 minutes — a successor re-reads the predecessor's transcript, re-exceeds, rotates again — closed with `VerdictHold` hysteresis, because a ceiling only helps an agent whose context grows *through* it.
- **Plan remaining is the one honest budget a flat subscription has** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T390, [marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.21.0) — claudia now publishes session and weekly remaining across Claude and Codex (Grok and Bedrock return explicit unavailable, never invented numbers). `PlanRemaining` is a `*float64` because **0 means exhausted and nil means unpublished**, and collapsing those two is how admission reported 100% headroom on an account already at its limit. The cockpit draws the remaining as compact bars.
- **Codex as a fourth provider, and every field a path cannot honour is refused** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.21.0, 🎯T24) — Codex Task over `codex exec` with subscription-auth preflight that fails closed on API-key fall-through; model selection fails loud rather than hanging. The capability audit found Grok Session dropping `DisallowTools` and hardcoding always-approve, Bedrock accepting a `SessionID` against a stateless API, and every non-Codex path accepting `SandboxMode` and running unrestricted. `capabilityRefusal` keeps the refusal alive even if a claim flips to supported ahead of the wiring.
- **bullseye v0.45.0 — a UTF-8 hang, and a ledger SHA that stays reachable** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)) — subprocess output that was not valid UTF-8 hung the server; subprocesses are now bounded. Separately, amend eligibility inferred from "HEAD is unpushed and touches only `bullseye.yaml`" let concurrent agents rewrite each other's commits — four amends in under three minutes on 15 August orphaned SHAs already cited as evidence. Ownership is now a process-local record of `git rev-parse HEAD` after each of *this* process's ledger commits.
- **spyder v0.79.0 — wait for a slice, set only allowlisted device keys** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) 🎯T129/🎯T130) — `wait_state` polls an app-channel slice until a jq select is truthy and returns the satisfying value; a timeout carries the last observed slice rather than a bare "timed out". `device_setting` pins and restores Android refresh rate without host `adb`; unknown keys never reach a shell; iOS fails closed.

### Significant Progress

- **A tiered runtime whose identity is a content hash** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) 🎯T27) — the model is the escalation path, not the entry point. Procedural rules and episodic journal are sibling stores (losing rules is amnesia; losing episodes costs only future opportunity). Identity is a content hash of the serialised form, not a version counter; recall is a seam the consumer scores, because claudia will not acquire an embedding model; consolidation returns candidates and installs nothing.
- **Host pressure is a first-class admission dimension** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T463) — at the incident, capacity reported `pressure: normal, headroom 100%` at load 247 with swap pinned. The host run-queue and swap occupancy now fold into the existing pressure ladder; `0` on a provider cap is unpublished, not unlimited. Owner turns stay exempt.
- **A gate's exit status comes from the gate** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T386/🎯T396) — `go test ./... | tail -20` reports tail's success. Twice in one session that turned a timeout-panic into a cited green. `bin/gate` runs the command as a process — no shell, no pipeline — and a zero exit over `FAIL`/`panic` output is SUSPECT, never GREEN.
- **Treeguard on every write path, not just the Write tool** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T391) — `cat >`, `tee`, `sed -i` walked straight past a hook that only saw Claude's Write/Edit. Bash classification, a journal that reports losses only, and a pre-commit coverage notice (the one boundary every provider crosses).
- **Cockpit virtual list that actually virtualises** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T119) — a 280k-line journal had become ~11k DOM nodes; scroll was cheap and clicks waited on a full-flow layout flush. An absolute canvas with a viewport-band cap, parked real elements on detach, and one `applyWireEvent` for every agent.
- **A mid-turn paste is submitted or reported, never "Message sent"** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) 🎯T28/🎯T30) — `classifyComposer` tested turn chrome *before* the composer, so the previous turn's spinner satisfied both gates before the paste rendered. The composer is read first; "Press up to edit queued messages" is the mid-turn submit evidence, not chrome.
- **AppKit's HTML importer is a process** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum) 🎯T23) — on macOS 26, `NSAttributedString` HTML init brokers to `com.apple.textkit.nsattributedstringagent`. Outside a GUI session — which is how vellum runs behind the Aperture gateway — every conversion failed. Convert and write are now separate; the fallback to pandoc is named on the result, not silent.

### Tough Challenges Overcome

- **A machine that looked CPU-bound and was not** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)) — userland wanted ~60% of a 16-core host; the rest of the stall was the compressor at ~2 GB/s. RSS never added up to 128 GB once pages were compressed. The first theories (Bitdefender, ollama, 64 leaked `zsh` burners from a botched load-generator) were measured and dropped; the machine recovered when the fleet was stopped and nothing else changed.
- **Units that matched one provider and were catastrophic for the other** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)) — described above. Both fixtures were Grok-only. A test that only exercises the provider whose units happen to match cannot detect a units bug.
- **A supervisor whose absence produced no alarm** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)) — launchd stopped holding the watchdog; the plist on disk was perfect; the owner found it by asking. Mutual supervision from different process trees is the only shape that survives "the supervisor is what broke".
- **Turn chrome is evidence that *some* turn is running** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — briefing a busy agent is the ordinary fleet case, so the previous turn's chrome is already on the pane. Two fixtures labelled "queued" were this bug, caught on camera a day before it was filed, and had made the chrome-first rule look safe.
- **A launchd agent, not a framework call** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum)) — `pbcopy` kept working, so the pasteboard was fine. The paired sandbox oracles (deny TextKit agent → pandoc; deny WindowServer → still AppKit) pin the cause to that one mach service and refute "AppKit needs a GUI session".
- **Four amends in three minutes, evidence already dead** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)) — the store was never at risk (flock + CAS). What died was the ability to re-check a claim from its cited SHA, which is the fleet's verification currency.

### Contributors

- Marcelo Cantos (AI co-authors — Claude Opus 5, Grok, and other Claude models — appear on `Co-authored-by` trailers throughout; most of the jevons and claudia landing was done by the supervised fleet).

---

## Agent & Fleet Infrastructure

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — The Fleet Survives Itself (158 commits)

**The biggest effort of the week.** No version tag; the daily daemon is the product. 540 file changes, **+45,282/−5,417**, ~304 net new test declarations. The incident, adopt contract, mutual supervision, ceiling units, hysteresis, plan remaining and host admission are above. Also landing:

- **Rotation is not migration** (🎯T392.1.1) — a successor gets a bounded brief (last turns, promises, open threads under a hard token cap), not a transcript walk. Same-provider rotations never use the provider-switch seed; last-rotation is persisted so a SIGHUP cannot compact-now on a just-migrated overseer.
- **Send is confirmed from the receiver** (🎯T416) — four callers, one root. Transcript growth and raw-file text match both passed while wrong; each is now killed by its own fixture. A send is begun when the agent says so.
- **Convergence exhaustion notifies from deterministic code** (🎯T415) — a diagnostician that outlives the daemon, bounded and self-reporting; a stuck agent is left alone rather than doubled.
- **Worktrees reaped from outside the process that leaks them** (🎯T440) — a half-deleted worktree is a corpse, not somebody's work.
- **An idle product owner on a kickable frontier is a fault** (🎯T380), not sleep. The sentinel (🎯T407) distinguishes a blocked fleet (auth/quota, auto-spawn paused) from an unattended stall, and does not tell the PO to spawn into a wall.
- **A 15 August host-RAM post-mortem** committed as product doctrine, including the three things the incident is *not* a licence to do: reap on ordinary start, make adopt the default of `Launch`, use process groups as cleanup (agents are children of the claudia tmux server; `cmd/detach` exists so a group sweep of the caller cannot reach them).
- **Cockpit**: grouped plan bars with time-pace triangles, weekly waste coloured continuation-versus-locked, one widget owning grow-and-send on main and sidebar, size-only bubble clip, thumbs reserved at 120 px before load so the virtual-list prefix does not jump.

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Codex, Refusal, Adopt (48 commits, v0.21.0)

v0.21.0 is Bedrock + Codex + `QueryPlanUsage`. The capability-refusal matrix, leftover-window `Adopt`, paste-submit evidence and the T27 ladder are above. Additionally:

- **Broker Unix socket** (🎯T2.1) — parked wire contract inherited; spawn/release/tail over a bound socket rather than a hidden side channel.
- **A wall clock may bound cleanup, never decide a verdict** (🎯T31) — hermetic oracles had been asserting that this machine, right now, is fast enough. Readiness is now a signal the fake or the product emits, or it is unbounded; `go test -timeout` is the single hang backstop.
- **Ordinary `Launch` does not reap leftovers** (🎯T34) — the first cut reaped; the incident write-up forbade it. Isolated-tmux oracles: leftover+`Launch` = 2 windows; `Adopt` keeps the same window id; `StartAll`+`StopAll` leaves zero of what *this* process started.
- **268 file changes**, **+28,966/−2,537**, **~316 net new tests**.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Hang, Bounds, SHA Stability (3 commits, v0.45.0)

Covered above. The published-release probe refuses to run under `BULLSEYE_REACHABILITY_CHECK=skip` (this job *is* the enforcement point). **30 new tests**; +3,682/−487 across 33 files.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Drop the Jevons Peer (3 commits)

mnemo no longer dials jevonsd or speaks the provider contract (🎯T147). Generic `/health` and `/mcp` stay; Jevons is not a dependency. −747 lines of peer code.

---

## Tooling & Workflow

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Wait and Device Settings (1 commit, v0.79.0)

Covered above. Live-proven on a named iPhone and an Android serial in CI. **15 new tests**; +1,336/−18 across 25 files.

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — TextKit Agent Fallback (4 commits)

The AppKit/pandoc split is above. Alongside it, advertised MCP tool names are checked against the registered set over an in-memory transport, so a second place to name tools cannot resurrect `convert_to_clipboard` after the four-tool collapse. Instructions are declared empty on purpose. **9 new tests**; +865/−73.

---

## Commercial

### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-08-16](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-16.md).*

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **marcelocantos/claudia** — 7 commits in-flight; **marcelocantos/jevons** — 1; **marcelocantos/skills** — 2; **marcelocantos/ytt** — 2.
- **Health-Management-Systems/hms** — 1 in-flight; detail in [private week 2026-08-16](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-16.md).

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-08-10…16. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **8** |
| Total landed commits | **263** |
| Total lines added (landed, filtered) | +82,797‡ |
| Total lines removed (landed, filtered) | −9,666‡ |
| Net new lines (landed, filtered) | +73,131‡ |
| File changes | 953 |
| New files created | 345 |
| Bulk paths excluded from ☲ | +5,333 / −614 (lockfiles, `bullseye.yaml`, standing per-repo globs) |
| Releases published | **3** (claudia v0.21.0, bullseye v0.45.0, spyder v0.79.0) |
| Languages | Go, JavaScript, Rust, C#, Starlark, Python, TLA+, HTML, YAML, Markdown |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. No new globs this run.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 158 | 540 | +45,282 | −5,417 | +39,865 |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 48 | 268 | +28,966 | −2,537 | +26,429 |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 45 | 68 | +2,666 | −387 | +2,279 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 3 | 33 | +3,682 | −487 | +3,195 |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 4 | 13 | +865 | −73 | +792 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 1 | 25 | +1,336 | −18 | +1,318 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 3 | 6 | +0 | −747 | −747 |
| minicadesmobile/Minicadeskit | 1 | 0 | +0 | −0 | 0† |

† *target-ledger update only — machine-written, excluded from ☲.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~316 | Codex hermetic exec, capability-refusal matrix, Adopt leftover windows, T28/T30 pane-frame oracles, T31 signal-not-deadline waits, ladder/memory |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~304 | watchdog/supervise mutual oracles, Claude-shaped ctxcap frame, hysteresis hold, host-saturation admission, gate false-green, virtual-list attach |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 30 | SHA-stability with `git merge-base --is-ancestor` from a second process, reachability, CLI parity |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 15 | `wait_state` jq select, allowlisted `device_setting`, iOS fail-closed |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 9 | paired sandbox-exec TextKit/WindowServer oracles, advertised-name reflection walk |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 4 | carousel wall-time pump |
| **Total** | **~678** | landed only; net growth in test declarations across the window |

### Daily Activity

![Daily active repositories](daily-activity-2026-08-16.svg)

*(Active repositories per day: Mon 08-10 3, Tue 08-11 1, Wed 08-12 0, Thu 08-13 0, Fri 08-14 0, Sat 08-15 4, Sun 08-16 6. Wednesday through Friday are empty — the incident and the bulk of the landing concentrated on the weekend.)*

---

## Ideas & Innovations

### Crash-Survival Without Recovery ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
Keeping a child alive after its consumer dies is usually sold as robustness. Here it was the defect. Claudia's tmux windows survive by design; jevonsd restart had no way to *reacquire* them, and `Stop` consulted a map that is empty after every bounce, so **every restart doubled the fleet**. The missing primitive was not a more thorough kill — ordinary start is deliberately forbidden from reaping, so an exit leak stays visible — but a third intent, upgrade, whose handoff names the window to adopt. Survival and recovery are different properties; shipping the first without the second is how a 128 GB host fills with ghosts.

### 0 Is Exhausted, Nil Is Unpublished ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
A flat subscription has one number that is not an estimate: how much of the plan is left. The moment that reading is stored as a `float64`, **zero and missing collapse**, and admission reports 100% headroom on an account already at its limit — the same shape as last week's "unknown never compacts", applied to budget. Making `PlanRemaining` a pointer, and making Grok/Bedrock return explicit unavailable rather than an invented zero, is what lets the cockpit draw a bar that means something.

### Count What the Other Provider Bills ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
A units bug that only exists on one of two providers will pass every test written against the other. Grok's `inputTokens` already includes cached reads; Claude's `input_tokens` does not. Reading `Usage.Input` at both call sites made the spend report look absurd (0.1M input, 3912% output ratio) *and* made the ceiling inert — the worse failure, because the numbers were not obviously broken, only quietly small. **The oracle earned its place**: four levers were reported as landed, and measuring the shipped path against the frozen baseline was the only thing that said one of them was doing nothing.

### A Ceiling Must Not Become a Treadmill ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
Once the units bug was fixed, the overseer rotated five times in 23 minutes and then stayed down, taking owner chat with it. Compaction hands the successor the predecessor's transcript; an agent whose steady state *lives above* the ceiling therefore rotates, re-reads, re-exceeds, rotates again. **A ceiling only helps an agent whose context grows through it.** `VerdictHold` is deliberately not `VerdictOK`: a persistent hold is a configuration signal, logged at WARN, rather than passing silently as healthy.

### Mutual Supervision from Different Trees ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
A watchdog that the daemon starts inside its own process tree dies with the daemon. A watchdog that launchd holds, with no one watching launchd, dies silently while its plist still looks perfect. The working shape is two processes that cannot share a fate: the watchdog probes the port from outside every tree a restart tears down; the daemon checks that launchd still holds the job *and* that the job still probes. **Loaded is not running** — a job whose binary dies on start is held forever and probes never.

### The Importer Is Another Process ([marcelocantos/vellum](https://github.com/marcelocantos/vellum))
`NSAttributedString` HTML init looks like a framework call and is a round-trip to `com.apple.textkit.nsattributedstringagent`. A sandboxed or non-GUI context cannot look that agent up, so every conversion fails while `pbcopy` keeps working. Splitting convert from write lets the conversion take another route; naming the route on the result stops a quiet rescue from becoming a permanent invisible degradation. The paired sandbox oracles — deny TextKit, stay on pandoc; deny WindowServer, stay on AppKit — are what make the first arm mean anything.

### A Wall Clock Is Not a Verdict ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
A 5 s readiness wait and a 200 ms scheduling allowance do not assert a product property. They assert that this machine, under this load, is fast enough — and on 15 August, under a drowning host, they produced a RED for work the suite never exercised. Widening the constant only moves the load at which it fires. The replacement is causal: wait for the event the product emits, or do not decide; `go test -timeout` is the hang backstop, once per suite, with every goroutine dumped.

---

## Effort Estimate: Traditional vs. AI-Assisted

A narrower week than the last — no new product, almost no game-engine work — and structurally the same: the fleet spent the week making its own continued existence a property rather than a hope, then landing the findings of a host that had already run out of RAM.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| jevons ghost-fleet adopt + mutual supervision | 5-8 | Process-lifecycle contracts across tmux, launchd and a consumer that must not reap on start; the missing property was recovery, not a more thorough kill. |
| jevons ctxcap units, hysteresis, bounded brief | 3-5 | Two providers' billing frames disagree about what "input" includes; the follow-on treadmill is a design flaw the units bug had been hiding. |
| jevons plan remaining + host admission | 2.5-4 | Pointer-versus-value honesty on a budget reading, plus folding host run-queue and swap into a ladder that must not halt the owner. |
| jevons cockpit virtual list / transcript IR | 3-5 | Absolute-canvas virtualisation of a 280k-line journal without destroying parked chrome on page-up. |
| jevons gates, write paths, worktrees, send confirmation | 4-6 | Making a green un-fabricable by construction; extending treeguard past the Write tool; confirming a send from the receiver. |
| claudia T27 tiered ladder + memory | 6-10 | A runtime whose model is the last rung, with content-hash identity, a consumer-owned scorer, and episodic/procedural stores that must not share a lock. |
| claudia Codex, Bedrock plan-usage, T24 refusal | 3-5 | A fourth provider plus a matrix that fails closed on every field a path cannot honour, including the ones the audit found after the known two. |
| claudia paste-submit evidence + leftover Adopt | 2.5-4 | Terminal chrome is not this-send evidence; leftover windows are an upgrade input, never a Launch default. |
| bullseye UTF-8 hang + SHA stability | 2-3 | Bounded subprocesses, and amend ownership that cannot be inferred from the changed-file set under concurrent agents. |
| spyder wait_state + device_setting | 1-1.5 | A timeout that returns the last slice; an allowlist that never reaches the shell. |
| vellum TextKit-agent fallback | 1-2 | Identifying a launchd agent as the real importer, then proving it with a paired sandbox that refutes the rival explanation. |
| mnemo drop Jevons peer | 0.3-0.5 | Deleting a coupling. |
| Client work (private) | 4-7 | Detail in the private companion. |

### The Diversity Tax

This week spans Go (jevons, claudia, spyder, vellum, mnemo), vanilla JavaScript at cockpit scale, Rust (bullseye), C# and Unity (client), Starlark (device recipes), a TLA+ seam, and platform surfaces spanning launchd job control, tmux window identity, macOS mach-service lookup for TextKit, Claude versus Grok versus Codex billing and capability frames, git amend ownership, and IL2CPP crash reporting. No single engineer holds launchd supervision semantics, provider billing units, NSAttributedString's out-of-process importer and Unity scroll-rect pose mapping at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| Host-down incident and fleet contract | 6-10 | Reading a drowning machine correctly (compressor, not CPU), deciding that ordinary start must not reap, and accepting the three-intent drain/start/upgrade table as the product. |
| jevons / claudia landing review | 4-7 | Calling the ceiling inert from the spend report, rejecting the first T34 reap-on-launch, and keeping adopt off the default of `Launch`. |
| Client and device work (private) | 3-5 | On-device carousel feel, TestFlight approvals, Crashlytics console proof. |
| bullseye / vellum / spyder | 1-2 | Confirming the TextKit diagnosis against `pbcopy` still working, and cutting the three version tags. |

### What If It Were One Person?

The expert band sums to roughly 38-61 person-days. A single generalist pays a steep ramp-up on launchd/tmux lifecycle, two providers' incompatible usage frames, macOS 26's out-of-process text importer, and Unity's scroll-rect coordinate space — four domains that do not appear in the same career. The context-switch tax is milder than last week's (no new product running concurrently with the infrastructure push) and harsher than a specialist-team split, where a platform engineer and a runtime engineer could have taken the incident and T27 in parallel.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~48-76 person-days (~2.4-3.8 months)** |
| Specialist team (traditional) | **~28-46 person-days (~1.4-2.3 person-months)** |
| Actual human effort this week | **~14-24 hours (~1.8-3.0 person-days)** |
| **Multiplier vs. generalist** | **~40-70x** |
| **Multiplier vs. specialist team** | **~25-45x** |

The multiplier peaks on the incident contract and on T27, where the expensive step is naming the property that was missing (recovery, not a better kill; a content hash, not a version chain). It runs lowest on the parts that need a human body in the loop — watching a machine drown, judging carousel feel, cutting a store build — which is the same floor every week in this series has hit. The human contribution concentrated on what a tool must refuse to do: that ordinary start must not reap, that unknown remaining must not render as fine, that a field a provider cannot honour is refused, and that a wall clock is not a verdict.

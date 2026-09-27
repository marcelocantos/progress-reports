# Weekly Progress Report — 2026-09-14…20

## Executive Summary

**Twelve repositories** landed **206 commits**. The centre of gravity stayed on the fleet: **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** ran **v0.32.0→v0.41.0** (ten tags) — Resolve as the sole placement chooser, a daemon pool for Acquire/Release, purpose-quality intel, Cursor ACP chunk-join, and a live-gate programme that stopped wall-clock weather from deciding hermetic verdicts. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** (32 commits) hardened seat-reap, parent-report dedupe, EMPTY-vs-GREEN test gates, and Grok `GOAL_STATUS` closing. **[marcelocantos/csp](https://github.com/marcelocantos/csp)** v0.30.0 drove continuous Lifeboat choreography from CSP motion streams with bounded scene updates. **[marcelocantos/threedee](https://github.com/marcelocantos/threedee)** finished the OpenSCAD→[build123d](https://github.com/gumyr/build123d) port under a geometric oracle and deleted the last SCAD sources. **[marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)** v0.53–v0.56 made declared checks a real gate and closed Fable highs that bypassed achieved immutability. **[squz/ge](https://github.com/squz/ge)** adopted the source-only doctrine (prebuilts cooked, never published) and fixed FreeType UTF-8 plus wrist-pivot hints. **[arr-ai/arrai](https://github.com/arr-ai/arrai)** made function values behave as `{f}`, keyed Reduce/GenericJoin on frozen/v2, and added a tree-level simplifier. Commercial still in-flight only: [private week 2026-09-20](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-09-20.md).

**206 commits** | **+35,614 net lines** | **~55-85 person-days traditional equivalent** | **~30-55x multiplier**

> Honesty note: headline ☲ is gather `landed:` after standing `data/line-excludes.yaml` globs (no new globs this week). Excluded bulk this week **+22,652/−809** (mostly bullseye.yaml/lockfile churn and standing globs). Claudia gather count is **63** first-parent-landed on master in-window; the release train itself is ten tags.

### Major Achievements & Innovations

- **Resolve is the only placement chooser** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.32–v0.41) — purpose-quality picks from a daily intel series; model catalog is a set, not a ranking; seats are not placed on a spent allowance; Grok rollover reads as 100% remaining. Daemon pool serves Acquire/Release/`keep_alive_for`; the daemon package builds only on exported API (🎯T64/🎯T75).
- **Live gates measure the seam, not the weather** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) 🎯T33/🎯T92–🎯T105) — wall-clock deadlines no longer decide hermetic Codex verdicts; dropped frames are not silent agents; a slow peer is not a lost brief; scratch files cannot RED every seat's gate; Cursor ACP chunk-join is one word on the shipped path.
- **Lifeboat continuous choreography** ([marcelocantos/csp](https://github.com/marcelocantos/csp) v0.30.0) — dedicated motion imps drive continuous cargo; WebSocket aborts join safely; scene updates are bounded streams; allocation ratchet and lost-wake fixes from the prior week stay the gate.
- **SCAD port closed under an oracle** ([marcelocantos/threedee](https://github.com/marcelocantos/threedee)) — OpenSCAD reference vs build123d OFF export with vertex merge; involute bevel gears, pure-algebra screw-box, true offsets instead of fake fillets; every verified SCAD source deleted.
- **Checks that actually gate** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) v0.53–v0.56) — `command:` check kind executed; recursive check runs refused; single-target writes no longer rewrite unrelated records; Fable highs that bypassed achieved immutability closed; Home Convergence TLA+ and a local push gate.
- **ge source-only doctrine** ([squz/ge](https://github.com/squz/ge) 🎯T181/🎯T190) — Mode A cancelled; `ensure-prebuilt` cooks from the working tree; vendor SDL archives on demand; NDK by glob not `ls` parse; FreeType UTF-8; wrist pivot at palm heel in screen space.

### Significant Progress

- **jevons fleet survival oracles** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)) — reaped seats only on their own completion claims; parent reports deduped; EMPTY not GREEN for empty `go test`; Grok `GOAL_STATUS` in chat_history closes the mission; leftover commits surfaced after reap.
- **arrai post-42× cleanup** ([arr-ai/arrai](https://github.com/arr-ai/arrai) v0.342.0) — functions as one-element sets; frozen/v2 map keys; dead hand-written lexer removed; tree-level one-shot let folding.
- **mcpbridge envelope path** ([marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) v0.10.0) — classify without a cJSON tree; SSE past 64 KiB; oversized stdio lines fail with EPROTO; shared C/Go config corpus.
- **mnemo tool CLI parity** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) v0.98–v0.100) — every MCP tool has a CLI counterpart through the daemon; owner can turn summarisation off without stopping the daemon.
- **ytt one Resolve pick** ([marcelocantos/ytt](https://github.com/marcelocantos/ytt)) — host synopsis ladder deleted; Claudia decides purpose/quality/Cursor eligibility.
- **spyder host Wi-Fi monitor** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) v0.87.0) — confirmed auto-bounce from app-channel staleness.

### Tough Challenges Overcome

- **A wait nothing can wake** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) 🎯T91/🎯T96) — Cursor ACP hangs and dead peers were reading as silent agents; the bound now answers to the deadline the wait is running under, and dropped frames are counted without blaming the connection.
- **Quoted completion claims** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T750/🎯T752) — a worker that only *read* a GOAL_STATUS marker was being reaped; reap now requires a completion claim the seat made, and Grok's chat_history marker is heard at the product entry point.
- **BuildPart clobbering located copies** ([marcelocantos/threedee](https://github.com/marcelocantos/threedee)) — several SCAD ports looked right until the oracle compared OFF meshes; rebuilds without BuildPart and true geometric offsets closed the gaps.
- **Prebuilts as published artefacts** ([squz/ge](https://github.com/squz/ge)) — LFS binaries and `ls`-parsed toolchains made consumer CI and source-only builds disagree; cook-from-tree and glob NDK resolution are the doctrine.

### Contributors

- Marcelo Cantos (AI co-authors — Claude, Grok, Cursor, Codex — appear on `Co-authored-by` trailers throughout; claudia live-gate and jevons oracle programmes were largely the supervised fleet).

---

## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Continuous Lifeboat (25 commits, v0.30.0)

124→132 file changes band, **+6,816/−605**. Continues last week's Lifeboat landing.

- **Continuous choreography**: dedicated motion imps drive cargo without a discrete step clock; labels align with imps and phases; browser renders from CSP motion streams.
- **Streaming contract**: bounded scene updates; WebSocket aborts join safely; verified live-stream measurements recorded.
- **Carry-forward**: lost-wake Note CAS, allocation ratchet (🎯T55), `src/` as LIB_SRCS authority, dist amalgamation protocol tests.

### [arr-ai/arrai](https://github.com/arr-ai/arrai) — Function-as-Set + Simplifier (7 commits, v0.342.0)

- **Semantics**: function values behave as the one-element set `{f}`; Reduce/GenericJoin maps keyed with frozen/v2 so equal keys group.
- **Cleanup**: dead hand-written lexer and orphaned helpers removed; NOTICE/goreleaser/agent-guide release prep.
- **Simplifier** (#768): one-shot let folding and unused-let dropping at tree level.

### [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) — Envelope Path (6 commits, v0.10.0)

- Classify MCP envelopes without building a cJSON tree; delete undriven crash-recovery FSM state; pin C and Go validators to one corpus; fail oversized child lines with `EPROTO`; stop truncating SSE past 64 KiB.

### [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) — Sandbox Tabs (2 commits)

- Parse results as Tree / Events / Tree JSON tabs; Python `keyword.py` demo; stop glyphing spaces in strings.

### [marcelocantos/threedee](https://github.com/marcelocantos/threedee) — Port Oracle Closed (25 commits)

**The geometric programme of the week.** Port oracle: OpenSCAD reference vs build123d OFF, vertex merge within 1e-3–1e-4 mm, manifold3d seam close. Ports fixed and SCAD sources removed for bosch-adapter, router-bit-rack, triton-lifter (real involute bevel), screw-box-partitions (pure algebra), catflap_rpi, baby-gate-latch, nailgun-tip, magnet-tube, machinist-square-mount, starlock-holders. Four-view render sheets. **+981/−2,793** (SCAD deletions dominate removals).

---

## Agent & Fleet Infrastructure

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Pool, Resolve, Live Gates (63 commits, v0.32.0–v0.41.0)

**The biggest effort of the week.** 320 file changes, **+16,743/−3,345**. **~258 new `func Test` additions** on the Go surface (gross; many replace flaky clocks).

- **Resolve / usage**: purpose-quality from daily intel (T71); catalog as a set; stop placing on spent allowance; Grok weekly rollover = 100%; pace every vendor door and keep what it said (🎯T84/🎯T85).
- **Daemon pool** (🎯T64/🎯T75): Acquire/Release/`keep_alive_for` through the daemon; daemon is `claudia/daemon` on exported API only; Rewind/GoalCompleteCheck/Task.SetRawLog on daemon-held seats; MCPHost as library API.
- **Cursor ACP** (🎯T79/🎯T83): chunk-join on the shipped path; mint that swallows the opening brief is the harness's problem; turn-delivery API (🎯T72).
- **Live-gate honesty** (🎯T33, 🎯T91–🎯T105): re-derived wall-clock teeth; dropped-frame vs silent-agent; bound split from the seam; author-private scratch; census-driven live gate; WaitReady dismisses Claude workspace-trust (#57).

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Survival Oracles (32 commits)

258 file changes, **+8,530/−905**. **~574 new test lines** of `func Test` additions (gross).

- Reap only on completion claims the seat made (not quoted markers); Grok GOAL_STATUS closes missions; parent report body not re-offered; EMPTY vs GREEN; leftover commits after reap; non-destructive drain as an operation; string-matching false-green ratchet; pane-busy held not failed as startup stall.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Checks Gate (20 commits, v0.53.0–v0.56.0)

- Declared checks execute (`command:` kind); recursive runs refused; migration constraint mechanical; single-target writes stop ledger-wide heal (🎯T82); Fable highs/mediums on achieved immutability and write lies closed; Home Convergence TLA+; local push gate.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — CLI Counterparts (6 commits, v0.98.0–v0.100.0)

- Every MCP tool has a CLI counterpart through the daemon; summarisation opt-out without stopping; tool-command flags follow positionals.

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — One Resolve Pick (5 commits)

- Delete host synopsis ladder; ask Claudia for purpose/quality/analysis; Cursor eligibility is Claudia's call.

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Wi-Fi Monitor (3 commits, v0.87.0)

- Host Wi-Fi monitor with confirmed auto-bounce from app-channel staleness.

---

## Game Engine

### [squz/ge](https://github.com/squz/ge) — Source-Only (12 commits)

- **Source-only doctrine** (🎯T181/🎯T185/🎯T190/🎯T191): cancel Mode A published prebuilts; cook from working tree; vendor SDL on demand; NDK by glob; restore vendor pins moved silently; Android Play upload keychain + bundle ship path.
- **Input/text**: FreeType UTF-8 codepoints; hint wrist pivot at palm heel, screen-space only (🎯T180).

---

## Commercial

No commercial work landed on a default branch this week. In-flight HMS layout-parity and stock-car 3.26/Halloween/repair work: [private week 2026-09-20](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-09-20.md).

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **Health-Management-Systems/hms** — 6 in-flight (gather); detail in the private companion.
- **minicadesmobile/stock-car-racing** — 15 in-flight (gather); 3.26 Halloween/Thunderdome/repair-notification train; detail in the private companion.
- **marcelocantos/jevons** — 58 in-flight (gather); large unmerged oracle/fleet branch work beside the 32 landed.
- **arr-ai/arrai** — 17 in-flight (gather); benchmark-corpus programme continues into next week.
- **squz/ge** — 6 in-flight; **marcelocantos/csp** — 5; **squz/yourworld2** / **squz/esfera2** — minor.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-09-14…20. In-flight branch work is excluded by design. `progress-reports` / `progress-reports-private` commits omitted from repo counts (narrative about the work).*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **12** |
| Total landed commits | **206** |
| Total lines added (landed, filtered) | +47,136‡ |
| Total lines removed (landed, filtered) | −11,522‡ |
| Net new lines (landed, filtered) | +35,614‡ |
| File changes | 1,052 |
| New files created | ~526 |
| Bulk paths excluded from ☲ | +22,652 / −809 (lockfiles, bullseye.yaml, standing globs) |
| Releases published | **~20** (claudia v0.32–v0.41, bullseye v0.53–v0.56, mnemo v0.98–v0.100, csp v0.30.0, mcpbridge v0.10.0, spyder v0.87.0, arrai v0.342.0) |
| Languages | Go, C++, Python, TLA+, JavaScript, HTML, CSS, YAML, Markdown, Shell, SCAD/build123d |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. No new globs this week.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 63 | 320 | +16,743 | −3,345 | +13,398 |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 32 | 258 | +8,530 | −905 | +7,625 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 25 | 132 | +6,816 | −605 | +6,211 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 20 | 101 | +5,677 | −356 | +5,321 |
| [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) | 6 | 39 | +1,995 | −239 | +1,756 |
| [squz/ge](https://github.com/squz/ge) | 12 | 36 | +1,912 | −1,021 | +891 |
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | 7 | 45 | +1,636 | −1,544 | +92 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 3 | 27 | +1,206 | −307 | +899 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 6 | 19 | +1,061 | −58 | +1,003 |
| [marcelocantos/threedee](https://github.com/marcelocantos/threedee) | 25 | 41 | +981 | −2,793 | −1,812* |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 5 | 30 | +445 | −320 | +125 |
| [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) | 2 | 4 | +134 | −29 | +105 |

\* *Net negative from deleting verified OpenSCAD sources after oracle PASS.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~574 gross `func Test` adds | reap/GOAL_STATUS/EMPTY/parent-dedupe oracles |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~258 gross | pool, Resolve, live-gate seam oracles |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | checks + TLA+ | Home Convergence; Fable closures |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | choreography + stream | continuous Lifeboat measurements |
| [marcelocantos/threedee](https://github.com/marcelocantos/threedee) | port oracle | OFF mesh compare / vertex merge |
| [squz/ge](https://github.com/squz/ge) | cook/NDK tooling | source-only doctrine gates |
| **Total** | **large (fleet-oracle heavy)** | landed only |

### Daily Activity

![Daily active repositories](daily-activity-2026-09-20.svg)

*(Active repositories per day: Mon 09-14 6, Tue 09-15 6, Wed 09-16 2, Thu 09-17 5, Fri 09-18 0, Sat 09-19 1, Sun 09-20 6.)*

---

## Ideas & Innovations

### Placement Is a Predicate, Not a Ladder ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
Host-side provider ladders encode yesterday's preference as today's policy. **Resolve returns one Provider+Model+Effort from purpose/quality/background predicates and live remaining.** Spent allowance is not headroom; a rollover that still shows last week's zero is a bug. The catalog is a set of admitted options, not a ranked shelf the caller walks.

### The Bound Belongs to the Seam ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
A hermetic Codex verdict decided by wall-clock weather is not a test of the product. **The wait's deadline is the bound under test; a dropped frame is counted without indicting the connection; a slow peer is not a lost brief.** Live gates that cannot cite their own evidence are weather reports.

### Geometry Is the Oracle ([marcelocantos/threedee](https://github.com/marcelocantos/threedee))
Porting SCAD by eye leaves BuildPart clobbers and fake fillets invisible. **Render reference and port to OFF, merge vertices, close manifold seams — then delete the SCAD.** The oracle retires when every source is gone, not when the screenshots look fine.

### Cook, Don't Publish ([squz/ge](https://github.com/squz/ge))
Committed prebuilt `libge.a` and `ls`-parsed NDK paths made "source-only" a slogan. **`ensure-prebuilt` cooks from the working tree; toolchains resolve by glob; Mode A publication is cancelled.** Consumer CI that cannot cook cannot claim the doctrine.

### Reap the Claim, Not the Quote ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
A seat that *reads* another seat's GOAL_STATUS is not finished. **Completion is a claim the seat made at the product entry point;** quoted markers and chat_history echoes are evidence for the reader, not a reap signal.

---

## Effort Estimate: Traditional vs. AI-Assisted

A fleet-correctness week sitting next to a geometry-port week: claudia's live-gate programme and jevons's reap oracles do not share a cache with involute bevel gears or FreeType UTF-8.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| claudia Resolve/pool/live-gate train (v0.32–v0.41) | 14-22 | Multi-provider grant/pool semantics; hermetic vs live seam separation; Cursor ACP chunk-join; ten-tag release train without auto-rebind regressions. |
| jevons survival oracles | 6-10 | Reap/quoted-marker/EMPTY/parent-dedupe correctness under a live fleet. |
| csp continuous Lifeboat + v0.30 | 4-7 | Motion streams as the scene clock; WebSocket abort join; measurement gates. |
| threedee SCAD→build123d oracle close | 5-8 | Exact mesh compare; involute gears; BuildPart clobber classes. |
| bullseye checks gate + Fable closures | 3-5 | Declared checks that execute; achieved-immutability highs; TLA+ convergence. |
| ge source-only + UTF-8/hints | 3-5 | Cook doctrine; NDK glob; FreeType; wrist pivot. |
| arrai function-as-set + simplifier | 2-3 | Set semantics for functions; frozen/v2 keying. |
| mcpbridge / mnemo / ytt / spyder / xbnf | 3-5 | Envelope path, CLI parity, Resolve-only synopsis, Wi-Fi bounce, sandbox tabs. |

### The Diversity Tax

This week spans multi-provider broker pool semantics, fleet reap oracles, C++ CSP streaming demos, CAD port oracles, game-engine cook doctrine, and language-runtime set semantics. No single engineer holds Cursor ACP chunk-join, involute bevel construction, and ge prebuilt cook at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| claudia live-gate / Resolve | 6-10 | Refusing weather-based verdicts; pool-not-process; catalog-as-set. |
| jevons reap/quoted-marker | 3-5 | Completion claims vs quotes; EMPTY vs GREEN. |
| threedee oracle retire | 2-4 | Accepting OFF mesh compare as the finish line; deleting SCAD. |
| ge source-only | 2-3 | Cancel Mode A; cook-from-tree as doctrine. |
| csp / bullseye / others | 3-5 | Choreography measurements; checks that execute. |

### What If It Were One Person?

The expert band sums to roughly 40-65 person-days. A single generalist pays ramp-up on broker pool semantics, CAD oracles, and engine cook doctrine — three careers. Friday at zero active repos is the week's pause; Sunday then ran a six-repo close with the claudia v0.41 and csp v0.30 tags.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~55-85 person-days (~2.8-4.3 months)** |
| Specialist team (traditional) | **~40-62 person-days (~2.0-3.1 person-months)** |
| Actual human effort this week | **~16-27 hours (~2.0-3.4 person-days)** |
| **Multiplier vs. generalist** | **~30-55x** |
| **Multiplier vs. specialist team** | **~22-40x** |

The multiplier peaks on claudia's live-gate honesty (the expensive step is making the bound answer to the seam) and on threedee's oracle-closed port. It runs lowest on the xbnf sandbox tabs. The human contribution concentrated on what a tool must refuse: that wall-clock weather is not a hermetic verdict, that a quoted GOAL_STATUS is not a reap, that Mode A prebuilts are not source-only, and that a SCAD port is unfinished while the reference file still exists.

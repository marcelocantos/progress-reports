# Weekly Progress Report — 2026-09-07…13

## Executive Summary

**Twelve repositories** landed **115 commits**. The two heaviest landings would each have been a headline: **[arr-ai/arrai](https://github.com/arr-ai/arrai)** (v0.340.0–v0.341.0) closed the evaluator overhaul at **42× end-to-end / 106× on eval** against the v0.338.0 reconstruct baseline, then evaluated relation rows in-place under a seedless 64-bit hash; **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** v0.31.0 became a **host daemon** (`claudia broker serve`) that parents every provider process, reclaims seats by name, and is the one plan-usage evaluator. **[marcelocantos/csp](https://github.com/marcelocantos/csp)** (23 commits) shipped Lifeboat — an orbital-dock demo whose logistics and motion are real CSP imps over typed channels, with paired TLA+ models for lost wakes. **[marcelocantos/xbnf](https://github.com/marcelocantos/xbnf)** can replace wbnf for arr.ai (🎯T33) and emits a 24-byte event stream that tiles the input (🎯T34). **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** consumes the claudia daemon: seats are reclaimed, not stopped. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** v0.95–v0.97 stopped the packer starving `/health` (~95 s → leftover-membership). **[marcelocantos/pigeon](https://github.com/marcelocantos/pigeon)** v0.33.0 added Yamux-class L4 stream lifecycle. **[arr-ai/frozen](https://github.com/arr-ai/frozen)** v2.0.0 is seedless hashing on a new module path. Commercial in-flight only: [private week 2026-09-13](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-09-13.md).

**115 commits** | **+40,842 net lines** | **~52-82 person-days traditional equivalent** | **~35-60x multiplier**

> Honesty note: **new `data/line-excludes.yaml` globs this run** — `arr-ai/arrai` `perf/reconstruct/model.sysl.pb` + `perf/reconstruct/vendor/**` (85k-line protobuf dump and a vendored sysl-in-arrai workload). Headline ☲ is gather `landed:` after those globs. Excluded bulk this week is **+89,888/−274**. The arrai **42×/106×** figures are against the reported v0.338.0 reconstruct (58.8–67.8 s → 1.51 s); last week's interned-shapes slice was already on that ladder (2.13 s). This merge is the rest of the programme plus in-place rows and the hash-contract change.

### Major Achievements & Innovations

- **Evaluator overhaul lands at 42× / 106×** ([arr-ai/arrai](https://github.com/arr-ai/arrai) v0.340.0–v0.341.0) — reconstruct wall-clock 58.8–67.8 s → **1.51 s** vs v0.338.0 (algo 106× after subtracting the ~925 ms compile floor). Direct calls, index-backed `where`, `let rec` as a once-written cell, parallel `where`/`=>` and `>>`/`>>>`, linear concat, interned `$`-strings. Then 🎯T29: common relational paths keep rows on the arena instead of boxing them as Tuples; Hash128 is gone — values use a seedless 64-bit `Hash()` with mix/xor and kind salts, matching frozen/v2.
- **claudia is a daemon** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.31.0, 🎯T2) — `claudia broker serve` parents every provider process through a persisted grant table. Seats survive the consumer unowned with a 256-event replay ring and are reclaimed by name. One host-wide plan-usage evaluator (TTL refresh, 429 invalidation). On boot, seats held before the last stop are adopted or relaunched with session resume. The library takes the socket when a daemon answers and today's direct path otherwise; it never auto-rebinds. Live reclaim attested for Claude, Grok and Cursor.
- **mnemo `/health` without a fast tier** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) v0.95.0–v0.97.0) — quiesced GET `/health` was ~95 s on a 7.8 GiB store because `compress.backfill` ran live `SUM(length())` over overflow blob pages. Status uses leftover membership (`z IS NULL` plus stored `plain_len`) and new partial indexes. No `?tier=fast`, no TTL cache — the full payload stays the path. A WAL alert keys on a pinned reader (zero frames copied for 45 minutes), not on file size: the 7 Sep backfill grew to 1,016 MiB and was fine.
- **Yamux-class L4 on native QUIC streams** ([marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) v0.33.0, 🎯T63) — reset unmatched streams, name-aware admission, FIN vs RST, GoAway drain. Still native QUIC streams, not an app-level muxer.
- **frozen/v2 — seedless hash, new module path** ([arr-ai/frozen](https://github.com/arr-ai/frozen) v2.0.0) — `github.com/arr-ai/frozen/v2`; the arr-ai/hash dependency is gone. Breaking on purpose so nested values can cache.
- **vellum viewer: TOC, live reload, task toggles** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum) v0.18.0–v0.19.0) — static in-document TOC for convert sinks (🎯T38); viewer live reload; editable task-list checkboxes behind a consent modal.

### Significant Progress

- **xbnf replaces wbnf for arr.ai** ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) 🎯T33/🎯T34) — macros expand at compile, `%%` hooks and `#import` run on the product path, `\b` matches as in Go regexp; converted `arrai.wbnf` agrees with wbnf on a pinned accept/reject set. Parse output is an event stream (open/close/leaf/skip) whose leaf+skip lengths tile `[0, End)`; an Event is 24 bytes. vs `a9188b3`: TIME WIN 1.094 (18/20), MEM WIN 2.88 → 1.30 MB, KEEP. Sandbox runs the committed T22 grammars as a tree viewer.
- **jevons consumes the daemon** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)) — `LoadPlanUsage` reads the daemon snapshot; `StopNonAdoptable` stops nothing on upgrade when the daemon holds the processes; the next jevonsd grants by name. Cursor seats whose `session/load` is refused are reminted. Frontier hovercards open from the id only (🎯T643/🎯T648/🎯T649).
- **Lifeboat — a live CSP application** ([marcelocantos/csp](https://github.com/marcelocantos/csp)) — six logistics imps plus per-rig motion imps over typed channels; the browser observes `127.0.0.1:8042`. Evacuation drains accepted cargo; a tripped crane is supervised without replaying completed waypoints. Paired TLA+ for Note-wake, cancel-reason publication, WebSocket join/close. An allocation ratchet (not nanobench) gates 2,000 rendezvous at 11 allocations.
- **ytt climbs the claudia ladder** ([marcelocantos/ytt](https://github.com/marcelocantos/ytt)) — synopsis resolves the provider ladder from Claudia plan usage and runs on the claudia daemon when present.

### Tough Challenges Overcome

- **A packer that held SQLite's writer for the whole batch** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) 🎯T167–🎯T169) — auto backfill packed 2,000 rows per transaction with zstd encode-and-verify inside it. `/health` timed out at 45 s; the WAL grew to 1,215 MiB because TRUNCATE waits for a write lull a multi-hour pack never provides. Encoding moved outside the transaction; inter-batch pause is proportional to batch cost; PASSIVE checkpoint every 64 MiB. Measured: worst foreground write 10 ms across a live backfill. A UNIQUE collision on one row used to abort the whole family; constraint failures now skip and continue.
- **A WAL alert that would have fired on health** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) 🎯T172) — keying on size, or on growth sustained for N minutes, fires on the healthiest heavy workload. Zero frames copied across ongoing attempts for 45 minutes means a reader is pinned. Six of eight tests assert SILENCE; a ratchet fails the build if the window shrinks below 3× the longest reader the daemon opens itself.
- **Lost worker wakes** ([marcelocantos/csp](https://github.com/marcelocantos/csp)) — a Note CAS race when a worker enters sleep during wake; work publication paired with the parking fence. Regression fails against the original Note. Dist test inventories are configuration-matched, including TLS-disabled sanitizer builds.
- **Cursor `session/load` refused through the daemon** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) / [marcelocantos/jevons](https://github.com/marcelocantos/jevons)) — a daemon-wrapped refusal was not recognised as the T304/T328 "will not mint a replacement" class, so remint never ran. The broker remints a standing Cursor seat; jevons waits for `store.db` and does not time out that remint.

### Contributors

- Marcelo Cantos (AI co-authors — Claude Opus 5, Claude Fable 5.1, Grok, Cursor, Codex — appear on `Co-authored-by` trailers throughout; arrai, claudia broker and xbnf T33/T34 were largely the supervised fleet).

---

## Libraries & Infrastructure

### [arr-ai/arrai](https://github.com/arr-ai/arrai) — 42× Evaluator (2 commits, v0.340.0–v0.341.0)

**The biggest effort of the week.** Two squash-merges, 276 file changes, **+14,813/−2,488** after excluding the reconstruct protobuf dump. **~126 net new tests**.

- **Programme close** (v0.340.0, #739): the ladder in `docs/perf-ledger-2026-08.html` — direct function application (no one-element-set wrap; 5.8 M calls on reconstruct), compile-time `where .attr = key` from the relation index (two sites had been 4,000,000 scanned rows), `let rec` as a once-written scope cell rather than a Y combinator, single-pass hashing, parallel `where`/`=>` and `>>`/`>>>`, linear string/array concat, interned `$`-strings, reflection-free sorts. Output byte-identical at every rung. `ARRAI_TIMING=1` splits compile from eval.
- **In-place rows + seedless 64-bit hash** (v0.341.0, #761, 🎯T29): `Names` is the interned attribute set (Shape is gone); hole-free strings use a byte backing with memoised Hash128-then-not. Common `where`/`=>`/`nest`/`orderby` keep rows on the arena. Hash128 and the hashidentity bridge are deleted; frozen/v2 wraps its own sets and maps. 32-bit CI: mix salts truncated through a runtime helper so GOARCH=386 does not overflow `uintptr`.
- **Next**: `docs/design-evaluation-as-query-execution.md` — the interpreter and the query executor as the same machine; streaming the default edge; materialize as an explicit pipeline breaker.

### [arr-ai/frozen](https://github.com/arr-ai/frozen) — frozen/v2 (1 commit, v2.0.0)

Covered above. Module path `github.com/arr-ai/frozen/v2`; arr-ai/hash dropped. **~9 tests touched**; +924/−1,798 across 89 files (hash128 assembly and the hash module go).

### [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) — Replace wbnf, Event Stream (15 commits)

Continued from last week's engine. 88 file changes, **+4,051/−891**. **~36 new tests**.

- **T33**: macros, `%%` hooks, `#import`, Go-regexp `\b`; converted arrai.wbnf agrees with wbnf on a pinned accept/reject set; stack `@` at the tightest level wraps to the stack start.
- **T34**: `Result.Events` replaces `Result.Tree`. Open/close/leaf/skip; leaf+skip lengths sum to `End` and cover every byte, so `#wrap` is visible as skip. `Node.Text(input)` slices `input[Start:End]`; `Result.Tree()` decodes on demand. Event is 24 bytes, counted exactly before allocation. Golden fingerprints unchanged (hash runs over the decoded tree).
- **T23/T32**: tree positions; converted wbnf grammars match wbnf's language.
- **T31**: capture-context corpus baseline vs `9c47802` recorded; idle load bar is half of ncpu, not a 2.5-core constant.
- **Sandbox**: cheat-sheet examples and T22 language grammars render as a shared tree viewer (🎯T35/🎯T36).

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Lifeboat (23 commits)

124 file changes, **+6,711/−596**. **~6 new tests** plus TLA+ model pairs.

- **Lifeboat / Port Meridian**: `make lifeboat` → `127.0.0.1:8042`. Arrival → Aster/Boreal cranes → warehouse → fabricator → tram, with bounded channel capacities (rendezvous at zero). Each cargo completes four sends; Aster's durable slot belongs to its supervisor scope. Motion imps own pose, execute timed waypoints, acknowledge; logistics wait on those acks. Channel view shows topology and stage populations. Evacuation stops admission, drains accepted cargo, completion screen only after every logistics and motion imp exits.
- **Lost wakes** (paper 36): Note CAS retry when a worker enters sleep during wake; work publication paired with the parking fence; paired fix/bug TLA+.
- **Allocation ratchet** (🎯T55): `perf/alloc_ratchet.cc` through a replacement global `operator new`. 2,000 unbuffered rendezvous = 11 allocations; 2,000 eight-way prialt = 60. Band ±1% in both directions. `src/` is the authority for both `LIB_SRCS` lists; objects rebuild when compile flags change; protocol tests run against the dist amalgamation.

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) — L4 Stream Lifecycle (6 commits, v0.33.0)

Covered above. **~18 new tests**; +1,229/−89 across 29 files.

---

## Agent & Fleet Infrastructure

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Broker Daemon (20 commits, v0.31.0)

**The architectural shift of the week.** 159 file changes, **+8,558/−421**. **~52 new tests**.

- **Wire**: grant / release-by-name / send / interrupt / set_model / migrate / agent_info / term_subscribe / resize / close_goal / task_run / task_cancel / usage / resolve / grants, plus per-grant event streams. Table-driven parse/encode, golden vectors, `Handler` seam. Error codes: `unknown_grant`, `grant_held`, `not_available`, `agent_failed`, `unknown_run`.
- **Daemon**: `claudia broker serve` via a direct-mode Registry persisted as `grants.json`; operator surface status / grants / tail / usage / release / install / uninstall / socket. supervisord (and a brew-services stanza with operator CLI oracles, 🎯T2.7). Host MCP connections on the daemon (🎯T2.16); an unowned stream is held across a consumer bounce (🎯T70).
- **Usage** (🎯T61): classify plan bands, share a usage snapshot, resolve a model from predicates. Grok and Cursor plan remaining always fetched. Vertices retuned to the owner map (🎯T641).
- **Library**: `Start`, Registry Launch/Adopt/AdoptOrLaunch/Stop, `Task.Run`, `LoadPlanUsage` and `Resolve` take the socket when a daemon answers. `CLAUDIA_NO_BROKER=1` pins the hermetic suite so an installed daemon is never granted fixture seats. `--version` / `--help-agent` on the packaged binary.

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Consume the Daemon (24 commits)

Continued. 107 file changes, **+3,164/−711**. **~25 new tests**.

- **Daemon consumer** covered above. T63 journey: prime the daemon seat before jevonsd so Grok exclusive home exists; wait for the SIGHUP'd connection to drop before reclaiming; send the pong after reclaim, and only if a leftover turn already finished.
- **Cursor remint**: wait for `store.db`; a bound Launch is a created seat; do not time out the remint. Stay silent on a broker-held bounce (🎯T646).
- **Chrome**: frontier hovercard from the id only, never over the trigger (🎯T643/🎯T648/🎯T649); theme cycle with one icon, opposite of the OS first (🎯T642); usage-bar triangles coloured by remaining period; Grok/Cursor usage opt-in flags dropped (🎯T640). Ledger fields are markdown; agents escape HTML they cite (🎯T650).

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Health, WAL, Packer (13 commits, v0.95.0–v0.97.0)

Covered above. Compaction failure rate is a named constant on `HealthSnapshot` (a 0.79 fail ratio had been reporting "healthy" because the breaker only tripped when fully open). Insert statements picked by schema shape so a T170-only probe cannot bind columns that land after the deferred upgrade. **~29 new tests**; +3,415/−256 across 57 files.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Markdown Prose (1 commit)

Prose fields are markdown and HTML is interpreted (🎯T88). +173/−21 across 6 files.

---

## Tooling & Workflow

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — TOC, Live Reload (7 commits, v0.18.0–v0.19.0)

Covered above. **~37 new tests**; +1,928/−57 across 40 files.

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — Claudia Ladder (2 commits)

Covered above. **~4 new tests**; +144/−382 across 7 files.

### [marcelocantos/skills](https://github.com/marcelocantos/skills) — Republish (1 commit)

`Update skills from ~/.claude/skills`. +3,508/−66 across 31 files.

---

## Commercial

No commercial work landed on a default branch this week. In-flight (HMS layout-parity journeys; stock-car 3.25 live on both stores, then Halloween/Thunderdome on the 3.26 train) is summarised in [private week 2026-09-13](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-09-13.md).

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **Health-Management-Systems/hms** — 17 in-flight; detail in the private companion.
- **minicadesmobile/stock-car-racing** — 42 in-flight (3.25 store live, 3.26 Halloween/Thunderdome, scr-editor); detail in the private companion.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-09-07…13. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **12** |
| Total landed commits | **115** |
| Total lines added (landed, filtered) | +48,618‡ |
| Total lines removed (landed, filtered) | −7,776‡ |
| Net new lines (landed, filtered) | +40,842‡ |
| File changes | 783 |
| New files created | ~300 |
| Bulk paths excluded from ☲ | +89,888 / −274 (arrai reconstruct protobuf + vendor, lockfiles, standing globs) |
| Releases published | **10** (arrai v0.340–v0.341, frozen v2.0.0, claudia v0.31.0, mnemo v0.95–v0.97, pigeon v0.33.0, vellum v0.18–v0.19) |
| Languages | Go, C++, TLA+, JavaScript, HTML, CSS, Rust, YAML, Markdown, Shell |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. New this run: arrai `perf/reconstruct/model.sysl.pb` + `perf/reconstruct/vendor/**`.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | 2 | 276 | +14,813 | −2,488 | +12,325* |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 20 | 159 | +8,558 | −421 | +8,137 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 23 | 124 | +6,711 | −596 | +6,115 |
| [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) | 15 | 88 | +4,051 | −891 | +3,160 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 1 | 31 | +3,508 | −66 | +3,442 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 13 | 57 | +3,415 | −256 | +3,159 |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 24 | 107 | +3,164 | −711 | +2,453 |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 7 | 40 | +1,928 | −57 | +1,871 |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 6 | 29 | +1,229 | −89 | +1,140 |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | 1 | 89 | +924 | −1,798 | −874 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 1 | 6 | +173 | −21 | +152 |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 2 | 7 | +144 | −382 | −238 |

\* *After excluding `perf/reconstruct/model.sysl.pb` and `perf/reconstruct/vendor/**` (+87,783 excluded).*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | ~126 net | arena rows, seedless hash, plan-roundtrip; 138 added / 12 removed |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~52 | broker grant/reclaim, ModelPick parity, usage evaluator |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | ~37 | TOC, live reload, checkbox consent |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~29 | T167–T169 packer, T172 WAL silence ratchet, leftover-membership health |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~25 | T63 reclaim journey, daemon-held seats neither stopped nor reaped |
| [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) | ~36 | T33 wbnf parity, T34 event-stream tiling, T32 converted grammars |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | ~18 | T63 reserved-path and allowlist oracles |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | ~9 | v2 module-path / seedless hash |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~6 | lost-wake regression; Lifeboat is demo+TLA+ |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | ~4 | claudia-ladder resolve |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 1 | markdown/HTML prose |
| **Total** | **~343** | landed only |

### Daily Activity

![Daily active repositories](daily-activity-2026-09-13.svg)

*(Active repositories per day: Mon 09-07 5, Tue 09-08 2, Wed 09-09 0, Thu 09-10 0, Fri 09-11 0, Sat 09-12 8, Sun 09-13 8.)*

---

## Ideas & Innovations

### The Interpreter Is the Query Executor ([arr-ai/arrai](https://github.com/arr-ai/arrai))
arr.ai's surface syntax already *is* the relational algebra — there is no SQL-to-algebra gap. The 42× programme mined out representation-level wins (rows that *are* tuples, hashes that can be cached, `let rec` that is a cell). The next order of magnitude is a different claim: **evaluation becomes plan execution**. Streaming is the default edge; materialize is an explicit pipeline breaker inserted only where something forces it (a dedup boundary, an order, a join's build side, fan-out). Sequence pipelines (`>>` chains) carry no deduplication semantics at all, so they fuse freely.

### A Grant, Not a Process ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
Every consumer that wanted a durable agent used to parent the provider process. A consumer restart then had to Adopt leftovers or double the fleet. **The daemon owns the seats; the consumer owns a grant.** Reclaim-by-name after consumer death, a 256-event replay ring for the first subscriber, boot resume that nudges relaunched seats and stays quiet on adopted ones. The library never auto-rebinds: a grant is a decision, not a reconnect loop.

### Size Is Not a Fault ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo))
A WAL that grew to a gigabyte during a healthy backfill is the workload succeeding. An alert keyed on size, or on growth duration, trains people to dismiss it. **Zero frames copied across ongoing PASSIVE attempts for 45 minutes** is the mechanism: a reader is pinned, which is a leaked transaction, which the user can act on. Tracking "stuck since" rather than "last advanced" is required — a zero last-advance cannot distinguish a fresh boot from a daemon that has never once succeeded.

### An Event Stream That Tiles the Input ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf))
A tree whose nodes store text copies the input and hides `#wrap`. **Open/close/leaf/skip events whose lengths sum to `End`** make the wrap visible, make positions a prefix sum, and drop `Node.Text` for a slice of the original input. 24 bytes per event, counted before allocation; `Tree()` is a decode. The golden hash still runs over the decoded tree, so a stream change that moved semantics would fail the ratchet.

### Logistics Imps, Not a Game Loop ([marcelocantos/csp](https://github.com/marcelocantos/csp))
Lifeboat's cranes, warehouse, fabricator and tram are independently scheduled CSP imps over typed channels with stated buffer capacities. The coordinator owns the observation ledger; it does not schedule cargo or choose a crane. **Successful sends are reported after they commit** — out-of-order sender/receiver notifications cannot rewind cargo. A tripped crane freezes its twins at current pose; supervision resumes the unfinished movement without replaying completed steps. The browser is a glass, not the runtime.

---

## Effort Estimate: Traditional vs. AI-Assisted

A language-runtime week sitting next to a process-architecture week: the evaluator overhaul and the claudia daemon do not share a cache, and Lifeboat is a third specialism (C++ CSP + TLA+ + a live WebSocket scene).

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| arrai 42× evaluator + in-place rows + seedless 64-bit hash | 10-16 | Byte-identical reconstruct at every rung; arena rows that must still hash/equal; GOARCH=386 salt truncation. |
| claudia broker daemon, reclaim, host usage | 8-12 | Grant/reclaim protocol with replay; seats that survive the consumer; live attestation across Claude/Grok/Cursor. |
| csp Lifeboat + lost-wake + alloc ratchet | 6-10 | Real CSP application (not a toy); paired TLA+; allocation counts that must not move with load. |
| xbnf T33 wbnf-replace + T34 event stream | 4-7 | Language parity on converted arrai.wbnf; stream that tiles the input; KEEP vs previous HEAD. |
| mnemo packer/WAL/health | 4-6 | Encode-outside-txn; stuck-reader alert that stays silent on a gigabyte-healthy WAL; covering indexes without a fast tier. |
| jevons daemon consumer + Cursor remint | 4-6 | Upgrade that must not reap daemon-held seats; T63 reclaim journey; session/load refusal class. |
| pigeon Yamux-class L4 | 2-3 | FIN vs RST vs GoAway on native QUIC streams. |
| vellum TOC + live reload + consent | 1.5-2.5 | Static TOC for convert sinks; checkbox consent. |
| frozen/v2 module path | 1-2 | Breaking hash contract on a new import path. |
| ytt / bullseye / skills | 1-2 | Ladder-from-daemon; markdown prose; republish. |

### The Diversity Tax

This week spans query-engine representation (arena rows, seedless 64-bit mix/xor), a multi-provider agent broker over a Unix socket, C++ CSP with TLA+ lost-wake models, GLL event-stream layout, SQLite WAL checkpoint mechanics, and QUIC stream lifecycle. No single engineer holds arr.ai's arena hash contract, claudia's grant/reclaim wire, CSP Note-CAS and Yamux-on-QUIC at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| arrai 42× close and hash contract | 4-7 | Requiring reconstruct byte-identity; accepting frozen/v2 as a break; 386 salts. |
| claudia daemon / jevons consume | 5-8 | Grant-not-process; never auto-rebind; live reclaim across three providers; CLAUDIA_NO_BROKER=1 so fixtures cannot capture the installed daemon. |
| mnemo WAL-is-not-a-fault | 2-4 | Alert on pinned readers, not size; encode outside the writer txn. |
| csp Lifeboat / lost-wake | 2-4 | Channel capacities as the demo; alloc ratchet not nanobench. |
| xbnf T33/T34 | 2-3 | wbnf parity as the replace gate; stream tiling as the layout change. |

### What If It Were One Person?

The expert band sums to roughly 42-67 person-days. A single generalist pays ramp-up on query-engine arenas, multi-provider grant/reclaim, CSP/TLA+ and QUIC L4 — four careers. Wednesday–Friday at zero active repos is the week's pause, not a ramp; Saturday and Sunday then ran eight-repo days.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~52-82 person-days (~2.6-4.1 months)** |
| Specialist team (traditional) | **~38-60 person-days (~1.9-3.0 person-months)** |
| Actual human effort this week | **~16-28 hours (~2.0-3.5 person-days)** |
| **Multiplier vs. generalist** | **~35-60x** |
| **Multiplier vs. specialist team** | **~25-40x** |

The multiplier peaks on the arrai overhaul (the expensive step is keeping reconstruct byte-identical while deleting Hash128) and on the claudia daemon (the expensive step is reclaim-by-name with a replay ring, not "add a socket"). It runs lowest on the skills republish. The human contribution concentrated on what a tool must refuse to do: that a WAL gigabyte is not a fault, that a library must never auto-rebind a grant, that an optimisation which needs a golden update is a tree change, and that 42× is cited against v0.338.0, not against last week's already-improved 2.13 s.

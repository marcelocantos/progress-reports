# Weekly Progress Report — 2026-08-31…09-06

## Executive Summary

**Nine repositories** landed **244 commits**. The week's largest landing is a new product: **[marcelocantos/xbnf](https://github.com/marcelocantos/xbnf)** (79 commits) — a scannerless CFG parser generator that succeeds [wbnf](https://github.com/arr-ai/wbnf) rather than upgrading it, with a [GLL](https://en.wikipedia.org/wiki/GLL_parser) engine, a DFA layer for regular fragments, seven live language tracks at Failed=0 against present oracles, and a KEEP-gated optimisation programme that took nested JSON 64 KB from 11.78 ms to 4.06 ms. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** (49 commits) retired the vanilla cockpit, switched live agents instead of stop-and-relaunch, and turned long cycle tools into job handles. **[marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)** (36 commits, v0.49.0–v0.52.0) collapsed nine write verbs onto one `apply` engine and made HTTP the only MCP transport. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** (v0.91.0–v0.94.0) dropped stdio, compressed backups with multithreaded zstd, and moved the daemon under supervisord. **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** v0.30.0 added `Agent.Migrate`. **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** v0.82–v0.86 cut GitHub Actions for local tapper bottles. Commercial in-flight only: [private week 2026-09-06](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-09-06.md).

**244 commits** | **−11,020 net lines** | **~55-85 person-days traditional equivalent** | **~40-70x multiplier**

> Honesty note: **new `data/line-excludes.yaml` globs this run** — `marcelocantos/xbnf` `eval/testdata/*/corpus/**` (pinned third-party language corpora, ~5.9k lines), `marcelocantos/jevons` `docs/audits/**/*.json` (generated suite/fidelity maps; `legacy-suites.json` alone is 12,724 lines). Headline ☲ is gather `landed:` after those globs. Excluded bulk this week is **+28,416/−2,992**. jevons **−51,856 net** is the vanilla cockpit deletion (`web/index.html` and its scripts), not a wipe of this week's authorship. Twenty jevons commits and seven sawmill commits landed on master under agent git identities (`commitbase@example.invalid`, `Test@example.com`) and are excluded from ℂ/☲ by gather's `--author` filter.

### Major Achievements & Innovations

- **A GLL+DFA parser generator in one week** ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf)) — empty repo to a self-hosting engine that parses `docs/xbnf.xbnf`. Alternation is unordered; ambiguity is a compile error unless a `#prefer` / `#longest` / `|>` disambiguator is declared. Regular fragments compile to DFAs; the rest run as Scott & Johnstone GLL. Seven live tracks (SQL, XML, Go, Python, YAML, JavaScript, CommonMark) are Failed=0 against present oracles on pinned third-party corpora. The 🎯T25 programme KEEP-gated JSON 64 KB 11.78 ms → **4.06 ms** / 2.35 MB / 2 allocs, corpus aggregate **3.043×** with B/op 18.89 → 3.20 MB.
- **One write verb over a policy table** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) 🎯T76, v0.49.0–v0.52.0) — nine commit verbs are sugar over `apply`. HTTP is the only MCP transport (🎯T78/🎯T81); stdio is gone. Achieving a target whose blockers are still open is refused (🎯T79). History caches key on git refs with a TTL so a long-lived daemon cannot serve a stale ledger (🎯T78.1). Ship is local via tapper; GitHub Actions dropped.
- **`Agent.Migrate` keeps the handle** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.30.0) — host-called inter-provider Session migrate mints a new native destination, seeds it from a retained live-turn log rather than replaying foreign tools, and leaves event subscriptions on the same `Agent`. Stuck rate-limit/quota events are observed without auto-fallback.
- **Stdio is gone; backups compress and prune** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) v0.91.0–v0.94.0, 🎯T158–🎯T160) — mode comes from argv. Every backup path prunes; `backup_now` no longer skipped GC; scratch files are swept; retention failure is a disk warning. Backups are multithreaded zstd with a verified artefact. supervisord owns `:19419`, not `brew services`.
- **spyder ships bottles from the Mac** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) v0.82.0–v0.86.0) — GitHub Actions dropped; tapper cuts local bottles. brew spyder runs under supervisord, not launchd. Listen address survives restart; `app_exec` progress beats the dispatch watchdog.

### Significant Progress

- **Vanilla is deleted; React is the packaged UI** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)) — `feat(ui): package React and retire the vanilla runtime` removes the `web/` cockpit. Live `PinModel` calls `SetModel` instead of Stop-then-Launch (🎯T617): a failed relaunch had been advertising grok-4 on a stopped seat whose session would not load. Long cycle tools return a handle rather than blocking the turn past the 90 s stuck timer (🎯T600). An omitted provider lands on Claude while Claude has headroom (🎯T583). supervisord owns jevonsd (🎯T594).
- **Parse timeout and a pathological GLR fixture** ([marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) v0.19.0–v0.20.0, 🎯T56) — every parse is bounded so no source file can wedge the daemon; the git index takes the same guard. gotreesitter pinned at v0.47.1 (pathological on neither bash nor C).
- **Equality dispatch and tunable parallelism** ([arr-ai/frozen](https://github.com/arr-ai/frozen) v1.14.0) — `Equal(any)` dispatch fixed; parallelism is a knob rather than an implicit fan-out.

### Tough Challenges Overcome

- **A live switch that stopped the seat** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T617) — `PinModel` did `Stop` then `Launch`. Reproduced: pinning jevons-po grok-4.5 → grok-4 failed `session/load` ("Path not found; existing conversation; refusing to mint a replacement"), left `running=false`, and wrote grok-4 into the registry anyway. Live `SetModel` never touches the session; relaunch is only for `CapabilityError`, and that path snapshots and restores.
- **A healthy ambient cycle looked wedged** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T600) — cycle tools ran a whole model-backed pass inline against a 10-minute deadline while the cockpit's stuck-busy timer is 90 seconds, so a working agent earned roughly seven stuck verdicts before it was allowed to finish. Jobs validate synchronously, return a handle, persist across restart, and report `lost` rather than resolving to nothing.
- **Capture matching was order-dependent** ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) 🎯T29/🎯T30) — reference matching selected invalid bindings while sharing callees. The correction keeps successful golden fingerprints; ten failed-tree hashes were a deliberate T30 rebase. The optimisation keep/discard against `9c47802` is DISCARD/NOISY — not a reason to restore the old semantics.
- **A lost tmux window is a dead agent** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) 🎯T602) — a vanished window used to leave the `Agent` handle claiming life. Combined with 🎯T601 (a tmux Claude session can say whether a turn is running), event silence is no longer treated as absence of work on the jevons side.

### Contributors

- Marcelo Cantos (AI co-authors — Claude Opus 5, Claude Fable 5, Grok, Cursor — appear on `Co-authored-by` trailers throughout; xbnf, jevons and bullseye landings were largely the supervised fleet).

---

## Libraries & Infrastructure

### [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) — GLL+DFA Engine (79 commits, initial)

**The biggest effort of the week.** New product, not a wbnf upgrade. 489 file changes, **+29,253/−4,237** after excluding pinned third-party corpora. **~189 test functions** at week-end.

- **Language**: grammars and regexes are the same notation. `/term/` is a terminal in the language; `#wrap` is scoped whitespace; `|` is unordered (compile error unless a disambiguator is declared); `|>` is ordered choice and must not mix with `|`. `#prefer` / `#avoid` / `#assoc` / `#priority` / `#longest` are first-class. Self-host: `docs/xbnf.xbnf` is parsed by the engine.
- **Engine** (🎯T4/🎯T5): GLL for the general case (scannerless, native left recursion); regular fragments compile to character-class DFAs. Trees from GLL derivations (🎯T16); construction linear on lists (🎯T18). `fromwbnf` parses old `.wbnf` into an IR of meaning; leftover kinds are named gaps.
- **Seven languages Failed=0** (🎯T22): SQL vs `pg_query` (4/4), XML vs `xmllint` (8/8, including two W3C not-wf rejects), Go vs `go/parser` (5/5), Python vs CPython `compile` (6/6, invalid UTF-8 rejected), YAML vs PyYAML events (12/12; 2JQS follows the oracle not the suite label), JavaScript vs Acorn (5/5), CommonMark vs cmark (2/2). Pin lists were not shrunk after misses. Nestable `(?i:)` / `(?~i:)` is 🎯T24.
- **Speed with a keep/discard gate** (🎯T25): interleaved old/new pairs, load-idle, golden-identical trees required. KEEP: H2 fusion, H3 predecessor-linked evidence, unit-production shortcut, DFA ASCII tables, callee sharing (Afroozeh-style GSS), chart pool, 16-byte `uMap` slots. Final JSON 64 KB median **4.06 ms** / 2.35 MB / 2 allocs vs master 11.78 ms in the same run (2.882×, 10/10). Corpus aggregate 3.043×, B/op 18.89 → 3.20 MB. Public tree is the API floor; remaining candidates sit below the 3% KEEP bar.
- **Sandbox**: supervisord-hosted cheat sheet and syntax reference with runnable examples.

### [arr-ai/frozen](https://github.com/arr-ai/frozen) — Equality Dispatch (1 commit, v1.14.0)

Covered above. **~9 new tests**; +560/−41 across 8 files.

---

## Agent & Fleet Infrastructure

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — React Packaged, Live Switch (49 commits)

Continued from last week's React-daily landing. 381 file changes, **+10,439/−62,295**. **~111 new test declarations**.

- **Vanilla retired**: React is the packaged UI; the `web/` cockpit and vanilla proxy/devserver are deleted. Supervisor ownership is preserved during activation; the rendered React daemon definition is what supervisord applies.
- **Live model switch** (🎯T617), **job handles** (🎯T600), **claude-first mint** (🎯T583) are above. Also: Grok default/ladder/migrate picker are grok-4.6 (🎯T618); badge names the Grok session model under `GROK_HOME` (🎯T619); `event_push` to a mid-turn agent queues like `agent_send` (🎯T620).
- **Plan usage is a daemon verdict** (🎯T610): the ticker paints the band the daemon computed; colour answers how hard we must correct, not where we land (🎯T596). The hover is a table (🎯T588.1); rollover is local time to the minute. Memory can be taken out of the assessment for diagnosis (🎯T588).
- **Seats**: a briefless-seat check resolves the current session; active seats are never re-briefed (🎯T597). An undeliverable sendq message never makes a seat unkillable (🎯T599). A backlog held on a finished seat is routed, not re-announced (🎯T582). A blocked PO is obeying the product, not stalling (🎯T586). Codex work seats reach the gate store and loopback (🎯T598).
- **Chat**: owner user is a stream barrier (🎯T540.7.1); growing content is not the owner scrolling away (🎯T587); a reconnect during fan-out no longer kills the daemon (🎯T590); event silence is not absence of work (🎯T601); restart recovery stays on canonical history.

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Migrate, Turn Probe (8 commits, v0.29.0–v0.30.0)

Covered above. Also: a dependent package can stand up an overseer that is alive (`stub_agent`); Codex carries sandbox writable roots and network access (🎯T598); Claude dest identity is kept across migrate and stale ACP close is ignored. **~45 new tests**; +3,068/−215 across 48 files.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Apply Engine, HTTP Only (36 commits, v0.49.0–v0.52.0)

Covered above. Also: `graph.rs` split by role (frontier, validate, mermaid, render); unmaintained `fs2` dropped for `std::fs::File::try_lock`; `ErrorCode` threaded through ops/store instead of classifying by English; tests split into domain modules under `tests/core/`; broken-pipe on truncated CLI output exits quietly (🎯T77); `BLOCKED` is said where agents read, not only in the frontier (🎯T80); the product no longer instructs agents to hand-edit the ledger. **~24 net new `#[test]`** after the test-file split (201 added / 177 removed). +15,287/−11,210 across 117 files.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Argv Mode, Zstd Backup (18 commits, v0.91.0–v0.94.0)

Covered above. Compression finishes itself; a deferral cannot exile a session. Windows test binary gets a `.exe` suffix. **~25 new tests**; +3,204/−488 across 91 files.

---

## Tooling & Workflow

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Supervisord, Local Bottles (15 commits, v0.82.0–v0.86.0)

Covered above. Also: Squz team codesign picker; bullseye dirty-tree warn; `app_perf_get` retries until perf push lands; fakeApp writes serialised during progress beats; two achievement dates restored after a bullseye bug dropped them. **~14 new tests**; +1,356/−310 across 60 files.

### [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) — Bounded Parse (11 commits, v0.19.0–v0.20.0)

Covered above. Hygiene posture reconciled with the entropy-audit follow-up. Watcher FD-budget and tapper publish (🎯T58/🎯T59) landed on master under a test git identity and are not in these counts. **~11 new tests** in the Marcelo-authored slice; +2,278/−57 across 18 files.

### [marcelocantos/skills](https://github.com/marcelocantos/skills) — Single Tree (27 commits)

A backlog of `~/.claude/skills` republishes lands together with the unification onto one install tree and the progress-report gather path that reads `data/line-excludes.yaml`. Entropy-audit findings tracked as bullseye targets. +3,120/−732 across 100 files.

---

## Commercial

No commercial work landed on a default branch this week. In-flight (HMS Client Explorer and repository-schema repair; stock-car 3.25 Autodrive and Extreme Pro; dragster Unity IAP cutover) is summarised in [private week 2026-09-06](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-09-06.md).

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **Health-Management-Systems/hms** — 136 in-flight; detail in the private companion.
- **minicadesmobile/stock-car-racing** — 115 in-flight (3.25 Autodrive physics, Extreme Pro tracks, TestFlight/Play internals); detail in the private companion.
- **minicadesmobile/dragster-mayhem** — 9 in-flight (Unity IAP / Play Billing 8, Prime31 drop); detail in the private companion.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-08-31…09-06. In-flight branch work is excluded by design. Two progress-report pointer commits are omitted from the tables (reports/docs already excluded from ☲).*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **9** |
| Total landed commits | **244** |
| Total lines added (landed, filtered) | +68,565‡ |
| Total lines removed (landed, filtered) | −79,585‡ |
| Net new lines (landed, filtered) | −11,020‡ |
| File changes | 1,312 |
| New files created | ~357 |
| Bulk paths excluded from ☲ | +28,416 / −2,992 (xbnf corpora, jevons audit JSON, lockfiles, standing globs) |
| Releases published | **18** (bullseye v0.49–v0.52, claudia v0.29–v0.30, mnemo v0.91–v0.94, spyder v0.82–v0.86, sawmill v0.19–v0.20, frozen v1.14.0) |
| Languages | Go, Rust, TypeScript, TSX, JavaScript, Python, YAML, Markdown, Shell, HTML, CSS |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. New this run: xbnf `eval/testdata/*/corpus/**`, jevons `docs/audits/**/*.json`. jevons −51,856 net is vanilla-cockpit deletion.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) | 79 | 489 | +29,253 | −4,237 | +25,016 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 36 | 117 | +15,287 | −11,210 | +4,077 |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 49 | 381 | +10,439 | −62,295 | −51,856* |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 8 | 48 | +3,068 | −215 | +2,853 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 18 | 91 | +3,204 | −488 | +2,716 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 27 | 100 | +3,120 | −732 | +2,388 |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 11 | 18 | +2,278 | −57 | +2,221 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 15 | 60 | +1,356 | −310 | +1,046 |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | 1 | 8 | +560 | −41 | +519 |

\* *Vanilla cockpit (`web/`) deleted; React is the packaged UI.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) | ~189 | GLL/DFA, golden ratchet, seven-language eval, fromwbnf |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~111 | T617 live switch, T600 jobs, T583 claude-first, T610 band paint |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~45 | Migrate inert-seed, T601 turn probe, T602 lost window |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~25 | T158 prune-all-paths, T159 zstd artefact, T160 argv mode |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | ~24 net | apply engine + HTTP transport; test-file split inflates gross + |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~14 | watchdog beats, listen-addr persist, fakeApp serialise |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | ~11 | T56 parse timeout, pathological GLR fixture |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | ~9 | equality dispatch, parallelism knob |
| **Total** | **~428** | landed only; bullseye net after split |

### Daily Activity

![Daily active repositories](daily-activity-2026-09-06.svg)

*(Active repositories per day: Mon 08-31 9, Tue 09-01 4, Wed 09-02 5, Thu 09-03 5, Fri 09-04 1, Sat 09-05 2, Sun 09-06 4.)*

---

## Ideas & Innovations

### Alternation That Means Nothing Until You Say How ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf))
PEG ordered choice (`A / B`) is a control-flow construct pretending to be a grammar combinator: the first arm that matches wins, so a grammar change that reorders alternatives silently changes the language. xbnf's `|` has **no source-order meaning**. A decision that is neither provably deterministic nor covered by an explicit disambiguator (`#prefer`, `#longest`, `|>`) is a compile error. Unnecessary disambiguation is a warning. The engine can be GLL because the language never asked it to guess.

### Keep/Discard Is a Pair Ratio, Not a Median ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf))
Absolute ns/op on this laptop wanders with package temperature and P-core load. The gate compiles two test binaries, waits until load1 is a fraction of ncpu, then alternates old/new for 10 × 2 s at `GOMAXPROCS=1`. **Pair ratios cancel common-mode drift.** `KEEP` requires ≥3% faster on ≥80% of pairs, or a time-tie with a memory win; `NOISY` and `SELF-FAIL` refuse to decide. A golden update in an optimisation candidate is not an optimisation — it is a tree change and is judged as one.

### Stop, Then Launch, Is Not a Switch ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
claudia grew `Agent.SetModel` and `CapabilityModelSwitch` so a provider that can change model in-session does not have to re-attach. jevons kept doing Stop-then-Launch, which has to `session/load` the existing conversation, and claudia correctly refuses to mint a replacement. The failed path still wrote the new model into the registry. **Try the live switch first; relaunch only on `CapabilityError`; record the model only on success.** A supported switch that failed is a real failure, not a prompt to destroy the seat.

### A Handle That Survives Restart, or the Truth ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
A tool that blocks for minutes makes a working agent indistinguishable from a wedged one when the stuck timer is 90 seconds. Returning a handle is the easy half. **A handle that silently resolves to nothing after a restart is worse than the blocking call it replaces**, because the caller cannot tell "still running" from "gone". Records persist; a job that did not survive reports `lost`, with the reason.

### Nine Verbs, One Policy Table ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye))
Split, achieve, defer, reopen, and the rest had drifted into nine slightly different write paths. **`apply` is the engine; the verbs are sugar.** Drift tests fail when a verb's CLI/MCP surface and the engine disagree. The product also stopped telling agents to hand-edit the ledger — the instruction was the bug.

---

## Effort Estimate: Traditional vs. AI-Assisted

A parser-generator week sitting next to a fleet cockpit deletion and a ledger-engine rewrite. The xbnf KEEP gate and the jevons live-switch failure are the two places a wrong answer would have been silent.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| xbnf GLL+DFA engine, seven-language oracles, T25 KEEP programme | 18-28 | Scannerless GLL with a DFA layer; oracles are real parsers (pg_query, go/parser, CPython, PyYAML events, Acorn, cmark); speed changes must not move trees. |
| jevons React retirement, live switch, job handles | 8-12 | Packaged UI cutover without losing supervisor ownership; SetModel vs Stop-Launch; handles that survive daemon death. |
| bullseye apply engine + HTTP-only daemon | 5-8 | One write verb over a policy table with drift tests; process-lifetime caches under HTTP; stdio deletion. |
| claudia Agent.Migrate + turn/window probes | 3-5 | Inert-seed migrate that keeps subscriptions; a vanished tmux window is death, not a handle. |
| mnemo argv mode, zstd backup, supervisord | 3-5 | Every backup path must prune; artefact verified; one owner of the port. |
| spyder supervisord + local bottles | 2-3 | Watchdog beats from app_exec; listen-addr across restart; tapper not Actions. |
| sawmill bounded parse | 2-3 | Timeout around tree-sitter so a pathological file cannot wedge the daemon. |
| skills single-tree republish | 1-2 | Unification and exclude-path maintenance, not greenfield. |
| frozen equality dispatch | 1-1.5 | `Equal(any)` plus a parallelism knob. |

### The Diversity Tax

This week spans GLL/SPPF parser implementation, DFA construction, seven host-language oracles, Go cgo/zstd, Rust MCP-over-HTTP, tmux session lifetime, React packaging, Homebrew tapper bottles, and supervisord. No single engineer holds Scott–Johnstone GLL, frozen's `Equal(any)` dispatch, claudia's ACP migrate contract and Apple codesign bottle cutting at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| xbnf language and KEEP bar | 6-10 | Unordered `|`, oracle-present Failed=0, pair-ratio gate rather than a median, capture-context must not be reverted for speed. |
| jevons live-switch / handles | 4-6 | Reproducing Stop-Launch on a real seat; insisting a handle report `lost`. |
| bullseye apply / HTTP | 2-3 | One documented write verb; stdio deletion as a product decision. |
| mnemo/spyder supervisord | 2-4 | One owner of each port; bottles from the Mac. |
| Canticode / sawmill pin | 1-2 | gotreesitter 0.47.1 as the non-pathological pin. |

### What If It Were One Person?

The expert band sums to roughly 43-68 person-days. A single generalist pays ramp-up on GLL, seven parser oracles, Rust MCP HTTP, and tmux-anchor lifetime — four careers. The context-switch tax is the week's real cost: the parser generator, the cockpit deletion and the ledger engine do not share a cache.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~55-85 person-days (~2.8-4.3 months)** |
| Specialist team (traditional) | **~40-62 person-days (~2.0-3.1 person-months)** |
| Actual human effort this week | **~16-26 hours (~2.0-3.3 person-days)** |
| **Multiplier vs. generalist** | **~40-70x** |
| **Multiplier vs. specialist team** | **~25-45x** |

The multiplier peaks on xbnf (the expensive step is the KEEP gate plus oracle-present Failed=0, not writing a recursive-descent sketch) and on the live-switch failure (the expensive step is noticing the registry lied). It runs lowest on the skills republish. The human contribution concentrated on what a tool must refuse to do: that `|` does not mean ordered choice, that a pair-ratio of NOISY is not a speedup, that a failed model switch must not advertise the new model, and that a job handle which vanished is `lost`.

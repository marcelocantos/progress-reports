# Weekly Progress Report — 2026-06-29…07-05

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Excl-vendor landed lines: **+54,760/−49,810** (net **+4,950**).

## Executive Summary

**Nineteen repositories** saw landed work this week, and the week's defining event was not a single project but a **cross-fleet, AI-driven security and correctness audit** — the "Fable-5 deep audit" — run against **eight repos** (mnemo, sawmill, csp, pigeon, sqlpipe, doit, mcpbridge, [squz/ge](https://github.com/squz/ge)) with a disciplined methodology: per-dimension finders, two-lens adversarial re-verification that defaults every finding to "refuted" until a reachability lens *and* an invariant-validity lens both confirm it, findings filed as convergence targets, then same-week remediation shipped in releases. It surfaced genuine criticals — an AES-GCM nonce-reuse race in [pigeon](https://github.com/marcelocantos/pigeon), a `mnemo_query` read-only guard bypassable to `DELETE` and `ATTACH DATABASE` over federation, a [sawmill](https://github.com/marcelocantos/sawmill) `rename_file` that escaped its root to overwrite `~/.zshrc`, a [sqlpipe](https://github.com/marcelocantos/sqlpipe) diff-sync that wiped content-identical tables, a [doit](https://github.com/marcelocantos/doit) policy engine that failed *open* — and drove fixes verify-first, each landing with a regression test that fails on the unfixed code. Around that spine, **[squz/ge](https://github.com/squz/ge)** finished the **bgfx eradication** (sokol_gfx now the sole renderer, vendored submodules deleted — a −42,729-line purge), added a **render-on-demand** tier that idles when the scene is static, hardened `ge::Sprite` with RAII to kill an iPhone-13 crash, and built a **differential oracle harness** that makes the revived 2013 TiltBuggy the executable ground truth for its box2d reimplementation — shipping six releases (v0.66→v0.71). **[marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)** was again the highest-volume effort (46 commits, +5,670 Rust) and added a **no-oracle parity honesty ratchet** (🎯T14) that fails on both regressions *and* unrecorded improvements. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** shipped a **macOS menu-bar session navigator**, Codex CLI transcript ingest, and Developer-ID-signed releases (v0.55→v0.59); **[marcelocantos/sawmill](https://github.com/marcelocantos/sawmill)** landed a **discovery/retrieval tier** (FTS5 + reference-graph PageRank + vector embeddings with RRF fusion + AST-anchored `find_by_concept`, v0.16.0); **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** shipped **session rewind** (v0.14.0); **[marcelocantos/ytt](https://github.com/marcelocantos/ytt)** hardened its ingest pipeline against silent multi-day hangs (v0.9.0); and **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** collapsed its MCP surface to a single Starlark `app_exec` entry point. Commercial project detail: [private week 2026-07-05](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-05.md).

**169 commits** | **~+54,760 / ~−49,810** (excl. vendor) | **~14–24 person-days traditional equivalent** | **~30–55x multiplier**

> Honesty note: the raw line totals are dominated by non-authored content. **ge's −42,729** is almost entirely deletion of vendored bgfx/bimg/bx submodule sources (one commit is −39,767); **stock-car-racing's +10,343** is mostly Unity PSD decal assets and release churn; **sqlpipe's +1,535** is largely triplicated across `dist/`/Go/Swift mirrors. Genuinely hand-authored source is led by rustuml (+5.7k Rust), mnemo (~+10k Go incl. design docs), sawmill (~+8k Go), ge (~+3.9k C++), and csp (+2.9k C++).

### Major Achievements & Innovations

- **Fleet-wide Fable-5 deep audit + same-week remediation** ([csp](https://github.com/marcelocantos/csp), [pigeon](https://github.com/marcelocantos/pigeon), [sqlpipe](https://github.com/marcelocantos/sqlpipe), [mnemo](https://github.com/marcelocantos/mnemo), [sawmill](https://github.com/marcelocantos/sawmill), [doit](https://github.com/marcelocantos/doit), [mcpbridge](https://github.com/marcelocantos/mcpbridge), [squz/ge](https://github.com/squz/ge)) — an AI security/correctness audit ran across eight repos, surfacing multiple confirmed criticals and shipping fixes in csp **v0.20.0/v0.21.0**, pigeon **v0.25.0** and sqlpipe **v0.25.0** the same week. The methodology is the achievement as much as the findings: two-lens adversarial re-verification defaulting to "refuted" caught a false positive in mcpbridge (a self-unlinking listener) and set it aside rather than filing it.
- **ge bgfx eradication + render-on-demand + differential oracle harness** ([squz/ge](https://github.com/squz/ge)) — six releases (v0.66→v0.71): sokol_gfx becomes the sole renderer with the vendored bgfx submodules removed outright (🎯T77/T98), a render-on-demand loop idles when the scene is static (🎯T131/T132/T134), `ge::Sprite` gains RAII ownership to fix an iPhone-13 sprite-pool crash (🎯T135), the Android swapchain gets a depth buffer on both Vulkan and GLES3 (🎯T133), and 🎯T137's TiltBuggy feel pass ships a headless Chipmunk-vs-box2d differential harness (see Ideas).
- **sawmill discovery/retrieval tier** ([marcelocantos/sawmill](https://github.com/marcelocantos/sawmill), v0.16.0) — 🎯T38/T39/T40 build FTS5 search + a reference graph with PageRank, hybrid retrieval fusing vector embeddings via [Reciprocal Rank Fusion](https://en.wikipedia.org/wiki/Learning_to_rank), and `find_by_concept` — AST-anchored concept search that binds concepts to syntax nodes so they survive reformatting.
- **mnemo menu-bar navigator + Codex ingest + signed releases** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo), v0.55→v0.59) — a macOS menu-bar session navigator with live SSE (🎯T85/T86), a live config toggle without daemon restart (🎯T95), `mnemo_status` served from one nested sqldeep query (🎯T94), a drift-proof `mnemo_config` allowlist derived from the struct (🎯T96), Codex CLI transcript ingest (🎯T99), and macOS Developer-ID signing in the release pipeline.
- **claudia session rewind** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia), v0.14.0) — 🎯T5 rolls a conversation back *n* user turns (kill the process, truncate the session JSONL, resume replays the surviving prefix), made undoable via a `.rewind-bak` sidecar and careful never to land mid-tool-use; plus a stale-session resume-menu auto-advance that unblocks long-lived fleet agents.
- **ytt ingest hardening** ([marcelocantos/ytt](https://github.com/marcelocantos/ytt), v0.9.0) — after a run wedged silently for four-plus days, every network/LLM call gets a hard `SIGKILL` timeout, a run-level watchdog caps fan-out, and scheduled ingest survives network-unavailable fire windows, failing loudly with an honest non-zero exit rather than hanging.
- **csp concurrency-runtime hardening** ([marcelocantos/csp](https://github.com/marcelocantos/csp), v0.19.0→v0.21.0) — 🎯T3.10 forwards per-register provenance across `BL` call boundaries, 🎯T17.4 reworks TLS over a generic stream with two TLA+ specs modelling the drain protocol, and the audit's 🎯T31/T33 fix a stack-slot sizing bug that could silently corrupt cross-microthread stacks on arm64.
- **pigeon multi-service relay nodes** ([marcelocantos/pigeon](https://github.com/marcelocantos/pigeon), v0.25.0) — 🎯T44 lets one pairing fan out to concurrent services with a fresh per-session nonce in the HKDF, `Route` sub-addressing carried *inside* the end-to-end AEAD (the relay never learns the service), and an `enumerate` RPC over a reserved discovery stream.

### Significant Progress

- **rustuml — swimlane-v2 engine + parity honesty ratchet (46 commits, on master)** ([marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)) — the highest-volume effort: +5,670 Rust, continuing the second-generation swimlane activity-layout engine (nested fork/decision/while/repeat routing, break-corridor and backward-repeat geometry) matched family-by-family against the ~11k-entry golden corpus. 🎯T14 adds a `golden_no_oracle` tier that renders every golden through the real CLI with no oracle and exact-matches a recorded baseline — failing on regressions *and* unrecorded improvements — plus a `harness_guards` tier that freezes the anti-gaming constants (`GEOM_EPS == 0.02`, the 1,199-entry error-golden census). Honest baseline: 5,019/11,251 no-oracle exact matches (44.6%). No version tagged this week — develops on master.
- **spyder — single Starlark MCP entry point (2 commits)** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — 🎯T88 replaces the one-off MCP tools with `app_exec`, which runs an agent-supplied Starlark script server-side with every spyder verb as a builtin, so ordered/timed/looping device automation happens in one call; a shared `toolHandlers` map gives MCP-dispatch/Starlark parity by construction, with step-budget and wall-clock caps and a hermetic sandbox (no host I/O, no `load()`, no unbounded loops).
- **multimaze2 — iOS release-blocker clearance (10 commits)** — detail in [private week 2026-07-05](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-05.md)
### Tough Challenges Overcome

- **An AES-GCM nonce-reuse race hidden in C** (pigeon) — the audit found the production channel counter shared across every stream pump and the datagram pump and advanced by a non-atomic C read-modify-write; 16,384 concurrent encrypts produced 1,964 colliding nonce prefixes. The race lives in C, invisible to Go's race detector, so the fix needed a keystream-uniqueness oracle rather than `-race`.
- **A read-only database guard the client could switch off** (mnemo) — `mnemo_query` ran arbitrary client SQL on a pool guarded only by a client-resettable `PRAGMA query_only=1`, so `PRAGMA query_only=0; DELETE` wiped the DB and `ATTACH DATABASE` read arbitrary files — both reachable over mTLS federation. The fix installs a SQLite authorizer via `ConnectHook` denying ATTACH/DETACH and any query_only toggle.
- **A stack-slot size taken from a sample, not a bound** (csp) — 🎯T33 found `StackClass::Small` arena slots sized from a checkpoint-sampled high-water table that misses between-checkpoint peaks, risking silent cross-microthread stack corruption on arm64 with no guard page; the fix gates slot sizing on a *sound* analyser bound, restoring the repo's own `is_exact` invariant.
- **A file-mutation tool that could escape its root** (sawmill) — because sawmill rewrites user files, the audit weighted data-loss findings heavily: `rename_file` with `to="../../.zshrc"` overwrote arbitrary files with no recoverable backup, and undoing an edit to an originally-empty file *deleted* it (an empty-blob sentinel overload). Both are now root-contained and undo-safe.

### Contributors

- Marcelo Cantos

---

## Tooling & Workflow

### [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) — Swimlane-v2 + Parity Honesty Ratchet (46 commits)

**The highest-volume effort of the week.** As in Significant Progress — continuing the second-generation swimlane activity-layout engine (nested fork/decision/while/repeat connector routing, break and backward-repeat corridor geometry, terminal-survivor fusion) against the ~11k-entry golden corpus, plus re-enabled legacy v1 rendering for partitions/notes/chains. 🎯T14's `golden_no_oracle` tier renders every golden through the real `render_svg` CLI and exact-matches `no_oracle_baseline.txt`, failing on regressions *and* unrecorded improvements; `harness_guards` freezes the anti-gaming constants. +5,670/−383, 14 new `#[test]`, validated golden-by-golden against the Java PlantUML reference. (A large share of the 46-commit count is `Update bullseye.yaml` autosaves.)

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Menu-Bar Navigator + Codex Ingest (13 commits, v0.55→v0.59)

- **macOS menu-bar session navigator**: a Threads menu-bar app with live SSE (🎯T85/T86), toggling live without a daemon restart (🎯T95).
- **Query + config surface**: `mnemo_status` served from one nested sqldeep projection (🎯T94); a drift-proof `mnemo_config` patch allowlist derived from the struct (🎯T96).
- **Ingest reach**: Codex CLI transcripts from `~/.codex/sessions/` folded into the search spine (🎯T99); a topic-segmentation design doc (🎯T64.10).
- **Release engineering**: macOS Developer-ID signing integrated into the pipeline; Windows validated on the local VM rather than as a required CI gate.
- **Fable-5 audit** (`docs/audit/fable-2026-07.md`): 2 critical, 4 high filed; F2 (the read-only-guard bypass) and F4/F5 (`ATTACH` under `query_only=1`, a mid-stream commit persisting an overshooting Seek offset) confirmed. +10,075/−265, ~59 new `func Test`.

### [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) — Discovery/Retrieval Tier (6 commits, v0.16.0)

- **🎯T38 discovery tier**: FTS5 search + a reference graph + PageRank over the AST index.
- **🎯T39 hybrid retrieval**: vector embeddings fused with FTS via RRF, exposed as `semantic_search`.
- **🎯T40**: claudia-driven summaries feeding an LLM knowledge graph; `find_by_concept` binds concepts to syntax nodes (survives reformatting).
- **Fable-5 audit**: 2 critical, 8 high, data-loss-heavy — the `rename_file` root-escape and empty-file-undo deletion (both fixed), plus a 0o644 exec-bit drop, a non-atomic multi-file rename with no rollback, and a concurrent-map crash on `SummaryVecs`. +8,014/−149, ~64 new `func Test`.

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Session Rewind (8 commits, v0.14.0)

- **🎯T5 session rewind**: `RewindSession`/`Rewind`/`Unrewind` — a scorched-earth model (kill the process, truncate the session JSONL back *n* user turns, resume replays the surviving prefix), made undoable via a `.rewind-bak` sidecar; tool-result JSONL entries aren't counted as turns, so a rewind never lands mid-tool-use.
- **Stale-session auto-advance**: a readiness classifier distinguishes the `--resume` summary menu from an idle prompt and auto-confirms the default, unblocking long-lived fleet agents that wedge on `--resume`. +927/−520, ~10 new `func Test` plus a live `CLAUDIA_LIVE` e2e.

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — Ingest-Pipeline Hardening (7 commits, v0.9.0)

- **Hard timeouts everywhere**: `timeout`/`gtimeout` with `SIGKILL` on every network/LLM call (transcript 120s, synopsis 600s, discovery 120s), exit-124 classified transient and retried; a run-level watchdog caps ingest fan-out.
- **Survive the network being down** (🎯T5): scheduled ingest waits (bounded, ~4h) for connectivity in DarkWake windows, isolates a failing channel, validates 11-char video IDs before any `rm -rf`, and exits non-zero on an incomplete run. Root cause: a real run that wedged silently for four-plus days. +1,028/−202, ~9 new Bats (suite: 33 Bats + 18 pytest green).

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Starlark `app_exec` (2 commits)

- **🎯T88 app_exec**: a single Starlark entry point replacing the one-off MCP tools, running an agent-supplied script server-side with every spyder verb as a builtin; a shared `toolHandlers` map guarantees MCP/Starlark parity, with step-budget and wall-clock caps and a hermetic sandbox. An optional `path` param writes screenshots to disk instead of pushing base64 into context. +1,818/−410, ~19 new `func Test`.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) · [marcelocantos/skills](https://github.com/marcelocantos/skills) — Hygiene Posture + Auto-Sync

- **bullseye** (2 commits): declared its `hygiene.yaml` posture (second fleet repo after csp — tier 2, aspiring 3) and migrated it to schema v1 with per-dimension tiers and a `floors` ratchet map. +353/−11. **skills** (12 commits): mechanical `~/.claude/skills` auto-sync, +1,069/−193.

---

## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Concurrency-Runtime Hardening (11 commits, v0.19.0→v0.21.0)

- **🎯T3.10 provenance forwarding**: the stack-analysis walker forwards per-register provenance across `BL` boundaries so CONST-arg pruning survives calls.
- **🎯T17.4 stream-backed TLS**: `tls::conn` reworked over a generic stream, with `TlsConnDrain.tla` + `_Bug.tla` modelling the drain protocol (🎯T30 idiomatic examples alongside).
- **Audit remediation**: 🎯T31/T33 fix the stack-slot sizing bound and an ASan over-read; a CI hang watchdog makes a Linux-arm64 TSan intermittent hang core-dump and self-backtrace (🎯T29). +2,966/−1,023, ~4 doctest `TEST_CASE` plus a new `stack_slot_sizing` suite.

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) — Multi-Service Nodes + Audit (4 commits, v0.25.0)

- **🎯T44 multi-service nodes**: one `PairingRecord` fans out to concurrent sessions — a fresh 16-byte per-session client nonce in the HKDF (`info = direction ‖ nonce`), `Route` sub-addressing carried inside the end-to-end AEAD handshake, and an `enumerate` RPC over a reserved AEAD discovery stream.
- **Fable-5 audit**: 8 of 9 crit/high confirmed — the non-atomic `send_seq++` nonce-reuse race (fixed downstream next week), deterministic keys from a static pairing record with a counter reset, and a ~19.9-bit SAS code with no commit-reveal that a relay MitM can grind. +1,993/−144, ~6 new Go tests.

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Audit + Full Remediation (2 commits, v0.25.0)

- **Audit + remediation**: 2 critical, 6 high, 1 medium, several with compiled live reproductions (🎯T15–T23). The criticals: diff-sync keyed rows by `rowid` not PRIMARY KEY (wiping content-identical TEXT/composite-PK tables), and a `flush_pending` never reset so a committed-then-rolled-back transaction streams a phantom row into permanent replica divergence. All nine fixed in `dist/sqlpipe.cpp` and mirrored across the Go/Swift copies, with CI added. +1,535/−120, ~8 C++ doctest `TEST_CASE` (1:1 with the targets).

---

## Game Projects

### [squz/ge](https://github.com/squz/ge) — bgfx Eradication + TiltBuggy Oracle (13 commits, v0.66→v0.71)

**The biggest engine effort of the week.** As in Major Achievements — the bgfx purge (🎯T77/T98: vendored submodules removed, sokol_gfx the sole renderer, the dormant brokered H.264 path stubbed; the −42,729 is almost all deleted vendor source), the render-on-demand tier (🎯T131/T132/T134, `renderWhenStateChanges(gen)`, frames tracked via `framesPresented()`), `ge::Sprite` RAII crash hardening (🎯T135/T136) that flowed into multimaze2's 0.70 bump, an Android depth buffer on Vulkan+GLES3 (🎯T133), and 🎯T137's TiltBuggy feel pass with its differential oracle harness (see Ideas). The Fable-5 audit filed six targets (🎯T140–T144): stale `.d` dependency files never `-include`d (ODR/ABI skew), NULL-deref of the sokol dispatch table on the VK→GLES fallback, and a `PlayerWireBridge::pump` unsigned-underflow OOB read on malformed video messages. +4,205/−42,729 across 289 files; ~3 golden reference images refreshed plus the harness.

### [squz/multimaze2](https://github.com/squz/multimaze2) — iOS Release-Blocker Clearance (10 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-05](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-05.md).*
### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) — July-4th USA Promo (28 commits, v3.21→v3.23)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-05](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-05.md).*
### [unwisegames/tiltbuggy](https://github.com/unwisegames/tiltbuggy) · [minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit) — Reference Revival + Editor Fix

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-05](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-05.md).*
## Strategic Planning & Documentation

### [marcelocantos.com](https://github.com/marcelocantos/marcelocantos.com) — "The gut you can't code" (1 commit)

- A published blog post (a Socratic dialogue with Claude) arguing that an LLM session's cost is O(n²) not from self-attention but from *re-reading the whole transcript each turn* — a linear per-turn bill summing to quadratic cumulative — so the lever is keeping context lean; brains are cheap because they consolidate and *forget*, and quadratic is the price of refusing to. It ties the argument to why oracles exist: the model confabulates "done", a gut verdict with its reasoning stripped. +100.

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

Reported as a forward signal; excluded from shipped metrics to avoid cross-report double-counting.

- **Health-Management-Systems/hms** — detail in [private week 2026-07-05](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-05.md)
- **squz/esfera2** — detail in [private week 2026-07-05](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-05.md)
- **marcelocantos/rustuml** — 17 in-flight; **squz/yourworld2** — 41 in-flight; **marcelocantos/spyder** — 11 in-flight; **marcelocantos/mnemo** — 7; **marcelocantos/sawmill/mcpbridge/doit/csp** — small in-flight tranches.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-06-29…07-05. In-flight branch work is excluded by design. The report repo itself is excluded.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | 19 |
| Total landed commits | 169 |
| Total lines added (landed) | +54,760‡ |
| Total lines removed (landed) | −49,810‡ |
| Net new lines (landed) | +4,950‡ |
| Authored net lines (estimate) | ~+25–30k (rustuml, mnemo, sawmill, ge, csp leading) |
| Languages | Rust, Go, C++, Objective-C++, C, GLSL, C#, Python, Starlark, TLA+, Markdown, YAML, shell |
| Contributors | 1 (Marcelo Cantos) |

‡*Line totals are distorted by non-authored content: **ge's −42,729 is a vendored bgfx-submodule purge**, stock-car-racing's +10,343 is largely Unity PSD assets, and sqlpipe's diff is triplicated across language mirrors. The net collapses to ~+4k because of the bgfx deletion; hand-authored net is ~+25–30k. A large share of the 169-commit count is `Update bullseye.yaml` autosaves (rustuml) and skills auto-sync.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | 46 | 52 | +5,670 | −383 | +5,287 |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 28 | 156 | +10,343 | −1,373 | +8,970 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 13 | 92 | +10,075 | −265 | +9,810 |
| [squz/ge](https://github.com/squz/ge) | 13 | 289 | +4,205 | −42,729 | −38,524† |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 12 | 25 | +1,069 | −193 | +876* |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 11 | 46 | +2,966 | −1,023 | +1,943 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 10 | 26 | +1,222 | −193 | +1,029 |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 8 | 17 | +927 | −520 | +407 |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 7 | 32 | +1,028 | −202 | +826 |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 6 | 80 | +8,014 | −149 | +7,865 |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 4 | 28 | +1,993 | −144 | +1,849 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 2 | 18 | +1,818 | −410 | +1,408 |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 2 | 27 | +1,535 | −120 | +1,415 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 2 | 2 | +353 | −11 | +342 |
| [marcelocantos/doit](https://github.com/marcelocantos/doit) | 1 | 2 | +503 | −53 | +450 |
| [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) | 1 | 2 | +483 | −1 | +482 |
| [unwisegames/tiltbuggy](https://github.com/unwisegames/tiltbuggy) | 1 | 8 | +880 | −1,392 | −512 |
| [marcelocantos/marcelocantos.com](https://github.com/marcelocantos/marcelocantos.com) | 1 | 1 | +100 | −0 | +100 |
| [minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit) | 1 | 1 | +8 | −1 | +7 |

\* *skills: auto-sync of `~/.claude/skills`.*
† *ge: net is dominated by the −42,729 bgfx-submodule purge; authored engine code is ~+3.9k.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | ~64 | discovery/retrieval tier + audit regressions |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~59 | menu-bar/config/ingest + `TestQueryRejects…` audit regressions |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~19 | app_exec engine + structural parity assertions |
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | 14 (+2 golden tiers) | swimlane geometry + no-oracle parity ratchet over ~11k goldens |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~10 | rewind prefix/metamorphic + live e2e |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | ~9 | ingest-timeout Bats |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~8 | audit repros (1:1 with 🎯T15–T23) |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | ~6 | per-nonce distinctness, multi-service e2e |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~4 | stack-slot sizing suite + TLS drain specs |
| [squz/ge](https://github.com/squz/ge) | ~3 goldens | TiltBuggy reference images + differential harness |
| **Total** | **~196 (+goldens)** | landed only; conservative diff-grep estimates |

### Daily Activity

![Daily active repositories](daily-activity-2026-07-05.svg)

*(All-repo active-repository counts per day — a broad signal counting all authors and branches, so it runs higher than landed Marcelo-only work. Plotted: Mon 06-29 14, Tue 06-30 10, Wed 07-01 6, Thu 07-02 1, Fri 07-03 8, Sat 07-04 4, Sun 07-05 8. A front-loaded week: the bulk of releases and the bgfx purge landed Monday–Tuesday.)*

---

## Ideas & Innovations

### An Executable 2013 Game as the Parity Oracle ([squz/ge](https://github.com/squz/ge))
ge's new TiltBuggy is a [box2d](https://box2d.org/) reimplementation of a 2013 game that ran on [Chipmunk](https://chipmunk-physics.net/) 6.2.1. Rather than tune physics by eye against video, 🎯T137 makes the *original game the oracle*: `oracle.cpp` extracts the 2013 physics verbatim — every constant, body, constraint, tread and per-axle grip callback — and runs it headless against the real vendored Chipmunk from the revived tiltbuggy repo, while `harness.cpp` drives both it and the box2d scene through identical seeded scenarios and measures trajectory drift. The insight is that **the ground truth is executable, not a golden video**: it samples divergence at fixed horizons (1/3/10/30/60/90 frames), reports p50/p90/p99/max so linear ULP drift is distinguishable from chaotic blow-up, and *semantically classifies* wild heading divergence into benign bifurcation (both cars fishtailing — chaos, but game semantics agree) versus genuine disagreement (only one spins). Reviving a 13-year-old game to serve as a decision procedure is oracle-first parity taken to its logical end.

### An Audit That Defaults to "Refuted" ([marcelocantos/csp](https://github.com/marcelocantos/csp), and seven others)
Most automated security passes over-report: they flag a pattern and leave a human to sift true positives from noise. The Fable-5 deep audit inverts the burden of proof — every candidate finding is **assumed refuted until two independent lenses confirm it**, a reachability lens (can an adversary actually reach this?) and an invariant-validity lens (is the violated property real?). The elegance is what it buys downstream: findings that survive are filed as convergence targets with compiled live reproductions, so remediation is verify-first (a test that fails on the unfixed code), and findings that *don't* survive — like mcpbridge's "socket hijack" that turned out to be a self-unlinking listener — are set aside with a recorded rationale rather than clogging the backlog. An audit whose output is a set of *decidable* targets, not a report, is one whose fixes can be proven.

### A Parity Ratchet That Refuses Silent Improvement ([marcelocantos/rustuml](https://github.com/marcelocantos/rustuml))
Byte-exact reproduction of an undocumented layout engine is easy to overfit and easy to game: nudge an epsilon, and a "pass" can hide a regression or an accidental, unexplained improvement. 🎯T14's `golden_no_oracle` tier renders every one of ~11,251 goldens through the real CLI with the oracle switched off and exact-matches a recorded baseline — **so both a regression and an unrecorded improvement fail the build** — while `harness_guards` freezes the anti-gaming constants (`GEOM_EPS`, the error-golden census) so the ratchet itself can't be loosened silently. The honesty is structural: every gain in parity must be explicitly recorded to be admitted, which turns "44.6% exact" into a number you can trust.

### Retrieval That Survives Reformatting ([marcelocantos/sawmill](https://github.com/marcelocantos/sawmill))
Text search over code breaks the moment the code is reformatted, renamed, or moved — the string index points at bytes, not meaning. sawmill's discovery tier layers three retrieval models — FTS5 for lexical hits, a reference graph with PageRank for structural centrality, and vector embeddings fused via Reciprocal Rank Fusion for semantic recall — and tops them with `find_by_concept`, which **binds concepts to AST nodes rather than line ranges**, so a concept survives a rename or a whitespace churn that would invalidate a text index. The combination turns "where is the thing that does X" from a grep into a ranked, structure-aware query.

### Rolling a Conversation Back Without Landing Mid-Tool-Use ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
Resuming an agent after a wrong turn usually means starting over or hand-editing a transcript. claudia's 🎯T5 rewind kills the process, truncates the session JSONL back *n* user turns, and lets resume replay the surviving prefix — but the subtlety is in *what counts as a turn*: **tool-result entries are excluded from the turn count**, so a rewind can never land in the middle of a tool call and leave the agent expecting a result that will never come. A `.rewind-bak` sidecar makes the whole operation undoable, so an over-eager rewind is itself reversible.

### Idle-Safe Rendering as a Battery Contract ([squz/ge](https://github.com/squz/ge))
A mobile game engine that redraws every frame regardless of whether anything changed burns battery for nothing. ge's render-on-demand tier stops and starts the render loop so a static scene costs no frames, and — the harder half — **decouples sensor streams from forcing a redraw**, so a device that is merely being held still doesn't defeat the idle. Frame ground truth is tracked explicitly via `framesPresented()`/`recordPresent()` rather than assumed, so the engine can prove it idled rather than hope it did.

---

## Effort Estimate: Traditional vs. AI-Assisted

A heavy week, defined less by a single flagship than by a **fleet-wide correctness campaign** (the Fable-5 audit across eight repos, with same-week remediation) running alongside a major engine consolidation (ge's bgfx eradication and TiltBuggy oracle), a highest-volume layout-engine push (rustuml), and a clutch of shipped tool releases (mnemo, sawmill, claudia, ytt, csp, pigeon, sqlpipe). Hardening and correctness in character, but across an unusually broad surface.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| Fable-5 audit (8 repos) + remediation | 5-8 | Reachability-plus-invariant adversarial verification across concurrent C/Go/C++ code, crypto (AES-GCM nonce reuse), SQL authorizers, and file-mutation safety — each finding needing a compiled live repro and a verify-first fix. |
| ge bgfx purge + render-on-demand + TiltBuggy oracle | 3-5 | A renderer-backend eradication touching every graphics primitive, an idle-safe render loop with sensor decoupling, and a headless Chipmunk-vs-box2d differential harness with statistical horizon sampling and semantic divergence classification. |
| rustuml swimlane-v2 + parity ratchet | 3-4 | Byte-exact reverse-engineering of PlantUML's undocumented swimlane geometry against a Java reference, plus an anti-gaming parity harness that fails on unrecorded improvement. |
| mnemo menu-bar + Codex ingest + signing | 2-3 | A live macOS menu-bar SSE navigator, a second transcript-source ingest, single-query status, and Developer-ID release signing. |
| sawmill discovery/retrieval tier | 2-3 | FTS5 + PageRank + vector embeddings + RRF fusion + AST-anchored concept binding — a full retrieval stack over a code index. |
| claudia rewind + ytt hardening + spyder app_exec | 2-4 | Turn-safe conversation rewind, `SIGKILL`-timeout ingest hardening after a silent multi-day wedge, and a hermetic Starlark automation sandbox. |
| multimaze2 + stock-car + Minicades | 2-3 | iOS release-blocker clearance (paywall/nav/gating) and a date-gated store promo across three versions. |

### The Diversity Tax

This week spans Rust (rustuml's layout engine), Go (mnemo, sawmill, claudia, spyder, pigeon), C++ and GLSL (ge, csp, sqlpipe), Objective-C++ and Metal (ge, the tiltbuggy revival), Chipmunk and box2d physics, C# and Unity (stock-car, multimaze2), Starlark sandbox design, TLA+ (csp's drain specs), plus applied cryptography, SQLite authorizers, and cross-platform release engineering. No single engineer holds adversarial crypto audit, PlantUML-layout reverse-engineering, GPU renderer eradication, physics-parity oracle design, and code-retrieval ranking at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| Fable-5 audit + remediation | 3-5 | Judging which findings are real, approving verify-first fixes and the set-aside of false positives, release approvals across six repos. |
| ge / tiltbuggy | 3-5 | Reviving the original game, validating physics-parity feel, judging the differential-harness thresholds, on-device crash verification. |
| rustuml | 2-3 | Steering the parity push, deciding replicate-vs-approximate, blessing the honesty ratchet's baseline. |
| mnemo / sawmill / claudia / ytt / spyder | 3-5 | Menu-bar UX checks, retrieval-quality judgement, rewind-safety review, ingest-wedge diagnosis, sandbox-scope decisions. |
| Games + everything else | 2-4 | Store-promo timing and play-testing, release approvals, convergence triage. |

### What If It Were One Person?

A single generalist would pay a ramp-up cost re-entering each domain — Rust reverse-engineering, Go daemons, C++/Metal rendering, Chipmunk physics, applied crypto, SQLite internals — and a heavy context-switching tax bouncing across nineteen repos and a fleet-wide audit in one week. The expert-days band (~14–24) understates the generalist total once those costs are added, which is why the generalist estimate sits well above a specialist team's.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~14-24 person-days (~0.7-1.2 months)** |
| Specialist team (traditional) | **~9-15 person-days (~0.45-0.75 person-months)** |
| Actual human effort this week | **~13-23 hours (~2-3.5 person-days)** |
| **Multiplier vs. generalist** | **~30-55x** |
| **Multiplier vs. specialist team** | **~15-30x** |

The multiplier runs highest on the Fable-5 audit — cross-domain adversarial reasoning over concurrent crypto, SQL and file-safety code is exactly the recall-and-search task where the AI dominates a lone generalist — and on ge's TiltBuggy oracle, where reviving a 13-year-old physics engine to serve as an executable ground truth is unthinkable to schedule manually. It runs lowest on the release/plumbing tail (skills auto-sync, the store-version bumps, the bullseye.yaml autosaves). The human contribution concentrated on judgement a specification can't reach: which audit findings are real and which are noise, how faithful the physics parity must feel, where the honesty ratchet's baseline sits, and the on-device verification no agent can perform.

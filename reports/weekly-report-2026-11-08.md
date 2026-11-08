# Weekly Progress Report — 2026-11-02…11-08

## Executive Summary

**Forty-two repositories** landed **1,099 commits**, and twenty-one of them were created this week. **[marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)** ran a parity-recovery campaign of 680 commits that made its gates fail closed and rebuilt its parity evidence as reviewed maker/checker rounds. **[marcelocantos/gouml](https://github.com/marcelocantos/gouml)** began as a Java-to-Go transpiler for PlantUML and already emits the whole `klimt` tree. **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** shipped five releases (v0.81.0–v0.85.0) of fleet-agent autonomy, from broker-mediated seat messaging to interrupts that cannot lose a steered message. On 6–7 November a burst of small oracle-first repositories appeared — **killset**, **quorum**, **witness**, **relic**, **fidelity**, **falsify**, **teddy**, **headroom**, **gist** and a dozen more — each built around a frozen exam that its own author cannot edit. **sqlpipe**, **mnemo**, **spyder**, **bullseye** and **vellum** shipped eight more releases. Client work on [HMS](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-11-08.md) and Stock Cars continued (private companion).

**1,099 commits** | **<span style="color:#1a7f37">+350,638</span> net lines** | **~93-143 person-days traditional equivalent** | **~20-55x multiplier**

### Major Achievements & Innovations

- **Fleet agents that survive failure and each other** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.81.0–v0.85.0). Seats manage and message each other through the broker, and a fleet agent keeps its conversation through ordinary failures (T247). Fleets gained timers, budgets and checks, with check exports produced by walking git objects, streamed, and refused when commit paths collide (T248). One rule of authority applies to every agent, and a retiring agent hands what it created to its creator (T249). Expectations wake a sender once, and an expedite steers or interrupts (T250). Each ledger entry was achieved against a live oracle on the tagged release.
- **sqlpipe reaches Postgres** ([marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) v0.35.0–v0.36.0). Bundles are reproducible and a live Go Postgres path exists. The sqldeep PostgreSQL runtime is vendored for JSON, joins and `RECURSE`, and a bundled Postgres sqlift supplies schema fingerprints. A live replica keeps applying after an early `DiffReady`, and migrations no longer read sqlpipe's own tables as drift.
- **spyder drives Android apps** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) v0.103.0–v0.104.0). Native-app UI verbs landed as 🎯T180: `input_text`, `input_key` with repeat, `ui_tree`, `ui_tap` and `screen_secure`, with a refreshed test report.
- **bullseye keys ledgers by remote** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) v0.58.0). External ledgers are keyed by origin remote with the path as fallback (🎯T113), which achieved worktree discovery (🎯T108). Portfolio discovery no longer follows symlinks into cloud storage, and the TLC formal run chooses its JDK explicitly instead of trusting the jenv shim.
- **mnemo v0.115.0–v0.116.0** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)). One stuck stream pass no longer stalls every reconciler stream. `/health` warns when Apple Vision OCR is process-disabled, release archives ship the zstd BSD licence, and the release flow is local and PR-free (#208).
- **vellum v0.37.0** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum)). Viewer tables use the panel width and size columns to content, the Confluence layout capture runs in Chrome with the sandbox on, and macOS builds pin Apple's clang unless `CC` is set.

### Significant Progress

- **rustuml parity recovery** ([marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)). The campaign started from a measured baseline: `golden_pairs` 10,496 pass and 755 fail, `parity_perturbations` 349 of 810, two harness guards failing. Parity gates now fail closed, reference provenance is pinned, and empty baseline overrides are rejected. Work then ran as numbered maker rounds with independent checker batches — TIM line continuation went through seven, with YAML block porting, HarfBuzz buffer marks, SVG text CR and per-face font advances following the same pattern. The code fixes run to 86 plain `fix` commits plus 18 sequence and 7 preprocess fixes, and 275 review records document the evidence. About 335 test declarations were added.
- **gouml, a transpiled PlantUML** ([marcelocantos/gouml](https://github.com/marcelocantos/gouml)). `j2go` parses the whole PlantUML tree with tree-sitter, attributes types, and emits one Go package with stubs for everything else; the `rt` shim supplies Java semantics for strings, numbers, collections, exceptions and dispatch. Klimt-wide emission (285 files) reaches the runtime boundary, the source reader compiles with faithful dispatch, embedded Graphviz drives source-based graph rendering, and source diagrams render through the generated pipeline.
- **jv0, a fleet client spike** ([marcelocantos/jv0](https://github.com/marcelocantos/jv0), 🎯T1391). How much unattended work can agents coordinate with only `start`, `send`, `stop` and `list`? The spike moved from a private broker to the shared claudia broker, pursues a measured objective with a steward instead of a driver, and ended as a terminal with no commands of its own.
- **Oracle-first toolkit.** Eighteen repositories started on 6–7 November, each leaning on a frozen contract and planted mutants that must fail. They are covered below under *Oracle-First Experiments*.

### Tough Challenges Overcome

- **A worker that claims it is done** ([marcelocantos/witness](https://github.com/marcelocantos/witness), [quorum](https://github.com/marcelocantos/quorum), [relic](https://github.com/marcelocantos/relic)). A file the worker writes cannot prove completion. Witness has the signer measure the tree itself and sign with a key the worker cannot read, and `witness check` refuses a push unless the receipt names the tip tree. Quorum runs an allow-listed oracle outside the worker's tree against a `git archive` of the claimed commit, and Relic turns receipts that name a different tree into queryable rows.
- **Interrupts that lose a message** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia), T250). An interrupt could arrive after a message had been steered in, hit a turn the seat no longer had, mask the turn's own error, or block a stop. Interrupts are now tied to their turn, take back an already steered message, keep the turn's error, and never block a stop. A failed interrupt leaves the steered message in its turn, and a rerun says so.
- **Gates that pass vacuously** ([marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)). At the campaign's start the decimal and review-evidence guards failed and a deployment ratchet was off by one, so a green run meant little. The gates now fail closed, pin provenance, and reject empty overrides.
- **Java semantics under transpilation** ([marcelocantos/gouml](https://github.com/marcelocantos/gouml)). Emitted code needed Java's operator precedence on infix expressions, parenthesised compound-assignment right-hand sides, class initialisation before instance code reads statics, boxed `byte` and `short` font attributes, and generic collection views that keep object identity and aliasing.

### Contributors

- Marcelo Cantos (AI co-authors — Claude, Grok, Cursor, Codex — on trailers throughout).

---

## Parity & Transpilation

### [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) — Parity Recovery Campaign (680 commits)

520 file changes, <span style="color:#1a7f37">+112,401</span>/<span style="color:#cf222e">−15,838</span> after excluding the generated review records, font-chain dumps and vendored `third_party/`. **~335 added test declarations**. No tag.

- **Fail-closed gates**: the parity gates reject missing evidence, pin the reference build's provenance, and refuse empty baseline overrides. A fresh-assessment table at the campaign's start records `golden_no_oracle` 11,180 of 11,251, `golden_pairs` 10,496 pass and 755 fail of 12,550 pairs (1,199 Java error pages and 100 ditaa cases skipped), and `parity_perturbations` 349 of 810.
- **Maker and checker rounds**: 212 `docs` and 75 `targets` commits record each round's measurements, a checker batch, and a verdict. TIM line continuation took seven rounds, and the sprite, creole, YAML and font-advance work followed the same pattern.
- **Fixes**: 86 `fix`, 18 `fix(sequence)` and 7 `fix(preprocess)` commits, covering YAML block parsing, YAML line preprocessing, HarfBuzz 15.0.0 buffer marks, SVG text carriage returns, and Verdana and Arial per-face ASCII advances read from the face files.
- **Housekeeping**: the Homebrew formula publishes through tapper (#58), CI moved to Node 24 action majors (#56), and a hygiene declaration and entropy audit are tracked.

### [marcelocantos/gouml](https://github.com/marcelocantos/gouml) — Java-to-Go PlantUML Transpiler (39 commits, initial)

A Go port of [PlantUML](https://plantuml.com) produced by mechanical transpilation of the Java source, not by hand. 439 file changes, <span style="color:#1a7f37">+41,060</span>/<span style="color:#cf222e">−1,845</span> after excluding `pu/` (the generated package), lifted Graphviz and expat trees, embedded assets and font tables.

- **The transpiler** (`cmd/j2go`): a tree-sitter front end, type attribution, a JDK table and an emitter with stubs. `klimt.geom` first emitted with one diagnostic; klimt-wide emission reached 285 files; `--exclude` works at class level; AWT `AffineTransform` and `Float.isFinite` were added.
- **The runtime** (`rt`): Java strings, numbers, collections, exceptions and dispatch, with DOM, stream, `Random`, `Font` and XML-factory shims, and an encoding contract in `docs/encoding.md`.
- **Rendering**: embedded Graphviz connects to source-driven graph rendering, reference SVGs come from the oracle's Graphviz 12.2.0, and source diagrams render through the generated pipeline. Syntax-error pages draw with the golden version header, and the empty-diagram welcome page renders.
- **Targets**: T1.1 (phase-1 gate) was achieved, with a boxed-null census (T1.5) and runtime residue (T1.6) tracked.

---

## Agent & Fleet Infrastructure

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Fleet Autonomy (29 commits, v0.81.0–v0.85.0)

119 file changes, <span style="color:#1a7f37">+9,725</span>/<span style="color:#cf222e">−948</span>. **~117 added test declarations**.

- **Fleet liveness (T247, v0.81)**: seats manage and message each other through the broker, and agents keep their conversation through ordinary failures.
- **Timers, budgets and checks (T248, v0.82)**: check commits are exported by walking objects and streamed with confined links, a check whose commit has colliding paths fails, and interrupted turns finish.
- **Authority (T249, v0.83)**: one rule of authority, tools chosen by whoever starts an agent, and a retiring agent's creations passed to its creator.
- **Expectations and interrupts (T250, v0.84–v0.85)**: expectations wake a sender once, an expedite steers or interrupts, interrupts reach only a turn the seat has, and the residue is tracked as T251.

### [marcelocantos/jv0](https://github.com/marcelocantos/jv0) — Coordination Spike (29 commits, initial)

111 file changes, <span style="color:#1a7f37">+5,912</span>/<span style="color:#cf222e">−4,219</span>. A spike for 🎯T1391 in Jevons, built on claudia's broker and finishing as a client that pins v0.85.0.

- **Shape**: `start`, `send`, `stop` and `list` as the only primitives, a steward that pursues a measured objective with fresh attempts, an overseer and stewards that stay reachable, and `!` and `!!` to hurry the owner's messages.
- **Testing**: a fake seat, fake hub and HTTP clients exercise REPL dispatch, objective lifetime, MCP identity and paste handling.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — v0.58.0 (5 commits)

Ledgers keyed by origin remote (🎯T113), T108 achieved, T112 filed (link fork ledgers to surface cross-repo candidates), and discovery no longer follows symlinks into cloud storage.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — v0.115.0–v0.116.0 (12 commits)

See Major Achievements. The bullseye content hash was refreshed after a rebase, and the Windows VM gate pins the sqldeep version CI builds.

### [marcelocantos/headroom](https://github.com/marcelocantos/headroom) — Admission Check (5 commits, initial)

Answers `allow`, `defer` or `deny` before an agent session starts. It reads a loadmon SQLite file, a mnemo-shaped session snapshot and a hardware fixture, gates claudia spawn, and replays a recorded hour or a copied loadmon history against frozen admission decisions and the mutants that must fail them.

### [marcelocantos/loadmon](https://github.com/marcelocantos/loadmon) (2 commits), [marcelocantos/den](https://github.com/marcelocantos/den) (2 commits)

loadmon packages the macOS release from its checkout and records that directory growth must stay readable with the popover closed. den's scheduled source-build smoke job gained a per-job timeout (#208) and an automatic retry on macOS runner capacity cancels (#209).

---

## Oracle-First Experiments

Eighteen repositories began on 6–7 November. Each leans on a frozen contract and on planted mutants that must fail. Several gate through `make oracle` targets rather than test declarations.

### [marcelocantos/killset](https://github.com/marcelocantos/killset) — A Frozen Exam for Test Suites (30 commits, initial)

Scores a test suite by the planted, historically real defect classes it actually kills. The suite never writes the corpus, the expected kill set or the threshold. The week added the output-vector and sealed-output exams, an adversary that hashes the shipped output inverse, canonicalisation outside the sandbox, and tracked fingerprint residue as 🎯T9 and 🎯T10.

### [marcelocantos/fidelity](https://github.com/marcelocantos/fidelity) — Provable Migration Fidelity (17 commits, initial)

Drives a legacy system and its port with the same tapes, compares structured fields, honours explicit waivers for bug-for-bug quirks, and emits a certificate. It added a Lyapunov horizon contract for dynamical ports, a second post-horizon statistic so energy drift alone cannot pass, residue comparison by class, and certificates that are rejected when they hide a different port. The OpenBSD `cal` port is certified, with the first port kept as a failing case.

### [marcelocantos/witness](https://github.com/marcelocantos/witness), [quorum](https://github.com/marcelocantos/quorum), [relic](https://github.com/marcelocantos/relic) — Completion Receipts (4, 6 and 6 commits, initial)

Witness signs a receipt for the tree a signer measured and refuses a push without it, generalising claudia's gate-attestation pattern. Quorum appends a hash-chained attestation only when an oracle the worker did not choose passes, and requires a witness signature on each pass receipt. Relic is a read-only SQLite database over `bullseye.yaml` ledgers, receipts, gate attestations and git history, whose flagship query finds achieved goals whose receipt names a different tree or does not exist.

### [marcelocantos/falsify](https://github.com/marcelocantos/falsify), [gist](https://github.com/marcelocantos/gist), [teddy](https://github.com/marcelocantos/teddy) — Agent Memory and Claims (8, 3 and 7 commits, initial)

falsify turns the falsifiable part of a video-knowledge corpus into typed claims with runnable checks whose failures are the product, freezing labels and the scorer before any model run and scoring the held-out extraction once. gist is a fixed-size lossy memory with one lossless, content-addressed quote organ, scored against a frozen corpus and byte budget. teddy stops a repeating agent until it writes a structured note (what it believes, tried and still has red), then hands a collaborator a capped excerpt; a detector agreed with hand labels on held-out and 200-window sets.

### [marcelocantos/openwindow](https://github.com/marcelocantos/openwindow), [nightkernel](https://github.com/marcelocantos/nightkernel), [inkline](https://github.com/marcelocantos/inkline) — Checkers and Provers (4, 6 and 6 commits, initial)

openwindow checks a JSONL trace of `(pre_state, action, post_state)` against an action spec and calls a spec that accepts every mutant vacuous; it now checks traces against unmodified TLA+ with TLC. nightkernel has a local drafter propose a Lean 4 proof or a counterexample for 32 corpus items (sixteen true, sixteen false), with a verdict `proved` only when the Lean kernel accepts it. inkline compiles an Orthograph scene into a structural invariant a Go codebase can fail, checking `depends` edges from `types.Info.Uses`, and a PlantUML picture of it.

### [marcelocantos/membrane](https://github.com/marcelocantos/membrane) — Placing Relational Programs (12 commits, initial)

One relational program runs unchanged on client, edge or server, with a planner choosing where each derived relation lives and sqlpipe replicating every cross-site edge. The week proved every legal placement computes the same inbox, replayed one recorded trace on sqlpipe sites for each placement (🎯T7.4, 🎯T7 achieved), re-executed a derived table for the changed group only, and placed semijoin, union, difference and rank.

### Workshop and bench repositories (initial)

- **[marcelocantos/benchbook](https://github.com/marcelocantos/benchbook)** (14 commits): a ledger of local-inference runs with prefill and decode rates and a host snapshot. Each trial gets its own prefixed prompt, cached prefills are rejected, cells are warmed before recording, and installed Ollama models were measured with variance.
- **[marcelocantos/holdstill](https://github.com/marcelocantos/holdstill)** (8 commits): a stop-motion bench that accepts a frame only when every locked rectangle still matches, now scored with photometric correlation instead of an 8×8 hash and with small-fault labels on a second held-out seed.
- **[marcelocantos/chipwindow](https://github.com/marcelocantos/chipwindow)** (4 commits): a feeds-and-speeds calculator that stays inside a published window or refuses with a reason.
- **[marcelocantos/turnaround](https://github.com/marcelocantos/turnaround)** (8 commits): a discrete-event launch-site toy with seeded logs, three golden site policies, and each pad owning its trench.
- **[marcelocantos/reactionpath](https://github.com/marcelocantos/reactionpath)** (12 commits): a workholding puzzle held only when a planar statics solver names a reaction for every applied force, with twelve playable levels in a `file://` page and an offline contact simplex.

---

## Libraries, Hardware & Documents

### [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) — Opt-In Decimal, Aligned with the Fork (10 commits)

99 file changes, <span style="color:#1a7f37">+6,699</span>/<span style="color:#cf222e">−1,587</span>. **~27 added test declarations**. The proposal now argues for built-in types and is aligned with the fork on IEEE 754-2019, per-target encoding, NaN payloads and FPgen gates (#13, #16). Decimal is opt-in behind a playground experiment switch (#20), the playground shares programs through the URL fragment (#15) and runs an IEEE 754-2019 operations example with a ppc64le QEMU job (#18), the fork is pinned with a GDB decimal printer (#19), and a reflection-library survey is checked in CI (#17).

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) — Hygiene Targets T60 (12 commits)

67 file changes. **~24 added test declarations**. The pairing wire driver steps a generated FSM through a shared trace (🎯T60.4), a PathSwitch TLC ratchet has a non-tautological oracle (🎯T60.6), relay TLS config threads through the pairing ceremony (ENT-007), a dual-API commentary hazard is closed with a cwire ratchet (🎯T60.8), and a hygiene posture declares SDLC scanners (🎯T60.10).

### [marcelocantos/gadgets](https://github.com/marcelocantos/gadgets) — ESP32-S3 `sshbox` and GhostKey (9 commits)

`sshbox` gives SSH into a tiny Unix-like shell on the ESP32-S3, working over Wi-Fi with libssh atomic uploads, cursor movement and readline-style editing, a `power` command, and `x`, a small stack language with a typed C FFI. GhostKey is firmware for USB keyboard passthrough with keep-awake.

### [marcelocantos/threedee](https://github.com/marcelocantos/threedee) — Dissections and a Dovetail (7 commits)

A printable Dudeney haberdasher from exact piece coordinates with closed-form areas, Perigal, a Greek cross and a 9×4 rectangle in the dissection cabinet, and a 14.25° dovetail frozen as a referent before the solid is built. **~20 added test declarations**.

### Smaller landings

**[marcelocantos/think](https://github.com/marcelocantos/think)** (26 commits): the 6 November idea storm of four lenses and 31 pitches, plus transcript ingestion and an active-projects table. **[canticode/orthograph](https://github.com/canticode/orthograph)** (2): the in-car agent surface (T28) and a daemon-hosting decision (T29), recorded in the bullseye ledger. **[goeezi/check](https://github.com/goeezi/check)** and **[goeezi/gopkgdep](https://github.com/goeezi/gopkgdep)** (1 each): CI on current Actions majors and supported Go releases, and ignored errors fixed in the path walk, dot renderer and trie writer. **[marcelocantos/skills](https://github.com/marcelocantos/skills)**, **[progress-reports](https://github.com/marcelocantos/progress-reports)** and **[progress-reports-private](https://github.com/marcelocantos/progress-reports-private)** (1 each) are housekeeping.

---

## Commercial

**[Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms)** — 46 commits, <span style="color:#1a7f37">+30,383</span>/<span style="color:#cf222e">−2,492</span> after the new `hms2/tools` evidence and generated-file excludes. **[minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing)** — 3 commits on `main`. Full narrative: [private week 2026-11-08](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-11-08.md).

**[squz/ge](https://github.com/squz/ge)** had no activity.

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **[canticode/orthograph](https://github.com/canticode/orthograph)**: 179 on branches. **[marcelocantos/rustuml](https://github.com/marcelocantos/rustuml)**: 305. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)**: 52. **[marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal)**: 37, and the Go decimal fork: 32.
- **[marcelocantos/slacker](https://github.com/marcelocantos/slacker)**: 28. **[marcelocantos/real](https://github.com/marcelocantos/real)**: 16. **gouml**: 6. **finance**: 6. **mnemo**: 5. **jv0**: 5. Commercial in-flight work is in the private companion.

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **42** |
| Total landed commits | **1,099** |
| Total lines added (landed, filtered) | <span style="color:#1a7f37">+384,586</span>‡ |
| Total lines removed (landed, filtered) | <span style="color:#cf222e">−33,948</span>‡ |
| Net new lines (landed, filtered) | <span style="color:#1a7f37">+350,638</span>‡ |
| File changes | 3,828 (summed per commit; a path touched twice counts twice) |
| Bulk paths excluded from ☲ | <span style="color:#1a7f37">+13,399,507</span>/<span style="color:#cf222e">−6,386,840</span> on counted repos, dominated by rustuml's 11.5M-line parity-review records and an HMS evidence tree deleted in one commit |
| Releases published | **13** (claudia v0.81.0–v0.85.0; mnemo v0.115.0–v0.116.0; sqlpipe v0.35.0–v0.36.0; spyder v0.103.0–v0.104.0; vellum v0.37.0; bullseye v0.58.0) |
| Languages | Rust, Go, Python, C, C++, Lean, Delphi/Pascal, C#, Shell, TLA+, Markdown, YAML |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. **New this run:** rustuml `docs/parity-reviews/**`, `tools/font-chain-reference/**` and `third_party/**`; gouml `pu/**`, `third_party/**`, `pu/assets/**` and font tables; HMS `hms2/tools` oracle evidence, portsets and generated stubs; think `analysis/**`.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | 680 | 520 | <span style="color:#1a7f37">+112,401</span> | <span style="color:#cf222e">−15,838</span> | <span style="color:#1a7f37">+96,563</span> |
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | 46 | 429 | <span style="color:#1a7f37">+30,383</span> | <span style="color:#cf222e">−2,492</span> | <span style="color:#1a7f37">+27,891</span> |
| [marcelocantos/gouml](https://github.com/marcelocantos/gouml) | 39 | 439 | <span style="color:#1a7f37">+41,060</span> | <span style="color:#cf222e">−1,845</span> | <span style="color:#1a7f37">+39,215</span> |
| [marcelocantos/killset](https://github.com/marcelocantos/killset) | 30 | 203 | <span style="color:#1a7f37">+10,049</span> | <span style="color:#cf222e">−1,164</span> | <span style="color:#1a7f37">+8,885</span> |
| [marcelocantos/jv0](https://github.com/marcelocantos/jv0) | 29 | 111 | <span style="color:#1a7f37">+5,912</span> | <span style="color:#cf222e">−4,219</span> | <span style="color:#1a7f37">+1,693</span> |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 29 | 119 | <span style="color:#1a7f37">+9,725</span> | <span style="color:#cf222e">−948</span> | <span style="color:#1a7f37">+8,777</span> |
| [marcelocantos/think](https://github.com/marcelocantos/think) | 26 | 37 | <span style="color:#1a7f37">+2,987</span> | <span style="color:#cf222e">−55</span> | <span style="color:#1a7f37">+2,932</span> |
| [marcelocantos/fidelity](https://github.com/marcelocantos/fidelity) | 17 | 591 | <span style="color:#1a7f37">+32,450</span> | <span style="color:#cf222e">−633</span> | <span style="color:#1a7f37">+31,817</span> |
| [marcelocantos/benchbook](https://github.com/marcelocantos/benchbook) | 14 | 64 | <span style="color:#1a7f37">+6,837</span> | <span style="color:#cf222e">−175</span> | <span style="color:#1a7f37">+6,662</span> |
| [marcelocantos/reactionpath](https://github.com/marcelocantos/reactionpath) | 12 | 112 | <span style="color:#1a7f37">+5,051</span> | <span style="color:#cf222e">−264</span> | <span style="color:#1a7f37">+4,787</span> |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 12 | 67 | <span style="color:#1a7f37">+3,183</span> | <span style="color:#cf222e">−353</span> | <span style="color:#1a7f37">+2,830</span> |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 12 | 72 | <span style="color:#1a7f37">+2,829</span> | <span style="color:#cf222e">−876</span> | <span style="color:#1a7f37">+1,953</span> |
| [marcelocantos/membrane](https://github.com/marcelocantos/membrane) | 12 | 82 | <span style="color:#1a7f37">+9,325</span> | <span style="color:#cf222e">−107</span> | <span style="color:#1a7f37">+9,218</span> |
| [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) | 10 | 99 | <span style="color:#1a7f37">+6,699</span> | <span style="color:#cf222e">−1,587</span> | <span style="color:#1a7f37">+5,112</span> |
| [marcelocantos/gadgets](https://github.com/marcelocantos/gadgets) | 9 | 86 | <span style="color:#1a7f37">+7,355</span> | <span style="color:#cf222e">−377</span> | <span style="color:#1a7f37">+6,978</span> |
| [marcelocantos/turnaround](https://github.com/marcelocantos/turnaround) | 8 | 37 | <span style="color:#1a7f37">+7,176</span> | <span style="color:#cf222e">−602</span> | <span style="color:#1a7f37">+6,574</span> |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 8 | 52 | <span style="color:#1a7f37">+2,992</span> | <span style="color:#cf222e">−435</span> | <span style="color:#1a7f37">+2,557</span> |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 8 | 23 | <span style="color:#1a7f37">+2,080</span> | <span style="color:#cf222e">−62</span> | <span style="color:#1a7f37">+2,018</span> |
| [marcelocantos/holdstill](https://github.com/marcelocantos/holdstill) | 8 | 45 | <span style="color:#1a7f37">+7,665</span> | <span style="color:#cf222e">−392</span> | <span style="color:#1a7f37">+7,273</span> |
| [marcelocantos/falsify](https://github.com/marcelocantos/falsify) | 8 | 48 | <span style="color:#1a7f37">+8,153</span> | <span style="color:#cf222e">−96</span> | <span style="color:#1a7f37">+8,057</span> |
| [marcelocantos/threedee](https://github.com/marcelocantos/threedee) | 7 | 30 | <span style="color:#1a7f37">+10,431</span> | <span style="color:#cf222e">−234</span> | <span style="color:#1a7f37">+10,197</span> |
| [marcelocantos/teddy](https://github.com/marcelocantos/teddy) | 7 | 73 | <span style="color:#1a7f37">+10,651</span> | <span style="color:#cf222e">−88</span> | <span style="color:#1a7f37">+10,563</span> |
| [marcelocantos/relic](https://github.com/marcelocantos/relic) | 6 | 41 | <span style="color:#1a7f37">+3,745</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+3,745</span> |
| [marcelocantos/quorum](https://github.com/marcelocantos/quorum) | 6 | 26 | <span style="color:#1a7f37">+4,224</span> | <span style="color:#cf222e">−119</span> | <span style="color:#1a7f37">+4,105</span> |
| [marcelocantos/nightkernel](https://github.com/marcelocantos/nightkernel) | 6 | 49 | <span style="color:#1a7f37">+4,475</span> | <span style="color:#cf222e">−153</span> | <span style="color:#1a7f37">+4,322</span> |
| [marcelocantos/inkline](https://github.com/marcelocantos/inkline) | 6 | 61 | <span style="color:#1a7f37">+6,233</span> | <span style="color:#cf222e">−82</span> | <span style="color:#1a7f37">+6,151</span> |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 5 | 15 | <span style="color:#1a7f37">+235</span> | <span style="color:#cf222e">−15</span> | <span style="color:#1a7f37">+220</span> |
| [marcelocantos/headroom](https://github.com/marcelocantos/headroom) | 5 | 33 | <span style="color:#1a7f37">+3,556</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+3,556</span> |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 5 | 15 | <span style="color:#1a7f37">+735</span> | <span style="color:#cf222e">−98</span> | <span style="color:#1a7f37">+637</span> |
| [marcelocantos/witness](https://github.com/marcelocantos/witness) | 4 | 48 | <span style="color:#1a7f37">+5,242</span> | <span style="color:#cf222e">−414</span> | <span style="color:#1a7f37">+4,828</span> |
| [marcelocantos/openwindow](https://github.com/marcelocantos/openwindow) | 4 | 78 | <span style="color:#1a7f37">+5,031</span> | <span style="color:#cf222e">−82</span> | <span style="color:#1a7f37">+4,949</span> |
| [marcelocantos/chipwindow](https://github.com/marcelocantos/chipwindow) | 4 | 65 | <span style="color:#1a7f37">+3,796</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+3,796</span> |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 3 | 4 | <span style="color:#1a7f37">+65</span> | <span style="color:#cf222e">−16</span> | <span style="color:#1a7f37">+49</span> |
| [marcelocantos/gist](https://github.com/marcelocantos/gist) | 3 | 27 | <span style="color:#1a7f37">+11,315</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+11,315</span> |
| [marcelocantos/loadmon](https://github.com/marcelocantos/loadmon) | 2 | 5 | <span style="color:#1a7f37">+49</span> | <span style="color:#cf222e">−1</span> | <span style="color:#1a7f37">+48</span> |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 2 | 3 | <span style="color:#1a7f37">+174</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+174</span> |
| [canticode/orthograph](https://github.com/canticode/orthograph) | 2 | 0 | <span style="color:#1a7f37">+0</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+0</span> |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 1 | 5 | <span style="color:#1a7f37">+116</span> | <span style="color:#cf222e">−93</span> | <span style="color:#1a7f37">+23</span> |
| [marcelocantos/progress-reports-private](https://github.com/marcelocantos/progress-reports-private) | 1 | 1 | <span style="color:#1a7f37">+1</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+1</span> |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 1 | 3 | <span style="color:#1a7f37">+36</span> | <span style="color:#cf222e">−17</span> | <span style="color:#1a7f37">+19</span> |
| [goeezi/gopkgdep](https://github.com/goeezi/gopkgdep) | 1 | 6 | <span style="color:#1a7f37">+153</span> | <span style="color:#cf222e">−5</span> | <span style="color:#1a7f37">+148</span> |
| [goeezi/check](https://github.com/goeezi/check) | 1 | 4 | <span style="color:#1a7f37">+11</span> | <span style="color:#cf222e">−11</span> | <span style="color:#1a7f37">+0</span> |

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | ~335 | Parity gates, sequence and preprocess fixes, harness guards |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~117 | Fleet liveness, authority, expectations and interrupt races |
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | ~34 | Delphi-semantics and census tests |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~27 | Android UI verbs |
| [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) | ~27 | Playground and fork-pin checks |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | ~24 | Pairing driver, TLC ratchet, hygiene gates |
| [marcelocantos/threedee](https://github.com/marcelocantos/threedee) | ~20 | Dissection areas, dovetail and gauge checks |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | ~16 | Ledger keying, discovery |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~13 | Reconciler streams, health warning |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~9 | Postgres runtime, replica recovery |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | ~2 | Viewer tables |
| **Total** | **~624** | |

### Daily Activity

![Daily active repositories](daily-activity-2026-11-08.svg)

---

## Ideas & Innovations

### The Signer Measures the Tree ([witness](https://github.com/marcelocantos/witness), [quorum](https://github.com/marcelocantos/quorum), [relic](https://github.com/marcelocantos/relic))

A completion claim written by the agent that wants the credit is worthless, however it is formatted. **Move the measurement out of the worker's reach.** Witness has a signer run the oracle itself and sign a receipt for the exact tree with a key the worker cannot read, so a receipt for any other tree is refused at push time. Quorum attests only from an allow-listed command stored outside the worker's tree, run against a `git archive` of the claimed commit, and Relic then makes "achieved, but the receipt names another tree" a plain SQL query.

### An Exam the Suite Cannot Write ([killset](https://github.com/marcelocantos/killset))

Test suites are usually graded by the people who wrote them. killset **scores a suite by the planted, historically real defect classes it kills**, with the corpus, expected kill set and threshold all outside the suite's control. Adversaries that edit the source, spoof a path or hash the shipped output inverse are added as frozen exams of their own, and the fingerprint residue they expose is tracked as targets.

### A Spec That Accepts Every Mutant Is Vacuous ([openwindow](https://github.com/marcelocantos/openwindow))

A checker that says yes to a trace proves nothing if it would also say yes to a corrupted one. openwindow **mutates each trace and treats a spec that accepts all of them as a failure**, not a pass, then validates the spec against unmodified TLA+ with TLC. A yes only counts when a no was possible.

### Transpile, Do Not Port ([gouml](https://github.com/marcelocantos/gouml))

Hand-porting PlantUML's Java would drift from its rendering quirks. gouml **transpiles the Java mechanically and keeps Java's semantics in a runtime shim**, so generated code is never edited by hand and `make gen` regenerates it. Faithful dispatch, boxed numerics and shared collection views live once in `rt` instead of being rediscovered per diagram.

### Expectations Wake a Sender Once ([claudia](https://github.com/marcelocantos/claudia), [jv0](https://github.com/marcelocantos/jv0))

A fleet whose agents message each other either floods or goes quiet. Claudia lets a sender state what it expects back, **wakes a sender once about its expectations**, and lets an expedite choose between steering a running turn and interrupting it. jv0's `!` and `!!` use the same two levers for the owner, so one mechanism serves agents and humans.

### Bound the Memory, Keep One Exact Organ ([gist](https://github.com/marcelocantos/gist))

Session cost grows quadratically when every turn re-reads the transcript. gist **updates a fixed-size state as each turn is written** and keeps a single lossless, content-addressed quote organ for the text that must survive verbatim, then scores the pair against a frozen corpus and a byte budget with planted budget and quote mutants.

---

## Effort Estimate: Traditional vs. AI-Assisted

The week's volume came from an authorised parity campaign in rustuml, a new transpiler, five claudia releases, and a burst of eighteen small repositories that each carry their own frozen exam. Most of the week's difficulty is correctness surface: gates that cannot be gamed, and evidence that has to be re-measured rather than asserted.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| rustuml parity campaign | 18-28 | Pixel and XML parity with a Java renderer; font metrics and HarfBuzz shaping; fail-closed gates with pinned provenance; ~335 tests and 275 review records. |
| gouml | 15-24 | A tree-sitter Java front end with type attribution, a JDK table and a Java-semantics runtime; embedded Graphviz; klimt-wide emission of 285 files. |
| Oracle-first repositories (18) | 30-45 | Frozen contracts and mutant corpora in each; signing and attestation, Lean proofs, TLC trace checking, statics solving, dynamical-system certificates, local-inference benchmarking. |
| claudia v0.81–v0.85 and jv0 | 10-15 | Broker-mediated seat messaging, authority rules, timers and budgets, object-walking check exports, steer and interrupt races. |
| HMS | 8-12 | Delphi 6 semantics translated and checked against real Delphi; Variant, DFM and VCL behaviour. |
| sqlpipe, mnemo, spyder, bullseye, vellum, pigeon, go-decimal-proposal, gadgets, threedee, others | 12-19 | Postgres replication with reproducible bundles; Android UI automation; ledger keying; TLC ratchets; decimal proposal and ESP32 firmware. |

### The Diversity Tax

Java-to-Go transpilation, PlantUML layout and font metrics, signed attestation and key custody, test-suite mutation scoring, Lean 4 proofs, TLA+ trace checking, agent-broker protocol races, Delphi 6 semantics, Postgres replication, Android UI automation, ESP32 firmware, rigid-body statics and CAD dissections. No single specialist holds that range.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| rustuml | 5-9 | Authorising the campaign, setting the acceptance rules, reviewing and integrating the checked rounds. |
| gouml | 2-4 | Choosing transpilation over a hand port and setting the encoding contract. |
| Oracle-first repositories | 5-9 | Selecting pitches from the idea storm, reviewing each frozen contract and mutant set. |
| claudia and jv0 | 3-6 | The authority and expectation rules, and release sign-off. |
| HMS | 2-4 | Real-Delphi comparison runs and fidelity review. |
| Stock Cars | 1-2 | The Thanksgiving and Black Friday go-ahead. |
| Others | 2-4 | Release sign-off and small design calls. |

### What If It Were One Person?

The specialist band sums to roughly 65-100 person-days. A generalist would also need ramp-up on the PlantUML internals, Lean and TLA+ tooling, the broker wire protocol and Delphi 6. Landed activity ran every day (4–23 repositories), peaking on Saturday 7 November when the new repositories began.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~93-143 person-days (~4.4-6.8 months)** |
| Specialist team (traditional) | **~65-100 person-days (~3.1-4.8 person-months)** |
| Actual human effort this week | **~20-38 hours (~2.5-4.8 person-days)** |
| **Multiplier vs. generalist** | **~20-55x** |
| **Multiplier vs. specialist team** | **~14-40x** |

The multiplier is highest on the rustuml campaign and the new-repository burst, where machine-checked review rounds and frozen exams absorb most of the cost. It is lowest on HMS and Stock Cars, where real-Delphi runs and studio decisions set the pace. The human contribution was mostly rules: a gate must fail closed, a claim needs a measurement the claimant did not make, and a port is only done when an exam it cannot edit says so.

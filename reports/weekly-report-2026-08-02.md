# Weekly Progress Report — 2026-07-27…08-02

## Executive Summary

**Nineteen repositories** landed work this week, and the dominant thread is *containment of the agent fleet itself*. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** had its largest week of the series — 27 commits and **fourteen releases** (v0.69.0→v0.82.0) — carrying streaming topic segmentation, a first-principles token-cost engine, and the fix for a genuine incident: a summariser obeyed an instruction embedded in a transcript it was asked to describe and spawned roughly **33,000 subagents over two hours, burning about 4.3 billion tokens**. Closing that required a fix in **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** first (v0.20.0), whose Task mode had silently never applied the tool restrictions the package documented. **[squz/ge](https://github.com/squz/ge)** cut **eight tags** (v0.84.0→v0.91.0) including a gesture-hint service in which one authored timeline both draws an SDF cartoon hand *and* injects real synthetic touch events through the production input path, and a `.getp` cube-sphere tile-pyramid format whose coarser variants are **byte prefixes** of the finer ones. **[marcelocantos/csp](https://github.com/marcelocantos/csp)** shipped v0.27.0–v0.29.0: a Windows listen hang traced to a missing `FD_ACCEPT`, an ARM64 machine-code stack analyser that sizes microthread stacks from measured SP displacement, and a five-target audit campaign that fixed six latent bugs. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** (v0.8.0) became a daily driver — mid-session MCP reconnect, prefix-first attention threads, queued overseer notifications. **[marcelocantos/ytt](https://github.com/marcelocantos/ytt)** was ported to Go and *dropped* a dependency doing it; **[marcelocantos/slacker](https://github.com/marcelocantos/slacker)** was created. Forty releases across eleven repositories. Commercial project detail: [private week 2026-08-02](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-02.md).

**115 commits** | **+73,514 net lines** | **~22-36 person-days traditional equivalent** | **~35-60x multiplier**

> Honesty note: ☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs; **+8,171/−2,793** of bulk was filtered this week (ge generated `headers/` and LFS `prebuilt/`, csp's `dist/` amalgamation, lockfiles, `bullseye.yaml`). No new exclude globs were needed for this week's repositories. Commercial project detail: [private week 2026-08-02](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-02.md).

### Major Achievements & Innovations

- **Stripping summarisers of the ability to act on what they read** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) 🎯T139, [marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.20.0) — a tool that summarises transcripts by feeding them to a headless model is running untrusted input through a live agent, and the model cannot distinguish data from instructions. A transcript containing the casual line *"research X and Y. go deep with fanout"* was obeyed: the summariser opened "I will research X and Y, fanning out across multiple angles" and spawned on the order of **33,000 subagents over two hours — roughly 4.3 billion tokens**, many failing on blocked tools and *retrying* rather than aborting. mnemo had two paths of that shape and both were exposed. The restriction could not be written until claudia was fixed: Task mode passed **no** `--disallowedTools` at all and `TaskConfig` had no field to supply one, at every release through v0.19.0, while the package documented `Agent`, `TeamCreate`, `TeamDelete`, `SendMessage` and `EnterWorktree` as always disallowed. That guarantee existed only in Session mode.
- **A token-cost engine derived from published pricing, not from a vendored tool** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) 🎯T135/🎯T136/🎯T137, v0.79.0) — a behavioural specification for turning transcripts into a figure that *reconciles with an invoice*, written against observed behaviour and public rate cards rather than a reference implementation that ships only as a compiled binary. The conclusion was that mnemo does not need the tool at all: everything beyond pricing is a `GROUP BY` over data already ingested, and the rate card is a public 1.6 MB JSON file covering 2,984 models. Four real defects fell out, each verified against live data — **message-id duplication** (192,442 groups appear twice against 168,167 once, one group repeating `input=5/output=1/cacheRead=18,529` six times, so naive summing over-counts by **1.95× to 2.83×** with the factor varying by class, so no scalar correction works); **cache-write TTL tiers** (73% of cache-write volume is the long-TTL tier, proven arithmetically when an Opus day fit no single rate — $6.527 computed against $7.9230 reported — and closed exactly at the long-TTL rate); **long-context repricing** above a per-model threshold, making cache writes a 2×2 matrix over TTL and context size; and an O(entire corpus) shape mismatch that would have had a daemon re-reading 9.9 GB every tick.
- **One timeline drives the hand and the touch events** ([squz/ge](https://github.com/squz/ge) 🎯T170/🎯T177/🎯T179/🎯T180, v0.86.0→v0.90.0) — `ge::hint` compiles a gesture into a keyframed `Clip`: per-pointer tracks of position, contact, press and opacity plus tagged events (`contact`, `release`, `apex`, `pinch-start`) that fire through a callback at the exact timeline moment. Trajectory is a runtime parameter, never baked, so a swipe hint runs from *this* card to *that* slot, and motion is interpolated continuously rather than quantised to authored frames (ProMotion-friendly). Two independent consumers hang off it: an SDF hand renderer that re-derives a white-fill/black-outline cartoon hand from the gesture skeleton every frame in a fragment shader via a smooth-min capsule union — no textures, no atlas, resolution-independent — and a **strictly opt-in** `InputDriver` that converts the same interpolated states into synthetic SDL finger events delivered through the app's normal event path, so a drag demo rotates a real `GlobeController` and a tap demo presses a real `ge::Button` **with zero correlation code and no possibility of drift between what is drawn and what is injected**. Synthetic events carry a reserved `SDL_TouchID` (`'SP2G'`) so games can filter consequences, and `cancel()` lifts held fingers cleanly so a game is never left mid-drag.
- **A tile-pyramid format whose coarse packs are byte prefixes of the fine ones** ([squz/ge](https://github.com/squz/ge) 🎯T168, v0.84.0) — the new `.getp` container holds, per plane, a quadtree pyramid over six gnomonic cube faces whose order and orientation match sokol's cubemap slice order exactly, so a direction sampling texel (u,v) of slice F hits the same ground point in tile space. Payload blobs are ordered coarse level → fine, planes interleaved per level, so **cooking with a smaller `levelCap` yields a byte-prefix-compatible pack and a device can simply stop reading early**. Planes carry independent encodings — ASTC 4×4 for imagery, RG8 carrying a 16-bit id for per-pixel country identity after 254 regions overflowed a `u8`, nearest-sampled and single-mip. `queryDeviceTier()` decides depth once from physical RAM and a live `sg_query_pixelformat` ASTC check, with the threshold set at 5.5 GiB because devices under-report RAM through carve-outs; games call it and pass `tier.levelCap(levels)` with no branching of their own.
- **csp v0.28.0 — an audit campaign that fixed six latent bugs and then deleted code** ([marcelocantos/csp](https://github.com/marcelocantos/csp) 🎯T46–🎯T50) — five targets landing in two days: six real defects from a code-smell audit, removal of dead and vestigial code, single-sourcing of network-stack helpers and of hot-path duplicated protocols (with benches verified flat, so the consolidation cost nothing), and a consistency pass over the combinator library. The `dist/` amalgamation mirrors every `src/` edit, which is why csp's authored ☲ (+6,414/−3,031) sits well below its raw diff.
- **An ARM64 stack analyser that sizes microthread stacks from machine code** ([marcelocantos/csp](https://github.com/marcelocantos/csp) 🎯T52, v0.29.0) — `analyze_stack_depth` walks the compiled function, following calls to a bounded depth, and returns the maximum SP displacement in bytes plus an `is_exact` flag that goes false on unresolvable indirect branches. Indirect `BLR` targets loaded from data-derived addresses are resolved by reading live memory and evaluating recursively; unresolvable ones consume a documented per-call budget. The composed slot rule is `kShellStackBytes + analyze(invoke).max_depth`, where the 1 KiB shell constant is a **measured** true-peak of the leanest imp under stack painting (≈352 B) with a ≥2× margin, and an audit gate asserts the measured peak stays under the constant whenever painting is on. The residual — the deep exception-report path in `spawn_entry` — is declared rather than papered over, with soft-guard overflow checks left as the tripwire.
- **Windows listen hang, root-caused to one missing event bit** ([marcelocantos/csp](https://github.com/marcelocantos/csp) 🎯T39, v0.27.0) — the reactor's `WSAEventSelect` mask omitted `FD_ACCEPT`, so a listening socket never signalled readiness and the whole suite wedged. Landing it also required making `win-validate.ps1` reliable enough to believe.
- **sawmill v0.18.0 — rename that understands scope, and an equivalence oracle** ([marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) 🎯T50/🎯T51/🎯T55) — `RenameInFile` no longer rewrites every identifier text match: for Go and Python it builds a lexical binding model and renames only occurrences of the *selected* binding, module-level by default or the binding at a given position. A `behavioural_equiv` oracle joins it, the adapter matrix reached **18 languages** (Lua, Protobuf, Zig, Bash and SQL added), and a `languages` MCP tool serves per-language capability cards with caveats — because agents connecting to a server do not read the agents guide, and the honest answer to "can you rename in Bash" is "best-effort", which now arrives at the point of use.
- **ytt v0.11.0 — a port that removed a dependency** ([marcelocantos/ytt](https://github.com/marcelocantos/ytt) 🎯T14) — the CLI and transcript layer became Go, dropping Python and `youtube-transcript-api` in favour of `yt-dlp`, which was *already* required for discovery: ytt had been carrying two YouTube-facing dependencies with overlapping capability. A Go transcript library was deliberately **not** adopted — YouTube churns its internal caption APIs constantly, yt-dlp absorbs that with near-daily releases, and a small Go package would rot while leaving ownership of the breakage hardest to detect. Verified differentially: golden outputs were captured from the installed 0.11.0 binary *before* the port and replayed against the Go build.
- **vellum v0.8.0 — one media-orthogonal `convert`** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum) 🎯T14) — four MCP tools collapsed into a single `convert` taking `from`/`to` media (`file`, `content`, `clipboard`, `file_reference`), formats inferred aggressively, with only content/clipboard PDF sinks refused. Legacy sugars expand into the same `convert.Run` router rather than living beside it, and the clipboard gained Finder-style file references that survive process exit.
- **bullseye v0.40.0–v0.43.0 — attestation, postponement, and machine-scoped ids** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) 🎯T41/🎯T50–🎯T58) — `achieve` now **requires a free-text attestation** and rejects trivial tokens like "done": not formal proof, but a note on how the target is met, persisted on the target and surfaced in every view. Alongside it: a content hash stamped on `bullseye.yaml` with rehash repair, postpone/wake frontier gating, machine-scoped `T{node}.{seq}` allocation (subsequently backed out in favour of short sequential numbers when dual clones on one machine proved the scheme wrong), advisory graph hygiene, and Mermaid subgraph selection for `view=graph`.
- **spyder v0.74.0–v0.76.0 — app-advertised RPCs and Android OS control** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) 🎯T111/🎯T112) — spyder now accepts *every* method name in an app's hello rather than only the engine catalogue, so `app_methods` discovers a session's surface (kind `engine` or `app`, with optional `example_params` and `doc`) and `app_call` invokes game-private commands — **no per-game MCP tools ever again**. Separately, compositor and UI FPS windows via `dumpsys gfxinfo`, TCP port-forward lifecycle, and minimal tap/swipe injection landed behind MCP and CLI so agents stop reaching for raw `adb`; `perf_fps` got its own 150 s deadline after the shared 60 s one silently timed out mid-measure for any window above 60 s.
- **slacker — a multi-workspace Slack MCP, created** ([marcelocantos/slacker](https://github.com/marcelocantos/slacker)) — named accounts in YAML, tokens in the OS keychain or mode-0600 files, every tool requiring an account label, and a CLI for account management. Apache-2.0 from the first commit.

### Significant Progress

- **Streaming topic segmentation with an explicit supersession lineage** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) 🎯T132) — a bounded-state watcher draws topic spans as a conversation runs, and a later batch pass may overturn them. That gives `topic_segments` two pointers between spans meaning opposite things: `parent_id` says "this fine span sits *inside* that coarse one", `superseded_by` says "that span later *overturned* this one". Conflating them would have let `AttachSegmentExpand` widen a search hit into a correction and present it as surrounding context — a wrong answer that reads as entirely reasonable — so `TestSupersessionIsNotHierarchy` pins the distinction. Superseded spans are **demoted, never hidden**: they sort below every live span but stay queryable, because the stream-versus-finalisation divergence *is* the freshness metric and deleting the loser would delete the measurement. Mutation-tested — removing the demotion lets a superseded LLM span outrank a live one.
- **FD-bounded tree watching after a vnode-exhaustion incident** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) 🎯T142, v0.82.0) — recursive `fsnotify` Walk+Add opens every file under kqueue on macOS, which exhausted vnodes on 2026-08-01. `internal/store/fswatch` replaces it with FSEvents roots on Darwin, capped directory watches on Linux and Windows, path filters and a hot-set safety poll; a `PollTracker` round-robins known ingest offsets so open/write/close writers that produce no tree event are still re-stated within a bounded budget. Watch telemetry (backend, roots, open FDs, poll counters) is exposed through `mnemo_status`, `mnemo_stats` and the health endpoint, with an FD oracle to keep it honest.
- **jevons v0.8.0 as a daily driver** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T59–🎯T79) — `jevons_mcp_reconnect` cycles a named MCP server (or all of them) mid-session, so tools dropped by the underlying CLI return without rotating the session or touching the TUI. Prefix-first attention threads (`aside:`, `capture:`, `park:`, `main:`, `pursue:`) let voice or typed input steer focus with no chrome at all. Mermaid fences render as SVG, gated to *sealed* content so a half-streamed diagram never flashes a parse error. Collapse is decided by rendered height ratio rather than character count, measured only once the bubble is in the DOM, so tables and rich markdown stop missing the gate.
- **The worker-reply delivery bug, in three parts** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T61/🎯T62/🎯T63) — "the worker did the work but never replied" turned out to be three independent faults stacked. The terminal-stop trigger was wrong; then `wireAgentEvents` was called only from the MCP spawn path, so agents auto-started at boot by `registry.StartAll` had no event sink at all; then `SendToOverseer` used the overseer's single-prompt ACP session, so a worker finishing mid-turn got `prompt already in flight`, and the reply was **logged and dropped**, leaving the overseer to scavenge the worker's transcript. Notifications are now queued rather than discarded on collision.
- **Per-session scoping for the whole dev plane** ([squz/ge](https://github.com/squz/ge) 🎯T174/🎯T175, v0.88.0/v0.89.0) — `ge::debug` state, the app channel, buttons, capture, sensors and metrics all moved off process globals onto a per-session `Scope`, with a process-globals audit to keep them there. Two game instances in one process can no longer cross-talk through the debug plane.

### Tough Challenges Overcome

- **A summariser that took its input as instructions** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo), [marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — described above; what makes it a genuine challenge rather than a configuration slip is the ordering. The obvious fix — restrict the summariser's tools — was **unwritable** until claudia's Task mode grew the capability, and the reason nobody noticed was that claudia's README promised the restriction and its Session mode delivered it, so the documentation was actively misleading. The fix moves the baseline to a shared constant applied in both modes.
- **Thread-safe text rasterisation by reading the contract rather than adding a lock** ([squz/ge](https://github.com/squz/ge) 🎯T176, v0.89.0) — the tempting fix is one big mutex around [FreeType](https://freetype.org/). The documented contract is narrower and much better: a single `FT_Library` is shared by every thread and needs a lock **only** around `FT_New_*_Face` / `FT_Done_Face`; `FT_Load_Glyph` and siblings are thread-safe without any lock provided a given `FT_Face` is used by one thread at a time. So ge creates a face per rasterise call and leaves the expensive part — glyph rendering — fully parallel. The insight that makes it cheap is that an `FT_Face` can never be the shared immutable artefact (it is a mutable scratchpad by design: the glyph slot is reused, size and hinter state live in it) — the immutable artefact is the **font bytes**, and `FT_New_Memory_Face` does not copy its buffer, so every face on any thread sits over one write-once cache entry and costs microseconds to create.
- **A Windows suite that hung for two unrelated reasons** ([marcelocantos/csp](https://github.com/marcelocantos/csp) 🎯T39) — the full-suite hang and the listen hang looked like one bug. They were not: the second was the missing `FD_ACCEPT` bit in the event-select mask, and reaching it required first making the validation harness reliable enough that a hang could be distinguished from slow output.
- **den's daemon install that did nothing, twice over** ([marcelocantos/den](https://github.com/marcelocantos/den) v0.13.0) — the macOS launchd path resolved its own binary through `/proc/self/exe`, a Linux-only interface, and emitted an argv (`daemon --run --den-home`) the CLI does not accept. Resolved via `_NSGetExecutablePath` with `DEN_HOME` in the environment and a proper `launchctl bootstrap`. The companion defect: `set_setting` inferred JSON type from the existing value, so a first-time `den set daemon.auto_upgrade true` stored the *string* `"true"`, which the reader's `is_boolean()` check skipped — the fix corrects the writer and teaches both readers to accept the legacy form so configs already broken on disk heal on next read.
- **A rename that had to be un-shipped** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) 🎯T51) — machine-scoped `T{node}.{seq}` ids shipped in v0.40.0 to make target numbers globally unique, then broke on the case that motivated them: two clones of the same repo on one machine share a node id, so the scheme collided exactly where it promised not to. A clone-path-scoped variant was tried and also rejected, and the whole thing was backed out to short sequential numbers within one week of shipping.

### Contributors

- Marcelo Cantos (AI co-authors — Claude Fable 5, Grok, and other Claude models — appear on `Co-authored-by` trailers throughout).

---

## Agent & Fleet Infrastructure

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Containment, Cost, and Segmentation (27 commits, v0.69.0→v0.82.0)

**The biggest effort of the week**, and mnemo's largest week of the series: fourteen releases, +24,210/−1,475, **216 new tests**. The summariser containment, the cost engine, streaming segmentation and FD-bounded watching are covered above; the remainder:

- **Bounding terminal automation, and correcting its failure message** — the second exposed path alongside the summariser, with a spend ceiling and an image-describer gate closing the last two summariser gaps.
- **Segmentation folded into summarisation** — one pass rather than two, plus the daemon defects that only surfaced while verifying it. A later commit reverted seal-pressure on measurement and split **segmentation quality** from **operating point**, because a metric that the thing being measured can influence is not a metric.
- **Span provenance and gated retirement** — end-of-session spans are salvaged rather than dropped, spans record where they came from, and retiring the structural method is gated on measurement rather than intent. Structural spans were then retired across existing history.
- **PKM vault profile, bridges, and persisted patterns** (🎯T64.7) — workaround patterns are persisted and rendered rather than re-derived, and the vault gained a profile for personal-knowledge-management use.
- **Resume a session by describing it** — reopening a conversation from the shell, session provenance repair, and unblinding the compactor's owed metric. A 🎯T130 target was filed for a cloud Windows CI job that flips pass/fail against its own timeout, rather than being retried until green.
- **Two honesty commits**: 🎯T54's prior attempt and the reason it was not landed are recorded in the repo, and an automation-liveness exploration note was landed as archived history instead of being deleted.

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Daily-Driver Chat and Fleet Control (15 commits, v0.8.0)

- **An isolated owner-chat journey suite** (🎯T79): boots a throwaway `jevonsd` on a spare port with a temporary state directory so live journeys never touch the daily stream; `make test-journey` runs J1–J5 and is deliberately *not* part of `make test`.
- **Independent sessions per agent name** (🎯T86): claudia's name-keyed `EnsureAgent` removed a workdir-based session steal, and `agent_list`/`agent_start` use a session display string so concurrent UUIDv7 peers stop looking identical.
- **Owner bubbles only** (🎯T63): genuine owner turns carry a `[user]` marker so the wire layer can discriminate the owner's own words from the ACP echo; agent and system notifications fold into an activity strip instead of masquerading as chat. Relaying is the overseer's job.
- **117 file changes, +11,406/−271, 140 new tests.**

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Tool Restrictions and Fleet Identity (8 commits, v0.20.0)

- **The documented-but-absent restriction** (see Major Achievements) — the release that unblocked mnemo's containment work.
- **`AgentDef.Purpose`** for a unified fleet model (`work` | `aside` | `overseer`) and **`AgentDef.Parent`** lineage so kill authorisation can be checked against who spawned what.
- **ACP correctness**: `tool_call` raw input is preserved on `Event.Raw`, and shell tools select the offered permission `optionId` rather than guessing.
- **A Grok tmux Session driver spiked** with 8/8 gates passing and filed as 🎯T10 — then deliberately **set aside as won't-fix** rather than left as an open promise.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Attestation and Store Integrity (5 commits, v0.40.0→v0.43.0)

Covered above. Also: an "origin report" documenting the project's history, YAML store design and usage reflections, and a longform graph-engineering evaluation captured against bullseye and the oracle-first doctrine for deliberate deferred re-read rather than immediate reaction. **19 new tests**; +2,742/−475.

### [marcelocantos/slacker](https://github.com/marcelocantos/slacker) — Multi-Workspace Slack MCP (1 commit, initial)

A new Go MCP server over stdio. The distinguishing constraint is in the name: Slack's own MCP offering is single-session, and the whole reason this exists is to hold several workspaces at once. Named accounts live in YAML, tokens live in the OS keychain (or mode-0600 files), and **every tool requires an account label** so there is no ambient "current workspace" to get wrong. +1,653/−0, **5 tests**, Apache-2.0 from the first commit.

---

## Libraries & Systems

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Stack Analysis, Windows, and an Audit Campaign (13 commits, v0.27.0→v0.29.0)

The stack analyser, the `FD_ACCEPT` fix and the 🎯T46–🎯T50 campaign are above. Additionally:

- **Walker soundness hardening and ground-truth oracles** (🎯T52.1/.2/.6): the analyser is checked against measured true-peaks rather than against itself, and an unwind spike explored what a future exception-aware walk would cost.
- **Stack analysis off imp stacks** (🎯T52.4): analysis moved to an async worker returning `Default`-on-miss, with `analyze_stack_depth_cached` as a safe lookup for threads that cannot afford recursion — analysing a deep call graph *on* a small microthread stack is exactly the recursion you cannot afford.
- **Concrete spawn analysis, data-path pre-scan, and a fan-in helper** closed the week.
- **243 file changes** (half of them the `dist/` amalgamation, excluded from ☲), **+6,414/−3,031**, **22 new tests**, and the ARM64 stack analyser documented as shipped.

### [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) — Scope-Aware Rename (2 commits, v0.18.0)

Covered above. **40 new tests**; +5,697/−55 across 40 files.

### [marcelocantos/den](https://github.com/marcelocantos/den) — Daemon Install (1 commit, v0.13.0)

Covered in Tough Challenges. Multi-provider support (pip/npm/cargo/go) was also promoted from future tense to present in the docs, and `fmt` attributed in NOTICES. +251/−176.

---

## Tooling & Workflow

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — App-Advertised RPCs (4 commits, v0.74.0→v0.76.0)

Covered above. Also: dual-platform OS-control wording in CLI help, and OS-control results always printed as JSON — a small fix with an outsized effect on agents that parse them. **29 new tests**; +2,505/−47.

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — Go Port (4 commits, v0.11.0)

Phase 1 of 🎯T14 with the bash ingest pipeline deliberately untouched. Also this week: notification events now report to [blurter](https://github.com/marcelocantos/blurter) and ytt's own notifier was deleted, and the bundled ingest scripts were made to run on a stock macOS `/bin/bash` 3.2. **33 new tests** (bats), +1,265/−1,216 — a port that is close to net-zero on lines while removing a language and a dependency.

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — Media-Orthogonal Convert (3 commits, v0.6.0→v0.8.0)

Covered above, plus a Markdown viewer, clipboard *content* input, and cache-health reporting. The Vellum Viewer double-click fix is an Apple Events applet subtlety: a double-clicked document arrives as an `odoc` event, not as `argv`, so the viewer had to become an applet that answers it. **18 new tests**; +3,240/−707.

---

## Game Engine

### [squz/ge](https://github.com/squz/ge) — Gesture Hints and Tile Pyramids (21 commits, v0.84.0→v0.91.0)

Eight tags. The hint service, the `.getp` tile pyramid, per-session scoping and the FreeType contract are covered above. The remainder:

- **Engine-owned perf HUD strip with game-supplied segments** (🎯T173, v0.87.0) — the HUD belongs to the engine so every title gets the same one; games contribute segments rather than drawing their own.
- **`cmdstream` image recipes off by default and bounded when enabled** (🎯T169) — an image-producing recipe is an unbounded egress and memory surface, so it fails closed.
- **App methods advertised with `example_params` and `doc` in the hello handshake**, which is the engine half of spyder's `app_methods`/`app_call`.
- **STABILITY snapshots on every release** — ge's pre-1.0 interaction-surface catalogue (every public API, CLI surface, wire item and file format tagged Stable / Needs review / Fluid) is re-cut per tag as the diffable baseline the release process audits against.
- **Nine new golden fixtures** for hint clips (tap-hover, tap-press, swipe-mid, drag-mid, long-press, double-tap, pinch-zoom, pinch-rotate, ring-tap). **87 new tests**; +7,878/−723 authored, with 275 further file changes of generated `headers/` and LFS `prebuilt/` excluded from ☲.

### [squz/multimaze2](https://github.com/squz/multimaze2) · [squz/yourworld2](https://github.com/squz/yourworld2) · [squz/esfera2](https://github.com/squz/esfera2)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-08-02](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-02.md).*

---

## Commercial

### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) · minicadesmobile/Minicadeskit · minicadesmobile/dragster-mayhem

*Detailed narrative in the private sibling: [progress-reports-private — week ending 2026-08-02](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-02.md).* One item is general enough to keep here: this repository redirects `core.hooksPath` to `scripts/hooks`, which makes git ignore `.git/hooks` **entirely** — only `pre-push` had been committed there, so a fresh clone got the test gate but none of git-lfs's `post-checkout`/`post-merge`/`post-commit` hooks, and LFS pointers would never have been smudged into real files. The three vanilla LFS hooks are now tracked alongside the gate, which already chains `git lfs pre-push`, so `git lfs install` is never required and can no longer clobber the gate.

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **marcelocantos/rustuml** — 0 landed, **1,083 commits in-flight** (+220k/−36k): by far the largest unmerged tranche in the fleet.
- **marcelocantos/jevons** — 24 in-flight; **marcelocantos/writ** — 17; **marcelocantos/csp** — 15; **marcelocantos/mnemo** — 6; **marcelocantos/ytt** — 5; **marcelocantos/skills** — 3.
- **Health-Management-Systems/hms** — 145 in-flight; detail in [private week 2026-08-02](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-02.md).

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-07-27…08-02. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **19** |
| Total landed commits | 115 |
| Total lines added (landed, filtered) | +82,251‡ |
| Total lines removed (landed, filtered) | −8,737‡ |
| Net new lines (landed, filtered) | +73,514‡ |
| File changes | 1,102 |
| New files created | 328 |
| Bulk paths excluded from ☲ | +8,171 / −2,793 (ge `headers/`+`prebuilt/`, csp `dist/`, lockfiles, `bullseye.yaml`) |
| Releases published | **40 across 11 repos** (mnemo ×14, ge ×8, bullseye ×4, csp ×3, spyder ×3, vellum ×3, claudia, den, jevons, sawmill, ytt) |
| Languages | Go, C++, Rust, C, Objective-C++, Python, JavaScript, GLSL, Bash, Starlark, PowerShell, C#, Swift, Kotlin, YAML, Markdown |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. No new globs were required this week.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 27 | 256 | +24,210 | −1,475 | +22,735 |
| [squz/ge](https://github.com/squz/ge) | 21 | 119 | +7,878 | −723 | +7,155\* |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 15 | 117 | +11,406 | −271 | +11,135 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 13 | 243 | +6,414 | −3,031 | +3,383\* |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 8 | 25 | +1,304 | −63 | +1,241 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 5 | 46 | +2,742 | −475 | +2,267 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 4 | 37 | +2,505 | −47 | +2,458 |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 4 | 30 | +1,265 | −1,216 | +49 |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 3 | 83 | +9,718 | −300 | +9,418 |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 3 | 33 | +3,240 | −707 | +2,533 |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 2 | 40 | +5,697 | −55 | +5,642 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 2 | 37 | +3,449 | −192 | +3,257 |
| [squz/esfera2](https://github.com/squz/esfera2) | 2 | 7 | +502 | −3 | +499 |
| [marcelocantos/slacker](https://github.com/marcelocantos/slacker) | 1 | 15 | +1,653 | −0 | +1,653 |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 1 | 11 | +251 | −176 | +75 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 1 | 3 | +17 | −3 | +14 |
| [marcelocantos/blurter](https://github.com/marcelocantos/blurter) | 1 | 0 | +0 | −0 | 0† |
| minicadesmobile/Minicadeskit | 1 | 0 | +0 | −0 | 0† |
| [minicadesmobile/dragster-mayhem](https://github.com/minicadesmobile/dragster-mayhem) | 1 | 0 | +0 | −0 | 0† |

\* *ge's figures exclude 275 file changes of generated `headers/` and LFS `prebuilt/` churn; csp's exclude the auto-generated `dist/` amalgamation, which mirrors every `src/` edit.*
† *target-ledger (`bullseye.yaml`) updates only — machine-written, excluded from ☲.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 216 | segmentation supersession, cost dedup/TTL/long-context, FSEvents FD oracle, summariser containment |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 140 | attention-thread model, notify queue, MCP reconnect (fails closed on no-op), collapse-by-height |
| [squz/ge](https://github.com/squz/ge) | 87 | hint clip timing + tags, SDF hand layout without a GPU, synthetic input driver, tile-pack index maths, per-session scoping |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 40 | scope-aware rename bindings, behavioural equivalence, 18-language matrix smoke |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 33 | Go transcript layer against goldens captured from the 0.11.0 binary pre-port |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 29 | `app_methods`/`app_call` dispatch, gfxinfo parsing, deadline class bound |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 22 | stack-analysis ground truth, walker soundness, six audit regressions |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 19 | attestation rejection, content-hash repair, postpone gating, Mermaid subgraph export |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 18 | media-orthogonal router, clipboard file references, cache health |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 14 | Task-mode disallowed-tools baseline, name-keyed `EnsureAgent`, ACP raw input |
| [marcelocantos/slacker](https://github.com/marcelocantos/slacker) | 5 | account resolution and keychain round-trip — whole repo is new |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 2 | tile-globe parity contract |
| **Total** | **~680** | landed only; counted as net growth in test declarations across the window |

### Daily Activity

![Daily active repositories](daily-activity-2026-08-02.svg)

*(Active repositories per day: Mon 07-27 10, Tue 07-28 6, Wed 07-29 5, Thu 07-30 2, Fri 07-31 5, Sat 08-01 6, Sun 08-02 7. The week opens at its peak rather than closing there — Monday alone carried ge's tile-pyramid landing, the csp Windows fix and the ytt Go port — and Thursday is the one genuinely narrow day.)*

---

## Ideas & Innovations

### A Coarser Pack Is a Prefix of a Finer One ([squz/ge](https://github.com/squz/ge))
The usual way to ship a texture pyramid at several quality levels is to cook several packs, or to cook one and let low-end devices skip records scattered through it. `.getp` does neither. Payload blobs are laid out coarse level → fine, planes interleaved per level, and the header records truncation offsets — so **a smaller pack is not a different file, it is the first N bytes of the big one**. A device on the capped tier stops reading; a build for a constrained target truncates. The same property makes progressive delivery free: whatever prefix has arrived is a valid, complete, coarser globe. The cube-face convention is chosen with equal care — face order and orientation match sokol's cubemap slices exactly, so a direction that samples texel (u,v) of slice F samples the same ground point in tile space, which removes an entire class of "why is Australia upside down" from every consumer.

### The Same Timeline Draws the Hand and Presses the Button ([squz/ge](https://github.com/squz/ge))
Tutorial hands and automated demos are normally two systems: art that animates a finger, and a script that injects taps, with a human keeping them in sync. ge collapses them. `hint::Player` is a pure timeline of pointer states and tagged events; the SDF hand is *one* consumer and the synthetic-input driver is *another*, both reading the same interpolated state in the same frame. **Drift between what the user sees and what the app receives becomes structurally impossible** — not tested-for, impossible. The driver is nevertheless strictly opt-in per player, because presentation and injection are genuinely different intents: a hint that *suggests* a gesture must not perform it, and driving mutates real game state that is not cheaply revertible. The reserved touch id and `isSyntheticFinger()` let a game accept the hand while filtering its consequences.

### The Rate Card Is Upstream of the Tool ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo))
Faced with an established tool that computes token spend, the reflex is to shell out to it. The analysis instead asked what the tool's *value* actually is, and found that everything beyond pricing is a `GROUP BY` over data mnemo already ingests — while the one genuinely external input, the rate card, is a public JSON file sitting *upstream* of the tool itself. So mnemo fetches the card and does its own arithmetic, keeping the single-Go-binary property and an O(new bytes) ingest shape instead of inheriting an O(entire corpus) one. The tool is retained as a **validation oracle** rather than a dependency, which is the right end state: an independent implementation you can diff against is worth more than a subprocess you must trust.

### Two Pointers That Mean Opposite Things ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo))
When a streaming segmenter and a hindsight segmenter both draw spans over the same conversation, the schema needs to express both *containment* and *correction*. It would be very easy to reuse one edge for both. The commit's argument for why that must not happen is the sharpest kind: context expansion walks `parent_id` to widen a search hit, so conflating the edges would silently present a **correction as though it were the surrounding conversation** — a wrong answer that looks entirely reasonable, which is the worst class. The complementary decision is to demote superseded spans rather than delete them, because the divergence between the streaming guess and the final answer *is* the freshness metric, and deleting the loser deletes the measurement.

### Reading the Threading Contract Instead of Adding a Lock ([squz/ge](https://github.com/squz/ge))
The default response to "the rasteriser is not thread-safe" is a mutex around the rasteriser, which serialises the expensive part and buys nothing. FreeType's documented contract is much more generous — one library shared everywhere, a lock needed **only** around face creation and destruction, glyph loading thread-safe as long as a face is used by one thread at a time. Once you accept that a face is a mutable scratchpad rather than a cacheable artefact, the design falls out: create a face per call, share only the immutable font bytes (which `FT_New_Memory_Face` deliberately does not copy), and leave glyph rendering fully parallel. **The performance came from reading the documentation, not from writing code.**

### A Port That Removes a Dependency ([marcelocantos/ytt](https://github.com/marcelocantos/ytt))
Rewrites usually add surface. ytt's Go port removed some: `yt-dlp` was *already* required for channel discovery, so the Python transcript library was a second YouTube-facing dependency with overlapping capability. Deliberately declining to adopt a Go transcript package is the interesting call — YouTube churns its internal caption APIs constantly, and a small Go library would rot while leaving ownership of the breakage that is hardest to detect. The verification method matches: goldens were captured from the **installed binary before the port** and replayed against the new one, so the port is checked against the thing users actually had, not against a specification of it.

### Restrictions That Only Exist in One Mode ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
The most alarming detail of the summariser incident is not that a model followed an instruction in its input — that is the expected failure. It is that the library documented five always-disallowed tools, implemented them in Session mode, and passed **no** `--disallowedTools` at all in Task mode, with no field on `TaskConfig` to supply one. Every reader of the README believed they were protected. The lesson generalises past this bug: a guarantee stated in prose and implemented on one of two code paths is worse than no guarantee, because it suppresses the check that would have caught it. The fix moves the baseline to a shared constant so the two modes cannot diverge again.

### Advisory Ids Are Better Than Wrong Ids ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye))
Machine-scoped target ids shipped and were withdrawn inside a week, which is the healthy outcome. The scheme keyed uniqueness on node identity; two clones of one repo on one machine share it, so the collision arrived precisely in the scenario the change existed to fix. A clone-path variant was attempted and also rejected — at which point the honest move is to stop, not to keep patching the discriminator. What survived the round trip is the part that was independently good: `achieve` now demands a written attestation, so the ledger records *how* a target was met rather than only that someone said so.

---

## Effort Estimate: Traditional vs. AI-Assisted

A containment-and-consolidation week. Two real incidents drove the largest work items — a runaway summariser and a vnode exhaustion — and the response in both cases went past the fix into the class. Shipping density was the highest of the series so far: forty releases across eleven repositories.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| mnemo cost engine + segmentation + containment + FSEvents | 6-9 | Reconciling a token figure with an invoice requires discovering deduplication, cache-write TTL tiers and long-context repricing from data alone; streaming segmentation needs a schema that distinguishes containment from correction; FSEvents versus kqueue versus inotify is three different FD models with three different failure modes. |
| ge gesture-hint service + tile pyramid + per-session scoping | 5-8 | A keyframed timeline with tagged events driving both an SDF fragment-shader hand and synthetic SDL input is animation, signed-distance rendering and event-loop surgery at once; the tile pyramid is gnomonic cube-sphere maths plus a binary container designed for prefix truncation plus device-capability probing. |
| csp ARM64 stack analyser + Windows + audit campaign | 3-5 | Walking AArch64 machine code to bound SP displacement — following calls, resolving indirect branches through live data, and being honest about inexactness — is a small static analyser; the Windows hang needed a trustworthy harness before the one-bit bug was even visible. |
| jevons daily-driver chat + fleet control plane | 2-4 | Three stacked causes behind one symptom, spanning ACP session semantics, event-sink wiring at boot, and a UI collapse heuristic that has to measure rendered height after layout. |
| ytt Go port with differential verification | 1.5-2.5 | Porting a working tool without regressions, against goldens captured from the shipped binary, while removing a language and a dependency and leaving the bash pipeline intact. |
| sawmill scope-aware rename + equivalence oracle | 1.5-2.5 | Lexical binding models for two languages with different scoping rules, plus a behavioural-equivalence oracle and five new language adapters. |
| claudia tool restrictions + fleet identity | 1-2 | The fix is small; finding it required tracing a 4.3-billion-token incident back through two repositories to a documented-but-unimplemented promise. |
| bullseye attestation + store hash + id experiment | 1-2 | Content hashing with repair, frontier gating, and an id scheme that had to be designed, shipped, falsified and withdrawn. |
| spyder app-advertised RPCs + Android OS control | 1-2 | A pass-through RPC surface that must not become per-game tooling, plus `dumpsys` parsing and port-forward lifecycle with honest deadlines. |
| vellum media-orthogonal convert | 1-1.5 | Collapsing four tools into one router without losing the sugar, plus an Apple Events applet for `odoc`. |
| slacker initial + den daemon install | 1-1.5 | Keychain-backed multi-account credential handling from scratch; two silent-failure bugs in one install path. |
| Game and client downstream (private) | 2-3 | Detail in the private companion. |

### The Diversity Tax

This week spans Go (mnemo, jevons, claudia, spyder, sawmill, slacker, ytt, vellum), C++ (ge, csp, den), Rust (bullseye), C# and Unity (client work), GLSL (the SDF hand, tile sampling), Python and Bash (cook tooling, ingest), Starlark (spyder recipes), PowerShell (Windows CI), and platform surfaces spanning FSEvents, kqueue, launchd, FreeType, Winsock event-select, AArch64 instruction encoding, ASTC, Apple Events and the macOS keychain. No single engineer holds instruction-level stack analysis, texture-compression container design, LLM billing archaeology and Slack OAuth at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| mnemo / claudia containment | 4-7 | Noticing the spend spike at all, deciding the summariser must not be able to act rather than merely be told not to, and accepting the ordering constraint that a library fix had to land first. |
| ge / games | 4-6 | Judging the hand's articulation on a real device — the wrist pivot went through two corrections by eye — plus release judgement across eight tags. |
| csp / sawmill / bullseye | 3-5 | Interpreting the stack-analysis margin evidence, blessing the audit campaign's scope, and calling time on the machine-scoped id scheme. |
| jevons / tooling | 3-6 | Living in the chat UI daily, which is how the dropped worker replies and the collapse-heuristic gaps were found in the first place. |

### What If It Were One Person?

The expert band sums to roughly 26-43 person-days, but a single generalist would not achieve that rate. They would ramp on AArch64 instruction semantics, FreeType's threading contract, FSEvents versus kqueue FD accounting, gnomonic cube-sphere projection and LLM billing structure — five unfamiliar domains — and then pay a heavy context-switch tax across nineteen repositories and forty releases in seven days. Against that, the specialist-team figure is lower precisely because ramp-up disappears when the right person already knows the domain.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~22-36 person-days (~1.1-1.8 months)** |
| Specialist team (traditional) | **~14-24 person-days (~0.7-1.2 person-months)** |
| Actual human effort this week | **~14-24 hours (~2-3.4 person-days)** |
| **Multiplier vs. generalist** | **~35-60x** |
| **Multiplier vs. specialist team** | **~22-38x** |

The multiplier runs highest on the incident work — the summariser containment and the FD exhaustion — where the expensive human step is *noticing*, and a system that indexes its own transcripts and bills notices faster than a person reading green logs. It runs lowest on the ge release train and the audit campaign, both mechanical once the contract is written. Human contribution concentrated where judgement cannot be delegated: how a cartoon hand should pivot at the wrist, whether an id scheme is worth another attempt, and the decision that a tool which reads untrusted text must not be able to act on it at all.

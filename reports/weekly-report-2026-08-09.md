# Weekly Progress Report — 2026-08-03…09

## Executive Summary

**Nineteen repositories** landed **297 commits** — by a wide margin the largest week of the series, and the first in which the agent fleet's own infrastructure did most of the building. **[marcelocantos/orthograph](https://github.com/marcelocantos/orthograph)** went from an empty repository to a `brew install`-able product in six days: a Pencil-first iPad sketch surface whose document lives on the Mac, is readable and writable by agents as a vector scene graph over MCP, and reaches the iPad over [pigeon](https://github.com/marcelocantos/pigeon)'s encrypted pairing — 86 commits, a SQLite op-log document store, 60-odd MCP tools, and a working iPad app. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** landed 80 commits and five releases (v0.9.0→v0.13.0) largely by supervising itself, and the substance is unusually sharp: a **fleet spend oracle** that decomposes cost as *turns × calls-per-turn × context-per-call* from the providers' own billing frames, a **hard context ceiling** that compacts agents instead of letting quadratic conversation growth run, **wake coalescing** after measurement showed over half of the most expensive agent's prompts were machine noise, a compare-and-swap **write guard** after concurrent workers silently reverted each other's edits three times in one mission, and a `GIT_INDEX_FILE`-based pre-commit gate that makes a worker's commit contain only its own paths *by construction*. **[marcelocantos/slacker](https://github.com/marcelocantos/slacker)** replaced paste-a-token with browser OAuth over a **TLS loopback callback** — Slack, unlike most providers, grants no plain-HTTP exemption for localhost — and ties requested scopes to the API methods actually called by reading the source at test time. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** cut its MCP tool surface from **70 tools to 18** behind one search. **[marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge)** v0.9.0 ended a self-feeding reload loop running at ~3 reloads/second against an unchanged binary. Eighteen releases across seven repositories. Commercial project detail: [private week 2026-08-09](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-09.md).

**297 commits** | **+237,246 net lines** | **~46-76 person-days traditional equivalent** | **~60-95x multiplier**

> Honesty note: three new `data/line-excludes.yaml` entries this run. `marcelocantos/orthograph: ios/build-spm-check/**` removes a briefly-tracked Swift Package Manager build tree — **4,996 of the repo's 5,441 raw file changes** were machine-written module caches. `marcelocantos/progress-reports` and `progress-reports-private`: `reports/**` and `docs/**`, because the public/private split rewrote the public repo's history and a single commit re-adds the whole back-catalogue (+59k), which would double-count prose already reported in the weeks it describes. Total excluded bulk: **+72,004/−4,850**. jevons's +160,946 was checked and is genuine authored source — 632 distinct files, 502 of them new, spread across Go packages and vanilla-JS modules with no vendored blob. Commercial project detail: [private week 2026-08-09](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-09.md).

### Major Achievements & Innovations

- **orthograph — a shared drawing surface for a human and their agents, nothing to installable in six days** ([marcelocantos/orthograph](https://github.com/marcelocantos/orthograph)) — the stated problem is precise: agents can read code, logs and screenshots, but cannot *share a drawing surface* with a human in real time, so technical discussion collapses into ASCII, PlantUML links, or "describe what you mean". Orthograph is a Mac daemon (Homebrew service) owning a vector document in SQLite with an append-only op log, an HTTP MCP server giving agents a full observation and mutation surface over stable ULID-keyed objects, a deterministic render hash so an agent can tell whether the canvas changed, content-addressed media with four export formats, and an iPad SwiftUI app taking per-sample Apple Pencil force and tilt with Pencil-only ink and three-finger viewport control. Pairing runs the pigeon QR ceremony, proven **through the shipped binary** rather than in a test harness. 86 commits, +43,945/−3,269, **399 tests**.
- **A spend oracle measured along the axes the levers act on** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T392.6) — `tokens = turns × calls-per-turn × context-per-call`, because *a sum of tokens cannot tell you which lever to pull*. `cost.Event` now carries `ModelCalls` and `StopReason` from both providers, so context-per-call — the quantity a ceiling actually binds — is derived from the provider's own billing frames rather than estimated (Grok reports calls per turn; Claude bills one call per assistant frame). Spend is split coordinator/implementer with a cancelled-turn share, and **unattributed spend is its own bucket that stays in the denominator**, because a share that quietly drops what it cannot classify overstates itself. The oracle reproduces a frozen baseline, which is what makes the subsequent optimisations measurable rather than plausible.
- **A hard context ceiling, because conversation cost is quadratic** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T392.1) — every model call resends the whole conversation, so a session's cost grows with the square of its length and fleet spend grows linearly with how long agents run before compacting. In the frozen baseline one agent grew 2.2k of context per turn from 42k to 399k, and *the only thing bounding the overseer was accidental daemon restarts*, roughly one every five hours. `internal/ctxcap` is a pure policy over an `Observation` carrying the tokens the last call actually billed. Two refusals make it safe: **unknown never compacts** — a missing measurement is not evidence of a small context, and acting on one would rotate agents at random — and a ceiling below `MinCeiling` is raised rather than honoured, since constant rotation costs more in handovers than it saves.
- **Coalescing machine wakes into one digest per recipient** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T392.2) — waking a coordinator carrying 235k of context to deliver one line of "a worker went idle" buys roughly a million input tokens. Measurement showed **27% of that agent's prompts were idle nudges, 13% daemon-restart notices and 12% bare system reminders — over half of what woke the fleet's most expensive agent was neither the owner nor a worker result.** Those events are additive and order-free, so batching divides the cost by the batch size at no loss of information. A single pending event renders as itself, because digest ceremony around one line would make the common case more expensive than what it replaced.
- **Compare-and-swap at the write boundary** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T376) — several fleet workers share one clone, and a full-file write derived from a read that predates another worker's edit silently reverts it. That happened **three times while landing a single target, all on a ~10.6k-line file, costing about half the mission's wall-clock in re-applying correct edits**. `internal/treeguard` records the whole-file hash each session observed on every read or write of a guarded path and refuses a write whose base no longer matches disk, **naming the specific lines it would have dropped**. Silent loss becomes a loud, recoverable refusal. It is wired for every worker through tracked `PreToolUse`/`PostToolUse` hooks — the settings file is now committed because it is fleet policy, not local preference — and the oracle is two-sided so neither failure mode can hide.
- **A worker's commit contains only its own paths, by construction** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T377) — one clone has one index, so `git add` is a write to shared mutable state and a bare `git commit` turns whatever every concurrent worker has staged into a single tree under one worker's message. That is how one refactor commit came to contain the whole of an unrelated target, such that reverting the first would have silently reverted the second. The detection needs no ownership ledger: **git already tells a pre-commit hook, in `GIT_INDEX_FILE`, which index the commit is being built from**, and that one string separates a commit whose contents were chosen from one that merely inherited whatever was lying around.
- **Reaping is the irreversible branch, so it stops being the default under ambiguity** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T395) — the fleet's auto-reap fired whenever a completion word appeared anywhere in a terminal report. An agent briefed to establish a mechanism and report *before* changing anything opened with "Diagnosis complete", laid out four rows of evidence, and handed a decision to the overseer; the word "complete" reaped it, the reply bounced off "agent is not running", and the diagnosis was stranded. Three specimens landed in one afternoon, and two of the three losses were replies *to* the agent — a reaped agent is not merely gone, it is an unanswerable address, and the caller only finds out afterwards. The fix vetoes the reap for a report that asks for a decision, states it has not acted, ends on a question, or arrives visibly cut; and it matches the completion claim on **word boundaries**, because a substring test made "incomplete" a claim of "complete", "unfinished" a claim of "finished" and "abandoned" a claim of "done" — three words asserting the opposite of completion, read as completion.
- **slacker — browser OAuth with a TLS loopback callback** ([marcelocantos/slacker](https://github.com/marcelocantos/slacker) 🎯T2/🎯T3/🎯T4) — the interactive token prompt, `--token` and `--token-file` are gone; tokens are acquired only through Slack's consent screen and land in the keychain, so **nothing secret is ever typed, pasted, or written to config**. Three findings shaped it. Slack's docs contradict themselves on scheme, and the primary source resolves against loopback HTTP: the *host* `localhost` is fine, the *scheme* must be TLS — so the callback serves a persisted self-signed certificate covering `localhost`, `127.0.0.1` and `::1`. Slack matches `redirect_uri` byte-for-byte, so an ephemeral port is impossible; a new `preflight` command checks everything verifiable without contacting Slack, and earned its keep on the first live run by finding port 8765 already held by an unrelated MCP server — a failure that would otherwise have surfaced *after* the one-shot human consent. And app credentials had lived under one fixed keychain key, so configuring a second workspace's app silently overwrote the first — fatal for the multi-workspace case that is the product's entire reason to exist.
- **mnemo's MCP tool surface: 70 → 18** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) 🎯T143, v0.83.0→v0.85.0) — sized to actual recorded usage in two passes (70 → 38 → 18), with one search now spanning the whole index rather than a tool per corpus. `mnemo_self` was removed rather than reimplemented, on evidence: its nonce round-trip recorded **2 rows in four months against 11 tool calls**, and the sibling mechanism was no healthier at 374 daemon-connection rows against exactly one connection-session row, none in the last 30 days — so neither path could reliably answer "which session am I", which is why it could not simply be rebuilt on the other. The table stays under the append-only schema policy, written and read by nothing, and STABILITY.md says so.
- **mcpbridge v0.9.0 — a reload loop that fed itself** ([marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) 🎯T20) — the binary watcher treated fsnotify's `Chmod` as "binary changed", but on macOS kqueue reports `NOTE_ATTRIB` — surfaced as `Chmod` — when a binary is merely *executed*. A reload re-execs the binary in every wrapper, each exec fires `Chmod`, and the next reload lands one coalesce window later. Observed in the field at **~3 reloads/second indefinitely against a binary untouched for a day: 51 backends churning, a 5.1 GB daemon log, and every in-flight tool call longer than the 300 ms window losing its response.** Two independent fixes, either sufficient: `Chmod` leaves the trigger mask, and **a reload now requires evidence** — each watched path carries a size+mtime signature captured when tracked, and an event that does not move it is dropped, so the daemon can no longer claim "binary changed" about a file it never compared.
- **vellum v0.9.0→v0.13.0 — an e2e corpus that cannot verify its own producer** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum)) — import fixtures now come from implementations with **no pandoc lineage**, with hand-authored ground truth, because round-tripping through pandoc would verify its self-consistency and pass even if both directions were symmetrically wrong. `TestCorpus_ProvenanceIsUntainted` fails if a manifest ever names pandoc, WeasyPrint, Prince or vellum as producer. It found two real defects on its first run: legacy `.doc` (and any unrecognised extension) was read as Markdown because `formatFromExt` returns empty and ingest defaults to markdown, so 19 KB of OLE2 binary came back as *content* with a nil error; and pandoc 3.10.1's RTF reader hoists an ordered list above the first heading. Concurrent Mermaid rendering, a full media matrix and a locally-runnable gate shipped alongside.
- **claudia — a third provider and a durable Grok** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) 🎯T11/🎯T12) — `ProviderBedrock` adds an AWS `ConverseStream` Task path with a hermetically injectable streamer and an env/profile/default config chain; `ProviderClaude` gained `RequireResume` fail-closed semantics so a session is never silently replaced when its JSONL transcript is missing, plus a documented oracle map and hermetic coverage across start/send/stream/tool-use/cancel/stop/resume. Separately, detached `grok agent serve` with ACP over WebSocket lets agents outlive the consumer process, with `ConnectURL`/`ConnectPID` persisted and reattachment via `session/load` while the PID is alive.
- **sqlpipe v0.31.0 — prediction through CGo and into Swift** ([marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe)) — a C API and Go bindings for `begin`/`commit`/`end`/`rollback_prediction` and `queue_while_predicting`, with a Swift `TruthReplica` over a synchronous `CSqlpipe`. This is the substrate under orthograph's dual-pipe design: the pad predicts locally while the daemon owns truth.

### Significant Progress

- **Standing staff cycles inside the daemon** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T356/🎯T357/🎯T359) — an **ambient research cycle** folds findings into durable versioned notes rather than one-shot chat dumps, with periodic context refresh (git history by scope, sibling repos, the convergence frontier, the event-log tail, recent sessions) and an optional feed trigger; a changed claim *supersedes* its predecessor explicitly, and an unchanged observation refreshes provenance without appending a revision, so a quiet context produces a quiet diff. A **periodic full-scan audit** covers code, skills and prompts in one pass — "a partial habit is how prompts and skills end up never audited at all" — with residue keyed on scope plus normalised path and title, *deliberately not the line number*, so a finding that drifts as code moves updates its entry instead of minting a new one. **Capacity-aware admission** (`internal/capacity`) then gives all of them one holistic view: owner turns and open build missions are never gated, control-plane repair is the load-bearing background class, and a pressure ladder degrades from elevated to critical rather than running everything until the cost clamp fires.
- **Owner interaction as a convergence plane** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T355) — a live daemon is not a usable chat. Existing machinery kept the overseer process alive and fleet missions converging, but nothing observed whether *talking to Jevons actually works*. `internal/converge/owner.go` is a pure, level-triggered model with three predicates: `send_landed` (the owner turn is durable in the chatlog **and** acked out of the notify queue into the overseer's session), `chrome_truthful` (published chrome matches server truth), and `reply_or_residual` (a sealed reply, or a **named** residual, within a documented bound that governs silence rather than turn duration).
- **Serialising daemon restarts under a real lock** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T392.5) — five restart runs fired in 17 minutes, the last two 59 seconds apart; the second killed the first mid-flight and the daily daemon was left down with nothing to bring it back. Every in-flight agent turn was cancelled, and **a cancelled turn bills a full context for work that is thrown away — 6.6% of the baseline, 59.7M tokens, went exactly this way.** The script already had a mutex, and the mutex was the bug: between `mkdir` succeeding and the holder writing its pid file, a second caller reads an empty pid, concludes the holder is stale, removes the lock and proceeds. Stale detection could not simply be deleted, because a crashed holder would otherwise wedge the fleet forever.
- **Cross-site rejection by construction, and other chat-plane hardening** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T385/🎯T382/🎯T384/🎯T363) — every state-changing endpoint rejects cross-site requests structurally rather than per-handler; an owner turn paints exactly once under every provider; owner turns persist in the same shape as agent turns; and scrolling up preserves the viewport when rows *above* the anchor resize, which is the hard direction of that problem.
- **orthograph's dual-pipe intent/truth model** ([marcelocantos/orthograph](https://github.com/marcelocantos/orthograph)) — the daemon owns truth and the pad owns intent, with sqlpipe's `Replica` prediction API supplying tentative ink; the earlier live-stroke dual-render layer was **deleted** once prediction could carry it, rather than kept as a fallback. Documents rebuild from snapshot plus ops on load, with an atomic scene+op transaction (and `set_meta` deliberately non-undoable) after an op-log durability gap was found.
- **spyder v0.77.0/v0.78.0 — agent UX and mobile spawn without a registry** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) 🎯T117) — `app_spawn` resolves a target through an explicit ordering (factory session id, device+bundle whose live session is a factory, device+bundle direct, unique-live fallback), because *there is no mobile games registry — a mobile game **is** an installed bundle on a device spyder already knows*. A live non-factory session returns `already_running=true` rather than double-launching, and an uninstalled bundle fails closed pointing at `deploy_app`. `ensure_session`, session addressing, structured results and topical help landed alongside, plus a `SPYDER_ADDR` override in the brew service plist so the managed daemon can serve the LAN.

### Tough Challenges Overcome

- **A watcher that reloaded because it had just reloaded** ([marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge)) — described above. What makes it hard is that every individual component behaved correctly: kqueue reports attribute changes on exec as documented, fsnotify surfaces `NOTE_ATTRIB` as `Chmod` as documented, and the watcher reloads on change as designed. The loop only exists in composition, and it is invisible from any single layer.
- **Two workers, one index, one silent revert** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T376/🎯T377) — a shared clone turns both the working tree and the git index into unsynchronised mutable state. The two fixes are worth contrasting: the tree problem needed *new* machinery (a hash recorded at read time, compared at write time), while the index problem needed only an existing signal nobody was reading — `GIT_INDEX_FILE` already distinguishes `git commit` from `git commit -- <paths>`, so the gate is a string comparison in a pre-commit hook.
- **A lock whose stale-detection window was the race** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T392.5) — the tempting reading is "the script forgot to lock". It locked. The bug lives in the gap between acquiring the lock and becoming identifiable as its holder, and the stale-detection that opens that gap is itself necessary. Fixing it required a lock primitive where acquisition and identification are the same event.
- **A substring test that inverted three words** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T395) — "incomplete" containing "complete" is the kind of bug that reads as trivial in hindsight and is nearly invisible in review, because the *shape* of the code is right. The deeper correction is the bias: the destructive branch was the default under ambiguity while the cheap branch (a lingering agent) was not.
- **Slack's own documentation disagreeing with itself** ([marcelocantos/slacker](https://github.com/marcelocantos/slacker)) — the design had flagged the redirect scheme as the assumption most likely to force a redesign, and it was: unlike most OAuth providers, Slack grants no plain-HTTP loopback exemption, so `http://localhost:8765/callback` would have failed at the owner's *very first* setup step. Resolved against the primary source, which marks every `http://` example BAD; the "you can use localhost for development" line reconciles as *the host is fine, the scheme still must be TLS*.
- **Audio outliving the GPU on quit** (private) and **UTF-8 codepoints in the FreeType rasteriser** ([squz/ge](https://github.com/squz/ge)) — the rasteriser had been treating text bytes as codepoints, so anything above ASCII rendered wrong; the fix decodes properly, which is what unblocked non-ASCII place names in the geography title.

### Contributors

- Marcelo Cantos (AI co-authors — Claude Fable 5, Grok, Codex, and other Claude models — appear on `Co-authored-by` trailers throughout; much of the jevons work was landed by jevons's own supervised fleet).

---

## New Projects

### [marcelocantos/orthograph](https://github.com/marcelocantos/orthograph) — Shared Sketch Surface (86 commits, initial)

**The biggest effort of the week.** A Pencil-first collaborative sketch surface for technical diagrams, shared between a human on an iPad and coding agents on the Mac. The design states its non-goals as firmly as its goals: not an illustration suite, not a CAD constraint solver, not a replacement for text-defined diagrams — a complement to them.

- **The Mac owns the document.** `orthographd` holds a vector scene in SQLite with an append-only op log; documents rebuild from snapshot plus ops on load, and an early durability gap was closed by making scene and op writes one atomic transaction. Objects carry ULIDs and authors in a stable v1 schema, so an agent that created a rectangle can find it again after a restart.
- **Agents get a full surface, not a screenshot.** `orthograph_scene` returns the vector graph; `orthograph_render` returns pixels on request. The MCP tool set covers observation, the whole v1 object vocabulary, batch creation returning stable ids, clean-up, organisation and undo, media in and out, and document identity plus a **deterministic render hash** — so "did the canvas change?" is a cheap comparison rather than an image diff.
- **Dual-pipe intent and truth.** The daemon owns truth; the pad owns intent. Tentative ink comes from sqlpipe's `Replica` prediction API (v0.31, shipped this week for exactly this), and the earlier live-stroke dual-render layer was deleted rather than retained — the prediction path is the only path.
- **Pencil-native input.** Per-sample Apple Pencil force drives stroke segment thickness; tilt is preserved; the palm is kept off the canvas. Fingers pan, pinch-zoom and rotate the viewport — reserved to **three fingers**, so one and two fingers stay available for objects — and Pencil-only ink means a resting hand cannot draw. Tap-as-dot-then-type-as-text places a caret on the dot; Return is newline and Esc or the pen ends the edit.
- **Paper that looks like paper.** The default is a fine faint dot lattice rather than ruled lines; square and isometric grids are modelled as **lattices, not settings**, so an agent can set the grid a human draws on; the dark and light technical papers stay subtle at any zoom.
- **Pairing and networking.** The iPad pairs over the pigeon QR ceremony, verified through the shipped binary; a stranded pad can name its daemon and be repointed on-device; and the daemon **never advertises a loopback address to a pad**, which is the kind of bug that only appears on someone else's network. A spectator can watch read-only from across the room without write access.
- **Packaging.** Installs and runs as a Homebrew service with an end-to-end brew-service test, and the whole thing is documented as a standalone product rather than a Jevons feature.
- **445 file changes** (after excluding a briefly-tracked SPM build tree), **+43,945/−3,269**, **399 tests**, evidence screenshots committed for the Phase 0 MVP.

---

## Agent & Fleet Infrastructure

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — The Fleet Turns On Itself (80 commits, v0.9.0→v0.13.0)

Five releases, 968 file changes, **+160,946/−4,376**, and Go test functions growing 183 → 1,456 with JS test cases 80 → 991 — **+2,028 tests in one week**. The spend oracle, context ceiling, wake batching, treeguard, index guard, reap safety, staff cycles and owner-convergence plane are covered above. Also landing:

- **A frontier cockpit and fleet inspection surface**, progressive streaming markdown, chat resilience, and an RSI coach tab for judgements and dispositions.
- **One pending-owner-turn contract** (🎯T372) — a fork inventory was written first, exception candidates named, and only then did the main path adopt the agent path. The commit that recorded it also closed the design item, rather than leaving the inventory as a document nobody revisits.
- **Composer and chat affordances**: A/B/C design choices render as selectable cards; Tab cycles main and sidebar message boxes; target-filing asides paint distinct chrome from idea asides; sidebar conversations persist via the main chat journal; image markers no longer defeat command prefixes; protocol frames never appear as owner bubbles.
- **Build hygiene**: a clean checkout of `HEAD` builds without a generator step (🎯T360), and the daily serve-from-disk path now flags missing cockpit modules instead of silently serving a broken page.

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Bedrock, Durability, Fleet Identity (25 commits)

Covered above. Additionally: `AgentDef.Description` and `AgentDef.TargetID` for owner-facing labels and fleet engagement; `Materialized` set only on conversation evidence rather than on intent; `promptID` cleared on cancel with `PromptInFlight` exposed for the cockpit; a fall-through to spawn when a reattach dial fails; and hermetic gating of live Claude and Grok paths so `go test` stays offline. The tmux driver work is the fiddliest: `ready` now means **the composer accepts input**, not that it has been drawn (🎯T284), and large pastes are submitted with a confirmation that the turn actually began (🎯T305) — both bugs where the visible state and the usable state diverge. **51 new tests**; +4,313/−199.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Tool-Surface Reduction and Vault Themes (5 commits, v0.83.0→v0.85.0)

The 70 → 18 reduction is above. Alongside it, **document-level vault theme clustering** (🎯T64.8): a local-default TF-IDF plus single-link pipeline over decisions, compactions, patterns and user notes, with stable theme ids, label quality gates, pin/retire, run telemetry, MCP recluster/inspect/pin, generated theme pages and a 24-hour reconciler. The cost profile deliberately avoids a super-quadratic dendrogram retired earlier, taking a phase-1 cut with a document cap; a Voyage embeddings engine is wired but **opt-in with zero egress unless configured**. Context-aware mirror subprocesses (🎯T124) mean cancelling a worker terminates its `gh`/`git` children rather than letting one run to completion — and cancellation is deliberately *not* recorded as a mirror failure, since counting it would let a few restarts back a healthy repo off for hours. A recurring `git log ... exit status 128` turned out not to be non-repositories at all but real checkouts with **zero commits**, now distinguished as a third state (quiet success) from "not a checkout" (memoised) and genuine failure (propagated). **83 new tests**; +10,564/−3,990.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Graph Hygiene (1 commit, v0.44.0)

Advisory **merge completeness** for multi-predecessor fan-in: validate and summary report expected versus terminal predecessor counts when an active node has two or more dependencies and only partial fan-in. Shared vocabulary — fake edge, merge completeness, anchors, fresh-context — was recorded in the agents guide after a deliberately delayed re-read of a longform graph-engineering critique, with implementation follow-ups filed as targets and orchestration-runtime scope explicitly declined. **17 new tests**; +1,022/−114.

### [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) — Reload Loop and Stranded Sessions (1 commit, v0.9.0)

Covered above. +740/−7 across 12 files.

---

## Tooling & Workflow

### [marcelocantos/slacker](https://github.com/marcelocantos/slacker) — Browser OAuth and Multi-Workspace Credentials (19 commits)

The OAuth flow, TLS callback, preflight and per-account credential scoping are above. Two further items are the sharpest:

- **No secret is ever a tool argument** — tool arguments become conversation content: they pass through the model context and land in the transcript. Account labels and handles are fine; the client secret and OAuth token are not, so the secret is typed into a one-shot loopback form and the token goes browser → keychain, deliberately absent from every tool result. **A test walks every tool schema asserting no secret-shaped argument exists**, so a future tool cannot quietly reintroduce one. Login is asynchronous — begin returns a handle and the authorize URL, status polls — because many MCP clients cap tool-call duration well below the five-minute OAuth window.
- **Scopes tied to the methods actually called** — built from two independent inputs per the no-self-owned-gate-inputs rule: the method list is **read from the source at test time** so a newly added API call surfaces whether or not anyone remembered scopes, and the scope requirements are a frozen table transcribed from Slack's reference with a source URL per method. The two must agree exactly, so both a missing scope (login succeeds, calls fail) and an over-broad one are caught. It also confirmed the constraint the whole design rests on: `search.messages` is user-token-only.
- **12 MCP tools total** after six new configuration and onboarding tools, so an agent can take the owner from nothing to a working account without them touching a terminal. **53 new tests**; +3,730/−342.

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — Untainted Corpus and Concurrent Mermaid (9 commits, v0.9.0→v0.13.0)

Five releases. The corpus provenance rule and its two first-run defects are above; alongside them, rich import extracting media from RTF and DOCX and rendering PDF pages, Mermaid as SVG on the HTML path and PNG on the PDF path, loud Mermaid failures instead of silent blanks, concurrent Mermaid rendering, PR CI, and a dependency ratchet. Pasteboard tests are gated on a usable pasteboard rather than assumed. **25 new tests**; +2,983/−274.

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Agent UX and Mobile Spawn (2 commits, v0.77.0/v0.78.0)

Covered above. **39 new tests**; +3,407/−246.

---

## Libraries

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Replica Prediction (3 commits, v0.31.0)

An optional prediction inbound queue, the `Replica` prediction API exposed through CGo, and a Swift `TruthReplica` over a synchronous `CSqlpipe` — the substrate orthograph's tentative ink runs on, shipped in the same week as its first consumer. **30 new tests**; +1,622/−60.

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) — Swift Consumption (2 commits)

A `PigeonCore` pure-Swift product for iOS consumers and a fix to SPM linker paths for app consumers, with consumption documented. Small in lines (+131/−29) and load-bearing for orthograph's iPad build, which consumes pigeon as a sibling package.

### [squz/ge](https://github.com/squz/ge) — UTF-8 Text (1 commit)

Codepoint decoding in the FreeType rasteriser: text above ASCII had been rendering as mojibake. +76/−6.

---

## Web & Meta

### [marcelocantos/marcelocantos.com](https://github.com/marcelocantos/marcelocantos.com) — Open Source Page (2 commits)

An `/open-source/` products page on the Hugo site. +170/−1.

### [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) · [progress-reports-private](https://github.com/marcelocantos/progress-reports-private) (1 commit each)

The series split into a public repository and a private commercial companion, with the classifier, residual rules and dual-write procedure written into the guide. The public repository's history was rewritten in the process, which is why its line stats are now excluded from ☲ (see the honesty note). +4,175 and +60 respectively in headline ☲, with +54,953 and +1,775 of re-added back-catalogue excluded.

---

## Game Projects

### [squz/yourworld2](https://github.com/squz/yourworld2)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-08-09](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-09.md).*

---

## Commercial

### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) · minicadesmobile/Minicadeskit

*Detailed narrative in the private sibling: [progress-reports-private — week ending 2026-08-09](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-09.md).*

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **marcelocantos/jevons** — 114 commits in-flight (+24.6k/−1.4k); **marcelocantos/claudia** — 35; **marcelocantos/orthograph** — 6; **marcelocantos/sawmill** — 6; **minicadesmobile/stock-car-racing** — 3; **marcelocantos/rustuml** — 2; **marcelocantos/skills** — 2.
- **Health-Management-Systems/hms** — 16 in-flight; detail in [private week 2026-08-09](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-09.md).

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-08-03…09. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **19** |
| Total landed commits | **297** |
| Total lines added (landed, filtered) | +251,576‡ |
| Total lines removed (landed, filtered) | −14,330‡ |
| Net new lines (landed, filtered) | +237,246‡ |
| File changes | 2,049 |
| New files created | 884 |
| Bulk paths excluded from ☲ | +72,004 / −4,850 (progress-reports back-catalogue re-add, orthograph SPM build tree, lockfiles, `bullseye.yaml`, Unity/LFS churn) |
| Releases published | **18 across 7 repos** (jevons ×5, vellum ×5, mnemo ×3, spyder ×2, bullseye, mcpbridge, sqlpipe) |
| Languages | Go, Swift, JavaScript, C, C++, Rust, Python, C#, Objective-C, GLSL, Bash, Starlark, SQL, YAML, Markdown |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs — three entries added this run (see the honesty note).*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/orthograph](https://github.com/marcelocantos/orthograph) | 86 | 445 | +43,945 | −3,269 | +40,676\* |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 80 | 968 | +160,946 | −4,376 | +156,570 |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 31 | 140 | +6,832 | −584 | +6,248 |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 25 | 56 | +4,313 | −199 | +4,114 |
| [marcelocantos/slacker](https://github.com/marcelocantos/slacker) | 19 | 53 | +3,730 | −342 | +3,388 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 19 | 64 | +3,651 | −712 | +2,939 |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 9 | 68 | +2,983 | −274 | +2,709 |
| minicadesmobile/Minicadeskit | 8 | 29 | +3,209 | −121 | +3,088 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 5 | 105 | +10,564 | −3,990 | +6,574 |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 3 | 26 | +1,622 | −60 | +1,562 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 2 | 34 | +3,407 | −246 | +3,161 |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 2 | 16 | +131 | −29 | +102 |
| [marcelocantos/marcelocantos.com](https://github.com/marcelocantos/marcelocantos.com) | 2 | 2 | +170 | −1 | +169 |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 1 | 12 | +4,175 | −0 | +4,175\* |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 1 | 14 | +1,022 | −114 | +908 |
| [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) | 1 | 12 | +740 | −7 | +733 |
| [squz/ge](https://github.com/squz/ge) | 1 | 3 | +76 | −6 | +70 |
| [marcelocantos/progress-reports-private](https://github.com/marcelocantos/progress-reports-private) | 1 | 2 | +60 | −0 | +60\* |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 1 | 0 | +0 | −0 | 0† |

\* *orthograph's figures exclude 4,996 file changes of a briefly-tracked SPM build tree; the two report repositories exclude `reports/**` and `docs/**`, which the history rewrite re-added wholesale.*
† *target-ledger updates only — machine-written, excluded from ☲.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~2,028 | Go 183→1,456 and JS 80→991: spend oracle against a frozen baseline, ctxcap policy, wakebatch, treeguard two-sided oracle, reap classification, CSRF, virtual list |
| [marcelocantos/orthograph](https://github.com/marcelocantos/orthograph) | 399 | whole repo is new: document durability across restart, op-log rebuild, MCP tool surface, render hash determinism, pairing through the shipped binary |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 83 | theme clustering quality gates, tool-surface consolidation, mirror cancellation, empty-checkout classification |
| [marcelocantos/slacker](https://github.com/marcelocantos/slacker) | 53 | scope↔method agreement from two independent inputs, no-secret-argument schema walk, per-account credential isolation, dynamic loopback ports |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 51 | Bedrock hermetic streamer, `RequireResume` fail-closed, WebSocket connect-mode fake, setsid detach oracle |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 39 | `app_spawn` resolution ordering, `ensure_session`, structured results |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 30 | prediction begin/commit/rollback across C, Go and Swift bindings |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 25 | untainted-provenance guard, media matrix, concurrent Mermaid, binary-reached-markdown rejection |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 17 | POI axis conversion, menu flow, fleet E2E harness |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 17 | merge completeness across mixed, all-active, single-dep and fully-terminal fan-in |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 12 | save-at-award durability, cloud-resync guard |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 9 | adapter follow-ups |
| [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) | 2 | signature-evidence gate, Chmod exclusion |
| **Total** | **~2,766** | landed only; counted as net growth in test declarations across the window |

### Daily Activity

![Daily active repositories](daily-activity-2026-08-09.svg)

*(Active repositories per day: Mon 08-03 9, Tue 08-04 6, Wed 08-05 7, Thu 08-06 0, Fri 08-07 7, Sat 08-08 6, Sun 08-09 6. Thursday is completely empty — the only such day since 2026-07-24 — and the fleet still landed 297 commits in the remaining six.)*

---

## Ideas & Innovations

### Measure Along the Axes the Levers Act On ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
Almost every cost dashboard reports one number: total spend, perhaps split by day or by model. The jevons oracle refuses that shape, because **a sum of tokens cannot tell you which lever to pull**. Decomposing spend as *turns × calls-per-turn × context-per-call* maps each factor onto a distinct intervention — fewer wakes, fewer calls, smaller contexts — and every subsequent optimisation this week targets exactly one factor and can be checked against the frozen baseline. Two details keep it honest: context-per-call comes from the providers' own billing frames rather than an estimate, and unattributed spend is its own bucket that **stays in the denominator**, so an attribution scheme cannot flatter itself by discarding what it cannot classify.

### Unknown Never Compacts ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
A context ceiling is trivially easy to write and easy to write wrongly: if a missing measurement is treated as "small", the policy does nothing when it matters; if treated as "large", it rotates healthy agents at random and pays handover costs forever. `ctxcap` makes `unknown` a first-class third answer rather than a default, on the principle that **a missing measurement is not evidence of a small context**. The companion rule is the same instinct applied to configuration: a ceiling set below the minimum is *raised* rather than honoured, because obeying an obviously self-defeating setting is not respect for the operator.

### The Index Already Knows Who Chose the Commit ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
When several agents share one clone, distinguishing "this worker deliberately committed these paths" from "this worker swept up whatever was staged" looks like it needs a ledger of path ownership — which would be a whole subsystem, and wrong at the edges. Git already draws the distinction and hands it to every pre-commit hook: `git commit` builds from `$GIT_DIR/index`, while `git commit -a` or `git commit -- <paths>` builds from a temporary `index.lock`. **One string comparison separates a chosen commit from an inherited one.** The best guards are usually a signal already present that nobody was reading.

### An Alarm That Names the Lines It Would Have Dropped ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
Compare-and-swap on file writes is not novel; what makes treeguard good is the refusal message. A guard that says "conflict, re-read the file" leaves the agent to rediscover what it nearly destroyed. This one **names the specific lines the write would have removed**, which converts an interruption into a merge instruction and makes the recovery mechanical. The two-sided oracle matters for the same reason: a guard tested only for "refuses bad writes" can pass while refusing everything, so the test suite pins both directions.

### An Untainted Corpus, Enforced by a Test ([marcelocantos/vellum](https://github.com/marcelocantos/vellum))
The natural way to build fixtures for a document converter is to produce them with the converter's own dependency, which quietly makes the test suite a consistency check on that dependency rather than a correctness check on the product — it would pass even if both directions were symmetrically wrong. vellum's corpus is produced by implementations with no shared lineage, ground truth is hand-authored, and **the provenance rule is itself a test**: `TestCorpus_ProvenanceIsUntainted` fails if any manifest ever names pandoc, WeasyPrint, Prince or vellum as producer. That the corpus found two real bugs on its first run — including 19 KB of OLE2 binary returned as Markdown *content* with a nil error — is the strongest possible argument for the discipline.

### The Scope List Reads the Source ([marcelocantos/slacker](https://github.com/marcelocantos/slacker))
An OAuth scope set is a classic drift surface: someone adds an API call, nobody updates the consent request, and the failure appears months later at a user's terminal. Slacker's test builds one side by **reading the API method names out of the client source at test time** and the other from a frozen table transcribed from the vendor's reference with a per-method source URL, then demands exact agreement. Neither input is owned by the thing under test, so the gate cannot be satisfied by editing the answer, and it catches over-broad consent as loudly as it catches a missing scope.

### Secrets Are Not Tool Arguments ([marcelocantos/slacker](https://github.com/marcelocantos/slacker))
An MCP tool argument is not a function parameter. It passes through the model's context and lands in a transcript that is indexed, searched and possibly summarised elsewhere, so **any secret accepted as an argument is a secret published**. Slacker routes both the client secret and the OAuth token around the model entirely: the secret into a one-shot loopback browser form, the token from browser to keychain, absent from every tool result. Making that structural rather than aspirational is a test that walks all tool schemas and fails if a secret-shaped argument ever reappears. The asynchronous begin/poll login shape follows from the same realism — MCP clients cap tool-call duration well below a human's five-minute OAuth window.

### A Reload That Requires Evidence ([marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge))
The fix that ends the loop is not "ignore `Chmod`" — that alone would work, and the commit does it — but the second, independent change: **a reload now requires evidence that the binary actually differs.** Each watched path carries a size and mtime signature captured when it was tracked, and an event that does not move the signature is dropped, so the daemon can no longer assert "the binary changed" about a file it never compared. This is the general shape of defending against a filesystem-notification API you do not fully control: treat the event as a hint to check, never as the finding itself.

### The Rate of a Removal Is Evidence Too ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo))
`mnemo_self` was deleted rather than repaired, and the argument is entirely quantitative: two nonce rows in four months against eleven tool calls, and the alternative identity mechanism at 374 connection rows against exactly one session row, none in a month. Neither path could answer "which session am I", which is precisely why the tool could not simply be rebuilt on the other one. Sizing the whole MCP surface the same way — 70 tools down to 18 against recorded usage — treats tool count as a cost paid by every agent on every connection rather than as free optionality.

### A Coarse Pack of Agent Attention ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
Wake coalescing is arithmetically obvious once the cost is visible — batching *k* additive, order-free events divides their delivery cost by *k* with no information lost. What makes it a real insight is the measurement that preceded it: a breakdown showing that **over half of the wakes reaching the fleet's most expensive agent were neither the owner nor a worker result**. Nobody optimises notification plumbing on instinct; you do it after the profile says 27% idle nudges, 13% restart notices, 12% bare system reminders. The refinement — a single pending event renders as itself, without digest ceremony — keeps the common case from becoming more expensive than what it replaced.

---

## Effort Estimate: Traditional vs. AI-Assisted

The largest week of the series by every measure, and structurally different from the others: a new product went from nothing to installable while the fleet infrastructure spent most of its effort making its own operation measurable, bounded and safe. Much of the jevons work was landed by jevons's own supervised workers, which is also why several of the week's bugs are *coordination* bugs — shared indexes, shared trees, ambiguous completion claims — that simply do not arise with one engineer at one keyboard.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| orthograph nothing → brew-installable | 14-22 | A vector document model with an append-only op log and deterministic rendering, an MCP surface an agent can actually drive, a SwiftUI iPad app with per-sample Pencil force and correct palm rejection, pigeon pairing, prediction-backed tentative ink, and Homebrew service packaging — five unrelated specialisms, none of which can be stubbed. |
| jevons spend oracle, ceiling, wake batching, capacity | 8-13 | Deriving per-call context from two providers' differing billing frames, then designing policies whose failure directions are safe by construction; the arithmetic is easy and the honesty is not. |
| jevons fleet-coordination safety (treeguard, index guard, reap) | 5-8 | Concurrency bugs across processes with a filesystem and a git index as shared mutable state, each discovered only through real loss, each needing a guard that is loud rather than clever. |
| jevons staff cycles + owner-convergence plane | 4-7 | Standing background cycles that must converge, supersede rather than overwrite, and never starve owner work — plus a level-triggered health model for the chat plane itself. |
| slacker OAuth, TLS callback, multi-workspace credentials | 3-5 | OAuth against a provider whose documentation contradicts itself, with byte-exact redirect matching, a one-shot human consent that must not be wasted, keychain-scoped per-app credentials, and a hard rule that no secret crosses the model. |
| claudia Bedrock + Grok connect mode + tmux readiness | 3-5 | A third provider's streaming API, process-durable agents over WebSocket, and terminal-driving bugs where the visible state and the usable state diverge. |
| vellum untainted corpus + media matrix | 2-3 | Building fixtures with no shared lineage with the tooling under test, and enforcing that as a property rather than a convention. |
| mnemo tool-surface reduction + vault themes | 2-4 | Clustering with quality gates and a cost profile that avoids a known super-quadratic path, plus deciding what to delete on evidence. |
| sqlpipe prediction across C, Go and Swift | 1.5-2.5 | A prediction protocol exposed through CGo with matching Swift bindings, shipped in the same week as its first consumer. |
| spyder mobile spawn + agent UX | 1.5-2.5 | A resolution ordering that must fail closed on every ambiguous input, against real devices. |
| bullseye, mcpbridge, pigeon, ge, site | 2-3 | A composition-only reload loop, advisory fan-in validation, Swift packaging, and a UTF-8 decode. |
| Client and game downstream (private) | 5-8 | Detail in the private companion. |

### The Diversity Tax

This week spans Go (orthograph, jevons, claudia, mnemo, slacker, vellum, spyder, sqlpipe, mcpbridge), Swift and SwiftUI (the iPad app, PigeonCore, CSqlpipe), vanilla JavaScript at scale (the jevons cockpit), C (sqlpipe's CGo surface), C++ (ge), Rust (bullseye), C# and Unity (client work), Python (cook tooling), Starlark (device recipes), SQL, and platform surfaces spanning Apple Pencil input, PencilKit-adjacent gesture arbitration, Swift Package Manager, Homebrew services, launchd, kqueue and fsnotify semantics, AWS Bedrock streaming, Slack OAuth v2, and git's plumbing environment. No single engineer holds Pencil input arbitration, LLM billing decomposition, OAuth TLS loopback constraints and git index internals at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| orthograph | 7-11 | Deciding the product boundary against Jevons, judging on real hardware how ink and palm rejection feel, choosing three-finger viewport control, accepting the paper look, and running the pairing ceremony on an actual iPad. |
| jevons fleet economics and safety | 5-8 | Reading the spend breakdown and deciding which levers were worth pulling, accepting the frozen baseline as the gate, and calling the reap bias backwards after watching three agents die badly in an afternoon. |
| slacker / claudia / vellum | 3-5 | Provisioning the Slack app, sitting through live consent flows, and the standing call that secrets never cross the model. |
| Client and game work (private) | 3-6 | Perceptual judgement on the watermark working point, device regression runs, and release approvals. |

### What If It Were One Person?

The expert band sums to roughly 51-83 person-days, and a single generalist would fare considerably worse: the week requires Apple Pencil input semantics, SwiftUI, SQLite op-log design, two providers' billing formats, Slack's OAuth quirks, kqueue notification semantics and git plumbing — seven unfamiliar domains — before any of the actual work begins. The context-switch tax is unusually severe here because a new product and a large infrastructure push ran *concurrently* rather than in sequence, and because coordination bugs surfaced across repository boundaries. The specialist-team figure is lower for the usual reason, and lower than proportion would suggest for orthograph specifically, where an iOS specialist and a Go specialist working in parallel would have collapsed most of the calendar time.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~46-76 person-days (~2.3-3.8 months)** |
| Specialist team (traditional) | **~30-50 person-days (~1.5-2.5 person-months)** |
| Actual human effort this week | **~18-30 hours (~2.5-4.3 person-days)** |
| **Multiplier vs. generalist** | **~60-95x** |
| **Multiplier vs. specialist team** | **~40-62x** |

The multiplier peaks on orthograph, where a five-specialism product reached `brew install` in six days, and on the jevons economics work, where the expensive step is producing a measurement trustworthy enough to optimise against. It runs lowest on the parts that need a human body in the loop — Pencil feel on real hardware, perceptual judgement, store releases — which is the same floor every week in this series has hit. The human contribution concentrated on what a tool must refuse to do: that a reap must not be the default under ambiguity, that a secret must never be a tool argument, that an unknown measurement must not trigger an action, and that a drawing surface is a product rather than a feature of something else.

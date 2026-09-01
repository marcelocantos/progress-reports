# Weekly Progress Report — 2026-08-17…23

## Executive Summary

**Ten product repositories** landed the week's engineering; a Saturday entropy-audit documentation pass then touched **sixty-eight** others — **411 commits** in all, the second-largest week of the series by commit count. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** (280 commits, 138 of them `bullseye.yaml` ledger updates) spent the week making the fleet *interpretable*: host-owned MCP, a Session Goal the host can close without waiting for the model, Codex Session over `codex app-server`, a typed envelope layer, and the start of a fog-of-war scout that refuses to implement into an unseen map. **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** cut five releases (v0.23.0–v0.27.0) that are that substrate — Codex Session, a host-owned Goal loop across Claude/Grok/Codex, an HTTP MCP proxy that never stores tokens, `MCPExclusive`, and `AgentDef.Role`. **[marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)** v0.46.0 stopped auto-committing the ledger after every mutation, which is why the yaml-only chatter is at least now a *choice*. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** v0.86–v0.88 bounded queries, isolated reconcilers, and bound the local MCP server to loopback. **[marcelocantos/ytt](https://github.com/marcelocantos/ytt)** v0.12.0 split paced YouTube download from unthrottled analysis. **[marcelocantos/vellum](https://github.com/marcelocantos/vellum)** v0.14.0 grew a localhost Markdown view and a Confluence ADF package. **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** v0.80.0/v0.81.0 reports USB link speed with a ceiling and an anomaly. Commercial project detail: [private week 2026-08-23](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-23.md).

**411 commits** | **+35,928 net lines** | **~55-85 person-days traditional equivalent** | **~40-70x multiplier**

> Honesty note: new `data/line-excludes.yaml` entries land with next week's report (mnemo zstd amalgamation, housekeeping snapshots) — they do not apply here. Headline ☲ is gather `landed:` after the existing globs. Excluded bulk this week is **+7,983/−2,132** (lockfiles, `bullseye.yaml`, standing per-repo trees). Net is depressed by a sawmill entropy-follow-up squash that replaced the tree with a one-line `f.py` (**+1/−54,789**); reverted 31 August, outside this window. 138 of jevons's 280 commits are yaml-only ledger updates (lines already excluded from ☲; they still count toward ℂ). The Saturday fan-out is **69 documentation commits across 68 repos** (+31,716 / −0).

### Major Achievements & Innovations

- **Host-owned MCP, and a proxy that does not keep the keys** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.23–v0.27, [marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T464/🎯T520) — `LoadMCP` reads the machine's existing Claude/Grok/Codex maps; `EnsureMCP` merges one HTTP server under flock; `ProbeMCP` classifies open/static/oauth; `AuthorizeMCP` runs PKCE and *returns* tokens. The new `MCPProxy` is a mountable `http.Handler` whose tokens live in the handler and in the host, never in claudia. Silent `RefreshMCPToken` on 401; the browser opens only when refresh is missing or fails. Concurrent 401s on the same server used to open one tab each; refresh is now serialised per server.
- **A Session Goal the host can close** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) 🎯T53, [marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T510/🎯T528) — Goal is a durable host-owned objective, not a prompt prefix. `CloseGoal` plus `GoalCompleteCheck` stop `Continue` when the host's ledger already knows the work is done; remint cannot reopen it. Live journeys on Claude, Grok and Codex saw a second turn, then Stop. Codex Session itself moved onto `codex app-server` JSON-RPC (v0.23.0).
- **`MCPExclusive` so a Session is not drowned by user-scope maps** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.27.0) — default stays additive. When set, Claude gets `--strict-mcp-config`, Grok a private `GROK_HOME` with no `mcp_servers`, Codex a process-private `CODEX_HOME` holding only `Config.MCPServers`. v0.27.0 then dropped `EnsureMCP` from the surface: Session attach materialises MCP from `Config.MCPServers` without writing provider configs; hosts own durable merges themselves.
- **bullseye v0.46.0 — mutations write, they do not commit** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)) — T22's yaml-only commits were the dominant source of commit chatter. The store now leaves `bullseye.yaml` dirty; standing-invariants dirty-tree checks ignore the ledger; durability stays on `/commit` (stage) and `/push` (refuse). The T72 amend path is deleted, not left as dead code.
- **ytt v0.12.0 — paced download, unthrottled analysis** ([marcelocantos/ytt](https://github.com/marcelocantos/ytt)) — download ticks stay paced whenever the laptop is online; analysis processes anything already fetched and is not throttled. Synopses go through claudia (Grok → Claude → Codex). The skip ledger records only genuine YouTube dead-ends. `ytt build-index` is a Go subcommand; scheduled ingest pins a binary that actually has it.
- **spyder v0.80.0 — USB link speed as a ratchet** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) #155) — `devices()` joins one `ioreg` `IOUSBHostDevice` census onto adapter `List()` and reports `usb_speed`, a ratchet-up `usb_ceiling` under `~/.spyder/usb-speed.json`, and `usb_anomaly` when live is slower. Wireless ADB, sims, emus and desktop omit the fields.

### Significant Progress

- **Fog-of-war before implement, and a read-only auditor** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T536) — a scout phase (`FogMap.NeedsReslice` when blindspots hide more map) runs before implement; role comes from `agent_roles.json`, not `AgentDef.Role` baked into the binary. A silent-decision ledger on finish-report envelopes records what was decided without a prompt.
- **React cockpit restored onto master** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T537.1) — `/ws/mux` and the React UI land on the daily path, with Playwright on a clean-checkout rail (`make playwright-deps`) so a missing `node_modules` cannot skip-and-green.
- **Connect-replay paints the live end, not a desert of empty slots** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T494/J19) — pin connect to the last owner bubble, not the slot tail; snapshot display before fold so replay paints every turn; a void-after-detour oracle stays red until the canvas is not snapped. One owner-send path (`sendToNamedAgentAs`); inspect hydrates like main chat.
- **mnemo query deadlines, reconciler isolation, budget as a surface** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) v0.86–v0.88) — `Store.Query` runs under a 30 s budget distinct from `busy_timeout`; stream reconcilers take per-pass deadlines in parallel so one hung stream cannot starve the rest. Throttle engage/lift pushes OS/SSE alerts. Local MCP binds loopback by default (dual listeners).
- **vellum localhost Markdown view and Confluence ADF** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum) v0.14.0) — a view server plus an ADF package, landing in the same squash as last week's already-described TextKit-agent fallback. Advertised MCP tool names are checked against the registered set over an in-memory transport.

### Tough Challenges Overcome

- **A shared tmux paste buffer under concurrent send** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) T46/T469) — the fixed literal `claudia-send` raced: one sibling's `paste-buffer -d` deleted the shared buffer between another's load and paste. Each send is now `claudia-send-<pid>-<seq>`. Hermetic barrier oracles keep the shared-name path RED and the unique path GREEN.
- **One Authorize per 401 burst** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia), jevons T531) — concurrent Session 401s on the same proxied OAuth server each opened a browser tab. Serialise refresh/Authorize on the server; skip when another request already replaced the token that failed.
- **A live Goal continuation that hung Claude's paste-chip** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — a multi-line continuation hung submit after the first turn. The host now sends a single-line continuation. The live `TestGoalJourneyLiveBackends` gate is what saw the second turn on all three backends.
- **J19 connect-replay collapse** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)) — reload painted empty turn-slots between leftover bubbles because connect pinned to the slot tail, not the last owner bubble. The journey fails on an empty pane, not only a collapsed model; a second oracle fails when two leftover bubbles have a void between them.
- **An entropy-follow-up squash that deleted sawmill** ([marcelocantos/sawmill](https://github.com/marcelocantos/sawmill)) — `Land entropy-audit follow-up` replaced 249 files with a one-line `f.py` (the squash mixed test-fixture commits into the audit landing). Headlines this week include **+1/−54,789**. Reverted 31 August.

### Contributors

- Marcelo Cantos (AI co-authors — Claude Opus 5, Grok, Cursor, and other Claude models — appear on `Co-authored-by` trailers throughout; most of the jevons and claudia landing was done by the supervised fleet).

---

## Agent & Fleet Infrastructure

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Interpretable Fleet (280 commits)

**The biggest effort of the week.** No version tag; the daily daemon is the product. 752 file changes, **+39,661/−4,451**, ~478 net new test declarations. 138 commits are `Update bullseye.yaml`. The MCP/Goal/Codex/exclusive work, fog-of-war, React restore and J19 paint are above. Also landing:

- **Typed jevons envelopes** (🎯T509) — load-bearing fleet messages are typed, not free prose that a classifier has to re-parse.
- **Provider hard-block is fleet intent `blocked_provider`** (🎯T406) — spend/auth walls detected without relying on `ClassifyText`. Refusal-only turns must not clear impatience (🎯T454).
- **Plan-usage steers mint** (🎯T390.1.5) — session remaining-low/exhausted vetoes mint dest; daemon policy parks hot seats; early-window burn is damped so week-start is not hot; omit-provider mint is usage-first, config only breaks green ties. The header ticker is `jevons_plan_usage`.
- **Attribution on every stop** (🎯T466) — every stop drains the index; every write feeds the record; `ViaDrain` plus `bin/attrib` in `make all`.
- **Reaped agents stay reachable** (🎯T401) with reason + held sendq; survive held sendq across parent kill/remint (🎯T530). Depth-ceiling checkpoints stay registered and do not auto-reap as finished (🎯T471/🎯T497). Mid-mission checkpoint and false-green never reap as finished (🎯T470).
- **Never-materialized sessions report as dead, not running** (🎯T412). Spawn-brief delivery failure surfaces to the owning PO (🎯T433). Queued/unconfirmed start is brief-in-flight, not `unbriefed_seat` (🎯T518).
- **PO mint defaults `task_type=ceo`**, not `code_implement` (🎯T475). Codex work agents request a writable Session sandbox. Session Goal is set on work mint; J21 observes Codex continuation via phase, not Claude JSONL.
- **Grok Session ACP gets only live `jevonsmcp`** (🎯T525); `MCPExclusive` stamped on the overseer and leftover Grok serves. Loopback HTTP MCP proxy with silent token refresh (🎯T520).
- **Cited evidence SHAs must stay reachable from HEAD** (🎯T427). Blessed private-index commit recipe re-checks HEAD (🎯T432). `bin/gate` gains a `KILLED` verdict for host SIGKILL (🎯T461).
- **Idle Chat tab** skips T486 clear-measure (🎯T532); a TIME-delta sampler for idle Firefox cockpit CPU; Chat tab self-monitors idle snap/longtask storms. Provider model migration menu (🎯T285.2); Bedrock mark; ChatGPT mark for OpenAI. Auto-pin Spark/grok-build for short-context mint (🎯T325.2.1).
- **Work identity recovered on bare-thread remint** (🎯T474). Stop Session Goal Continue when mission evidenced complete (🎯T528). Live-stream handover seed ignores phantom Claude JSONL (🎯T519). Direct-route records named so T392.7 cannot fake-route idle (🎯T515).

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Codex Session, Goal, Exclusive MCP (26 commits, v0.23.0–v0.27.0)

Five releases in seven days. Codex Session via app-server, host-owned Goal, host-owned MCP inventory/proxy, `MCPExclusive`, token refresh, unique paste buffers, and `AgentDef.Role` are above. Additionally:

- **Cursor Session ACP + Task print** (v0.26.0) — `ProviderCursor` for Session (`agent acp`) and Task (`--print` stream-json), hermetic fakes, live gates, exclusive project MCP without HOME rewrite, opt-in plan usage. Codex binary discovery hardened against cmux shims.
- **Live MCP oracle under `MCPExclusive`** — rejects bare `"mnemo"` substrings (false positives on refusals); prefers direct mnemo `:19419/mcp` when jevons upstream is unrouted.
- **167 file changes**, **+11,620/−1,314**, **~107 net new tests**.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Stop Auto-Committing the Ledger (4 commits, v0.46.0)

Covered above. Also filed the 2026-08-22 entropy-audit findings as child targets of the parent analysis. **5 new tests**; +914/−1,036 across 16 files (the deletion is `src/git_commit.rs`, 816 lines — the amend path, gone).

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Deadlines, Throttle, Loopback (4 commits, v0.86.0–v0.88.0)

Query budgets, reconciler isolation, budget/throttle surfaces and loopback bind are above. `make bullseye` is hermetic under `GOWORK=off` so a parent `go.work` listing only claudia and jevons cannot fail this module's vet. **~38 new tests**; +3,607/−234 across 56 files.

---

## Tooling & Workflow

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — Paced Fetch, Unthrottled Analysis (2 commits, v0.12.0)

Covered above. Also: members-only skipped at listing, dash-prefix video IDs treated as IDs not flags, `--dry-run` leaves orphan dirs, a critique layer on the synopsis contract, and a ratchet that `pipx` / Python 3 / `youtube-transcript-api` stay off the README. `unset GOWORK && make test` — Go `-race` ok, bats 73/73. **~25 new tests**; +3,576/−559 across 30 files.

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — Markdown View + ADF (2 commits, v0.14.0)

Covered above. **~29 new tests**; +4,169/−386 across 37 files. The TextKit-agent fallback described last week is in this squash; it is not re-counted as a new idea.

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — USB Speed Ratchet (5 commits, v0.80.0–v0.81.0)

USB link-speed reporting is above. gofmt drift fixed and `GOWORK=off` forced for bullseye (ENT-007). **~13 new tests**; +2,288/−100 across 32 files.

### [marcelocantos/homebrew-tap](https://github.com/marcelocantos/homebrew-tap) — Drop tern.rb (2 commits)

`tern.rb` removed — the project was renamed to pigeon. Plus the entropy-audit report.

### [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) — Tree Replaced by `f.py` (1 commit)

The entropy-follow-up squash wiped the repository to a one-line test fixture. See Tough Challenges. Not product work.

---

## Fleet entropy audit (68 repositories, 69 commits)

On 22 August a documentation pass landed `docs/audits/entropy-audit-2026-08-22.md` (and, in repos that already had a parent analysis target, child ENT-* findings) across the fleet. The progress-reports copy is typical: competing oracles on daily-count headlines, a producer/docs split that puts T1/T2 in three places, and a published content store whose generators live out of tree. These commits are in the metrics tables and in Saturday's 78-repo spike; they do not each get a narrative section. Open-source `squz/ge` is in this set.

---

## Commercial

### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-08-23](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-23.md).*

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **Health-Management-Systems/hms** — 96 in-flight; detail in [private week 2026-08-23](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-23.md).
- Other unmerged branches exist across the entropy-audit fan-out (typically the same docs commit on a side branch); they are not product WIP.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-08-17…23. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **78** |
| of which product work | **10** |
| of which entropy-audit docs only | **68** |
| Total landed commits | **411** |
| of which jevons yaml-only ledger | **138** |
| Total lines added (landed, filtered) | +99,005‡ |
| Total lines removed (landed, filtered) | −63,077‡ |
| Net new lines (landed, filtered) | +35,928‡ |
| File changes | 1,475 |
| New files created | ~470 |
| Bulk paths excluded from ☲ | +7,983 / −2,132 (lockfiles, `bullseye.yaml`, standing per-repo globs) |
| Releases published | **13** (claudia v0.23–v0.27, mnemo v0.86–v0.88, spyder v0.80–v0.81, vellum v0.14.0, ytt v0.12.0, bullseye v0.46.0) |
| Languages | Go, JavaScript, TypeScript, TSX, YAML, Markdown, HTML, Rust, Python, Swift, Shell, CSS |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. Net includes sawmill **+1/−54,789** (tree wipe). Without that commit, net is ~+90,716. No new globs this week.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 280 | 752 | +39,661 | −4,451 | +35,210 |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 26 | 167 | +11,620 | −1,314 | +10,306 |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 16 | 60 | +1,122 | −168 | +954 |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 2 | 37 | +4,169 | −386 | +3,783 |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 2 | 30 | +3,576 | −559 | +3,017 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 4 | 56 | +3,607 | −234 | +3,373 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 5 | 32 | +2,288 | −100 | +2,188 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 4 | 16 | +914 | −1,036 | −122 |
| [marcelocantos/homebrew-tap](https://github.com/marcelocantos/homebrew-tap) | 2 | 4 | +331 | −40 | +291 |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 1 | 248 | +1 | −54,789 | −54,788* |
| 68 other repositories (entropy-audit docs) | 69 | 73 | +31,716 | −0 | +31,716 |

\* *Entropy-follow-up squash replaced the tree with `f.py`. Reverted 2026-08-31.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~478 | J19 connect-replay, exclusive MCP, Goal journeys, plan-usage mint veto, Playwright clean-checkout, typed envelopes |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~107 | Codex app-server Session, MCP proxy/refresh, unique paste-buffer barriers, Goal live backends, Cursor ACP fakes |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | ~29 | advertised-name reflection, Markdown view, ADF |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | ~25 | paced download vs analysis, build-index Go, skip-ledger, shipped-docs ratchet |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~38 | query deadline vs busy_timeout, reconciler isolation, loopback bind, throttle alerts |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~13 | USB speed/ceiling/anomaly |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 5 | no auto-commit after mutation; dirty-tree ignores ledger |
| **Total** | **~695** | landed only; net growth in test declarations across the window |

### Daily Activity

![Daily active repositories](daily-activity-2026-08-23.svg)

*(Active repositories per day: Mon 08-17 4, Tue 08-18 3, Wed 08-19 4, Thu 08-20 0, Fri 08-21 3, Sat 08-22 78, Sun 08-23 4. Saturday is the entropy-audit fan-out.)*

---

## Ideas & Innovations

### The Host Owns MCP; the Library Does Not Keep the Keys ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
Every previous MCP helper wrote into the provider's user-scope config, which is how a fleet Session inherited whatever the laptop's Claude install happened to have — including servers that 502 the worker. The split is **inventory, proxy, persist**: claudia will load, probe, authorise and reverse-proxy; it will not write tokens to disk. `SetToken` / `OnTokenChange` exist so jevons can reseed. Exclusive mode then *subtracts*: a Session sees only `Config.MCPServers`, even if `~/.claude.json` is a bazaar. Additive-by-default keeps other clients working; exclusive is the fleet's opt-in.

### CloseGoal Is a Host Fact, Not a Model Utterance ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
A Session Goal that continues until the model prints `GOAL_STATUS: complete` will continue after the ledger already knows the work is done — remint reopens it, and a second turn is spent restating a closed case. **`CloseGoal` plus a host `GoalCompleteCheck`** make completeness a property of the consumer. The live gate (Claude, Grok, Codex) is the point: hermetic green on a fake that emits `GOAL_STATUS` cannot see a paste-chip that hung on a multi-line continuation.

### Connect Must Pin to a Person, Not a Slot ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
A virtualised transcript has two tails: the slot array and the last owner bubble. Reload that pins to the slot tail paints a desert of empty turn-slots between leftover bubbles — the chat looks alive and is not. **J19 fails on an empty pane, not only a collapsed model**, and a second oracle fails when two leftover bubbles have a void between them. The live end is a person, not an index.

### Mutations That Auto-Commit Cannot Be Reviewed ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye))
A ledger that commits itself after every MCP mutation produces a git history of "Update bullseye.yaml" — 138 of them in jevons this week alone, still, because agents also commit. Stopping the *server* from committing is the half it can keep: the file goes dirty, `/commit` stages, `/push` refuses a dirty ledger. The amend path that inferred ownership from "HEAD is unpushed and touches only `bullseye.yaml`" is deleted, because that inference was last week's SHA-stability incident.

### Download Is I/O; Analysis Is Compute ([marcelocantos/ytt](https://github.com/marcelocantos/ytt))
A single paced loop that both fetches YouTube and calls three LLM providers will stall fetch whenever Codex is at quota. **Splitting the clocks** — download ticks whenever the laptop is online; analysis processes the pile without waiting — is what lets a mixed-ladder miss (next week: don't abort the queue) stay a miss instead of an outage. The skip ledger recording only genuine YouTube dead-ends is the same instinct: a capacity miss is not a 404.

---

## Effort Estimate: Traditional vs. AI-Assisted

A louder week than the last on commit count, quieter on new product: the fleet spent it making MCP, Goal and Session a host-owned contract, then documenting entropy across seventy repositories in a day.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| claudia host-owned MCP + proxy + Exclusive + Goal | 8-12 | OAuth PKCE that must not store tokens; per-provider isolation (Claude `--strict-mcp-config`, Grok `GROK_HOME`, Codex `CODEX_HOME`); live Goal journeys on three backends. |
| jevons fleet interpretability (envelopes, plan-usage mint, attribution, J19) | 10-16 | A virtualised 280k-line journal whose connect pin, inspect hydrate and owner-send path must agree; mint vetoes that treat 0 remaining as exhausted. |
| jevons fog-of-war + auditor role | 2-4 | A scout that reslices when blindspots hide map; role from a file, not a compiled enum. |
| mnemo deadlines / throttle / loopback | 2-3 | Query budget distinct from lock wait; reconcilers that cannot starve each other. |
| ytt paced download vs analysis | 2-3 | Two clocks, a skip ledger that is not a capacity miss, a Go `build-index` the scheduled binary actually has. |
| vellum Markdown view + ADF | 2-3 | A localhost view and a Confluence package on top of last week's importer split. |
| spyder USB speed ratchet | 1-1.5 | `ioreg` census joined onto adapter list; ceiling stored, anomaly when live is slower. |
| bullseye stop auto-commit | 1.5-2.5 | Deleting the amend path rather than leaving it; dirty-tree checks that ignore the ledger. |
| Entropy-audit documentation fan-out | 3-5 | Seventy honest per-repo snapshots in a day, with ENT children where a parent analysis target already existed. |
| Client work (private) | 2-4 | Detail in the private companion. |

### The Diversity Tax

This week spans Go (jevons, claudia, spyder, vellum, mnemo, ytt), vanilla JavaScript and TSX at cockpit scale, Rust (bullseye), C# / Unity (client), tmux paste-buffer identity, HTTP MCP OAuth (PKCE, DCR, refresh), Codex app-server JSON-RPC, Cursor ACP, launchd-adjacent USB `ioreg`, and a documentation audit whose findings now live as bullseye children. No single engineer holds MCP OAuth token lifetime, tmux paste-buffer races, Unity GPU denylists and Codex app-server session resume at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| Fleet MCP/Goal contract | 6-10 | Deciding that claudia does not persist tokens, that Exclusive is opt-in not default, that CloseGoal is a host fact, and that live Goal journeys on three backends are the gate. |
| jevons landing review | 4-7 | Calling J19's empty-pane a paint bug not a model bug; keeping yaml-only commits out of ☲; rejecting skip-and-green Playwright. |
| Entropy-audit direction | 2-4 | Naming competing oracles as the headline finding; not treating the fan-out as product work. |
| Client and device work (private) | 2-4 | Play crash-table GPU names, Adaptive-icon viewport, TestFlight/Play scope. |
| sawmill wipe | 0.5-1 | Noticing the tree was `f.py`. |

### What If It Were One Person?

The expert band sums to roughly 34-54 person-days. A single generalist pays ramp-up on MCP OAuth, three providers' Session Goal loops, a virtualised chat connect-pin, and Unity's GPU-vendor denylist — domains that do not appear in the same career. The context-switch tax is milder than a week that founds a product, harsher than a specialist split where a runtime engineer could have taken claudia and a cockpit engineer J19 in parallel.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~55-85 person-days (~2.8-4.3 months)** |
| Specialist team (traditional) | **~40-62 person-days (~2.0-3.1 person-months)** |
| Actual human effort this week | **~16-26 hours (~2.0-3.3 person-days)** |
| **Multiplier vs. generalist** | **~40-70x** |
| **Multiplier vs. specialist team** | **~25-45x** |

The multiplier peaks on the MCP/Goal contract, where the expensive step is naming who owns tokens and who owns completeness. It runs lowest on the entropy-audit fan-out (mechanical once the template is honest) and on the human-in-the-loop GPU denylist. The human contribution concentrated on what a tool must refuse to do: that claudia does not persist tokens, that Exclusive is not the default of `Launch`, that a wall clock is still not a verdict, and that an entropy squash is not a licence to replace a tree with `f.py`.

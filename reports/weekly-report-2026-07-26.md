# Weekly Progress Report — 2026-07-20…26

## Executive Summary

**Sixteen repositories** landed work this week, and the centre of gravity moved from platform lanes to *containment, delivery, and the pipes that carry evidence*. The biggest single effort is **[marcelocantos/writ](https://github.com/marcelocantos/writ)**, a new project that went from empty repo to working MVP in four days: it compiles a declared JSON *intent manifest* — what a command will read, write, fetch, and exec — into an OS-enforced environment (a macOS [seatbelt](https://developer.apple.com/library/archive/documentation/Darwin/Reference/ManPages/man1/sandbox-exec.1.html) profile, a manifest-keyed egress proxy, a filtered environment) and then runs the command unmodified inside it. Ten releases shipped across five repos. **[squz/ge](https://github.com/squz/ge)** cut four tags (v0.80→v0.83) carrying a compressed-texture cook-and-load pipeline ([ASTC](https://en.wikipedia.org/wiki/Adaptive_scalable_texture_compression)/[ETC2](https://en.wikipedia.org/wiki/Ericsson_Texture_Compression)), a zero-I/O per-instance frame-metrics ring, and an automated [SDL3](https://www.libsdl.org/) 3.4.12 prebuilt recook; **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** (v0.72→v0.73) turned both into agent-drivable surfaces — semantic `hit_targets` addressing that taps buttons by stable id rather than pixel coordinates, and a per-instance metrics proxy. **[marcelocantos/csp](https://github.com/marcelocantos/csp)** shipped v0.25.0 and v0.26.0: a scheduler-thrash fix worth **~3× on multi-writer `alt/8ch`** (3.2 µs → 1.07 µs) plus a two-tier Windows strategy — a fast cloud smoke job and an authoritative local ARM64 VM gate. **[marcelocantos/blurter](https://github.com/marcelocantos/blurter)** went from nothing to a tapped v0.1.0 release in a single day: a spool-first notification daemon born from a real fortnight-long silent alert loss. **[marcelocantos/ytt](https://github.com/marcelocantos/ytt)** v0.10.0 ended a **16-day silent ingest outage** in which fifteen consecutive scheduled runs did nothing and exited zero. Commercial project detail: [private week 2026-07-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-26.md).

**63 commits** | **+20,805 net lines** | **~16-26 person-days traditional equivalent** | **~30-50x multiplier**

> Honesty note: `data/line-excludes.yaml` gained six entries this run, so ☲ is stricter than in prior reports. New fleet defaults exclude machine-written files — dependency lockfiles and `bullseye.yaml`, which the bullseye MCP server owns and which moved **1,089 lines in a single csp commit**. Total excluded bulk: **+2,877/−1,211**. Earlier reports were not restamped, so week-on-week ☲ comparison now understates this week slightly. Commercial project detail: [private week 2026-07-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-26.md).

### Major Achievements & Innovations

- **Compressed texture cook and load, owned by the engine** ([squz/ge](https://github.com/squz/ge), 🎯T167, v0.83.0) — a new `bin/ge-texenc` CLI where the *output extension* selects the encoder, backed by statically built ARM [astc-encoder](https://github.com/ARM-software/astc-encoder) and [etcpak](https://github.com/wolfpld/etcpak) (neither linked into `libge.a` — cook path only). Make pattern rules (`%.astc.getex: %.png`) mean consumers just declare the cooked artefact as a dependency. At runtime `ge::loadTexture` queries `sg_query_pixelformat` for real backend support and walks an ordered ASTC → ETC2 → PNG candidate list, so games never branch on encoding and device packages can ship compressed-only while desktop keeps source PNGs for the authoring loop.
- **A zero-I/O frame-metrics ring, end to end from engine to agent** ([squz/ge](https://github.com/squz/ge) 🎯T166 v0.81.0, [marcelocantos/spyder](https://github.com/marcelocantos/spyder) 🎯T110 v0.73.0) — `ge::metrics::metric<T>` makes per-frame capture a plain assignment guarded by one branch, with no formatting or syscall on the hot path and the whole surface compiled out under `NDEBUG`. Rings are bound to a per-instance `Scope`, not process-global statics, so two game instances in one process cannot cross-talk. Five wire methods expose it as spyder's `app_metrics_*` tools, which return the **full retained frame history** rather than the latest-value gauges the existing `app_perf_get` provided.
- **Scheduler thrash fix worth ~3×** ([marcelocantos/csp](https://github.com/marcelocantos/csp), 🎯T37, v0.25.0) — multi-writer `alt/8ch` went from ~3.2 µs to ~1.07 µs on an M4 Max with `send/recv` unchanged at ~150 ns, by closing a hole in an existing fast path and converting work-stealing from global-queue bouncing to direct steal-to-local. The TLA+ specs `StealWork.tla` and `StealWork_Bug.tla` were updated in the same commit.
- **Two-tier Windows CI with an honest known issue** ([marcelocantos/csp](https://github.com/marcelocantos/csp), 🎯T39/T40, v0.26.0) — a 10-minute cloud MSVC job runs a curated 16-unit doctest smoke, while the *authoritative* merge gate is a local Parallels Win11 ARM64 VM that refuses to run unless `HEAD` is already pushed, clones the exact SHA, and keys pass/fail on an in-band `csp_test_exit=0` marker rather than trusting ssh exit-code propagation. v0.26.0 shipped with the residual full-suite hang declared as a known issue rather than papered over.
- **blurter v0.1.0 — spool-first notification delivery, nothing to released in a day** ([marcelocantos/blurter](https://github.com/marcelocantos/blurter)) — `blurter send` is an atomic durable file write that holds no credential and never touches the network; the daemon owns the token, the policy, and the sinks, and records delivery state only *after* a sink confirms. Per-app dedup, `renotify_after` windows with a `STILL BROKEN (Nd)` prefix, exactly one `RECOVERED` notice, and an `audit.jsonl` line for every decision including each suppression and its reason. Released and tapped the same day it was created.
- **ytt v0.10.0 — ending a 16-day silent outage, then instrumenting against the class** ([marcelocantos/ytt](https://github.com/marcelocantos/ytt), 🎯T11) — channel ingest had done nothing since 2026-07-10 across fifteen scheduled runs, exiting zero every time. Beyond the fix, every unhealthy outcome now routes through a single exit path that both fails the run and alerts, and a **liveness backstop fires on a non-event** — nothing ingested for seven days while channels are tracked is itself a failure. A new `--dry-run` resolves config and prints the would-be queue without spending, which is how the fix was verified without paying for the 51-video backlog it uncovered.
- **Semantic UI addressing for agent-driven games** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) 🎯T109 v0.72.0, [squz/ge](https://github.com/squz/ge), [squz/multimaze2](https://github.com/squz/multimaze2)) — `ge::Button` now exports `id`/`role`/`label`/`hitBounds` through a built-in `hit_targets` state slice registered *before* the hello handshake, with `bbox_norm`/`center_norm` in 0–1 inject space. spyder resolves targets by **id first, then role, and deliberately never by display label** (localisation-safe), and fails closed on a disabled target rather than tapping a dead button. MultiMaze wired stable ids through its top bar and level/pack/buy chrome.
- **SDL3 3.4.12 with an automated prebuilt recook** ([squz/ge](https://github.com/squz/ge), v0.82.0) — a new 287-line `tools/rebuild-sdl-prebuilts.sh` builds static SDL3 for macos-arm64, ios-arm64, ios-arm64-simulator and android-arm64, then SDL_image and SDL_ttf for the three Apple destinations, and assembles seven xcframeworks — replacing a manual ritual, and ending with a `strings`-based version assertion.
- **A live interactive-maths demo platform in a day** ([marcelocantos/marcelocantos.github.io](https://github.com/marcelocantos/marcelocantos.github.io)) — a shared [Three.js](https://threejs.org/) shell (camera framing, orbit/pan, a draggable-handle registry) plus content-only demo modules and a Python CLI for scaffolding, serving, and content-scoped publishing. Two demos are live; a 505-line monolith became a 104-line content module in the process.

### Significant Progress

- **writ — declared-intent execution, scaffold to MVP in four days** ([marcelocantos/writ](https://github.com/marcelocantos/writ), 8 commits, +5,192/−701) — a versioned JSON schema with five intent classes (`fs`, `net`, `exec`, `ssh`, `env`), an SBPL compiler that confines all seatbelt knowledge to one package, a CONNECT-bridging egress proxy that refuses undeclared hosts with a structured denial naming the manifest field that *would* have permitted them, an env allow-list so secrets are never granted by omission, and a drift audit that diffs [`eslogger`](https://developer.apple.com/documentation/endpointsecurity) NDJSON against the manifest. Zero external dependencies — `go.mod` has no `require` block. Fail-closed by construction: path-prefix `net` intents are a *compile error* until a TLS-terminating proxy exists rather than a silent host-wide over-permit.
- **jevons chat UI at scale** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons), 🎯T55/T57/T58) — bounded server replay (30 turns plus a paged `/api/history`), preview-only client rendering, an rAF-debounced streaming coalescer that turns O(N²) re-parses into O(N), and an `IntersectionObserver` infinite scroll that preserves scroll position when prepending older windows. Load on the owner's real history fell from 15–20 s to ~1.5 s with DOM nodes bounded to ~276. The durable journal was deliberately left untouched — only what the UI *materialises* is bounded.
- **GitHub issues as a target event path** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) 🎯T33/T35, [marcelocantos/issuepipe](https://github.com/marcelocantos/issuepipe) 🎯T32) — issuepipe gained an export API scoped by the caller's *GitHub* identity with no local ACLs, deliberately returning 403 rather than 404 for unauthorised repo ids so the existence of a Master is not leaked. bullseye added a feature-gated consumer that maps issues to `GH{repo_id}-{n}` targets, treats authorisation and consent as separate (opt-in is strict), skips a forbidden repo without aborting the cycle, and now runs continuously on an `--interval` whose sleep is sliced so shutdown stays responsive. Measured end-to-end pickup: **4 seconds**.
- **Store telemetry without a browser** ([marcelocantos/asc](https://github.com/marcelocantos/asc), 🎯T1 retired) — ES256 JWTs minted per request with a 19-minute TTL against Apple's 20-minute cap, multi-key credential resolution outside the repo, and gzip-TSV sales-report parsing. The domain insight that makes it correct: Sales Trends "Units" counts *first-time downloads only*, so product-type identifiers are classified and updates excluded by default — without which reported units would have inflated ~2.5× on the test fixture. Cross-checked live against Apple's own figures for MultiMaze.
- **Agent DX truth pass across the game stack** ([squz/ge](https://github.com/squz/ge), [squz/esfera2](https://github.com/squz/esfera2), [squz/multimaze2](https://github.com/squz/multimaze2), [squz/yourworld2](https://github.com/squz/yourworld2)) — not a docs polish but a correctness pass: every game's agent entrypoint still described the pre-Plateau-P world (bgfx renderer, the deleted `ged` daemon and its dashboard, wire-mode workflows). ge added a "Consumer DX contract" mandating alignment, and each game converged on `AGENTS.md` as canonical with a thin `CLAUDE.md` adapter, deleting dead Makefile targets along the way.
### Tough Challenges Overcome

- **Three confinement escapes in a sandbox that had just shipped** ([marcelocantos/writ](https://github.com/marcelocantos/writ)) — found by adversarially probing his own MVP. `/Users` sat in the default read list so `getcwd()` could resolve ancestors, which silently made *every* home secret readable and defeated the manifest's central premise; SSH was pinned by a `PATH`-front wrapper that `exec`'d `/usr/bin/ssh`, so the profile had to allow that binary and the child could simply call it by absolute path; and the drift audit ran `eslogger` as a blocking call *after* the child exited, so it could never observe what it audited. Fixes respectively: drop `/Users` and rely on directory metadata plus manifest paths; copy the real binary to a private name off `PATH` and allow only that; restructure into a streaming session started before the child, with the sandbox PID fed back via an `OnStart` callback.
- **A 16-day silent outage caused by pinning a binary** ([marcelocantos/ytt](https://github.com/marcelocantos/ytt)) — an earlier hardening change pinned the scheduler to the *installed* binary, which repointed `$HERE` at a Homebrew Cellar directory that never contains the gitignored `channels.yaml` and is replaced wholesale on every upgrade. The lesson recorded in the commit generalises: **pinning an executable also repins every path derived from that executable's location.** The sharper observation is that eighteen prior hardening changes all asked "did this step fail?" and none asked "is this pipeline still producing anything?" — exit codes are not monitoring.
- **A fast path with a hole in it** ([marcelocantos/csp](https://github.com/marcelocantos/csp), 🎯T37) — 🎯T34 had already introduced wake-to-local, but the *deferred*-wake path taken on every close-race rendezvous — precisely the fan-in case under measurement — still hard-coded the old global-queue push and unpark, silently re-entering the park/steal storm the optimisation was meant to end. Compounding it, every steal bounced through the global queue and unparked a second worker to race for the work. The fix rested on a non-obvious lock-ordering insight: because `placed_` already serialises against `schedule()`, a stolen imp can move victim-ring → thief-ring under two sequential single locks, letting an entire dual-lock dance be deleted.
- **A CSS fix that measurably improved the wrong thing** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons), 🎯T55→T57) — clamping oversized message bodies looked like a legitimate solution and made bubbles visibly smaller, but the browser still parsed and built DOM for every turn and then hid it after the fact, so the owner still watched 15–20 s of lists scrolling. The real cost was the server replaying the entire journal on each WebSocket reconnect, compounded by an O(N²) streaming coalescer. Only attacking all three layers fixed it, and true node virtualisation is left explicitly open rather than claimed.
- **A belief that made a context-destroying hack look mandatory** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons), 🎯T58) — the overseer was rotated onto a fresh session on every daemon restart and re-seeded with a lossy recap, because the Grok CLI was believed to drop MCP servers on `session/load`. A decisive experiment falsified it with a precise distinction: only the *session-scoped* ACP `mcpServers` parameter is ignored on load; a *user-scoped* config entry attaches on both new and loaded sessions. The overseer now keeps full model context across restarts, and the rewind path still rotates deliberately, because in-place truncation genuinely is impossible.
- **Shadow quality that blinked on a 4-second cycle** — detail in [private week 2026-07-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-26.md)
- **Two silent-failure bugs in one daemon install** ([marcelocantos/den](https://github.com/marcelocantos/den)) — the macOS launchd path resolved its own binary through `/proc/self/exe`, a Linux-only interface inside an `#ifdef __APPLE__` block, and emitted argv the CLI does not accept; separately, `set_setting` inferred JSON type from the *existing* value, so a first-time `den set daemon.auto_upgrade true` stored the string `"true"`, which the reader's `is_boolean()` check skipped. The user enabled a feature and nothing happened, with no error anywhere. The fix corrects the writer *and* teaches both readers to accept the legacy string form, so configs already broken on disk heal on next read.

### Contributors

- Marcelo Cantos (AI co-authors — Claude Fable 5, Grok, and other Claude models — appear on `Co-authored-by` trailers throughout; spyder's `hit_targets` commit is co-authored with Grok).

---

## Security & Execution Infrastructure

### [marcelocantos/writ](https://github.com/marcelocantos/writ) — Declared-Intent Execution (8 commits, initial)

**The biggest effort of the week.** A new standalone product: the caller declares what a command will do, writ synthesises an environment in which only that is physically possible, and the command runs unmodified inside it. The thesis is recorded in `docs/design.md` — command-text filters run *pre-expansion*, so the shell executes something the filter never saw, and all-or-nothing sandboxes cannot distinguish a legitimate fetch from exfiltration, so they fail the whole command and the caller rationally retries *outside* the sandbox. Containment that is too blunt manufactures its own bypass pressure.

- **The schema is the product**: a versioned, tool-agnostic JSON manifest with five intent classes — `fs` read/edit globs, `net` host-or-URL, `exec` with `argv_taint`, pinned `ssh` host/user/cmd, and an `env` allow-list. Backends are codegen targets; the v0→v1 redesign replaced a verbose object array with compact glob-string lists under one invariant — **every target is a glob, and a fixed path is a glob matching one path** — with a custom unmarshaller that detects the v0 form and rejects it pointing at a migration doc.
- **Enforcement**: an SBPL compiler (470 lines) confining all undocumented-Scheme knowledge to one package behind a `Compile()` interface, including handling the `/var/folders` vs `/private/var/folders` symlink duality; a localhost egress proxy holding a host → manifest-field map, hijacking CONNECT and stripping hop-by-hop headers; and an env filter that grants nothing by omission.
- **Audit as an injection detector**: diffing declared intent against `eslogger` reality is free prompt-injection detection — a process that declared "edit `*.c` under `src/`" and then touches `~/.ssh` is not merely denied, it has produced the highest-signal alarm in the stack, *because stated intent finally provides a baseline*.
- **Fail-closed discipline**, pinned by tests: unimplementable `net` path-prefixes and `argv_taint: deny` are compile errors rather than silent over-permits.
- **A red team promoted into a standing oracle**: an adversarial harness plants victim files outside scope (including a fake `~/.ssh/id_rsa`) and three bait symlinks inside it, then attacks with ~18 path-construction techniques — `../` walks, symlink traversal, path-normalisation tricks, `find -delete`, `python3 os.unlink`, shell truncation, mv-then-rm laundering, nested `sh -c` — and asserts every victim survives byte-identical, with a positive control first proving legitimate in-scope writes still work. The follow-up commit promoted the 195-line throwaway script into a Go test driving `run.Exec` directly, leaving an 8-line wrapper. **36 new tests**, all green; +5,192/−701.

---

## Tooling & Workflow

### [marcelocantos/blurter](https://github.com/marcelocantos/blurter) — Spool-First Notification Daemon (4 commits, initial, v0.1.0)

New this week and released the same day. Applications spool events to disk; a daemon owns the credential, the policy, and the sinks.

- **Durability inversion**: `Spool` is a temp-file + `fsync` + `rename`, so a reader never sees a partial event and a power cut cannot lose one; delivery state is recorded only after a sink confirms, and undeliverable events are parked rather than deleted.
- **Failure taxonomy**: transient conditions (no network, 5xx, rate limit) retry with exponential backoff; permanent ones (`invalid_auth`, `channel_not_found`, `missing_scope`, …) do not, because retrying a misconfiguration forever buries real alerts. The Slack sink parses the response body rather than the HTTP status, since `chat.postMessage` answers 200 with `{"ok":false}` for logical failures.
- **An MCP surface defined by what it refuses**: `blurter_send`/`_status`/`_recent` spool and read exactly like the CLI, so an agent is a submitter like any other application and **no LLM sits in the delivery path**. Four protocol details that otherwise fail silently are handled explicitly: a request with no `id` is a notification and must never be answered, the client's `protocolVersion` is echoed back, tool failures return `isError` results rather than JSON-RPC errors, and the stdio scanner buffer is raised to 8 MiB so a pasted log body cannot truncate and desynchronise the stream.
- **Packaging hygiene**: the token file is refused unless mode 600, config lives in `$XDG_CONFIG_HOME` rather than beside the binary, the launchd plist is generated rather than committed (no home directory or Slack member id in a public repo), and the Homebrew `service` block lives in `formula_includes` because the release automation regenerates the formula and would silently clobber a hand edit. **39 new tests**; +3,485/−3.

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — Config Anchoring and Alerting (3 commits, v0.10.0)

- **Config resolution independent of the install prefix** (see Tough Challenges): `$YOUTUBE_CHANNELS_FILE` → `$XDG_CONFIG_HOME/ytt/channels.yaml` → the dev-checkout copy, with the scheduler plist pinning the first. A missing config is promoted to a **hard failure when cursor state proves channels previously worked** — an orphaned config is a regression, not a preference — while a genuinely playlist-only setup stays silent.
- **Alerting (🎯T11)**: webhook read from a mode-600 file outside the repo and refused if group-readable, dedup by problem digest, re-alert windows, one `RECOVERED` notice, silence when healthy, and notification failure never changing the run's exit status.
- **Delivery that does not depend on how the run was invoked**: draining the v0.10.0 backlog produced a run that correctly judged itself unhealthy and alerted — with a banner and no DM, because the DM target was readable only from an environment variable the scheduler sets and an ad-hoc run does not. Also fixed an inert notification button: an `osascript` notification posts on behalf of Script Editor with no click handler and no surviving process, so its **Show** button is inert *by construction*; switching to `terminal-notifier`, which posts from its own bundle, makes clicking open that run's log. **37 new bats cases**; +1,257/−50.

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Chat UI at Scale (7 commits)

- **🎯T55 → 🎯T57**: clamping, then the real fix in three layers — server replay bounded to 30 turns with a `history_meta` frame and a paged `/api/history`, client rendering of a 14-line preview so `marked.parse` and DOM construction run on the preview rather than the whole body, and an rAF-debounced coalescer. Live-verified against a scratch daemon replaying a copy of the owner's real 4,707-line chatlog.
- **Infinite scroll**: a zero-height sentinel with a 400 px `rootMargin` pages older windows and preserves scroll position on prepend; the observer tears down at the oldest message. Owner refinements followed live use — user previews are half the assistant's, and the newest message auto-expands while the previously expanded one reverts unless manually toggled.
- **🎯T58 overseer session resume**: the rotate-and-recap hack is gone (see Tough Challenges); a surviving subtlety is pinned by test — the MCP endpoint must be a concrete address, never `localhost`, which can resolve to `::1` while the loopback default binds IPv4. **4 new Go tests plus two Playwright oracles** (20 assertions); +1,022/−205.

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Semantic App Control (3 commits, v0.72→v0.73)

- **`hit_targets`** (🎯T109): `find_hit_target` matches id then role and never label, fails closed on disabled targets, and resolves coordinates through a documented preference order (`center_norm` → `bbox_norm` → `screen` → `bbox`) where a malformed `center_norm` is a hard "slice contract gap" rather than a guess. Packaged as a Starlark recipe that lists, finds, resolves, and taps.
- **`app_sensor_*`** (fine-grained authority): `app_input(type="accel")` is one-shot and CoreMotion overwrites it on the next frame, so sustained tilt was impossible. The shipped design is one concern per call — sticky `suppress` claims the stream without setting a value, `set` requires a prior suppress, `unsuppress` restores the device — after two intermediate API shapes were tried and discarded within the same change.
- **`app_metrics_*`** (🎯T110): five tools proxying ge's ring, each optionally targeting an `instance`, all failing closed with an explicit "app does not advertise" error when the app lacks the capability. **14 new tests**; +1,352/−20.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) · [marcelocantos/issuepipe](https://github.com/marcelocantos/issuepipe) · [marcelocantos/asc](https://github.com/marcelocantos/asc) · [marcelocantos/den](https://github.com/marcelocantos/den)

- **bullseye** (5 commits): the issuepipe consumer and its continuous poller, as in Significant Progress; mapping, opt-in and idempotency tests run without the feature flag so the default build stays free of the HTTP dependency. **7 new tests**; +888/−12.
- **issuepipe** (1 commit): authorisation resolved from the caller's GitHub token with a 60-second cache invalidated on 401, and tokens never persisted beyond the request. **3 new tests**; +700/−27.
- **asc** (2 commits, initial): the App Store Connect client described above, proving 9 first-time MultiMaze downloads over 30 days against Apple's UI, and capturing that App Manager access is insufficient for sales reports — a Sales or Finance key is required. **1 new test**; +1,369/−0.
- **den** (1 commit): the two silent-failure install bugs in Tough Challenges. Landed without a regression test, which is the week's one soft spot given both bugs are the recurring kind. +99/−25.

---

## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Scheduler Thrash and a Windows Gate (4 commits, v0.25→v0.26)

- **🎯T37 scheduler thrash**: three amplifying causes — the deferred-wake path bypassing wake-to-local, `steal_work` bouncing every steal through the global queue and unparking a second worker to race for it, and idle workers taking the global mutex on every park cycle merely to test emptiness. Fixed by extracting a shared `place_on_run_queue()`, converting stealing to direct local placement, and short-circuiting on an atomic `has_global_work_`. Victim scans now start at the thief's own id so idle workers stop convoying on the same processor.
- **🎯T38 non-channel performance ranking**: a deliberately investigation-only target producing paper 35 — channel `send/recv` at 149–150 ns (flat from 2 to 16 processors) sits far below spawn at 1.76–2.90 µs, net steady echo at 86–89 µs, and HTTP GET at 220 µs. The notable outcome is a defensible **"no large actionable opportunities"** conclusion with the residue declared and **zero follow-up targets filed** — including an honest "not measured, Darwin-only host" for the Linux comparison.
- **Docs hygiene**: `docs/todo.md` deleted (task tracking is bullseye-only), a 610-line WIP patch removed from the tree, `NOTICES` added. **3 new test cases** (13 assertions), one of which is a structural oracle asserting paper 35 actually documents each ranked surface and its verdict; whole-suite oracle stands at 767 cases / 26,522 assertions. +1,096/−1,074.

---

## Game Projects

### [squz/ge](https://github.com/squz/ge) — Textures, Metrics, Sensor Authority (6 commits, v0.80→v0.83)

Four tags in the window. Compressed-texture cook and load, the metrics ring, and the SDL3 recook are covered in Major Achievements; the remaining substance:

- **Sensor authority without breaking the constructional invariant** (🎯T109): the prior design deliberately had *no* arbitration in `pumpEvents`, because authority was constructional — the synthetic accelerometer only existed for a virtual device that declared no real one. Allowing a script to override tilt breaks that assumption. The fix needed three parts landing together: a sentinel `SDL_SensorID` so injected samples are distinguishable inside the event loop, mode-based filtering, and a per-pump **re-assertion** of the latched value so one call holds a tilt indefinitely without flood-injecting — rotated through the display orientation exactly like a real sample, and correctly skipped when the wire path already supplies screen-framed samples.
- **STABILITY snapshots**: ge's pre-1.0 interaction-surface catalogue — every public API, CLI surface, wire-protocol item and file format tagged Stable, Needs review, or Fluid — is the diffable baseline the release process audits against. The texture load surface was promoted to Stable this week. **16 new doctest cases** plus a standalone 12-assertion sensor harness; +2,578/−59 authored (204 further file changes in generated `headers/`/`prebuilt/` excluded from ☲).

### [squz/multimaze2](https://github.com/squz/multimaze2) · [squz/yourworld2](https://github.com/squz/yourworld2) · [squz/esfera2](https://github.com/squz/esfera2)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-07-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-26.md).*
## Web & Demos

### [marcelocantos/marcelocantos.github.io](https://github.com/marcelocantos/marcelocantos.github.io) — Demo Platform (10 commits, initial)

The site's entire life so far is one day. Beyond the shell/CLI architecture in Major Achievements:

- **Geometry as a pure module**: `shared/math.js` has zero DOM and zero Three.js imports specifically so it is unit-testable under `node --test`, and the tests import *the shipped module*, not a copy. Endpoint dragging is a genuine ray-cast — a pinhole ray from NDC intersected with the plane through the handle whose normal faces the eye — so a dragged endpoint stays at its own depth.
- **The cross-product demo asserts its own pedagogy**: the parallelogram spanned by `a` and `b` is drawn as a two-triangle buffer geometry, and the on-screen readout prints *measured* arrow-tip lengths alongside computed `|a×b|`, so the claim "the arrow length is the parallelogram area" is visibly falsifiable. An RHS/LHS toggle negates the result while preserving magnitude, naming the conventions (maths/OpenGL/Three.js versus DirectX/Unity).
- **Layout that WebGL cannot drive**: a `1fr` grid row sizes to intrinsic content and a canvas *has* an intrinsic size, so the renderer's backbuffer was driving panel height rather than the reverse, ratcheting the panel under the footer on each resize. Fixed with `minmax(0, 1fr)`, `min-height: 0`, and an absolutely positioned canvas, with resize measured from the layout box.
- **Browser oracle hooks**: demos publish state and setter functions on `window` so a driver can set inputs and assert on rendered geometry rather than pixels. **15 new tests**, all passing; +2,561/−666. Three.js is loaded from CDN via import maps — nothing vendored, no `node_modules`.

---

## Strategic Planning & Documentation

### [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) — Series Restamp and Exclude Fleet File (5 commits)

Published the 2026-07-13…19 report, then corrected its line stats and **restamped the entire series** to exclude `vendor/` and `node_modules/` from ☲, and introduced `data/line-excludes.yaml` as the single fleet-wide exclude configuration with a documented schema — so per-repo exclude rules never scatter into project repos. +4,192/−2,099 (report markdown, charts, and methodology).

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **marcelocantos/rustuml** — 0 landed, **278 commits in-flight** (+64k/−10k): the largest unmerged tranche in the fleet.
- **Health-Management-Systems/hms** — detail in [private week 2026-07-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-07-26.md)
---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-07-20…26. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **16** |
| Total landed commits | 63 |
| Total lines added (landed, filtered) | +27,321‡ |
| Total lines removed (landed, filtered) | −6,516‡ |
| Net new lines (landed, filtered) | +20,805‡ |
| File changes | 393 |
| New files created | 166 |
| Bulk paths excluded from ☲ | +2,877 / −1,211 (ge `headers/`+`prebuilt/`, csp `dist/`, lockfiles, `bullseye.yaml`) |
| Releases published | 10 across 5 repos (ge ×4, csp ×2, spyder ×2, ytt, blurter) |
| Languages | Go, C++, Objective-C++, C, Rust, Python, JavaScript, Bash, Starlark, TLA+, PowerShell, JSON Schema, GNU Make, YAML, Markdown |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs — six of which were added this run (see the honesty note). Generated amalgamations, lifted header mirrors, LFS prebuilts, lockfiles, and the bullseye ledger no longer score as authorship.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [marcelocantos/marcelocantos.github.io](https://github.com/marcelocantos/marcelocantos.github.io) | 10 | 35 | +2,561 | −666 | +1,895 |
| [marcelocantos/writ](https://github.com/marcelocantos/writ) | 8 | 76 | +5,192 | −701 | +4,491 |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 7 | 19 | +1,022 | −205 | +817 |
| [squz/ge](https://github.com/squz/ge) | 6 | 40 | +2,578 | −59 | +2,519\* |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 5 | 6 | +888 | −12 | +876 |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 5 | 68 | +4,192 | −2,099 | +2,093 |
| [marcelocantos/blurter](https://github.com/marcelocantos/blurter) | 4 | 23 | +3,485 | −3 | +3,482 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 4 | 32 | +1,096 | −1,074 | +22\* |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 3 | 25 | +1,352 | −20 | +1,332 |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 3 | 16 | +1,257 | −50 | +1,207 |
| [marcelocantos/asc](https://github.com/marcelocantos/asc) | 2 | 15 | +1,369 | −0 | +1,369 |
| [squz/esfera2](https://github.com/squz/esfera2) | 2 | 5 | +296 | −363 | −67 |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 1 | 3 | +99 | −25 | +74 |
| [marcelocantos/issuepipe](https://github.com/marcelocantos/issuepipe) | 1 | 5 | +700 | −27 | +673 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 1 | 16 | +711 | −801 | −90 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 1 | 9 | +523 | −411 | +112 |

\* *ge's figures exclude 204 file changes of generated `headers/` and LFS `prebuilt/` churn; csp's exclude the auto-generated `dist/` amalgamation, which mirrors every `src/` edit. Both are new excludes this week.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/blurter](https://github.com/marcelocantos/blurter) | 39 | drain, policy, and MCP protocol conformance — whole repo is new |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 37 | bats cases for config resolution, health gating, alert dedup |
| [marcelocantos/writ](https://github.com/marcelocantos/writ) | 36 | schema validation, seatbelt profile, security regressions, sneaky-delete oracle |
| [squz/ge](https://github.com/squz/ge) | 16 | texture load, metrics ring, app-channel, button hit targets (+12-assertion sensor harness) |
| [marcelocantos/marcelocantos.github.io](https://github.com/marcelocantos/marcelocantos.github.io) | 15 | pure-geometry assertions against the shipped module |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 14 | metrics dispatch, target resolution, Starlark helper |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 7 | event-id stability, strict opt-in, idempotency, 403 isolation |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 4 | MCP server spec, chatlog tail/range (+2 Playwright oracles, 20 assertions) |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 3 | paper-35 structural oracle + shipped-path smoke (13 assertions) |
| [marcelocantos/issuepipe](https://github.com/marcelocantos/issuepipe) | 3 | token scoping, isolation, bearer parsing |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 2 | eleven-series contract and per-instance isolation |
| [marcelocantos/asc](https://github.com/marcelocantos/asc) | 1 | download-kind filtering and unit summing |
| **Total** | **177** | landed only; counted from diffs, cross-checked by running the suites |

### Daily Activity

![Daily active repositories](daily-activity-2026-07-26.svg)

*(All-repo active-repository counts per day. Plotted: Mon 07-20 2, Tue 07-21 3, Wed 07-22 1, Thu 07-23 1, Fri 07-24 0, Sat 07-25 6, Sun 07-26 8. The distribution is the most weekend-loaded of the series so far — Friday is empty, and two-thirds of the week's repositories were touched on the final two days, when the ge release train, the csp scheduler work, and blurter's entire lifetime all landed.)*

---

## Ideas & Innovations

### Policy as the Shape of the World ([marcelocantos/writ](https://github.com/marcelocantos/writ))
Declared-intent security is not new — SELinux and AppArmor profiles are literally "this program will read A and write B" — and it has always died of *authorship burden*: nobody writes the profiles. writ's wager is that this constraint has quietly expired, because **an LLM caller emits a manifest for free**. The caller that was too expensive to exist for thirty years is now the default caller. What follows is Plan 9-flavoured: policy is not a filter evaluated at call time but the shape of the world the process wakes up in, so there is no expansion step to sneak past and no decision point to race. The child runs unmodified and simply finds that undeclared things are not there.

### The Declared-Versus-Actual Diff as an Injection Detector ([marcelocantos/writ](https://github.com/marcelocantos/writ))
The audit half of writ is the more interesting half. Prompt-injection detection is hard mostly because there is no baseline: a request to read a file looks identical whether the user asked for it or a poisoned document did. A manifest supplies exactly that missing baseline. **A process that declared it would edit `*.c` under `src/` and then reaches for `~/.ssh` has not merely violated a rule — it has produced the highest-signal injection alarm available anywhere in the stack.** Enforcement never depends on the audit (seatbelt and the proxy are the line, and the no-root path degrades to a clean "audit skipped"), so the detector is pure upside.

### Recording Delivery Only After a Sink Confirms ([marcelocantos/blurter](https://github.com/marcelocantos/blurter))
blurter exists because of a specific, humbling bug: a notifier recorded an alert as *sent* on the attempt rather than on confirmation, so an alert raised during a network outage was dropped **and then suppressed by its own dedup** — permanent silent loss, precisely when it mattered most, for a fortnight. The inversion is small and total: **submission is a durable local write that cannot fail on network, and delivery state is written only after a sink says yes.** A related decision is backed by measurement rather than opinion — a headless agent had its Slack connector available in one of six invocations, which disqualifies an LLM from a path that must work while things are broken. The MCP surface still ships; it just spools like everyone else.

### Bounding What the UI Materialises, Not What the Log Stores ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
The chat performance fix had an easy wrong answer available — trim the history — which would have traded a durability guarantee for frames per second. Instead the journal is untouched and every bound is placed on *materialisation*: the server replays 30 turns and pages the rest, the client parses a 14-line preview and builds the full body only on demand, and the coalescer batches per animation frame. **The conversation remains complete; only the browser's working set is finite.** That the honest successor problem — true node virtualisation for unbounded histories — is left explicitly open rather than declared solved is part of the same discipline.

### A Metrics Ring Because Logging Changed the Answer ([squz/ge](https://github.com/squz/ge), [marcelocantos/spyder](https://github.com/marcelocantos/spyder))
The frame-metrics ring was not built because telemetry seemed nice; it was built because diagnosing a carousel hitch on a slow Android device by logging per frame **perturbed the very timing under investigation**. The design follows from that: per-frame capture is a single guarded assignment with no serialisation until dump, the ring is bound to a game instance rather than a global, and the whole surface compiles out in release. The observer effect is the requirement, and an agent can arm a named subset of series, run a scenario, and pull the full retained history afterwards.

### Addressing UI by Identity, Never by Label ([marcelocantos/spyder](https://github.com/marcelocantos/spyder), [squz/ge](https://github.com/squz/ge))
Automation that taps pixel coordinates breaks on every layout change, and automation that matches visible text breaks on translation. The `hit_targets` contract resolves by **id first, then role, and refuses to match the display label at all** — the error message says so explicitly rather than leaving it as folklore. Two adjacent choices make it robust: `setHitRect` sets the interaction rectangle and the exported bounds from one value so the two cannot drift, and a disabled target is an error rather than a tap into the void, so a test that "passes" against a dead button is not possible.

### Two Tiers of Windows CI, One of Them Trusted ([marcelocantos/csp](https://github.com/marcelocantos/csp))
The instinct when a platform is flaky is one heroic CI job; the result is usually a required check everyone learns to re-run. csp split the concern instead: a cheap cloud job runs a curated smoke over 16 core units in seconds and is explicitly **not** a required check, while the authoritative gate is a local ARM64 VM that refuses to run on an unpushed `HEAD`, clones the exact SHA, and reads pass/fail from an **in-band marker in stdout** rather than trusting ssh to propagate an exit code. The harness itself had been lying — verbose test output through a redirected pipe on a slow VM disk is indistinguishable from a hang — and fixing the measurement had to come before the bugs it was hiding could be seen.

### Testing Geometry by Refusing to Import a Renderer ([marcelocantos/marcelocantos.github.io](https://github.com/marcelocantos/marcelocantos.github.io))
A 3D demo is usually verified by looking at it. Here the pure geometry lives in a module with **zero DOM and zero Three.js imports**, so `node --test` can assert `i×j = k`, anticommutativity, perpendicularity, and that ray-plane intersection error stays under 1e-8 — against the shipped module, not a copy. The complementary half is equally deliberate: the demo publishes its state and setters on `window` so a browser driver can set inputs and assert on *rendered* geometry. The bug this caught is the one that matters — arrows that silently stopped tracking `|a×b|` would have made the demo's entire pedagogical claim false while still looking fine.

---

## Effort Estimate: Traditional vs. AI-Assisted

A founding week more than a platform week: three projects went from nothing to working (one of them released and tapped the same day), and much of the remaining effort went into making failures *visible* — a silent outage, a silent alert loss, a silent install no-op, a sandbox that silently over-permitted. Shipping density stayed high with ten releases across five repos.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| writ MVP + schema v1 + confinement hardening | 4-6 | SBPL is undocumented Scheme with symlink-duality traps; a CONNECT-bridging egress proxy, Endpoint Security audit streaming, and adversarial self-red-teaming are four unrelated specialisms, and the failure mode of getting any of them subtly wrong is silent over-permission. |
| ge textures + metrics ring + SDL3 recook + sensor authority | 3-5 | Texture compression across ASTC/ETC2 with backend capability probing and mip-chain upload; a lock-free-in-spirit per-instance ring that must not perturb frame timing; four-platform static SDL builds and xcframework assembly; and sensor arbitration that preserves an existing constructional-authority invariant. |
| csp scheduler thrash + Windows gate + paper 35 | 2-3 | Scheduler mutex discipline is easy to get subtly wrong and hard to measure honestly; the fix required proving a dual-lock could be deleted, with TLA+ specs updated alongside, plus untangling three stacked causes of a Windows hang including a lying harness. |
| blurter 0→v0.1.0 released | 1.5-2.5 | Durability semantics, a retry taxonomy that distinguishes transient from permanent, MCP protocol details that fail silently when wrong, and release/packaging hygiene — all in one day, ending at a working `brew install`. |
| marcelocantos.github.io demo platform | 1.5-2.5 | Screen-plane ray-casting for handle dragging, aspect-aware camera framing, a canvas that must not drive layout, and a shell/content split that keeps geometry unit-testable. |
| spyder semantic control surfaces | 1.5-2.5 | Wire protocol, MCP tools, Starlark helpers and recipes across three features, each failing closed against apps that do not advertise the capability. |
| jevons chat UI at scale + session resume | 1.5-2.5 | Diagnosing "hidden" versus "not done" across server, render, and streaming layers, then falsifying a long-held belief about a third-party CLI with a decisive experiment. |
| ytt outage diagnosis + alerting layer | 1-2 | Sixteen days of green-but-empty runs, root-caused to install-prefix path derivation, then closing the class with single-exit-path alerting and a liveness backstop that fires on a non-event. |
| bullseye + issuepipe issue event path | 1-1.5 | Authorisation mirrored from GitHub with no local ACLs, existence-non-disclosure on 403, idempotent mapping, and a responsive continuous loop behind an optional feature flag. |
| Game downstream: lighting, parallax, metrics, DX truth | 1-2 | An oscillation whose cause is that the measurement invalidates itself, a fixed-timestep port bug visible only on slow devices, and a documentation correctness pass across three repos. |
| asc App Store Connect client | 0.5-1 | ES256 JWT minting, gzip-TSV report parsing, and the product-type domain knowledge without which the numbers are quietly wrong. |

### The Diversity Tax

This week spans Go (writ, blurter, jevons, spyder, issuepipe), Rust (bullseye), C++ and Objective-C++ (ge, csp, the games), Python (asc, the demos CLI), JavaScript and WebGL (jevons UI, the demo platform), Bash and bats (ytt), Starlark (spyder recipes), TLA+ (csp), PowerShell (Windows CI), JSON Schema, and macOS-specific surfaces — seatbelt/SBPL, Endpoint Security, launchd, CoreMotion, and the App Store Connect API. No single engineer holds sandbox policy compilation, M:N scheduler internals, texture-compression pipelines, and Apple store telemetry at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| writ | 3-5 | Deciding the product boundary (no policy engine, no LLM in the module), judging which fail-closed gaps were acceptable to ship, and directing the adversarial probe of the just-shipped sandbox. |
| ge / spyder / games | 3-5 | On-device tilt and texture verification, release judgement across four ge tags, feel judgement on parallax, and accepting the one-way lighting-quality trade. |
| jevons / ytt / blurter | 3-5 | Live use of the chat UI against a real history, spotting the missing DM on a backlog drain, and the call to keep an LLM out of the delivery path. |
| csp / bullseye / asc | 2-4 | Interpreting scaling curves, blessing the two-tier Windows gate, and cross-checking store units against Apple's own UI. |

### What If It Were One Person?

The naive expert band above sums to roughly 19–31 person-days, but a single generalist would not get that rate. They would pay ramp-up on seatbelt policy compilation, texture-compression toolchains, M:N scheduler internals, Endpoint Security streaming, and the App Store Connect API — five unfamiliar domains in one week — and then a heavy context-switch tax, since the same week founded three projects, cut ten releases, and diagnosed four distinct silent-failure bugs in unrelated systems. Calendar time stretches further than the expert-days band suggests; the specialist-team figure is lower precisely because the ramp-up disappears when the right person already knows the domain.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~16-26 person-days (~0.8-1.3 months)** |
| Specialist team (traditional) | **~10-17 person-days (~0.5-0.85 person-months)** |
| Actual human effort this week | **~12-20 hours (~1.7-2.8 person-days)** |
| **Multiplier vs. generalist** | **~30-50x** |
| **Multiplier vs. specialist team** | **~18-32x** |

The multiplier runs highest on writ, where a working confinement layer plus its own red team landed in four days across four unrelated specialisms, and on the silent-failure diagnoses — the ytt outage, the den install no-ops, the jevons session belief — where the expensive part is *noticing*, and an agent that reads its own history and cursor state notices faster than a human reading green logs. It runs lowest on the ge version bumps in consumer games and the documentation truth pass, which are mechanical once the contract is written. Human contribution concentrated where judgement cannot be delegated: what writ should refuse to do, whether a fail-closed gap is honest enough to ship, how tilt should feel on a real phone, and whether an alert path is allowed to depend on anything cleverer than a file write.

# Weekly Progress Report — 2026-10-05…11

## Executive Summary

**Thirteen repositories** landed **136 commits**. **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** v0.49.0–v0.51.0 (55 commits) carries a host `RequestID` on the broker wire, stamps `TurnID` / `FragmentSeq` / `Final` on OMP events, and refuses a payload that does not correlate. **[marcelocantos/sentinel](https://github.com/marcelocantos/sentinel)** (18) attributes disk fill to a per-volume size trie fed by FSEvents, with the root observer on stdio and Touch ID actually offered. **[marcelocantos/xbnf](https://github.com/marcelocantos/xbnf)** (8) made the arr.ai grammar's trees and greediness match wbnf; a leaf alternation cut `perf/scale/join.arrai` from 7.8 s to 84 ms. **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** (37) routes the Android app channel over `adb reverse` and serves a dismissed Verify run by stable link. **[marcelocantos/vellum](https://github.com/marcelocantos/vellum)** v0.26.0 vendors KaTeX instead of fetching it. HMS paired visual oracles and yourworld2 HUD oracles remain unmerged: [private week 2026-10-11](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-10-11.md).

**136 commits** | **<span style="color:#1a7f37">+14,870</span> net lines** | **~45-70 person-days traditional equivalent** | **~25-40x multiplier**

> Honesty note: **new `data/line-excludes.yaml` glob this run** — `marcelocantos/xbnf` `fromwbnf/testdata/arrai/stdlib/**` (pinned arr.ai stdlib for the tree oracle, +352). Headline ☲ is gather `landed:` after that adjustment, recomputed for xbnf only; the fleet `gather.sh` was not re-run. **<span style="color:#1a7f37">+15,866</span>/<span style="color:#cf222e">−996</span>**. Excluded bulk this week **+7,777/−2,062** (standing globs plus the new stdlib pin). KaTeX `.woff2` files are binary and do not enter ☲. Two of the thirteen repos are the report series publishing last week; their `reports/**` and `docs/**` stay excluded.

### Major Achievements & Innovations

- **Request identity on the wire** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.49.0–v0.51.0) — the host mints a durable `RequestID`; Claudia carries it on broker sends and provider events. An OMP sidecar turn has `TurnID`, per-turn `FragmentSeq`, and a daemon-authored `Final` fragment. A payload that does not correlate is refused. Three tags. Bare Claude and Codex seats route to OMP; Codex control is refused.
- **KaTeX never leaves the binary** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum) v0.26.0) — stylesheet and fonts ship inside the process (`embed/katex`, `scripts/vendor-katex.sh`). A converted page does not fetch a CDN. pptx slide text is matched across pandoc's per-token code runs.

### Significant Progress

- **Disk fill named while it happens** ([marcelocantos/sentinel](https://github.com/marcelocantos/sentinel)) — a size trie per volume, an FSEvents observer that only streams events and walks when asked, growth alerts that name path, delta, size, and a partial mark. The root process stays on stdio; scheduling and alerts stay in `sen`. No tag.
- **arr.ai trees, not accept/reject** ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf)) — `fromwbnf` compares adapted trees against wbnf. A capture nests a named node instead of renaming it; a wrap-around stack tail is greedy, as in PEG; lookaheads are memoised and FIRST-checked; `Compiled.Parse` is safe to call concurrently (🎯T28). Go directive pinned at 1.25.0 so arr.ai's CI can build it. No tag.
- **USB app channel, and a Verify link that survives dismiss** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)) — Android app traffic goes over `adb reverse` and binds loopback, with a per-serial LAN exception where USB reverse is restricted. A `#verify/<id>` link opens a dismissed run read-only. Homebrew ships the stream player. `devicectl` foreground-launch was evaluated and rejected. No tag. The disposable iOS Local Network fixture compiles; the device journey is still blocked on Xcode provisioning.
- **Native photo picker on the backup clone** ([marcelocantos/jevons-mobile](https://github.com/marcelocantos/jevons-mobile)) — one `image_picker` path for the iOS composer channel and the Android HTML chooser; the page hears `jevons-picked-image`. The only local checkout is `jevons-mobile.pre-merge-backup`, which has no git remote. Not a release.

### Tough Challenges Overcome

- **`sudo -n` never offers Touch ID** ([marcelocantos/sentinel](https://github.com/marcelocantos/sentinel)) — non-interactive sudo returns before PAM runs, so `pam_tid` never prompts. The root observer authenticates in-process; `make pin-observe` then pins the passwordless rule to this binary's sha256, and a pre-existing unrelated drop-in no longer fails the target after the rule is in place.
- **The observer filled its own growth ring** ([marcelocantos/sentinel](https://github.com/marcelocantos/sentinel)) — saving the size trie on the watched volume fed another FSEvents event. A uid of 0 had also been dropped from the hello line. The server skips its personal directory, accumulates nonzero fill instead of replacing it, and applies events that arrive during a reconcile after the walk result.
- **A capture renamed the node the compiler dispatches on** ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf)) — `name=` of one node renamed it, so `std=IDENT` was a leaf called `std` with no trace of `IDENT`. A capture now names only an anonymous node; a node that already has a rule or capture name gets a seq wrapper, on both the GLL path and the DFA walk.
- **Ordered choice inside a leaf** ([marcelocantos/xbnf](https://github.com/marcelocantos/xbnf)) — Go's regexp backtracks, so wbnf's `\((?:<|<>)\)` matches `(<>)`. The converter's `|>` committed to `<` and failed. Emitting `|` inside leaves takes the longest match, which agrees for every leaf in arr.ai's grammar, and removes the stacked negative lookaheads that made `join.arrai` take 7.8 s.
- **Enter on the trust dialog was No** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — the tmux walker confirmed Claude's trust prompt with Enter, which selected "No, exit". It now walks to "Yes". Separately, ChatGPT's relocated Codex CLI is found on disk, and providers that cannot start are the ones left skipped.

### Contributors

- Marcelo Cantos (AI co-authors — Claude, Grok, Cursor, Codex — on trailers throughout).

---

## Agent & Fleet Infrastructure

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Request Identity (55 commits, v0.49.0–v0.51.0)

**The biggest landed effort of the week.** 125 file changes, <span style="color:#1a7f37">+5,571</span>/<span style="color:#cf222e">−315</span>. **~78 new `func Test`**. Continuation of last week's sidecar: the process lifetime was already sealed; this week the events inside it become addressable.

- **Correlation (🎯T179–T186)**: Jevons mints a host-durable `RequestID`; Claudia carries it on the broker wire and on an explicit send-scoped API, including across backend retries. Sidecar answer events carry the turn. The daemon authors the final fragment and the per-turn sequence. Uncorrelated payloads are refused. A fail-closed check ties `RequestID`, `TurnID`, and `FragmentSeq`, with a degraded indicator when they disagree.
- **Three tags**: v0.49.0, v0.50.0, v0.51.0. `Resolve` takes an owner band override and a catalog slack tie-break (`TieBreak` crosses the broker wire, with a typed tie error). `ShouldRemintMigrate` is destination-independent. One Claudia entry point decides and executes seat migration; a destination is loaded, never adopted. A sidecar seat publishes its own tool calls. `CapabilityMCPTools` and `Steerable()` are the steerability jevons consumes.
- **Plan usage**: Claude's spend / `extra_usage` block maps into `PlanUsage`. Codex `wham/usage` credits that arrived unparsed now do too. Per-candidate rejection reasons are recorded; the broker log tees to a file.
- **Seats and grants**: a Claudia-native per-seat provider policy store. OMP seats whose host tools are absent from the bound model tools are refused. Stale hosted MCP HTTP origins are replaced on a fresh grant. An owner-approved legacy grant inventory is pruned once; three personal-work seats are excluded from that cleanup. Bare Claude and Codex seats route to OMP, and Codex control is refused.
- **Host edges**: tmux trust dialog walks to "Yes". Codex CLI is found after ChatGPT moved it. `make live` is serialised across the host with a durable lock (🎯T88). `pre-push` skips `refs/backup/*`. A design note maps the legacy CLI seat transport (🎯T177) before it is removed; three follow-up commits that delete the Task CLI backends are still unmerged.

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — USB Reverse, Verify Links (37 commits)

81 file changes, <span style="color:#1a7f37">+2,417</span>/<span style="color:#cf222e">−139</span>. **~24 new `func Test`**. No version tag.

- **Android app channel**: USB devices route over `adb reverse` and bind loopback by default. A per-serial LAN exception covers OEMs that restrict USB reverse. Listener connectivity is exposed as diagnostics. An opt-in physical app-channel oracle recorded a failed app dial; the app-UID limitation is documented.
- **Verify after dismiss (🎯T147)**: a dismissed run is served by stable link; `#verify/<id>` opens a non-live run read-only, including a committed real-browser test. The system-alert tap is guarded by the expected title before it answers.
- **iOS process list**: terminate recovery from a transient DTX process-decode failure. `terminateExisting` is not activate — appservice launch keeps `terminateExisting=false`. An app-channel sweep waits on a ping barrier before it drains. `SPYDER_ADDR` no longer clobbers the supervised daemon's remembered listen address. `--all-physical` fans install and deploy out.
- **What did not ship**: `devicectl` foreground-launch evaluated and rejected (🎯T105). Disposable iOS Local Network permission fixture compiles and is safe to run; the device journey is blocked on Xcode provisioning (🎯T154). Player vendor submodule object-store alternates detached. Patched `go-ios` pin bumped to fix a `quic.Connection` build break. Homebrew packaging ships the stream player artefacts (🎯T102).

### [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) — Disk Trie (18 commits)

56 file changes, <span style="color:#1a7f37">+4,799</span>/<span style="color:#cf222e">−171</span>. **~35 new `func Test`**. No tag. The owner rejected third-party indexers: `duc` is a batch snapshot, and there is no APFS live size index to call.

- **Attribution (🎯T7)**: a size trie per watched volume. The root observer is a stdio child that streams filesystem events and walks only when `sen` asks. Whole volumes, defaulting to the volume that holds `~`; unreadable paths recorded; walk stops at mounts. Growth snapshots and alerts name each grown path with delta, current size, and a partial mark. Volume-watcher liveness is in runtime status. Disk state is supplied to deep Jevons reviews.
- **Honesty of the delta**: the observer's own writes are ignored (a uid of 0 had been dropped, and saving the trie on the watched volume filled the ring). Nonzero fill accumulates. A reconcile seeds sizes and is not itself growth; events that arrive during the walk apply after it. A second reconcile waits until published paths are restored, so a later grow is the difference.
- **Pin-observe**: `sudo -n` returns before PAM, so Touch ID never appeared. The helper prompts in-process, then `make pin-observe` records this `sen`'s sha256. The fragment is checked on its own before install, so an unrelated pre-existing drop-in cannot fail the target after the rule is in place. Passwordless observe fails closed on a replaced binary.
- **Fleet stoppage**: an alert when plan policy stops the fleet. Healthy Jevons probes skip a routine model turn. Owner-parked agents are classified in the cheap probe. A broker-rejected health task is retried on another provider.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — 1.0 Judgment (2 commits)

2 file changes, <span style="color:#1a7f37">+105</span>/<span style="color:#cf222e">−113</span>, all in `STABILITY.md`. The settling clock is retired as the 1.0 gate. The agent's judgment is recorded in its place. No product code, no tag.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — 1.0 Judgment (2 commits)

2 file changes, <span style="color:#1a7f37">+61</span>/<span style="color:#cf222e">−28</span>, all in the stability notes. Same retirement of the pre-1.0 surface-settling rule, and the agent's 1.0 judgment. No product code, no tag.

### [marcelocantos/skills](https://github.com/marcelocantos/skills) — /stability (1 commit)

3 file changes in the headline, <span style="color:#1a7f37">+160</span>/<span style="color:#cf222e">−18</span>. The authored addition is the `/stability` skill. The same sync copied a third-party Google Workspace skill tree under `skills/synced/**`, excluded from ☲ (<span style="color:#1a7f37">+2,690</span>/<span style="color:#cf222e">−19</span>).

### [marcelocantos/serviceboard](https://github.com/marcelocantos/serviceboard) — Sample Paths (1 commit)

Personal paths in the Supervisor sample config replaced (2 files, <span style="color:#1a7f37">+8</span>/<span style="color:#cf222e">−6</span>).

---

## Libraries & Documents

### [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) — arr.ai Tree Oracle (8 commits)

32 file changes after the new stdlib exclude, <span style="color:#1a7f37">+930</span>/<span style="color:#cf222e">−92</span>. **~5 new `func Test`**, one of them a tree oracle with a fixed probe list. Pinned stdlib <span style="color:#1a7f37">+352</span> is footnoted, not in ☲.

- **Tree oracle**: `TestConvertArraiTree` parses every input with wbnf and with the converted grammar and compares adapted trees. Named captures and rule names bracket their children; literals are text; a single stack level collapses; `@choice` and `@skip` are left out because arr.ai reads neither. Probes include `let x = 1; x + x`, `\x x + 1`, `{1} (<>) {2}`, `a if b else c + 1`, and a `{: … :}` macro body. `BenchmarkArrai` keeps xbnf within 5× of wbnf (the Phase 0 bound is 10×). `SOURCES.md` records the pin; the stdlib files themselves are excluded.
- **Shape**: a capture nests; it does not rename. An external reference's span is a leaf. A DFA state is not accepting merely because it carries a capture label — that had parsed arr.ai's current-value `.` as a `get`. Golden fingerprints change only in node count.
- **Greedy stack tail**: arr.ai's tightest level ends in `@`, which wraps to the loosest (`"let" pat "=" @ ";" @`). wbnf treats that `@` as greedy, so `let x = 1; x + x` is one let. xbnf had dropped the stack fallback whenever a looser operator competed and produced `(let x = 1; x) + x`. A fallback whose tighter level can end in a self-reference to the stack top is marked greedy at compile time and beats the level's own productions for the same span, after `#priority` and `#prefer`, before `#avoid`.
- **Lookahead cost**: ordered choice lowers to nested negative lookaheads. On arr.ai's bottom level (seventeen alternatives) that was the remaining super-linear cost. A lookahead has no capture context, so the answer is memoised per nonterminal and position, and a FIRST-set pre-check answers most of them from one byte. `perf/corpus/csvetl/inline.arrai` is now faster than wbnf.
- **Leaf alternation**: `|` inside a leaf, not `|>`. `(<>)` and `(<>=)` become reachable, and `join.arrai` goes from 7.8 s to 84 ms because the leaf compiles to one DFA.
- **Concurrency (🎯T28)**: ASCII transition table and memoised start state are atomic pointers; the state memo and rune maps take a mutex on the miss path; the tree walker lives on the per-parse chart. `TestConcurrentParse` runs eight goroutines against a sequential fingerprint. `go` directive is 1.25.0 so arr.ai's CI, which pins 1.25, can build the module. CI installs `cmark` so CommonMark tree fixtures verify instead of failing the T25.1 lock as unverified.

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — Offline KaTeX (8 commits, v0.26.0)

61 file changes, <span style="color:#1a7f37">+1,181</span>/<span style="color:#cf222e">−75</span>. **~7 new `func Test`**. Fonts are binary and not in those lines.

- **🎯T30.6**: `scripts/vendor-katex.sh` embeds KaTeX's minified CSS and woff2 fonts. Converted maths does not fetch a CDN.
- **pptx**: slide text is matched across pandoc's per-token code runs, so a run boundary is not a missed string.
- **Confluence corpus**: a Playwright capture script and a small markdown layout set (tables, media, portrait SVG) for the converter. Authored fixtures, not a generated dump.
- **Stability**: settling-clock gate retired; the agent's 1.0 judgment recorded. 🎯T30.2, T30.7, and T30.9 retired, with the gate described as local rather than CI. `pr-workflow` skipped for the Colossus gated-push.

---

## Sites & Shells

### [canticode/canticode.github.io](https://github.com/canticode/canticode.github.io) — Company Pages (1 commit)

9 file changes, <span style="color:#1a7f37">+467</span>/<span style="color:#cf222e">−25</span>. About, Orthograph, contact, and privacy pages, plus a 404 and a shared stylesheet. Static HTML and CSS.

### [marcelocantos/jevons-mobile](https://github.com/marcelocantos/jevons-mobile) — Photo Picker (1 commit)

Landed on the only local checkout, directory `jevons-mobile.pre-merge-backup`, which has **no remote**. 5 headline file changes, <span style="color:#1a7f37">+132</span>/<span style="color:#cf222e">−0</span> after the `pubspec.lock` exclude (<span style="color:#1a7f37">+145</span>/<span style="color:#cf222e">−1</span> excluded).

- **`image_picker`**: `_pickImage` serves both the iOS composer message channel and Android's WebView file chooser (`_selectWebViewFiles`, including capture). The page receives `jevons-picked-image`. `Info.plist` gains the usage strings. `test/shell_test.dart` moves with it. Not pushed from this clone.

---

## Commercial

Nothing commercial landed on a default branch.

**[Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms)** — 273 in-flight commits, <span style="color:#1a7f37">+1,741,607</span>/<span style="color:#cf222e">−261,630</span> in gather's in-flight ☲. Subjects are paired legacy-vs-port visual oracles (referral, episode, journal voucher) and `Hms.Vcl` rendering fixes, with generated retranslation commits still in the same window. Not re-split into generated versus authored this run. Full narrative: [private week 2026-10-11](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-10-11.md).

**[squz/yourworld2](https://github.com/squz/yourworld2)** — 13 in-flight commits on the chore branch: HUD active-name, carousel level order, a production-path GPU render oracle for the face-user transform. Still unmerged. Same private companion.

**minicadesmobile** titles and **[squz/multimaze2](https://github.com/squz/multimaze2)** had no commits in this window. Stock Cars 3.26 remains the live store build from last week.

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **marcelocantos/jevons** — 340 in-flight. Subject clusters: owner-question routing, quiet routine worker reports, history-page anchors, Flutter keyboard Return policy, cost-switch degrade, and a held Task-CLI purge (🎯T1055) pending owner confirmation. Not read commit-by-commit.
- **Health-Management-Systems/hms** — 273 in-flight. See Commercial. Gather ☲ <span style="color:#1a7f37">+1,741,607</span>/<span style="color:#cf222e">−261,630</span> still includes generated retranslation.
- **arr-ai/arrai** — 16 in-flight. Closure comparison by function node and captured bindings; hoist of loop-invariant subexpressions; packrat memoisation of named-rule parses after a 243× backtracking blowup; native `//str.parse_number`.
- **squz/yourworld2** — 13 in-flight. See Commercial.
- **marcelocantos/den** — 11 in-flight. Linux bottle relocate: ELF interpreter and RPATH via patchelf, wrong-arch bottles rejected, keg cleanup limited to kegs den itself installed.
- **marcelocantos/sqldeep** — 7 in-flight commits, 0 file changes. Stash-index noise (`index on chore/hygiene-init`), not product.
- **marcelocantos/claudia** — 3 in-flight. Remove direct CLI Task backends and fail them before broker dispatch; the replacement OMP path is the refusal, not a new runner.
- **marcelocantos/csp** — 1 in-flight. Free PicoTLS certs and keys on `quic::listen` teardown.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-10-05…11. In-flight branch work is excluded by design. xbnf's pinned arr.ai stdlib is excluded via `data/line-excludes.yaml` and is not in the headline.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **13** |
| Total landed commits | **136** |
| Total lines added (landed, filtered) | <span style="color:#1a7f37">+15,866</span>‡ |
| Total lines removed (landed, filtered) | <span style="color:#cf222e">−996</span>‡ |
| Net new lines (landed, filtered) | <span style="color:#1a7f37">+14,870</span>‡ |
| File changes | 381 (summed per commit; a path touched twice counts twice) |
| New files created | 123 unique paths after the same excludes |
| Bulk paths excluded from ☲ | <span style="color:#1a7f37">+7,777</span>/<span style="color:#cf222e">−2,062</span> (standing globs + xbnf stdlib pin) |
| Releases published | **4** (claudia v0.49.0, v0.50.0, v0.51.0, vellum v0.26.0) |
| Languages | Go, TypeScript, Dart, Python, Swift, Ruby, HTML, CSS, Shell, Markdown, YAML, arr.ai |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. **New this run:** `marcelocantos/xbnf` `fromwbnf/testdata/arrai/stdlib/**` (+352). xbnf's headline was recomputed with that pathspec; other repos are gather's `landed:` lines unchanged. KaTeX fonts are binary and were never in ☲.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 55 | 125 | <span style="color:#1a7f37">+5,571</span> | <span style="color:#cf222e">−315</span> | <span style="color:#1a7f37">+5,256</span> |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 37 | 81 | <span style="color:#1a7f37">+2,417</span> | <span style="color:#cf222e">−139</span> | <span style="color:#1a7f37">+2,278</span> |
| [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) | 18 | 56 | <span style="color:#1a7f37">+4,799</span> | <span style="color:#cf222e">−171</span> | <span style="color:#1a7f37">+4,628</span> |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 8 | 61 | <span style="color:#1a7f37">+1,181</span> | <span style="color:#cf222e">−75</span> | <span style="color:#1a7f37">+1,106</span> |
| [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) | 8 | 32 | <span style="color:#1a7f37">+930</span> | <span style="color:#cf222e">−92</span> | <span style="color:#1a7f37">+838</span>* |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 2 | 2 | <span style="color:#1a7f37">+105</span> | <span style="color:#cf222e">−113</span> | <span style="color:#cf222e">−8</span> |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 2 | 2 | <span style="color:#1a7f37">+61</span> | <span style="color:#cf222e">−28</span> | <span style="color:#1a7f37">+33</span> |
| [canticode/canticode.github.io](https://github.com/canticode/canticode.github.io) | 1 | 9 | <span style="color:#1a7f37">+467</span> | <span style="color:#cf222e">−25</span> | <span style="color:#1a7f37">+442</span> |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 1 | 3 | <span style="color:#1a7f37">+160</span> | <span style="color:#cf222e">−18</span> | <span style="color:#1a7f37">+142</span> |
| [marcelocantos/jevons-mobile](https://github.com/marcelocantos/jevons-mobile) | 1 | 5 | <span style="color:#1a7f37">+132</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+132</span>† |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 1 | 3 | <span style="color:#1a7f37">+35</span> | <span style="color:#cf222e">−14</span> | <span style="color:#1a7f37">+21</span> |
| [marcelocantos/serviceboard](https://github.com/marcelocantos/serviceboard) | 1 | 2 | <span style="color:#1a7f37">+8</span> | <span style="color:#cf222e">−6</span> | <span style="color:#1a7f37">+2</span> |
| [marcelocantos/progress-reports-private](https://github.com/marcelocantos/progress-reports-private) | 1 | 0 | <span style="color:#1a7f37">+0</span> | <span style="color:#cf222e">−0</span> | <span style="color:#1a7f37">+0</span> |

\* *Pinned `fromwbnf/testdata/arrai/stdlib/**` excluded (+352 / 5 file changes). `SOURCES.md` stays in the headline.*

† *Commit `e27f825` is on local directory `jevons-mobile.pre-merge-backup`, which has no remote. `pubspec.lock` excluded. Not known to be on GitHub.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~78 | Added `func Test` lines: correlation, migration, grants, tie-break, livelock |
| [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) | ~35 | Trie, volwatch, pin-observe, disk deltas, plan-blocked |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~24 | adb reverse, diagnose, verify deep link, DTX terminate, fan-out |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | ~7 | KaTeX CSS embed |
| [marcelocantos/xbnf](https://github.com/marcelocantos/xbnf) | ~5 | Tree oracle, greedy stack tail, concurrent parse |
| **Total** | **~149** | Gross added test functions in the landed diff. In-flight tests are not included. |

### Daily Activity

![Daily active repositories](daily-activity-2026-10-11.svg)

*(Active repositories per day, landed commits: Mon 10-05 8, Tue 10-06 2, Wed 10-07 7, Thu 10-08 3, Fri 10-09 2, Sat 10-10 2, Sun 10-11 2.)*

---

## Ideas & Innovations

### A Payload That Does Not Correlate Is Not a Turn ([claudia](https://github.com/marcelocantos/claudia))

Once a sidecar can outlive a buggy broker, the next failure is an event that arrives with no owner. **The host mints a durable `RequestID`; Claudia only carries it; every fragment has a `TurnID` and a `FragmentSeq`; `Final` is daemon-authored; anything that does not match is refused.** Retries and reissues keep the same request identity, so a second attempt is not a second conversation.

### Growth Is a Trie of Deltas, Not a Batch Index ([sentinel](https://github.com/marcelocantos/sentinel))

`duc` can say what is large. It cannot say what grew in the last few seconds, and nothing in open source keeps a live APFS size index. **FSEvents adjust a per-volume trie; a walk `sen` itself runs is the reconcile; the observer does not schedule and does not alert.** The trie file lives off the watched tree, because the first version's save was a growth event that filled the ring.

### Greedy Where the PEG Is Greedy ([xbnf](https://github.com/marcelocantos/xbnf))

arr.ai's tightest operator level ends in `@`, which means "parse a looser level here". **A fallback that can recurse to the top of the stack is marked greedy at compile time and wins the span**, after priority and prefer, before avoid. Without that, `let x = 1; x + x` splits after the first `x`, and no grammar directive can say otherwise.

### Longest Match Inside a Leaf ([xbnf](https://github.com/marcelocantos/xbnf))

A regexp alternation backtracks when the rest of the pattern fails. Ordered choice does not. **Inside a leaf, the converter emits `|`, so the DFA takes the longest match — the one the regexp actually took — and the leaf is one automaton instead of a stack of negative lookaheads.** `(<>)` parses, and a file that took 7.8 s takes 84 ms, with the tree unchanged.

### USB Reverse, Not a LAN Hole ([spyder](https://github.com/marcelocantos/spyder))

An app on a phone reaches a developer's loopback by opening a port on the network, or by letting the USB daemon own the forward. **`adb reverse` plus a loopback bind is the default; a per-serial exception is the escape for an OEM that refuses USB reverse.** The failure mode stays on one device instead of becoming a subnet listener.

### Touch ID Is a Prompt ([sentinel](https://github.com/marcelocantos/sentinel))

`sudo -n` is documented as "fail if a password would be required". On this Mac it returns before PAM, so the Touch ID module never runs. **The observer requests the admin right in-process, where `pam_tid` can show UI, and only then installs a passwordless rule pinned to the binary's hash.** A later check of every drop-in is not the success test; the fragment is checked on its own, or a pre-existing file fails a rule that already installed.

---

## Effort Estimate: Traditional vs. AI-Assisted

A landed week of identity, disk attribution, and parser agreement, with a large unmerged cockpit and clinical port beside it. The public estimate covers landed work only. In-flight HMS and yourworld2 hours are not in the totals, matching last week's treatment of unmerged HMS.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| claudia request identity (v0.49–v0.51) | 8-12 | Host-minted id carried across retries; fail-closed fragment correlation; migration loaded not adopted; grant purge that must not touch personal seats. |
| sentinel disk trie + pin-observe | 6-9 | FSEvents size trie; stdio root observer; self-write exclusion; `sudo -n` versus `pam_tid`; hash-pinned passwordless rule. |
| xbnf arr.ai trees | 6-9 | Capture nesting; PEG-greedy stack tail; lookahead memo and FIRST; leaf DFA versus ordered choice; concurrent `Parse`. |
| spyder USB reverse + verify links | 5-8 | adb reverse and per-serial exception; DTX terminate; dismissed-run deep link; provisioning-blocked iOS fixture. |
| vellum v0.26.0 | 3-5 | Vendored KaTeX; pandoc per-token pptx runs; Confluence layout corpus. |
| Stability judgments (bullseye, mnemo, vellum notes) | 1-2 | Retire the settling clock; write the 1.0 judgment. No product code. |
| jevons-mobile photo picker | 1-2 | One picker for the composer channel and the Android chooser, on a clone with no remote. |
| canticode pages, /stability, serviceboard sample | 1-2 | Static company pages; skill text; sample paths. |

### The Diversity Tax

OMP correlation, FSEvents and PAM, GLL/PEG disambiguation, Android USB reverse, and offline maths rendering in one week. No single engineer holds broker wire identity, Touch ID policy, and scannerless greediness at once. The clinical port and the globe oracles were also moving, on branches, in specialisms this table does not score.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| claudia correlation and grants | 4-6 | Who mints `RequestID`; refuse uncorrelated; which grants the purge may drop; three releases. |
| sentinel disk and Touch ID | 3-5 | No third-party indexer; trie must not watch itself; `sudo -n` is the wrong prompt. |
| xbnf greediness and trees | 2-4 | Agree with wbnf's tree and with PEG greediness; keep the 7.8 s → 84 ms change only because the tree holds. |
| spyder devices | 2-4 | USB reverse as default; devicectl foreground-launch rejected; provisioning blocks the iOS fixture. |
| vellum KaTeX and pptx | 1-2 | Vendor the fonts; match text across pandoc runs; cut v0.26.0. |
| Stability notes | 1-2 | 1.0 judgment on bullseye, mnemo, and vellum; settling clock retired. |
| Photo picker, site, skills, serviceboard | 1-1 | Picker behaviour on both platforms; company pages; sample paths. |

### What If It Were One Person?

The expert band sums to roughly 31-49 person-days. Ramp-up on OMP wire identity, PAM versus sudo, and PEG stack tails would dominate a generalist's month before a line of the week's code was familiar. Landed activity ran every day (2–8 repos), heaviest on Monday and Wednesday.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~45-70 person-days (~2.3-3.5 months)** |
| Specialist team (traditional) | **~31-49 person-days (~1.6-2.5 person-months)** |
| Actual human effort this week | **~14-24 hours (~1.8-3.0 person-days)** |
| **Multiplier vs. generalist** | **~25-40x** |
| **Multiplier vs. specialist team** | **~15-30x** |

The multiplier is highest on xbnf's leaf alternation (the expensive step is knowing that `|` and `|>` disagree with regexp backtracking, not typing the emitter) and on sentinel's decision that a batch indexer is the wrong instrument. It is lowest on the company pages and the sample-config path edit. The human contribution concentrated on refusals: an uncorrelated fragment is not a turn, the observer's own write is not disk growth, `sudo -n` is not Touch ID, a backup clone is not a release, and a settling clock is not a 1.0 gate.

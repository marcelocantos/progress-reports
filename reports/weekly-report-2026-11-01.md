# Weekly Progress Report — 2026-10-26…11-01

## Executive Summary

**Twenty-nine repositories** landed **572 commits**. **[marcelocantos/den](https://github.com/marcelocantos/den)** shipped three GA releases (v0.14.0, v0.15.0, v0.16.0) and v0.17.0-rc.1 across 125 commits. It now installs and updates itself without Homebrew, builds from source in a sandbox under its own prefix, and will not upgrade into a package that upstream has disabled. **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** cut fifteen releases (v0.66.0–v0.80.0, 179 commits): persisted usage observations, Bash cancellation, plan-safe stops, a destructive-git guard for shared clones, and switch-time compaction. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** squash-landed a second usable-state train and replaced pull requests with a gated push whose gate runs in about eight minutes instead of two hours. **[marcelocantos/pigeon](https://github.com/marcelocantos/pigeon)** v0.34–v0.35 (87) brings the relay to Android over ngtcp2 through JNI, proven on a physical tablet. **[marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal)** moved to a corrected decimal kernel and a static playground. **[marcelocantos/finance](https://github.com/marcelocantos/finance)** gained a PocketSmith puller and an IG Markets adapter. Stock Cars 3.27 reached both stores: [private week 2026-11-01](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-11-01.md).

**572 commits** | **<span style="color:#1a7f37">+177,911</span> net lines** | **~87-133 person-days traditional equivalent** | **~20-60x multiplier**

### Major Achievements & Innovations

- **den installs without Homebrew** ([marcelocantos/den](https://github.com/marcelocantos/den) v0.15.0). Release binaries link a vendored static libarchive and need no Homebrew libraries (#112). `install.sh`, `den self-update --version` and a Homebrew-free `make verify-release` replace the formula (#113). The Homebrew release path (bottles, tapper, release-tap) is retired (#155), and the den formula is removed from the tap. `migrate-prefix` moves a legacy den home off Homebrew's prefix and leaves hard-coded-Cellar kegs with brew (#119, #125). A self-update replaces the binary on a fresh inode and restarts the daemon (#118).
- **Source builds under den's own prefix** ([marcelocantos/den](https://github.com/marcelocantos/den) v0.15.0–v0.16.0). Configure, build and install run inside a macOS write sandbox that denies Homebrew prefixes and `~/Library` (#129, #131). Opt-prefix builds stage through DESTDIR and fall back to a staging keg for install steps that ignore it (#127, #152). Every Mach-O file in the keg gets its linkage fixed (#128). Dependencies are planned and routed through fixed-Cellar opt links (#144), the bundled Ruby gets Homebrew's `Library/Homebrew` layout and `post_install` steps (#145, #150), and an unwatched single-source install is held back (#134).
- **Fifteen claudia releases** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.66.0–v0.80.0). Broker usage observations persist and replicate to subscribers, and expired broker credentials renew without a sign-in (v0.66). A hollow `length` stop is retried within the turn, then folds the conversation (v0.68–v0.70). An openai-codex seat's host tools are capped at 250 without dropping a consumer's own server (v0.71–v0.72). The broker enforces a two-file consumer fleet-intent and policy hold on boot resume, grant and adopt (T233). An interrupted turn kills the Bash process group (T235). A stop whose turn will not settle discards the seat (T239), and fleet-seat Bash refuses destructive git in a shared clone (T240). v0.80.0 adds compaction at switch time (T243).
- **Gated push replaces pull requests** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)). A squash of 2,280 branch commits (63375185) makes `make gate` attest the tree it measured, and the pre-push hook checks that attestation (🎯T1279). The gate runs its layers in parallel and the journeys as three shards, each with its own overseer, which cuts it from about 2 h to about 8 min (🎯T1299, 🎯T1302). `make land` squashes an attested branch onto master and refuses an unattested or stale tree (🎯T1312).
- **pigeon on Android over ngtcp2** ([marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) v0.34.0–v0.35.0). ngtcp2 and quictls are cross-built for a JNI AAR. A JNI-owned connection carries pairing and activation, and a Kotlin relay client is bound to it (🎯T66). A Pixel Tablet ran real pairing and an encrypted echo, checked byte for byte before the encrypted ACK. The AAR is published through JitPack under its corrected Maven coordinate, and a fresh-consumer smoke test checks each released Go module tag.

### Significant Progress

- **den refuses what upstream disabled** ([marcelocantos/den](https://github.com/marcelocantos/den) v0.16.0). `den install` and `den upgrade` refuse a disabled formula, cask or dependency unless `--force` is given (#177, #181). The daemon never auto-upgrades into one, records each blocker and when it was seen (#182, #184), and `--dry-run` reports exactly what a real run would do (#183). A `version_scheme` bump to a lower version is held, so openssl@3 3.6.3 is not "upgraded" to 3.5.9 (#163). The daemon builds its launchd PATH from den's own prefix and refreshes it at startup (#176, #190). v0.17.0-rc.1 retries index, GHCR, self-update and archive downloads (#198, #203–#205).
- **den v0.14.0 and the cask surface** ([marcelocantos/den](https://github.com/marcelocantos/den)). Uninstall stanzas (#68), font artifacts (#95), `command_wrapper` binaries (#96), `$APPDIR` and staged-path binaries (#89, #91), and Homebrew renames (#94) are supported. Downloads stream to disk with no 500 MiB cap (#92, #97). An mmap'd lookup cache makes `info`, `install` and `upgrade` about 30× faster (#72). `den pin` and `den unpin` were added (#78).
- **A decimal proposal with a working fork** ([marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal)). The proposal for built-in `decimal64` and `decimal128` now tracks a corrected BID kernel, a static playground on the fork (#3, #9), big-endian CI (#4), the zero value as `decimal64(0)` (#8), and decimal hardware with DPD on s390x and ppc64le (#11). It has a BSD 3-Clause licence and a deep-dive audit of how far the fork is from an upstream PR. The fork itself (114 in-flight commits) routes the runtime operators through `internal/bid` and checks them against Intel's `readtest.in` vectors.
- **Personal finance ingestion** ([marcelocantos/finance](https://github.com/marcelocantos/finance)). A read-only PocketSmith puller loads accounts, balances and transactions into the local ledger. A signed Go fetcher reads its key from the login keychain through Security.framework (#12). An IG Markets adapter downloads ledger PDFs and contract notes (#13). Bank fetch now drives the installed Firefox with a shared profile and waits for a human login (#10, #11).
- **spyder in the browser** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder)). A WebCodecs H.264 decoder plays the wasm glass in Chrome (🎯T101.5). Browser snapshots persist per game in IDBFS, a same-origin pairing link and QR code were added, and archived run screenshots are stored as lossy JPEG XL.
- **tapper across the fleet**. Thirteen repositories now publish their Homebrew formula with tapper instead of homebrew-releaser (Mon 26 Oct), and sentinel reads disk use from loadmon instead of running its own FSEvents observer (<span style="color:#cf222e">−4,250</span> lines).

### Tough Challenges Overcome

- **Homebrew's packages without Homebrew** ([marcelocantos/den](https://github.com/marcelocantos/den)). Formulae assume Homebrew's prefix, Ruby layout and environment, and some install steps write straight past DESTDIR. den gives the bundled Ruby the layout it expects, retries a DESTDIR-ignoring step into a staging keg, fixes Mach-O linkage across the keg, and sandboxes the whole build so a stray write fails instead of landing in another prefix.
- **Hollow replies from Codex seats** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia)). openai-codex seats returned empty `length` stops in per-session streaks. In-turn retries and folding contained the symptom (v0.68–v0.70), and the root cause was the number of host tools. The 250-tool cap fixed it, and T229 was set aside.
- **Buffered frames lost at FIN** ([marcelocantos/pigeon](https://github.com/marcelocantos/pigeon)). Closing an ngtcp2 stream dropped replies that were still buffered. The fix keeps buffered stream frames across FIN and close, serialises ngtcp2 I/O without blocking full-duplex streams, removes a session-close lock inversion, and gates the case in a tagged C SDK relay suite.
- **A two-hour gate** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons)). The landing gate was too slow to run before every push. Running layers in parallel, splitting journeys into shards, making isolates die with the suite, and replacing fixed 25 s waits with readiness checks brought it to about eight minutes, which made gated push practical.

### Contributors

- Marcelo Cantos (AI co-authors — Claude, Grok, Cursor, Codex — on trailers throughout).

---

## Agent & Fleet Infrastructure

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Fifteen Releases, Plan-Safe Stops (179 commits, v0.66.0–v0.80.0)

366 file changes, <span style="color:#1a7f37">+14,356</span>/<span style="color:#cf222e">−1,619</span>. **~223 added test declarations**.

- **Usage and credentials (v0.66)**: broker observations persist, subscriptions replicate, and one native query watch is kept across links. sqlpipe v0.34.0 is pinned. Cursor quota walls are typed as rate limits, and a test binary never starts an interactive login.
- **Hollow stops (v0.67–v0.72)**: Bash accepts a timeout of up to 600 s, a hollow `length` stop retries and then folds, and the Codex host-tool cap keeps consumer-owned servers.
- **Fleet intent (T233, v0.73–v0.74)**: an isolated broker usage fixture for Jevons journeys, then broker enforcement of `fleet/intent.json` and `fleet/policy-hold.json` on boot resume, grant and adopt.
- **Cancellation (T235–T239, v0.75–v0.78)**: Bash process groups are cancelled with the turn, a prompt after a mid-tool cancel gets a real reply, fleet signal commands are refused before the shell runs, an adopt's provider mismatch is decided by session and liveness, and a stop that will not settle discards the seat.
- **Shared clones and compaction (T240–T244, v0.79–v0.80)**: Bash refuses destructive git in a shared clone, including after a chained `cd` or `-C`. Anthropic rate-limit errors are typed. Switch-time compaction rolls back a switch that fails, including on ENOSPC. A synchronous `Registry.Compact` is gated but not yet released.

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Gated Push and Plan Safety (8 commits)

1,347 file changes, <span style="color:#1a7f37">+89,204</span>/<span style="color:#cf222e">−9,561</span> after the standing excludes and new globs for the Android widget's vendored native code. **~1,158 added test declarations**, mostly inside the squash. No tag.

- **Squash 63375185 (2,280 branch commits)**: gated push (🎯T1279), a parallel and sharded gate (🎯T1299, 🎯T1302), journey isolates that die with the suite (🎯T1294), a late abort that no longer swallows the owner's reply (🎯T1295), and a plan-policy park that ends the running turn (🎯T1305). It also carries the steer modes and stop guards, the Android plan-usage widget (🎯T1244), and the mined burn-profile line (🎯T1283, 🎯T1284).
- **Follow-up landings**: the landing veto now explains a kept worker to its parent (🎯T1310). The cockpit never relaunches an overseer that plan policy parked (🎯T1316). The kill guard kills only what you started (🎯T1296). Stray sibling worktrees are removed only after a `git cherry` proof (🎯T1311), and the T1300 replay-cassette core landed.
- **Overseer token burn (🎯T1339)**: sentinel repairs are logged instead of sent, backlog counts stay in bands, and the stale-lease page waits 30 minutes. The standing whole-module gate is fixed and paused behind `standing_gate.enabled`.
- Claudia pins moved v0.76.0 → v0.78.0 → v0.79.0.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Attested Push Gate (9 commits)

The push gate attests `make gate`'s tree and the pre-push hook checks it. Commit-mode concurrency oracles retry lock timeouts (T109), and the external-root sentinel test runs in its own binary (T110). T107 and T108 were filed: per-target executor and reviewer model preference, and external ledger discovery from worktrees.

### [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) — Disk Use from loadmon (1 commit)

<span style="color:#1a7f37">+517</span>/<span style="color:#cf222e">−4,250</span>. Sentinel now reads the disk-use census from loadmon's local API. The root FSEvents observer, journal, size trie and walker are deleted, since that observer needed a root password and never ran. A disk alert carries a three-level census excerpt of the home volume, labelled as allocated bytes. Tests stub loadmon and the volume mount instead of scanning the real work tree.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Oh My Pi Sessions (2 commits)

Oh My Pi's version-3 JSONL sessions are indexed with the same content model as other agents, tagged `source=omp`, and reopen with `omp --resume` (🎯T198).

---

## Packaging & Developer Tools

### [marcelocantos/den](https://github.com/marcelocantos/den) — Homebrew-Free, Three GA Releases (125 commits, v0.14.0–v0.16.0, v0.17.0-rc.1)

922 file changes, <span style="color:#1a7f37">+59,176</span>/<span style="color:#cf222e">−5,244</span>. **~770 added `TEST_CASE`s**. Three GA releases, one RC for v0.17.0, and eleven earlier RCs.

- **v0.14.0 (28 Oct)**: the cask surface, streamed downloads, the mmap'd index cache, `den pin`, tap formulae installed natively, the root environment linked into the prefix, and `make verify-release` with release-version guards.
- **v0.15.0 (30 Oct)**: Homebrew-free install, update and verify, `migrate-prefix`, never downgrade, rollback of a version change that cannot be linked, and the sandboxed source-build stack.
- **v0.16.0 (31 Oct)**: disabled-package refusal and blockers, a single-pass upgrade-all, upgrades compared only against each provider's own index, doctor warnings for held packages and dangling `cert.pem` links, and the launchd PATH taken from den's prefix.
- **v0.17.0-rc.1 (31 Oct)**: retries for the index, GHCR token and blob, self-update and plain archives, with `Retry-After` honoured on 503. The daemon logs its PATH at each startup.
- **Release hygiene**: RC notes and harness docs use placeholders for the test machine, and a `verify-release` step is skipped when its index update fails, instead of reporting a false failure.

### [marcelocantos/homebrew-tap](https://github.com/marcelocantos/homebrew-tap) — den Formula Removed (1 commit)

den now installs with `install.sh` and has no brew path. Thirteen other repositories moved their formula publishing to tapper on Mon 26 Oct: [blurter](https://github.com/marcelocantos/blurter), [crosshair](https://github.com/marcelocantos/crosshair), [cv](https://github.com/marcelocantos/cv), [doit](https://github.com/marcelocantos/doit), [jevons](https://github.com/marcelocantos/jevons), [mcpbridge](https://github.com/marcelocantos/mcpbridge), [mnemo](https://github.com/marcelocantos/mnemo), [pageflip](https://github.com/marcelocantos/pageflip), [pigeon](https://github.com/marcelocantos/pigeon), [rustuml](https://github.com/marcelocantos/rustuml), [sqldeep](https://github.com/marcelocantos/sqldeep), [sysinfo-mcp](https://github.com/marcelocantos/sysinfo-mcp) and [ytt](https://github.com/marcelocantos/ytt). cv cut v0.12.0.

### vendep — C/C++ Source Vendoring (4 commits, local repo)

`vendor/vendep.lock` records each vendored package's tag and commit and can be checked offline. A project can describe libraries that ship no `vendep.json` in its own manifest, and `vendep sync` re-vendors entries that have changed. Headers kept under a library's `include/` land in `vendor/include/`. This was checked live against fmt 11.0.2. CI and a hermetic Makefile prepare it for publication (T1).

### loadmon — Faster, Lazier Trees (6 commits, local repo)

The popover fetches one tree level at a time, and the disk census no longer blocks the process list. Quiet rows above a heavier one are hidden, an "other…" row opens onto the processes it replaced, and directory wrappers that contain only one directory are collapsed.

---

## Networking, Devices & Media

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) — Android Relay over ngtcp2 (87 commits, v0.34.0–v0.35.0)

240 file changes, <span style="color:#1a7f37">+9,055</span>/<span style="color:#cf222e">−4,452</span>. **~61 added test declarations**.

- **Android (🎯T66)**: the JNI connection, pairing and activation seams, the Kotlin relay client and endpoint codec, a pigeon-host instrumentation target, and the Pixel Tablet device oracle.
- **Native transport**: buffered frames survive FIN, ngtcp2 I/O is serialised without blocking full-duplex streams, datagram AEAD buffers are isolated, stream-credit waits abort on close, and bracketed IPv6 hosts are normalised.
- **Distribution**: JitPack builds the nested AAR with pinned cmdline-tools and autotools bootstrapped from source. The Go module uses the system libsodium, and each released tag gets a fail-closed fresh-consumer smoke test.

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — WebCodecs Playback (16 commits)

65 file changes, <span style="color:#1a7f37">+3,129</span>/<span style="color:#cf222e">−286</span>. **~34 added test declarations**. This covers the WebCodecs H.264 decoder and Chrome SP2V oracle (🎯T101.5), IDBFS snapshots, browser pairing links, JPEG XL screenshot archives, install and deploy deadlines scaled for large USB2 iOS transfers (🎯T172), Android dev-policy leases kept alive during slow iOS dispatch (🎯T174), and iOS automation recovery after a USB reconnect.

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — v0.18.0 (12 commits)

`ytt analyze` requires the jevons broker (T33), exhausted synopsis capacity is a quiet deferral, background ingestion is quiet on Claudia v0.76.0, and the release builds on a C++23-capable macOS runner.

### [marcelocantos/blurter](https://github.com/marcelocantos/blurter) — v0.2.0 (5 commits)

Independent alert keys no longer overwrite each other's state, the daemon runs under Supervisor, and release archives include dependency licence notices.

---

## Languages, Libraries & Documents

### [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) — Corrected Kernel, Static Playground (17 commits)

115 file changes, <span style="color:#1a7f37">+7,622</span>/<span style="color:#cf222e">−2,880</span>. The playground became a static site, so its sandbox and security code are gone (−1,929 lines in #3). Code runs only with a token and never gets the host environment. The toolchain is pinned to a recorded SHA and tarball digest, design decisions are recorded with corrected status claims, and the proposal gained a Non-goals section, derived and float-like typed constants, and governing principles.

### [marcelocantos/finance](https://github.com/marcelocantos/finance) — PocketSmith and IG Markets (4 commits)

98 file changes, <span style="color:#1a7f37">+13,338</span>/<span style="color:#cf222e">−876</span>. **~125 added test declarations**. These are the four merged PRs (#10–#13) described under Significant Progress. The PocketSmith migration widens transactions to `user_version` 5 and dedupes against mid-cycle CSV rows.

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — v0.36.0 (3 commits)

A leading viewer title stays pinned under the toolbar as the page scrolls. The release ships a Scoop manifest.

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — v0.34.0 (2 commits)

The Go and Swift wrapper copies are re-bundled from dist, and claudia pins this release.

### [marcelocantos/skills](https://github.com/marcelocantos/skills), [progress-reports](https://github.com/marcelocantos/progress-reports), [progress-reports-private](https://github.com/marcelocantos/progress-reports-private) — Publication Rules (2 + 3 + 3 commits)

The progress-report skill and both report repositories record a rule that published reports carry no host names and no methodology notes.

---

## Commercial

**[minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing)** — 75 commits on `main`, <span style="color:#1a7f37">+7,180</span>/<span style="color:#cf222e">−1,419</span> after the standing `Assets/Tracks/**` exclude. **Stock Cars 3.27 is live** on the App Store and Google Play. Full narrative: [private week 2026-11-01](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-11-01.md).

**[Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms)** — 15 commits on branches. **[squz/yourworld2](https://github.com/squz/yourworld2)** — 3 in-flight. **[minicadesmobile/Minicadeskit](https://github.com/minicadesmobile/Minicadeskit)** — 1 in-flight. Same private companion.

**[squz/ge](https://github.com/squz/ge)** had no activity.

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **marcelocantos/jevons**: 930 in-flight commits on worker and feature branches.
- **marcelocantos/den**: 174 on PR branches, most of them already squash-merged under other SHAs.
- **golang/go** (decimal fork): 114 on the `decimal` branch. These are the runtime and compiler cutover to `internal/bid`, `strconv.ParseDecimal`, quantum-preserving printing, and kernel ratchets.
- **marcelocantos/go-decimal-proposal**: 57 on branches. **marcelocantos/claudia**: 19, including T244's synchronous compact. **marcelocantos/pigeon**: 12.
- **Health-Management-Systems/hms**: 15. See Commercial. **marcelocantos/spyder**: 7. **marcelocantos/sentinel**: 4.
- **marcelocantos/protocol-app**: 3. This is a data-driven routine and checklist app with escalating reminders and an office-parking flow.
- **squz/yourworld2**, **marcelocantos/rustuml**, **marcelocantos/sqlpipe**: 3 each. Single in-flight commits in several fleet repos.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** commits within 2026-10-26…11-01 by commit date. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **29** |
| Total landed commits | **572** |
| Total lines added (landed, filtered) | <span style="color:#1a7f37">+211,198</span>‡ |
| Total lines removed (landed, filtered) | <span style="color:#cf222e">−33,287</span>‡ |
| Net new lines (landed, filtered) | <span style="color:#1a7f37">+177,911</span>‡ |
| File changes | 3,654 (summed per commit; a path touched twice counts twice) |
| New files created | ~1,240 after the same excludes |
| Bulk paths excluded from ☲ | <span style="color:#1a7f37">+348,851</span>/<span style="color:#cf222e">−3,157</span> on counted repos, <span style="color:#1a7f37">+342,208</span> of it jevons' vendored Android native code |
| Releases published | **25** (claudia v0.66.0–v0.80.0; den v0.14.0, v0.15.0, v0.16.0; pigeon v0.34.0–v0.35.0; vellum v0.36.0; sqlpipe v0.34.0; ytt v0.18.0; blurter v0.2.0; cv v0.12.0), plus den v0.17.0-rc.1 and Stock Cars 3.27 on both stores |
| Languages | C++, Go, TypeScript, Kotlin, C, Python, Swift, C#, Shell, TLA+, Markdown, YAML |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. **New this run:** jevons `mobile/android/app/src/main/cpp/` vendored code (the sqlite3, sqlpipe and lz4 amalgamations, `include/**` and the generated `deepparser/**`). The `marcelocantos/think` vault is excluded from the headline, as in previous weeks.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 179 | 366 | <span style="color:#1a7f37">+14,356</span> | <span style="color:#cf222e">−1,619</span> | <span style="color:#1a7f37">+12,737</span> |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 125 | 922 | <span style="color:#1a7f37">+59,176</span> | <span style="color:#cf222e">−5,244</span> | <span style="color:#1a7f37">+53,932</span> |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 87 | 240 | <span style="color:#1a7f37">+9,055</span> | <span style="color:#cf222e">−4,452</span> | <span style="color:#1a7f37">+4,603</span> |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 75 | 215 | <span style="color:#1a7f37">+7,180</span> | <span style="color:#cf222e">−1,419</span> | <span style="color:#1a7f37">+5,761</span> |
| [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) | 17 | 115 | <span style="color:#1a7f37">+7,622</span> | <span style="color:#cf222e">−2,880</span> | <span style="color:#1a7f37">+4,742</span> |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 16 | 65 | <span style="color:#1a7f37">+3,129</span> | <span style="color:#cf222e">−286</span> | <span style="color:#1a7f37">+2,843</span> |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 12 | 52 | <span style="color:#1a7f37">+1,070</span> | <span style="color:#cf222e">−192</span> | <span style="color:#1a7f37">+878</span> |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 9 | 9 | <span style="color:#1a7f37">+280</span> | <span style="color:#cf222e">−150</span> | <span style="color:#1a7f37">+130</span> |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 8 | 1,347 | <span style="color:#1a7f37">+89,204</span> | <span style="color:#cf222e">−9,561</span> | <span style="color:#1a7f37">+79,643</span>† |
| loadmon (local) | 6 | 28 | <span style="color:#1a7f37">+1,681</span> | <span style="color:#cf222e">−374</span> | <span style="color:#1a7f37">+1,307</span> |
| [marcelocantos/blurter](https://github.com/marcelocantos/blurter) | 5 | 25 | <span style="color:#1a7f37">+468</span> | <span style="color:#cf222e">−231</span> | <span style="color:#1a7f37">+237</span> |
| [marcelocantos/finance](https://github.com/marcelocantos/finance) | 4 | 98 | <span style="color:#1a7f37">+13,338</span> | <span style="color:#cf222e">−876</span> | <span style="color:#1a7f37">+12,462</span> |
| vendep (local) | 4 | 40 | <span style="color:#1a7f37">+2,069</span> | <span style="color:#cf222e">−1,362</span> | <span style="color:#1a7f37">+707</span> |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 3 | 8 | <span style="color:#1a7f37">+107</span> | <span style="color:#cf222e">−8</span> | <span style="color:#1a7f37">+99</span> |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 3 | 6 | <span style="color:#1a7f37">+38</span> | <span style="color:#cf222e">−16</span> | <span style="color:#1a7f37">+22</span> |
| [marcelocantos/progress-reports-private](https://github.com/marcelocantos/progress-reports-private) | 3 | 3 | <span style="color:#1a7f37">+6</span> | <span style="color:#cf222e">−2</span> | <span style="color:#1a7f37">+4</span> |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 2 | 22 | <span style="color:#1a7f37">+1,297</span> | <span style="color:#cf222e">−68</span> | <span style="color:#1a7f37">+1,229</span> |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 2 | 11 | <span style="color:#1a7f37">+162</span> | <span style="color:#cf222e">−28</span> | <span style="color:#1a7f37">+134</span> |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 2 | 4 | <span style="color:#1a7f37">+41</span> | <span style="color:#cf222e">−7</span> | <span style="color:#1a7f37">+34</span> |
| [marcelocantos/sentinel](https://github.com/marcelocantos/sentinel) | 1 | 28 | <span style="color:#1a7f37">+517</span> | <span style="color:#cf222e">−4,250</span> | <span style="color:#cf222e">−3,733</span> |
| [marcelocantos/homebrew-tap](https://github.com/marcelocantos/homebrew-tap) | 1 | 2 | <span style="color:#1a7f37">+0</span> | <span style="color:#cf222e">−69</span> | <span style="color:#cf222e">−69</span> |
| [marcelocantos/crosshair](https://github.com/marcelocantos/crosshair) | 1 | 7 | <span style="color:#1a7f37">+56</span> | <span style="color:#cf222e">−23</span> | <span style="color:#1a7f37">+33</span> |
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | 1 | 6 | <span style="color:#1a7f37">+54</span> | <span style="color:#cf222e">−19</span> | <span style="color:#1a7f37">+35</span> |
| [marcelocantos/pageflip](https://github.com/marcelocantos/pageflip) | 1 | 6 | <span style="color:#1a7f37">+54</span> | <span style="color:#cf222e">−22</span> | <span style="color:#1a7f37">+32</span> |
| [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) | 1 | 6 | <span style="color:#1a7f37">+53</span> | <span style="color:#cf222e">−39</span> | <span style="color:#1a7f37">+14</span> |
| [marcelocantos/sysinfo-mcp](https://github.com/marcelocantos/sysinfo-mcp) | 1 | 6 | <span style="color:#1a7f37">+47</span> | <span style="color:#cf222e">−21</span> | <span style="color:#1a7f37">+26</span> |
| [marcelocantos/cv](https://github.com/marcelocantos/cv) | 1 | 5 | <span style="color:#1a7f37">+47</span> | <span style="color:#cf222e">−27</span> | <span style="color:#1a7f37">+20</span> |
| [marcelocantos/doit](https://github.com/marcelocantos/doit) | 1 | 6 | <span style="color:#1a7f37">+46</span> | <span style="color:#cf222e">−21</span> | <span style="color:#1a7f37">+25</span> |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | 1 | 6 | <span style="color:#1a7f37">+45</span> | <span style="color:#cf222e">−21</span> | <span style="color:#1a7f37">+24</span> |

† *Squash 63375185 carries 2,280 branch commits.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~1,158 | Gate, journeys, fleet landings, cockpit UI, replay cassettes |
| [marcelocantos/den](https://github.com/marcelocantos/den) | ~770 | `TEST_CASE`s: source builds, disabled packages, upgrade planning, casks, self-update |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~223 | Cancellation, policy hold, switch rollback, usage replication |
| [marcelocantos/finance](https://github.com/marcelocantos/finance) | ~125 | PocketSmith, IG Markets parser, bank fetch |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | ~61 | JNI lifecycle, relay FIN and close, Kotlin pairing |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~34 | WebCodecs oracle, pairing links, deadlines |
| vendep | ~27 | Lockfile check, manifests, impact |
| [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) | ~15 | Playground site, toolchain pin |
| Others | ~30 | ytt, loadmon, mnemo, blurter, stock-car-racing, sentinel, bullseye |
| **Total** | **~2,440** | Gross added `func Test` / `TEST_CASE` / `#[test]` / `@Test` / `test(` / `it(` lines in the landed diff. jevons' figure spans the whole squash. |

### Daily Activity

![Daily active repositories](daily-activity-2026-11-01.svg)

*(Active repositories per day, landed commits by commit date: Mon 10-26 17, Tue 10-27 7, Wed 10-28 9, Thu 10-29 7, Fri 10-30 10, Sat 10-31 6, Sun 11-01 4. Monday's peak is the fleet-wide tapper rollout. The README timeline counts all-branch activity by author date, so its days for this week are higher.)*

---

## Ideas & Innovations

### A Homebrew Replacement Must Not Need Homebrew ([den](https://github.com/marcelocantos/den))

A tool meant to replace Homebrew cannot depend on Homebrew to be installed, updated or tested. **The release binary now links a vendored static libarchive, installs from a script, updates itself, and is verified through that same path.** The brew formula, bottles and release-tap step were deleted rather than kept as a fallback.

### Never Upgrade into What Upstream Disabled ([den](https://github.com/marcelocantos/den))

An unattended upgrader is dangerous when it treats "newer in the index" as "safe to install". **den refuses disabled packages and dependencies, holds a `version_scheme` bump that would lower a version, and records why each upgrade was blocked.** `--dry-run` reports exactly what the real run would do, so the daemon's behaviour can be previewed.

### Attest the Tree, Then Push ([jevons](https://github.com/marcelocantos/jevons), [bullseye](https://github.com/marcelocantos/bullseye))

A pull request is a slow way to answer "did the gate pass on this tree?" **`make gate` writes an attestation for the exact tree it measured, and the pre-push hook refuses anything else.** Once the gate takes eight minutes instead of two hours, review can happen before the push instead of in a PR queue.

### A Stop That Will Not Settle Discards the Seat ([claudia](https://github.com/marcelocantos/claudia))

When a plan runs out, a seat that ignores its stop keeps spending the plan it was meant to leave. **If a release's turn will not settle, the seat is discarded rather than left running**, and the consumer's policy hold is enforced again on boot, grant and adopt.

### Ask the Process That Can See ([sentinel](https://github.com/marcelocantos/sentinel), loadmon)

Sentinel's own FSEvents observer needed root and so never ran. **loadmon already holds a root-sampled disk census, so sentinel asks it instead and deletes 4,250 lines of watcher, journal and trie.** Duplicated monitoring was replaced by a dependency on the component that already had the data.

### A Language Proposal Backed by a Working Fork ([go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal))

The decimal proposal now points at a fork whose runtime operators go through a BID kernel checked against Intel's reference vectors, with a playground to try them. **Each design claim can be run as well as read**, and an audit records how far the fork still is from an upstream PR.

---

## Effort Estimate: Traditional vs. AI-Assisted

The week's volume came from two release trains (den and claudia), jevons' second large squash, and pigeon's Android transport. den's three GA releases follow the decision that it must not depend on Homebrew. claudia's releases mostly tightened what happens when a turn is cancelled or a plan runs out.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| den v0.14–v0.17-rc.1 | 15-22 | Homebrew-free install and self-update; sandboxed, relocated source builds with Mach-O linkage fixes; disabled-package and version-scheme policy; cask surface; ~770 test cases. |
| claudia v0.66–v0.80 | 12-18 | Fifteen releases: usage replication, hollow-stop handling, policy hold enforcement, process-group cancellation, destructive-git guard, switch-time compaction with ENOSPC rollback. |
| jevons squash and follow-ups | 10-15 | Gated push and a sharded gate; plan-safety fixes on the owner path; landing veto, kill guard, worktree cleanup; replay cassettes; overseer token burn. |
| pigeon v0.34–v0.35 | 8-12 | ngtcp2/quictls cross-built for JNI; Kotlin pairing; FIN and close semantics; a physical-device oracle; JitPack and Go module distribution. |
| Stock Cars 3.27 | 3-5 | Catalogue, events and real-money products; seven iOS builds and several Android candidates through both store reviews. |
| finance | 3-5 | PocketSmith puller with a signed keychain fetcher; IG Markets PDF parsing; Firefox-driven bank fetch. |
| go-decimal-proposal | 3-5 | Proposal rework, corrected kernel, static playground, big-endian CI, fork audit. |
| spyder | 2-4 | WebCodecs H.264 path, IDBFS snapshots, pairing links, USB2 deadlines. |
| vendep, loadmon, sentinel, mnemo, ytt, blurter, bullseye, vellum, sqlpipe, tapper rollout | 6-9 | A new vendoring tool, loadmon tree work, sentinel's dependency switch, OMP indexing, four small releases, and thirteen formula pipelines moved. |

### The Diversity Tax

Homebrew's formula and cask semantics, macOS sandboxing and Mach-O relocation, an agent broker's cancellation and compaction protocol, QUIC over JNI on Android, IEEE 754 decimal arithmetic in a Go fork, browser video decoding, bank and broker statement parsing, and two app-store submissions. That range is far wider than any one specialist covers.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| den | 4-7 | The no-Homebrew decision, standing release approval, GA calls, test-machine checks. |
| claudia | 3-6 | Plan-policy and fleet-intent contract decisions (the two-file schema), and release sign-off. |
| jevons | 2-4 | Approving the gated-push model, the standing-gate pause, and landing sign-off. |
| Stock Cars | 3-5 | Content and pricing decisions with the studio, store submissions, and the rollout waiver. |
| finance | 2-4 | Human bank logins, keychain setup, and checking the ledger results. |
| pigeon | 1-3 | Running the physical tablet and reviewing the Android design. |
| go-decimal-proposal | 1-2 | Proposal wording and design principles. |
| Others | 2-4 | tapper rollout, the den formula removal, loadmon UI iteration. |

### What If It Were One Person?

The specialist band sums to roughly 62-95 person-days. A generalist would also need ramp-up on Homebrew internals, ngtcp2 and JNI, the broker wire protocol, and decimal floating point. Landed activity ran every day (4–17 repos), with Monday's fleet-wide tapper rollout the peak.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~87-133 person-days (~4.4-6.7 months)** |
| Specialist team (traditional) | **~62-95 person-days (~3.1-4.8 person-months)** |
| Actual human effort this week | **~18-35 hours (~2.3-4.4 person-days)** |
| **Multiplier vs. generalist** | **~20-60x** |
| **Multiplier vs. specialist team** | **~15-40x** |

The multiplier is highest on den's and claudia's release trains, where most of the cost is careful, heavily tested change. It is lowest on Stock Cars and finance, where store reviews, studio decisions and human bank logins set the pace. The human contribution was mostly policy: den must not need Homebrew, a stop must actually stop, and a push must carry proof that its gate passed.

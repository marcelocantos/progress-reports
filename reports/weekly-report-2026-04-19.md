# Weekly Progress Report — 2026-04-13…19

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Excl-vendor landed lines: **+98,123/−15,758** (net **+82,365**).

## Executive Summary

A 7-day sprint across **21 repositories** spanning the launch of two greenfield products (**pageflip** — a Rust meeting-capture pipeline with macOS Vision face-blur, OCR PII redaction, ScreenCaptureKit audio, WhisperX transcription, pyannote diarisation, and a Go "meetcat" specialist-agent shell; **spyder** — an HTTP MCP server for cross-platform mobile device orchestration that reached v0.5.0 in three days and now owns iOS/Android inventory, reservations, screenshot, app lifecycle, crash collection, network shaping, and run artefacts), a massive expansion of **mnemo** from v0.15.0 to v0.21.0 across six releases that added image indexing with Opus-generated descriptions plus OCR plus CLIP embeddings, a live compaction pipeline with an LLM-driven summariser, a connection-identity pivot that re-keyed session chains around daemon connections, a collapse to a single HTTP-transport MCP daemon, and native Windows support, a TLA+-verified drain-window cutover protocol plus ngtcp2 QUIC C transport plus one-time-token multi-client pairing in **pigeon** v0.17.0, a mobile-platform engine release in **squz/ge** v0.1.0 that split the engine into engine/render/bridge subsystems behind a RenderHost interface and landed physical-device matrix cells on iOS + Android, a **bullseye** v0.15.0–v0.17.0 trilogy that pivoted from machine-wide external storage to per-repo location discovery and added an mtime-keyed parse cache, a **doit** v0.6.0 that added a shell-script content-hash approval gate plus timeout enforcement plus learned per-pattern duration anomaly detection from audit-log data, a **jevons** v0.4.0 with mTLS CA + device provisioning plus a cross-repo active-work MCP dashboard plus draft/preview/promote for Lua view scripts, an **esfera2** port of the sphere + pieces onto bgfx (9.7k lines of Dawn WebGPU code replaced), and an **HMS** de-identification audit round 7. The dominant motion was **shipping greenfield** — two new products went from zero to brew-installable CLIs in a week, while the existing MCP ecosystem (mnemo, bullseye, doit, pigeon) absorbed major correctness and platform work.

**391 commits** | **~+98,123 / ~−15,758** (excl. vendor) | **~140-220 person-days traditional equivalent** | **~35-55x multiplier**

### Major Achievements & Innovations

- **pageflip launched** (pageflip) — Rust + Go meeting-capture pipeline from zero to v0.1.0 in four days. Rust binary does window-relative ScreenCaptureKit region capture with an interactive rubber-band picker, 64-bit DCT pHash dedup (Hamming-distance threshold), Apple Vision face detection + two-pass box-blur redaction, VNRecognizeTextRequest OCR + regex PII matching with black-rect masking (email, phone, SSN, credit card, IP), a compile-time egress gate (`RedactedFrame` sealed type with `pub(crate) new_sealed`) that makes it a compile error to ship a raw frame without redaction, and a `policy.rs` app allowlist + paranoid-mode gate. Go "meetcat" sibling spawns five persistent claudia.Agent specialist sessions (skeptic, constructive, neutral, dejargoniser, contradictions-via-mnemo) in parallel via a SessionPool, writes structured meeting artefacts (decisions.md, actions.md, open-questions.md, contradictions.md) from the neutral specialist at stop, and ships a pyannote diarisation pipeline that aligns speakers with slide events. The project has a hard legal invariant — raw audio bytes never leave the audio module (enforced by private fields on `AudioSamples` and a `Segment`-only boundary). Homebrew formula, release workflow, doctor subcommand, STABILITY.md, CONTRIBUTING.md. **30 targets achieved**
- **spyder launched** (spyder) — HTTP MCP server for mobile device orchestration, from initial scaffold Fri Apr 17 to v0.5.0 Sun Apr 19. 65 commits across 206 files (+18,790/-649). iOS adapter uses pymobiledevice3 + CoreDevice (the path mobile-mcp's WDA layer often fails on); Android adapter uses adb + dumpsys. Reservation system for parallel dev sessions with canonical UDID normalisation. tunneld lifecycle + probe + Handler gate. Screenshot, list_apps, launch_app, terminate_app, install_app, uninstall_app, deploy_app, device_state, orientation, screen recording (iOS sim + Android), crash report collection, network-condition shaping (tc/netsh), simulator + emulator lifecycle management, run-artefact store with atomic-rename manifests and path-traversal guards, REST API + CLI subcommands. KeepAwake iOS companion app (free-tier signing) auto-deploys across every iOS device; auto-launches on unplug. **5 releases**
- **mnemo v0.16.0 → v0.21.0** (mnemo) — six releases, 80 commits, adding: `mnemo_whatsup` live session resource monitoring, `mnemo_decisions` past-decision surfacing with retroactive backfill, query templates (`mnemo_define`/`evaluate`/`list_templates`), `mnemo_prs` GitHub PR/issue indexing (schema v14), `mnemo_discover_patterns` for self-improving feature discovery, `mnemo_commits` git history indexing (schema v15), `mnemo_images` with Opus-generated descriptions (schema v16), image OCR (schema v17), CLIP embeddings for semantic + visual similarity search, `mnemo_docs` for project md/txt/pdf indexing across tracked repos, `mnemo_restore` for compacted-session restoration, and `mnemo_chain` with connection-identity-anchored session chaining. v0.18.0 shipped a live compaction lifecycle: a `Watcher` polls LiveSessions() every 30s, spawns per-session goroutines that compact on 5-minute tickers with a token-budget guard, and reaps idle sessions after 10 minutes — all via a `claudia.Task` LLM caller. v0.20.0 collapsed the stdio proxy + daemon into a single HTTP MCP daemon via mark3labs/mcp-go's StreamableHTTP transport (killed the custom JSON-RPC-over-UDS protocol entirely). v0.21.0 added native Windows support
- **pigeon v0.17.0 with TLA+-verified cutover + ngtcp2 QUIC + multi-client pairing** (pigeon) — 43 commits. The CutoverProtocol.tla model (TLC-verified across 159K states) proves bounded-loss cutover: CUTOVER marker signals last message on old path, receiver drains within a timeout window. Implementation sends FrameCutover before closing LAN, drains 2s. One-time-token pairing consumes the token at `pair_hello` acceptance (WaitingForClient→DeriveSecret), not at completion — closes the concurrent-race window. Multi-client relay via client counter (N independent bridges per instance ID). `IssueCredential()` API generates PairingRecord credentials without a live device (browser serverCertificateHashes via LAN offer). Swift `PairingCeremonyMachineTests` rewritten for composed actors; cross-language confirmation test passes on macos-14 CI. ngtcp2 + quictls/openssl + nghttp3 vendored under `c/vendor/` as submodules; `pigeon_ngtcp2_transport` vtable backed by raw QUIC (ALPN "pigeon") with zero heap allocations in pigeon code
- **ge v0.1.0 + engine/render/bridge split** (squz/ge) — 49 commits on the shared mobile engine, reaching v0.1.0 release. `Split ge into engine + render + bridge subsystems` introduces a `RenderHost` interface separating rendering from engine logic. In-tree `tiltbuggy` sample added (consumed via `add_subdirectory(ge)` pattern from both iOS and Android samples). Physical-device matrix cells pass on Pippa / iPhone / Android; Android emulator dist GL-context crash fixed on modern AVDs; Android startup-flash check records from before launch. Vendored SDL_ttf for Android consumers so Text-rendering works via add_subdirectory. Push H.264 colour-space conversion onto the GPU via SDL3 YUV textures. Triangle library licence clarified as non-commercial + opt-in. NOTICES.md, STABILITY.md, agents-guide.md
- **bullseye v0.15.0 → v0.17.0** (bullseye) — three releases, 18 commits. v0.15.0 added external-storage mode (`~/.config/bullseye/config.yaml` + `bullseye_configure`) for corporate contexts where `bullseye.yaml` can't be committed. v0.16.0 **threw that away and redesigned** — location is now a per-repo property encoded by where `bullseye.yaml` lives; `discover_anywhere(cwd)` probes in-repo walk-up first, then shadow walk-up under `~/.local/share/bullseye/`; `bullseye_init` and `bullseye_import` grow a required `location` parameter. v0.17.0 made `value`/`cost` optional at repo scope, aligning with phase-boundary design. `perf(🎯T13)` adds an mtime-keyed parse cache to `store::load()` — no fsnotify needed; `load()` checks mtime before reading disk and returns the cached parse on hit
- **spyder pmd3 bridge pivot + KeepAwake deletion** (spyder, partial — spans into 21-22 Apr) — the iOS path originally used a KeepAwake companion app for power-assertion; this week began the pivot to a bundled Python pmd3-bridge (FastAPI + uvicorn over Unix domain socket, PyInstaller-bundled, Go client with `http.Client` + Unix-socket `DialContext`). Power assertion moves server-side and the companion-app layer disappears
- **doit v0.6.0 with shell-script content-hash gate + timeout + anomaly detection** (doit) — 12 commits. `scriptGate` (tier-0, pre-policy) detects plain shell-script invocations (`bash|sh|zsh <path>` or `./<path>` with a shell shebang), requires an explicit elicitation keyed by SHA-256 of the script contents, persists approvals at `~/.config/doit/script-approvals.yaml`, and re-elicits on content change. `TimeoutSeconds` wraps exec context with a deadline that SIGKILLs the whole process group on expiry (Setpgid + Cancel hook so bash-spawned children die with the shell). `ExpectedDurationSeconds` lets callers declare typical durations; `AggregateDurations` scans audit entries, groups by `(cap, subcmd)`, computes interpolated p50/p95 for successful non-timed-out runs, persists stats at `~/.config/doit/duration-stats.yaml`, and `CheckDurationAnomaly` returns a bypassable Deny when declared duration deviates sharply from learned history
- **jevons v0.4.0 with mTLS + active-work dashboard + Lua drafts** (jevons) — 15 commits. `internal/auth` implements Ed25519 CA (10-year validity), client cert issuance (1-year, ExtKeyUsageClientAuth, device ID as CN), server cert issuance, TLS 1.3 `RequireAndVerifyClientCert`. Device provisioning endpoint `POST /api/provision` with `ClientCertMiddleware` exempting `/health` and `/api/provision`. `jwork` MCP tool does depth-limited (max 3) recursive delegation with progress heartbeats extracted from markdown headings and raw log persistence. `jevons_active_work` MCP tool aggregates recent Claude sessions + dirty trees + open PRs into a ranked cross-repo table (bounded concurrency: 8 goroutines for git, 4 for gh). Lua view scripts get a draft/preview/promote flow
- **esfera2 Dawn → bgfx port** — detail in [private week 2026-04-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-19.md)
- **HMS de-identification audit round 7** — detail in [private week 2026-04-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-19.md)
### Significant Progress

- **mnemo connection-identity pivot** (mnemo) — restructured 🎯T25 as umbrella for an MCP-connection pivot: one writer (connection observer writing definitive rows), one reader layer (`mnemo_chain` composing definitive + query-time heuristic via a `mode` parameter), compactor anchored to connection identity. Required vendoring mcpbridge into `internal/bridge/`, threading `ConnContext` through the bridge, persisting `daemon_connections`, adding `connection_id` to compactions, and a definitive chain writer that deletes the ingest-time heuristic. End-to-end connection-observer test closes the AC. This is foundational correctness work for every compacted session restore that follows
- **pigeon cascading relay architecture doc** (pigeon) — exploration doc filed (🎯T12) for cascading relay architecture alongside the drain-window cutover implementation. STUN and Bluetooth proximity investigations (🎯T4, 🎯T5). LAN offer now includes cert hash so browsers can use `serverCertificateHashes` (🎯T6.2)
- **bullseye concurrent-writer tolerance** (bullseye) — 🎯T17 filed and implemented post-window (2026-04-20+): the `store` layer tolerates concurrent writers to `bullseye.yaml` via the mtime cache + atomic-rename discipline. T16 (self-describing repo-scope ordering) filed

### Tough Challenges Overcome

- **Compile-time egress gate for redacted frames** (pageflip): the architectural constraint is that captured frames must be redacted before any write or network egress. Runtime checks would add bugs; a type-level proof is stronger. Solution: `RedactedFrame` with private fields and `pub(crate) new_sealed` constructor, plus `RedactPipeline::apply_and_seal` as the only path to produce one. Raw `Frame` cannot be passed where `RedactedFrame` is required — the Rust type system makes unredacted egress a compile error
- **Connection-identity pivot under an already-shipping compaction pipeline** (mnemo): the compactor was anchored to session IDs, but `/clear`-bounded transcripts have indistinct boundaries and cwd-based heuristics were both unreliable and baked into ingest. Fix: introduced daemon_connections + connection_id as the primary key, re-keyed compactor and mnemo_restore around connection identity, deleted the ingest-time cwd heuristic entirely and moved heuristic-chain inference to query time via a `mode` parameter on mnemo_chain. One definitive writer + one composed reader, no more double-source-of-truth
- **Drain-window cutover without sequence numbers** (pigeon): the naïve dual-path cutover requires per-message sequence numbering and receiver-side ordering logic — expensive in C. Insight: a single CUTOVER marker on the old path combined with a bounded drain window on the receiver gives bounded loss. TLA+ verified 159K states. Implementation is simpler than dual-path and compatible with the existing single-active-path state machine
- **One-time-token race at pair_hello** (pigeon): consuming the pairing token at ceremony completion leaves a window where concurrent `pair_hello`s can both pass the token check before either completes. Fix: consume at `pair_hello` acceptance (`WaitingForClient → DeriveSecret`), not at pairing completion. Guard `token_valid` checks `active_tokens`; consumption immediately moves to `used_tokens`
- **External-storage design churn in bullseye** (bullseye): v0.15.0 shipped a machine-wide config file + `bullseye_configure` tool to select in-repo vs. external storage. Within 3 hours of v0.15.0 the design was rethrown — location is a per-repo property, not a machine property. v0.16.0 replaced the machine config with path-driven probing (`discover_anywhere` tries in-repo walk-up then shadow walk-up under `~/.local/share/bullseye/`). Required making `location` a required parameter on `bullseye_init`/`bullseye_import` so locked-repo behaviour is deterministic
- **Learned per-pattern durations from audit log** (doit): declaring every command's expected duration up-front is impractical; so doit learns. `AggregateDurations` scans the audit log, groups by `(cap, subcmd)`, computes interpolated p50/p95 for successful non-timed-out runs, persists stats, and `CheckDurationAnomaly` flags deviations. The twist: the Deny is bypassable — flags unusual timing without blocking valid long runs
- **Engine/render/bridge split in ge** (squz/ge): the engine code was intermixing rendering (bgfx commands, texture management) with bridge (SessionHost, H.264 streaming, player handshake) and pure-engine logic (scene graph, input, physics). Split into three subsystems behind a `RenderHost` interface — render consumes engine, bridge composes both. De-hardcoded `yourworld` throughout SessionHost and player; `config.appName` replaces hardcoded strings

Contributor: Marcelo Cantos

---

## Tooling

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Transcript Intelligence, Images, and Connection Identity (80 commits)

**The biggest single effort of the week.** Continued from last week's v0.15.0 with six more releases and a fundamental model pivot:

- **Six new MCP tools** (v0.16.0, 2026-04-13): `mnemo_whatsup` for live session resource monitoring (enriched with cwd + transcript mapping, postmortem mode); `mnemo_decisions` for surfacing past decisions with retroactive backfill; `mnemo_define` / `mnemo_evaluate` / `mnemo_list_templates` for reusable query templates; `mnemo_prs` with GitHub PR/issue indexing (schema v14); `mnemo_commits` with git history indexing (schema v15); `mnemo_discover_patterns` for self-improving feature discovery
- **Image indexing pipeline** (v0.17.0, 2026-04-14/15): schema v16 adds `images`, `image_occurrences`, `image_descriptions` + FTS5. Inline base64 images are ingested from entry JSON during ingest; file-path references with image extensions are ingested alongside. A background worker pool (2 goroutines) polls for undescribed images, downscales >1568px via CatmullRom, and calls the Anthropic vision API (claude-sonnet-4-5 with claude-3-5-sonnet-20241022 fallback) with surrounding conversation context as grounding. Schema v17 adds image OCR via VNRecognizeTextRequest (CGO + ObjC in-process — moved from Swift subprocess for ~2-5x speedup). CLIP embeddings added for semantic + visual similarity search. Golden image fixtures for OCR system tests via git-LFS. Claude -p batched invocation replaces per-image calls
- **Live compaction lifecycle** (v0.18.0, 2026-04-16): `internal/compact/` — summariser, prompt, payload parser, `Watcher` polling LiveSessions() every 30s, per-session goroutines on 5-minute tickers, idle reap at 10min, self-exclusion via cwd prefix to prevent recursion. `ClaudiaCaller` implements LLMCaller via `claudia.Task` (`claude -p` headless, parses stream-json, returns full token/cost). `mnemo_restore` tool reads back compactions with telemetry. Token-budget guard prevents over-sized compactions
- **Connection-identity pivot (🎯T25)** (v0.18.0): re-keyed compactor and mnemo_restore around daemon connection identity instead of session IDs. Added `connection_sessions` binding + `mnemo_self` hook. Definitive chain writer deletes the ingest-time heuristic; `InferChainHeuristic` moves to query-time via `mnemo_chain` `mode` parameter. One writer, one composed reader
- **Progress logging during ingest** (v0.19.0): per-file and progress logging for large backfills
- **Collapse to single HTTP daemon** (v0.20.0, 2026-04-18): `Collapse mnemo to a single HTTP MCP daemon (🎯T27)`. Previously shipped two binaries coupled by custom JSON-RPC over UDS (stdio proxy + serve daemon); now speaks MCP directly over HTTP via mark3labs/mcp-go's `StreamableHTTP` transport. Users register with `claude mcp add --scope user --transport http mnemo http://localhost:19419/mcp`. Stale stdio registrations detected with migration hint
- **Native Windows support** (v0.21.0, 2026-04-19): `🎯T22 achieved: mnemo daemon runs natively on Windows`

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Cross-Platform Mobile Device MCP Server (65 commits, initial)

New Go MCP server orchestrating iOS + Android development workflows. Fri Apr 17 initial scaffold → v0.5.0 Sun Apr 19:

- **Platform adapters**: iOS via pymobiledevice3 + CoreDevice (picks up where mobile-mcp's WDA path fails); Android via `adb` + `dumpsys`. `device_state` (battery, charging, foreground app) unified across platforms
- **Reservation system** (🎯T11): exclusive device holds so parallel agent sessions don't yank each other's state. `internal/reservations` with `Acquire / Release / Renew / Authorize / List / Get`. Device identity canonicalised through a `Normalizer` (raw UDIDs → CoreDevice UUIDs). `spyder run` test-wrapper auto-restores KeepAwake after
- **Device operations** (🎯T7-T9): tunneld lifecycle + probe + Handler gate; `screenshot`, `list_apps`, `launch_app`, `terminate_app`, `install_app`, `uninstall_app`, `deploy_app` MCP tools
- **Session lifecycle**: auto-deploy + auto-launch of KeepAwake across every iOS device (🎯T10); KeepAwake exits on unplug; macOS notification after auto-launch; free-tier Personal Team signing
- **Parallel fan-out (7 mobile-dev primitives)** (🎯T13-T19, T21): orientation control (T13), screen recording for iOS sim + Android (T14), crash report collection for iOS + Android (T15), `install/uninstall/deploy_app` (T16), network-condition shaping (T17), simulator/emulator lifecycle management (T18), device log tailing with filters over the daemon (T19), visual regression docs (T21), run-artefact store (T20): each reservation opens `~/.spyder/runs/<run-id>/` with `manifest.json`; release closes the run; daemon startup prunes old/oversize runs. `runs_list`/`runs_show` REST + CLI
- **Architecture**: HTTP-based MCP server, dropped the mcpbridge stdio-proxy approach. `spyder mcp add` self-registration. `bridge/` scaffolded for the pmd3 Python bridge (realised post-window as v0.6.0)
- **5 releases**: v0.1.0 through v0.5.0 in 3 days

### [marcelocantos/pageflip](https://github.com/marcelocantos/pageflip) — Meeting Capture Pipeline (53 commits, initial)

New Rust + Go meeting-capture pipeline. Designed to feed live slides from screen-shared meetings into a Claude Code session for real-time analysis. v0.1.0 Homebrew-installable Sat Apr 18:

- **Capture core (Rust)** (T1-T5): `src/capture/` abstracts `WindowCapture`; macOS backend uses ScreenCaptureKit. Interactive rubber-band region picker via winit + softbuffer. Window capture by title substring, `--list-windows`. 64-bit DCT pHash dedup (`image_hasher` 8x8 DCT + mean); Hamming-distance threshold skips cursor movement, compression noise, mid-animation frames. Interval loop with Ctrl-C streaming; stdout-of-saved-paths enables a `pageflip-feed` filesystem-watching feeder for live Claude analysis
- **Face-blur redactor** (T10.1): `FaceBlurRedactor` detects faces via `VNDetectFaceRectanglesRequest`, applies two-pass box-blur (radius 15) over each detected bounding box. Degrades to no-op when Vision inference context is unavailable (e.g. CI/headless). Deps: objc2, objc2-foundation, objc2-core-foundation, objc2-vision
- **OCR + PII text redactor** (T10.2): `ocr_frame()` via `VNRecognizeTextRequest` returns `OcrWord{text, bbox}`. `detect_pii()` with `OnceLock`-compiled regexes for Email, Phone, CreditCard, GovernmentId (SSN), IpAddress; multi-word match support via concat + offset mapping. `TextPiiRedactor` draws opaque black over each `PiiMatch` bbox
- **Compile-time egress gate** (T10.3): `RedactedFrame` sealed type with private fields and `pub(crate) new_sealed` constructor. `RedactPipeline::apply_and_seal` is the only path to produce one. Shipping an unredacted frame is a compile error. `policy.rs` adds `AppAllowlist` loaded from JSON config, `frontmost_app_bundle_id()` via NSWorkspace, and `ParanoidSaver` persisting unredacted frames to a local-only dir with path-traversal guards
- **Audio capture with no-egress invariant** (T9.1): `src/audio/` enforces the project's hard policy — raw audio bytes never leave the audio module. `AudioSamples` has private fields; only a `Segment` (derived transcript text) can exit via the `Transcriber` trait. `AudioCaptureHandle` owns the ScreenCaptureKit audio tap
- **WhisperX + pyannote transcription** (T9.2, T9.3): `WhisperxTranscriber` runs Whisper large-v3 in batch mode post-hoc. Pyannote `speaker-diarization-3.1` runs in-memory on the 16kHz numpy array; `whisperx.assign_word_speakers` merges speaker labels. NDJSON output gains `speaker_id` when `--diarize`. No temp files
- **Slide-event NDJSON protocol** (T18): slide events emitted as NDJSON lines consumed by the Go meetcat shell
- **meetcat Go shell (T19)**: spawns persistent `claudia.Agent` specialist sessions (skeptic, constructive, neutral, dejargoniser, contradictions) in parallel via a `SessionPool`. Slides injected via goroutines; agent stdout streamed to stderr tagged `[specialist-name]`. `attach` subcommand prints tmux-attach command. Session IDs resumable across `/clear`
- **ArtifactWriter** (🎯T12): at meeting-stop, sends a structured prompt to the neutral specialist agent and writes `decisions.md`, `actions.md`, `open-questions.md`, `contradictions.md`, `references.json` stub, `session-ids.json`. Slides symlinked from SlidesDir; transcript.jsonl copied
- **Resolver** (🎯T11): extracts and resolves slide references across artefacts
- **Specialist config files + OSC 8 hyperlinks** (T13, T15, T19.4): `--specialists` flag, neutral session persistence
- **Weekly meeting digest + launchd installer** (T17); **Confluence glossary cache** for the dejargoniser (T16); **contradictions specialist** (Opus model) queries mnemo_search for cross-meeting conflicts (T14)
- **Release infrastructure**: Homebrew formula, CONTRIBUTING.md, STABILITY.md, issue templates, doctor subcommand with auto-invoked meetcat doctor, structured session log
- **All 30 bullseye targets achieved**

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — External Storage Redesign + Perf (18 commits)

Three releases (v0.15.0 → v0.17.0), with a significant mid-release redesign:

- **v0.15.0 — external storage mode** (🎯T12): `~/.config/bullseye/config.yaml` with `mode: in_repo` or `external` (shadow tree under `~/.local/share/bullseye/` mirroring absolute cwd paths, path-driven — no git-remote or layout assumptions). `bullseye_configure` MCP tool records the one-time choice
- **v0.16.0 — per-repo storage discovery** (3 hours later): machine-wide config file and `bullseye_configure` **removed**. Location is a per-repo property encoded by where `bullseye.yaml` lives. `discover_anywhere(cwd)` probes in-repo walk-up first, shadow walk-up under `~/.local/share/bullseye/` second. `bullseye_init` and `bullseye_import` grow a required `location` parameter
- **v0.17.0 — optional value/cost at repo scope** (🎯T11): `bullseye_put` no longer requires value/cost at repo scope, aligning with phase-boundary design
- **mtime-keyed parse cache** (🎯T13): `store::load()` now caches parsed `TargetsFile` values keyed by canonical path, invalidating on mtime change. `parse_file()` extracted as the uncached inner parser. No fsnotify needed — the lazy alternative satisfies the target
- **Parallelised Makefile convention** (🎯T9) documented; **T2.4** `/cv` global mode retired; **T1.2/T1.3** momentum + /cv rewrite complete

### [marcelocantos/doit](https://github.com/marcelocantos/doit) — Time + Approval Gates (12 commits)

v0.6.0:

- **Shell-script content-hash approval gate** (🎯T27): tier-0, pre-policy. Detects `bash|sh|zsh <path>` and `./<path>` with shell shebangs. Requires explicit elicitation keyed by SHA-256 of script contents. Subsequent invocations of the same content bypass elicitation; modifications force re-approval. Persists at `~/.config/doit/script-approvals.yaml`. `internal/script` has the shell-word tokeniser, detector, hasher, content-preview extractor, YAML-backed approval store
- **Timeout enforcement** (🎯T26.1): `doit_execute` and `doit_dry_run` accept `timeout_seconds`. When >0, exec context wraps with a deadline that SIGKILLs the whole process group on expiry (exit 137). `Setpgid + Cancel` hook so bash-spawned children die with the shell
- **L1 access to time expectations** (🎯T26.2)
- **Learned per-pattern durations + anomaly detection** (🎯T26.3): `AggregateDurations` scans audit entries, groups by `(cap, subcmd)`, computes interpolated p50/p95 for successful non-timed-out runs. `DurationStore` persists stats at `~/.config/doit/duration-stats.yaml`. `CheckDurationAnomaly` returns a bypassable Deny when `expected_duration_seconds` deviates sharply from learned history
- **--help-agent flag** (🎯T28): agent-guide emission built into the binary (convention from CLI binaries directive)

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — mTLS + Active Work + Lua Drafts (15 commits)

v0.4.0:

- **mTLS CA management** (internal/auth): CA generation/persistence (Ed25519, 10-year validity); client cert issuance (1-year, `ExtKeyUsageClientAuth`, device ID as CN); server cert issuance; `TLSConfig` (`RequireAndVerifyClientCert`, TLS 1.3 minimum). CA round-trip, cert issuance, and live mTLS handshake all covered by tests
- **Device provisioning endpoint**: `POST /api/provision` issues certs; `ClientCertMiddleware` exempts `/health` and `/api/provision`. `--tls` flag for mTLS on the HTTP listener; `CertPEM` method on CA for response body
- **jwork MCP tool** (🎯T8.1): depth-limited (max 3) recursive delegation with progress heartbeats extracted from markdown headings, raw log persistence via `db`, and delegation-guidance injection at the depth boundary
- **jevons_active_work MCP tool** (🎯T16.1): aggregates recent Claude Code sessions (discovery.Scanner), dirty working trees (`git status`), and open PRs (`gh pr list`) into a ranked text table sorted by most recent activity. Registry checked for active agents per repo. Bounded concurrency: 8 goroutines for git ops, 4 for gh queries
- **Lua view scripts** — draft/preview/promote flow with dead server-side view rendering code removed
- **Bullseye standing-invariants hook** + frontier targets marked observable

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Windows Advisory Flock (3 commits)

v0.7.0: split advisory `flock` into platform-gated helpers for Windows support. Small but unblocks spyder and mnemo's Windows stories.

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Housekeeping (2 commits)

ccache wire-up, test fix, `targets.yaml` → `bullseye.yaml` migration; T17 (composable pull-based sized-read abstraction) filed; Homebrew tap disabled for /release.

---

## Game Projects

### [squz/ge](https://github.com/squz/ge) — Engine Split + v0.1.0 (49 commits)

The shared mobile engine reached its first release — the biggest game-engine milestone since Dawn→bgfx migration:

- **Engine/render/bridge split** with `RenderHost` interface separating rendering concerns from engine logic and bridge composition. Engine → render consumption, bridge composes both
- **In-tree tiltbuggy sample** added; consumed via `add_subdirectory(ge)` + APP_NAME convention from iOS and Android samples
- **Physical-device matrix cells pass** on Pippa / iPhone / Android (🎯T21). Android emulator dist GL-context crash fixed on modern phone AVDs (🎯T22 background); startup-flash check records from before launch (🎯T23 background)
- **Player launch-time server params** (🎯T23): player accepts `ged_addr` launch param on iOS + Android (host-controlled)
- **H.264 colour-space conversion on the GPU** (🎯T32): SDL3 YUV textures replace CPU YUV→RGB conversion
- **Android text rendering** (🎯T30.1–T30.3): vendor SDL_ttf for Android so consumers get text via add_subdirectory; Android FontLoader so Text-using consumers link cleanly; sample/tiltbuggy Android consumes ge via add_subdirectory
- **Triangle licence clarity** (🎯T31): non-commercial + opt-in model documented
- **Matrix-cell infrastructure**: 10s default soak cell (🎯T27), desktop-long-soak cell, per-cell sim/emu parallelism, `--brokered` start in reconnect sub-check (🎯T25)
- **Packaging**: NOTICES.md (third-party attribution), agents-guide.md, STABILITY.md, CLAUDE.md directives
- **v0.1.0 released**

### [squz/esfera2](https://github.com/squz/esfera2) — Dawn → bgfx Port (9 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-19.md).*
### [squz/multimaze2](https://github.com/squz/multimaze2) — UI + ge Integration (19 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-19.md).*
### [squz/multimaze](https://github.com/squz/multimaze) — ES1 Oracle (12 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-19.md).*
### [squz/yourworld2](https://github.com/squz/yourworld2) — ge Submodule Updates (7 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-19.md).*
## Libraries & Infrastructure

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) — TLA+ Cutover + QUIC C + Multi-Client Pairing (34 commits)

v0.17.0 and v0.18.0:

- **TLA+ cutover model** (🎯T3, 🎯T2.1, 🎯T2.2): `CutoverProtocol.tla` verified by TLC across 159K states. CUTOVER marker signals last message on old path; receiver drains within timeout window. No sequence numbering — simpler than dual-path, compatible with existing single-active-path state machine. Implementation: executor sends `FrameCutover` before closing LAN path, drains remaining messages for 2s. `FallbackToRelay()` and `IsDirectActive()` exported for app use
- **ngtcp2 QUIC transport for C** (🎯T11.4): ngtcp2 + quictls/openssl + nghttp3 vendored under `c/vendor/` as git submodules (avoids collision with Go's `vendor/`). `pigeon_ngtcp2_transport` — a `pigeon_transport` vtable backed by raw QUIC (ALPN "pigeon") with zero heap allocations in pigeon code. Build script (`c/vendor/build.sh`) and Makefile targets (`build-vendor-deps`, `test-c-ngtcp2`). All 15 existing C tests still pass. Regenerated amalgamated `dist/` C output
- **One-time token pairing** (🎯T15): token consumed at `pair_hello` acceptance (WaitingForClient→DeriveSecret), not completion — closes concurrent-race window. Guard `token_valid` checks `active_tokens`; consumption immediately moves to `used_tokens`
- **Multi-client relay** (🎯T15): `inst.occupied: bool` → client counter; N independent bridges per instance ID
- **IssueCredential() API**: generates PairingRecord credentials without a live device. Enables browser `serverCertificateHashes` via the LAN offer (🎯T6.2)
- **Swift PairingCeremonyMachineTests rewritten** for composed actors (🎯T16). **testCrossLanguageConfirmationCode** passes on macos-14 CI runner (🎯T17) — took multiple iterations: install Go in swift-test CI job (RelayE2ETests builds the relay binary); stream relay + crypto-peer stderr into test output; print crypto-peer instance ID to stdout not stderr
- **Exploratory work**: cascading relay architecture doc (🎯T12); STUN and Bluetooth proximity investigations (🎯T4, 🎯T5); `make deploy` target for Fly.io (🎯T9)

### [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) — ccache (2 commits)

ccache wire-up + TODO note: the C API should accept `sqlite3*` directly.

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — ccache (1 commit)

ccache wire-up in build toolchain.

### [marcelocantos/sysinfo-mcp](https://github.com/marcelocantos/sysinfo-mcp) — ccache (1 commit)

ccache wire-up.

### [marcelocantos/mk](https://github.com/marcelocantos/mk) — ccache (1 commit)

Wrap cc/cxx with ccache in std libs. The wave of ccache wire-ups this week came from a cross-project latency reduction campaign.

---

## Healthcare & Enterprise

### [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) — De-Identification Audit Round 7 (1 commit)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-19](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-19.md).*
## Strategic Planning & Documentation

### [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) (3 commits)

Last week's report added; achievements linked to their week; scoring rubric for executive-summary item selection added to `docs/guide.md`.

### [marcelocantos/skills](https://github.com/marcelocantos/skills) (4 commits)

Skills sync commits from `~/.claude/skills/`.

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only. Git log queried with `--since=2026-04-13 --until=2026-04-20` (inclusive Mon-Sun calendar boundary) **without** `--all`, so commits on merged feature branches are counted once on master via the squash-merge commit.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 21 |
| Total commits | 391 |
| Total lines added | +98,123 |
| Total lines removed | −15,758 |
| Net new lines | +82,365 |
| Net new lines (excl. vendored/generated) | ~+86,000 (of +87,603 real insertions) |
| File changes | 1,356 |
| Languages | Rust, Go, C, C++, Swift, Kotlin, TypeScript, Python, TLA+, YAML, SQL, Objective-C, Metal, GLSL |
| Contributors | 1 (Marcelo Cantos) |

Note: ge's +15,129 includes ~4.2k vendored shaderc binaries, SDL_ttf source tree, and web/dist rebuild. pageflip's +19,418 includes ~4.4k Cargo.lock + Go module bootstrap. esfera2's +9,657/-9,416 is a near-zero-net port of the rendering layer from Dawn/WebGPU to bgfx. multimaze's -2,957 is cleanup of the ES1 original codebase used as oracle for multimaze2.

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 80 | 276 | +13,452 | -4,259 | +9,193 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 65 | 206 | +18,790 | -649 | +18,141 |
| [marcelocantos/pageflip](https://github.com/marcelocantos/pageflip) | 53 | 204 | +19,418 | -1,582 | +17,836* |
| [squz/ge](https://github.com/squz/ge) | 49 | 207 | +15,129 | -2,414 | +12,715** |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 34 | 115 | +9,360 | -1,865 | +7,495*** |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 19 | 86 | +1,994 | -186 | +1,808 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 18 | 53 | +2,383 | -904 | +1,479 |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 15 | 38 | +2,110 | -912 | +1,198 |
| [marcelocantos/doit](https://github.com/marcelocantos/doit) | 12 | 50 | +3,557 | -103 | +3,454 |
| [squz/multimaze](https://github.com/squz/multimaze) | 12 | 32 | +563 | -3,520 | -2,957**** |
| [squz/esfera2](https://github.com/squz/esfera2) | 9 | 22 | +9,657 | -9,416 | +241***** |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 7 | 8 | +15 | -16 | -1 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 4 | 9 | +180 | -14 | +166 |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 3 | 8 | +97 | -8 | +89 |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 3 | 20 | +3,378 | -1,259 | +2,119 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 2 | 13 | +750 | -460 | +290 |
| [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) | 2 | 2 | +11 | -1 | +10 |
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | 1 | 3 | +275 | -14 | +261 |
| [marcelocantos/mk](https://github.com/marcelocantos/mk) | 1 | 2 | +4 | -2 | +2 |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 1 | 1 | +3 | -2 | +1 |
| [marcelocantos/sysinfo-mcp](https://github.com/marcelocantos/sysinfo-mcp) | 1 | 1 | +8 | -0 | +8 |

\* pageflip net includes ~4.4k Cargo.lock + Go module bootstrap; real code ~15.0k.  
\** ge net includes ~4.2k vendored shaderc binaries + SDL_ttf source tree; real code ~10.9k.  
\*** pigeon net includes ~100 lines of amalgamated `dist/` regeneration.  
\**** multimaze negative net is cleanup of the ES1 oracle codebase used as reference for multimaze2.  
\***** esfera2 near-zero net is a full rewrite of the rendering layer from Dawn/WebGPU to bgfx (+9,657 bgfx code replacing -9,416 Dawn code).

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/pageflip](https://github.com/marcelocantos/pageflip) | ~232 | Rust dedup + picker + face-blur + OCR + policy tests; Go meetcat agents + artifact + resolver + hash + revisit tests |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~206 | MCP handler tests, reservation tests, notify/autoawake helpers, daemon HTTP roundtrip, runs store tests, tunneld tests |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | ~83 | Swift composed-actor ceremony tests, ngtcp2 C vtable tests, TLA+ cutover model, cross-language confirmation, credential API |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~62 | Connection-observer end-to-end, image OCR system tests (golden fixtures via LFS), embedding similarity system tests, compaction watcher tests, chain tests |
| [marcelocantos/doit](https://github.com/marcelocantos/doit) | ~52 | script-gate tests, duration-store tests, timeout process-group tests, anomaly detection tests |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | ~20 | Discover-anywhere tests, storage-mode tests, mtime cache tests, optional-value-cost tests |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~15 | mTLS auth tests (CA round-trip, cert issuance, live handshake), jwork tests, active-work tests, Lua draft tests |
| **Total** | **~670** | |

### Daily Activity

![Daily active repositories](daily-activity-2026-04-19.svg)

---

## Ideas & Innovations

### Compile-Time Egress Gate for Redacted Frames ([pageflip](https://github.com/marcelocantos/pageflip))

The problem: meeting-capture software must redact frames (face-blur, PII OCR) before any disk write or network egress. Runtime checks are easy to forget and easy to bypass — one unlabelled save path and you have a compliance breach. Pageflip solves this with a **sealed newtype backed by a privacy-scoped constructor**: `RedactedFrame` has private fields; `pub(crate) new_sealed` is the sole constructor; `RedactPipeline::apply_and_seal` is the only path that calls it. Every `Frame → write` path must accept `RedactedFrame`, which can only be obtained from `apply_and_seal`, which always runs the redaction pipeline. Shipping a raw `Frame` where a `RedactedFrame` is required is a compile error, not a runtime assertion. The Rust type system becomes the compliance auditor.

### Connection-Identity as the Session-Chain Anchor ([mnemo](https://github.com/marcelocantos/mnemo))

Claude Code sessions are bounded by `/clear` into separate JSONL files; reconstructing the logical work span requires stitching files together. Last week's approach used cwd-based heuristics at ingest time — unreliable when `/cd` changes mid-session and hard to retract. This week's pivot: **daemon connection identity is the primary key**. `daemon_connections` tracks each MCP connection lifetime; `connection_id` is added to compactions; `mnemo_chain` exposes a `mode` parameter so callers can choose definitive (connection-anchored) or heuristic (retroactive cwd-inferred) chaining. One writer for definitive rows, one reader that composes. The retroactive heuristic remains for the pre-connection-observer epoch, but it's decisively not the source of truth. Deleting the ingest-time heuristic and moving inference to query time is the key move — it lets the definitive source evolve without schema migrations of already-ingested data.

### Drain-Window Cutover Without Sequence Numbering ([pigeon](https://github.com/marcelocantos/pigeon))

Cleanly cutting over from a LAN path to a relay path (or vice versa) traditionally requires either (a) sequence numbers + receiver-side ordering logic to deduplicate, or (b) dual-path transmission with deduplication by message ID. Pigeon's insight: **a single CUTOVER marker + a bounded drain window on the receiver delivers bounded loss with no sequence numbering**. TLA+ model verified 159K states — the protocol terminates, no messages are delivered twice, and no message sent before CUTOVER is lost within the drain window. The implementation side is 200 lines of Go rather than a full ordering state machine, and it composes cleanly with the existing single-active-path model.

### One-Time Tokens Consumed at Handshake Acceptance ([pigeon](https://github.com/marcelocantos/pigeon))

Consuming a pairing token at ceremony completion leaves a race window: two concurrent `pair_hello`s can both pass the token check before either completes the ceremony. Pigeon closes this by **consuming the token at `pair_hello` acceptance** (`WaitingForClient → DeriveSecret`), not at completion. `token_valid` checks `active_tokens`; acceptance atomically moves the token to `used_tokens`. Any second client hitting `pair_hello` with the same token sees an invalid token and is rejected. The ceremony can then fail mid-flight without worrying about token reuse, because the token was already burned at handshake acceptance.

### Learned Durations From Audit Logs ([doit](https://github.com/marcelocantos/doit))

Declaring every command's expected runtime up front is impractical and brittle — the right numbers depend on the machine, the project, the phase of the moon. doit learns from its own audit log: `AggregateDurations` groups successful non-timed-out runs by `(cap, subcmd)` and computes interpolated p50/p95 via the standard `(pos_lo, pos_hi)` weighted formula; `DurationStore` persists to YAML; `CheckDurationAnomaly` flags deviations. The twist that keeps it useful is the **bypassable Deny** — anomaly doesn't hard-fail, it requires user acknowledgement. A command that's unusually long for this workspace still runs, but with a pause and a recorded reason. The agent gets feedback without being blocked.

### In-Tree Engine Sample Consumed Via add_subdirectory ([squz/ge](https://github.com/squz/ge))

When a shared mobile engine is consumed by many games, each integration re-implements the boilerplate: CMake fragments, APP_NAME conventions, framework linkage, shader pipelines. ge v0.1.0 puts **the canonical integration pattern in-tree as a working sample** — `tiltbuggy` is a real app that consumes ge via `add_subdirectory(ge)` and exercises the full APP_NAME + `ge/FRAMEWORKS` + shaderc pipeline + player + SessionHost surface. Downstream games (esfera2, multimaze2, yourworld2) adopt the pattern by mirroring what tiltbuggy does. The sample doubles as the matrix-cell integration test on physical devices. This eliminates the "ge is a black box you have to reverse-engineer" problem that plagued the engine before v0.1.0.

### Bullseye.yaml Per-Repo Location Discovery ([bullseye](https://github.com/marcelocantos/bullseye))

Bullseye originally stored `bullseye.yaml` in each repo's root, which breaks down in corporate contexts where `bullseye.yaml` can't be committed. The first fix was a machine-wide config file selecting in-repo vs. external — which muddled "where does bullseye live?" with machine state. The v0.16.0 redesign **encodes location as a per-repo property determined by where the file physically lives**: in-repo walk-up first, shadow walk-up under `~/.local/share/bullseye/<abs-cwd>` second. The shadow tree is purely path-driven (no git-remote assumption, no host/org/repo layout), so it works for any filesystem layout. The design is stateless beyond file existence. `bullseye_init` and `bullseye_import` take a required `location` parameter so the choice is explicit, not implicit. The machine-wide config disappears.

---

## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| mnemo 6 releases + connection-identity pivot | 18-28 | Go daemon with SQLite FTS5 + schema v14→v17 migrations; image indexing with Anthropic vision API + CLIP embeddings + OCR (CGO + ObjC); live compaction pipeline with LLM summariser + token-budget guard; HTTP MCP transport collapse; Windows port; fundamental re-architecture of session-chain identity |
| spyder 5 releases from scratch | 12-20 | HTTP MCP server with iOS (pymobiledevice3 + CoreDevice) and Android (adb + dumpsys) adapters; reservation system with device canonicalisation; tunneld lifecycle; 7 mobile-dev primitives including orientation, screen recording, crash collection, network shaping (tc/netsh), sim/emu lifecycle, log tailing, run-artefact store; REST API + CLI |
| pageflip from scratch | 12-18 | Rust screen-capture with ScreenCaptureKit, perceptual hashing, interactive winit+softbuffer picker; Apple Vision face detection + text OCR with objc2 bindings; compile-time egress gate via sealed types; ScreenCaptureKit audio with no-egress invariant; WhisperX + pyannote diarisation pipeline; Go meetcat shell with claudia-backed 5-specialist sessions and artefact writer; Homebrew packaging |
| pigeon TLA+ cutover + ngtcp2 + multi-client | 8-14 | TLA+ model for cutover protocol (159K states); ngtcp2 + quictls + nghttp3 vendored and wired as a zero-allocation C transport vtable; one-time-token pairing with race-window closure; multi-client relay refactor; Swift composed-actor test rewrites; CI diagnostics for macos-14 cross-language parity |
| ge v0.1.0 + engine/render/bridge split | 10-15 | Architectural decomposition of a shared mobile engine across engine/render/bridge subsystems with a `RenderHost` interface; Android text-rendering support (vendored SDL_ttf + FontLoader); GPU YUV colour-space conversion via SDL3; physical-device matrix cells on iOS+Android; in-tree sample as canonical integration; STABILITY.md snapshot for v0.1.0 |
| bullseye v0.15-v0.17 | 6-10 | Rust MCP server; redesign of storage-mode from machine-wide config to per-repo path-driven discovery; mtime-keyed parse cache; schema evolution with optional value/cost at repo scope; cross-rebundle with the `bullseye_init`/`import` API |
| doit v0.6.0 | 5-8 | Shell-script invocation detection with tokeniser + shebang analysis; SHA-256 content-hash approval gate with YAML persistence; process-group timeout enforcement with SIGKILL; audit-log-driven p50/p95 duration aggregation and anomaly detection |
| jevons v0.4.0 | 5-8 | Ed25519 CA + client/server cert issuance + TLS 1.3 mTLS config; device-provisioning HTTP endpoint; jwork depth-limited recursive delegation; cross-repo active-work aggregation with bounded goroutine concurrency; Lua draft/preview/promote |
| esfera2 Dawn → bgfx port | 6-10 | Full rewrite of the rendering layer for a geodesic chess game; bgfx shader pipeline; ge v0.1.0 integration; shaderc pipeline adoption |
| multimaze2 | 3-5 | Main menu + pack selection UI; mobile build polish; ge version churn tracking |
| multimaze ES1 oracle | 2-4 | Resurrection of a legacy ES1 codebase on modern Xcode for oracle purposes: CALayer delegate fixes, CMMotionManager migration, FBO thumbnail fixes, orientation lock |
| claudia Windows support | 1-2 | Platform-gated flock helpers |
| pigeon exploratory (STUN, Bluetooth, Fly deploy, cascading) | 2-3 | Architecture exploration docs; deployment infrastructure |
| HMS audit round 7 | 1-2 | Coverage analysis of 8 AX assessment extension tables; manifest addition |
| other (csp housekeeping, ccache rollout, sqlift/sqlpipe/sysinfo-mcp/mk, skills, progress-reports) | 2-4 | Small improvements across many repos |

### The Diversity Tax

Specialisms exercised this week:

- **Rust systems programming** — screen capture, perceptual hashing, Apple Vision bindings via objc2, ScreenCaptureKit audio with compile-time invariants, winit+softbuffer overlays, Homebrew release pipeline
- **Go MCP daemon architecture** — HTTP MCP transport via mark3labs/mcp-go StreamableHTTP, live compaction pipelines, schema migrations, claudia.Task LLM callers, cross-process identity tracking, mTLS CA management
- **Pure C library engineering** — ngtcp2 QUIC transport vtable with zero heap allocations, amalgamated C distribution, git-submodule vendored dependencies (quictls, nghttp3)
- **TLA+ formal verification** — cutover protocol model with 159K states verified by TLC
- **iOS / Android device automation** — pymobiledevice3 + CoreDevice, adb + dumpsys, orientation control, screen recording, crash report collection, install/launch/terminate app
- **Mobile game engine architecture** — engine/render/bridge decomposition with abstract RenderHost, bgfx + SDL3 integration, SDL_ttf vendoring for Android, GPU YUV colour-space conversion, Dawn-to-bgfx port
- **macOS platform depth** — ScreenCaptureKit, Vision framework (VNDetectFaceRectanglesRequest, VNRecognizeTextRequest), NSWorkspace, CGO + ObjC in-process OCR, tmux agent management, launchd installers
- **Audio/ML pipelines** — WhisperX + Whisper large-v3 batch transcription, pyannote 3.1 speaker diarisation with in-memory numpy passthrough, speaker-label alignment via whisperx.assign_word_speakers
- **Security engineering** — compile-time egress gates via sealed types, one-time-token consumption at handshake acceptance, content-hash approval gates, mTLS certificate issuance, PII regex detection + OCR redaction, audit-log-driven anomaly detection, healthcare PII manifest
- **Rust MCP server development** — per-repo path-driven storage discovery, mtime-keyed parse caches, schema-optional fields at repo scope
- **Cryptographic protocol implementation** — X25519 confirmation codes cross-language on macos-14 CI; one-time token lifecycle with racewindow closure
- **Go library design** — claudia.Agent sessions for persistent specialist roles; SessionPool in parallel; structured artefact writers
- **Build infrastructure** — ccache wire-up across 6 repos

No single developer holds production-level expertise across Rust screen-capture + Vision + sealed-type compliance, Go MCP daemon architecture + HTTP transport collapse + connection-identity re-anchoring, pure C QUIC + TLA+ cutover verification, iOS/Android device automation, bgfx mobile engine decomposition, macOS system-API work, pyannote/WhisperX ML pipelines, healthcare PII compliance, Rust MCP server design, and cross-platform security engineering simultaneously.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| mnemo | 3-5 | Connection-identity pivot design, image-pipeline scope decisions, HTTP transport collapse architecture, Windows support prioritisation |
| spyder | 3-4 | Mobile primitives priority (what to ship in the first week), reservation model, pmd3 bridge direction |
| pageflip | 3-4 | Sealed-type egress gate strategy, specialist-agent roles, no-audio-recording constraint, diarisation vs. transcription split |
| pigeon | 2-3 | TLA+ model design (what invariants to prove), ngtcp2 vendoring decision, token-consumption timing fix |
| ge | 2-3 | Engine/render/bridge split decision, v0.1.0 STABILITY surface, matrix-cell model for device parity |
| bullseye | 1-2 | Storage-mode redesign (machine-wide → per-repo), location parameter placement on init/import |
| doit | 1-2 | Script-gate model (tier-0 pre-policy), anomaly-detection UX (bypassable Deny) |
| jevons | 1-2 | mTLS scope, active-work aggregation sources, Lua workflow model |
| other | 2-3 | ccache rollout coordination, esfera2 port direction, multimaze ES1 oracle scope, HMS audit-round-7 direction |
| **Total** | **~18-28** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | Ramp-up cost |
|---------|------------|-----------------|--------------|
| mnemo | 18-28 | 26-42 | Go daemon + FTS5 + Claude Code transcript internals + vision API + CLIP + pyannote or equivalent + HTTP MCP transport |
| spyder | 12-20 | 18-30 | pymobiledevice3 + CoreDevice + adb + Android power management + launchd + Homebrew packaging |
| pageflip | 12-18 | 18-28 | Rust + Apple Vision + objc2 + ScreenCaptureKit + WhisperX + pyannote + tmux/claudia + Go channel orchestration |
| pigeon | 8-14 | 13-22 | C QUIC + ngtcp2/quictls build + TLA+ + Swift actors + cross-language crypto |
| ge | 10-15 | 15-23 | bgfx + SDL3 + SDL_ttf + CMake + iOS + Android + shaderc + matrix testing |
| bullseye | 6-10 | 9-15 | Rust MCP SDK + filesystem walk-up semantics + schema evolution |
| doit | 5-8 | 8-12 | Security policy + process groups + audit-log aggregation + percentile stats |
| jevons | 5-8 | 8-12 | Go crypto/tls + Ed25519 CA + mTLS + Lua VM |
| esfera2 | 6-10 | 9-15 | bgfx port of existing Dawn code + ge integration |
| multimaze / multimaze2 | 5-9 | 8-14 | iOS ES1-to-modern build + CMMotionManager + Box2D + level-pack UI |
| other | 4-7 | 6-11 | Various |

Context-switching tax (12+ domain switches): +15-25 person-days

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **140-220 person-days (5.5-9 months)** |
| Specialist team (traditional) | **115-185 person-days (4-7 person-months)** |
| Actual human effort this week | **~18-28 hours (~2.5-4 person-days)** |
| **Multiplier vs. generalist** | **~35-55x** |
| **Multiplier vs. specialist team** | **~30-45x** |

The multiplier is highest on pageflip and spyder (zero-to-brew-installable in a week — work that would take a specialist mobile/macOS team months), on the mnemo image-indexing + connection-identity pivot + HTTP transport collapse sequence (each of those is a week of focused work on its own and they shipped together), and on the pigeon TLA+ + ngtcp2 + multi-client sequence (formal verification plus vendored QUIC plus protocol racewindow closure is conventionally a 2-3 week specialist effort). The multiplier is lowest on the ccache wire-up wave and the multimaze ES1 resurrection (both are mechanical once the direction is set). The human contribution concentrated on architectural pivots (mnemo connection identity, bullseye per-repo location, ge engine/render/bridge split), security posture decisions (pageflip compile-time egress gate, doit bypassable-Deny, pigeon token-at-acceptance), and scope discipline (what to ship in spyder's first week, what not to ship in pageflip v0.1.0).

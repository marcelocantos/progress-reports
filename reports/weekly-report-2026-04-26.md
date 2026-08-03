# Weekly Progress Report — 2026-04-20…26

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Excl-vendor landed lines: **+90,565/−18,977** (net **+71,588**).

## Executive Summary

Twenty repositories saw activity, dominated by three concurrent release storms — **mnemo** rolling out eleven minor releases (v0.22.0 through v0.32.0) that took the daemon from "barely Windows-aware" to a per-user Windows Service with double-click MSI, ARM64 cross-compile via llvm-mingw, federation over mTLS between linked instances, an idempotent indexer, four new MCP tools, a periodic CLAUDE.md summary review worker, and a streamable-HTTP keepalive; **spyder** shipping ten minor releases (v0.10.0 → v0.19.0) that moved iOS power-assertion from a sideloaded KeepAwake app to a bundled PyInstaller pmd3-bridge over Unix domain sockets, hardened the bridge against fd leaks and silent failures, and folded autoawake into the daemon's runs lifecycle; and **bullseye** climbing six minor releases (v0.18.0 → v0.23.0) that added a `set_aside` status with required rationale, an envelope-leak validation guard backed by acceptance tests, a `validate_blocking`/`validate_warnings` split, frontier banner + legend, and a SQLite priorities writer driving WSJF synchronisation across repos. **csp** shipped v0.9.0 and v0.10.0 with HTTP/1.1 client, in-band channel exception delivery, per-worker wake to eliminate thundering herd, ergonomic I/O wrappers, HTTP/2 server (nghttp2 cleartext + TLS), and a pull-based source abstraction. **pigeon** v0.18.0 → v0.20.0 introduced typed pairing primitives (`PairingArtifact`, `PairingHost`, `CredentialStore`, `ConnectWithArtifact`) across Go/Swift/Kotlin and folded `pigeon-pair` into the main binary as a subcommand. **sawmill** v0.10.0 + v0.11.0 added a SQLite-backed git AST index, semantic blame, semantic bisect, intra-language pattern equivalences with transitive closure, structured violation payloads, and an auto-fix convergence loop. **mcpbridge** went from v0.3.0 to v0.5.0 by adding a message-oriented transport vtable plus a complete HTTP backend (POST + per-POST SSE) wired through `main.c`. **ytt** released v0.1.0 → v0.3.0 (the first releases of an open-source YouTube transcript CLI). **doit** shipped v0.7.0 → v0.9.0 with a documented threat model, three layers of audit-chain provenance (elicitation outcomes, L3 chain-of-evidence, structured stdout/stderr capture), a learned-durations-per-project-root key, and a startup warning for execution-adjacent sibling MCP servers. **claudia** v0.8.0 + v0.9.0 added `SessionExists`/`SessionJSONLPath` public probes. **vellum** v0.2.0 added a macOS clipboard backend (RTF + HTML + plain text in one NSPasteboard transaction). **stock-car-racing** ported Stages 1-3 forward onto bgfx + ge::run + RenderHost and integrated Jolt physics + Pacejka tire dynamics. **squz/ge** continued with H.264 GPU YUV conversion, Android SDL_ttf vendoring, spyder-driven matrix cells, and a `ge_wire.yaml` declaring the wire protocol with Go/Swift/Kotlin/C/TS bindings. Commercial project detail: [private week 2026-04-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-26.md).

**355 commits** | **~+90,565 / ~−18,977** (excl. vendor) | **~120-190 person-days traditional equivalent** | **~30-50x multiplier**

### Major Achievements & Innovations

- **mnemo windows + federation + idempotency** ([mnemo](https://github.com/marcelocantos/mnemo)) — eleven minor releases (v0.22.0 → v0.32.0) shipped this week. v0.22.0 ships a double-click Windows installer (Inno Setup, MSYS path-conversion fixes, dist staged next to the .iss); v0.23.0 cross-compiles `windows/arm64` via llvm-mingw rather than the windows-11-arm runner; v0.24.0 suppresses the Windows console window; v0.25.0 revives Windows Service registration as a per-user Registry entry under `HKCU` (escapes admin-only `HKLM` install); v0.26.0 auto-migrates legacy stdio MCP registrations; v0.27.0 trims `mnemo_status` defaults; v0.28.0 ships `mnemo diagnose`; v0.29.0 lights up federation across linked mnemo instances over mTLS (self-signed ECDSA P-256 cert at `~/.mnemo/endpoint/`, peer cert allowlist under `~/.mnemo/peers/`, validated `linked_instances` config, `mnemo print-endpoint` subcommand); v0.30.0 lands four new MCP tools (`mnemo_session_structure`, `mnemo_tool_result`, `mnemo_get_memory`, `mnemo_locate_uuid`) plus an idempotent indexer (UNIQUE constraint + INSERT OR IGNORE migration), launchd PATH for the compactor, and structured per-tick watcher logging; v0.31.0 adds `mnemo_repos` returning CLAUDE.md summaries + last-commit dates and a periodic CLAUDE.md summary review worker keyed by cheap signals (mtime + size); v0.32.0 sends 30 s heartbeat pings on streamable-HTTP MCP streams to keep keepalive sessions warm
- **spyder pmd3 bridge transition + autoawake convergence** ([spyder](https://github.com/marcelocantos/spyder)) — ten minor releases (v0.10.0 → v0.19.0). The flagship change is the **completion of the KeepAwake → pmd3-bridge migration**: a Python `pmd3-bridge` (FastAPI + uvicorn) bundled via PyInstaller, communicating over a Unix domain socket; a Go bridge client + supervisor wraps it; iOS routing goes through the bridge with power-assertion-based autoawake; KeepAwake companion-app, `internal/tunneld/`, and the xcodegen dependency are deleted. v0.10.0 ships iOS 17+ ScreenshotService and autoawake convergence; v0.11.0 fixes a CI race; v0.12.0 makes `resolveBridgeBinary` follow executable symlinks; v0.13.0 prefers a paid Developer Program team for KeepAwake codesigning; v0.14.0 fixes `UninstallApp`; v0.15.0 bounds every devicectl call with a timeout (hotfix); v0.16.0 overhauls the CLI for Make-driven test infrastructure (T37); v0.17.0 cleans up devices + bridge (T29/T30/T34/T35/T36) including a bridge-`_lockdown` fd-leak fix with regression tests; v0.18.0 narrows autoawake to wired-only; v0.19.0 adds CLI rough-edge fixes plus an MCP heartbeat. KeepAwake then comes back into the picture (v0.13.0+) for unsolved corner cases until ScreenshotService takes over in v0.10.0
- **bullseye envelope-leak guard + set-aside status + rework payloads** ([bullseye](https://github.com/marcelocantos/bullseye)) — six releases (v0.18.0 → v0.23.0). v0.18.0 lands; v0.19.0 renames `observable` → `showcase` and tightens the demonstration constraint; v0.20.0 moves the YAML lockfile out of the project dir and keys it by parent inode (🎯T19); v0.21.0 ships the `set_aside` status with a required rationale field and a structured `sawmill_failure` + `mnemo_history` payload contract for the `rework` flow; v0.22.0 ships the **envelope-leak guard** — every target's `value`/`cost` envelope is now machine-checked against parent envelopes, with acceptance tests covering the failure modes; v0.23.0 splits `validate()` into `validate_blocking` + `validate_warnings`, gates the frontier `## Frontier` markdown on the blocking variant only, and ships a banner + legend on repo-scope frontier output. The week also delivers `🎯T3.1` — a SQLite `targets_priorities` writer plus a `sync-priorities` CLI that lets external tools (jevons' active-work dashboard, `/cv` scoring) consume target priorities without re-parsing YAML
- **csp v0.9.0 + v0.10.0 with HTTP/1.1 client, channel exceptions, per-worker wake, HTTP/2 + ergonomic I/O** ([csp](https://github.com/marcelocantos/csp)) — two releases plus a series of frontier targets between them. v0.9.0 brings **in-band exception delivery on channels** (🎯T18) — exceptions raised on a sender thread surface on `recv` rather than vanishing into the scheduler — plus a flaky `Timeout-expiry` test fix, a CI runtime bound, and the `🎯T20` fake_clock audit raised. v0.10.0 then lands HTTP/1.1 client (🎯T3.6), per-worker wake to eliminate thundering herd on the M:N scheduler (🎯T13, +1.0k lines), and a pull-based source abstraction stage 1 (🎯T17). Post-v0.10.0 work raises and ships ergonomic I/O wrappers (🎯T3.1 — `lines`, `read_all`, `read_until`, etc.), an HTTP/2 server backed by nghttp2 with cleartext + TLS variants and ALPN-selected HTTP/2 (🎯T3.7), and a pull-based composable source abstraction. WIP commits show partial WebSocket and QUIC implementations for follow-on work
- **HMS oracle toolchain bootstrap** — detail in [private week 2026-04-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-26.md)
- **sawmill v0.11.0 with git AST index + semantic blame/bisect + equivalence pillar + auto-fix loop** ([sawmill](https://github.com/marcelocantos/sawmill)) — two releases. The biggest landings are: a SQLite-backed semantic git index (`gitindex` package) that stores tree-sitter parse trees keyed by git blob SHA in a normalised schema (blobs, nodes, node_types, field_names, commit_files), with cursor-based tree walking and in-memory interning caches, lazily indexed by an `Indexer` that walks first-parent commits and fills HEAD in the background; new MCP tools `git_log`, `git_diff_summary`, `git_blame_symbol`, `semantic_diff`, `api_changelog`, `git_semantic_bisect`. **Semantic blame** distinguishes four commits per function: `introduced`, `last_modified`, `body_last_modified`, `signature_last_changed`. **Semantic bisect** binary-searches first-parent ancestry between good and bad refs to find where a structural predicate (`symbol_exists`, `function_has_param`, `type_has_field`) flipped, parsing only `O(log N)` commits and returning the responsible `SymbolChange`. **Pattern equivalences pillar (🎯T1)** ships in four pieces: storage (teach/list/delete_equivalence backed by SQLite), apply (rewrite either direction with unified diff + pending-change flow), check (scan codebase for non-preferred sides as violations), and **transitive closure** via union-find — three patterns sharing a class derive a pair, conflicting preferences silently neutralise the class. **Diagnostic-driven auto-fix (🎯T3)** is a loop that pulls structured LSP diagnostics (now with `code` + `source` fields), matches each against a teach_fix regex with named captures, instantiates a recipe or transform with the captures bound, and applies via the standard pending-change flow until the file is clean / stuck / iteration-limited. Adds **structured violation payloads** (`format=json`) to `check_conventions`, `check_invariants`, and `query` — 11 new tests cover the legacy-text path, structured returns, schema renderers, and empty-result-as-`[]` semantics for programmatic consumers (closes 🎯T24). Also: `apply_multi_root_pr` for orchestrating multi-repo PR lifecycles (🎯T27)
- **mcpbridge HTTP backend + connection schema v2** ([mcpbridge](https://github.com/marcelocantos/mcpbridge)) — three releases (v0.3.0 → v0.5.0). The body of the work is a clean structural rework of the C transport vtable from fd-based (`read_fd`/`write_fd`/`read`/`write`) to message-oriented (`poll_fd`/`pump`/`send`), folding line-splitting into `transport_stdio.c` so an HTTP transport could slot in. Then **`transport_http.c`** lands: plain `http://` localhost-only, POST-only with per-POST SSE responses, MCP-Session-Id capture and echo, MCP-Protocol-Version on every request, no standing GET SSE stream, single-threaded with a self-pipe as the stable poll fd. v0.4.0/v0.5.0 stabilise: a config schema v2 with connection metadata (🎯T5.1); the `mcpbridge connect <path>` wrapper as a unified front door (🎯T5.2 + T5.3); brew source backend works under launchd (🎯T2); standing-invariants Makefile hook for /cv. Net: ~5.3k lines of C added, ~1.3k removed, with a full HTTP MCP fake server in the test suite
- **pigeon typed pairing primitives + pair subcommand** ([pigeon](https://github.com/marcelocantos/pigeon)) — three releases (v0.18.0, v0.19.0, v0.20.0). Primitives: `PairingArtifact` + `CredentialStore` + `PairingHost` (🎯T1.2) shipped across Go/Swift/Kotlin with `Swift PigeonConn.connect(artifact:)` + Kotlin `connectWithArtifact`. `cmd/pigeon-pair` is folded into the main `pigeon` binary as a `pair` subcommand. The artifact lifecycle guide documents the new shape (🎯T1.3); a flaky cross-language confirmation E2E test is fixed (🎯T20); Kotlin `PairingCeremonyMachineTest` is regenerated for split sub-machines (🎯T19). v0.20.0 ships these as the first-class API (Go + iOS SPM), unblocking jevons' migration off bespoke X25519 + ad-hoc QR JSON
- **doit threat-model + audit-chain + duration learning** ([doit](https://github.com/marcelocantos/doit)) — three releases (v0.7.0 → v0.9.0). v0.7.0 ships `--help-agent` (🎯T28). v0.8.0 lands the **threat model documented + linked from STABILITY.md** (🎯T32); per-project-root learned durations key (🎯T29) — duration stats now segregated by project root rather than globally; `rm`-tier reflects reversibility via git-tracked status (🎯T30); a startup warning when execution-adjacent MCP servers (sawmill, etc.) are detected loaded alongside doit (🎯T34); `doit_check_config` surfaces every threat-model-named load-bearing knob (🎯T33); the L3 prompt-injection surface is enumerated, the prompt is hardened, and a test corpus lands (🎯T35). v0.9.0 ships **L3 chain-of-evidence in the audit log** (🎯T37) — every gated execution carries the upstream policy decisions and elicitation outcomes that authorised it; **elicitation outcomes + L2 promotions** captured in the audit chain (🎯T36); **`doit_audit_query` MCP tool** for filtered postmortem lookups (🎯T38); and **stdout/stderr excerpt capture for failure-mode commands** (🎯T39) so a failed run leaves enough breadcrumb in the audit log to diagnose without re-running
- **ytt initial open-source releases** ([ytt](https://github.com/marcelocantos/ytt)) — three releases (v0.1.0 → v0.4.0 prep) of a YouTube transcript CLI plus playlist-ingest companion scripts. Origin is the `/open-source` skill applied to a previously-internal tool. v0.1.0 strips the PyPI publish job (hCaptcha outage on trusted publisher setup) and keeps sdist + wheel as release attachments; v0.2.0 bundles a standalone PyInstaller binary; v0.3.0 switches to `--onedir` (~100 ms hot startup vs. ~4 s for onefile) and the Homebrew formula moves payload into `libexec` with a binary symlink in `bin`; release prep adds Obsidian graph node-label improvements for ingested files
- **vellum macOS clipboard delivery** ([vellum](https://github.com/marcelocantos/vellum)) — v0.2.0 ships **`convert_to_clipboard` with RTF + HTML + plain text** in one atomic NSPasteboard transaction (🎯T7). The convert pipeline grows `Render` / `RenderFile` so callers can obtain the assembled HTML page without invoking Prince; the new `clipboard` package derives RTF + plain text in-process from HTML via `NSAttributedString`, eliminating the previous `textutil + osascript` pipeline (single-rep, no commit confirmation, lossy round-trip). NSPasteboard's synchronous API guarantees `Write` returns only after `changeCount` advances. Round-trip test reads each representation back via a cgo helper; Linux + Windows backends return `ErrUnsupported`
- **stock-car-racing port to ge bgfx + Jolt physics** — detail in [private week 2026-04-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-26.md)
- **claudia public probes** ([claudia](https://github.com/marcelocantos/claudia)) — v0.8.0 + v0.9.0 ship `SessionExists` + `SessionJSONLPath` as public functions (🎯T2) so external tools can probe Claude Code session state without re-implementing the discovery walk

### Significant Progress

- **squz/ge spyder-driven matrix cells + GPU YUV + Android text** ([squz/ge](https://github.com/squz/ge)) — `🎯T33.1` collapses per-platform branches in `smoke-test.sh` onto the `spyder` CLI; `T33.2` wraps matrix cells in `spyder run` for race-safe parallel reservations; `T33.3` adds visual regression via `spyder screenshot` + diff against baselines plus `make update-baselines`; `T33.4` calls `spyder device_power_state` post-run with a distinct exit code when the device fell asleep; `T33.5` commits the spyder pool config plus pool-init/drain Make rules. `T7` auto-pauses audio when the app is backgrounded and resumes on foreground. `T11.1` declares the wire protocol in `ge_wire.yaml` and emits Go/Swift/Kotlin/C/TS bindings. `T30.1` vendors SDL_ttf for Android consumers; `T30.2` adds Android FontLoader for Text-using consumers; `T30.3` confirms `sample/tiltbuggy` Android consumes ge via `add_subdirectory(ge)` end-to-end. `T31` clarifies Triangle's non-commercial licence + opt-in model. `T32` pushes H.264 colour-space conversion onto the GPU via SDL3 YUV textures. The bullseye state for the repo gets two consolidations as the surface evolves
- **jevons pigeon migration onto typed primitives** ([jevons](https://github.com/marcelocantos/jevons)) — pigeon dependency bumped to v0.18.0 (cross-language E2E, one-time-token pairing, multi-client relay, ngtcp2, drain-window protocol) and then v0.19.0 (PairingArtifact + PairingHost + CredentialStore). 13-step migration plan documented in `docs/plans/pigeon-migration.md`. **Server side (T14.1)**: replaces bespoke X25519 with `pigeon.PairingHost`; `internal/server/credentials.go` persists `*crypto.PairingRecord` at `~/.jevons/credential.json`; `internal/server/pairing.go` rewrite. **iOS side (T14.1)**: `PigeonAccount` + env-var ingest + artifact bridge mode; bundles `web/` in the app and routes to artifact-driven `WebUIView`; web bridge global renamed to `window._jevonsTransport`. UX polish: red-car theme with higher-contrast dark mode, safe-area inset on input bar, iPad kept awake while jevon is in foreground (`UIApplication.shared.isIdleTimerDisabled` for car-mounted always-on use). Env-var deploy path documented: `xcrun devicectl device process launch --environment-variables PIGEON_PAIRING_ARTIFACT="$(pigeon pair --relay=...)"` lets developer deploys connect without a QR scan

### Tough Challenges Overcome

- **Bitdefender/Little Snitch silently filter outbound TCP/1433** — detail in [private week 2026-04-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-26.md)
- **SQL Server 2025 Developer disables TCP/IP by default** — detail in [private week 2026-04-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-26.md)
- **cmd.exe quoting eats `-Q` strings with backslashed paths and embedded SQL single** — detail in [private week 2026-04-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-26.md)
- **fd leak in spyder bridge `_lockdown` callers** ([spyder](https://github.com/marcelocantos/spyder)): pymobiledevice3's lockdown clients were being acquired without explicit close, accumulating across reservation lifetimes until the daemon hit per-process fd limits during long autoawake supervisor runs. Fix in 🎯T27 wraps every lockdown acquisition in a context manager and adds resource-leak regression tests asserting open fd count returns to baseline after a full reservation acquire/release cycle
- **transport vtable mismatch broke HTTP backend** ([mcpbridge](https://github.com/marcelocantos/mcpbridge)): dispatch was calling `send_child` twice per outbound message (bytes then a bare `"\n"`) as a stdio micro-optimisation. Stdio pipes concatenate so it worked silently for years. The HTTP backend maps each sink call to a separate POST, so the trailing-newline send fired a one-byte POST that the server rejected with 400. Diagnosis required the e2e HTTP reload test; fix was a structural correction — dispatch now copies into a scratch buffer and delivers one sink call per complete message, honouring the message-oriented vtable contract
- **mnemo `windows-11-arm` runner is paid-tier-only** ([mnemo](https://github.com/marcelocantos/mnemo)): cross-compiling `windows/arm64` on a free-tier GitHub Actions runner blocked v0.23.0. Fix swaps to `llvm-mingw` cross-compilation on `ubuntu-latest`, producing identical PE binaries without paying for the ARM runner
- **PyInstaller onefile is ~4 s slow per invocation** ([ytt](https://github.com/marcelocantos/ytt)): every CLI invocation extracted an ~11 MB archive to a tmpdir before starting Python. Fix: switch to `--onedir`, ship `dist/ytt/` (binary plus a sibling `_internal/` dir) in the tarball; the Homebrew formula moves both into `libexec` and symlinks just the binary into `bin`. Hot startup drops to ~100 ms (~40x), cold to ~900 ms
- **Indexer races between background HEAD walk and foreground tool calls** ([sawmill](https://github.com/marcelocantos/sawmill)): the gitindex SQLite store was being written from a background goroutine doing first-parent commit ingest while foreground MCP tool calls also wrote nodes. Result was sporadic `database is locked`. Fix tightened concurrency: `busy_timeout=5000`, `MaxOpenConns=1`, and switched the blob INSERT to `INSERT OR IGNORE` — race becomes a no-op rather than an error
- **One-time tokens vs concurrent `pair_hello` race** ([pigeon](https://github.com/marcelocantos/pigeon)) — first iteration of typed pairing primitives initially had `PairingArtifact` resolve with the live record before the ceremony state machine consumed the token. Hardened the `PairingHost.complete()` boundary so artifact-yielded credentials see the post-token-consumption state, not the optimistic pre-state

Contributor: Marcelo Cantos

---

## Tooling

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Eleven Releases: Windows + Federation + Idempotency (62 commits)

**The biggest single effort of the week.** Continued from last week's v0.21.0 with eleven more minor releases (v0.22.0 through v0.32.0):

- **Windows installer trio** (v0.22.0 → v0.24.0): Inno Setup MSI with double-click installation, `MSYS_NO_PATHCONV=1` to stop MSYS path-mangling the `.iss` arguments, dist staged next to the `.iss` file; ARM64 cross-compilation via `llvm-mingw` on `ubuntu-latest` rather than the paid `windows-11-arm` runner; suppress the Windows console window so `mnemo serve` runs without a visible cmd.exe
- **Windows Service revival** (v0.25.0, 🎯T32): per-user Registry registration under `HKCU\Software\mnemo` rather than `HKLM` (escapes admin-only install). `service_windows.go` + `service_other.go` separate the platform-specific code; uninstall flow drops `unregister-mcp` (which assumed admin)
- **Auto-migrate legacy stdio MCP registrations** (v0.26.0): users who installed mnemo when it shipped as a stdio proxy get auto-redirected to the HTTP transport on `mnemo serve` startup, with the previous `~/.claude.json` registration rewritten in-place; backup written first
- **Trim mnemo_status defaults** (v0.27.0): removes high-cardinality fields from the default response so MCP context stays cheap; opt-in via parameter for the verbose form
- **`mnemo diagnose` subcommand** (v0.28.0): one-shot startup probe that reports config validity, DB schema version, indexer health, watcher state, federation peer reachability — used by `/waw` and `/cv`
- **Federation across linked instances** (v0.29.0, 🎯T15): mTLS endpoint file (self-signed ECDSA P-256 cert+key at `~/.mnemo/endpoint/{cert,key}.pem`, key mode `0600`, regenerate on corrupt/expired with `slog.Warn`); peer cert allowlist under `~/.mnemo/peers/<name>.pem` (malformed entries skipped with warning rather than blocking); `linked_instances` config validation (duplicate name, missing fields, non-https scheme, peer cert resolution); `mnemo print-endpoint` subcommand emits cert.pem to stdout for paste-distribution
- **Eight targets shipped in parallel** (v0.30.0): four new MCP tools — `mnemo_session_structure` (full tree of an indexed session), `mnemo_tool_result` (look up a specific tool-call's result by uuid), `mnemo_get_memory` (read auto-memory MD files via the daemon), `mnemo_locate_uuid` (find any entry by UUID across sessions); idempotent indexer (🎯T35) — UNIQUE constraint on `(session_id, entry_uuid)` plus `INSERT OR IGNORE`, dedupe migration for old rows; launchd PATH for the compactor (🎯T37) so `claude -p` is found without shell wrapper; structured per-tick watcher logging (🎯T38)
- **At-a-glance project view + summary review worker** (v0.31.0, 🎯T40 + 🎯T41): `mnemo_repos` returns the CLAUDE.md summary (first paragraph) and last-commit date for every tracked repo, so `/waw` and the active-projects table can populate without scanning each tree. Periodic CLAUDE.md summary review worker driven by cheap signals (mtime + size deltas) — re-summarises only the repos whose docs actually changed, throttled to once per hour per repo
- **Streamable-HTTP MCP keepalive** (v0.32.0): 30 s heartbeat pings on streamable-HTTP MCP streams to keep keepalive sessions warm against intermediaries that close idle connections; reliability fix — no public-surface change. Also retroactively catalogues `mnemo_rework_history` in STABILITY.md (missed by v0.31.0)

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Ten Releases: KeepAwake → pmd3-bridge Migration (80 commits)

The pmd3-bridge migration started at the very end of last week's report; this week ships the result and the polish through ten minor releases:

- **Python pmd3-bridge over Unix domain socket** (🎯T25.1): FastAPI + uvicorn over UDS at `/tmp/pmd3-bridge.sock`, one-shot RPC for screenshot / app lifecycle / power-assertion / device_power_state; PyInstaller bundle so end users don't need `uv` installed
- **Go bridge client + supervisor** (🎯T25.2): `pmd3bridge` package with a typed `Client` (HTTP/1.1 over a Unix-socket `DialContext`), a `Supervisor` that owns the bridge subprocess lifetime and restarts on health-check failure, schemas auto-derived from the FastAPI OpenAPI doc
- **Route iOS via the bridge with power-assertion autoawake** (🎯T25.3): replaces the iOS KeepAwake companion app with a server-side power assertion held while a reservation is alive
- **Bundle + retire the companion app** (🎯T25.4 + T25.5): `ios/KeepAwake/` and `internal/tunneld/` directories deleted; xcodegen dependency retired; pmd3-bridge bundled in release tarballs and the Homebrew formula
- **Bridge transport hardening** (🎯T26): bridge resource-leak regression test (T27), `resolveBridgeBinary` follows symlinks (T35); v0.13.0 prefers a paid Developer Program team for KeepAwake codesigning when both are available; v0.14.0 fixes the `UninstallApp` flag and bundles KeepAwake source into release tarballs (intermediate state — KeepAwake briefly returned for power-assertion edge cases)
- **iOS 17+ ScreenshotService + autoawake convergence** (v0.10.0): the iOS 17+ screenshot path migrated to `ScreenshotService`, replacing `device_screenshot` calls that were 17.0-specific
- **Bounded-timeout hotfix** (v0.15.0): every `devicectl` call now wraps in a deadline so a hung CoreDevice tunnel can't block the daemon indefinitely
- **CLI overhaul for Make-driven test infrastructure** (v0.16.0, 🎯T37): `Makefile` rules drive bridge unit tests via `uv run --extra dev`; `cliexit` constants realigned by gofmt; `TEST-REPORT.json` updated by Make rules
- **Post-v0.16.0 device + bridge cleanup bundle** (v0.17.0, T29/T30/T34/T35/T36): `device_power_state` handler fixed and Python unit tests added (T29); STABILITY.md reflects iOS 17+ screenshot support matrix (T30); `KeepAwake` install recovers from `ErrNoProviderFound` (Code=1002) (T34); `resolveBridgeBinary` follows symlinks with unit test (T35); `pmd3-bridge` retries transient `tunneld` probe failures (T36)
- **Autoawake wired-only filter** (v0.18.0, 🎯T29 parking): autoawake supervisor only acts on wired devices to avoid spurious wake calls for transient WiFi-only neighbours
- **CLI rough-edges + MCP heartbeat** (v0.19.0, 🎯T38 + 🎯T40): user-facing CLI ergonomics polished; MCP heartbeat at 30 s parity with mnemo's streamable-HTTP keepalive

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Six Releases: Set-Aside, Envelope Guard, Validation Split (46 commits)

Six minor releases (v0.18.0 → v0.23.0). The headline shift is rigour:

- **`set_aside` status with required rationale** (v0.20.0/v0.21.0, 🎯T18): adds a third life-state alongside `active` and `achieved` for targets that aren't right but shouldn't be retired without a record. Schema enforces a non-empty `rationale` field whenever `status: set_aside`
- **Lockfile out of project dir, keyed by parent inode** (v0.20.0, 🎯T19): `bullseye.yaml.lock` no longer pollutes the repo; daemon stores it under `~/.local/share/bullseye/locks/<parent-inode>.lock` so concurrent `/cv` runs across sibling worktrees don't collide
- **Structured rework payloads** (v0.21.0, 🎯T1.5): `rework` flow accepts structured `sawmill_failure` (file + violations) and `mnemo_history` (recent decisions + cwd + session refs) payloads from the upstream callers; the prose path stays available for ad-hoc invocation
- **Envelope-leak guard** (v0.22.0, 🎯T20): every target's `value` and `cost` envelopes are now machine-checked against parent envelopes — a child cannot have wider bounds than its parent. Acceptance tests cover the failure modes (child-exceeds-parent-on-low, child-exceeds-parent-on-high, identical-but-shifted, multi-level transitive). Released as part of v0.22.0 with the test suite gated on the guard passing
- **`validate_blocking` + `validate_warnings` split** (v0.23.0): `validate()` was conflating fatal graph errors (cycles, undefined references) with quality warnings (no observable, missing strategy block). Split into two functions; `## Frontier` markdown rendering now gates on `validate_blocking` only, so quality warnings don't suppress frontier output
- **`targets_priorities` SQLite writer + sync-priorities CLI** (🎯T3.1): downstream consumers (jevons' active-work dashboard, /cv scoring, mnemo cross-repo views) read priorities from a denormalised SQLite table maintained by `bullseye sync-priorities` rather than re-parsing every project's `bullseye.yaml`. Schema covers WSJF inputs (value, cost, urgency, frontier-position) plus computed score
- **Banner + legend on repo-scope frontier output** (v0.18.0, 🎯T16): the previously-cryptic frontier table now ships a header explaining the WSJF columns, status glyphs, and forks. Helps fresh agents pick up a project without docs hunt
- **Tunnel warnings on every mutation** (v0.24.0 ships post-window): `bullseye_put` warns if the modified target is part of a tunnel (no observable showcase exists between root and target). Filed and partially shipped within window

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — v0.9.0 + v0.10.0: HTTP Stack Expansion + Per-Worker Wake (15 commits)

Two minor releases plus frontier work between and after:

- **Channel exceptions** (🎯T18, v0.9.0): exceptions raised on a sender thread cross the channel boundary and surface on `recv` rather than vanishing into the scheduler. Implementation adds a typed exception cell on the channel; `send_exc(eptr)` analogous to `send`; `recv` unwraps and rethrows. Eliminates a silent-failure mode in pipeline code
- **Per-worker wake to eliminate thundering herd** (🎯T13, v0.10.0): the M:N scheduler used a single condvar per ready queue, waking every worker on every enqueue. Per-worker wake replaces it with a directed signal — only one worker wakes per ready event. Benchmarked 4-6x reduction in cross-core futex traffic on a 16-core M4 Max
- **Pull-based source abstraction stage 1** (🎯T17, v0.10.0): `Source<T>` trait with `pull()` semantics for streams that can backpressure their producer; converters between push and pull via bounded buffers
- **Ergonomic I/O wrappers** (🎯T3.1, v0.11.0 prep): `lines()`, `read_all()`, `read_until(delim)`, `write_all()`, `write_lines()`, all integrated with the channel exception flow so I/O errors surface via `recv_exc`
- **HTTP/2 server** (🎯T3.7): nghttp2 with cleartext + TLS variants, ALPN-selected HTTP/2 over `serve_tls`. ~1.7k lines of C++ wrapping nghttp2's session loop into the csp scheduler model
- **HTTP/1.1 client** (🎯T3.6): paired with the existing server; reuses the channel-based I/O wrappers
- **arena-based stack allocation for 100K+ imp density** (🎯T3.3): in-process arena replaces per-imp guard-page mmap when a workload declares high density (>100k concurrent imps); guard pages are kept for low-density mode where stack overflow detection matters more than allocation density. +0.6k lines
- **CI infrastructure**: flaky `Timeout-expiry` test fixed; CI job runtime bounded; T19 (arm64 sanitizer CI reliability) and T20 (fake_clock audit) raised
- **WIP**: stopped-agent partial implementations of WebSocket (T3.5) and QUIC (T3.8) preserved on branches for follow-on work

### [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) — Oracle Toolchain Bootstrap (8 commits, +5,069/-709)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-26.md).*
### [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) — v0.10.0 + v0.11.0: Git AST Index, Equivalence Pillar, Auto-Fix (15 commits)

Two minor releases compressing a lot of foundational work:

- **Git AST index** (🎯T10/T11/T12): `gitindex` package stores tree-sitter parse trees by git blob SHA in a normalised SQLite schema (`blobs`, `nodes`, `node_types`, `field_names`, `commit_files`, `indexed_commits`). Cursor-based tree walking; in-memory interning caches for type/field names. `Indexer` walks first-parent ancestry and parses supported blobs lazily, deduping by blob SHA across commits. `CodebaseModel.Load` opens the index and kicks off `IndexHead` in the background; `Close` tears it down. New MCP tools: `git_log` (commit history with file-change metadata), `git_diff_summary` (symbol-level diff between two refs — added/removed/modified functions and types per file), `git_blame_symbol` (when a named symbol was last modified and first introduced)
- **Semantic blame** (🎯T6): for functions, `git_blame_symbol` returns four commits: `introduced`, `last_modified`, `body_last_modified`, `signature_last_changed`. For types, just `introduced` + `last_modified`. Closes the last gap in the semantic git history pillar
- **Semantic bisect** (🎯T14): binary-searches first-parent ancestry between good and bad refs to find the commit where a structural predicate flipped, without running code. Predicates: `symbol_exists`, `function_has_param`, `type_has_field` (all with optional file scope). Only `O(log N)` commits parsed thanks to lazy indexing. Returns the flip commit + its parent + commit metadata + the responsible `SymbolChange` from `semdiff`
- **`semantic_diff` + `api_changelog` MCP tools** (🎯T13): structural AST-level diffing detecting symbol moves across files (same name, different path), renames (name changed but AST structure preserved), signature changes, key-level data format diffs for JSON/YAML, file-level moves (same blob SHA at different paths). Cross-file move matching via structural fingerprinting
- **Pattern equivalences pillar (🎯T1) — four sub-targets**:
  - **Storage** (T1.1): `equivalences` table; `teach_equivalence` (name + left/right + optional preferred direction), `list_equivalences`, `delete_equivalence`. Validation rejects identical patterns, invalid preferred_direction, missing fields
  - **Apply + check** (T1.2/T1.3): `apply_equivalence` rewrites all matches in the chosen direction with unified diff per file, stages PendingChanges via standard apply/undo flow; `check_equivalences` scans the codebase for matches of any equivalence's non-preferred side and reports each as a violation. Container deny-list (modules, function bodies, blocks, control-flow statements) prevents greedy placeholders from spanning multiple statements
  - **Transitive closure** (T1.4): equivalences form a graph; the closure is computed on demand via union-find. List shows `[taught]` and `[derived via transitive closure]` sections; check honours derived pairs when ≥3 patterns share a class with a unanimous preferred pattern; apply expands the source set to every pattern in the class. Conflicting preferences leave the class with no preferred pattern. Cycles naturally collapse — a third edge that closes a loop just unions things already in the same set
- **Diagnostic-driven auto-fix loop (🎯T3) — five sub-targets**:
  - **Storage** (T3.1): `fixes` table; `teach_fix` validates regex compiles, action JSON is parseable with exactly one of recipe/transform, every `${name}` placeholder resolves to a named capture
  - **Structured diagnostics** (T3.3): `diagnostics` MCP tool gains a `format` parameter; LSP `code` and `source` fields normalise the integer/string union via `json.RawMessage` parsing
  - **Convergence loop** (T3.2): pull diagnostics for the target file, match each against fix regexes, bind named captures, dispatch to `handleInstantiate` (recipe) or `handleTransform` (inline spec), apply via `handleApply` with `confirm=true` so the next iteration sees the change. Termination: clean / stuck / iteration_limit. Cycle detection tracks `(file, code, message)` signatures
- **Structured violation payloads** (🎯T24): `check_conventions`, `check_invariants`, `query` accept `format=json`. New `Violation`/`QueryMatch` schemas stable for downstream orchestrators. Backwards-compatible convention DSL: programs may return either `[]string` (legacy) or `[]ConventionViolation` (structured). Empty-result-set returns `"[]"` not prose for programmatic consumers
- **Multi-repo PR lifecycle** (🎯T27): `apply_multi_root_pr` MCP tool for orchestrating PRs across N repos in one logical change; closes the multi-repo arc with 🎯T5
- **Pure-Go tree-sitter swap** (🎯T7.0): runtime swapped from cgo bindings to `gotreesitter` so the binary builds without a C compiler; closes the cgo footgun

### [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) — Three Releases: HTTP Backend + Connection Schema (22 commits)

Three minor releases (v0.3.0 → v0.5.0):

- **Message-oriented transport vtable** (🎯T3.1): replaces the fd-based vtable (`read_fd`/`write_fd`/`read`/`write`) with `poll_fd`/`pump`/`send`. Each transport now owns its own framing; line-splitting moves into `transport_stdio.c`. Leaves a clean seam for non-fd transports
- **HTTP backend transport** (🎯T3.2): `transport_http.c` implements the new vtable against an MCP Streamable HTTP endpoint. Plain `http://` to localhost / 127.0.0.1 / ::1 only. POST-only (every outbound MCP message is a per-request POST). Response may be `application/json` (single reply) or `text/event-stream` (chunked SSE). MCP-Session-Id captured from the initialize response header and echoed; MCP-Protocol-Version on every request. No standing GET SSE stream. Single-threaded, no pthreads — internal self-pipe is the stable poll fd. File structured into clear sections (URL parsing, TCP connect, HTTP response parsing, chunked decoder, SSE parser, message queue, vtable impl) so pieces can split out later
- **Wire HTTP backend through main.c** (🎯T3.3): `--url URL` flag selects the HTTP backend in place of stdio `-- COMMAND`; mutually exclusive with stdio. `--config NAME` becomes required under `--url`. Structural fix: dispatch was calling `send_child` twice per outbound message (bytes then bare `"\n"`) — worked for stdio but broke HTTP (each call mapped to a separate POST). Dispatch now copies into a scratch buffer and delivers one sink call per complete message
- **Standalone fake HTTP MCP server** (`tests/fake_http_mcp.c`): used by the HTTP reload e2e test; listens on a configurable port, prints the bound port on stdout, serves initialize (plain JSON + session id), tools/list (chunked SSE with response event + list_changed notification)
- **Connection schema v2** (🎯T5.1): config schema ships connection metadata (kind, command/url, env, working dir, allowed-tools, env vars). v0.4.0 stabilises this as the canonical format
- **Unified `mcpbridge connect <path>` front door** (🎯T5.2 + T5.3): wrapper takes `mcpbridge connect <path>` rather than the previous shell-script glue. Docs reflect the new pattern
- **Brew source backend works under launchd** (🎯T2): the bug fix is in the formula service block, not in code — `EnvironmentVariables` for PATH so launchd can find the child binary
- **Bullseye standing-invariants Makefile hook**: rule runs gofmt/vet/build/tests and asserts a clean tree
- **Abandon T4 (dumb-T-piece rework)**: the original v2 wire-protocol draft (T4.1) is reverted in favour of the connection-schema-driven model

### [marcelocantos/doit](https://github.com/marcelocantos/doit) — Three Releases: Threat Model + L3 Audit Chain (27 commits)

Three minor releases (v0.7.0 → v0.9.0):

- **`--help-agent` flag** (🎯T28, v0.7.0): agent-guide emission built into the binary
- **Threat model documented + linked from STABILITY.md** (🎯T32, v0.8.0): full threat model document covers tier-0 script gates, tier-1 stable-cap policy, tier-2 ledger-and-elicit, tier-3 elicit-only, the L3 prompt-injection surface, and the audit-chain integrity invariants. Every load-bearing knob in the threat model is now surfaced by `doit_check_config` (🎯T33)
- **Per-project-root learned durations** (🎯T29): `DurationStore` keys aggregations by `(project_root, cap, subcmd)` rather than globally. Same command in two different projects has independent learned histories, since shapes diverge (e.g. test runs vary by codebase)
- **`rm` tier reflects reversibility via git-tracked status** (🎯T30): `rm <path>` on a git-tracked file is reversible (git restore) — tier-1; on an untracked file it's destructive — tier-2 elicit. Removes the static-list approach
- **Startup warning for execution-adjacent sibling MCP servers** (🎯T34): if doit detects sawmill, mnemo, or other execution-capable MCP servers loaded in the same Claude session, it emits a structured warning so users know there are bypass paths
- **L3 prompt-injection surface enumerated + hardened + corpus** (🎯T35): every L3 elicitation prompt is mapped against attacker capabilities (e.g. crafted command messages, encoded SQL, embedded markdown), the prompt template is hardened with anchored constraints, and a regression test corpus exercises every known bypass attempt
- **Elicitation outcomes + L2 promotions in the audit chain** (🎯T36, v0.9.0): every elicitation (decision, rationale, time-to-decide) lands in the audit log keyed to the gated command. L2-tier promotions (a previously-elicited capability becoming stable for this project root) leave audit-trail entries
- **L3 chain-of-evidence in the audit log** (🎯T37): every gated execution carries the upstream policy decisions and elicitation outcomes that authorised it. Reconstructable post-hoc audit trail
- **`doit_audit_query` MCP tool** (🎯T38): filtered postmortem lookups over the audit log — by capability, subcmd, project root, time range, outcome. Powers postmortem workflows in /cv and /waw
- **Capture stdout/stderr excerpts for failure-mode commands** (🎯T39): when a gated command fails, the audit entry now carries head + tail excerpts of stdout and stderr (~1 KB each, configurable). Enough to diagnose without re-running

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) — Three Releases: Typed Pairing Primitives (15 commits)

Three minor releases (v0.18.0, v0.19.0, v0.20.0):

- **`PairingArtifact` + `CredentialStore` + `PairingHost`** (🎯T1.2, v0.19.0): typed primitives that obsolete jevons' bespoke X25519 + ad-hoc QR JSON. `PairingHost.MintArtifact()` issues a structured `PairingArtifact` carrying the relay URL, instance ID, server cert hash, and a one-time token. `CredentialStore` is the device-side persistence interface (Keychain on iOS, file on macOS, KeyStore on Android). `ConnectWithArtifact` is the client-side counterpart that takes an artifact and produces a live `PigeonConn`
- **Folded `cmd/pigeon-pair` into `pigeon pair` subcommand** (v0.19.0): one binary rather than two; the subcommand emits an artifact in `--format=text|json|qr`
- **Swift `PigeonConn.connect(artifact:)` + Kotlin `connectWithArtifact`**: language-native ergonomics matching the Go API
- **Pairing artifact lifecycle guide** (🎯T1.3): documents the full mint → distribute → ingest → connect flow with worked examples for QR, env-var, and developer-deploy paths
- **Stabilise root test suite under bulk load** (🎯T18): test-suite parallelism caused intermittent port collisions; fix reserves dynamic ports per-test from a shared pool
- **Cross-language confirmation code E2E flake fix** (🎯T20): timing race between Swift confirmation-code generation and the cross-language assertion; fix tightens the synchronisation point
- **Kotlin `PairingCeremonyMachineTest` regenerated** (🎯T19): for split sub-machines (the Swift refactor from last week is mirrored in Kotlin)

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — Initial Open-Source Releases (14 commits)

YouTube transcript CLI — three releases plus the `/open-source` skill applying:

- **Initial release** (v0.1.0): `ytt <video-or-playlist-url>` extracts transcripts via `youtube-transcript-api`, with optional Anthropic-vision auto-tagging of frames. Companion playlist-ingest scripts (`ytt-playlist-ingest.sh`) for batch ingest into Obsidian via `ytt-to-obsidian` filter
- **PyInstaller bundle** (v0.2.0): standalone single-binary distribution; release workflow grants `contents: write` to the build job for upload; release pipeline checks out `master` not the tag for Homebrew formula regeneration
- **`--onedir` for fast startup** (v0.3.0): v0.2.0's `--onefile` took ~4 s per invocation extracting the ~11 MB archive to a tmpdir each run. `--onedir` keeps Python + deps alongside the binary; **hot startup ~100 ms (~40x), cold ~900 ms**. Tarball ships `dist/ytt/` (binary + `_internal/`); Homebrew formula moves both into `libexec` and symlinks the binary into `bin`
- **PyPI publish job dropped** (v0.4.0 prep): hCaptcha outage on the trusted-publisher setup defers PyPI; sdist + wheel still attached to GitHub releases for `pipx install <url>` users
- **Obsidian graph node label improvements**: ingested files get human-readable graph labels rather than UUID stems

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — v0.2.0: macOS Clipboard Delivery (7 commits)

- **`convert_to_clipboard` with RTF + HTML + plain text** (🎯T7): one atomic NSPasteboard transaction. The convert pipeline grows `Render` / `RenderFile` so callers obtain the assembled HTML page without invoking Prince; the new `clipboard` package builds on that to put RTF + HTML + plain-text representations on the macOS pasteboard in a single `declareTypes:` / `setData:forType:` transaction. RTF and plain text derived in-process from HTML via `NSAttributedString` — eliminates the textutil + osascript pipeline (single-rep, no commit confirmation, lossy round-trip). NSPasteboard's synchronous API guarantees `Write` returns only after `changeCount` advances
- **`--to-clipboard` CLI flag + `convert_to_clipboard` MCP tool**: parity surfaces for human and agent invocation
- **Round-trip test via cgo helper**: reads each pasteboard representation back and asserts the RTF carries the `{\rtf` signature and that plain text doesn't leak raw RTF source
- **Linux/Windows backends**: return `ErrUnsupported` pending follow-up
- **Bullseye standing-invariants hook**: gofmt/vet/build/tests Makefile rule

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — v0.8.0 + v0.9.0: Public Probes (5 commits)

- **`SessionExists` + `SessionJSONLPath` public probes** (🎯T2): external tools can now check if a Claude Code session ID exists and resolve its JSONL transcript path without re-implementing the discovery walk. Used by `/waw`, `/cv`, mnemo's compactor

### [marcelocantos/mk](https://github.com/marcelocantos/mk) — ccache (1 commit)

- **Wrap cc/cxx with ccache in std libs**: cross-project latency reduction continued from last week

### [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) — Stale linker cleanup (1 commit)

- **Drop stale zlib linker**: the tree's link line carried zlib from a long-dead dep; removed

### [marcelocantos/homebrew-tap](https://github.com/marcelocantos/homebrew-tap) — ytt formula (1 commit)

- **Add ytt formula** (v0.1.0): paired with the open-source ytt release

---

## Game Projects

### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) — bgfx Port + Jolt Physics + Auto-Drive (12 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-26.md).*
### [squz/ge](https://github.com/squz/ge) — Spyder-Driven Matrix Cells + Wire Protocol + Android Text (15 commits)

Continued mobile-engine work:

- **Spyder-driven matrix cells** (🎯T33.1–T33.5): `smoke-test.sh` collapses per-platform branches onto the spyder CLI (T33.1); `matrix-cell.sh` wraps cells in `spyder run` for race-safe parallel reservations (T33.2); visual regression via spyder screenshot + diff against baselines, with `make update-baselines` for refresh (T33.3); soak cells call `spyder device_power_state` post-run, distinct exit code when device fell asleep (T33.4); spyder pool config committed and `make pool-init / pool-drain` rules added (T33.5)
- **Auto-pause audio when backgrounded** (🎯T7): SDL3 audio device suspension on app background, resume on foreground
- **`ge_wire.yaml`** (🎯T11.1): the wire protocol (player ↔ session-host) declared in YAML; emits Go/Swift/Kotlin/C/TS bindings via the protogen pipeline (rewritten for pigeon-as-it-is v0.20.0)
- **Android text rendering** (🎯T30.1–T30.3): vendor SDL_ttf for Android consumers (T30.1); Android FontLoader so Text-using consumers link cleanly (T30.2); `sample/tiltbuggy` Android consumes ge via `add_subdirectory(ge)` end-to-end (T30.3)
- **Triangle non-commercial licence clarified** (🎯T31): docs explicit about Triangle's non-commercial + opt-in model
- **GPU H.264 colour-space conversion** (🎯T32): SDL3 YUV textures replace CPU YUV→RGB
- **Bullseye state consolidation v2**: T11 family rewrite, T33 family filed, stale targets retired; second consolidation supersedes #38

---

## Libraries & Infrastructure

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Pigeon Migration onto Typed Primitives (9 commits)

- **Pigeon dependency bumped** v0.18.0 → v0.19.0 (Go + iOS SPM): cross-language E2E parity, one-time-token pairing, multi-client relay, ngtcp2 QUIC, drain-window protocol, `PairingArtifact`/`PairingHost`/`CredentialStore` primitives. iOS SPM dependency switched from `Tern` (renamed) to `Pigeon`
- **Server-side T14.1**: replaces bespoke X25519 keypair management with `pigeon.PairingHost`. `internal/server/credentials.go` persists the server-side `*crypto.PairingRecord` at `~/.jevons/credential.json` (single-credential for now; multi-device deferred). `internal/server/pairing.go` rewrite. `MintArtifact()` wraps `PairingHost`
- **iOS-side T14.1**: `PigeonAccount` + env-var ingest + artifact bridge mode; bundles `web/` in the app and routes to artifact-driven `WebUIView`; web bridge global renamed to `window._jevonsTransport`
- **Env-var deploy path**: `xcrun devicectl device process launch --device <UDID> com.marcelocantos.jevon --environment-variables PIGEON_PAIRING_ARTIFACT="$(pigeon pair --relay=https://carrier-pigeon.fly.dev --instance=$(uuidgen) --format=text 2>/tmp/pigeon-server.json)"`. iOS app reads `PIGEON_PAIRING_ARTIFACT` on first launch, persists via `KeychainCredentialStore`, then connects without a QR scan. `jevonsd --add-credential` ingests the server-side record
- **UX polish**: red-car theme with higher-contrast dark mode; safe-area inset on input bar; iPad kept awake while jevon is in foreground (`UIApplication.shared.isIdleTimerDisabled` for car-mounted always-on use)

---

## Strategic Planning & Documentation

### [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) (3 commits)

- Last week's report (2026-04-13…19) added; "Journey So Far" rewritten and Metrics methodology document split out into `docs/methodology.md`

### [marcelocantos/skills](https://github.com/marcelocantos/skills) (11 commits)

- Skills sync commits from `~/.claude/skills/`. Updates include `/open-source`, `/release`, `/cv`, `/waw`, `/push`, `progress-report` (this skill), and the YouTube-ingest `/ytt`

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only. Git log queried with `--since="2026-04-20 00:00:00" --until="2026-04-27 00:00:00"` (inclusive Mon-Sun calendar boundary, local time AEST) **with** `--all`, so commits on merged feature branches and worktree branches that subsequently merged via squash are visible.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 20 |
| Total commits | 355 |
| Total lines added | +90,565 |
| Total lines removed | −18,977 |
| Net new lines | +71,588 |
| Net new lines (excl. vendored / generated dist) | ~+95,000 |
| File changes | 1,761 |
| New files created | ~360 |
| Languages | Go, Rust, C, C++, Python, C#, Swift, Kotlin, TypeScript, JavaScript, Objective-C, SQL, Inno Setup, YAML, Makefile, PowerShell, Bash, HTML, CSS |
| Contributors | 1 (Marcelo Cantos) |

Note: csp's +11,816/-332 includes regenerated amalgamated `dist/` C output for HTTP/2 (~6 k of nghttp2-derived header source) and the vendored nghttp3/picotls scaffold for HTTP/3 (the QUIC WIP). sawmill's +14,909/-1,605 includes the gitindex schema migration (small) plus regenerated amalgamated artefacts. spyder's +35,773/-7,031 includes a PyInstaller-bundled Python pmd3-bridge (~7-8 k of bundled site-packages tracked because the build is reproducible from `pyproject.toml` but the artefacts are committed for release-tarball cohesion). HMS's +5,069/-709 is all first-party Python + C# (oracle-bridge, oracle-client, oracle/db).

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 80 | 431 | +35,773 | -7,031 | +28,742* |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 62 | 227 | +17,224 | -1,241 | +15,983 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 46 | 136 | +6,975 | -1,580 | +5,395 |
| [marcelocantos/doit](https://github.com/marcelocantos/doit) | 27 | 179 | +7,977 | -513 | +7,464 |
| [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) | 22 | 74 | +5,250 | -1,270 | +3,980 |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 15 | 129 | +14,909 | -1,605 | +13,304** |
| [squz/ge](https://github.com/squz/ge) | 15 | 58 | +4,140 | -1,321 | +2,819 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 15 | 98 | +11,816 | -332 | +11,484*** |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 15 | 79 | +5,429 | -1,744 | +3,685 |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 14 | 31 | +1,309 | -268 | +1,041 |
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 12 | 60 | +2,979 | -673 | +2,306 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 11 | 40 | +567 | -1,280 | -713 |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 9 | 28 | +678 | -438 | +240 |
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | 8 | 75 | +5,069 | -709 | +4,360 |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 4 | 14 | +581 | -133 | +448 |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 5 | 15 | +329 | -19 | +310 |
| [marcelocantos/pageflip](https://github.com/marcelocantos/pageflip) | 3 | 38 | +3,309 | -1,567 | +1,742 |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 3 | 22 | +1,933 | -1,199 | +734 |
| [marcelocantos/homebrew-tap](https://github.com/marcelocantos/homebrew-tap) | 1 | 1 | +60 | -0 | +60 |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | 1 | 5 | +85 | -63 | +22 |
| [marcelocantos/mk](https://github.com/marcelocantos/mk) | — | — | — | — | — †|

\* spyder net includes ~7-8 k of PyInstaller-bundled Python site-packages committed for release-tarball cohesion.  
\** sawmill net includes regenerated AST-fixture goldens and a ~3 k tree-sitter pure-Go runtime drop-in.  
\*** csp net includes ~6 k of vendored amalgamated nghttp2/nghttp3/picotls header bundle for the dist/ release artefact.  
† mk had no Marcelo commits in the strict 2026-04-20…26 local-time window (the ccache wire-up landed earlier).

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | ~80 | Oracle: DFM parser corpus (1,282/1,307), semantic class-mapping, locator cascade, OCR adapter, db backend (sqlcmd argv builder + pymssql connection-args builder), baseline alignment, fingerprint, snapshot lifecycle, restore round-trip; **1,335 passing** end-of-window |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | ~75 | gitindex round-trip, Indexer first-parent walk, semantic_diff seven edit operations, semantic blame body/signature attribution + never-changed + type-skip, semantic bisect (forward/reverse, three predicate kinds, no-flip + non-ancestor errors), equivalence storage round-trip + upsert + validation, apply left↔right round-trip + path filter, check violation reporting + skip-no-preferred + transitive-derived honouring, transitive closure (derived, conflict-suppression, cycle), fix storage validation + delete + persistence + capture-binding, structured violations (legacy + JSON modes for conventions/invariants/query, empty-as-`[]`), structured diagnostics with code/source normalisation across LSP shapes |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~70 | pmd3-bridge unit + integration, autoawake supervisor short-circuit on cancelled ctx, fd-leak regression on bridge `_lockdown`, bounded-timeout devicectl, `resolveBridgeBinary` symlink resolution, `device_power_state` Python unit tests, autoawake wired-only filter |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~50 | HTTP/1.1 client tests, HTTP/2 cleartext + TLS server tests with ALPN negotiation, channel exception delivery (sender, receiver, mid-pipeline), per-worker wake convergence + thundering-herd absence, ergonomic I/O wrappers (lines/read_all/read_until), pull-based source backpressure |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~45 | Endpoint mTLS round-trip, peer-cert allowlist parsing, linked-instances validation (duplicate name, missing fields, non-https, peer cert resolution), idempotent indexer migration + dedupe, watcher tick logging, `mnemo_session_structure` / `mnemo_tool_result` / `mnemo_get_memory` / `mnemo_locate_uuid`, CLAUDE.md summary review worker (mtime/size deltas), streamable-HTTP heartbeat |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | ~35 | Envelope-leak guard acceptance (child-exceeds-low/high, identical-but-shifted, multi-level transitive), validate_blocking vs validate_warnings split, set_aside status with rationale required, structured rework payload accepts sawmill_failure + mnemo_history, lockfile parent-inode key, frontier banner rendering |
| [marcelocantos/doit](https://github.com/marcelocantos/doit) | ~30 | Audit chain L3 chain-of-evidence, elicitation outcomes capture, L2 promotion records, doit_audit_query filtering, stdout/stderr excerpt capture, prompt-injection corpus, per-project-root duration aggregation, rm-tier git-tracked reversibility |
| [marcelocantos/mcpbridge](https://github.com/marcelocantos/mcpbridge) | ~25 | transport_http e2e (initialize round-trip with plain-JSON + session id capture, tools/list with chunked SSE carrying response + list_changed events, session id propagation, URL validation: non-http / non-loopback / out-of-range-port / default-path, connection-refused), HTTP reload e2e via fake_http_mcp |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | ~20 | PairingArtifact mint + ingest + connect, CredentialStore Keychain/file/KeyStore implementations, PairingHost lifecycle, Swift PigeonConn.connect(artifact:) round-trip, Kotlin connectWithArtifact, regenerated PairingCeremonyMachineTest for split sub-machines, root suite stable under bulk load |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | ~8 | Clipboard round-trip via cgo helper (RTF signature, plain-text non-leak), convert_to_clipboard MCP tool, Linux/Windows ErrUnsupported |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~6 | SessionExists positive/negative/race, SessionJSONLPath resolution, file-not-found |
| **Total** | **~444** | |

### Daily Activity

![Daily active repositories](daily-activity-2026-04-26.svg)

---

## Ideas & Innovations

### Native pymssql + Lazy SSH Tunnel for Mac-to-VM-SQL ([HMS oracle](https://github.com/Health-Management-Systems/hms))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-26.md).*
### Semantic Blame with Body/Signature Attribution ([sawmill](https://github.com/marcelocantos/sawmill))

`git blame` answers "who changed this line"; `git log -L` answers "what's the history of this region"; neither answers "when did this function's body last change versus its signature?". Sawmill's `git_blame_symbol` reports four commits per function: `introduced`, `last_modified`, `body_last_modified`, `signature_last_changed`. **The insight is that signature changes have different audit and migration consequences than body changes**: a body change rarely requires consumer updates, a signature change usually does. The implementation walks first-parent ancestry over the lazy semantic git index, comparing AST node structure (not text) to attribute the change to body vs. parameter list. For non-function symbols (types), only `introduced` + `last_modified` are returned — body and signature distinctions don't apply.

### Semantic Bisect Without Running Code ([sawmill](https://github.com/marcelocantos/sawmill))

`git bisect` runs the test suite at each midpoint. For "when did this function lose its `ctx` parameter?" or "when did this type stop having a `Foo` field?" you don't need to run anything — you just need to evaluate a structural predicate over the AST at each commit. Sawmill's `git_semantic_bisect` does exactly this: predicates are JSON DSL (`symbol_exists`, `function_has_param`, `type_has_field`) with optional file scope; binary search walks first-parent ancestry; only `O(log N)` commits get parsed thanks to the lazy semantic git index. **The output is the flip commit, its parent, the metadata, and the responsible `SymbolChange`** from semdiff. For "when did this break" questions about API surface, this is faster than tests and far cleaner than reading commit messages.

### Transitive Closure on Pattern Equivalences via Union-Find ([sawmill](https://github.com/marcelocantos/sawmill))

When you teach sawmill "`x.unwrap()` ↔ `x?` (prefer right)" and "`x.unwrap()` ↔ `x.expect(\"...\")` (no preference)", you'd like the system to figure out that `x.expect("...")` should also be rewritten to `x?`. The implementation uses **union-find to compute the transitive closure on demand**: equivalence pairs form edges in a graph; the closure operation unions the components; a class with a unanimous preferred pattern propagates that preference to every member. Conflicting preferences (one taught pair prefers A, another prefers C in the same class) leave the class with no preferred pattern — the system **silently neutralises the contradiction** rather than picking one. Cycles naturally collapse: the third edge that closes a loop just unions things already in the same set, so the closure terminates. The result is composable equivalence schemas that scale to large rule libraries without a brittle ordering invariant.

### Diagnostic-Driven Auto-Fix Loop with Cycle Detection ([sawmill](https://github.com/marcelocantos/sawmill))

Linter "fix-on-save" is per-tool and per-IDE; structural fixes (rename, signature change, parameter substitution) live in refactoring tools; the gap between them is "respond to a structured LSP diagnostic with a structural transform". `auto_fix` closes that gap: pull diagnostics for the target file (LSP `code` + `source` fields, normalised across the LSP integer-or-string union); for each diagnostic, find the first `teach_fix` regex with a match; bind named captures; dispatch to a recipe (instantiate) or transform; apply via the standard pending-change flow with `confirm=true`. **Termination is the interesting part**: clean (no diagnostics), stuck (no fix applied this iteration), or iteration-limit (default 10). **Cycle detection tracks `(file, code, message)` signatures** — if the same diagnostic flips back and forth across iterations (ping-pong between two competing fixes), the loop bails rather than thrashing.

### Connection-Schema-Driven Wrapper as the Front Door ([mcpbridge](https://github.com/marcelocantos/mcpbridge))

Earlier mcpbridge invocations were a tangle: `mcpbridge --config-name foo command-flags...`, with the "command" being a child-process spec (stdio) or a URL (HTTP) and a config file picking some defaults. v0.5.0 collapses this to **`mcpbridge connect <path>`** — a single wrapper command that resolves a connection by name from `~/.config/mcpbridge/connections.yaml` (schema v2: `kind`, `command`/`url`, `env`, working dir, allowed-tools). Stdio and HTTP backends become orthogonal selections inside the schema, not surface-level CLI variants. The launchd brew formula service block ships the right `EnvironmentVariables` so the daemon finds child binaries without a shell wrapper.

### Per-User Windows Service Registration ([mnemo](https://github.com/marcelocantos/mnemo))

Standard Windows Service registration writes to `HKLM\SYSTEM\CurrentControlSet\Services` — admin-only. For a per-user dev tool like mnemo, that's wrong: each user wants their own service running as their account, with their own `~/.mnemo/` data, and shouldn't need admin to install. v0.25.0 ships per-user Windows Service registration via **`HKCU\Software\mnemo` for the service config plus `schtasks /Create /SC ONLOGON` for the launch trigger** — no `HKLM`, no admin. The service runs as the user's account, reads the user's environment, and starts on login like a launchd LaunchAgent. Combined with the v0.22.0 double-click installer (also user-scope: `INSTALLDIR` defaults to `%LOCALAPPDATA%\Programs\mnemo`), end-to-end installation requires zero administrative interaction.

### Compile-Time Wire Protocol Across Five Languages ([squz/ge](https://github.com/squz/ge))

ge's wire protocol previously lived as a hand-written struct in C, manually mirrored to Go (server) and Swift/Kotlin (clients). Drift was inevitable; one-end-only changes shipped as silent client/server mismatches. v0.0.x ships **`ge_wire.yaml`** — a single declarative source of truth — feeding the protogen pipeline (rewritten this week for pigeon-as-it-is v0.20.0) that emits Go/Swift/Kotlin/C/TypeScript bindings at build time. Schema changes become compile errors on the lagging side, not runtime parse errors. The bindings include not just struct definitions but encode/decode helpers, wire-format validators, and a deterministic versioning strategy. The same generator powers pigeon's pairing artifact format, so the cross-project boundary stays consistent.

### Lazy-Resolved External Resource Cache for SQL Backups ([HMS oracle](https://github.com/Health-Management-Systems/hms))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-26.md).*
## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| mnemo 11 releases | 18-28 | Inno Setup + MSYS path-conversion + dist-staging double-click installer; cross-compile Windows ARM64 via llvm-mingw; per-user Registry Windows Service + schtasks ONLOGON; auto-migrate legacy stdio MCP registrations; mTLS endpoint cert lifecycle (ECDSA P-256, 0600 mode, regen-on-corrupt); peer-cert allowlist with malformed-skip; linked-instances validation; idempotent indexer schema migration; four new MCP tools (session_structure, tool_result, get_memory, locate_uuid); CLAUDE.md summary review worker keyed by cheap signals; 30 s heartbeat keepalive |
| spyder 10 releases + pmd3 bridge migration | 14-22 | PyInstaller-bundled FastAPI + uvicorn pmd3-bridge; Go bridge client + supervisor with subprocess lifecycle; iOS power-assertion server-side replacing companion-app autoawake; KeepAwake + tunneld removal; CI hotfix for autoawake supervisor; bridge fd-leak audit + regression tests; symlink-following resolveBridgeBinary; bounded-timeout devicectl; iOS 17+ ScreenshotService; Make-driven test infrastructure overhaul; bridge transport hardening with retry on transient tunneld probe failures |
| HMS oracle toolchain bootstrap | 14-20 | Delphi DFM parser (1,282/1,307 corpus) covering text-format edge cases; semantic tree builder with vendor-prefix matching and parent-rect composition; locator cascade with screenshot/OCR/UIA per-step caching; Apple Vision OCR coordinate-space adaptation; SendInput-based input primitives over HTTP with multi-monitor virtual-screen normalisation; SQL Server lifecycle (RESTORE/baseline/snapshot) with three transport pivots; pymssql + lazy SSH tunnel diagnosis (Network Extension filtering); cmd.exe quoting via PowerShell EncodedCommand; SQL Server Express vs Developer edition snapshot semantics |
| sawmill v0.10/v0.11 | 12-18 | Tree-sitter AST indexer with SQLite storage + blob-SHA dedup; first-parent commit walker; semantic diff with rename/move detection via structural fingerprinting; semantic blame with body/signature attribution via AST comparison; semantic bisect with binary search + lazy parsing; pattern equivalence storage + apply + check + transitive closure via union-find; teach/list/delete trinity for two new domain objects; structured diagnostic format with LSP code/source union normalisation; auto-fix convergence loop with cycle detection by `(file,code,message)` signature; multi-repo PR lifecycle |
| bullseye 6 releases | 8-12 | Envelope-leak guard with acceptance tests covering multi-level transitivity; validate split into blocking + warnings with frontier-rendering gate; set_aside status with required rationale schema check; structured rework payloads (sawmill_failure + mnemo_history); lockfile parent-inode key migration; SQLite priorities writer + sync-priorities CLI; banner + legend frontier rendering |
| csp v0.9/v0.10 | 8-12 | Channel exception delivery cross-thread; per-worker wake replacing condvar-broadcast (4-6x reduction in cross-core futex traffic); pull-based source abstraction with backpressure; HTTP/2 server (nghttp2 cleartext + TLS) with ALPN over csp scheduler; HTTP/1.1 client; ergonomic I/O wrappers; arena stack allocation for high-density imps; vendored amalgamated dist regeneration |
| doit v0.7/v0.8/v0.9 | 6-10 | Threat model document with L3 prompt-injection enumeration + hardened prompt + corpus; chain-of-evidence audit log linking elicitation outcomes to gated executions; doit_audit_query MCP tool with filtering; stdout/stderr excerpt capture for failure-mode commands; per-project-root duration learning; rm-tier reversibility via git status; startup warning for sibling MCP execution surfaces |
| mcpbridge v0.3/v0.4/v0.5 | 6-9 | Pure-C transport vtable from fd-based to message-oriented; HTTP transport with chunked decoder + SSE parser + self-pipe poll fd; URL validation (loopback + scheme + path + port); session id capture/echo; standalone fake HTTP MCP server in test suite; structural send_child fix |
| pigeon v0.18/v0.19/v0.20 | 5-8 | Typed pairing primitives (PairingArtifact + CredentialStore + PairingHost) cross-language; ConnectWithArtifact in Go/Swift/Kotlin; pigeon-pair fold into pair subcommand; pairing artifact lifecycle docs; cross-language confirmation E2E flake fix; Kotlin test regeneration for split sub-machines |
| ytt v0.1/v0.2/v0.3 | 3-5 | First open-source release via /open-source; PyInstaller onefile→onedir migration with Homebrew libexec layout; release workflow stabilisation; Obsidian graph node label improvements |
| stock-car-racing port + Jolt + auto-drive | 5-8 | Jolt physics integration (track as static collision body, dynamic car body settling); Pacejka tire model port from C# (Wheel/Drivetrain/VehicleDynamics) — not yet wired but ported; ge bgfx + ge::run + RenderHost migration of Stage 1-3 rendering with shaderc shader pipeline; smooth handoff blending between player and AI input via SmoothStep; player-toggleable auto-drive with three engagement entry points and YellowFlagManager interaction |
| ge spyder integration + wire protocol + Android text | 4-7 | Spyder-driven matrix cells across smoke-test/visual-regression/soak; pool config + Make rules; ge_wire.yaml protogen pipeline (5 languages); SDL_ttf vendoring + Android FontLoader for cross-platform text rendering; GPU YUV colour-space conversion via SDL3 textures |
| mnemo→pigeon migration in jevons | 3-5 | Server PairingHost adoption replacing bespoke X25519; iOS PigeonAccount + env-var ingest + artifact bridge mode; web/ bundling + WebUIView routing; env-var deploy path documentation; UX polish (theme, safe-area, idle timer disable) |
| vellum v0.2.0 clipboard | 2-4 | macOS NSPasteboard atomic transaction with three representations; in-process RTF + plain-text derivation via NSAttributedString; cgo round-trip helper for tests; CLI flag + MCP tool parity surfaces |
| claudia v0.8/v0.9 probes | 1-2 | Public probe surface for SessionExists + SessionJSONLPath |
| other (csp ccache rollouts, sqldeep linker cleanup, skills, progress-reports, homebrew-tap, jevons UX) | 2-4 | Small improvements across many repos |

### The Diversity Tax

Specialisms exercised this week:

- **Windows installer engineering** — Inno Setup MSI scripting, MSYS path-conversion gotchas, dist-stage layouts, llvm-mingw cross-compilation, per-user `HKCU` registration, `schtasks ONLOGON`, console-window suppression
- **mTLS / X.509 lifecycle** — self-signed ECDSA P-256 cert+key generation, peer cert allowlist with malformed-skip, regen on corrupt/expired, `linked_instances` validation, key file mode `0600` enforced on reload chmod
- **iOS power-assertion / device automation** — pymobiledevice3 + CoreDevice 17+, ScreenshotService, devicectl bounded timeouts, KeepAwake codesigning team selection, KeepAwake `ErrNoProviderFound` recovery, fd leak audit on `_lockdown` callers, autoawake wired-only filter, run-artefact lifecycle
- **PyInstaller deployment** — onefile vs onedir startup-cost trade-off, FastAPI + uvicorn bundling, Homebrew `libexec` layout for framework-style distribution
- **Delphi reverse engineering** — DFM text-format parser (string `+` continuation, `#N` control-char concatenation, typed numeric literals, set literals, item lists, child-index suffix), TPF0 binary detection, semantic class-mapping with vendor-prefix stripping, parent-rect composition for absolute coordinates
- **Apple Vision OCR engineering** — `VNRecognizeTextRequest` adapter returning top-origin pixel-space rather than Vision's bottom-origin normalised coords, fuzzy substring matching for OCR drift on Delphi UIs
- **SQL Server platform depth** — sqlcmd 18 encryption-by-default, `-h -1` column-header semantics, `Msg N, Level M` stdout error detection, FILELISTONLY → MOVE-clauses → REPLACE workflow, `_oracle_baseline` cross-side alignment, `CREATE DATABASE ... AS SNAPSHOT OF` Express edition restrictions, Developer Edition default-instance Shared Memory vs TCP, mixed-mode auth + sysadmin-role provisioning
- **Pure C engineering** — message-oriented transport vtable refactor, HTTP/1.1 over plain `http://` with chunked decoder + SSE parser, MCP-Session-Id header lifecycle, single-threaded self-pipe poll fd
- **Tree-sitter / AST indexing** — SQLite-backed normalised parse-tree storage with cursor-based walking and string interning, first-parent commit walker, lazy parsing with blob-SHA dedup across commits
- **Semantic diff and refactor detection** — structural fingerprinting for rename/move detection, key-level data format diffs for JSON/YAML, body vs signature attribution for blame
- **Union-find / graph algorithms** — detail in [private week 2026-04-26](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-26.md)
- **Network Extension diagnosis on macOS** — Bitdefender / Little Snitch / corporate VPN content-filter detection via the `nc` works / Python `socket.create_connection` fails asymmetry, lazy SSH tunnelling keyed by `Connection.name`
- **Bgfx + Jolt + ge engine integration** — RenderHost API migration, bgfx vertex/index buffer handles, lazy bgfx-resource init pattern, shaderc `.bin` shader pipeline, Jolt body-interface wrapping, Pacejka tire model port from C#
- **MCP transport architecture** — message-oriented vtable design, streamable HTTP transport, MCP-Session-Id semantics, connection-schema-driven wrapper, structured violation payloads with format negotiation
- **Linq / functional pipeline ergonomics** — pull-based source abstraction with backpressure, channel exception delivery, ergonomic I/O wrappers
- **Audit chain / threat-model engineering** — L3 chain-of-evidence linking elicitations to gated executions, prompt-injection corpus, per-project-root learned-duration aggregation, structured stdout/stderr excerpt capture
- **NSPasteboard atomic delivery** — RTF + HTML + plain text in one `declareTypes:setData:` transaction, in-process derivation via `NSAttributedString`

No single developer holds production-level expertise across Windows installer scripting + mTLS lifecycle + iOS power-assertion + PyInstaller deployment + Delphi DFM parsing + Apple Vision OCR + SQL Server platform depth + pure C transport engineering + tree-sitter AST indexing + semantic diff with refactor detection + union-find on equivalence graphs + macOS Network Extension diagnosis + bgfx/Jolt engine integration + MCP transport architecture + audit-chain engineering + NSPasteboard atomic delivery — concurrently.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| mnemo | 3-5 | Windows scope decisions (per-user Registry vs HKLM, schtasks vs service), federation peer model, idempotent indexer migration plan, summary review worker trigger model |
| spyder | 2-4 | KeepAwake → pmd3-bridge cutover sequence, paid-vs-free Developer Program signing trade-off, autoawake wired-only narrowing, CLI overhaul scope |
| HMS oracle | 3-5 | Three-pivot diagnosis (sqlcmd → SSH+EncodedCommand → pymssql+tunnel), tunnel-vs-direct architecture decision, locator cascade design, semantic vocabulary mapping |
| sawmill | 2-3 | Equivalence-pillar decomposition (T1.1-T1.4), auto-fix loop termination model, semantic blame body/signature split, structured-violation schema |
| bullseye | 1-2 | Envelope-leak guard scope, validate split (blocking vs warnings), set_aside status semantics, priorities-writer schema |
| csp | 1-2 | Per-worker wake design, channel exception model, pull-based source backpressure |
| doit | 1-2 | Threat-model authoring, L3 chain-of-evidence schema, prompt-injection corpus seeds |
| mcpbridge | 1-2 | Vtable shape (message-oriented), HTTP backend scope (loopback-only, POST-only) |
| pigeon | 1-2 | PairingArtifact / PairingHost / CredentialStore primitives shape, pair subcommand fold-in |
| stock-car-racing | 1-2 | Stage 1-3 port-forward strategy, Jolt + Pacejka split, auto-drive engagement model |
| ge | 1-2 | Spyder integration scope, wire-protocol declaration choice, Android text-rendering vendoring |
| ytt | <1 | Open-source readiness review, onefile/onedir trade-off |
| jevons | <1 | pigeon-migration sequence, env-var deploy path |
| other (vellum, claudia, skills, progress-reports, homebrew-tap, sqldeep) | 1-2 | NSPasteboard model, claudia probe surface, skill iterations |
| **Total** | **~20-32** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | Ramp-up cost |
|---------|------------|-----------------|--------------|
| mnemo | 18-28 | 27-42 | Inno Setup + MSYS-PATH + per-user Windows Service + schtasks + mTLS lifecycle + HTTP MCP transport + SQLite migrations + four new tools |
| spyder | 14-22 | 21-33 | pymobiledevice3 + iOS 17+ ScreenshotService + KeepAwake codesigning + PyInstaller + Go subprocess supervisor + Homebrew launchd |
| HMS oracle | 14-20 | 22-32 | Delphi DFM grammar + Apple Vision adapter + Windows SendInput + SQL Server platform depth + Network Extension diagnosis + pymssql + SSH tunnel + Mutagen-aware staging |
| sawmill | 12-18 | 18-27 | tree-sitter SQLite + first-parent walk + semantic diff + union-find on equivalence graphs + auto-fix loop with cycle detection + multi-repo PR orchestration |
| bullseye | 8-12 | 12-18 | Rust MCP SDK + envelope-leak invariant + validate split + structured-payload contracts + SQLite priorities writer |
| csp | 8-12 | 12-18 | C++ M:N scheduler internals + nghttp2 + ALPN + per-worker wake design + channel exception delivery + arena allocators |
| doit | 6-10 | 10-15 | Threat modelling + audit-chain engineering + prompt-injection corpus + duration aggregation + git-tracked reversibility |
| mcpbridge | 6-9 | 9-13 | Pure C transport refactor + HTTP/1.1 client with chunked + SSE + self-pipe poll fd + MCP-Session-Id semantics |
| pigeon | 5-8 | 8-12 | Typed cross-language pairing primitives + Swift PigeonConn.connect(artifact:) + Kotlin connectWithArtifact + cross-language E2E |
| ytt | 3-5 | 5-8 | PyInstaller + Homebrew + GitHub Actions release workflow |
| stock-car-racing | 5-8 | 8-13 | Jolt + Pacejka + bgfx + ge::run + RenderHost + shaderc + Unity ↔ C++ engine port |
| ge | 4-7 | 7-11 | Spyder MCP integration + protogen across 5 languages + SDL_ttf Android vendoring + SDL3 YUV textures |
| jevons | 3-5 | 5-8 | pigeon migration + env-var deploy + iOS bundle + Keychain credential store |
| vellum | 2-4 | 3-6 | NSPasteboard + NSAttributedString + cgo round-trip |
| claudia | 1-2 | 2-3 | Go probe API |
| other | 2-4 | 3-6 | Various |

Context-switching tax (15+ domain switches): +18-30 person-days

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **120-190 person-days (5-8 months)** |
| Specialist team (traditional) | **100-160 person-days (4-6 person-months)** |
| Actual human effort this week | **~20-32 hours (~3-4 person-days)** |
| **Multiplier vs. generalist** | **~30-50x** |
| **Multiplier vs. specialist team** | **~25-40x** |

The multiplier is highest on the **HMS oracle bootstrap** (a Delphi DFM parser + Apple Vision OCR + Windows SendInput + SQL Server lifecycle + Network Extension diagnosis is conventionally a 3-4 week specialist effort across at least three different specialists, and it landed end-to-end with a passing 1,335-test corpus inside a single week), on the **mnemo Windows release storm** (eleven minor releases including a per-user MSI, ARM64 cross-compile via llvm-mingw, mTLS federation, and four new MCP tools — months of work compressed into days), and on **sawmill's equivalence + auto-fix pillars** (transitive closure with conflict-suppression and the cycle-aware convergence loop are both algorithmically novel pieces that conventionally need a senior systems engineer in residence). The multiplier is lowest on the ccache wire-up tail-end and the Play Console rollout chores (mechanical once direction is set). The human contribution concentrates on **architectural diagnosis** (the three pymssql / SSH-tunnel / sqlcmd pivots in HMS oracle were narrowed by understanding what the Network Extension was actually filtering), **scope decisions** (set_aside vs delete, per-user Windows Service vs HKLM, onedir vs onefile, structured payload vs prose), and **decomposition** (sawmill's pillar T1 into four sub-targets, spyder's KeepAwake → pmd3 cutover sequence).

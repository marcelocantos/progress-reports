# Weekly Progress Report — 2026-03-30…04-05

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Vendor omitted this week: **+56,300/−330** (marcelocantos/sqldeep +33,732, squz/ge +19,459, marcelocantos/sqlpipe +3,108). Excl-vendor landed lines: **+1,049,946/−521,207** (net **+528,739**).

## Executive Summary

A 7-day sprint across **15 repositories** spanning a Rust-to-Go rewrite of a semantic code transformation MCP server with open-sourcing and 11 frontier milestones, a WebTransport relay's session protocol redesigned around generated hierarchical state machines with TLA+ verification, XML/HTML literal syntax added to a C++ SQL transpiler across 8 releases, continued PlantUML SVG parity work in a Rust port, a new TUI git file history browser, a C++ game engine's scene-protocol-to-H.264 pivot, and a CSP library reaching v0.8.0 with file I/O and example applications. **sawmill** was rewritten from Rust to Go with a daemon architecture, open-sourced, and pushed through 11 frontier milestones from Phase 2 to Frontier K — the single largest effort this week. **pigeon** (renamed from tern) gained a unified session protocol with generated state machines in Go/Swift/Kotlin/TypeScript and TLA+ formal verification, plus path-switching with chaos tests. **sqldeep** went from v0.9.0 to v0.18.0, adding XML/HTML literal syntax, JSONML output, JSX rendering, boolean semantics, and an interactive CLI shell.

**432 commits** | **~+1.05M added / ~−521k removed** (excl. vendor) | **~90-150 person-days traditional equivalent** | **~25-45x multiplier**

### Major Achievements & Innovations

- **Sawmill: complete Rust-to-Go rewrite with daemon architecture** — rewrote the entire semantic code transformation MCP server from Rust to Go in a single week, achieving all 7 sub-targets of T11. Go rewrite includes a persistent daemon with Homebrew services integration, binary hash validation handshake, file watcher with fsnotify, embedded QuickJS for codegen programs, and E2E tests for the full daemon-to-MCP-to-disk pipeline. Open-sourced with LICENSE, README, agents-guide, STABILITY.md, CI, release workflows, and 11 frontier milestones (Phases 2-6, Frontiers A-E, K) achieved
- **Unified session protocol with generated state machines** in pigeon: designed a complete session protocol (pairing + transport) in a single YAML spec, with code generators producing typed state machines in Go, Swift, Kotlin, and TypeScript. The Go generator produces `session_gen.go` with typed structs and state transitions. State machines now mediate all `Conn` I/O — no raw protocol handling in application code. TLA+ generator rewritten from PlusCal to pure TLA+ with channel elimination (121 states, <1 second verification)
- **XML/HTML literal syntax for SQL** in sqldeep: added embedded XML/HTML literals that transpile to SQLite function calls, enabling `SELECT <div class={cls}>{content}</div>` syntax in SQL. BLOB protocol for type-safe XML transport, JSONML output for structured XML processing, `jsx()` and `jsonml()` output modes, boolean attribute semantics, self-closing element preservation, multi-line dedentation, and an interactive CLI shell. 8 releases (v0.9.0 through v0.18.0) in one week
- **Path-switching protocol with TLA+ verification and chaos testing** in pigeon: continuous transport adaptation via a path router that switches between relay, LAN, and future transport paths. TLA+ specification with per-actor resource lifecycle invariants passes all model checking. 10 deterministic path-switching tests, multi-pair and live chaos tests, exponential backoff for LAN re-establishment
- **nostalgia: new TUI git file history browser** — detail in [private week 2026-04-05](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-05.md)
- **CSP library v0.6.0–v0.8.0**: opaque `fd_t` type for platform-portable file descriptors, ergonomic I/O wrappers (`read`, `write`, `read_all`), file I/O primitives (`open`, `close`), three example applications (pipeline, chat server, file copier), direct-pointer transfer optimisation (attempted then reverted for safety), Windows build fixes, and TSan fibre suppression
- **build123d migration** in threedee: ported 12 3D-printable designs from [OpenSCAD](https://openscad.org/) to [build123d](https://build123d.readthedocs.io/) with [py_gearworks](https://github.com/meadiode/py_gearworks) for proper involute bevel gears

### Tough Challenges Overcome

- **TLA+ PlusCal-to-pure-TLA+ rewrite** (pigeon): the PlusCal-generated TLA+ for the session protocol was too verbose and slow to model-check. Rewrote the TLA+ generator to emit pure TLA+ with constant promotion (lift invariant values out of the state space), phase-scoped transitions (only enable actions relevant to the current phase), and channel elimination — reducing the state space from intractable to 121 states verifiable in under 1 second
- **Direct-pointer transfer unsafe for stored chan_ops** (csp): an optimisation to eliminate the staging buffer for move-writes by transferring data directly through channel pointers was implemented and released in v0.8.0, then reverted when it proved unsafe for stored `chan_ops` — the pointer could be invalidated between the write and the read when channel operations are stored for later selection
- **State machine mediating all Conn I/O** (pigeon): retrofitting generated state machines to mediate all connection I/O required restructuring the `Conn` type so that every protocol message flows through the state machine's transition logic. The `executor.go` (891 new lines) implements the runtime that drives state machines, handles timeouts, and coordinates concurrent actors
- **Shell.c vendoring for interactive CLI** (sqldeep): integrating an interactive CLI shell into a single-file C++ transpiler required vendoring the [shell.c](https://github.com/nicowilliams/shell.c) library (33K lines), wiring it into the build system, and adding `--help-agent` support for AI coding agents
- **Sawmill daemon binary hash handshake** (sawmill): ensuring the stdio MCP proxy connects to a daemon built from the same binary required a binary hash validation in the daemon handshake. If the hashes mismatch, the proxy auto-restarts the daemon — preventing subtle bugs from version skew between the CLI tool and its background daemon
- **LAN upgrade race condition** (pigeon): the automatic LAN upgrade had a race where encrypt and write were not atomic under the write mutex, allowing interleaved writes from relay and LAN paths. Fixed by holding `writeMu` across the full encrypt+write sequence

Contributor: Marcelo Cantos

---

## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — File I/O & Examples (21 commits)

Continued from last week's M:N-only migration, now building the I/O layer and stabilising for release:

- **File I/O and fd_t** (T3.1): introduced opaque `fd_t` type for platform-portable file descriptors, ergonomic wrappers (`csp::read`, `csp::write`, `csp::read_all`), and file I/O primitives (`csp::open`, `csp::close`). Documentation updated with I/O convenience functions
- **Example applications** (T7.3, T7.4, T7.6): three worked examples — a pipeline processor, a chat server, and a file copier — demonstrating real-world CSP patterns. T7 now fully achieved (6/6 sub-targets)
- **v0.6.0 through v0.8.0 released**: v0.6.0 included M:N scheduler, `net::listen` fix, PicoTLS swap; v0.7.0 added fd_t and file I/O; v0.8.0 added examples and attempted direct-pointer transfer (reverted as unsafe for stored chan_ops)
- **Windows and CI**: fixed file I/O test for Windows (`temp_directory_path`), Windows build fix for `win_signal.cc` and `fd_t`, added TSan fibre suppression, fixed UBSan CI failure
- **Targets achieved**: T3.1 (file I/O), T11 (M:N default), T12 (scheduler selection removed), T7 (examples complete). T14 parked

### [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) — Session Protocol & State Machines (68 commits)

Renamed from tern. Major protocol redesign with generated state machines and formal verification:

- **Unified session protocol**: designed a complete session protocol (pairing ceremony + transport session) in a single [YAML specification](https://github.com/marcelocantos/pigeon/blob/master/protocol/session.yaml) with phases, typed variables, struct definitions, adversary guards, and fairness/liveness properties. 784-line unified spec replaces the previous ad-hoc protocol handling
- **State machine code generation** (T18, T19): generators produce typed state machines in Go, Swift, Kotlin, and TypeScript from the YAML spec. Go generator produces `session_gen.go` with typed structs, state transitions, and converters. State machines mediate all `Conn` I/O — application code never touches raw protocol messages. `executor.go` (891 lines) implements the state machine runtime
- **TLA+ generator rewrite**: rewrote from PlusCal to pure TLA+ with constant promotion, phase-scoped transitions, and channel elimination — 121 states verified in <1 second. Added per-actor resource lifecycle invariants, fairness constraints, and leads-to temporal properties
- **Path-switching protocol**: continuous transport adaptation via a path router. YAML-specified protocol with TLA+ verification (all invariants pass). 10 deterministic tests, multi-pair tests, live chaos tests, exponential backoff for LAN re-establishment
- **LAN upgrade** (T5): redesigned as `LANServer` standalone server with automatic detection and upgrade. Fixed encrypt+write atomicity race under `writeMu`. 13 comprehensive LAN upgrade tests
- **Deployment and clients**: Fly.io auto-start via TCP wake trigger (T16), `wakeRelay` transparent in all client libraries, Config struct replacing variadic options, renamed to carrier-pigeon.fly.dev
- **PlantUML diagrams**: phase-aware PlantUML generator, split state machine diagrams into peer and relay views, session protocol design doc with journey appendix
- **v0.9.0 through v0.14.0 released**

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Database API & XML Support (24 commits)

Continued from last week's convergence loop, now adding a unified database API and XML literal support:

- **Unified Database API** (#6): `sqlpipe::Database` wraps SQLite with bundled [sqldeep](https://github.com/marcelocantos/sqldeep) transpilation and [sqlift](https://github.com/marcelocantos/sqldeep) middleware. Applications write enhanced SQL (with deep expressions, XML literals, etc.) and sqlpipe handles transpilation transparently
- **XML literal support** via sqldeep v0.12.0: XML/HTML literals in SQL subscriptions, enabling reactive UI updates from database changes
- **Glob patterns for table ownership** (#5): `own("prefix_*")` syntax for pattern-based table ownership instead of explicit table lists
- **Convergence loop** (continued): edge case tests, E2E test through tern relay, TLA+ model, transport adapter for dual-channel replication
- **API simplification**: removed `Delivery`, `OutMessage`, `PeerOutMessage` — messages are just messages. Rewritten README with [Mermaid](https://mermaid.js.org/) sequence diagrams
- **Vendored sqldeep/sqlift as submodules**, upgraded to sqldeep v0.18.0
- **v0.17.0 through v0.20.0 released**

### [marcelocantos/targets](https://github.com/marcelocantos/targets) — Rework Loops & Verification (6 commits)

Continued from last week's MCP server bootstrap, adding formal target lifecycle features:

- **Verification targets**: new target type with `kind` field and `verifies` edges linking verification targets to work targets
- **Rework loops**: `rework` edges and retry budgets for bounded rework cycles — when verification fails, the target re-enters work with a decremented retry budget
- **Tunnel detection**: identifies work targets that are far from their verification gate, surfacing risky long tunnels
- **Frontier scheduling**: `targets_frontier` tool for topological frontier-based scheduling
- **Ops module**: extracted rework logic with comprehensive tests

---

## Tooling

### [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) — Rust-to-Go Rewrite & Open Source (91 commits)

**The biggest effort of the week.** A semantic code transformation engine that teaches AI coding agents project-specific patterns and conventions, rewritten from Rust to Go with a daemon architecture and open-sourced:

- **Open-sourcing**: added Apache 2.0 LICENSE, README, CLAUDE.md, agents-guide.md (271 lines), STABILITY.md (458 lines cataloguing the public interaction surface), CI and release workflows, `--help-agent` flag. Originally named Canopy, renamed to Sawmill. Comprehensive codebase audit with 242-line report
- **Rust improvements** (pre-rewrite): backup/undo safety for `apply`, convention invariants (Frontier C), teach-by-example with case-aware template extraction (Frontier B), rich `ctx` API with structural navigation and semantic mutations (Frontier A), LSP semantic queries on `ctx` in codegen programs (Frontier E), structural pre-flight checks for dangling references (Frontier D), agent prompt generation (Frontier K). Split `mcp.rs` into submodules. Bug fixes: path manipulation in `undo_from_backups`, convention checking on post-change state, `unsafe` consolidation in `LspProxy`, watcher `eprintln!` interfering with stdio MCP, LSP timeout fix
- **Go rewrite** (T11): ported all packages — adapters, forest, rewrite, transform, index, exemplar, codegen, jsengine, store, model. MCP server package (T11.4), daemon infrastructure with CLI entry point (T11.3), stdio proxy test (T11.5), Homebrew services support (T11.6), rewrite tests and CI (T11.7). File watcher ported with [fsnotify](https://github.com/fsnotify/fsnotify) and debouncing. Agents-guide embedded in binary via `go:embed`
- **Daemon architecture**: `sawmill` (stdio MCP proxy) and `sawmill serve` (persistent daemon). Binary hash validation in handshake — proxy auto-restarts daemon on version mismatch. Auto-start daemon from `serve` command. Working directory passed through handshake; parse is now optional. E2E tests for the full daemon→MCP→disk path
- **Rust codebase removed** after Go rewrite completion. Go release workflow with [goreleaser](https://goreleaser.com/)
- **Zero project footprint**: moved all sawmill state to `~/.sawmill/` — no files left in project directories
- **Research**: paper on intra-language pattern equivalences (T12)
- **Targets achieved**: T1-T11 (all sub-targets), Frontiers A-E and K. **v0.2.0 through v0.6.0 released**

### [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) — XML Literals & Interactive CLI (53 commits)

A C++ SQL transpiler that adds deep expressions to SQLite. Massive feature expansion this week:

- **XML/HTML literal syntax** (#13): embedded XML/HTML in SQL queries — `SELECT <div class={expr}>{content}</div>` transpiles to SQLite function calls. Design paper in `docs/papers/xml-literals.md`. Interactive CLI shell via vendored [shell.c](https://github.com/nicowilliams/shell.c)
- **XML function extraction** (#15): XML SQLite functions extracted into a shared library module (`sqldeep_xml.c`/`sqldeep_xml.h`) for reuse across Go bindings and CLI
- **BLOB protocol** (#16): replaced XML sentinel byte with SQLite BLOB type protocol for type-safe XML transport between functions
- **JSONML output** (#17, v0.12.0): `xml_to_jsonml()` transpiler macro for [JSONML](http://www.jsonml.org/) array output, then consolidated into `jsonml()` function
- **JSX and JSONML modes**: `jsx()` and `jsonml()` output wrappers for XML literals. Integer and float attribute values emitted as raw JSON
- **Boolean semantics**: `true`/`false` auto-wrapped as `json('true')`/`json('false')` in JSON/XML contexts. Boolean attribute semantics per XML literals design
- **Self-closing elements**: preserved distinction between self-closing (`<br/>`) and non-void (`<div></div>`) in output
- **Multi-line dedentation**: XML literals strip common whitespace prefix from multi-line content
- **Qualified bare fields**: `sm.repo` transpiles to `'repo', sm.repo` — implicit column name from qualified reference
- **Pure BLOB protocol** (v0.18.0): eliminated SQLite subtypes entirely, using pure BLOB protocol for all XML transport
- **`--help-agent` flag**: embedded agents-guide for AI coding agents (306-line `.inc` file)
- **v0.9.0 through v0.18.0 released** (10 releases including the patch for v0.14.0)

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — Native Bridge & Transport (14 commits)

Renamed from jevon. Continued WKWebView integration and transport work:

- **WKWebView native bridge**: Swift-side `JevonBridge` for WKWebView↔native communication. Transport abstraction supporting browser and native dual mode. Tern relay transport mode added to JevonBridge
- **Simplified ConnectView**: full-screen QR scanner replacing manual entry
- **Tern upgrade**: bumped from v0.7.0 to v0.11.0 with detailed migration plan for agent handoff
- **Design**: cost management design note, Grok as first-class agent target (T18), updated Grok full-duplex architecture target (T13)
- **Bug fix**: Swift 6 compiler crash in `ServerView`

### [marcelocantos/den](https://github.com/marcelocantos/den) — Source Builds & Bundled Ruby (7 commits)

Continued from last week's C++ rewrite, completing the Homebrew-free source build pipeline:

- **Source builds** (#9): compile packages from source using formula-parsed build commands — parse Homebrew formulae, extract configure/make/install steps, execute in a clean build environment
- **Embedded Ruby** (attempted and dropped): wired an embedded Ruby VM into the source build pipeline (Path A), then dropped in favour of subprocess invocation with a bundled Ruby binary — simpler and more reliable
- **Bundled Ruby** (#10, #11): embed a Ruby binary bundle for formula evaluation without requiring Homebrew's Ruby. Bottle relocation for Homebrew-free operation
- **v0.3.0 released**

### [marcelocantos/threedee](https://github.com/marcelocantos/threedee) — build123d Migration (4 commits)

Migrated 3D-printable designs from [OpenSCAD](https://openscad.org/) to [build123d](https://build123d.readthedocs.io/):

- **Infrastructure**: Python build123d project setup with VS Code OCP integration
- **12 designs ported**: first 3 ports, then remaining 9 in a single commit. [py_gearworks](https://github.com/meadiode/py_gearworks) for proper involute bevel gears in the triton lifter design
- **Live preview**: `ocp-vscode` `show()` calls for real-time 3D preview in VS Code

---

## Game Projects

### [squz/yourworld2](https://github.com/squz/yourworld2) + [ge](https://github.com/squz/yourworld2/ge) (submodule) — H.264 Pivot & Engine Ownership (72 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-05](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-05.md).*
### [squz/nostalgia](https://github.com/squz/nostalgia) — New TUI Git Browser (14 commits, initial)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-05](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-05.md).*
## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 15 (+ ge submodule) |
| Total commits | 432 |
| Total lines added | +1,049,946 |
| Total lines removed | −521,207 |
| Net new lines | +528,739 |
| Net new lines (excl. vendored) | ~+37,000 |
| File changes | 710 |
| New files created | ~180 |
| Languages | C++, C, Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Python, TLA+, YAML, SQL, HTML, PlantUML |
| Contributors | 1 (Marcelo Cantos) |

Note: den's +913K/-493K includes ~900K lines of vendored C++ dependencies. sqldeep's +39K includes ~33K vendored shell.c. sqlpipe's +50K includes vendored sqldeep/sqlift submodules.

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | 91 | 85 | +27,011 | -13,343 | +13,668 |
| [squz/yourworld2](https://github.com/squz/yourworld2) + ge | 72 | 65 | +26,094 | -1,706 | +24,388 |
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | 68 | 171 | +33,408 | -10,664 | +22,744 |
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | 55 | 37 | +16,209 | -5,493 | +10,716 |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | 53 | 24 | +39,155 | -1,373 | +37,782* |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 24 | 77 | +50,032 | -5,377 | +44,655** |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 21 | 127 | +9,992 | -6,499 | +3,493 |
| [squz/nostalgia](https://github.com/squz/nostalgia) | 14 | 8 | +1,715 | -444 | +1,271 |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 14 | 62 | +3,156 | -1,102 | +2,054 |
| [marcelocantos/den](https://github.com/marcelocantos/den) | 7 | 25 | +913,163 | -493,013 | +420,150*** |
| [marcelocantos/targets](https://github.com/marcelocantos/targets) | 6 | 10 | +1,704 | -58 | +1,646 |
| [marcelocantos/threedee](https://github.com/marcelocantos/threedee) | 4 | 16 | +1,173 | -120 | +1,053 |
| [marcelocantos/mpe2pdf](https://github.com/marcelocantos/mpe2pdf) | 1 | 1 | +1 | -0 | +1 |
| [marcelocantos/planker](https://github.com/marcelocantos/planker) | 1 | 1 | +191 | -0 | +191† |
| [marcelocantos/solarmon](https://github.com/marcelocantos/solarmon) | 1 | 1 | +191 | -0 | +191† |

\* sqldeep net includes ~33K vendored shell.c; own code net is ~+4.8K.
\** sqlpipe net includes vendored sqldeep/sqlift submodules; own code net is ~+4K.
\*** den net includes ~900K vendored C++ dependencies; own code net is ~+1K.
† License file additions only.

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/pigeon](https://github.com/marcelocantos/pigeon) | ~152 | Path-switching tests, LAN upgrade tests, chaos tests, executor tests, multi-pair tests |
| [marcelocantos/sawmill](https://github.com/marcelocantos/sawmill) | ~84 | Go rewrite tests, E2E daemon tests, MCP integration tests, stdio proxy test |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | ~49 | XML literal tests, JSONML tests, JSX tests, boolean semantics tests |
| [marcelocantos/rustuml](https://github.com/marcelocantos/rustuml) | ~35 | Oracle extraction tests, golden test improvements |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~26 | Convergence loop edge cases, E2E through tern, database API tests |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~15 | File I/O tests, example applications (which serve as integration tests) |
| [marcelocantos/targets](https://github.com/marcelocantos/targets) | ~8 | Rework loop tests, frontier scheduling tests |
| **Total** | **~369** | |

### Daily Activity

![Daily active repositories](daily-activity-2026-04-05.svg)

---

## Ideas & Innovations

### Unified Protocol-to-State-Machine Pipeline ([pigeon](https://github.com/marcelocantos/pigeon))

Network protocols are notoriously hard to implement correctly across multiple platforms. Pigeon's approach is to **specify the entire protocol in a single YAML file** — phases, transitions, typed variables, struct definitions, adversary guards, fairness properties — and generate typed state machines in Go, Swift, Kotlin, and TypeScript. The same YAML also generates TLA+ specifications for model checking and PlantUML diagrams for documentation. This means protocol changes happen in one place and automatically propagate to all platforms, all formal models, and all documentation. The channel elimination optimisation in the TLA+ generator reduced the state space from intractable to 121 states by replacing explicit message channels with direct variable updates — making model checking fast enough to run in CI.

### XML Literals as First-Class SQL Syntax ([sqldeep](https://github.com/marcelocantos/sqldeep))

SQL has no native syntax for structured document output. sqldeep's XML literal syntax lets you write `SELECT <div class={category}>{name}</div> FROM products` — the transpiler rewrites the XML into SQLite function calls that construct type-safe XML at runtime. The key insight is using **SQLite's BLOB type as the transport protocol** for XML fragments, which avoids the sentinel-byte approach that was fragile and incompatible with string operations. The `jsx()` and `jsonml()` output modes layer on top, letting the same XML literal syntax produce JSON arrays or JSX-compatible structures. Boolean attribute semantics (`checked` vs `checked={false}`) follow HTML conventions automatically.

### Binary Hash Handshake for Daemon Version Safety ([sawmill](https://github.com/marcelocantos/sawmill))

MCP servers that use a daemon architecture face a subtle version-skew problem: the CLI proxy and the background daemon can be different builds. Sawmill solves this with a **binary hash validation in the daemon handshake** — the proxy computes a hash of its own binary and sends it during connection. If the daemon's hash differs, the proxy kills and restarts the daemon. This is invisible to the user and eliminates an entire class of "works on my machine" debugging sessions where the daemon is stale.

### DAG Graph Rendering with Topological Sort ([nostalgia](https://github.com/squz/nostalgia))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-04-05](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-04-05.md).*
### Zero-Project-Footprint MCP Server ([sawmill](https://github.com/marcelocantos/sawmill))

MCP servers that analyse codebases typically store their state alongside the project (in `.sawmill/` or similar directories). This pollutes `.gitignore`, conflicts with other tools, and creates confusion about what's project state vs. tool state. Sawmill moved **all state to `~/.sawmill/`**, keyed by project path — the MCP server leaves zero footprint in the project directory. The daemon architecture makes this practical: the daemon holds the in-memory model, and the persistent state (conventions, patterns, recipes) lives in the user's home directory.

---

## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| sawmill Rust→Go + open source | 20-30 | Full language rewrite preserving semantics across 12 packages; daemon architecture with binary hash handshake; open-source preparation (audit, docs, CI, release); 11 frontier milestones each requiring novel capability |
| pigeon session protocol + state machines | 20-30 | Protocol design across 4 target languages; code generators producing typed state machines; TLA+ model checking with channel elimination optimisation; path-switching with chaos testing; multi-platform client libraries |
| sqldeep XML literals | 15-20 | C transpiler work (single-file architecture constraint); XML grammar integration into SQL parser; BLOB type protocol design; JSONML/JSX output modes; interactive CLI integration; 10 releases with documentation updates |
| yourworld2/ge H.264 pivot | 10-15 | bgfx internals for scene protocol (before pivot); Metal-specific VideoToolbox encode/decode; zero-copy IOSurface paths; engine ownership refactoring across game and engine boundaries |
| rustuml SVG parity | 8-12 | Continued Java AWT font metric extraction; 6 sub-renderer improvements; oracle test framework extensions to new diagram types |
| csp file I/O + examples | 5-8 | Platform-portable fd_t abstraction; Windows build compatibility; example applications exercising real CSP patterns |
| sqlpipe database API + XML | 5-8 | Unified database API wrapping transpiler + middleware; submodule vendoring; glob pattern ownership |
| nostalgia TUI | 4-6 | Bubble Tea TUI with DAG rendering; go-git integration; syntax highlighting with theme detection |
| jevons native bridge | 3-5 | Swift WKWebView bridge; transport abstraction for dual-mode operation |
| targets rework loops | 2-3 | Graph analysis for tunnel detection; bounded rework with retry budgets |
| den source builds | 2-3 | Homebrew formula parsing; embedded vs subprocess Ruby decision |
| threedee build123d | 1-2 | CAD library migration with gear library integration |

### The Diversity Tax

Specialisms exercised this week:

- **Compiler/transpiler engineering** — SQL transpiler with XML grammar integration, BLOB type protocols, JSONML output
- **Protocol design and formal verification** — TLA+ for session protocols, path-switching, channel elimination, pure TLA+ generation
- **Cross-platform code generation** — Go/Swift/Kotlin/TypeScript state machine generators from YAML specs
- **Language porting** — Rust-to-Go rewrite preserving semantics across MCP server, daemon, store, codegen, and JS engine
- **Graphics and video engineering** — bgfx RendererContextI, Metal VideoToolbox, IOSurface zero-copy, H.264 encode/decode
- **Terminal UI** — Bubble Tea TUI with DAG graph rendering, syntax highlighting, terminal background detection
- **Network protocols** — WebTransport path-switching, chaos testing, LAN upgrade with race condition fixes
- **CAD/3D printing** — build123d migration with involute gear generation
- **MCP server architecture** — daemon handshake, binary hash validation, stdio proxy, zero-footprint state management
- **Game engine architecture** — engine ownership patterns, signal handling, platform abstraction

No single developer holds production-level expertise across compiler engineering, formal verification, cross-platform code generation, video encoding, terminal UI, network protocols, and 3D CAD simultaneously.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| sawmill | 4-6 | Go rewrite decision, daemon architecture design, open-source strategy |
| pigeon | 4-6 | Session protocol YAML design, TLA+ spec review, state machine architecture |
| sqldeep | 3-4 | XML literal syntax design, BLOB protocol decision, output mode design |
| yourworld2/ge | 3-4 | T54 abandon decision, H.264 pivot, engine ownership design |
| rustuml | 2-3 | Oracle framework extensions, font metric debugging |
| csp | 2-3 | fd_t design, example application selection |
| nostalgia | 1-2 | TUI concept, DAG rendering approach |
| other | 2-3 | sqlpipe API design, jevons transport, targets rework model |
| **Total** | **~21-31** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | Ramp-up cost |
|---------|------------|-----------------|--------------|
| sawmill | 20-30 | 30-45 | Rust semantics, Go MCP ecosystem, daemon IPC, QuickJS embedding |
| pigeon | 20-30 | 30-45 | TLA+ model checking, code generation, 4 target language idioms, QUIC/WebTransport |
| sqldeep | 15-20 | 20-30 | C transpiler internals, SQLite extension API, XML grammar design |
| yourworld2/ge | 10-15 | 15-25 | bgfx source code, Metal API, VideoToolbox, game engine patterns |
| rustuml | 8-12 | 12-18 | PlantUML internals, Java AWT metrics, SVG spec |
| csp | 5-8 | 8-12 | Platform I/O abstraction, Windows compatibility, CSP theory |
| sqlpipe | 5-8 | 8-12 | SQLite internals, replication protocols, submodule management |
| nostalgia | 4-6 | 6-9 | Bubble Tea framework, go-git API, terminal rendering |
| jevons | 3-5 | 5-8 | WKWebView bridge, transport abstraction |
| other | 5-8 | 8-12 | Target graphs, CAD libraries, Ruby embedding |

Context-switching tax (12 domain switches): +15-25 person-days

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **110-170 person-days (5-7 months)** |
| Specialist team (traditional) | **90-150 person-days (3-5 person-months)** |
| Actual human effort this week | **~21-31 hours (~3-4 person-days)** |
| **Multiplier vs. generalist** | **~30-50x** |
| **Multiplier vs. specialist team** | **~25-45x** |

The multiplier is highest on the sawmill Rust-to-Go rewrite, where the AI ported 12 packages, built a daemon architecture, and achieved 11 frontier milestones in a week — work that would take a solo developer a month or more just for the mechanical porting. The multiplier is also very high on the pigeon protocol work, where generating state machines in 4 languages plus TLA+ from a single YAML spec would normally require separate expertise in each target language. The multiplier is lowest on the nostalgia TUI (straightforward Go development with well-documented libraries) and the threedee migration (mechanical porting between CAD tools). The human contribution concentrated on architectural decisions (daemon design, session protocol YAML schema, XML literal syntax, T54 abandonment) and quality judgement (when to revert the csp direct-pointer optimisation, how to structure the BLOB protocol, which output modes to support).

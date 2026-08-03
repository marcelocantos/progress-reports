# Weekly Progress Report — 2026-02-23…03-01

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Vendor omitted this week: **+295,753/−2,276** (marcelocantos/sqldeep +281,825, marcelocantos/sqlift +10,213, marcelocantos/sqlpipe +3,713). Excl-vendor landed lines: **+78,704/−15,241** (net **+63,463**).

## Executive Summary

A 7-day sprint across **13 repositories** spanning HAMT data structures, C++ concurrency, SQL tooling, AI agent infrastructure, mobile game development, and Go standard library contributions. **csp** completed a full 5-phase Windows port with three distinct reactor backends, TLA+ formal verification, and a subtle ARM64 thread-local corruption fix. **frozen** introduced H128 128-bit content hashing and recursive XOR hashing (h0), delivering 500x speedup on set inequality detection. **sqldeep** was designed from scratch as a SQL transpiler with FK-guided join path algebra, while **sqlift** shipped 6 releases including a full Go port with cross-language hash verification. Two new Claude Code infrastructure tools — **dais** (multi-session orchestrator) and **doit** (three-level capability broker) — were designed and shipped. Commercial project detail: [private week 2026-03-01](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-01.md).

**364 commits** | **~+78,704 / ~−15,241** (excl. vendor) | **~115-190 person-days traditional equivalent** | **~25-50x multiplier**

### Major Achievements & Innovations

- **5-phase Windows port of csp** with three distinct reactor backends: [kqueue](https://man.freebsd.org/cgi/man.cgi?query=kqueue) (macOS), [epoll](https://man7.org/linux/man-pages/man7/epoll.7.html) (Linux), and [Windows thread pool](https://learn.microsoft.com/en-us/windows/win32/procthread/thread-pool-api) (timers via `CreateThreadpoolTimer`, I/O via `WSAEventSelect`), plus console signal handling, `VirtualAlloc` stack pool, and cross-platform CI with sanitiser matrix — making the library truly portable
- **H128 content hash with single-call signature** in frozen: replaced two separate seeded hash calls per element with a single `func(T) H128` returning 128-bit lo/hi halves, enabling O(1) set equality via hash comparison. Combined with recursive XOR hash (h0) for O(1) inequality rejection — **500x speedup** on mismatched 1M-element sets
- **sqldeep SQL transpiler** from scratch to v0.4.0: FROM-first syntax (`FROM ... SELECT {...}`), auto-join via FK relationships (`c->orders`), join path algebra (reverse joins, chains, bridge joins), singular select (`SELECT/1`), FK-guided transpilation with multi-column composite key support — 111 tests
- **doit three-level capability broker**: deterministic L1 rules (<1ms) → learned L2 YAML policies (<10ms) → L3 LLM gatekeeper (~1-5s) with approval tokens and L3→L2 policy migration. Daemon with binary-framed IPC, hash-chained tamper-evident audit log, pipeline engine with Unicode operators — 164 tests
- **stock-car-racing Unity 6 upgrade** — detail in [private week 2026-03-01](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-01.md)
- **sqlift Go port** with cross-language SHA-256 hash verification (byte-identical across C++ and Go), redundant index detection (prefix-duplicate, PK-duplicate), documentation overhaul, and 6 releases (v0.6.0–v0.11.0) — 149 Go tests
- **TLA+ formal verification** for 4 concurrent protocols in csp (scheduler termination, reactor shutdown, main loop exit, timer race) with paired fix+bug specifications — bug variant violates in 7 steps, validating the scheduler exit race fix

### Tough Challenges Overcome

- **ARM64 thread-local corruption across context switches** (csp): the compiler caches the ELF thread pointer register (TPIDR_EL0) in a callee-saved register (e.g. x19) for efficiency; fcontext's context switch saves/restores callee-saved registers, so an imp resuming on a different OS thread used a stale thread pointer, causing TLS access to read another thread's data. Fixed by routing TLS access through cross-TU function calls, forcing the compiler to re-read the thread pointer on every access
- **Scheduler exit TOCTOU race** (csp): `pending_signals` decremented before the woken imp was consumed from the global queue, creating a window where the scheduler could exit while work remained. Formalised in TLA+ and verified — the bug variant violates the safety property in 7 steps. Fixed by adding a `has_global_work_` check so both conditions must hold
- **Cross-language hash equivalence** (sqlift): ensuring SHA-256 serialisation is byte-identical across C++ and Go requires careful field ordering, endianness handling, and string encoding — any deviation causes drift detection false positives across language boundaries
- **FK-guided join path transpilation** (sqldeep): composite multi-column foreign keys require AND-joined conditions in the generated SQL, with correct disambiguation when multiple FK paths exist between the same tables — a combinatorial problem that breaks naively recursive transpilation
- **Unity lifecycle audit across 11 singleton patterns** — detail in [private week 2026-03-01](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-01.md)
---

## Libraries & Infrastructure

### [arr-ai/frozen](https://github.com/arr-ai/frozen) — H128 Content Hash & HAMT Optimisation (36 commits)

Continued from prior weeks' HAMT optimisation campaign with two major hash innovations and a release:

- **H128 128-bit content hash**: New `struct{lo, hi uintptr}` cached in every HAMT node, replacing the two-separate-seeded-call pattern (`func(T, uintptr) uintptr` called twice) with a single `func(T) H128` returning both halves. Eliminates redundant hash computations. `EqArgs.fullHash` flag enables O(1) equality short-circuit for Sets (where hash captures full content). Internalised [arr-ai/hash](https://github.com/arr-ai/hash) into `internal/pkg/hash` with cross-platform [H128-AES](https://en.wikipedia.org/wiki/AES_instruction_set) assembly (amd64, arm64 optimised; software fallback for 386/arm/mips/ppc64/s390x). Geomean −3.3% time
- **Recursive XOR hash (h0)**: Every node caches `h0 = XOR` of all seed-0 element hashes, propagated up through `branch` XOR of children. `Equal()` compares h0 first — mismatch means entire subtrees differ without traversal. **500x speedup** on 1M-element set inequality detection (25 µs → 50 ns). Builder defers h0 computation to a single `computeH0()` bottom-up pass in `Finish()`
- **HAMT internals optimisation**: Batch spine allocations (single slice instead of per-level allocation, −60% GC objects at 1M elements), inlined branch copies, cached typed dispatch functions replacing `sync.Map` lookups per operation (−75% SetBuilder allocations at 1M elements), structural vetting via `frozen_vet` build tag
- **Benchmarking infrastructure**: `BenchmarkSetOps` covering Equal/Intersection/Difference/SubsetOf/Has at 1K/1M sizes with Same/Equal/Half/Disjoint/Near(99%)/Sparse(1%) overlap patterns. `benchstat` historical tracking with baseline captures
- **Release**: v1.9.0 (H128 + h0 + vendored hash + STABILITY.md). Audit report with 34 findings (7 high, 2 medium); lazy package correctness issues logged for remediation

### [arr-ai/arrai](https://github.com/arr-ai/arrai) — Generics Migration & Hot Path Caching (4 commits)

- **Generics migration**: Migrated all frozen types to generics (`Set[T]`, `Map[K,V]`, `Key[T]`) across 43 files. Replaced `anz-bank/pkg/log` with stdlib `log/slog`, replaced `anz-bank/pkg/mod` with custom `gomod.go` helper. Changed `multipleValues` to `Set[Value]` instead of `Set[any]` to prevent panics on uncomparable types. Eliminates external `anz-bank/pkg` dependency entirely
- **Hot path caching**: `GenericTuple.Names()` cached via `sync.Once` (was rebuilding `frozen.Set[string]` on every call despite immutability), `Relation.attrMap` eagerly computed in `newRelation()`. **−99% getBucket overhead**, −62% RelationAttrs, −44% Relation.Enumerate, −9–19% end-to-end GenericSetJoin
- **Frozen upgrade**: Bumped to v1.9.0 (H128 single-call hashing), wbnf to v0.38.0

---

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — Windows Port & Formal Verification (41 commits)

**The biggest effort of the week.** Continued from last week's combinator and topology surgery work with a complete cross-platform port:

- **Windows port (5 phases)**: Phase 1 — CMake build, platform guards (`#ifdef _WIN32`), `VirtualAlloc`/`VirtualFree` stack pool. Phase 2 — `CreateThreadpoolTimer`-based reactor with mutex-serialised cancel-vs-callback race resolution (whoever erases the map entry owns the `PTP_TIMER` handle). Phase 3 — `WSAEventSelect`+`RegisterWaitForSingleObject` socket I/O with death-signal pattern, `socket_t` typedef unifying Windows/Unix, loopback TCP pairs replacing Unix pipes in tests. Phase 4 — GitHub Actions CI (4 job groups: build-test, sanitisers, Windows MSVC, TLA+ model checking). Phase 5 — `csp::win::signal::notify()` console control events via loopback TCP socket-pair trick (mirrors Unix self-pipe pattern). Total: ~1,700 insertions across platform abstractions
- **Linux epoll reactor**: Platform-neutral `fd_event` enum replacing raw kqueue filter constants, full kqueue/epoll/Windows split in `reactor.cc`. Three distinct reactor backends from a single abstraction
- **20 demo programs**: Self-contained examples from ping-pong to dining-philosophers-deadlock-free (64 lines), showcasing csp vs `std::thread`. Standalone `demos/Makefile` building against `dist/`
- **TLA+ formal verification**: 4 fix+bug specification pairs (SchedulerTermination, ReactorShutdown, MainLoopExit, TimerCreateFire) totalling ~1,500 lines. Bug variants violate safety properties, proving the fixes correct
- **Concurrency bug fixes**: Scheduler exit TOCTOU race (pending_signals vs global queue). M:N scheduler premature exit (stale `mn_mode_` across test boundaries causing use-after-free). ARM64 thread-local corruption (`TPIDR_EL0` cached in callee-saved register across fcontext switches). `imp_exit` use-after-free in supervision tests
- **CI diagnostics**: GDB backtrace capture on Linux crashes (with `SIGUSR1` signal filtering), `MALLOC_CHECK_=3` + `MALLOC_PERTURB_=42` for deterministic heap corruption detection
- **API changes**: C++23 → C++20 downgrade (broader toolchain support), `cancel_op` → `done` rename, multi-handle `join` overloads (subsumes waitgroup), `[[nodiscard]]` attributes, spaceship operator, coverage-gap tests across cancel/channel/clock/dynamic/io/mn/tls/part edge cases

---

### [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) — SQL Transpiler from Scratch (33 commits, initial)

A new C++ transpiler that converts ergonomic SQL syntax extensions into standard SQLite [JSON functions](https://www.sqlite.org/json1.html):

- **FROM-first syntax**: `FROM customers c SELECT { "name": c.name, "orders": ... }` and plain `FROM ... SELECT expr` — top-down data flow instead of SQL's inside-out nesting
- **Auto-join via FK relationships**: `c->orders` navigates conventional FK naming (`<table>_id`). Reverse joins (`<-`), chains (`c->orders o->items i`), and bridge joins (`c->custacct<-accounts` for many-to-many). Two-pass lexer pre-scans for alias resolution
- **Singular select**: `SELECT/1` skips `json_group_array()` wrapping and adds `LIMIT 1` for single-row projections
- **FK-guided transpilation**: Explicit `std::vector<ForeignKey>` metadata for non-conventional column names and multi-column composite keys with AND-joined conditions
- **Releases**: v0.1.0 (parser + 5 security fixes), v0.2.0 (auto-join), v0.3.0 (join path algebra, GitHub Actions CI), v0.4.0 (singular select, FK-guided joins). 111 tests

---

### [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) — Go Port & Six Releases (38 commits)

Continued from last week's initial C++ release with a major expansion:

- **Go port** (v0.8.0): Full reimplementation in Go (`go/sqlift` package) with 127 tests. Cross-language SHA-256 hash verification ensures C++ and Go produce byte-identical fingerprints for drift detection interoperability
- **Redundant index detection** (v0.10.0): `DetectRedundantIndexes()` identifies prefix-duplicate, PK-duplicate, and exact-duplicate indices. Integrated into `Diff()` output with `WarningType`/`Warning` structs
- **Named constraints** (v0.7.0): Constraint name preservation through migration, version counter via `migration_version()` function
- **Documentation overhaul** (v0.9.0): Getting-started tutorial, Go API reference, guide rewrite with C++/Go example parity
- **Audit findings resolved**: FK enforcement restoration on `apply()` failure (PRAGMA is connection-level, not transactional), string-literal-aware parser (prevents CHECK constraint mis-parsing), `GeneratedType` enum validation
- **Example coverage** (v0.11.0): 9 Go `Example*` test functions covering full API. Releases: v0.6.0–v0.11.0 (6 releases in 7 days). 149 Go tests, 122 C++ tests

---

### [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) — Compression, Subscriptions & Reconnection (14 commits)

Continued from last week's initial release:

- **LZ4 changeset compression** (v0.6.0): Transparent compression with uncompressed fallback, per-message compressed/uncompressed marking
- **Query subscriptions** (v0.3.0): Register SQL queries on replica; uses SQLite's [authoriser API](https://www.sqlite.org/c3ref/set_authorizer.html) to discover table dependencies automatically. Subscribers notified only when results actually change
- **Schema migration hooks** (v0.5.0): `on_schema_mismatch` callback for automatic migration on divergence. Batched `handle_messages()` defers subscription re-evaluation until all messages applied. Message size limits (`kMaxMessageSize` 64 MB)
- **Reconnection support** (v0.6.0): `reset()` returns to Init state preserving subscriptions (Replica) or table ownership (Peer). Schema mismatch callback redesign with unified signature
- **Releases**: v0.1.0–v0.6.0 (6 releases). 74 test cases including fuzz/stress tests

---

## Tooling

### [marcelocantos/dais](https://github.com/marcelocantos/dais) — Multi-Session Claude Code Orchestrator (12 commits, initial)

A new Go tool for coordinating multiple concurrent [Claude Code](https://claude.ai/code) sessions:

- **Shepherd pattern**: Users talk to a single "shepherd" Claude Code session that intelligently delegates to worker sessions. The shepherd understands the full project context and decides whether to respond directly or spin up a specialised worker
- **Real-time broadcast**: Multiple TUI clients observe the same shepherd session via WebSocket. User messages and worker completions broadcast to all connected clients
- **SQLite persistence**: Transcript, worker session metadata (id, name, workdir, model, last_result), and key-value store for `--resume` continuity across daemon restarts. Raw NDJSON logging for audit
- **[Bubbletea](https://github.com/charmbracelet/bubbletea) TUI**: [Glamour](https://github.com/charmbracelet/glamour) markdown rendering, auto-reconnect with exponential backoff, command history (Ctrl+P/N), scroll-aware auto-scroll, status badges (Thinking/Disconnected/unread count), token usage tracking
- **Release**: v0.1.0 with `--version`, `--help-agent`, STABILITY.md, agents-guide.md, CI (darwin-arm64, linux-amd64, linux-arm64)

---

### [marcelocantos/doit](https://github.com/marcelocantos/doit) — Three-Level Capability Broker (21 commits, initial)

A new Go command gatekeeper that sits between Claude Code and the shell — Claude Code gets `Bash(doit:*)` permission, and doit decides what can run:

- **Level 1 — Deterministic fast-path** (<1ms): Fixed safety rules evaluated against command AST. Hardcoded blocks (`rm -rf /`), config-bypassable rules (`git push --force`), `--retry` override for L1 config rules
- **Level 2 — Learned policy engine** (<10ms): Human-curated YAML store with per-segment matching, first-match-wins evaluation, pipeline compositionality (any-deny → deny, all-allow → allow, mixed → escalate), spaced-repetition scheduling for entry review
- **Level 3 — LLM gatekeeper** (~1-5s): Invokes `claude -p` subprocess with command, justification, safety argument, and audit context. Issues time-limited single-use approval tokens for uncertain cases. **L3→L2 policy migration**: analyses audit patterns, generates L2 candidates, CLI `doit --policy {promote,list,approve,reject}`
- **Daemon + IPC**: Persistent daemon on Unix socket with binary-framed multiplexed I/O (5-byte header: tag + length), auto-spawn on first invocation, configurable idle timeout
- **Pipeline engine**: Unicode operators (`¦` pipe, `›`/`‹` redirects, `＆＆`/`‖`/`；` compound), two-level parser, per-segment policy evaluation
- **Audit**: Hash-chained append-only log with tamper detection, structured entries with command/exit-code/policy-level/result/rule-ID
- **Testing**: 164 test assertions across 18 test files covering all three policy levels, daemon lifecycle, IPC protocol, LLM client, audit queries, and pipeline parsing

---

### [marcelocantos/mk](https://github.com/marcelocantos/mk) — Inline Comments & Stability Tracking (4 commits)

- **Inline comment stripping**: Strip `# comment` from variable assignments and rule definitions while preserving `#` in recipe lines (where it may be meaningful in scripts)
- **Test expansion**: Tests for sibling cross-module references, nested includes, and nested pattern discovery
- **Stability tracking**: STABILITY.md cataloguing CLI flags, mkfile syntax, standard library, build state format, and Go API with Stable/Needs-review/Fluid ratings. Audit log with v0.8.0 entry

---

## Game Projects

### [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) — Unity 6 Upgrade & Null-Ref Audit (69 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-03-01](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-01.md).*
### [minicadesmobile/kart-stars](https://github.com/minicadesmobile/kart-stars) — Code Quality Audit (9 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-03-01](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-03-01.md).*
## Go Standard Library

### [golang/go](https://github.com/golang/go) — Decimal128 ABI & DWARF Support (2 commits)

Contributing to Go's native [IEEE 754 decimal floating-point](https://en.wikipedia.org/wiki/IEEE_754#Decimal) support:

- **ABI decomposition fix**: `decimal128` (16-byte type) decomposed into two `uint64` halves (lo, hi) for register passing, mirroring `complex128`'s pattern. Enables `reflect.Value.Call` to correctly handle decimal function arguments and return values
- **DWARF `DecimalFloatType`**: Added to `debug/dwarf` for encoding `0x0F` (`DW_ATE_decimal_float`), allowing debuggers to display decimal values. API entries moved from `api/next/` to `api/go1.26.txt`. BID128 exponent formatting fixed for 4-digit exponents (up to ~6176)

### [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) — Status Updates (3 commits)

- Updated status reflecting ABI, DWARF, and BID128 exponent fixes. Math decimal tests now blocking in CI (Linux bootstrap bug resolved). Statistics updated: 129 files, 18+ packages, 3,500+ test lines

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 23 (13 with substantial development) |
| Total commits | 364 |
| Total lines added | +543,690† |
| Total lines removed | −15,241 |
| Net new lines | +516,935† |
| Net new lines (excl. vendored/generated) | ~+102,000 |
| File changes | 4,361 |
| Languages | C++, Go, C#, TLA+, TypeScript, SQL, Assembly, Shell, YAML |

*†sqldeep vendors sqlite3.c (~250k lines). stock-car-racing includes Unity package upgrades and generated meta files (~100k). arrai includes go.sum/npm dependency management (~17k). hms is scaffolded Next.js (~20k).*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [minicadesmobile/stock-car-racing](https://github.com/minicadesmobile/stock-car-racing) | 69 | 1,778 | +118,130 | -4,966 | +113,164* |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 41 | 319 | +13,958 | -3,278 | +10,680 |
| [marcelocantos/skills](https://github.com/marcelocantos/skills) | 41 | 96 | +2,332 | -266 | +2,066† |
| [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) | 38 | 189 | +22,648 | -3,096 | +19,552 |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | 36 | 257 | +22,739 | -2,759 | +19,980 |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | 33 | 109 | +286,945 | -435 | +286,510* |
| [marcelocantos/doit](https://github.com/marcelocantos/doit) | 21 | 224 | +16,564 | -439 | +16,125 |
| [squz/yourworld2](https://github.com/squz/yourworld2) | 15 | 20 | +405 | -16 | +389‡ |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | 14 | 63 | +6,220 | -153 | +6,067 |
| [marcelocantos/progress-reports](https://github.com/marcelocantos/progress-reports) | 12 | 19 | +72 | -55 | +17† |
| [marcelocantos/dais](https://github.com/marcelocantos/dais) | 12 | 88 | +7,675 | -936 | +6,739 |
| [minicadesmobile/kart-stars](https://github.com/minicadesmobile/kart-stars) | 9 | 1,019 | +5,729 | -2,195 | +3,534 |
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | 4 | 57 | +19,032 | -7,869 | +11,163* |
| [marcelocantos/mk](https://github.com/marcelocantos/mk) | 4 | 5 | +446 | -1 | +445 |
| [squz/esfera2](https://github.com/squz/esfera2) | 3 | 3 | +73 | -2 | +71‡ |
| [marcelocantos/go-decimal-proposal](https://github.com/marcelocantos/go-decimal-proposal) | 3 | 5 | +51 | -57 | -6 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 2 | 11 | +238 | -159 | +79‡ |
| [golang/go](https://github.com/golang/go) | 2 | 8 | +162 | -73 | +89 |
| [Health-Management-Systems/hms](https://github.com/Health-Management-Systems/hms) | 1 | 87 | +20,025 | 0 | +20,025* |
| [marcelocantos/gg](https://github.com/marcelocantos/gg) | 1 | 1 | +29 | 0 | +29§ |
| [squz/bricabrac](https://github.com/squz/bricabrac) | 1 | 1 | +59 | 0 | +59§ |
| [squz/multimaze](https://github.com/squz/multimaze) | 1 | 1 | +54 | 0 | +54§ |
| [squz/yourworld](https://github.com/squz/yourworld) | 1 | 1 | +104 | 0 | +104§ |

*\*Includes vendored dependencies or generated content.*
*†Automated skill syncs / meta.*
*‡ge submodule updates + minor infrastructure.*
*§Audit log reconstruction only.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/sqlift](https://github.com/marcelocantos/sqlift) | ~188 | 149 Go tests (full port), 39 new C++ tests, cross-language hash verification |
| [marcelocantos/doit](https://github.com/marcelocantos/doit) | ~164 | All 3 policy levels, daemon/IPC, audit, pipeline (all new) |
| [marcelocantos/sqldeep](https://github.com/marcelocantos/sqldeep) | ~111 | Parser, transpiler, SQLite integration (all new) |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | ~30 | Coverage-gap tests, Windows signal, coin flip, 20 demos |
| [marcelocantos/dais](https://github.com/marcelocantos/dais) | ~18 | Session lifecycle, multi-client broadcast, persistence |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | ~15 | h0/H128 benchmarks, structural vetting, Near/Sparse patterns |
| [marcelocantos/sqlpipe](https://github.com/marcelocantos/sqlpipe) | ~14 | Compression, subscriptions, schema hooks, reconnection |
| [marcelocantos/mk](https://github.com/marcelocantos/mk) | ~4 | Cross-refs, nested includes, inline comments |
| **Total** | **~544** | |

---

### Daily Activity

![Daily active repositories](daily-activity-2026-03-01.svg)

## Ideas & Innovations

### Two-Level Hash Architecture for O(1) Set Operations ([frozen](https://github.com/arr-ai/frozen))

Persistent data structures traditionally require O(n) or O(n log n) comparisons for equality. frozen introduces a **two-level hash architecture** where every HAMT node caches both a recursive XOR hash (h0) and a full 128-bit content hash (H128). h0 provides O(1) inequality rejection — if the root h0 values differ, the sets are different, full stop (no traversal). When h0 matches, H128 provides O(1) equality confirmation for Sets (where the hash captures full content). The combination covers both the common case (different sets, rejected instantly) and the happy path (identical sets, confirmed instantly), leaving element-by-element comparison only for the rare case of hash collisions.

### Three-Level Policy Escalation for Agentic Safety ([doit](https://github.com/marcelocantos/doit))

AI agents executing shell commands face a tension between safety and throughput — per-command approval is safe but slow, blanket permission is fast but dangerous. doit resolves this with **three-level policy escalation**: L1 deterministic rules (<1ms) handle known-safe and known-dangerous commands instantly, L2 learned policies (<10ms) handle patterns that have been seen and approved before, and L3 LLM reasoning (~1-5s) handles novel cases with the ability to issue approval tokens for human review. The key insight is **L3→L2 migration**: as the LLM makes consistent decisions on similar commands, those patterns automatically promote to L2, reducing LLM invocations over time. The system learns from its own gatekeeper decisions.

### FK-Guided Join Path Algebra ([sqldeep](https://github.com/marcelocantos/sqldeep))

SQL's explicit JOIN syntax forces developers to write structural boilerplate that the database schema already knows. sqldeep introduces **join path algebra** where `c->orders` means "follow the FK from customers to orders" and `c->custacct<-accounts` navigates a many-to-many junction table. The transpiler resolves paths using either convention-based FK naming (`<table>_id`) or explicit metadata (supporting multi-column composite keys). This transforms nested JSON construction from verbose `json_group_array(json_object(...))` calls with manual JOINs into a declarative `FROM ... SELECT {...}` syntax that reads like the output structure.

### Shepherd Pattern for Multi-Session Orchestration ([dais](https://github.com/marcelocantos/dais))

Managing multiple concurrent AI coding sessions creates cognitive overhead — switching between terminals, tracking which session has which task, duplicating context. dais introduces **a "shepherd" LLM that acts as a conversational coordinator**, intelligently deciding whether to answer directly or delegate to a specialised worker session. Multiple human clients can observe the same shepherd via WebSocket broadcast, and SQLite persistence enables `--resume` continuity across daemon restarts. The architecture turns a collection of independent Claude Code sessions into a managed multi-agent system.

### Cross-Language Hash Verification ([sqlift](https://github.com/marcelocantos/sqlift))

Schema migration tools often detect drift by comparing fingerprints. When the same tool exists in two languages (C++ and Go), **hash divergence between implementations causes false-positive drift alerts**. sqlift's Go port includes dedicated cross-language hash tests that verify SHA-256 outputs are byte-identical for the same schema inputs, ensuring a Go application can reliably detect drift introduced by a C++ application (or vice versa). This required careful attention to field ordering, string encoding, and numeric serialisation across language boundaries.

### TLA+ Fix-Bug Specification Pairs ([csp](https://github.com/marcelocantos/csp))

Formal verification typically proves that a protocol is correct. csp takes this further by maintaining **paired specifications for each verified protocol** — a "fix" spec that passes TLC model checking and a "bug" spec that reproduces the exact race condition. The bug spec for the scheduler termination race violates the safety property in exactly 7 steps, demonstrating the precise interleaving that causes the TOCTOU window. This pairing serves as regression-proof documentation: if someone later removes the fix, the bug spec shows exactly what breaks and how.

---

## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **csp** | 25-40 | 5-phase Windows port requires deep knowledge of 3 OS-specific async I/O APIs (kqueue, epoll, Windows thread pool). ARM64 TLS corruption is an ABI-level bug requiring understanding of calling conventions and fcontext assembly. TLA+ specifications require formal methods expertise. |
| **frozen** | 15-25 | HAMT internals optimisation requires persistent data structure expertise. H128 with cross-platform assembly (6 architecture targets) requires ABI knowledge per platform. Benchmark infrastructure with statistical analysis. |
| **sqldeep** | 15-25 | Novel SQL syntax design, recursive-descent parser with two-pass alias resolution, FK join path algebra with combinatorial disambiguation, transpilation to SQLite JSON functions. |
| **doit** | 15-25 | Three-level policy engine with different latency budgets, daemon with binary IPC protocol, pipeline parser with Unicode operators, hash-chained audit log, LLM subprocess integration with approval tokens. |
| **sqlift** | 12-20 | Full language port (C++ → Go) with byte-identical hash verification, redundant index detection algorithms, documentation overhaul, 6 releases with CI. |
| **stock-car-racing** | 10-15 | Unity 6 engine upgrade across 1,778 files, auditing 11 singleton patterns for lifecycle correctness, thread-safety fixes for ad/Firebase callbacks, real-world-time auto-repair feature, Android 16KB alignment. |
| **dais** | 8-12 | Multi-session WebSocket architecture, SQLite persistence layer, Bubbletea TUI with markdown rendering, daemon lifecycle with --resume, release pipeline. |
| **sqlpipe** | 5-8 | LZ4 compression integration, query subscription dependency discovery via SQLite authoriser, schema migration hooks, reconnection state machine. |
| **kart-stars** | 3-5 | 92-finding code quality audit across Unity codebase, thread-safety analysis, singleton lifecycle fixes. |
| **arrai** | 3-5 | Generics migration across 43 files with type safety analysis, hot path profiling and caching. |
| **golang/go** | 3-5 | ABI decomposition for 16-byte types in Go compiler internals, DWARF encoding support, BID128 edge cases. |
| **mk** | 1-2 | Inline comment parsing, stability documentation. |
| **go-decimal-proposal** | 0.5-1 | Status documentation updates. |

### The Diversity Tax

Specialisms exercised this week:

- Persistent data structure optimisation (Go, HAMT, hash algorithms)
- C++ M:N scheduler and cooperative concurrency (kqueue, epoll, Windows thread pool, fcontext assembly)
- TLA+ formal methods and model checking
- ARM64 ABI and calling convention analysis
- SQL syntax design and recursive-descent parsing
- SQLite session extension, replication protocols, and migration algorithms
- Go compiler internals and DWARF debug format
- [BID encoding](https://en.wikipedia.org/wiki/Binary_integer_decimal) for IEEE 754 decimal floating-point
- Unity engine lifecycle management and C# singleton patterns
- Mobile platform engineering (Android 16KB alignment, ad SDK integration)
- AI agent infrastructure (LLM subprocess orchestration, policy engines)
- Cross-platform CI/CD (GitHub Actions, sanitisers, Windows MSVC)
- [Bubbletea](https://github.com/charmbracelet/bubbletea)/[Glamour](https://github.com/charmbracelet/glamour) TUI development
- Technical writing (stability catalogues, agent guides, design documents)

No single engineer holds expertise in HAMT data structures, ARM64 ABI, TLA+ formal verification, SQL parser construction, Unity lifecycle management, LLM orchestration, and Go compiler internals simultaneously.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **csp** (41 commits) | 5-10 | Architecture decisions (Windows reactor design, C++20 downgrade trade-off), reviewing TLA+ specs, debugging ARM64 TLS crash on CI |
| **frozen** (36 commits) | 3-5 | H128 API design decisions, reviewing benchmark results, approving hash package internalisation |
| **sqldeep** (33 commits) | 3-5 | SQL syntax design (FROM-first, join path algebra, SELECT/1), testing against real schemas |
| **doit** (21 commits) | 3-5 | Three-level policy architecture decisions, reviewing approval token flow, testing daemon lifecycle |
| **sqlift** (38 commits) | 2-4 | Reviewing Go port API, validating cross-language hash equivalence, approving releases |
| **stock-car-racing** (69 commits) | 3-5 | Play-testing auto-repair, reviewing null-ref audit priorities, ad SDK configuration |
| **dais** (12 commits) | 2-3 | Shepherd pattern architecture, testing multi-client UX |
| **Other** | 3-5 | kart-stars code quality review, sqlpipe API decisions, arrai generics migration, Go decimal status |
| **Total** | **~24-42 hours** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | Ramp-up cost |
|---------|------------|-----------------|--------------|
| csp | 25-40 | 40-60 | +10 (Windows APIs, ARM64 ABI, TLA+) |
| frozen | 15-25 | 25-40 | +8 (HAMT theory, hardware-specific hashing) |
| sqldeep | 15-25 | 20-35 | +5 (SQLite JSON functions, parser construction) |
| doit | 15-25 | 20-35 | +5 (LLM integration, daemon IPC) |
| sqlift | 12-20 | 18-30 | +4 (schema migration algorithms) |
| stock-car-racing | 10-15 | 15-25 | +5 (Unity lifecycle, ad SDKs, Android) |
| dais | 8-12 | 12-18 | +3 (WebSocket, Bubbletea TUI) |
| sqlpipe | 5-8 | 8-12 | +3 (SQLite sessions, LZ4) |
| Other | 7-13 | 12-20 | +5 |
| **Subtotal** | **112-183** | **170-275** | **+48** |
| Context-switching tax (30%) | | +51-83 | |
| **Total** | | **221-358** | |

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~115-190 person-days (6-10 months)** |
| Specialist team (traditional) | **~70-120 person-days (3-6 person-months)** |
| Actual human effort this week | **~24-42 hours (~3-5 person-days)** |
| **Multiplier vs. generalist** | **~25-50x** |
| **Multiplier vs. specialist team** | **~15-35x** |

The multiplier is highest for csp's Windows port, where navigating three platform-specific async I/O APIs, ARM64 ABI quirks, and TLA+ formal verification would require a rare combination of systems programming and formal methods expertise. It's lowest for the mobile game work, where Unity's visual, interactive nature means more human time spent play-testing and reviewing aesthetic decisions. The human contribution concentrated on architectural taste (doit's three-level policy design, sqldeep's syntax choices, dais's shepherd pattern) and correctness judgement (reviewing TLA+ specs, validating cross-language hash equivalence, auditing singleton lifecycle priorities).

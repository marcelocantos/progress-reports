# Weekly Progress Report — 2026-02-09…15

> **Series restamp (2026-07-25):** Headline line stats now exclude `**/vendor/**` and `**/node_modules/**` (same rule as `gather.sh`). Figures below use remeasured excl-vendor totals from current default-branch history. Commits and effort estimates are unchanged. Vendor omitted this week: **+266,135/−10** (squz/ge +266,135). Excl-vendor landed lines: **+49,689/−14,089** (net **+35,600**).

## Executive Summary

A remarkably broad week across **10 repositories** spanning game development, library engineering, tooling, and strategic planning. The headlines: the **csp** library was born — extracted from bricabrac and rapidly expanded with timer primitives, M:N threading, sanitizer support, and microbenchmarking (24 commits). **gg** received a comprehensive CLI overhaul in Rust (17 commits). Three research/strategic documents landed across **arrai**, **wbnf**, and **hash**. Commercial project detail: [private week 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md).

**129 commits** | **~+49,689 / ~−14,089** (excl. vendor) | **~120-220 person-days traditional equivalent** | **~30-90x multiplier**

### Major Achievements & Innovations

- **Built multimaze2 from scratch** — detail in [private week 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md)
- **Extracted and expanded the csp library** — from bricabrac extraction to standalone C++ microthreading platform with timer channels, M:N scheduling with work stealing, sanitizer support with fiber annotations, [nanobench](https://nanobench.ankerl.com/) microbenchmarking, and RingBuffer rewrite fixing memory leaks and UB
- **Eliminated shell injection by construction** in gg via a key=value protocol: the Rust binary never emits executable shell code; all interpolation happens in the shell function with proper quoting
- **Live-tunable physics** — detail in [private week 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md)
- **Carousel country selector**: Horizontally scrollable strip at screen bottom showing unplaced countries with physics-based scrolling ported from original GameState.mm — snap-to-grid, velocity accumulation with 5/6 boost decay, sub-stepped symplectic Euler integration (10 iterations/frame). 584-line Carousel.cpp with pImpl pattern
- **Proposed dissolving "hard" parsing problems** in wbnf: C typedef ambiguity and C++ template brackets recast as semantic analysis problems, not parsing problems

### Tough Challenges Overcome

- **Custom rigid-body physics from scratch then replacement** — detail in [private week 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md)
- **M:N scheduler design** (csp): building a work-stealing scheduler across OS threads with correct suspension semantics required careful reasoning about TOCTOU races between channel registration and context switching
- **Boost.Context migration** — detail in [private week 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md)
- **Box2D v3 collision geometry alignment** — detail in [private week 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md)
- **Porting carousel physics from Obj-C** — detail in [private week 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md)
---

## Game Projects

### [squz/multimaze2](https://github.com/squz/multimaze2) — From Scratch to Box2D (20 commits, 2 people, initial)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md).*
### [squz/yourworld2](https://github.com/squz/yourworld2) — Carousel, Placement & Audio (59 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md).*
## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — New CSP Library (24 commits, initial)
**Brand new library.** A C++ microthreading library extracted from [squz/bricabrac](https://github.com/squz/bricabrac) and rapidly expanded:
- **Initial extraction**: Cooperative microthreads with [Boost.Context](https://www.boost.org/doc/libs/release/libs/context/), typed synchronous channels, `alt`/`prialt` multiplexing (like Go's `select`). Rich stream combinators: `buffer`, `map`, `where`, `tee`, `fanout`, `chain`, `quantize`, `latch`, `killswitch`, `rpc`. Namespace renamed from `brac` to `csp`, headers restructured to `include/csp/`. 88 tests passing, standalone Makefile with Clang C++17
- **Timer primitives**: `sleep`, `after`, `tick` implemented as channels — timers compose naturally with `alt` for timeouts and periodic processing
- **M:N threading**: [GMP model](https://en.wikipedia.org/wiki/Green_thread) scheduler for multi-core scheduling with work stealing across OS threads via `init_runtime(n)`
- **RingBuffer rewrite**: Fixed memory leak and undefined behaviour, added comprehensive tests
- **Sanitizer support**: Full [ASan](https://clang.llvm.org/docs/AddressSanitizer.html), [UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html), [TSan](https://clang.llvm.org/docs/ThreadSanitizer.html) build targets with Boost.Context fiber annotations for correct stack reporting
- **Microbenchmarking**: [nanobench](https://nanobench.ankerl.com/) infrastructure for channel throughput baselines
- **Channel memory leak fix**: Channels now correctly delete when both endpoints close, tracked via independent endpoint refcounting
- **Build system**: Automatic header dependency tracking in Makefile, optimised `alt()` with random offset instead of shuffle

### [squz/bricabrac](https://github.com/squz/bricabrac) — Thread Module Evolution (3 commits)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md).*
### [anz-bank/decimal](https://github.com/marcelocantos/decimal) — Bug Fix (1 commit)
Fixed `Context.Sub()` silently ignoring the receiver context's rounding mode — it was calling `Decimal.Add` (which hardcodes HalfUp) instead of `ctx.Add`. Important for [IEEE 754-2019](https://en.wikipedia.org/wiki/IEEE_754) compliance.

### [arr-ai/hash](https://github.com/arr-ai/hash) — Benchmarking (2 commits)
- Added CLAUDE.md with project guidance
- **Comprehensive hash function benchmarks**: 21 benchmark cases covering all supported types (int8-64, uint8-64, float32/64, string, byte slices, struct, pointer, slice, map, Hashable interface)

---

## Tooling

### [marcelocantos/gg](https://github.com/marcelocantos/gg) — CLI Overhaul (17 commits, initial)
**Brand new public presence** for the `gg` git shorthand tool (Rust) — comprehensive modernisation and first release:
- **Interactive installer**: Running `gg` with no args now walks through setup (GGROOT, git protocol, directory viewer, aliases), writes config to `~/.zshrc`
- **SSH URLs by default**: Shorthand URLs now default to SSH; `GGHTTP=1` for HTTPS. Smart host directory creation with `git ls-remote` verification
- **Security**: Shell injection fix via `shell::escape()`, replaced `panic!()` with `bail!()`, removed `process::exit(1)` in favour of Result propagation
- **Code quality**: [clap](https://github.com/clap-rs/clap) v3 -> v4 upgrade, clippy fixes, LazyLock regex, key=value protocol replacing shell command output, descriptive CLI args
- **Testing**: 27 integration tests (14 for the installer alone), plus shell integration tests via real zsh + local bare repos
- **CI/CD**: New GitHub Actions CI workflow (clippy + tests + fmt), fixed release workflow for cross-compilation from macos-14 (arm64) since macos-13 runners are gone

---

## Strategic Planning & Documentation

### [arr-ai/arrai](https://github.com/arr-ai/arrai) — State of the Language (1 commit)
Added a 161-line research document analysing arr.ai's current state and future directions:
- Project health: peaked at 182 commits in 2021, effectively dormant since 2024, 146 open issues
- Proposes performance quick wins (object pooling, fast-path function application), medium-term work (bytecode compilation, lazy enumerators), and language evolution (gradual typing, deterministic parallelism)
- Strategic recommendation: position as an embeddable data transformation engine for Go

### [arr-ai/wbnf](https://github.com/arr-ai/wbnf) — Universal Grammar Research (1 commit)
Added a 717-line research paper "Toward a Universal Grammar" exploring wbnf's evolution:
- Proposes regex/grammar unification, integrated tokenization via labeled alternatives, generalised positional constraints (for indentation-sensitive parsing), and algebraic grammar composition
- Argues that "hard" parsing problems (C typedef ambiguity, C++ template brackets) dissolve when grammars describe only surface syntax
- Includes related work survey ([SDF](https://www.syntax-definition.org/), Rascal, PEG/OMeta/Ohm, [LPEG](http://www.inf.puc-rio.br/~roberto/lpeg/)) and implementation roadmap

### [squz/multimaze](https://github.com/squz/multimaze) — Documentation (1 commit)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md).*
## Other Team Work

### [squz/esfera2](https://github.com/squz/esfera2) — Spherical Chess (54 commits, Andrew Cantos)

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md).*
## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 10 |
| Total commits | 129 |
| Total lines added | +49,689 |
| Total lines removed | −14,089 |
| Net new lines | +35,600 |
| File changes | 356 |
| New files created | 136 |
| Languages | C++, Go, Rust, Markdown, WGSL, YAML, Shell, SQL, Python |
| Contributors | 2 (Marcelo Cantos, Andrew Cantos) |

*The csp lines include code extracted from bricabrac, not all written from scratch this week. The bricabrac removal (-5,556 lines) mirrors code now consumed from the csp submodule.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [squz/yourworld2](https://github.com/squz/yourworld2) | 59 | 55 | +2,492 | -1,031 | +1,461 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 24 | 80 | +24,881 | -2,767 | +22,114* |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 19 | 30 | +6,439 | -840 | +5,599 |
| [marcelocantos/gg](https://github.com/marcelocantos/gg) | 17 | 18 | +1,625 | -551 | +1,074 |
| [squz/bricabrac](https://github.com/squz/bricabrac) | 3 | 48 | +783 | -5,906 | -5,123** |
| [arr-ai/hash](https://github.com/arr-ai/hash) | 2 | 2 | +214 | -9 | +205 |
| [arr-ai/wbnf](https://github.com/arr-ai/wbnf) | 1 | 2 | +789 | -0 | +789 |
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | 1 | 2 | +234 | -0 | +234 |
| [anz-bank/decimal](https://github.com/marcelocantos/decimal) | 1 | 1 | +2 | -2 | 0 |
| [squz/multimaze](https://github.com/squz/multimaze) | 1 | 1 | +74 | -0 | +74 |
| [squz/esfera2](https://github.com/squz/esfera2) | 7 | 4 | +48 | -54 | -6*** |

*\*Includes code extracted from bricabrac; not all written from scratch this week.*
*\*\*Thread module replaced by csp submodule dependency.*
*\*\*\*sq submodule pointer updates only.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 88 | Full suite extracted with library, plus timer, scheduler, and RingBuffer tests |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 52 | 310 assertions; physics, levels, rendering |
| [marcelocantos/gg](https://github.com/marcelocantos/gg) | 27 | Rust integration tests + shell tests |
| [squz/bricabrac](https://github.com/squz/bricabrac) | 23 | Channels, alt fairness, volume stress |
| [arr-ai/hash](https://github.com/arr-ai/hash) | 21 | Benchmark suite covering all hashable types |
| **Total** | **211** | |

---

### Daily Activity

![Daily active repositories](daily-activity-2026-02-15.svg)

## Ideas & Innovations

### CSP Microthreading with Action RAII ([csp](https://github.com/marcelocantos/csp))
The csp library implements Go-style channel semantics in C++ with an elegant twist: channel operations return `action` objects whose **destructors invoke `prialt`**, so `w << val;` naturally blocks as a statement. Combined with per-endpoint independent refcounting (either end of a channel can close independently) and a rich combinator library (`tee`, `fanout`, `quantize`, `latch`, `killswitch`), this gives C++ a concurrency model that is arguably more expressive than Go's channels while remaining idiomatic C++.

### Timer Channels as First-Class Primitives ([csp](https://github.com/marcelocantos/csp))
Rather than providing timer callbacks or separate timeout APIs, csp implements `sleep`, `after`, and `tick` as **channels that produce values at scheduled times**. This means timers compose naturally with `alt` for timeouts ("read from data or timeout after 5s") and periodic processing ("tick every 100ms, merge with input"). The uniformity eliminates an entire category of API surface — there is no separate timer subsystem, just channels that happen to be time-driven.

### ASCII-Art Level Encoding ([multimaze2](https://github.com/squz/multimaze2))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md).*
### Live-Tunable Physics via Dashboard ([multimaze2](https://github.com/squz/multimaze2))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md).*
### GPU Mesh Reuse for 2D Silhouettes ([yourworld2](https://github.com/squz/yourworld2))

*Detailed narrative for this commercial work is in the private sibling: [progress-reports-private — week ending 2026-02-15](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-02-15.md).*
### Structured Binary/Shell Boundary ([gg](https://github.com/marcelocantos/gg))
The `gg` refactor introduced a clean separation: the Rust binary outputs **structured key=value data** (`action`, `git_dir`, `git_url`, `cd_dir`) instead of shell commands, and the generated shell function parses this data to perform git/cd/viewer operations with proper `"$var"` quoting. This eliminates shell injection **by construction** — the binary never produces executable shell code, and all interpolation happens in the shell function using properly quoted variables.

### Dissolving "Hard" Parsing Problems ([wbnf](https://github.com/arr-ai/wbnf))
The wbnf research paper argues that notorious parsing difficulties — C's typedef ambiguity, C++'s template angle brackets — are **not parsing problems at all** but semantic analysis problems. By constraining grammars to describe only surface syntax, these ambiguities dissolve. The paper proposes concrete mechanisms: regex/grammar unification (character classes as native grammar primitives), positional constraints (`@col`, `@line` predicates for indentation-sensitive languages), and algebraic grammar composition for clean sublanguage embedding.

---

## Effort Estimate: Traditional vs. AI-Assisted

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **yourworld2** | 20-35 | Country placement mechanics, carousel physics ported from Obj-C with sub-stepped symplectic Euler, GPU silhouette rendering from existing mesh buffers (spatial reasoning), audio integration, wire rendering continuation with iOS/Android direct mode, 59 commits of iteration. |
| **multimaze2** | 18-30 | Custom physics engine from scratch (ball-wall, ball-ball, springs, repulsion, friction — 52 tests, 310 assertions), then strategic replacement with Box2D v3 (constraint solver, shape types, joint system). Live-tunable tweaks system (self-registering, atomic, SQLite-persisted, dashboard-integrated, auto-rebuilding Box2D world). ASCII-art level parser for 72 levels. WebGPU sprite renderer with atlas UV mapping. |
| **csp** | 15-25 | Library extraction with namespace refactoring is mechanical but large. Timer primitives as channels require scheduler integration. M:N threading with work stealing is a PhD-level concurrency problem. Sanitizer support with fiber annotations requires deep understanding of ASan/TSan internals. RingBuffer rewrite fixing memory leaks and UB. nanobench integration. |
| **gg** | 8-12 | 17 commits of steady refinement. Interactive installer wizard, SSH/HTTPS URL handling with remote verification, shell injection fix (requires understanding the attack surface), clap v3 -> v4 migration, key=value protocol redesign, 27 integration tests, CI + release workflows, cross-compilation fix. |
| **wbnf** | 5-10 | A 717-line research paper with formal PL proposals, a related work survey spanning SDF/Rascal/PEG/OMeta/Ohm/LPEG/attribute grammars, and a concrete implementation roadmap. Academic-grade design work. |
| **bricabrac** | 3-5 | Test-first approach (23 new tests for concurrency correctness), assembly-to-Boost.Context migration (ABI expertise), then full module replacement with csp submodule (adapter header design). |
| **arrai** | 2-3 | Strategic analysis requiring deep codebase familiarity. |
| **hash** | 0.5 | Benchmark scaffolding. |
| **decimal** | 0.5 | Small fix, but requires understanding IEEE 754 rounding semantics to even spot the bug. |
| **multimaze** | 0.25 | Documentation. |

### The Diversity Tax

These estimates assume a developer who is already expert in the relevant domain. Specialisms exercised in a single week:

- WebGPU/Dawn rendering pipelines and WGSL shaders
- Custom rigid-body physics and Box2D v3 integration
- C++ microthreading, context switching, M:N scheduling
- C++ ABI and Boost.Context fiber annotations
- Rust CLI tooling (clap, shell code generation, cross-compilation)
- Go networking (TCP relay, WebSocket, REST)
- iOS and Android native development
- SQLite-backed live parameter tuning
- GPU orthographic projection and globe-space geometry
- Programming language theory and grammar formalisms
- IEEE 754 decimal arithmetic
- Hash function benchmarking and Go performance profiling

No single person holds all these at expert level. In a traditional team, this would involve 4-6 specialists with coordination overhead, design review meetings, and handoff friction.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|------------|----------------|
| **yourworld2** (59 commits) | 6-12 | Architecture decisions, carousel UX, visual comparison with original game, audio selection, testing on devices |
| **multimaze2** (19 commits) | 3-6 | Design intent, level verification, visual comparison with original, physics parameter tuning via tweaks UI, Box2D selection |
| **csp** (24 commits) | 3-6 | Deciding to extract, namespace/API design, M:N scheduler architecture, reviewing sanitizer integration |
| **gg** (17 commits) | 2-4 | Deciding the UX flow, testing shell integration, verifying CI |
| **bricabrac** (3 commits) | 1-2 | Directing test coverage, verifying Boost.Context migration, approving csp submodule switch |
| **wbnf** (research paper) | 1-3 | The PL ideas are human; the AI elaborated and surveyed related work |
| **arrai** (planning doc) | 0.5-1 | Strategic direction |
| **hash** (2 commits) | 0.25 | Quick benchmark pass |
| **decimal** | 0.25 | Spotting or reviewing the bug fix |
| **multimaze** | 0.15 | Quick doc pass |
| **Total** | **~17-35 hours** | |

### What If It Were One Person?

| Project | Expert days | Generalist days | The ramp-up cost |
|---------|------------|-----------------|------------------|
| **yourworld2** | 20-35 | 35-60 | Carousel physics porting from Obj-C requires matching exact force coefficients. GPU silhouette rendering straddles graphics and spatial math. Two mobile platforms. |
| **multimaze2** | 18-30 | 30-50 | Custom physics is trial-and-error-heavy. Box2D v3 integration. WebGPU pipeline setup. Atlas UV mapping with coordinate system quirks. SQLite-backed live tuning. |
| **csp** | 15-25 | 25-40 | M:N scheduling and work stealing are niche. Sanitizer fiber annotations require toolchain internals knowledge. |
| **gg** | 8-12 | 12-20 | Rust proficiency if not already there. Shell codegen subtleties. GitHub Actions. |
| **wbnf** | 5-10 | 10-20 | PL theory and grammar formalisms. The related work survey alone requires familiarity with the field. |
| **bricabrac** | 3-5 | 6-10 | C++ context switching, ABI details, Boost.Context API. Concurrency testing is subtle. |
| **arrai** | 2-3 | 5-8 | Requires deep codebase familiarity that a newcomer would need to build through extensive reading. |
| **hash** | 0.5 | 1 | Minor. |
| **decimal** | 0.5 | 1-2 | Understanding IEEE 754 rounding modes. |
| **multimaze** | 0.25 | 0.5-1 | Need to understand the legacy codebase to document it. |
| **Subtotal** | **73-126** | **~125-210** | |

Adding a ~15-25% context-switching tax for thrashing between C++/Go/Rust/iOS/PL-theory/physics/data-structures in a single week brings the realistic single-person estimate to **~145-260 person-days, or roughly 7-13 months**.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **120-220 person-days (6-11 months)** |
| Specialist team (traditional) | **73-126 person-days (4-7 person-months)** |
| Actual human effort this week | **~17-35 hours (~2-5 person-days)** |
| **Multiplier vs. generalist** | **~30-90x** |
| **Multiplier vs. specialist team** | **~15-50x** |

The multiplier is highest for cross-domain work (multimaze2 going from custom physics to Box2D integration in the same week, yourworld2 moving between GPU rendering and Obj-C physics porting) and for research/design work (wbnf paper, arrai strategic analysis) where the AI can explore design spaces and survey related work far faster than a human. The human contribution concentrates on vision, taste, architectural judgement, and the strategic decision-making that determines what gets built and how the pieces fit together.

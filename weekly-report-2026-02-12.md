# Weekly Progress Report — 2026-02-05…12 (8 days)

## Executive Summary

An exceptionally productive week across **10 repositories** spanning game development, library engineering, tooling, and strategic planning. The headline items: a game built from scratch (**multimaze2**), a major library extraction (**csp**), a significant data structure refactor (**frozen**), a CLI tool overhauled (**gg**), and a globe-based game brought to mobile with online multiplayer (**yourworld2**).

**115 commits** | **+22,834 net lines** | **~130-250 person-days traditional equivalent** | **~30-100x multiplier**

### Major Achievements & Innovations

- Built **multimaze2** from scratch — custom physics engine (gravity, friction, collisions, springs, repulsion), 72 levels parsed from ASCII art, WebGPU renderer with sprite atlas
- Invented **multi-round hashing** for frozen's HAMT: re-hashing with incremented seeds eliminates two node types (`leaf2`, `twig`), turning a fixed-depth trie into an effectively unbounded one (-280 lines, cleaner architecture)
- Designed **wire-based remote rendering** for yourworld2 — WebGPU wire protocol commands from headless server to mobile clients with progressive mipmapped texture streaming and ASTC compression (4x faster startup)
- Eliminated **shell injection by construction** in gg via a key=value protocol: the Rust binary never emits executable shell code; all interpolation happens in the shell function with proper quoting
- Proposed **dissolving "hard" parsing problems** in wbnf: C typedef ambiguity and C++ template brackets recast as semantic analysis problems, not parsing problems

### Tough Challenges Overcome

- **Custom rigid-body physics from scratch** (multimaze2): ball-wall and ball-ball collisions, spring bonds, repulsion forces, friction — notoriously fiddly to tune without an established engine, validated with 52 tests and 310 assertions
- **Wire rendering protocol design** (yourworld2): headless server → iOS/Android with robust reconnection (exponential backoff), progressive mip delivery with priority queues, wire-level truncation, and dual texture format support (ASTC + ETC2 fallback)
- **HAMT correctness reasoning** (frozen): proving multi-round hashing preserves semantics across all operations (Combine, Difference, Intersection, Get) while removing two node types required careful analysis of every code path
- **Boost.Context migration** (bricabrac): replacing 4 architecture-specific hand-written assembly files (~550 lines) with Boost.Context demanded ABI and calling-convention expertise across ARM64 and x86-64

Contributor: Marcelo Cantos

---

## Game Projects

### [squz/multimaze2](https://github.com/squz/multimaze2) — MultiMaze Rewrite (2 commits)
A complete rewrite of the [MultiMaze](https://github.com/squz/multimaze) physics-based maze puzzle game on the sq engine ([Dawn](https://dawn.googlesource.com/dawn)/WebGPU + [SDL3](https://github.com/libsdl-org/SDL)):
- **Initial implementation**: Maze model with wall bitmasks, artefacts (balls, homes, keys, switches, doors), ASCII-art level parser, 6 packs (72 levels), custom physics engine (gravity, friction, collisions, springs, repulsion), WebGPU renderer, HUD overlay, 52 tests with 310 assertions
- **Sprite rendering**: Replaced procedural geometry with textured sprite rendering from the original game's atlas, including quadrant corner system for walls, alpha-blended halos, and GL-to-WebGPU coordinate conversion

### [squz/yourworld2](https://github.com/squz/yourworld2) — Globe Game (83 commits)
Massive evolution of a globe-based world game:
- **Wire rendering architecture**: Headless server mode with wire-based remote rendering, robust reconnection with exponential backoff
- **Mobile support**: iOS direct mode with ETC2 texture fallback, Android direct mode, ASTC texture compression (4x faster startup), mipmapped progressive texture streaming
- **Networking**: Go TCP relay server with LSTN/ACPT/PING/ERRO protocol, web dashboard over WebSocket with dynamic ports
- **Performance**: Deferred mip streaming with priority queues, wire-level mip truncation, idle disconnect detection
- **Game mechanics**: Magnetic snap placement, placement detection/tracking, mouse + finger input with first-wins deduplication, drag inertia fix
- **Engine integration**: Simplified Application API (separate update/render), engine-managed resize, globe controller via sq::GlobeController
- **Infrastructure**: Visual regression tests, offscreen render capture, migrated to GitHub Issues

---

## Libraries & Infrastructure

### [marcelocantos/csp](https://github.com/marcelocantos/csp) — New CSP Library (1 commit, initial)
**Major library extraction** of a C++ microthreading library from [squz/bricabrac](https://github.com/squz/bricabrac) into a standalone repo:
- Cooperative microthreads with [Boost.Context](https://www.boost.org/doc/libs/release/libs/context/), typed synchronous channels, `alt`/`prialt` multiplexing (like Go's `select`)
- Rich stream combinators: `buffer`, `map`, `where`, `tee`, `fanout`, `chain`, `quantize`, `latch`, `killswitch`, `rpc`
- Namespace renamed from `brac` to `csp`, headers restructured to `include/csp/`
- 88 tests passing, standalone Makefile with Clang C++17

### [squz/bricabrac](https://github.com/squz/bricabrac) — Microthread Hardening (2 commits)
Test-first-then-refactor approach to the Thread subsystem:
- **23 new test cases** covering channels (move-only types, N-writers/N-readers, alt fairness, prialt priority), channel utilities (where, tee, latch, sinkhole), buffer edge cases, and volume stress tests (10K channel lifecycle, 2K microthreads)
- **Replaced custom assembly** (4 architecture-specific .s files) with [Boost.Context](https://www.boost.org/doc/libs/release/libs/context/) — eliminating ~550 lines of hand-written assembly while gaining cross-platform reliability

### [arr-ai/frozen](https://github.com/arr-ai/frozen) — HAMT Simplification (1 commit)
Significant structural refactor of the [Hash Array Mapped Trie](https://en.wikipedia.org/wiki/Hash_array_mapped_trie) internals:
- Eliminated `leaf2` and `twig` node types, replacing them with **multi-round hashing** (seed-parameterized rehashing when hash bits are exhausted) and a `collision` fallback node
- Node types reduced from 4 to 3; operation dispatch cases reduced from 4x4=16 to effectively 3x3=9
- Net **-280 lines** of code with cleaner architecture: removed `Canonical()` method, simplified with `collapse()`
- Correctness improvement: elements are now separated as long as their hashes differ in any round

### [anz-bank/decimal](https://github.com/marcelocantos/decimal) — Bug Fix (1 commit)
Fixed `Context.Sub()` silently ignoring the receiver context's rounding mode — it was calling `Decimal.Add` (which hardcodes HalfUp) instead of `ctx.Add`. Important for [IEEE 754-2019](https://en.wikipedia.org/wiki/IEEE_754) compliance.

---

## Tooling

### [marcelocantos/gg](https://github.com/marcelocantos/gg) — CLI Overhaul (17 commits)
Comprehensive modernization of the `gg` git shorthand tool (Rust):
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
- Proposes regex/grammar unification, integrated tokenization via labeled alternatives, generalized positional constraints (for indentation-sensitive parsing), and algebraic grammar composition
- Argues that "hard" parsing problems (C typedef ambiguity, C++ template brackets) dissolve when grammars describe only surface syntax
- Includes related work survey ([SDF](https://www.syntax-definition.org/), Rascal, PEG/OMeta/Ohm, [LPEG](http://www.inf.puc-rio.br/~roberto/lpeg/)) and implementation roadmap

### [squz/multimaze](https://github.com/squz/multimaze) — Documentation (1 commit)
Added CLAUDE.md documenting the legacy iOS game architecture for AI-assisted development.

---

## Other Team Work

### [squz/esfera2](https://github.com/squz/esfera2) — Spherical Chess (42 commits, Andrew Cantos)
Andrew built esfera2 from the ground up: a spherical chess game on a geodesic sphere board with pentagons and hexagons, two-pass translucency rendering, vertex welding, all 62 piece meshes with correct winding and rotation, click-to-select gameplay with legal move highlights, pawn promotion, endgame overlay, undo, move animation, game persistence, minimax AI with alpha-beta pruning on a background thread, 10-lesson interactive tutorial, platform migration from bgfx/GLFW/CMake to sq/SDL3/Make, iOS standalone app with touch coordinate handling, Go backend server with REST API + WebSocket game relay and matchmaking lobby, and OCI cloud deployment with security hardening. 42 commits, +10,092/-2,569 lines.

---

## Metrics

*All metrics below reflect Marcelo Cantos's contributions only.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched | 10 |
| Total commits | 115 |
| Total lines added | +27,025 |
| Total lines removed | -4,191 |
| Net new lines | +22,834 |
| File changes | 398 |
| Languages | C++, Go, Rust, Markdown, WGSL, YAML, Shell, SQL, Python |

*The csp lines are code extracted from bricabrac, not written from scratch this week.*

### Per-Repository Breakdown

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|
| [squz/yourworld2](https://github.com/squz/yourworld2) | 83 | 225 | +4,090 | -2,395 | +1,695 |
| [marcelocantos/gg](https://github.com/marcelocantos/gg) | 17 | 53 | +1,625 | -551 | +1,074 |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 2 | 33 | +5,794 | -246 | +5,548 |
| [squz/bricabrac](https://github.com/squz/bricabrac) | 2 | 18 | +697 | -264 | +433 |
| [arr-ai/wbnf](https://github.com/arr-ai/wbnf) | 1 | 2 | +789 | -0 | +789 |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | 1 | 10 | +399 | -679 | -280 |
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | 1 | 2 | +234 | -0 | +234 |
| [squz/multimaze](https://github.com/squz/multimaze) | 1 | 1 | +74 | -0 | +74 |
| [anz-bank/decimal](https://github.com/marcelocantos/decimal) | 1 | 1 | +2 | -2 | 0 |
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 1 | 49 | +13,273 | -0 | +13,273* |
| [squz/esfera2](https://github.com/squz/esfera2) | 5 | 4 | +48 | -54 | -6† |

*\*Extracted from bricabrac; not written from scratch this week.*
*†sq submodule pointer updates only.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [marcelocantos/csp](https://github.com/marcelocantos/csp) | 88 | Full suite extracted with library |
| [squz/multimaze2](https://github.com/squz/multimaze2) | 52 | 310 assertions; physics, levels, rendering |
| [marcelocantos/gg](https://github.com/marcelocantos/gg) | 27 | Rust integration tests + shell tests |
| [squz/bricabrac](https://github.com/squz/bricabrac) | 23 | Channels, alt fairness, volume stress |
| **Total** | **190** | |

---

## Ideas & Innovations

### Multi-Round Hashing for HAMTs ([frozen](https://github.com/arr-ai/frozen))
Rather than falling back to linear-scan nodes when hash bits are exhausted at maximum tree depth, the HAMT now **re-hashes keys with an incremented seed** to generate fresh hash bits on demand. This elegantly eliminates two special-case node types (`leaf2`, `twig`) and means the trie can keep splitting indefinitely for distinct keys, only resorting to a flat `collision` node for true hash-function degeneracy. The idea turns a fixed-depth trie into an effectively unbounded one without changing the external API.

### Wire-Based Remote Rendering ([yourworld2](https://github.com/squz/yourworld2))
The yourworld2 architecture sends WebGPU **wire protocol commands** from a headless server to remote clients (iOS, Android, browser) rather than streaming video or replicating game state. Combined with **progressive mipmapped texture streaming** (deferred mip delivery with priority queues, wire-level truncation, ASTC compression for 4x faster startup), this achieves a thin-client model where mobile devices render natively from a command stream — getting the quality of native rendering with the convenience of server-driven logic.

### CSP Microthreading with Action RAII ([csp](https://github.com/marcelocantos/csp))
The CSP library implements Go-style channel semantics in C++ with an elegant twist: channel operations return `action` objects whose **destructors invoke `prialt`**, so `w << val;` naturally blocks as a statement. Combined with per-endpoint independent refcounting (either end of a channel can close independently) and a rich combinator library (`tee`, `fanout`, `quantize`, `latch`, `killswitch`), this gives C++ a concurrency model that is arguably more expressive than Go's channels while remaining idiomatic C++.

### ASCII-Art Level Encoding ([multimaze2](https://github.com/squz/multimaze2))
The MultiMaze 2 level parser reads maze definitions from **ASCII art** — 72 levels across 6 packs are encoded as human-readable text art with wall bitmasks, artefact placement (balls, keys, switches, doors), and colour coding. This makes level design and debugging trivially visual while also serving as a compact, diff-friendly serialisation format.

### Dissolving "Hard" Parsing Problems ([wbnf](https://github.com/arr-ai/wbnf))
The wbnf research paper argues that notorious parsing difficulties — C's typedef ambiguity, C++'s template angle brackets — are **not parsing problems at all** but semantic analysis problems. By constraining grammars to describe only surface syntax, these ambiguities dissolve. The paper proposes concrete mechanisms: regex/grammar unification (character classes as native grammar primitives), positional constraints (`@col`, `@line` predicates for indentation-sensitive languages), and algebraic grammar composition for clean sublanguage embedding.

### Structured Binary/Shell Boundary ([gg](https://github.com/marcelocantos/gg))
The `gg` refactor introduced a clean separation: the Rust binary outputs **structured key=value data** (`action`, `git_dir`, `git_url`, `cd_dir`) instead of shell commands, and the generated shell function parses this data to perform git/cd/viewer operations with proper `"$var"` quoting. This eliminates shell injection **by construction** — the binary never produces executable shell code, and all interpolation happens in the shell function using properly quoted variables.

---

## Effort Estimate: Traditional vs. AI-Assisted

How much work would all of this represent in a traditional pre-agentic development setting? The line counts don't tell the real story — the diversity and intricacy of the work matters far more.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| **yourworld2** | 25-40 | The wire rendering architecture is a novel design — not off-the-shelf. Progressive mip streaming with priority queues and wire-level truncation is networking/graphics crossover work. ASTC/ETC2 texture pipeline. Custom TCP relay protocol. iOS *and* Android direct mode. 83 commits of iteration implies a lot of debugging and protocol tuning the line count doesn't capture. |
| **multimaze2** | 15-25 | Custom physics engine (ball-wall, ball-ball, springs, repulsion, friction) is notoriously fiddly to debug. 72 levels worth of ASCII-art parsing. WebGPU renderer. Then the atlas sprite work: quadrant corner system, UV mapping with GL→WebGPU V-flip, alpha blending. 52 tests with 310 assertions. |
| **gg** | 8-12 | 17 commits of steady refinement. Interactive installer wizard, SSH/HTTPS URL handling with remote verification, shell injection fix (requires understanding the attack surface), clap v3→v4 migration, key=value protocol redesign, 27 integration tests, CI + release workflows, cross-compilation fix. |
| **frozen** | 5-10 | The -280 net lines hides days of whiteboard time. Inventing multi-round hashing, reasoning about correctness across all HAMT operations (Combine, Difference, Intersection, Get), eliminating two node types while preserving semantics. This is pure algorithmic design work. |
| **wbnf** | 5-10 | A 717-line research paper with formal PL proposals, a related work survey spanning SDF/Rascal/PEG/OMeta/Ohm/LPEG/attribute grammars, and a concrete implementation roadmap. This is academic-grade design work. |
| **bricabrac** | 4-6 | Writing correct concurrency tests (channel fairness, move-only types, alt priority) is much harder than it looks. Assembly→Boost.Context migration requires ABI and calling-convention expertise. |
| **csp** | 3-5 | Extraction, not greenfield — but renamespacing, restructuring headers, standalone build system, and verifying 88 tests pass is real work. |
| **arrai** | 2-3 | Strategic analysis requiring deep codebase familiarity. |
| **decimal** | 0.5 | Small fix, but requires understanding IEEE 754 rounding semantics to even spot the bug. |
| **multimaze** | 0.25 | Documentation. |

### The Diversity Tax

These estimates assume a developer who is already expert in the relevant domain. But look at the range of specialisms exercised in a single week:

- WebGPU/Dawn rendering pipelines and WGSL shaders
- Custom rigid-body physics
- Go networking (TCP relay, WebSocket, REST)
- Rust CLI tooling (clap, shell code generation)
- iOS and Android native development
- ASTC/ETC2 texture compression and mip streaming
- HAMT algorithm design and hash theory
- C++ microthreading, context switching, and ABI
- Programming language theory and grammar formalisms
- IEEE 754 decimal arithmetic

No single person holds all these at expert level. In a traditional team, this would involve 4-6 specialists with coordination overhead, design review meetings, and handoff friction.

### Actual Human Effort This Week

In an AI-assisted workflow, the human role is directing, reviewing, deciding, and course-correcting — not writing every line. The actual human hours spent are a fraction of calendar time:

| Project | Human hours | The human work |
|---------|------------|----------------|
| **yourworld2** (83 commits) | 8-15 | Architecture decisions, testing on devices, debugging mobile-specific issues |
| **gg** (17 commits) | 2-4 | Deciding the UX flow, testing shell integration, verifying CI |
| **multimaze2** (2 big commits) | 2-4 | Design intent, level verification, visual comparison with original |
| **frozen** (1 commit) | 1-3 | The algorithmic insight — the most human-thinking-heavy per line |
| **bricabrac** (2 commits) | 1-2 | Directing test coverage, verifying Boost.Context migration |
| **csp** (extraction) | 1-2 | Deciding to extract, reviewing namespace changes |
| **wbnf** (research paper) | 1-3 | The PL ideas are human; the AI elaborated and surveyed related work |
| **arrai** (planning doc) | 0.5-1 | Strategic direction |
| **decimal** | 0.25 | Spotting or reviewing the bug fix |
| **multimaze** | 0.15 | Quick doc pass |
| **Total** | **~17-35 hours** | |

### What If It Were One Person?

The specialist estimates above assume a developer who is already expert in the relevant domain. But the work this week spans at least 10 distinct specialisms — WebGPU shaders, custom physics, Go networking, Rust CLI tooling, iOS/Android, texture compression, HAMT algorithm design, C++ ABI/context-switching, PL theory, and IEEE 754 arithmetic. No single person holds all of these at expert level.

A talented generalist — a strong senior/staff engineer comfortable picking up anything — would face two compounding costs: learning curves in unfamiliar domains, and serial context-switching with no ability to parallelise.

| Project | Expert days | Generalist days | The ramp-up cost |
|---------|------------|-----------------|------------------|
| **yourworld2** | 25-40 | 40-70 | Wire protocol is novel design work. ASTC/ETC2 texture formats are specialised. Progressive mip streaming straddles graphics and networking. Two mobile platforms. |
| **multimaze2** | 15-25 | 25-40 | Physics engine tuning is trial-and-error-heavy. WebGPU pipeline setup. Atlas UV mapping with coordinate system quirks. |
| **gg** | 8-12 | 12-20 | Rust proficiency if not already there. Shell codegen subtleties. GitHub Actions. |
| **frozen** | 5-10 | 10-20 | HAMT internals are niche. Without prior experience, understanding the existing 4-node-type design well enough to simplify it takes real study. |
| **wbnf** | 5-10 | 10-20 | PL theory and grammar formalisms. The related work survey alone requires familiarity with the field. |
| **bricabrac** | 4-6 | 8-12 | C++ context switching, ABI details, Boost.Context API. Concurrency testing is subtle. |
| **csp** | 3-5 | 4-7 | Mostly mechanical extraction — least affected by expertise gap. |
| **arrai** | 2-3 | 5-8 | Requires deep codebase familiarity that a newcomer would need to build through extensive reading. |
| **decimal** | 0.5 | 1-2 | Understanding the library's Context model and IEEE 754 rounding modes. |
| **multimaze** | 0.25 | 0.5-1 | Need to understand the legacy codebase to document it. |
| **Subtotal** | **70-115** | **~115-200** | |

Adding a ~15-25% context-switching tax for thrashing between C++/Go/Rust/iOS/PL-theory/data-structures in a single week brings the realistic single-person estimate to **~130-250 person-days, or roughly 7-13 months**.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **130-250 person-days (7-13 months)** |
| Specialist team (traditional) | **70-115 person-days (4-6 person-months)** |
| Actual human effort this week | **~17-35 hours (~2-5 person-days)** |
| **Multiplier vs. generalist** | **~30-100x** |
| **Multiplier vs. specialist team** | **~15-50x** |

The multiplier is highest for research/design work (frozen, wbnf) where the AI can explore a design space much faster than a human sketching on a whiteboard, and for cross-domain work (yourworld2) where a single agent seamlessly moves between wire protocol design, texture compression, and mobile platform integration without context-switch overhead. The human contribution concentrates on what humans do best: vision, taste, architectural judgement, and the occasional flash of algorithmic insight that sets the AI on the right path.

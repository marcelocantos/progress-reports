# [marcelocantos/cv](https://github.com/marcelocantos/cv)

cv is a from-scratch build tool in Go — Make's dependency-graph model without the accumulated friction: content hashing instead of timestamps, clean syntax, no `$$` escaping, and a single cross-project graph. It shipped its first five releases under the name `mk`.

## The journey

**mk** was conceived and delivered in a single four-day burst in February 2026 — 39 commits, +7,536/-380, five releases (v0.1.0 → v0.5.0) and a [Homebrew](https://brew.sh/) formula. The language was designed rather than cloned: pattern rules with glob and regex constraints on captures, multi-output rules, order-only prerequisites, `$[...]` functions, `for` loops that generate rules and variables across a matrix, build configs composable by `+` with exclusion and state isolation, user-defined functions with a hash cache, scoped includes with automatic path rebasing, and parallel execution with CPU-capacity detection. Two features were genuinely novel: `[fingerprint: command]` tracks non-file artefacts by the hash of a command's output, and `$changed` hands a recipe exactly the inputs that moved. An embedded standard library (`std/c.mk`, `std/cxx.mk`, `std/go.mk`), shell completions, an `--help-agent` guide, a `DESIGN.md`, CI across darwin-arm64 and Linux amd64/arm64, and a self-hosting build file all landed inside the same window. The hardest single problem was prerequisite merging: when several pattern rules match one target their prerequisites must combine without introducing a cycle, which needed a topological analysis phase during rule resolution that also reports ambiguous matches.

A quieter period followed — inline-comment stripping that leaves `#` alone inside recipes, tests for cross-module references and nested includes, and a `STABILITY.md` cataloguing the CLI, file syntax, standard library, build-state format and Go API with stability ratings. The tool's main visible effect over the next two months was on everything else: a cross-project latency-reduction campaign wrapped `cc`/`cxx` with **ccache** through mk's standard libraries, giving [csp](csp.md), [sqlift](sqlift.md), [sqlpipe](sqlpipe.md), sysinfo-mcp, esfera2 and yourworld2 a shared cache — roughly 30–50% hit rates on warm rebuilds and a 2–4× speedup on the first clean build of the day.

Then the project was **renamed to cv**, and its first major feature under the new name was the most self-contained new engineering of its week: the discovered-dependencies model of `DESIGN.md` §11, shipped in v0.9.0 with 37 new tests. It replaces Make's `-MMD` / `-include *.d` / `-MP` header-tracking ritual with a first-class distinction — **hard edges, declared in the build file, constrain ordering and staleness; soft edges, discovered after a run and recorded, constrain staleness only**. The elegant part is the vanished-soft-dep rule: a discovered dependency that disappears counts as *changed*, never as a missing input, so the stale edge triggers precisely the rebuild that erases it, and the `-MP` empty-phony-rule hack becomes unnecessary. The model then generalises symmetrically — depfile adapters across five formats, in-graph verification of undeclared reads, two-phase `[scan]` nodes that run analysis before the heavy recipe, dynamic `[writes: manifest]` outputs folded into the build database, and whole-recipe `strace` tracing on Linux that captures reads and writes no compiler-specific depfile would report. v0.10.0 completed the rename a week later, carrying the `.mk` → `.cv` stdlib extensions and the identifier sweep; the downstream repositories migrated in their own tail of mechanical PRs.

## Highlights

- **From language design to Homebrew in four days** — 39 commits and five releases covering parser, dependency graph, pattern rules with constraint propagation, build configs, fingerprinting, standard library, CI, formula, completions and a self-hosting build file. ([2026-02-22](../../reports/weekly-report-2026-02-22.md))
- **Stability surface declared** — `STABILITY.md` rates the CLI flags, file syntax, standard library, build-state format and Go API, alongside inline-comment handling and nested-include tests. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **ccache through the standard library** — one wrapper in `std` gives the whole C/C++ fleet a shared cache, worth ~30–50% on warm rebuilds and 2–4× on the first clean build of the day. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **Renamed cv, and discovered dependencies land** — v0.9.0's hard/soft edge model with self-healing vanished-dependency semantics, symmetric output discovery, scan nodes and Linux `strace` tracing, with 37 new tests. ([2026-05-31](../../reports/weekly-report-2026-05-31.md))
- **Rename completed in v0.10.0** — `.mk` → `.cv` stdlib extensions and the identifier sweep converge, and the stray binary committed mid-rename is removed. ([2026-06-07](../../reports/weekly-report-2026-06-07.md))

## Standouts

- **Merging prerequisites without minting a cycle** — when several pattern rules match one target their prerequisite lists must combine into a single dependency set that stays acyclic. Solved with a topological analysis phase inside rule resolution that also detects and reports ambiguous matches rather than silently picking one. ([2026-02-22](../../reports/weekly-report-2026-02-22.md))
- **A build language designed, not cloned, in four days** — parser, dependency-graph engine, pattern rules with glob/regex constraint propagation, composable build configs, parallel execution, an embedded standard library, CI, completions, a self-hosting build file and five releases to Homebrew. `[fingerprint: command]` tracks non-file artefacts by the hash of a command's output, and scoped `include` rebases paths automatically so definitions compose across nested projects. ([2026-02-22](../../reports/weekly-report-2026-02-22.md))
- **ccache smuggled in through the standard library** — wrapping `cc`/`cxx` in `std` handed the entire C/C++ fleet a shared cache in one change, worth roughly 30–50% on warm rebuilds and 2–4× on the first clean build of the day. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **The vanished dependency that heals itself** — Make needs `-MMD`, `-include *.d` and `-MP` to keep a deleted header from breaking the build. cv splits hard edges (declared, constrain ordering and staleness) from soft edges (discovered post-run, constrain staleness only), and treats a discovered dependency that disappears as *changed* rather than *missing* — so the stale edge triggers precisely the rebuild that erases it, and the empty-phony-rule hack becomes unnecessary. ([2026-05-31](../../reports/weekly-report-2026-05-31.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 7 |
| Commits | ~49 |
| Human attention | ~5–10 h |
| Traditional equivalent | ~2.3–3.5 months |
| Multiplier | ~20–95× |

## Weekly reports

[02-22](../../reports/weekly-report-2026-02-22.md), [03-01](../../reports/weekly-report-2026-03-01.md), [04-19](../../reports/weekly-report-2026-04-19.md), [04-26](../../reports/weekly-report-2026-04-26.md), [05-03](../../reports/weekly-report-2026-05-03.md), [05-31](../../reports/weekly-report-2026-05-31.md), [06-07](../../reports/weekly-report-2026-06-07.md)

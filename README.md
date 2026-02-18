# Progress Reports

Weekly progress reports for Marcelo Cantos's AI-assisted development work.

## Reports

<details>
<summary><a href="weekly-report-2026-02-18.md"><b>2026-02-13…18 (6 days)</b></a> M:N scheduler with TLA+ verification, 50+ stream combinators, mmap stack pool, HAMT allocation elimination (75%), Box2D integration, live-tunable physics, GPU mesh reuse for silhouettes</summary>

Built the **csp** C++ microthreading library from a bare extraction into a production platform (M:N scheduler, 50+ stream combinators, TLA+ formal verification, kqueue I/O, mmap stack pool, persistent HAMT for dynamic scoping). **frozen** HAMT allocation elimination campaign (batched spine allocation, leaf2 reintroduction, boxing elimination — up to 75% fewer allocations). **multimaze2** Box2D v3 integration and live-tunable physics with SQLite persistence. **yourworld2** country carousel with GPU mesh reuse for silhouettes and audio integration. 108 commits across 6 repos.

</details>

<details>
<summary><a href="weekly-report-2026-02-12.md"><b>2026-02-05…12 (8 days)</b></a> wire-based remote rendering, custom physics engine + 72 levels, multi-round HAMT hashing (-280 lines), shell injection elimination by construction, CLI interactive installer, universal grammar research</summary>

**yourworld2** wire-based remote rendering architecture with progressive mip streaming across iOS and Android. **multimaze2** built from scratch (custom physics, 72 ASCII-art levels, WebGPU renderer, sprite atlas). **gg** CLI overhaul (interactive installer, shell injection elimination, 27 integration tests). **frozen** HAMT simplification via multi-round hashing (-280 lines, 2 node types eliminated). **csp** library extraction from bricabrac. **wbnf** universal grammar research paper. 115 commits across 10 repos.

</details>

## Guide

See [weekly-report-guide.md](weekly-report-guide.md) for agent-optimised instructions on generating these reports.

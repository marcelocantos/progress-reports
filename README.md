# Progress Reports

Weekly progress reports for Marcelo Cantos's AI-assisted development work.

## The Journey So Far

These reports started on 5 February 2026. In the 32 days since, the output totals 1,051 commits across 27 repositories, spanning C++, Go, Rust, C#, Swift, Svelte, TLA+, WGSL, SQL, and assembly. The estimated traditional equivalent is 2.3 to 4.0 years of full-time work.

The numbers, whilst truly staggering, are the least interesting part.

What stands out is the nature of the work. This is not boilerplate generation. The period includes a C++ microthreading library with M:N scheduling, formal verification, and a cross-platform port across three OS-specific reactor backends. A build tool that went from nothing to Homebrew in 4 days. A persistent data structure campaign that yielded 500x speedup on set inequality through a two-level hash architecture. A SQL transpiler with FK-guided join path algebra and PostgreSQL backend. Contributions accepted into the Go compiler. A custom physics engine. Wire-based remote rendering for mobile. An AI capability broker with three-level policy escalation. ARM64 ABI debugging. Unity lifecycle audits. Programming language theory papers. A full-stack health management system rewrite (C#/SvelteKit/SQL Server with MFA, QR session transfer, 30+ screens). A geography game built from globe renderer to complete game experience in a single day. A native iOS app with QR-based server discovery.

No single person holds expert-level knowledge in all of these areas. Traditionally, this breadth would require a team of specialists with coordination overhead, handoff friction, and design meetings. Here, one person directed AI agents across all of it, moving freely between formal methods and game physics, between parser construction and mobile platform engineering, without context-switch penalty.

The human role shifted. Writing code is no longer the bottleneck. The actual human effort was roughly 90-170 hours across 32 days — about 3-5 hours per day — spent on architecture decisions, quality review, algorithmic insight, and course correction. The AI handled the volume. The human handled the direction.

Several projects went from nothing to released software in days: mk (build tool, 4 days to Homebrew with 5 releases), sqldeep (SQL transpiler to v0.5.0), doit (capability broker, MCP integration), jevon (multi-session orchestrator with iOS app). HMS2 went from vertical slice to 30+ functional screens with MFA and QR session transfer in a week. These were not prototypes. They shipped with CI, documentation, test suites, and versioned releases.

The consistency matters more than any individual result. Every week maintained a 25-100x multiplier over traditional development, across wildly different domains. The multiplier did not depend on easy problems — it held through formal verification, novel algorithm design, and cross-platform systems programming. It was highest on the hardest work, where the AI's ability to explore design spaces and handle cross-domain knowledge mattered most.

This is 32 days in. The tooling is still maturing and the workflows are still being refined. But the fundamental capability — one person directing AI to produce years of output per month, across arbitrary technical domains, at production quality — is already real and consistent.

## Reports

<details>
<summary><a href="weekly-report-2026-03-08.md"><b>2026-03-02…08 (7 days)</b></a> HMS2 full-stack rewrite (C#/SvelteKit/30+ screens/MFA/QR transfer), yourworld2 wave-based game buildout, csp channel use-after-free fix + buffered channels, jevon iOS app + QR discovery, frozen zero-alloc reads</summary>

<b>hms</b> HMS2 full-stack rewrite: Go-to-C# backend migration, SvelteKit SPA, 30+ screens across 16 API domains, TOTP MFA, QR session transfer. <b>yourworld2</b> wave-based feature buildout — 5 game modes, menu/tutorial/achievement systems, audio, zoom, HUD — from globe renderer to complete game in one day. <b>csp</b> channel use-after-free fix, buffered channels, CI flake resolution, Windows port completion (v0.3.0). <b>jevon</b> renamed from dais with iOS app, QR server discovery, filesystem session discovery, trust model. <b>frozen</b> zero-alloc read path (v1.10.0, v1.11.0). <b>ge</b> protocol v4 with orientation pipeline and reconnect reliability. SQL stack: sqldeep PostgreSQL backend, sqlift C-only API, sqlpipe Go wrapper. 305 commits across 15 repos. ~5-9 months traditional equivalent.

</details>

<details>
<summary><a href="weekly-report-2026-03-01.md"><b>2026-02-23…03-01 (7 days)</b></a> csp 5-phase Windows port + TLA+ verification, frozen H128 500x equality speedup, sqldeep transpiler from scratch, dais + doit new Claude Code tools, stock-car-racing Unity 6 + null-ref audit</summary>

<b>csp</b> completed a full 5-phase Windows port (kqueue/epoll/Windows thread pool reactors), TLA+ formal verification for 4 concurrent protocols, and ARM64 thread-local corruption fix. <b>frozen</b> H128 128-bit content hash + recursive XOR hash (h0) delivering 500x set inequality speedup. <b>sqldeep</b> built from scratch as SQL transpiler with FK-guided join path algebra (4 releases). <b>dais</b> multi-session Claude Code orchestrator and <b>doit</b> three-level capability broker both designed and shipped. <b>sqlift</b> Go port with cross-language hash verification (6 releases). <b>stock-car-racing</b> Unity 6 upgrade with 61-finding null-ref audit. 364 commits across 13 repos. ~6-10 months traditional equivalent.

</details>

<details>
<summary><a href="weekly-report-2026-02-22.md"><b>2026-02-19…22 (4 days)</b></a> mk build tool from scratch to Homebrew, csp topology surgery + cancellation + ~20 combinators, sqlift + sqlpipe new libraries, yourworld2 state sync via sqlpipe</summary>

<b>mk</b> built from scratch as a modern build tool (pattern rules, parallel execution, stdlib) and shipped 5 releases to Homebrew. <b>csp</b> added ~20 more combinators, channel topology surgery (swap/fuse/splice/tap), cancellation framework with cancel-aware TLS, C++23 migration, and 6-paper engineering series. Two new C++ libraries: <b>sqlift</b> (declarative SQLite migration) and <b>sqlpipe</b> (streaming SQLite replication). <b>yourworld2</b> gained SQLite-backed game state with bidirectional sync via sqlpipe. 159 commits across 10 repos. ~5-8 months traditional equivalent.

</details>

<details>
<summary><a href="weekly-report-2026-02-18.md"><b>2026-02-13…18 (6 days)</b></a> M:N scheduler with TLA+ verification, 50+ stream combinators, mmap stack pool, HAMT allocation elimination (75%), Box2D integration, live-tunable physics, GPU mesh reuse for silhouettes</summary>

Built the <b>csp</b> C++ microthreading library from a bare extraction into a production platform (M:N scheduler, 50+ stream combinators, TLA+ formal verification, kqueue I/O, mmap stack pool, persistent HAMT for dynamic scoping). <b>frozen</b> HAMT allocation elimination campaign (batched spine allocation, leaf2 reintroduction, boxing elimination — up to 75% fewer allocations). <b>multimaze2</b> Box2D v3 integration and live-tunable physics with SQLite persistence. <b>yourworld2</b> country carousel with GPU mesh reuse for silhouettes and audio integration. 108 commits across 6 repos. ~5-9 months traditional equivalent.

</details>

<details>
<summary><a href="weekly-report-2026-02-12.md"><b>2026-02-05…12 (8 days)</b></a> wire-based remote rendering, custom physics engine + 72 levels, multi-round HAMT hashing (-280 lines), shell injection elimination by construction, CLI interactive installer, universal grammar research</summary>

<b>yourworld2</b> wire-based remote rendering architecture with progressive mip streaming across iOS and Android. <b>multimaze2</b> built from scratch (custom physics, 72 ASCII-art levels, WebGPU renderer, sprite atlas). <b>gg</b> CLI overhaul (interactive installer, shell injection elimination, 27 integration tests). <b>frozen</b> HAMT simplification via multi-round hashing (-280 lines, 2 node types eliminated). <b>csp</b> library extraction from bricabrac. <b>wbnf</b> universal grammar research paper. 115 commits across 10 repos. ~7-13 months traditional equivalent.

</details>

## Metrics

| Period | Days | <img src="https://github.githubassets.com/favicons/favicon.svg" width="16"> | Equiv.&nbsp;(mo) | Gain | Highlights |
|--------|------|---|-------------|-------|------------|
| [03-02](weekly-report-2026-03-08.md) | 7 | 305 | 5-9 | 25-45x | HMS2 full rewrite, yourworld2 game buildout, csp channel fix + buffered channels, jevon iOS app, frozen zero-alloc |
| [02-23](weekly-report-2026-03-01.md) | 7 | 364 | 6-10 | 25-50x | csp Windows port + TLA+, frozen H128 500x speedup, sqldeep transpiler, dais + doit, Unity 6 audit |
| [02-19](weekly-report-2026-02-22.md) | 4 | 159 | 5-8 | 25-50x | mk from scratch to Homebrew, csp topology surgery + cancellation, sqlift + sqlpipe, yourworld2 state sync |
| [02-13](weekly-report-2026-02-18.md) | 6 | 108 | 5-9 | 30-75x | M:N scheduler + TLA+ verification, HAMT allocation -75%, Box2D physics, GPU silhouettes |
| [02-05](weekly-report-2026-02-12.md) | 8 | 115 | 7-13 | 30-100x | Wire-based remote rendering, custom physics + 72 levels, HAMT -280 lines, CLI installer |
| **Totals** | **32** | **1,051** | **2.3-4.2y** | | |

## Guide

See [weekly-report-guide.md](weekly-report-guide.md) for detailed instructions on generating these reports. Project-level directives are in [CLAUDE.md](CLAUDE.md).

# Per-Repo Pages

One summarised page per repository. Commercial detail for HMS, minicades, and non-`ge` Squz work lives in [progress-reports-private](https://github.com/marcelocantos/progress-reports-private); public pages keep names and links only. Each page distils that project's arc across
the whole series — organised by phases and themes, not week-by-week — with
highlights linking back to the weekly reports. Pages and this index are created
and maintained by the weekly report runs (see
[guide section 7](../guide.md#7-per-repo-pages)); a self-healing backfill sweep
on every run fills in anything missing.

A repository earns a page once it has two or more dedicated weekly-report
sections. Renamed projects are folded into one page: tern → [pigeon](pigeon.md),
mk → [cv](cv.md), dais → jevon → [jevons](jevons.md), targets →
[bullseye](bullseye.md), multimaze → multimaze2 (private), sq →
[ge](ge.md), marcelocantos/orthograph → [canticode/orthograph](orthograph.md).

## Games & Engines

- [squz/ge](ge.md) — cross-platform C++ game engine extracted from yourworld2; runs every squz title, now on four platforms
- **Commercial Squz titles** (detail private): [yourworld2](https://github.com/marcelocantos/progress-reports-private/blob/master/docs/repos/yourworld2.md), [yourworld](https://github.com/marcelocantos/progress-reports-private/blob/master/docs/repos/yourworld.md), [multimaze2](https://github.com/marcelocantos/progress-reports-private/blob/master/docs/repos/multimaze2.md), [esfera2](https://github.com/marcelocantos/progress-reports-private/blob/master/docs/repos/esfera2.md) — see [progress-reports-private](https://github.com/marcelocantos/progress-reports-private)


## Libraries & Infrastructure

- [marcelocantos/csp](csp.md) — C++ CSP concurrency library: M:N scheduler, channels, HTTP and QUIC stacks, TLA+ models
- [marcelocantos/pigeon](pigeon.md) — end-to-end encrypted relay with AEAD channels, QUIC transport, and five-language codegen
- [marcelocantos/sqlpipe](sqlpipe.md) — bidirectional SQLite replication with a TLA+-verified protocol and a predicate bytecode VM
- [marcelocantos/sqldeep](sqldeep.md) — SQL transpiler with FROM-first syntax and four-language bindings
- [marcelocantos/sqlift](sqlift.md) — schema migration in C and Go with cross-language verification
- [marcelocantos/rustuml](rustuml.md) — Rust PlantUML renderer pursuing pixel and XML parity with the Java original
- [arr-ai/frozen](frozen.md) — persistent immutable collections; 128-bit content hashing for fast inequality
- [arr-ai/hash](hash.md) — hashing primitives behind frozen; seedless hash128 so nested values can cache
- [arr-ai/arrai](arrai.md) — relational programming language; interned shape-backed tuples and lexical-frame scopes
- [arr-ai/wbnf](wbnf.md) — grammar language behind the arr.ai ecosystem
- [marcelocantos/cworkers](cworkers.md) — worker broker rewritten from Go to C, 15 MB to 35 KB
- [marcelocantos/mcpbridge](mcpbridge.md) — Go library for bimodal MCP servers: daemon plus stdio proxy over a socket
- [marcelocantos/go-decimal-proposal](go-decimal-proposal.md) — IEEE 754 decimal64/128 proposal for the Go standard library
- [marcelocantos/threedee](threedee.md) — parametric 3D models, migrated from OpenSCAD to build123d

## Agent & Fleet Tooling

- [marcelocantos/mnemo](mnemo.md) — indexes every agent transcript; search, compaction, federation, and a vault wing
- [marcelocantos/spyder](spyder.md) — mobile device orchestration and the game fleet's sole control plane
- [marcelocantos/jevons](jevons.md) — fleet cockpit: durable agent threads, cost governance, and a browser chat surface
- [marcelocantos/claudia](claudia.md) — Go library for embedding Claude Code and Grok agents in task or session mode
- [marcelocantos/bullseye](bullseye.md) — Rust MCP convergence-target ledger; the canonical record of followable work
- [marcelocantos/sawmill](sawmill.md) — structural code transformation over 18 languages, with a semantic git index
- [marcelocantos/cv](cv.md) — build tool with a content-hash graph and a discovered-dependencies model
- [marcelocantos/den](den.md) — universal development-environment manager sharing Homebrew's Cellar
- [marcelocantos/doit](doit.md) — three-level capability broker with an audit log and a threat model
- [marcelocantos/crosshair](crosshair.md) — Rust convergence-executor daemon with a stateless tick loop
- [marcelocantos/mcpsafe](mcpsafe.md) — credential-injecting MCP proxy with Starlark request transforms
- [marcelocantos/ytt](ytt.md) — YouTube transcript ingest pipeline with self-healing scheduled runs
- [marcelocantos/vellum](vellum.md) — document conversion MCP server with atomic clipboard delivery
- [marcelocantos/slacker](slacker.md) — multi-workspace Slack MCP; browser OAuth to the keychain, no secret ever a tool argument
- [canticode/orthograph](orthograph.md) — Pencil-first shared sketch surface; Mac daemon, MCP scene graph, iPad app; now a Canticode product
- [marcelocantos/pageflip](pageflip.md) — meeting capture behind a compile-time egress gate
- [marcelocantos/sysinfo-mcp](sysinfo-mcp.md) — C MCP server exposing macOS system metrics
- [marcelocantos/mpe2pdf](mpe2pdf.md) — Markdown to PDF conversion, later an MCP server

## Client Work

Detail for HMS and Minicades titles lives in the private sibling ([progress-reports-private](https://github.com/marcelocantos/progress-reports-private)):

- [Health-Management-Systems/hms](https://github.com/marcelocantos/progress-reports-private/blob/master/docs/repos/hms.md)
- [minicadesmobile/stock-car-racing](https://github.com/marcelocantos/progress-reports-private/blob/master/docs/repos/stock-car-racing.md)
- [minicadesmobile/kart-stars](https://github.com/marcelocantos/progress-reports-private/blob/master/docs/repos/kart-stars.md)
- [minicadesmobile/dragster-mayhem](https://github.com/marcelocantos/progress-reports-private/blob/master/docs/repos/dragster-mayhem.md)
- [minicadesmobile/mopar-drag-n-brag](https://github.com/marcelocantos/progress-reports-private/blob/master/docs/repos/mopar-drag-n-brag.md)
- [minicadesmobile/Minicadeskit](https://github.com/marcelocantos/progress-reports-private/blob/master/docs/repos/minicadeskit.md)


## Meta

- [marcelocantos/progress-reports](progress-reports.md) — this series, and the evolution of its measurement honesty
- [marcelocantos/skills](skills.md) — the published mirror of the shared agent skill tree
- [marcelocantos/homebrew-tap](homebrew-tap.md) — the fleet's Homebrew delivery endpoint

## Minor appearances

Repositories with a single dedicated section so far. They earn a page on their
second.

- marcelocantos/marcelocantos.com — personal Hugo site; blog and an open-source products page
- marcelocantos/writ — declared-intent execution: manifests compiled into a seatbelt profile, egress proxy, and drift audit
- marcelocantos/blurter — spool-first notification daemon; applications spool to disk, the daemon owns credential and policy
- marcelocantos/marcelocantos.github.io — interactive maths and 3D demos on a shared Three.js shell
- marcelocantos/asc — App Store Connect client for sales, apps, and reviews without a browser
- marcelocantos/issuepipe — GitHub issue webhooks ingested into per-repo tables for local consumption
- marcelocantos/gg — Git CLI overhaul with a structured binary and shell boundary
- marcelocantos/real — language design exploration
- marcelocantos/pairdroid — seamless Android wireless ADB via a relay
- marcelocantos/protocol-app — Android health and habit tracker, prepared for open-sourcing
- marcelocantos/solarmon — solar inverter monitor
- marcelocantos/go-ios — fork carrying the tunnel self-heal used by spyder
- linqgo/linq — LINQ for Go, migrated to `iter.Seq` in v2
- marcelocantos/tapper — Homebrew tap publisher with per-tap keychain tokens and codesigned ACLs
- marcelocantos/finance — personal statement fetchers, PDF transcripts as the oracle, double-entry journal; no data in the repo
- marcelocantos/downstream — incremental Markdown parser emitting Enter/Exit/Text/Attr events
- marcelocantos/housekeeping — disk-audit snapshots (486 GB reclaimed); authored findings only, dumps excluded from ☲
- squz/nostalgia — detail in [private](https://github.com/marcelocantos/progress-reports-private)
- squz/bricabrac — detail in [private](https://github.com/marcelocantos/progress-reports-private)
- unwisegames/tiltbuggy — the reference title behind ge's differential physics oracle
- golang/go — decimal128 ABI and DWARF support contributions
- anz-bank/decimal — arbitrary-precision decimal library bug fix

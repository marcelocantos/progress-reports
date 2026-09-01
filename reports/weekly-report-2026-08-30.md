# Weekly Progress Report — 2026-08-24…30

## Executive Summary

**Eighteen repositories** landed **183 commits** — a broader week than the last, with the fleet still the heaviest line and three other lines that would each have been a headline in a quieter month. **[marcelocantos/jevons](https://github.com/marcelocantos/jevons)** (77 commits) made the React cockpit the daily UI, persisted coalesced transcripts in SQLite, and taught Cursor ACP not to deadlock on remint; an exhausted model now falls down its ladder instead of being re-briefed forever, and the tmux **anchor pane** is what holds the fleet server open. **[marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)** (23 commits, v0.89.0–v0.90.0) compressed hot fields, stopped metadata-only migrations paying for an 18 GB backup, cut tool-surface *weight* 32%, and vendored multithreaded libzstd (the 52k-line amalgamation is excluded from ☲). **[arr-ai/arrai](https://github.com/arr-ai/arrai)** rebuilt tuples as interned shape-backed structs and scopes as lexical frames; **[arr-ai/hash](https://github.com/arr-ai/hash)** extracted seedless hash128 so nested values can cache. **[canticode/orthograph](https://github.com/canticode/orthograph)** became a Canticode product — closed-source conversion plus the work since 22 August, including HTTP MCP on the daemon and a padlink/render/iOS expansion, published through a new **[marcelocantos/tapper](https://github.com/marcelocantos/tapper)** (v0.2.0/v0.2.1) rather than a CI job holding a tap token. **[marcelocantos/claudia](https://github.com/marcelocantos/claudia)** v0.28.0 added Cursor models and recovered a vanished tmux server; **[marcelocantos/spyder](https://github.com/marcelocantos/spyder)** grew a ship front-door that puts studio secrets in the keychain, not in Actions. **[marcelocantos/vellum](https://github.com/marcelocantos/vellum)** v0.15–v0.17 is a Markdown viewer with TOC, lightbox and theme. **[marcelocantos/finance](https://github.com/marcelocantos/finance)** is new: statement fetchers, PDF transcripts as the oracle, a chained per-account audit, and a double-entry journal — no data in the repo. Commercial in-flight only this week: [private week 2026-08-30](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-30.md).

**183 commits** | **+107,414 net lines** | **~60-95 person-days traditional equivalent** | **~40-70x multiplier**

> Honesty note: **new `data/line-excludes.yaml` globs this run** — `marcelocantos/mnemo` `internal/zstdc/zstd.c`+`zstd.h` (Facebook amalgamation, ~55k lines), `marcelocantos/housekeeping` `snapshots/**` (du TSV + rescued stash patches, including a 212k-line yourworld dump). Headline ☲ is gather `landed:` after those globs. Excluded bulk this week is **+325,995/−673**. Orthograph **+41,249/−448** is a closed-source conversion squash that re-adds the existing product plus subsequent work — an activity signal, not this week's hand-authored delta. jevons +35,843 and finance +4,090 were checked: authored Go/JS/TSX/Python/SQL, no new golden corpus.

### Major Achievements & Innovations

- **React is the daily cockpit; transcripts live in SQLite** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T540/🎯T548) — React on `:13705`, vanilla on `:13706`. InstantTip pockets, frontier play chrome, inspect/composer hermetic `itOracle`s, and a status bar that paints overseer phase so recovery chrome is not a turn. `statedb` persists coalesced transcripts and the fleet tree; mux indexes continue across a statedb suffix so PageUp grows past the first-paint tail rather than renumbering history.
- **An exhausted model falls down its ladder** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T585) — re-briefing a seat whose model is out of quota is how an overseer loops. Fallback is down the seat's own provider ladder; the overseer can change model on that provider. Throwaway compact is not a work seat (🎯T543); reap COLD migrates instead of resurfacing (🎯T542).
- **The anchor pane holds the tmux server open** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T579, [marcelocantos/claudia](https://github.com/marcelocantos/claudia) v0.28.0) — eight fleet-health recoveries on 29 August failed with `tmux new-window: no server running` while the fleet's own panes were alive. The socket was never wrong (`-S` is on every call); the **anchor session that holds the server open had been reaped**. `EnsureServer` recreates it; spawn classifies the error and retries once.
- **mnemo v0.89–v0.90 — compress the hot path, stop paying for a backup you will not restore** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) 🎯T151–🎯T156) — `entries.raw` compressed, hot fields materialised, readers on `entries_v`. Metadata-only migrations no longer take an 18.9 GB snapshot. Default backups retained: 7 → 1 (~81 GB of copies against 18.9 GB of data). Tool surface measured in **bytes**: 36,667 → 24,917 (~9,910 → ~6,734 tokens) by dropping `mnemo_note`/`mnemo_config` and generating the schema catalogue from the live database. File-only config, with a watcher, because removing the write tool would otherwise have silently downgraded hot-reload.
- **arr.ai tuples are interned shapes** ([arr-ai/arrai](https://github.com/arr-ai/arrai) v0.338–v0.339, [arr-ai/hash](https://github.com/arr-ai/hash) v1.2.0, [arr-ai/frozen](https://github.com/arr-ai/frozen) v1.12–v1.13) — a tuple is an interned `Shape` (sorted names, cached hashes, With/Without transitions) plus values in shape order. Same attribute set means same `*Shape`, so Get/With/Equal/Hash are positional. Scopes are lexical frames; `IdentExpr` caches `(hops, slot)`. reconstruct repro 2.98 s → 2.13 s, 2.85 GB → 1.88 GB, output byte-identical. hash128 is a seedless `Hashable` so nested values can cache a result the seeded interface made impossible; AES assembly on amd64/arm64, ported out of frozen.
- **tapper v0.2.0/v0.2.1 — the tap token leaves CI** ([marcelocantos/tapper](https://github.com/marcelocantos/tapper), [canticode/orthograph](https://github.com/canticode/orthograph), [marcelocantos/vellum](https://github.com/marcelocantos/vellum)) — a Homebrew tap publisher with keychain helpers, codesigned `com.marcelocantos.tapper` so ACLs attach to the binary. Orthograph and vellum publish formulae from the dev Mac; release CI only builds the tarball.
- **claudia v0.28.0 — Cursor as a first-class provider** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia) 🎯T49/🎯T50) — `ListCursorModels`, `DisallowTools` on argv (isolated from a variadic Claude Task prompt), thought/plan/prompt-accepted/permission/tool identity on `Event` so jevons does not scrape JSON. ACP start-then-send without holding the start mutex (jevons T541).

### Significant Progress

- **spyder ship front-door** ([marcelocantos/spyder](https://github.com/marcelocantos/spyder) 🎯T133) — `internal/ship` with `SecItem*` keychain (no `/usr/bin/security`), clipboard absorb of ASC/Play/Firebase, live read-only store verify on import, `secret missing` preflight (exit 20), fastlane wrap with child-only env injection, redacted `~/.spyder/ship-audit`. Bottle Developer ID remains 🎯T134. No version tag this week.
- **Hot policy config, bounce only on successive diffs** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T574) — one loader/watch seam; first load seeds baseline so a restart is not a diff; `mcpscope` owner map classified bounce-required, pinned by a doc ratchet.
- **Host load is not a Build-stop** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T566/🎯T573) — remint before spawn; memory grind keys on kernel memory level, swap advisory only; one "overseer is back" per outage; stuck-busy stretches with host load. Daily activation peeled off the bounce ceremony (🎯T553); KeepAlive install uses repo `bin/jevonsd`, not argv0.
- **vellum viewer** ([marcelocantos/vellum](https://github.com/marcelocantos/vellum) v0.15–v0.17) — HTTP MCP on the view daemon, TOC, figure lightbox (Mermaid SVGs as data URLs so `width="100%"` does not collapse), theme cycle, scroll-pane focus so Page Up/Down work without a click. Local ship via `cv release`; GitHub Actions workflows dropped.
- **Orthograph as a Canticode product** ([canticode/orthograph](https://github.com/canticode/orthograph)) — daemon HTTP MCP at `:13720/mcp` with flock instance lock, padlink/presence/recognize/render (PNG/PDF/SVG, iso lattice, paper), iOS Pencil surface, peer-app study with a steal/avoid matrix. Conversion squash; see honesty note.
- **finance — transcripts are the oracle** ([marcelocantos/finance](https://github.com/marcelocantos/finance), initial) — ANZ/NAB/CBA fetchers inside an already-logged-in browser (human does 2FA); PDF → page-tagged JSON; running-balance reconcile; SQLite load; one audit chain per account; double-entry journal. OCR from the PDF's own stencil pixels, not a render. No data, no credentials in the repo.
- **downstream — incremental Markdown events, not HTML** ([marcelocantos/downstream](https://github.com/marcelocantos/downstream), initial) — Rust crate, Enter/Exit/Text/Attr, append-incremental parsing, Html and Term backends, split-equivalence tests.
- **bullseye v0.47.0/v0.48.0 — dotted children are umbrellas** ([marcelocantos/bullseye](https://github.com/marcelocantos/bullseye)) — `child_of`, explicit dotted create, and split add append the child to the parent's `depends_on` so a family cannot retire while children are open. Standing-invariants dirty tree warns instead of failing `make bullseye` (🎯T75).

### Tough Challenges Overcome

- **`/rc connecting` was being read from the transcript** ([marcelocantos/claudia](https://github.com/marcelocantos/claudia), jevons T565) — `MatchConnecting` scanned the whole captured frame, so an overseer whose own prose mentioned `/rc connecting` — diagnosing exactly this wedge — was reported not-ready on an idle composer for every delivery until the words scrolled away. 29 of 33 "ready pattern did not match" failures on 29 August were this frame. The status line lives under the composer's bottom rule; only the last six lines are consulted. Fixtures are the real frames.
- **A local done-word is not a finish** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T581) — send-by-name stays on the addressed PO (🎯T565); closed owner instructions do not re-fire as open intent (🎯T568); a checkpoint is not finished work (🎯T577).
- **Cursor ACP remint deadlocked on the start mutex** ([marcelocantos/jevons](https://github.com/marcelocantos/jevons) 🎯T541, [marcelocantos/claudia](https://github.com/marcelocantos/claudia)) — start-then-send without holding start; stop Cursor ACP on SIGHUP and reap leftovers before Launch; resume the same sessions after bounce, or tell the truth (🎯T545).
- **Group-by keys that silently miss every lookup** ([arr-ai/arrai](https://github.com/arr-ai/arrai)) — a single-column key stored as the bare `Value` would save two allocations per row and miss every lookup: frozen resolves equality for an `any` map key via `Equal(any) bool`, which `Values` has and an arr.ai `Value` does not. `keyOf` keeps a one-element `Values`; `TestGroupByKeyRoundTrip` fails if the encodings diverge.
- **A schema catalogue that truncated the views it was meant to advertise** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) 🎯T157, found while building T156) — `Store.Query` truncates at 100 rows with a bare break; `sqlite_master` is creation order, so a single listing dropped exactly `entries_v` / `messages_v` / `docs_v`. The catalogue paginates on name; every other caller is still exposed.
- **Backup retain=7 was 4.3× the data it protected** ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo)) — at keep=7 the backup directory held ~81 GB against an 18.9 GB database. Restore takes the newest copy; six older ones only cover damage noticed after the next snapshot. Default 1, tests pin both the count and that GC keeps the *newest*.

### Contributors

- Marcelo Cantos (AI co-authors — Claude Opus 5, Claude Fable 5, Grok, Cursor — appear on `Co-authored-by` trailers throughout; jevons, mnemo and arrai landings were largely the supervised fleet).

---

## Agent & Fleet Infrastructure

### [marcelocantos/jevons](https://github.com/marcelocantos/jevons) — React Daily, Statedb, Cursor (77 commits)

**The biggest effort of the week.** 782 file changes, **+35,843/−5,460**, ~214 net new test declarations. React daily, statedb, ladder fallback, anchor pane, hot config, host-load and Cursor remint are above. Also landing:

- **Dead work seat leaves the fleet tree** (🎯T544) — `RemoveDeadSeat` so the T435 chokepoint scan stays green; remaining `SweepDeadAgents` callers updated. `jevons_agent_kill` preserves descendants unless `subtree=true` (🎯T560).
- **Per-seat context ceiling off by default** (🎯T564); context remint stays on the seat's provider when weekly remains (🎯T561). Plan pace coloured from damped burn, not a 5% cutoff (🎯T390.1.6.2). Cursor billing cycle labelled monthly, not weekly (🎯T550).
- **Served-build identity includes the go.work sibling** (🎯T580) so a bounce does not silently run yesterday's claudia.
- **Chat: stop stripping history**; first-paint walks back to real assistant prose; do not replay already-delivered overseer prose (🎯T568/🎯T569). Tab locks on the visible message boxes (🎯T571). Tab stays on main when the sidebar composer is hidden (🎯T549).
- **`make test-ui-react` installs ui deps** instead of skip-and-green (🎯T563). Parallel JSONL parse bench of the daily journal.

### [marcelocantos/claudia](https://github.com/marcelocantos/claudia) — Cursor, Anchor Recovery (9 commits, v0.28.0)

Covered above. Also: drop TeamCreate/TeamDelete deny rules (Claude no longer ships them; denying them printed `matches no known tool` on every launch, and a warnings-only ready timeout used to hand that frame over as the diagnosis). WaitReady names `rc_connecting` / `splash` / `no_composer` / `settings_warning`. **~50 new tests**; +4,537/−162 across 59 files.

### [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) — Compress, Weigh, Watch (23 commits, v0.89.0–v0.90.0)

Compression, backup retain=1, tool-weight, file-only config and zstd vendor are above. Decoding no longer waits for the schema: `codec.decode` splits from `codec.ready`. Startup is a capability graph with supervised background work; boot-time materialisation reports rows visited, not id span. `mnemo_query(describe=true)` is callable on its own (`query` optional; handler enforces "one of"). Config watcher tested: an edit reaches adopt, a half-written file never replaces live config, cancellation stops it. **~108 new tests**; +13,399/−1,114 across 189 files after excluding the zstd amalgamation.

### [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) — Dotted Umbrellas (4 commits, v0.47.0–v0.48.0)

Covered above. **7 new tests**; +704/−68 across 17 files.

---

## Libraries & Infrastructure

### [arr-ai/arrai](https://github.com/arr-ai/arrai) — Interned Shapes, Lexical Frames (13 commits, v0.338.0–v0.339.0)

Shape-backed tuples, lexical-frame scopes, hash memoisation and the group-by `Values` trap are above. Also: IdentPattern arguments bound directly in calls/let/`=>` (no throwaway one-entry Scope); lazy match errors; flat pattern frames; memoised `//grammar.parse` and `//re.compile`; `Relation.Equal` fast path when layouts match; `Relation.Has` 224 µs → 82 µs (12k rows, 500 probes, 8 allocs → 1). Releases are tagged deliberately via `/release` rather than auto-bumped on every merge (the PAT that made every master push a release had expired). **~14 new tests**; +2,452/−446 across 83 files.

### [arr-ai/hash](https://github.com/arr-ai/hash) — hash128 (1 commit, v1.2.0)

Covered above. amd64 32-bit routine places its lane at offset 4 so `Uint32(x)` and `Uint64(x)` no longer share an input block. **8 new tests**; +1,344/−0 across 9 files.

### [arr-ai/frozen](https://github.com/arr-ai/frozen) — Consume hash128 (1 commit, v1.12.0–v1.13.0)

Elements hash through `hash128.Hashable` when they implement it. Also: `Map.With` no longer panics on uncomparable dynamic values. **~10 new tests**; +247/−79 across 20 files.

### [marcelocantos/downstream](https://github.com/marcelocantos/downstream) — Incremental Markdown Events (3 commits, initial)

Covered above. **~25 new tests**; +2,459/−7 across 19 files.

---

## Tooling & Workflow

### [marcelocantos/tapper](https://github.com/marcelocantos/tapper) — Tap Publisher (5 commits, initial, v0.2.0–v0.2.1)

Covered above. Taps may be personal or organisation; keychain is per tap. Release-publish bootstrap fixed so `brew upgrade` runs on the first cut. **8 new tests**; +1,634/−58 across 33 files.

### [marcelocantos/spyder](https://github.com/marcelocantos/spyder) — Ship Front-Door (9 commits)

Covered above. CGO enabled for spyder builds (Security.framework). `ScrubSecrets` hermetic coverage restored. **~34 new tests**; +3,977/−41 across 46 files.

### [marcelocantos/vellum](https://github.com/marcelocantos/vellum) — Viewer Chrome (12 commits, v0.15.0–v0.17.0)

Covered above. Supervisord local daemon config with a Homebrew-grade PATH so `mmdc` works outside a login shell. **~18 new tests**; +3,235/−355 across 66 files.

### [marcelocantos/ytt](https://github.com/marcelocantos/ytt) — Mixed-Ladder Miss Is Not an Outage (5 commits, v0.13.0–v0.14.0)

A mixed ladder failure (Grok unusable, Claude empty, Codex at quota) was leaking `*capacityError` and exiting 255, which stopped the rest of the analyze queue. Only a true all-available-capacity wall should do that. Synopsis Caveat lines distinguish ⚠️ caution from 👎 critique; founder-pitch notes are no longer auto-👎. **~6 new tests**; +480/−53 across 19 files.

### [marcelocantos/finance](https://github.com/marcelocantos/finance) — Statement Oracle (11 commits, initial)

Covered above. Idempotent refresh via `EXISTING` skip sets baked outside the Playwright run-code VM (it has no filesystem). **+4,090/−95** across 52 files. No unit-test count: the oracle is reconcile-against-transcripts.

### [canticode/orthograph](https://github.com/canticode/orthograph) — Canticode Product (4 commits)

Covered above. Companion: [canticode/homebrew-tap](https://github.com/canticode/homebrew-tap) initialised; [canticode/canticode.github.io](https://github.com/canticode/canticode.github.io) landing page. **~375 new tests** in the conversion squash (includes the pre-existing suite); +41,249/−448 across 210 files — see honesty note.

### [marcelocantos/housekeeping](https://github.com/marcelocantos/housekeeping) — Disk Audit (2 commits, initial)

First snapshot of a disk audit that reclaimed **486 GB**. Authored content is the README, findings and a bench; `snapshots/**` (raw `du` TSV and rescued stash patches) excluded from ☲. +85/−0 authored across 3 files.

### [squz/squz.com](https://github.com/squz/squz.com) — Canonical URLs (1 commit)

Canonical HTTPS apex URLs so Google indexes the right pages. +7/−0.

---

## Commercial

No commercial work landed on a default branch this week. In-flight (HMS extract/review lanes; stock-car 3.25 Autodrive HUD) is summarised in [private week 2026-08-30](https://github.com/marcelocantos/progress-reports-private/blob/master/reports/weekly-report-2026-08-30.md).

---

## In-Flight / Work-in-Progress (unmerged — not counted in shipped totals)

- **Health-Management-Systems/hms** — 45 in-flight; detail in the private companion.
- **minicadesmobile/stock-car-racing** — 11 in-flight (3.25 Autodrive HUD, Kangan Institute car, auto-repair notification); detail in the private companion.

---

## Metrics

*All metrics reflect Marcelo Cantos's contributions only, and count **landed** (default-branch) commits within 2026-08-24…30. In-flight branch work is excluded by design.*

### Aggregate

| Metric | Value |
|--------|-------|
| Repositories touched (landed) | **18** |
| Total landed commits | **183** |
| Total lines added (landed, filtered) | +115,801‡ |
| Total lines removed (landed, filtered) | −8,387‡ |
| Net new lines (landed, filtered) | +107,414‡ |
| File changes | 1,622 |
| New files created | ~600 |
| Bulk paths excluded from ☲ | +325,995 / −673 (zstd amalgamation, housekeeping snapshots, lockfiles, standing globs) |
| Releases published | **17** (claudia v0.28.0, mnemo v0.89–v0.90, vellum v0.15–v0.17, ytt v0.13–v0.14, bullseye v0.47–v0.48, tapper v0.2.0–v0.2.1, arrai v0.338–v0.339, frozen v1.12–v1.13, hash v1.2.0) |
| Languages | Go, TypeScript, TSX, JavaScript, Swift, Rust, Python, Ruby, SQL, YAML, Markdown, Shell, CSS |
| Contributors | 1 (Marcelo Cantos) |

‡*☲ excludes `**/vendor/**`, `**/node_modules/**`, and the fleet `data/line-excludes.yaml` globs. New this run: mnemo `internal/zstdc/zstd.{c,h}`, housekeeping `snapshots/**`. Orthograph +41k is a conversion squash of an existing product.*

### Per-Repository Breakdown

| Repo | Commits | Files | Lines added | Lines removed | Net |
|------|---------|-------|-------------|---------------|-----|
| [canticode/orthograph](https://github.com/canticode/orthograph) | 4 | 210 | +41,249 | −448 | +40,801* |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | 77 | 782 | +35,843 | −5,460 | +30,383 |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | 23 | 189 | +13,399 | −1,114 | +12,285 |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | 9 | 59 | +4,537 | −162 | +4,375 |
| [marcelocantos/finance](https://github.com/marcelocantos/finance) | 11 | 52 | +4,090 | −95 | +3,995 |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | 9 | 46 | +3,977 | −41 | +3,936 |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | 12 | 66 | +3,235 | −355 | +2,880 |
| [marcelocantos/downstream](https://github.com/marcelocantos/downstream) | 3 | 19 | +2,459 | −7 | +2,452 |
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | 13 | 83 | +2,452 | −446 | +2,006 |
| [marcelocantos/tapper](https://github.com/marcelocantos/tapper) | 5 | 33 | +1,634 | −58 | +1,576 |
| [arr-ai/hash](https://github.com/arr-ai/hash) | 1 | 9 | +1,344 | −0 | +1,344 |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 4 | 17 | +704 | −68 | +636 |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | 5 | 19 | +480 | −53 | +427 |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | 1 | 20 | +247 | −79 | +168 |
| [marcelocantos/housekeeping](https://github.com/marcelocantos/housekeeping) | 2 | 3 | +85 | −0 | +85 |
| [canticode/canticode.github.io](https://github.com/canticode/canticode.github.io) | 2 | 5 | +41 | −1 | +40 |
| [canticode/homebrew-tap](https://github.com/canticode/homebrew-tap) | 1 | 3 | +18 | −0 | +18 |
| [squz/squz.com](https://github.com/squz/squz.com) | 1 | 7 | +7 | −0 | +7 |

\* *Closed-source conversion squash of the existing Orthograph tree plus work since 22 August.*

### Testing

| Repo | New tests | Notes |
|------|-----------|-------|
| [canticode/orthograph](https://github.com/canticode/orthograph) | ~375 | conversion squash includes the pre-existing suite plus padlink/render/MCP |
| [marcelocantos/jevons](https://github.com/marcelocantos/jevons) | ~214 | React itOracles, statedb mux indexes, Cursor remint, ladder fallback, T579 anchor |
| [marcelocantos/mnemo](https://github.com/marcelocantos/mnemo) | ~108 | compression round-trip, retain=1 GC newest, config watcher, describe-without-query, zstd workers granted |
| [marcelocantos/claudia](https://github.com/marcelocantos/claudia) | ~50 | T579 vanished-server, `/rc connecting` real frames, Cursor Event kinds, DisallowTools argv |
| [marcelocantos/spyder](https://github.com/marcelocantos/spyder) | ~34 | ship envelope, clipboard absorb fixtures, missing preflight, ScrubSecrets |
| [marcelocantos/downstream](https://github.com/marcelocantos/downstream) | ~25 | split-equivalence incremental parse |
| [marcelocantos/vellum](https://github.com/marcelocantos/vellum) | ~18 | viewer chrome, lightbox SVG, theme cycle |
| [arr-ai/arrai](https://github.com/arr-ai/arrai) | ~14 | shape intern, group-by key round-trip, derive() hash cells |
| [arr-ai/frozen](https://github.com/arr-ai/frozen) | ~10 | hash128.Hashable elements |
| [marcelocantos/tapper](https://github.com/marcelocantos/tapper) | 8 | formula fragments, keychain helpers |
| [arr-ai/hash](https://github.com/arr-ai/hash) | 8 | hash128 Mix/Xor, asmdecl halves |
| [marcelocantos/bullseye](https://github.com/marcelocantos/bullseye) | 7 | dotted depends_on umbrellas, dirty-tree warn |
| [marcelocantos/ytt](https://github.com/marcelocantos/ytt) | ~6 | mixed-ladder exit 255, Caveat markers |
| **Total** | **~877** | landed only; orthograph count is inflated by the conversion squash |

### Daily Activity

![Daily active repositories](daily-activity-2026-08-30.svg)

*(Active repositories per day: Mon 08-24 5, Tue 08-25 2, Wed 08-26 5, Thu 08-27 5, Fri 08-28 5, Sat 08-29 8, Sun 08-30 5.)*

---

## Ideas & Innovations

### Weigh the Tool Surface, Do Not Count It ([marcelocantos/mnemo](https://github.com/marcelocantos/mnemo))
Cutting 70 MCP tools to 18 looked like a win and left the expensive problem untouched: eighteen tools serialised to ~9,900 tokens paid by every session, and the distribution was inverted — the five hottest tools were 95% of calls and 36% of the tokens; the eight coldest were 0.8% of calls and another 36%. **Bytes per registration**, not entry count, is the unit. Moving the schema catalogue out of the always-loaded description and generating it from the live database fixed a second bug for free: the hand-written listing still documented `entries.raw` after compression, so an agent following it wrote a query that silently returned empty strings.

### Same Shape Means Same Pointer ([arr-ai/arrai](https://github.com/arr-ai/arrai))
A tuple that stores attribute names next to values hashes and compares those names on every Get/With/Equal. Intern the name-set once as a `Shape` and **identity is a pointer**. Rows already in shape order inflate to tuples without copying; a tuple of the relation's own shape *is* the row. The reconstruct repro dropping a gigabyte of allocations without a single output byte changing is the proof the public API did not move.

### A Seeded Hash Cannot Be Cached Inside a Nested Value ([arr-ai/hash](https://github.com/arr-ai/hash))
`hash.Hash64` takes a seed, so a composite cannot store "its" hash — every caller seeds differently. **hash128 is seedless**: parts combine with Mix or Xor, and a value may cache the result. Frozen now asks `hash128.Hashable` when the element implements it. The amd64 32-bit lane sits at offset 4 so `Uint32(x)` and `Uint64(x)` no longer share an input block — a collision that only exists if you look.

### The Status Bar Is Not the Transcript ([marcelocantos/claudia](https://github.com/marcelocantos/claudia))
Matching `/rc connecting` against the whole tmux frame makes an agent that *talks about* the wedge become the wedge. 29 of 33 ready-timeouts on 29 August were the overseer diagnosing the status line, in prose, on an idle composer. **Consult the last six lines** — under the composer's bottom rule — and keep the real frames as fixtures, one with the mention in the transcript (must be ready) and one with the bar actually connecting (must not).

### First Load Is a Baseline, Not a Diff ([marcelocantos/jevons](https://github.com/marcelocantos/jevons))
A config watcher that treats the first read as a change will bounce the daemon on every start. **Seed the baseline on first load; bounce only on successive diffs.** Classify which keys are bounce-required (`mcpscope` owner map) and pin that set with a doc ratchet, so a new policy file cannot silently become restart-worthy.

### Stencil Pixels, Not a Render ([marcelocantos/finance](https://github.com/marcelocantos/finance))
OCR of a scanned bank statement from a rasterised PDF page fights anti-aliasing and JPEG artefacts that the PDF itself does not contain. The page's own stencil pixels are the ink. Rebuilding the scan from those, then reconciling running balances against the transcript, makes the transcript the oracle and the PDF the evidence — and keeps every number out of git.

---

## Effort Estimate: Traditional vs. AI-Assisted

A wider week than the last: the fleet still dominates, but a language-runtime rewrite, a closed-source product conversion, a tap publisher, a personal-finance oracle and a ship front-door all landed in the same seven days.

### Per-Project Estimates

| Project | Person-days | Why it's hard |
|---------|-------------|---------------|
| jevons React daily + statedb + Cursor remint + ladder fallback | 10-16 | Virtualised chat whose mux indexes must survive a SQLite suffix; Cursor ACP start-then-send without a held mutex; an exhausted model that must not be re-briefed. |
| mnemo compression, retain=1, tool-weight, zstd bind | 8-12 | Materialising hot fields without breaking readers; a backup GC that keeps the newest; cgo against libzstd's single-frame `nbWorkers`. |
| arrai interned shapes + lexical frames + hash128 | 8-12 | Public tuple/scope API unchanged; reconstruct output byte-identical; frozen `any` key equality trap on group-by. |
| claudia T579 / `/rc connecting` / Cursor Event | 3-5 | Real-frame oracles; an anchor session that is the tmux server's reason to exist. |
| spyder ship front-door | 4-6 | Security.framework ACLs on a codesigned binary; clipboard absorb that must not infer IDs from shape. |
| tapper + orthograph tap cutover | 2-3 | Per-tap keychain; formula fragments that must not drift from `orthograph.rb`. |
| vellum viewer chrome | 2-4 | Lightbox SVGs, theme cycle, focus restoration, local `cv release`. |
| finance statement oracle | 4-7 | Playwright-in-logged-in-browser; stencil-pixel OCR; chained per-account audit; double-entry from messy payee strings. |
| orthograph Canticode conversion + pad/MCP | 3-5 | Conversion is mechanical; the new daemon MCP, padlink and peer-app study are not. (The +41k squash is not costed as greenfield.) |
| downstream incremental markdown | 2-3 | Append-incremental events with split-equivalence. |
| ytt mixed-ladder + Caveat markers | 1-1.5 | Exit 255 only on a true all-available-capacity wall. |
| bullseye dotted umbrellas | 1-1.5 | A family cannot retire while children are open. |
| housekeeping disk audit | 0.5-1 | Snapshot discipline, not product. |

### The Diversity Tax

This week spans Go (jevons, claudia, mnemo, spyder, vellum, ytt, finance, tapper, orthograph), TSX/React at cockpit scale, Rust (arrai's consumer hash128, downstream, bullseye), Swift (Orthograph iPad, Vision OCR), C (vendored zstd), Python (finance transcripts), CGO/Security.framework, Homebrew formula generation, SQLite codec/materialisation, and arr.ai's interned-shape runtime. No single engineer holds libzstd's single-frame `nbWorkers`, frozen's `Equal(any)` map-key trap, tmux anchor-session lifetime and Apple Vision stencil OCR at once.

### Actual Human Effort This Week

| Project | Human hours | The human work |
|---------|-------------|----------------|
| Fleet React/Cursor/anchor contract | 5-8 | Deciding React is the daily UI, that compact is not a work seat, that the anchor pane is sacred, and that `/rc connecting` in prose is not the status bar. |
| mnemo retain=1 and tool-weight | 2-4 | Accepting one backup; weighing bytes not count; retiring the zstd-dict comment so abandoned work cannot look scheduled. |
| arrai output-identical rewrite | 2-3 | Requiring reconstruct byte-identity as the gate, not a benchmark improvement. |
| finance 2FA and Drive layout | 4-7 | Logging into three banks; confirming stencil-pixel OCR against real pages; no numbers in git. |
| Canticode / tapper / ship | 3-5 | Closed-source conversion as a product decision; tap token out of Actions; ship secrets in the keychain. |
| Disk audit | 1-2 | 486 GB reclaimed; what to snapshot vs delete. |

### What If It Were One Person?

The expert band sums to roughly 49-77 person-days. A single generalist pays ramp-up on interned-shape runtimes, libzstd's threading contract, Security.framework keychain ACLs, and three banks' statement HTML — four careers. The context-switch tax is the week's real cost: the fleet, the language runtime, the sketch product and the finance oracle do not share a cache.

### Bottom Line

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **~60-95 person-days (~3.0-4.8 months)** |
| Specialist team (traditional) | **~44-70 person-days (~2.2-3.5 person-months)** |
| Actual human effort this week | **~18-30 hours (~2.3-3.8 person-days)** |
| **Multiplier vs. generalist** | **~40-70x** |
| **Multiplier vs. specialist team** | **~25-45x** |

The multiplier peaks on the arr.ai rewrite (the expensive step is keeping the public API and the reconstruct bytes still) and on mnemo's backup/weight work (the expensive step is noticing 81 GB of copies). It runs lowest where a human body is the protocol — bank 2FA, on-device ship verify, disk-audit judgement. The human contribution concentrated on what a tool must refuse to do: that a conversion squash is not this week's authorship, that a first config load is not a diff, that a local done-word is not a finish, and that a transcript mentioning `/rc connecting` is not the status bar.

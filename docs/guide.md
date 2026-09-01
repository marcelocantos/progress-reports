# Guide: Writing Weekly Progress Reports

Instructions for an AI agent generating weekly progress reports for Marcelo Cantos.

## Dual-home series (public + private)

Commercial descriptive detail is **not** written into this public repo.

| Home | Repo | Holds |
|------|------|--------|
| **Public** | `marcelocantos/progress-reports` | Full non-commercial narrative; **`squz/ge` in full**; names + metrics + stubs for commercial work |
| **Private** | `marcelocantos/progress-reports-private` | Full HMS / minicades / non-`ge` Squz narrative, per-repo journeys, commercial achievements |

**Commercial classifier (detail → private):**

- `Health-Management-Systems/*` (HMS / HMS2)
- `minicadesmobile/*` (stock-car-racing, kart-stars, dragster-mayhem, mopar-drag-n-brag, Minicadeskit)
- `squz/*` **except** open-source `squz/ge`

**Public residual for commercial work:** keep org/repo **names** in metrics tables, executive one-liners, and README blurb cells; replace narrative `###` sections, Ideas items, and effort prose with a short stub linking to the matching private week file. Do **not** strip commercial rows from aggregate metrics.

**Each week dual-writes** when any commercial repo has narrative:

1. Public `reports/weekly-report-<end>.md` — full public detail + commercial stubs
2. Private `reports/weekly-report-<end>.md` — commercial extracts only
3. Commercial per-repo pages and achievement rows update under the private repo only

Private repo path: `~/work/github.com/marcelocantos/progress-reports-private`  
Private GitHub: https://github.com/marcelocantos/progress-reports-private

---

## 1. Data Gathering

### 1.1 Determine the reporting period

The report covers a Monday-to-Sunday calendar week. The date range goes in the title. All reports use consistent 7-day Mon-Sun boundaries.

### 1.2 Discover active repositories

Scan all repos under the working directory for commits within the reporting period. The known organisations/owners are:

- `squz/*` — game projects and shared engine code
- `marcelocantos/*` — personal libraries and tools
- `arr-ai/*` — arr.ai ecosystem (frozen, arrai, wbnf, etc.)
- `anz-bank/*` — work-related (decimal, etc.)

For each candidate directory containing a `.git` folder, run:

```sh
git -C <repo> log --oneline --after="<start>" --before="<end+1day>" --all
```

Any repo with commits in range is included. Collect the set of active repos before proceeding.

### 1.3 Per-repo metrics

For each active repo, collect:

| Metric | Command |
|--------|---------|
| Commit count | `git log --oneline --after=... --before=... \| wc -l` |
| Diff stats | `git log --after=... --before=... --stat --format=""` then sum insertions/deletions |
| Files changed | `git log --after=... --before=... --name-only --format="" \| sort -u \| wc -l` |
| New files | `git log --after=... --before=... --diff-filter=A --name-only --format="" \| sort -u \| wc -l` |
| Contributors | `git log --after=... --before=... --format="%aN" \| sort -u` |
| Languages | infer from file extensions in changed files |

Also collect the commit messages and diffs — these are the primary source material for the narrative sections.

### 1.4 Per-repo qualitative understanding

For each repo, read through the commit log (messages + diffs) and build an understanding of:

- **What was done** — features, fixes, refactors, infrastructure
- **Why it matters** — what problem it solves, what it enables
- **What's technically interesting** — novel algorithms, architectural patterns, clever solutions
- **What's hard about it** — domain expertise required, subtle correctness concerns, cross-cutting complexity

Group related commits into themes (e.g. "Rendering", "Networking", "Testing"). These become the bolded sub-topics in the per-repo bullet lists.

### 1.5 Test counts

Where applicable, count new test functions/cases added during the period. Look for test files in diffs and count `TEST_CASE`, `func Test`, `#[test]`, `it(` etc. as appropriate to the language.

---

## 2. Report Structure

The report is a single markdown file named `reports/weekly-report-<YYYY-MM-DD>.md` where the date is the last day of the reporting period.

### Sections in order:

```
# Weekly Progress Report — <YYYY-MM-DD…DD>

## Executive Summary
## <Category>          (repeated per category)
### [org/repo](url)    (repeated per repo within category)
## Metrics
### Aggregate
### Per-Repository Breakdown
### Testing
## Ideas & Innovations
## Effort Estimate: Traditional vs. AI-Assisted
```

---

## 3. Section Details

### 3.1 Executive Summary

A single punchy paragraph followed by two bullet-point subsections.

**Opening paragraph** — include:

- Repo count, bolded (exclude repos where Marcelo's only commits are submodule pointer updates)
- The domains spanned (game dev, library engineering, tooling, etc.)
- Headline items — name the significant efforts with a phrase each, repo names bolded. Drive selection from the scoring rubric below: any work that earned a bullet in Major Achievements, Significant Progress, or Tough Challenges belongs here. Do **not** impose a "3-5 item" quota or pick a dominant "theme" for the week — report what actually happened, including work across multiple unrelated domains.

Tone: confident, specific, no fluff. Lead with scope and impact.

**Key metrics line** — a single pipe-separated line of bolded figures between the opening paragraph and the achievements list:

```
**<N> commits** | **+<N> net lines** | **~<N> person-days traditional equivalent** | **~<N>x multiplier**
```

The traditional equivalent is the solo generalist estimate from the Effort Estimate section. The multiplier is vs. that same generalist baseline.

#### Scoring rubric

Score each piece of substantive work independently on four axes (0–5 each). **No ranking, no quotas, no "theme for the week".** Each axis is evaluated on the work's own merits — not against other work in the same week.

- **Impact** — does it ship, unlock something, or fix a real problem? Released version (highest), user-visible behavior change, or another repo/system now depends on it. Unreleased work caps out lower on this axis.
- **Platform/system depth** — native APIs, kernel primitives, video/audio codecs, GPU pipelines, crypto, OS-specific lifecycle. FFmpeg arm64 static integration or Metal/VideoToolbox work scores high here.
- **Correctness surface** — concurrency, cryptographic equivalence, formal verification, security audit hardening, transactional semantics, multi-session resource lifecycle. The higher the cost of silent wrongness, the higher the score.
- **Scope of change** — files touched × architectural layers crossed. A renderer backend swap touches shader pipelines, resource lifecycle, command recording, every graphics primitive — that's high scope regardless of the word "migration".

**Anti-framing rule**: judge by *what was done*, not by the word used to describe it. Words like "migration", "cleanup", "refactor", "rewrite", or "port" often mask significant architectural work. If a repo's activity reads as low-effort at first glance, re-read the diffs before scoring.

**Anti-bias rule**: polyglot novelty (C crypto, JNI bridges, cross-language test vectors) can *feel* harder than platform-deep mobile/GPU/codec work, but often isn't. Score on concrete axes, not on how exotic the description sounds.

#### Section gates

**Major Achievements & Innovations** (`### Major Achievements & Innovations`) — a bullet list gated on **Impact ≥ 4** (shipped or released this period). No minimum or maximum count; include every item that passes the gate. Each bullet should:

- Start with the key concept or technique in bold
- Name the repo
- Explain concretely *what* was achieved and *why* it's noteworthy in 1-2 sentences
- Quantify impact where possible (performance gains, lines eliminated, etc.)

**Significant Progress** (`### Significant Progress`) — a bullet list for **unreleased** work that scored high on depth, correctness, or scope (any axis ≥ 4). This captures major architectural work that didn't ship a version this week but represents real engineering progress. Released work always goes in Major Achievements regardless of how much it progressed — never double-list. Skip the section entirely if no work qualifies.

**Tough Challenges Overcome** (`### Tough Challenges Overcome`) — a bullet list of problems that scored high on correctness surface or platform/system depth, independent of whether the work shipped. Each bullet should:

- Start with a concise description of the problem in bold
- Name the repo in parentheses
- Explain the root cause and the specific solution in 1-2 sentences
- Focus on problems that required genuine debugging, insight, or domain expertise — not routine implementation work

Follow these subsections with a "Contributors" line.

### 3.2 Category sections

Group repos into categories. Typical categories (use whichever apply, add new ones if needed):

- **Game Projects** — games and interactive applications
- **Libraries & Infrastructure** — reusable libraries, shared code, data structures
- **Tooling** — CLI tools, build systems, dev workflow
- **Strategic Planning & Documentation** — research papers, planning docs, CLAUDE.md files

Separate categories with `---` horizontal rules.

### 3.3 Per-repo entries

Format:

```markdown
### [org/repo](https://github.com/org/repo) — Short Tagline (N commits)
```

The tagline is 1-4 words describing the week's theme for that repo (e.g. "CLI Overhaul", "Bug Fix", "HAMT Simplification"). Include "(N commits)" and optionally "(N commits, initial)" for new repos or "(N commits, 2 people)" for multi-contributor repos.

Below the heading, a one-line contextual intro if needed (especially for new or unfamiliar projects), then bullet points grouped by **bolded theme**:

```markdown
- **Theme**: Detail, detail, detail
- **Theme**: Detail, detail, detail
```

Style for bullets:

- **Dense and specific.** Pack multiple concrete details into each bullet. Mention specific APIs, data structures, algorithms, file counts, test counts. Avoid vague language.
- **Link liberally.** Link to external technologies, libraries, Wikipedia articles for algorithms/standards — anything a reader might want to look up. Use inline markdown links.
- **Use code formatting** for identifiers: function names, types, config keys, CLI flags, file paths.
- **Quantify where possible.** "52 tests with 310 assertions" not "comprehensive tests". "-280 lines" not "simplified". "4x faster" not "much faster".
- **Order by significance** within a repo, most important themes first.

For the biggest effort of the week, lead with a bold callout like **The biggest effort of the week.** before the bullet list.

### 3.4 Metrics — Aggregate

A table with these rows:

| Metric | Value |
|--------|-------|
| Repositories touched | N |
| Total commits | N |
| Total lines added | +N |
| Total lines removed | -N |
| Net new lines | +N |
| File changes | N |
| New files created | N |
| Languages | comma-separated list |
| Contributors | N (names) |

Add footnotes for anything that would distort the numbers (e.g. code extracted from another repo, Unity assets with no exclude glob yet). Line stats from `gather.sh` already **exclude** `**/vendor/**`, `**/node_modules/**`, and globs in **`data/line-excludes.yaml`** — do not hand-add those trees back into ☲. When `gather.sh` emits `landed-excluded: …` (or `exclude-config:`), mention the excluded bulk only as a footnote, never as the headline. Prefer adding a path under `data/line-excludes.yaml` over permanent prose footnotes.

**Keep `data/line-excludes.yaml` current.** On every report run, when you examine a **new repo** or **new bulk paths** in an existing repo (goldens, verdicts, fixtures, amalgamations, generated dumps), add or extend the `org/repo:` globs, re-run `gather.sh`, and ship the YAML change with the report. Do not scatter exclude config into project repos.

### 3.5 Metrics — Per-Repository Breakdown

A table sorted by commit count descending:

| Repo | Commits | Files changed | Lines added | Lines removed | Net |
|------|---------|---------------|-------------|---------------|-----|

Repo names are links. Use `+` prefix for additions, `-` for removals. Append `*` to net values that need footnoting.

### 3.6 Metrics — Testing

A table of repos that added tests, sorted by test count descending:

| Repo | New tests | Notes |
|------|-----------|-------|


Include a **Total** row. Only include repos that added tests.

### 3.7 Daily Activity Chart

An SVG bar chart showing the number of active repositories per day across the reporting period. This visualises how effort is distributed through the week.

**Generation**: Run the companion chart script with the daily data from `gather.sh`:

```sh
~/.claude/skills/progress-report/daily-chart.py \
    --output <report-repo>/reports/daily-activity-<YYYY-MM-DD>.svg \
    <<< "<daily_active_repos output from gather.sh>"
```

The script reads lines of `DOW YYYY-MM-DD COUNT` on stdin (the `# daily_active_repos` section of `gather.sh` output) and produces an SVG bar chart.

**Embedding**: Place the chart in the Metrics section, after Testing:

```markdown
### Daily Activity

![Daily active repositories](daily-activity-<YYYY-MM-DD>.svg)
```

Commit the SVG alongside the report. The date in the filename matches the report date (last day of the period).

### 3.8 Ideas & Innovations

This section highlights the technically interesting ideas from the week — things that go beyond routine implementation. Each entry is:

```markdown
### Descriptive Title ([repo](url))
```

Followed by a paragraph (not bullets) explaining:

1. **The problem or context** — what limitation or challenge existed
2. **The insight** — what's novel about the approach, bolded key phrase
3. **Why it's elegant** — what it enables, what complexity it eliminates

Style: explanatory and appreciative. Write for a technically sophisticated reader. Bold the key technical insight in each paragraph. Use links to algorithms/concepts where appropriate.

Aim for 4-7 entries per report. Skip anything that's just "implemented X using standard approach Y".

### 3.9 Effort Estimate

This section compares the AI-assisted output against traditional development. It has these subsections:

**Per-Project Estimates** — a table:

| Project | Person-days | Why it's hard |

Estimate how many person-days a domain expert would need for each project. The "Why it's hard" column should name specific technical challenges and specialisms, not generic difficulty claims. Be concrete: "geodesic geometry is research-grade 3D math" not "this is complex".

**The Diversity Tax** — a bulleted list of distinct specialisms exercised during the week, followed by commentary on how no single person holds all of them.

**Actual Human Effort This Week** — a table:

| Project | Human hours | The human work |

Estimate actual human hours spent directing, reviewing, testing, deploying. The "human work" column describes what the human actually did (architecture decisions, play-testing, aesthetic judgement, debugging device-specific issues).

**What If It Were One Person?** — a table comparing expert days vs. generalist days with ramp-up costs, plus a context-switching tax.

**Bottom Line** — a summary table:

| | Estimate |
|---|---|
| Single talented generalist (traditional) | **X person-days (Y months)** |
| Specialist team (traditional) | **X person-days (Y person-months)** |
| Actual human effort this week | **~X hours (~Y person-days)** |
| **Multiplier vs. generalist** | **~Nx** |
| **Multiplier vs. specialist team** | **~Nx** |

Followed by a paragraph on where the multiplier is highest and lowest, and what the human contribution concentrates on.

---

## 4. Authorship & Multi-Contributor Handling

The report is a personal progress report for Marcelo Cantos. Other contributors' work should be acknowledged but separated.

### 4.1 Determine authorship per repo

For every active repo, check per-commit authorship:

```sh
git -C <repo> log --after="<start>" --before="<end+1day>" --format="%aN" | sort | uniq -c | sort -rn
```

Collect per-author commit counts, line stats (insertions/deletions), and files changed.

### 4.2 Structure the report by author

- **Main body** (Executive Summary, category sections, per-repo entries): Only Marcelo's personal work, in full detail.
- **"Other Team Work" section** (after the last category section, before Metrics): A condensed summary of non-Marcelo contributions. One paragraph per repo, naming the contributor, summarising what they did, and giving commit count and line stats. No deep bullet-point breakdowns — keep it brief.
- **Executive Summary** (achievements, challenges, contributors): Only Marcelo's work. The "Contributor" line should list only Marcelo.
- **Metrics tables** (Aggregate, Per-Repository, Testing): Only Marcelo's data. Add a note: *"All metrics below reflect Marcelo Cantos's contributions only."* If Marcelo had trivial commits in a team-member's repo (e.g. submodule pointer updates), include them in the per-repo table with a footnote.
- **Effort Estimate**: Only Marcelo's work.
- **Ideas & Innovations**: Only innovations from Marcelo's work.

### 4.3 Edge cases

- If Marcelo's only commits in a repo are submodule pointer updates or other infrastructure plumbing, include the repo in the per-repo metrics table (with a footnote like "†sq submodule pointer updates only") but don't give it a full narrative entry in the category sections.
- If a repo is split roughly evenly, create separate narrative entries for each contributor's work within the category section, clearly labelled.

---

## 5. Follow-Up Reports

When writing a report that follows a previous one:

- **Don't re-explain projects.** If esfera2 was described as "a spherical chess game on a geodesic sphere board" last week, this week just say what's new. The reader has context.
- **Don't repeat the category/section structure explanation.** Just use it.
- **Do note continuation vs. new work.** If a repo appeared last week and continues this week, frame the entry as progress ("continued work on...", "further development of...") or as a specific new phase. If a repo is new this week, give it the full introductory treatment.
- **Do update the effort estimate framing** if the nature of the work shifted (e.g. less greenfield, more polish/debugging).
- **Maintain the same section order and formatting conventions** for consistency across the series.

---

## 6. Updating the Repository

After writing a new report:

1. **Rewrite "The Journey So Far"**: Replace the `## The Journey So Far` section at the top of `README.md` from scratch each iteration. Do not read the existing section before drafting — write a fresh narrative grounded in the current totals, this week's work, the achievements list, and (as needed) the previous reports. The section contextualises the cumulative body of work: total days, commits, languages, traditional equivalent, the nature of the work, the human role, and what stands out. Keep the tone confident, dense, British English, no emojis; feel free to restructure, re-emphasise, or change examples. Successive rewrites may converge on similar observations — that is fine; don't force artificial differences.

   **This is an overview, not a catalogue.** The per-project enumeration — which repos, releases, and features — lives in *Greatest Hits* and the weekly reports. Do **not** reproduce it here. The Journey conveys the *character and significance* of the cumulative body of work: what kind of work it is, what makes it notable, and what the headline numbers mean. Describe qualities — breadth, rigour, compounding tooling, the inverted human role — and name at most one or two projects as illustration. If a paragraph becomes "a X — **foo** — that does Y" three times over, it has slipped into enumeration; pull back to the general statement. A reader should finish with a *sense* of what was achieved, then descend to Greatest Hits and the reports for specifics.

   **Length budget (sub-linear, by series length).** Even as an overview the section may deepen as the body of work grows, but only *sub-linearly*. Let `N` = the number of weekly reports including this one (count `reports/weekly-report-*.md`). Hold it to: **~300 words** at N ≤ 8; **~400** at 9–16; **~500** at 17–28; **~600** at 29–44; **~700** at 45–72; **~800 (hard ceiling)** at 73+. The curve is logarithmic — ~100 words per doubling of the week span — so it keeps decelerating and never runs away. Length is a ceiling, not a target: a tighter overview is always better than a padded one.
2. **Update README.md**: Add a new collapsible entry under `## Reports`, above the existing entries (newest first). Use this template:

   ```html
   <details>
   <summary><a href="<filename>"><b><YYYY-MM-DD…DD></b></a> key achievement, key achievement, ...</summary>

   Full synopsis here: 2-3 sentences naming the key repos (<b>bolded</b>) and headline
   accomplishments. End with commit count, repo count, and traditional equivalent
   in months (e.g. "~5-8 months traditional equivalent").

   </details>
   ```

   **Important**: Use `<b>` tags (not `**`) for bold text inside `<details>` blocks. Markdown formatting does not render inside HTML elements on GitHub.

   Use `MM-DD…MM-DD` when straddling a month, `YYYY-MM-DD…YYYY-MM-DD` when straddling a year.

   **Length budgets (hard caps, not aspirations).** These are absolute and do
   **not** scale with the week's activity — a busy week produces a *denser*
   summary, not a longer one; pick the highest-scoring items and drop the rest.

   - **Summary line** (after the date link): **≤ 30 words.** An achievement-focused
     list of the 3-5 headline items (not a per-repo rundown). This is the
     *collapsed* teaser — keep it scannable; the `<details>` body holds the detail.
   - **Synopsis** (expanded body): **≤ 120 words**, 2-3 sentences, key repos
     <b>bolded</b>. End with commit count, repo count, and traditional equivalent.

   **Do not calibrate length against adjacent entries.** Write each entry to the
   fixed budgets above from a blank page. Earlier entries may have drifted longer;
   matching them is how the drift propagates. The budget is the reference, not the
   previous row.

   **Keep 🎯T-ids and ±line-counts out of the summary and synopsis.** They belong
   in the full weekly report, not the README index. Listing every target id or
   diff stat to prove significance is the main bloat vector — name the achievement,
   not its evidence trail.
3. **Update the metrics table**: Below `## Reports` and its collapsible entries, maintain a `## Metrics` table summarising every report. Add a new row at the **top** of the table body (newest first, matching the report order). The table has these columns:

   | Period | <img src="https://github.githubassets.com/favicons/favicon.svg" width="16"> | Hours | Equiv.&nbsp;(mo) | Gain | Highlights |
   |--------|---|-------|-------------|-------|------------|

   - **Period**: Link to the report file using the period start date only, e.g. `[02-16](reports/weekly-report-2026-02-22.md)`. Use `MM-DD` normally, `YYYY-MM-DD` when straddling a year.
   - **<img src="https://github.githubassets.com/favicons/favicon.svg" width="16">**: Total commits (GitHub favicon represents commits).
   - **Hours**: Actual human hours for the week, e.g. `18-28`. Taken from the Effort Estimate "Actual human effort this week" row (strip the `~` and the trailing `hours` / person-day annotation — keep just the range). In the **Totals** row, sum the low and high bounds across all periods.
   - **Equiv. (mo)**: Traditional generalist equivalent in months, e.g. `5-8` (unit is in the heading). Taken from the Effort Estimate "Single talented generalist" row. In the **Totals** row, convert the summed months to fractional years (one decimal place) with a `y` suffix, e.g. `1.9-3.3y`.
   - **Gain**: The vs. generalist figure, e.g. `25-50x` (approximate — values are ranges).
   - **Highlights**: **≤ 20 words (hard cap).** Pick the 3-5 most impressive items and abbreviate aggressively. Budget against this number, **not** against the `<summary>` line — anchoring it to the summary line lets it inherit any drift there.

   Maintain a **Totals** row at the bottom summing commits, Hours, and Equiv. Leave Gain and Highlights blank in the totals row.

   Then refresh the **At a Glance** bullets at the very top of the README (above "The Journey So Far") so they stay in sync with the updated Totals row. They are the same headline figures, surfaced for scanning — keep it to four bullets and the one-line date span:

   - the week span (`<N> weeks · <first Monday> – <latest Sunday>`) and the commit count, repository count, and language count;
   - total human attention (the Totals **AI** hours range);
   - the single-generalist equivalent in years (the Totals **H** figure) and the multiplier range;
   - net lines of tracked change (from the Totals **☲** added−removed; vendor/node_modules already excluded by gather), with the caveat that remaining counts are still an activity signal inflated by fixtures, prebuilts, and goldens.

   Do not invent new figures here — every number must already appear in the Totals row or the Journey. This block is a scannable mirror, not a new source of truth.

4. **Regenerate the timeline chart**: Run the timeline chart script to update the full-history chart in the README:

   ```sh
   ~/.claude/skills/progress-report/timeline-chart.py \
       --since 2026-01-19 \
       --cache <report-repo>/data/daily-repos.yaml \
       --weekly-dir <report-repo>/reports/ \
       -o <report-repo>/reports/timeline.svg
   ```

   The `--cache` flag reads/writes a YAML file of daily repo counts. Cached days are reused; only dates within the last 2 days are rescanned (to avoid timezone edge cases). The `--weekly-dir` flag also regenerates per-week SVGs from the same data. Commit the updated cache alongside the charts.

   The README embeds this as `![Daily active repositories — full timeline](reports/timeline.svg)` between "The Journey So Far" and "## Reports". The chart is regenerated on every report so it stays current.

5. **Commit and push**: Stage the new report, the daily activity SVG, the updated timeline SVG, and the updated README together in a single commit.

---

## 7. Per-Repo Pages

`docs/repos/` holds one summarised page per repository — the per-repo analogue of
"The Journey So Far". Each page distils that repository's entire arc across the
series, organised by phases and themes rather than week-by-week.
`docs/repos/README.md` is the index, linked from the root README.

### 7.1 Inclusion rule

A repository earns a page once it has **two or more dedicated weekly-report
sections** (`### [org/repo] — …` or `### org/repo — …`) across the series. Repos
below the threshold get a one-line entry under "Minor appearances" in the index
instead. Count sections after folding renames and extractions:

| Aliases (oldest first) | Canonical page |
|------------------------|----------------|
| tern → pigeon | `pigeon.md` |
| mk → cv | `cv.md` |
| dais → jevon → jevons | `jevons.md` |
| targets → bullseye | `bullseye.md` |
| multimaze (2010 original) → multimaze2 | private `multimaze2.md` |
| sq (engine dir in yourworld2) → ge | `ge.md` (public) |
| marcelocantos/orthograph → canticode/orthograph | `orthograph.md` |

Page filename: bare repo name, lower-case (`csp.md`, `ge.md`). Commercial
product pages (`hms`, `multimaze2`, `yourworld2`, minicades titles, …) live only
in `progress-reports-private/docs/repos/`. Extend the alias table when a repo is
renamed.

### 7.2 Page template

```markdown
# org/repo

One or two sentences stating what the project is, present tense, as of the latest
report. If the weekly reports hyperlink the repo, link the H1 name to that GitHub
URL; for repos the reports never hyperlink (private/client), plain text.

## The journey

A summarised narrative of the repo's arc across the series — chronological in
spirit, organised by phases (birth, rewrites, platform expansions, hardening,
shipping), never a week-by-week log. Mention renames and extractions where they
happened. Bold sparingly, for genuinely load-bearing moments.

## Highlights

- **Short label** — one dense sentence. ([2026-03-29](../../reports/weekly-report-2026-03-29.md))

## Standouts

- **Toughest challenge** — …
- **Neatest insight** — …
- **Headline achievement** — …

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | N |
| Commits | ~N |
| Human attention | ~X–Y h |
| Traditional equivalent | ~X–Y months |
| Multiplier | ~X–Y× |

## Weekly reports

[01-25](../../reports/weekly-report-2026-01-25.md), [02-22](../../reports/weekly-report-2026-02-22.md), …
```

- **The journey** scales sub-linearly with material: 1–2 paragraphs for a repo
  with ≤3 weekly sections, 3–4 at 4–9, 5–6 at 10+. Ceilings, not targets.
- **Highlights**: 5–12 bullets (fewer for minor repos), chronological, chosen by
  consequence. Twelve is a hard cap — once at it, a new highlight must displace an
  old one, not extend the list.
- **Standouts**: 3–6 bullets of the material that makes a reader think "that's
  cool" — the toughest challenge overcome, the neatest insight or technique, the
  headline shipping event. Mine the weekly "Tough Challenges Overcome" and
  "Ideas & Innovations" sections. Distinct from Highlights: Highlights is the
  chronological record of consequential landings; Standouts is the wow-reel.
  Skip the section only when a minor repo has no genuine standout — never pad.
- **Metrics**: the same accounting the weekly reports carry, aggregated for this
  repo across the series — weeks active, total commits, actual human attention
  (hours), traditional single-generalist equivalent, and the implied multiplier.
  Sum the per-repo rows of each week's "Per-Project Estimates" and "Actual Human
  Effort This Week" tables; keep ranges as ranges. Where a week's tables don't
  break the repo out, prefix the affected figure with `~` — do not invent a
  share. Every number must trace to report tables; never re-estimate from raw
  git data.
- **Weekly reports**: one compact line of comma-separated links to every report
  with a dedicated section or substantive mention of the repo.
- Cross-link related pages where the story demands it (`[ge](ge.md)` for the
  yourworld2 engine extraction, csp ↔ bricabrac, etc.).
- Every fact must be traceable to the weekly reports or `docs/achievements.md`.
  Copy figures exactly; never re-estimate. Keep the reports' honesty caveats
  (vendor bulk, landed-only counts) when citing affected numbers.

### 7.3 Weekly maintenance

On every report run, after drafting the weekly report:

1. For each repo with a dedicated section in the new report, update its page:
   reshape the journey narrative only where the week genuinely moves the arc (a
   new phase, a shipping event, a reversal) — do not append a weekly log entry;
   add a highlight only if it out-ranks the existing set; refresh a Standouts
   bullet only when the week produces something that displaces one; roll the
   week's per-project estimate rows into the Metrics block (weeks active,
   commits, hours, equivalent, multiplier); append the week's link to the
   Weekly reports line.
2. Create pages for repos that crossed the inclusion threshold this week, and
   move them from "Minor appearances" to a category in the index.
3. Refresh the repo's one-line index description if the project's nature shifted.

### 7.4 Backfill sweep (self-healing)

At the start of the per-repo pass, enumerate qualifying repos across the whole
series (`grep -hoE '^### \[?[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+' reports/*.md`, fold
aliases, apply the threshold) and diff against `docs/repos/*.md`. Any qualifying
repo without a page gets one, written from the full series; any repo below the
threshold missing from "Minor appearances" gets its index line. This makes a
normal run self-healing — including the initial population of `docs/repos/` —
so no separate one-off job ever exists for these pages. Use parallel subagents
for multi-page backfills.

### 7.5 Index

`docs/repos/README.md` groups pages by category (reuse the weekly-report
category instincts: games and engines, libraries and infrastructure, agent and
fleet tooling, client work, meta). One line per repo:

```markdown
- [org/repo](name.md) — one-line description, ≤18 words
```

"Minor appearances" at the bottom lists below-threshold repos as plain
`org/repo — one-liner` entries without pages. Keep the whole index scannable —
no prose beyond the intro sentence and the one-liners.

---

## 8. Tone & Style

- **Confident and direct.** No hedging, no "various improvements were made".
- **Technically precise.** Name algorithms, protocols, data structures, libraries. The reader is technical.
- **Dense.** Every sentence should carry information. No filler paragraphs.
- **Honest about what's hard.** Don't oversell routine work, but don't undersell genuinely difficult work either.
- **Resist the elaboration ratchet.** The anti-undersell rules above (and §3.1's anti-framing rule) all push one way: add detail to prove work mattered. Nothing intrinsic pushes back, so length creeps upward week over week. Counter it deliberately — if a README summary line, synopsis, or Highlights cell is at or over its budget, cut, don't append. Significance is shown by *which* items you pick, not by how many qualifiers you stack on each.
- **British English spelling** (colour, behaviour, minimise, etc.) to match the author's preference.
- **No emojis.**

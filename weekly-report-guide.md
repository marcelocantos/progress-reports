# Guide: Writing Weekly Progress Reports

Instructions for an AI agent generating weekly progress reports for Marcelo Cantos.

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

The report is a single markdown file named `weekly-report-<YYYY-MM-DD>.md` where the date is the last day of the reporting period.

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
- Headline items — name the 3-5 most significant efforts with a phrase each, repo names bolded

Tone: confident, specific, no fluff. Lead with scope and impact.

**Key metrics line** — a single pipe-separated line of bolded figures between the opening paragraph and the achievements list:

```
**<N> commits** | **+<N> net lines** | **~<N> person-days traditional equivalent** | **~<N>x multiplier**
```

The traditional equivalent is the solo generalist estimate from the Effort Estimate section. The multiplier is vs. that same generalist baseline.

**Major Achievements & Innovations** (`### Major Achievements & Innovations`) — a bullet list of 4-7 items highlighting the week's most significant technical accomplishments and novel ideas. Each bullet should:

- Start with the key concept or technique in bold
- Name the repo
- Explain concretely *what* was achieved and *why* it's noteworthy in 1-2 sentences
- Quantify impact where possible (performance gains, lines eliminated, etc.)
- These should be the items a reader remembers after skimming the report

**Tough Challenges Overcome** (`### Tough Challenges Overcome`) — a bullet list of 3-6 items describing the hardest problems encountered and how they were solved. Each bullet should:

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

Add footnotes for anything that would distort the numbers (e.g. code extracted from another repo, vendored dependencies, generated code).

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

### 3.7 Ideas & Innovations

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

### 3.8 Effort Estimate

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

1. **Update README.md**: Add a new collapsible entry under `## Reports`, above the existing entries (newest first). Use this template:

   ```html
   <details>
   <summary><a href="<filename>"><b><YYYY-MM-DD…DD></b></a> key achievement, key achievement, ...</summary>

   Full synopsis here: 2-3 sentences naming the key repos (<b>bolded</b>) and headline
   accomplishments. End with commit count, repo count, and traditional equivalent
   in months (e.g. "~5-8 months traditional equivalent").

   </details>
   ```

   **Important**: Use `<b>` tags (not `**`) for bold text inside `<details>` blocks. Markdown formatting does not render inside HTML elements on GitHub.

   Use `MM-DD…MM-DD` when straddling a month, `YYYY-MM-DD…YYYY-MM-DD` when straddling a year. The summary line after the `—` dash should be an ultra-condensed, achievement-focused list of the week's highlights (not a per-repo rundown). The expanded content holds the full synopsis.
2. **Update the metrics table**: Below `## Reports` and its collapsible entries, maintain a `## Metrics` table summarising every report. Add a new row at the **top** of the table body (newest first, matching the report order). The table has these columns:

   | Period | <img src="https://github.githubassets.com/favicons/favicon.svg" width="16"> | Equiv.&nbsp;(mo) | Gain | Highlights |
   |--------|---|-------------|-------|------------|

   - **Period**: Link to the report file using the period start date only, e.g. `[02-16](weekly-report-2026-02-22.md)`. Use `MM-DD` normally, `YYYY-MM-DD` when straddling a year.
   - **<img src="https://github.githubassets.com/favicons/favicon.svg" width="16">**: Total commits (GitHub favicon represents commits).
   - **Equiv. (mo)**: Traditional generalist equivalent in months, e.g. `5-8` (unit is in the heading). Taken from the Effort Estimate "Single talented generalist" row. In the **Totals** row, convert the summed months to fractional years (one decimal place) with a `y` suffix, e.g. `1.9-3.3y`.
   - **Gain**: The vs. generalist figure, e.g. `25-50x` (approximate — values are ranges).
   - **Highlights**: Ultra-condensed (aim for ~15-20 words). Pick the 3-5 most impressive items and abbreviate aggressively — shorter than the `<summary>` line.

   Maintain a **Totals** row at the bottom summing commits and Equiv. Leave Gain and Highlights blank in the totals row.

3. **Commit and push**: Stage the new report and the updated README together in a single commit.

---

## 7. Tone & Style

- **Confident and direct.** No hedging, no "various improvements were made".
- **Technically precise.** Name algorithms, protocols, data structures, libraries. The reader is technical.
- **Dense.** Every sentence should carry information. No filler paragraphs.
- **Honest about what's hard.** Don't oversell routine work, but don't undersell genuinely difficult work either.
- **British English spelling** (colour, behaviour, minimise, etc.) to match the author's preference.
- **No emojis.**

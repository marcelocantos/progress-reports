# [marcelocantos/homebrew-tap](https://github.com/marcelocantos/homebrew-tap)

The personal Homebrew tap through which the fleet's command-line tools reach the machines that run them. Formulae are updated automatically by [homebrew-releaser](https://github.com/Justintime50/homebrew-releaser) on tag push.

## The journey

The tap was created in February to distribute mk — later renamed [cv](cv.md) — and its first eight commits iterated the formula through five versions, moving from a source-based Go build to pre-built binary distribution with shell-completion installation, and finally to automated formula updates via homebrew-releaser. One bug is characteristic of the class: homebrew-releaser's version detection extracted **"64" from "arm64"** in tarball filenames. mk itself shipped five releases in four days behind that pipeline.

From there the tap became the fleet's delivery endpoint rather than one project's afterthought. [ytt](ytt.md)'s formula landed alongside its open-source v0.1.0. [vellum](vellum.md)'s formula was reshaped twice — first with a launchd service block to fix `PATH`, then, when that proved to cover only `brew services` and not terminal or MCP-client launches, by dropping the service block in favour of an install-time shell wrapper. New projects wired the tap into their release workflows from the start: [crosshair](crosshair.md)'s v0.1.0 workflow builds macOS arm64 and Linux amd64/arm64 binaries on tag push, uploads them to the release, then runs homebrew-releaser to update the tap.

## Highlights

- **Tap created for mk distribution** — five formula versions in eight commits, evolving from source build to pre-built binaries with shell completions and automated updates. ([2026-02-22](../../reports/weekly-report-2026-02-22.md))
- **The "64" from "arm64" bug** — homebrew-releaser's version detection was misreading tarball filenames, and was fixed rather than worked around. ([2026-02-22](../../reports/weekly-report-2026-02-22.md))
- **ytt formula** — added at v0.1.0 in step with the tool's open-source release. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))
- **vellum's service block replaced by a shell wrapper** — the tap carried the `PATH` fix that works for every launch context, not just `brew services`. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **Release workflows target the tap directly** — crosshair's first release builds three platform binaries and updates the tap automatically on tag push. ([2026-05-10](../../reports/weekly-report-2026-05-10.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 3 |
| Commits | ~12 |
| Human attention | ~4–8 h |
| Traditional equivalent | ~0.3–0.5 months |
| Multiplier | ~25–95× |

## Weekly reports

[02-22](../../reports/weekly-report-2026-02-22.md), [04-26](../../reports/weekly-report-2026-04-26.md), [05-03](../../reports/weekly-report-2026-05-03.md), [05-10](../../reports/weekly-report-2026-05-10.md)

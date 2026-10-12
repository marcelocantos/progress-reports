# [marcelocantos/jevons-mobile](https://github.com/marcelocantos/jevons-mobile)

Chrome-free Flutter WebView shell for the [jevons](jevons.md) cockpit. The week ending 2026-10-11's commit is on a local checkout with no git remote, so that commit is not known to be on GitHub.

## The journey

The shell was founded in the week ending 2026-10-04: eight landed commits, a Flutter WebView with no browser chrome, codesign through a wildcard profile without registering a portal App ID, and a deploy onto the Jevons iPad mini and the Pixel Fold.

The week ending 2026-10-11 added one commit, `e27f825`, on the only local checkout, directory `jevons-mobile.pre-merge-backup`. That clone has no remote. `image_picker` serves both the iOS composer channel and Android's WebView file chooser; the page hears `jevons-picked-image`. `pubspec.lock` is excluded from the headline line count. Not a release, and not claimed as pushed.

## Highlights

- **Chrome-free cockpit shell** — Flutter WebView, wildcard codesign without a portal App ID, on the Jevons iPad mini and the Pixel Fold. ([2026-10-04](../../reports/weekly-report-2026-10-04.md))
- **One photo picker, two platforms** — `image_picker` for the iOS composer channel and the Android HTML chooser. The commit is local-only. ([2026-10-11](../../reports/weekly-report-2026-10-11.md))

## Standouts

- **Wildcard, not a portal App ID** — the shell codesigns without registering an App ID, which is what let it onto the devices in the founding week. ([2026-10-04](../../reports/weekly-report-2026-10-04.md))
- **A backup clone is not a release** — the photo-picker commit has no remote. The report names the directory and does not link a commit URL. ([2026-10-11](../../reports/weekly-report-2026-10-11.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 2 |
| Commits | 9 |
| Human attention | not broken out; founding week shared, and this week's hour sits in a shared one-hour row |
| Traditional equivalent | ~1–2 person-days this week; founding week shared (6–10 days with other repos) and not split |
| Multiplier | not broken out |

## Weekly reports

[09-28](../../reports/weekly-report-2026-10-04.md), [10-05](../../reports/weekly-report-2026-10-11.md)

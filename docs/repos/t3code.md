# [marcelocantos/t3code](https://github.com/marcelocantos/t3code)

A fork of T3 Code that adds an external plugin protocol for sidebar panels, composer buttons, plugin surfaces and link handling, and keeps pace with upstream through a written merge process.

## The journey

The fork's first reported week introduced the plugin protocol: sidebar plugins and daemon-hosted panels, composer buttons, plugin surfaces, environment panels and a Settings page for plugins, then links that plugins claim, with glob patterns that also claim file links. Web and mobile clients ask the owning plugin before following a click, and plugin builds are signed with a Developer ID and notarised.

The following week shipped fork releases v0.6.0 and v0.7.0. Panels can replace built-in items and collapse, web surfaces and link cards set their own size, and plugin copy goes through i18n. The fork now merges upstream by a repeatable process with a friction ledger, and CI checks the fork's own footprint rather than all of upstream.

## Highlights

- **External plugin protocol** — sidebar panels, composer buttons, link claims and signed plugin builds. ([2026-11-15](../../reports/weekly-report-2026-11-15.md))
- **Fork releases v0.6.0 and v0.7.0** — panels that replace built-in items and plugin surfaces that size themselves. ([2026-11-22](../../reports/weekly-report-2026-11-22.md))
- **A repeatable upstream merge** — a written process, a friction ledger and a fork-footprint CI check. ([2026-11-22](../../reports/weekly-report-2026-11-22.md))

## Standouts

- **Ask the owner before following a click** — plugins register glob patterns and the web and mobile clients ask the claimant first. ([2026-11-15](../../reports/weekly-report-2026-11-15.md))
- **A fork that merges itself** — merge reviewers start from commands and a known ledger shape. ([2026-11-22](../../reports/weekly-report-2026-11-22.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 2 |
| Commits | 23 |
| Human attention | not broken out beyond the weekly tables |
| Traditional equivalent | ~0.4–0.6 months in the latest week |
| Multiplier | not broken out beyond the weekly tables |

## Weekly reports

[11-09](../../reports/weekly-report-2026-11-15.md), [11-16](../../reports/weekly-report-2026-11-22.md)

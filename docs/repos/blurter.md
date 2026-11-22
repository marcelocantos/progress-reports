# [marcelocantos/blurter](https://github.com/marcelocantos/blurter)

A spool-first notification daemon: applications spool events to disk, and the daemon owns the credential, the delivery policy and the sinks.

## The journey

blurter was created and released as v0.1.0 on the same day in late July. Its design inverted the usual notifier. Applications write an event with a temp-file, `fsync` and `rename`, so a reader never sees a partial event and a power cut cannot lose one, and the daemon records delivery only after a sink confirms. Undeliverable events are parked, not deleted, and the failure taxonomy separates transient conditions that retry with backoff from permanent misconfigurations that must not. The MCP surface spools and reads exactly like the CLI, so an agent is a submitter like any other application and no model sits in the delivery path.

v0.2.0 followed in the week ending 1 November. Independent alert keys no longer overwrite each other's state, the daemon runs under Supervisor, and release archives carry dependency licence notices.

## Highlights

- **Durability inversion** — atomic spool, delivery recorded only on sink confirmation, undeliverable events parked. ([07-26](../../reports/weekly-report-2026-07-26.md))
- **A failure taxonomy that refuses to retry misconfiguration** — the Slack sink parses the response body because `chat.postMessage` answers 200 for logical failures. ([07-26](../../reports/weekly-report-2026-07-26.md))
- **An MCP surface defined by what it refuses** — no model in the delivery path, and four protocol details handled explicitly. ([07-26](../../reports/weekly-report-2026-07-26.md))
- **v0.2.0** — per-key alert state, Supervisor operation and licence notices in release archives. ([11-01](../../reports/weekly-report-2026-11-01.md))

## Standouts

- **Toughest challenge** — keeping an agent-facing MCP server honest: notifications are never answered, tool failures are `isError` results, and the stdio scanner buffer is raised so a pasted log cannot desynchronise the stream.
- **Headline achievement** — created and released on the same day with 39 tests.

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 3 |
| Commits | 10 |
| Human attention | not broken out in report tables |
| Traditional equivalent | not broken out in report tables |
| Multiplier | not broken out in report tables |

## Weekly reports

[07-20](../../reports/weekly-report-2026-07-26.md), [10-26](../../reports/weekly-report-2026-11-01.md), [11-16](../../reports/weekly-report-2026-11-22.md)

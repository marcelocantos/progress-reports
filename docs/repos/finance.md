# marcelocantos/finance

[github.com/marcelocantos/finance](https://github.com/marcelocantos/finance)

## The journey

Personal dual-stream ledger: mid-cycle history load, persistent transfer identification across banks, controlled journal categories, reconcile/migrate/audit with a fixture corpus (ANZ/CBA/NAB).

Landed week ending 2026-09-27 (2 commits; further in-flight). The next week added a first-pass category matcher: case-insensitive substring, `re:` prefix for regex, higher `priority` wins, writing `postings.category_id` aligned to Beancount chart paths.

The week ending 1 Nov added a read-only PocketSmith puller with a signed keychain fetcher, an IG Markets adapter for ledger PDFs and contract notes, and a bank fetch that drives the installed Firefox and waits for a human login.

## Highlights

- Dual-stream mid-cycle + persistent transfer IDs
- Controlled categories for journal postings
- Substring/regex matcher writing `postings.category_id` from Beancount chart paths
- PocketSmith puller, IG Markets adapter, Firefox-driven bank fetch (2026-11-01)

## Metrics

| | |
|--|--|
| Weeks active (landed) | 3 |
| Landed commits (series) | 8 |

## Weekly reports

- [2026-09-21…27](../../reports/weekly-report-2026-09-27.md), [2026-09-28…10-04](../../reports/weekly-report-2026-10-04.md), [2026-10-26…11-01](../../reports/weekly-report-2026-11-01.md)

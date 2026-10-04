# marcelocantos/finance

[github.com/marcelocantos/finance](https://github.com/marcelocantos/finance)

## The journey

Personal dual-stream ledger: mid-cycle history load, persistent transfer identification across banks, controlled journal categories, reconcile/migrate/audit with a fixture corpus (ANZ/CBA/NAB).

Landed week ending 2026-09-27 (2 commits; further in-flight). The next week added a first-pass category matcher: case-insensitive substring, `re:` prefix for regex, higher `priority` wins, writing `postings.category_id` aligned to Beancount chart paths.

## Highlights

- Dual-stream mid-cycle + persistent transfer IDs
- Controlled categories for journal postings
- Substring/regex matcher writing `postings.category_id` from Beancount chart paths

## Metrics

| | |
|--|--|
| Weeks active (landed) | 2 |
| Landed commits (series) | 4 |

## Weekly reports

- [2026-09-21…27](../../reports/weekly-report-2026-09-27.md), [2026-09-28…10-04](../../reports/weekly-report-2026-10-04.md)

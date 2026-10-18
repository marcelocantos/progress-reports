# marcelocantos/sentinel

[github.com/marcelocantos/sentinel](https://github.com/marcelocantos/sentinel)

## The journey

**sen** is a never-ending host-health loop. Each check is a broker-admitted restricted Claudia task in a personal directory (`~/.local/share/sen/`) with an editable MEMORY.md addendum. Bounded Supervisor and health-port probes feed every provider; optional Jevons API + Playwright layers deepen the review; blurter alerts only after two distinct failed observations plus an intervening agent review.

Born week ending 2026-09-27 (27 commits landed). The next week added an AES-256-GCM `secrets.enc` store keyed in login Keychain (the daemon never pops a dialog), 1Password import that never prints the value, and a GoodWe SEMS+ JSON client with a daylight gate and two-observation hysteresis.

The week ending 2026-10-11 replaced batch size snapshots with a per-volume size trie, an stdio root observer, and FSEvents. The observer skips its own writes, after uid 0 and the personal directory had been filling the growth ring. Passwordless observe is pinned to the binary's sha256. The Touch ID prompt is in-process, because `sudo -n` returns before `pam_tid` and never offers the dialog. No tag.

The week ending 2026-10-18 tuned the Jevons probe: owner pause honoured, saturated stalls alerted, stop reasons summarised in the cheap probe, and failed reviews budgeted per actionable incident.

## Highlights

- Broker-admitted restricted Task runs; capacity deferral without fake green
- Jevons probe + Playwright UI smoke; incident hysteresis before Slack
- LaunchAgent install path separate from Jevons
- Keychain-backed `secrets.enc`; SEMS+ JSON with daylight gate and hysteresis
- Per-volume size trie and an stdio root observer that skips its own writes
- In-process Touch ID prompt; `sudo -n` returns before PAM

## Standouts

- Alert hysteresis: two failures + review before blurter (week 2026-09-27)
- The observer's own writes filled the growth ring; those paths are excluded from the trie
- `sudo -n` never reaches `pam_tid`, so the admin right is requested in-process and the passwordless rule is pinned to the binary hash

## Metrics

| | |
|--|--|
| Weeks active (landed) | 4 |
| Landed commits (series) | 58 |
| Human attention | ~3–5 h in the 10-11 week; the 10-18 week sits in a shared 1–2 h row; earlier weeks sit in shared rows and are not broken out |
| Traditional equivalent | ~10–15 person-days across the two weeks with their own rows (4–6 then 6–9); founding week not separated |

## Weekly reports

- [2026-09-21…27](../../reports/weekly-report-2026-09-27.md), [2026-09-28…10-04](../../reports/weekly-report-2026-10-04.md), [2026-10-05…11](../../reports/weekly-report-2026-10-11.md), [2026-10-12…18](../../reports/weekly-report-2026-10-18.md)

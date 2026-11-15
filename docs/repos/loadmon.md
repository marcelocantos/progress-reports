# marcelocantos/loadmon

A menu-bar load monitor for macOS: four meters and a popover graph over days of SQLite samples, with a root helper and a local API for agents. It is a local Swift package with no GitHub remote.

## The journey

loadmon appeared in the week ending 25 October with 18 commits. CPU, network and disk are counter deltas over a five-second step and GPU is a per-second gauge averaged into that step. The popover graph has a logarithmic time axis from 5 seconds to 7 days, and per-process identity is the pid plus the kernel start time. A `loadmond` root helper supplies directory I/O trees and a disk-use tree ranked by bytes stored, and the app stops sampling while the helper is alive.

The following week made the trees faster and lazier: the popover fetches one tree level at a time, the disk census no longer blocks the process list, quiet rows above a heavier one are hidden, and single-directory wrappers collapse. In the week ending 8 November it packaged the macOS release from its checkout and recorded that directory growth must stay readable with the popover closed. Other tools now read from it: sentinel takes disk use from loadmon, and headroom reads its SQLite file.

## Highlights

- **Four meters on a logarithmic 5 s to 7 d axis** — counter deltas for CPU, network and disk, a per-second GPU gauge. ([10-19](../../reports/weekly-report-2026-10-25.md))
- **Process identity as pid plus kernel start time** — scores of `sqrt(cpu²+gpu²+net²)/√3` accumulated over each process tree. ([10-19](../../reports/weekly-report-2026-10-25.md))
- **`loadmond` root helper** — directory I/O trees covering 60% of each level and a disk-use tree ranked by bytes stored. ([10-19](../../reports/weekly-report-2026-10-25.md))
- **Lazy trees** — one level per fetch, hidden quiet rows and collapsed wrappers. ([10-26](../../reports/weekly-report-2026-11-01.md))
- **Release packaging from the checkout** — and a recorded requirement that directory growth stays readable with the popover closed. ([11-02](../../reports/weekly-report-2026-11-08.md))

## Standouts

- **Neatest insight** — rank processes by a combined CPU, GPU and network score accumulated over the whole process tree, so a launcher's children count toward it.
- **Headline achievement** — became the source of truth for load and disk use that sentinel and headroom consume.

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 4 |
| Commits | 80 |
| Human attention | not broken out in report tables |
| Traditional equivalent | not broken out in report tables |
| Multiplier | not broken out in report tables |

## Weekly reports

[10-19](../../reports/weekly-report-2026-10-25.md), [10-26](../../reports/weekly-report-2026-11-01.md), [11-02](../../reports/weekly-report-2026-11-08.md), [11-09](../../reports/weekly-report-2026-11-15.md)

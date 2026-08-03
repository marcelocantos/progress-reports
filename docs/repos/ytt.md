# [marcelocantos/ytt](https://github.com/marcelocantos/ytt)

A YouTube transcript CLI and scheduled ingest pipeline. It extracts transcripts, synopsises them, and walks tracked channels and playlists into a knowledge base, distributed as a Homebrew-installable binary.

## The journey

ytt entered the series in late April as an open-sourcing exercise: the `/open-source` skill applied to a previously-internal tool, producing three releases in a week. v0.1.0 gave `ytt <video-or-playlist-url>` transcript extraction via `youtube-transcript-api` with optional Anthropic-vision frame tagging; v0.2.0 bundled a standalone PyInstaller binary; v0.3.0 fixed what that bundle cost. `--onefile` had been extracting an ~11 MB archive to a tmpdir on *every* invocation, ~4 s per run; `--onedir` ships `dist/ytt/` (binary plus a sibling `_internal/`) and the Homebrew formula moves both into `libexec` with a binary symlink in `bin`, taking hot startup to **~100 ms (~40x)** and cold to ~900 ms. PyPI publishing was dropped for an hCaptcha outage on the trusted-publisher setup, with sdist and wheel kept as release attachments.

The following week the tool became a pipeline. v0.5.0 added `ytt ingest [PLAYLIST_URL]` passing through to a bundled `scripts/playlist-ingest/ingest.sh`, with runtime path resolution that works for both source installs and the frozen brew binary, and `depends_on: [yt-dlp, jq, yq]` so `brew install ytt` is self-sufficient. The post-release work is the more interesting half: an orphan sweep at the top of `ingest.sh` reclaims any per-video directory not in `.processed`, every failure path cleans up and exits cleanly, `pipefail` around `yt-dlp | jq` stops a meta crash silently writing a 0-byte `meta.json`, channel-cursor advance is deferred to post-fan-out and advances only over contiguous landed IDs, and stale cursors are distrusted and walked past under a `CHANNEL_WALK_LIMIT=50` bound. A silently-failing daily cron became **self-healing**, verified by automatically recovering two stranded videos and ingesting 27 further uploads, taking the knowledge-base index from 22 to 49 entries.

Hardening then dominated. June brought `--json` payloads, paced fetching, newest-first ordering and a spend-limit abort; v0.9.0 in July responded to a real run that wedged silently for four-plus days by putting hard `SIGKILL` timeouts on every network and LLM call (transcript 120 s, synopsis 600 s, discovery 120 s) with exit-124 classified transient and retried, a run-level watchdog capping ingest fan-out, bounded waiting (~4 h) for connectivity in DarkWake windows, isolation of a failing channel, validation of 11-character video IDs before any `rm -rf`, and a non-zero exit on an incomplete run.

None of that caught the failure that mattered. In late July v0.10.0 ended a **16-day silent ingest outage**: channel ingest had done nothing since 2026-07-10 across fifteen consecutive scheduled runs, exiting zero every time. An earlier hardening change had pinned the scheduler to the *installed* binary, repointing `$HERE` at a Homebrew Cellar directory that never contains the gitignored `channels.yaml` and is replaced wholesale on every upgrade — **pinning an executable also repins every path derived from that executable's location**. Config resolution was re-anchored (`$YOUTUBE_CHANNELS_FILE` → `$XDG_CONFIG_HOME/ytt/channels.yaml` → the dev checkout) with a missing config promoted to a hard failure whenever cursor state proves channels previously worked. The sharper lesson was that eighteen prior hardening changes all asked "did this step fail?" and none asked "is this pipeline still producing anything?" — so 🎯T11 added an alerting layer and a liveness backstop that fires on a *non-event*: nothing ingested for seven days while channels are tracked is itself a failure.

## Highlights

- **Open-sourced in three releases** — the `/open-source` skill applied to an internal tool produced v0.1.0 through v0.4.0 prep in a single week, 14 commits. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))
- **PyInstaller `--onedir` for ~40x faster startup** — hot startup fell from ~4 s to ~100 ms by ending per-invocation archive extraction, with the Homebrew formula reshaped around `libexec`. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))
- **v0.5.0 `ytt ingest`** — the ingest script became a first-class subcommand resolving correctly under both source and frozen-binary installs, with `yt-dlp`/`jq`/`yq` as tap dependencies. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **Self-healing playlist ingest** — orphan sweep, per-failure cleanup, deferred cursor advance and stale-cursor distrust turned a silently-failing cron into a recovering one, taking the index from 22 to 49 entries with `done: 29 ingested, 0 failed`. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **Ingest hardening for real-world channels** — `--json` payloads, paced fetching, newest-first ordering, a spend-limit abort and full-transcript JSON persistence. ([2026-06-21](../../reports/weekly-report-2026-06-21.md))
- **v0.9.0 timeouts and watchdog** — every network/LLM call gets a hard `SIGKILL` timeout and a run-level watchdog caps fan-out, after a run wedged silently for four-plus days; +1,028/−202 with ~9 new Bats cases. ([2026-07-05](../../reports/weekly-report-2026-07-05.md))
- **v0.10.0 ends a 16-day silent outage** — fifteen scheduled runs had done nothing and exited zero; config resolution was decoupled from the install prefix and a `--dry-run` verified the fix without paying for the 51-video backlog it uncovered. ([2026-07-26](../../reports/weekly-report-2026-07-26.md))
- **Alerting that cannot itself fail loudly** — 🎯T11 reads a webhook from a mode-600 file outside the repo, refuses it if group-readable, dedups by problem digest, emits exactly one `RECOVERED` notice, and never lets notification failure change the run's exit status; 37 new bats cases. ([2026-07-26](../../reports/weekly-report-2026-07-26.md))
- **An inert notification button, fixed at the source** — an `osascript` notification posts on behalf of Script Editor with no click handler and no surviving process, so its **Show** button is inert by construction; `terminal-notifier` posts from its own bundle and makes the click open that run's log. ([2026-07-26](../../reports/weekly-report-2026-07-26.md))

## Standouts

- **A 16-day silent outage caused by pinning a binary** — pinning the scheduler to the installed binary repointed every path derived from its location at a Cellar directory replaced on upgrade; fifteen scheduled runs did nothing and exited zero. ([2026-07-26](../../reports/weekly-report-2026-07-26.md))
- **A liveness backstop that fires on a non-event** — eighteen prior hardening changes all asked "did this step fail?"; 🎯T11 asks whether the pipeline is still producing anything, treating seven days of nothing ingested while channels are tracked as a failure in its own right. ([2026-07-26](../../reports/weekly-report-2026-07-26.md))
- **A notification button that was inert by construction** — an `osascript` notification posts on behalf of Script Editor with no click handler and no surviving process, so its **Show** button could never work; `terminal-notifier` posts from its own bundle and makes the click open that run's log. ([2026-07-26](../../reports/weekly-report-2026-07-26.md))
- **A cron that repaired itself unattended** — orphan sweep, per-failure cleanup and deferred cursor advance recovered two stranded videos and ingested 27 further uploads on their own, taking the knowledge-base index from 22 to 49 entries with `done: 29 ingested, 0 failed`. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **PyInstaller `--onedir` for ~40x faster startup** — `--onefile` had been extracting an ~11 MB archive to a tmpdir on every invocation; shipping `dist/ytt/` into `libexec` with a symlinked binary took hot startup from ~4 s to ~100 ms. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 6 |
| Commits | 34 |
| Human attention | ~7–12 h |
| Traditional equivalent | ~0.6–1.0 months |
| Multiplier | ~25–95× |

## Weekly reports

[04-26](../../reports/weekly-report-2026-04-26.md), [05-03](../../reports/weekly-report-2026-05-03.md), [05-17](../../reports/weekly-report-2026-05-17.md), [05-24](../../reports/weekly-report-2026-05-24.md), [06-21](../../reports/weekly-report-2026-06-21.md), [07-05](../../reports/weekly-report-2026-07-05.md), [07-26](../../reports/weekly-report-2026-07-26.md)

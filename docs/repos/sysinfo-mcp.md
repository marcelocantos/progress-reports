# [marcelocantos/sysinfo-mcp](https://github.com/marcelocantos/sysinfo-mcp)

A pure C MCP server exposing macOS system information — CPU, GPU, memory, disk, OS, network, power and display — through a single `system_info` tool with selective category reporting.

## The journey

sysinfo-mcp went from initial commit to open-sourced and released inside one 19-commit week. The `system_info` tool reports CPU (cores, frequency, load), GPU (Metal cores, memory), memory (physical, used, swap), disk, OS (version, uptime, hostname), network (interfaces, IPs, MACs, primary detection) and power (state, capacity, charge), with a `categories` array parameter so a caller pays only for the metric groups it asks for. The open-sourcing pass in the same week added Apache 2.0 licensing, README, CLAUDE.md, an agents guide, STABILITY.md, `--version`/`--help`/`--help-agent` flags and a GitHub Actions release workflow, ending at v0.2.0. The series restamp later removed +3,532 vendored lines from that week's headline for this repo, so its raw first-week line figure overstates the hand-authored work.

Two smaller passes followed: ccache wired into the build, then **v0.3.0's `display` category**, which reports per-monitor configuration — name, id, main flag, connection type (internal, external, mirrored), pixel and logical resolution, scale, refresh rate, and the refresh range where discrete modes exist — answering a user request to know more about monitor topology than CPU and memory alone. The same release added a PR CI workflow and a bullseye standing-invariants Makefile hook so `/cv` has something to check against.

## Highlights

- **New pure C MCP server, initial to v0.2.0 in one week** — seven metric categories with selective reporting, open-sourced under Apache 2.0 with full agent-facing documentation in the same 19 commits. ([2026-04-12](../../reports/weekly-report-2026-04-12.md))
- **ccache wire-up** — build caching added to a C project whose whole value proposition is being cheap to run. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **v0.3.0 display category** — per-monitor topology including connection type, logical versus pixel resolution, scale and refresh range, plus PR CI and a standing-invariants hook for `/cv`. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 3 |
| Commits | 27 |
| Human attention | ~4–7 h |
| Traditional equivalent | ~0.3–0.6 months |
| Multiplier | ~25–65× |

## Weekly reports

[04-12](../../reports/weekly-report-2026-04-12.md), [04-19](../../reports/weekly-report-2026-04-19.md), [05-03](../../reports/weekly-report-2026-05-03.md)

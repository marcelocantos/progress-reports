# [marcelocantos/claudia](https://github.com/marcelocantos/claudia)

claudia is the Go library for embedding coding agents in other programs — one-shot tasks, persistent sessions and warm pools over Claude Code, with a Grok provider over the [Agent Client Protocol](https://agentclientprotocol.com/) and a Codex seam alongside it. Almost every other tool in the fleet that drives an agent drives it through claudia.

## The journey

claudia went from initial commit to v0.6.0 in a single week in April 2026 — 13 commits, +9,560/-2,677. The defining decision came mid-flight: the original design managed Claude Code through a PTY plus a custom daemon, and PTY lifecycle, signal handling and readiness detection all proved unreliable across macOS versions. The **pivot to tmux-backed agents** replaced the lot, deleting the daemon and its ~1,100-line state machine and adding a `probe-ready-tmux` binary for readiness detection, a warm pool that pre-spawns agents to amortise startup latency, and session chains that track logical work continuity across `/clear` boundaries. A Task mode for one-shot runs shipped in the same stretch.

Consumers arrived immediately and shaped the API from outside. [pageflip](pageflip.md) spawned five persistent specialist sessions in parallel through a `SessionPool`; [mnemo](mnemo.md)'s live compaction pipeline used `claudia.Task` as its LLM caller; [spyder](spyder.md) and mnemo's Windows stories were unblocked by a small v0.7.0 that split advisory `flock` into platform-gated helpers. v0.8.0 and v0.9.0 then exposed `SessionExists` and `SessionJSONLPath` as public probes so external tools — `/waw`, `/cv`, mnemo's compactor — could check session state without re-implementing the discovery walk.

May was **v1.0 readiness**. v0.10.0 clustered the breaking renames (`TaskID`/`TaskName`/`TaskWorkDir`/`TaskStatus` collapsing to `ID`/`Name`/`WorkDir`/`Status`, `RunTask`/`CancelTask`/`StopTask` to `Run`/`Cancel`/`Stop`, `DisallowTools` flipping from a comma-string to `[]string`, `Registry.Start` to `Launch`), clearing the API-design backlog in one go. v0.11.0 followed with the behavioural fixes and a documentation gate: cumulative usage accounting parsed from JSONL, a defined `TermLogPath` contract after silent disable, every exported symbol doc-audited, and runnable examples laid out for pkg.go.dev. The substantive fix in that release was replacing single-subscriber `OnEvent` with `SubscribeEvents`/`UnsubscribeEvents` — under bulk fan-out across a pool, consumers had been displacing each other and events simply vanished, including the library's own internal `WaitForResponse` consumer.

The Grok surface grew next, driven by [jevons](jevons.md)'s push-to-talk voice bridge, which needed three things server-side VAD does not give: `ManualCommit` to stop mid-phrase pauses auto-committing half an utterance, `CommitAndRespond` to request a response explicitly once auto-generation is suppressed, and `OnResponseDone` to know when a full turn has wrapped. `SendSystemNote` (a system-role item, distinct from the now-deprecated assistant-role `InjectAssistantText`) and per-call response modalities landed beside them, and v0.12.0 packaged the push-to-talk controls, system notes and conversation history replay.

July turned claudia into a multi-provider library and then made its session contract honest. v0.14.0 shipped **session rewind** — kill the process, truncate the session JSONL back *n* user turns, let resume replay the surviving prefix — with the subtlety that tool-result entries are excluded from the turn count, so a rewind can never land mid-tool-use and leave an agent waiting on a result that will never come, and a `.rewind-bak` sidecar making the operation itself undoable; a readiness classifier that distinguishes the `--resume` summary menu from an idle prompt unblocked long-lived fleet agents that had been wedging. v0.15→v0.17 then added a **Grok Task provider, a persistent Grok Session provider over ACP** with a hermetic fake ACP server for tests, and registry wiring so `Registry.Launch` honours `AgentDef.Provider` instead of always starting Claude (+5,263/−300, ~58 new test declarations). Finally v0.18 made `session/load` **fail closed** for materialised conversations rather than silently minting a replacement — a provider that "helpfully" recovers by discarding history is a data-loss bug wearing a recovery mask — and v0.19 passed ACP `mcpServers` through, preferring `mcp.claudia.json` so Grok cannot reclassify the servers as repo-local and drop them.

## Highlights

- **Bootstrap to v0.6.0, and the PTY-to-tmux pivot** — tmux-backed agents, a `probe-ready-tmux` readiness binary, warm pools and session chains, with the old daemon and its ~1,100-line state machine deleted. ([2026-04-12](../../reports/weekly-report-2026-04-12.md))
- **Windows advisory flock** — v0.7.0 splits `flock` into platform-gated helpers; small, but it unblocks spyder's and mnemo's Windows stories. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **Public session probes** — `SessionExists` and `SessionJSONLPath` let `/waw`, `/cv` and mnemo's compactor query session state without re-implementing discovery. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))
- **v1.0 API cluster and multi-subscriber events** — one breaking rename release, then behavioural fixes plus pkg.go.dev-ready docs, with `OnEvent` replaced by `SubscribeEvents` after subscriber starvation under bulk fan-out. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **Grok push-to-talk primitives** — `ManualCommit`, `CommitAndRespond` and `OnResponseDone`, built for jevons' voice bridge where server-side VAD was actively wrong. ([2026-05-10](../../reports/weekly-report-2026-05-10.md))
- **System notes and per-call modality** — `SendSystemNote` for out-of-band events the conversation should react to, and text-only versus text+audio selection per call. ([2026-05-17](../../reports/weekly-report-2026-05-17.md))
- **v0.12.0 Grok controls** — push-to-talk, system-note injection and conversation history replay ship together with a STABILITY document. ([2026-05-24](../../reports/weekly-report-2026-05-24.md))
- **Session rewind without landing mid-tool-use** — roll a conversation back *n* user turns, undoable via a `.rewind-bak` sidecar, plus a stale-session resume-menu auto-advance. ([2026-07-05](../../reports/weekly-report-2026-07-05.md))
- **Grok provider, Task then Session over ACP** — provider resolution, headless streaming-JSON mapped to `TaskEvent`, persistent ACP sessions with hermetic fakes, and a registry that stops always starting Claude. ([2026-07-12](../../reports/weekly-report-2026-07-12.md))
- **Fail-closed `session/load` and ACP MCP pass-through** — never silently mint a replacement for a materialised conversation, and prefer `mcp.claudia.json` so Grok's trust gate cannot drop the servers. ([2026-07-19](../../reports/weekly-report-2026-07-19.md))

## Standouts

- **The PTY-to-tmux pivot** — embedding Claude Code through PTY management and a bespoke daemon proved unreliable across macOS versions on lifecycle, signals and readiness detection. Replacing all of it with tmux sessions, a `probe-ready-tmux` readiness binary and a warm pool deleted the daemon and its ~1,100-line state machine outright. ([2026-04-12](../../reports/weekly-report-2026-04-12.md))
- **Event subscribers starving each other under fan-out** — the v0.x `OnEvent` API was single-subscriber, so any consumer displaced the previous one including claudia's own `WaitForResponse`; driving a pool of five or more tasks made events vanish. `SubscribeEvents`/`UnsubscribeEvents` made it multi-subscriber, with the internal waiter using the same path rather than evicting external ones. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **A rewind that cannot land mid-tool-use** — rolling a conversation back *n* user turns hinges on what counts as a turn: tool-result entries are excluded from the count, so a rewind never leaves the agent waiting on a result that will never arrive, and a `.rewind-bak` sidecar makes the whole operation undoable. ([2026-07-05](../../reports/weekly-report-2026-07-05.md))
- **Fail-closed `session/load` as conversation integrity** — a provider that helpfully mints a new session when load fails is a data-loss bug wearing a recovery mask. `RequireResume`/`Materialized` make load fail closed for materialised conversations, and the ACP path prefers `mcp.claudia.json` so a trust gate cannot silently drop the MCP servers. ([2026-07-19](../../reports/weekly-report-2026-07-19.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 11 |
| Commits | ~58 |
| Human attention | ~16–27 h |
| Traditional equivalent | ~1.3–2.1 months |
| Multiplier | ~18–95× |

## Weekly reports

[04-12](../../reports/weekly-report-2026-04-12.md), [04-19](../../reports/weekly-report-2026-04-19.md), [04-26](../../reports/weekly-report-2026-04-26.md), [05-03](../../reports/weekly-report-2026-05-03.md), [05-10](../../reports/weekly-report-2026-05-10.md), [05-17](../../reports/weekly-report-2026-05-17.md), [05-24](../../reports/weekly-report-2026-05-24.md), [06-14](../../reports/weekly-report-2026-06-14.md), [07-05](../../reports/weekly-report-2026-07-05.md), [07-12](../../reports/weekly-report-2026-07-12.md), [07-19](../../reports/weekly-report-2026-07-19.md)

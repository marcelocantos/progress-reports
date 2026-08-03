# [marcelocantos/doit](https://github.com/marcelocantos/doit)

A Go command gatekeeper that sits between Claude Code and the shell: the agent gets `Bash(doit:*)` permission and doit decides what actually runs, escalating through deterministic rules, learned policy and an LLM adjudicator, with every decision recorded in a hash-chained audit log.

## The journey

doit was designed and shipped in its first week as a **three-level capability broker**, resolving the tension between per-command approval (safe, slow) and blanket permission (fast, dangerous). Level 1 evaluates fixed safety rules against the command AST in under a millisecond — hardcoded blocks like `rm -rf /`, config-bypassable rules like `git push --force`. Level 2 consults a human-curated YAML policy store in under ten milliseconds, with per-segment matching, first-match-wins evaluation, pipeline compositionality and spaced-repetition review scheduling. Level 3 invokes `claude -p` for novel cases and issues time-limited single-use approval tokens. The mechanism that makes it improve rather than merely defer is **L3→L2 migration**: consistent LLM decisions are analysed out of the audit log and promoted into deterministic policy, so the system learns from its own gatekeeper. The initial release carried a Unix-socket daemon with binary-framed multiplexed IPC, a pipeline engine with Unicode operators, a hash-chained tamper-evident audit log and 164 test assertions; MCP integration and per-project policy followed the week after, exposing the engine as MCP tools through a dedicated `doit-mcp` binary.

The second phase simplified aggressively. The **opaque-strings security model** stopped parsing pipelines altogether — the shell handles composition, doit treats every command as an opaque string — deleting 503 lines of pipeline parser and the allow-safe-pipeline bypass along with it, while `deny-rm-catastrophic` grew to cover system paths, glob patterns and other users' home directories. L3 briefly moved to tmux-backed [claudia](claudia.md) sessions with a sonnet-fast/opus-deep cascade before reverting to one-shot `claude -p` for simplicity. Next came the time and approval gates: a tier-0 pre-policy **script content-hash gate** requiring explicit elicitation keyed to the SHA-256 of a shell script's contents, so modifications force re-approval; timeout enforcement that SIGKILLs the whole process group on expiry; and **learned per-pattern durations** computed from the audit log as interpolated p50/p95 per `(cap, subcmd)`, flagging anomalies as a *bypassable* deny so an unusually long command pauses for acknowledgement rather than failing outright.

The final arc is governance. Three releases documented a full threat model — tier-0 script gates, tier-1 stable-cap policy, tier-2 ledger-and-elicit, tier-3 elicit-only, the L3 prompt-injection surface, audit-chain integrity invariants — and made every load-bearing knob in it visible through `doit_check_config`. Durations became per project root, since the same command's shape diverges between codebases. `rm` tiering was rebuilt around reversibility rather than a static path list: a git-tracked file is restorable and stays tier-1, an untracked one is destructive and escalates. doit began warning at startup when execution-adjacent sibling MCP servers such as [sawmill](sawmill.md) or [mnemo](mnemo.md) are loaded in the same session, because they are bypass paths. The L3 prompt-injection surface was enumerated, hardened and given a regression corpus. And the audit log grew into a reconstructable chain of evidence — every elicitation with its decision, rationale and time-to-decide, every L2 promotion, the upstream policy decisions that authorised each gated execution, head-and-tail stdout/stderr excerpts on failures, and a `doit_audit_query` tool for filtered postmortems. doit was one of the eight repositories put through the fleet-wide Fable-5 deep audit in July.

## Highlights

- **Three-level capability broker** — L1 deterministic rules (<1 ms), L2 learned YAML policy (<10 ms), L3 LLM gatekeeper (~1–5 s) with approval tokens, behind a daemon with binary-framed IPC and a hash-chained audit log; 164 test assertions. ([03-01](../../reports/weekly-report-2026-03-01.md))
- **L3→L2 policy migration** — consistent LLM decisions are mined from the audit log and promoted to deterministic policy, so LLM invocations fall over time. ([03-01](../../reports/weekly-report-2026-03-01.md))
- **MCP integration** — public `engine` and `mcptools` packages plus a `doit-mcp` binary expose the policy engine as MCP tools, with per-project policy overrides. ([03-08](../../reports/weekly-report-2026-03-08.md))
- **Opaque-strings security model** — pipeline parsing dropped entirely, removing 503 lines of parser and the allow-safe-pipeline bypass; `rm` protection extended to system paths, globs and other users' homes. ([04-12](../../reports/weekly-report-2026-04-12.md))
- **Script content-hash approval gate** — tier-0, pre-policy elicitation keyed to the SHA-256 of script contents, so any edit forces re-approval. ([04-19](../../reports/weekly-report-2026-04-19.md))
- **Learned durations with a bypassable deny** — p50/p95 per `(cap, subcmd)` derived from the audit log; anomalies pause for acknowledgement rather than blocking. ([04-19](../../reports/weekly-report-2026-04-19.md))
- **Threat model and reversibility-based `rm` tiering** — every load-bearing knob surfaced through `doit_check_config`, and `rm` tiered by git-tracked status instead of a static path list. ([04-26](../../reports/weekly-report-2026-04-26.md))
- **Audit chain of evidence** — elicitation outcomes, L2 promotions, upstream authorising decisions and failure-mode output excerpts, queryable via `doit_audit_query`. ([04-26](../../reports/weekly-report-2026-04-26.md))
- **Fable-5 deep audit coverage** — one of eight repositories put through the fleet-wide two-lens adversarial audit that defaults every candidate finding to refuted. ([07-05](../../reports/weekly-report-2026-07-05.md))

## Standouts

- **A gatekeeper that learns from its own decisions** — three levels of escalation (deterministic rules under a millisecond, curated policy under ten, LLM adjudication in seconds) would merely defer the problem, except that consistent L3 decisions are mined out of the audit log and promoted into deterministic L2 policy. LLM invocations fall over time because the system reads its own gatekeeping history. ([2026-03-01](../../reports/weekly-report-2026-03-01.md))
- **Deleting the pipeline parser as a security improvement** — the opaque-strings model stopped parsing pipelines altogether: the shell composes, doit treats each command as an opaque string. That removed 503 lines of parser and the allow-safe-pipeline bypass with it, while `deny-rm-catastrophic` widened to system paths, glob patterns and other users' home directories. ([2026-04-12](../../reports/weekly-report-2026-04-12.md))
- **Learned durations with a deny you can walk through** — expected runtimes are impractical to declare up front, so doit derives interpolated p50/p95 per `(cap, subcmd)` from its own audit log and flags deviations. The twist is that the resulting deny is *bypassable*: an unusually long command pauses for acknowledgement rather than failing a legitimate long run. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **`rm` tiered by reversibility rather than by path** — a static list of protected paths answers the wrong question. A git-tracked file is restorable and stays tier-1; an untracked one is genuinely destructive and escalates, so the same command is dangerous or not depending on what the repository can give back. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))
- **A policy engine that failed open** — the fleet-wide Fable-5 audit, whose two-lens method defaults every candidate finding to refuted until both a reachability lens and an invariant-validity lens confirm it, surfaced a confirmed critical in the one component whose entire purpose is to fail closed. ([2026-07-05](../../reports/weekly-report-2026-07-05.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 5 |
| Commits | 116 |
| Human attention | ~6–11 h |
| Traditional equivalent | ~1.8–3.0 months |
| Multiplier | ~25–65× |

## Weekly reports

[03-01](../../reports/weekly-report-2026-03-01.md), [03-08](../../reports/weekly-report-2026-03-08.md), [04-12](../../reports/weekly-report-2026-04-12.md), [04-19](../../reports/weekly-report-2026-04-19.md), [04-26](../../reports/weekly-report-2026-04-26.md), [07-05](../../reports/weekly-report-2026-07-05.md)

# [marcelocantos/slacker](https://github.com/marcelocantos/slacker)

A Go MCP server that holds several Slack workspaces at once: named accounts, tokens acquired only through a browser OAuth consent and stored in the OS keychain, and twelve tools that all require an explicit account label.

## The journey

slacker was created at the very end of July 2026, in a single commit that already had the shape of a product rather than a prototype — named accounts in YAML, tokens in the OS keychain or mode-0600 files, an account label required on every MCP tool so there is no ambient "current workspace" to get wrong, a CLI for account management and `auth.test`, and Apache-2.0 licensing. The reason for its existence is in that first design decision: Slack's own MCP offering is single-session, and the whole point of slacker is to talk to more than one workspace from one agent.

The following week rebuilt authentication from the ground up. The interactive token prompt, `--token` and `--token-file` were all removed in favour of a **loopback browser OAuth flow**, so nothing secret is ever typed, pasted, or written to config — the token goes from Slack's consent screen to the keychain and is absent from every tool result. Three Slack-specific constraints shaped the implementation, and each was resolved against the primary source rather than assumed. Slack matches `redirect_uri` **byte-for-byte**, so an ephemeral callback port is impossible and the URL had to become configurable. Slack, unlike most OAuth providers, grants **no plain-HTTP exemption for loopback** — its documentation contradicts itself, and the reconciliation is that the *host* `localhost` is acceptable while the *scheme* must still be TLS — so the callback serves a persisted self-signed certificate covering `localhost`, `127.0.0.1` and `::1`. And Slack OAuth v2 requires a `client_secret` with no PKCE support, so the app is owner-provisioned and its credentials live in the keychain, keeping the repository publishable and the binary free of embedded credentials.

Two defects found by reading documentation rather than by a failing test are characteristic. App credentials had lived under a single fixed keychain key, so configuring a second workspace's app silently overwrote the first — fatal precisely for the multi-workspace case the product exists to serve, and made worse by a README that described it as "stores one app at a time". And because a browser consent is a **one-shot human action**, a failure that only surfaces after approval wastes it; `slacker preflight` checks everything verifiable without contacting Slack, and earned its keep on the first live run by finding the default callback port already held by an unrelated MCP server. The default moved to 18765 — below the ephemeral range so an outbound connection cannot transiently steal it — which was free to change then and would have been a breaking change once anyone registered the URL.

The MCP surface then grew to twelve tools so an agent can take an owner from nothing to a working account without them touching a terminal, under one rule: **no secret is ever a tool argument**, because arguments become conversation content that lands in a transcript.

## Highlights

- **Created as a multi-workspace Slack MCP** — named YAML accounts, keychain-backed tokens, a mandatory account label on every tool, Apache-2.0 from the first commit. ([2026-08-02](../../reports/weekly-report-2026-08-02.md))
- **Browser OAuth replaces every paste-a-token path** — tokens acquired only through Slack's consent screen, landing in the keychain, never typed or written to config. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))
- **A TLS loopback callback** — resolved against Slack's primary source, which grants no plain-HTTP loopback exemption; the certificate is generated once and persisted with an 0600 key. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))
- **Per-account app credentials** — a fixed keychain key had made configuring a second workspace destructively overwrite the first. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))
- **`preflight` protects the one-shot consent** — credentials, redirect shape, port bindability, TLS material and config writability checked before a human is asked to approve anything. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))
- **Full configuration surface over MCP** — twelve tools including asynchronous begin/poll login, because MCP clients cap tool-call duration well below a five-minute OAuth window. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))

## Standouts

- **The scope list reads the source** — a test builds the requested-scope set from the API method names *read out of the client source at test time* and checks it against a frozen table transcribed from Slack's reference with a per-method URL. Neither input is owned by the code under test, so the gate cannot be satisfied by editing the answer, and it catches over-broad consent as loudly as a missing scope. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))
- **Secrets are not tool arguments** — an MCP tool argument passes through the model's context and lands in a transcript, so both the client secret and the OAuth token are routed around the model entirely: the secret into a one-shot loopback browser form, the token from browser to keychain. A test walks every tool schema and fails if a secret-shaped argument reappears. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))
- **Documentation that contradicts itself, resolved before it cost a redesign** — the redirect scheme had been flagged in the design as the assumption most likely to force a rewrite, and it was; catching it before the owner's first setup step is the whole value of naming assumptions in advance. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 2 |
| Commits | 20 |
| Human attention | ~4–7 h |
| Traditional equivalent | ~0.2–0.35 months |
| Multiplier | ~30–60× |

## Weekly reports

[07-27](../../reports/weekly-report-2026-08-02.md), [08-03](../../reports/weekly-report-2026-08-09.md)

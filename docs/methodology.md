# Methodology

How the figures in the [Metrics table](../README.md#metrics) are derived.

The figures are not derived from line counts, pull-request counts, or raw commit volume. Each weekly report begins with a per-repository reading of the actual commits — messages and diffs — to build a qualitative picture of what was built, why it matters, and where the difficulty lay.

**Scoring.** Every substantive piece of work is then scored independently on four axes:

- **Impact** — does it ship, unlock something, or fix a real problem?
- **Platform / system depth** — native APIs, kernel primitives, GPU pipelines, crypto, codecs, OS-specific lifecycle.
- **Correctness surface** — concurrency, formal verification, security hardening, transactional semantics; anywhere silent wrongness is costly.
- **Scope of change** — files touched × architectural layers crossed.

Two explicit rules guard against surface-framing bias:

- Words like *migration*, *refactor*, *cleanup* or *port* often mask significant architectural work, so the diffs are re-read whenever a repo reads as low-effort at first glance.
- Polyglot novelty (C crypto, JNI bridges, cross-language vectors) can *feel* harder than platform-deep mobile, GPU or codec work without actually being so; scoring stays on the concrete axes rather than on how exotic the description sounds.

**Traditional-development baselines.** From the per-project assessment, estimates are produced twice:

- A **single talented generalist** who must ramp up on every domain, with ramp-up costs itemised per project.
- An **idealised specialist team** who each know their area but carry coordination overhead.

A context-switching tax is added for multi-domain weeks. A *Diversity Tax* section enumerates every distinct specialism exercised that week — Rust screen-capture via objc2, pure-C QUIC with ngtcp2, TLA+ verification, pymobiledevice3 orchestration, bgfx mobile engine work, WhisperX/pyannote ML pipelines, healthcare PII compliance, and so on — because the breadth itself is load-bearing.

**Actual human hours** are estimated separately per project, with explicit description of what the human did: architecture decisions, design pivots, scope discipline, red-team review, course correction.

**Ranges, not point estimates.** Every figure is a range — estimation uncertainty is reported honestly rather than hidden behind a single number.

**Totals.** The **Equiv.** column is the *single talented generalist* bound from each week's Effort Estimate section; the **Totals** row sums those bounds. Open any report to see the full derivation — per-project person-days with *why it's hard* rationales, the Diversity Tax list, the What-If-It-Were-One-Person ramp-up table, and the human-hours breakdown.

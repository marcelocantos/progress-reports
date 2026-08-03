# [marcelocantos/pageflip](https://github.com/marcelocantos/pageflip)

A Rust and Go meeting-capture pipeline. It captures slides from a screen-shared meeting, redacts faces and PII before anything is written, transcribes and diarises the audio, and feeds the result to parallel [claudia](claudia.md) specialist agents for live analysis.

## The journey

pageflip arrived complete: 53 commits from initial commit to a Homebrew-installable v0.1.0 within days, with all 30 of its bullseye targets achieved. The Rust capture core abstracts a `WindowCapture` behind a macOS ScreenCaptureKit backend, offers an interactive rubber-band region picker built on winit and softbuffer, captures windows by title substring, and deduplicates frames with a 64-bit DCT perceptual hash whose Hamming-distance threshold discards cursor movement, compression noise and mid-animation frames; the interval loop streams saved paths on stdout so a `pageflip-feed` filesystem watcher can drive live analysis.

The privacy architecture is the part worth studying. Frames pass a face-blur redactor (`VNDetectFaceRectanglesRequest` plus a two-pass box blur, degrading to a no-op where no Vision inference context exists) and an OCR PII redactor (`VNRecognizeTextRequest` with `OnceLock`-compiled regexes for email, phone, credit card, government ID and IP address, with multi-word matching via concatenation and offset mapping). What makes those non-optional is the **compile-time egress gate**: `RedactedFrame` is a sealed newtype with private fields whose only constructor is `pub(crate) new_sealed`, reachable only through `RedactPipeline::apply_and_seal`. Every write path demands a `RedactedFrame`, so shipping an unredacted frame is a compile error rather than a runtime assertion — the type system as compliance auditor. The audio side enforces the mirror-image invariant by construction: raw bytes never leave the audio module, `AudioSamples` has private fields, and only a derived `Segment` can exit via the `Transcriber` trait. Transcription runs Whisper large-v3 in batch post-hoc with pyannote `speaker-diarization-3.1` in-memory over the 16 kHz array and no temp files, merging speaker labels into NDJSON output. Above all that, a Go shell spawns five persistent specialist agent sessions in parallel — skeptic, constructive, neutral, dejargoniser and contradictions — injecting slides as they arrive, with an `ArtifactWriter` that produces `decisions.md`, `actions.md`, `open-questions.md` and `contradictions.md` at meeting stop, a cross-artefact slide-reference resolver, a Confluence glossary cache for the dejargoniser, and a contradictions specialist that queries [mnemo](mnemo.md) for cross-meeting conflicts. Roughly 232 tests landed with it.

A later rename clarified the shape for users: the Go orchestrator became the user-facing `pageflip` (it had been `meetcat`) and the Rust capture engine became `pageflip-capture`, spawned as a subprocess implementation detail. The release workflow packages all three binaries — `pageflip`, `pageflip-capture`, `pageflip-feed` — in the darwin-arm64 tarball, and the Homebrew formula installs all three.

## Highlights

- **Capture core with perceptual-hash deduplication** — ScreenCaptureKit capture, a rubber-band region picker, and a 64-bit DCT pHash threshold that discards cursor movement and mid-animation frames. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **Compile-time egress gate** — `RedactedFrame` is obtainable only from `apply_and_seal`, making an unredacted write a compile error rather than a missed runtime check. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **Face-blur and PII OCR redaction** — Vision face rectangles with two-pass box blur, plus regex PII detection over recognised text with opaque overdraw. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **Audio no-egress invariant** — raw samples are structurally unable to leave the audio module; only a derived transcript `Segment` crosses the boundary. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **Five parallel specialist agents and an artefact writer** — skeptic, constructive, neutral, dejargoniser and contradictions sessions producing decisions, actions, open questions and contradictions at meeting stop. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **Rename to a single user-facing binary** — the Go orchestrator became `pageflip` and the Rust engine `pageflip-capture`, with all three binaries packaged and tapped together. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))

## Standouts

- **The type system as compliance auditor** — `RedactedFrame` has private fields, one `pub(crate)` constructor and one caller, so shipping an unredacted frame is a compile error rather than a runtime assertion someone forgot to write on a new save path. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **Raw audio that structurally cannot escape** — `AudioSamples` keeps its bytes private and only a derived transcript `Segment` crosses the module boundary, so the no-recording policy is enforced by construction rather than by discipline. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **A specialist that argues with last month's meeting** — the contradictions agent queries [mnemo](mnemo.md) for cross-meeting conflicts, making the artefact writer's output span sessions rather than summarise one. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))
- **Initial commit to Homebrew-installable in days** — 53 commits delivered a Rust capture core, two Vision-backed redactors, a WhisperX/pyannote diarisation pipeline and a five-agent Go shell, with all 30 bullseye targets achieved and ~232 tests. ([2026-04-19](../../reports/weekly-report-2026-04-19.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 2 |
| Commits | ~55 |
| Human attention | ~3–5 h |
| Traditional equivalent | 0.7–1.0 months |
| Multiplier | ~25–55× |

## Weekly reports

[04-19](../../reports/weekly-report-2026-04-19.md), [05-03](../../reports/weekly-report-2026-05-03.md)

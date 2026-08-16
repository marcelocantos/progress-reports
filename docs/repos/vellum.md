# [marcelocantos/vellum](https://github.com/marcelocantos/vellum)

A Go MCP server and CLI that converts Markdown to styled PDF via goldmark and WeasyPrint (with Prince as an opt-in backend), delivers the result to the macOS pasteboard as RTF, HTML and plain text in one transaction, and imports rich-text documents back to Markdown.

## The journey

vellum was created in mid-April as a new Go MCP server for Markdown-to-PDF conversion, built on [goldmark](https://github.com/yuin/goldmark) and [Prince](https://www.princexml.com/), with KaTeX maths, Mermaid diagrams and GitHub-flavoured CSS. It arrived fully dressed rather than as a prototype — CLAUDE.md, README, STABILITY.md, an agents guide, HANDOVER.md, Apache 2.0 licensing, CI and release workflows and a test suite all landed in the same six commits as v0.1.0. It shares its problem domain with [mpe2pdf](mpe2pdf.md), which gained an MCP mode the same week.

The distinguishing feature came a fortnight later. v0.2.0's `convert_to_clipboard` (🎯T7) puts RTF, HTML and plain text on the macOS pasteboard in **one atomic NSPasteboard transaction** — a single `declareTypes:` / `setData:forType:` pair — with RTF and plain text derived in-process from the assembled HTML via `NSAttributedString`. That required splitting `Render` / `RenderFile` out of the convert pipeline so callers can obtain the HTML page without invoking Prince at all. It replaced a `textutil` + `osascript` pipeline that was single-representation, lossy on round-trip and offered no commit confirmation; NSPasteboard's synchronous API guarantees `Write` returns only after `changeCount` advances. A cgo round-trip test reads each representation back and asserts the RTF carries the `{\rtf` signature and that plain text does not leak RTF source. Linux and Windows backends return `ErrUnsupported`.

Two rounds of delivery mechanics followed. v0.3.0 replaced v0.2.0's launchd-`PATH`-via-service-block fix with an install-time shell wrapper at `bin/vellum` that prepends `HOMEBREW_PREFIX/bin`, `/usr/local/bin` and the usual user tool directories before exec'ing `bin/vellum-bin` — the same problem (node, mmdc and prince must resolve however vellum is launched) solved for terminal invocation, MCP clients with a stripped launchd Aqua context, and `brew services`, where the service block had only ever covered the third. The release workflow gained `CGO_ENABLED=1` on darwin, since the clipboard backend links Cocoa through `objc/foundation` bindings.

The last two releases broadened the surface. v0.4.0 made **WeasyPrint the default** and Prince an opt-in, behind a new `convert.Backend` interface, and expanded `convert.Style` into a 13-field customisation surface (font size, line height, font families, page size and margins, page numbers, running head, bookmarks, hyphenation, BCP-47 lang, PDF/A) resolved per-call over a `config/` package reading `~/.config/vellum/config.yaml` over built-in defaults, with a `--backend` CLI flag, `style`/`backend` options on the MCP tools, relative-path image resolution via `--baseurl`, and a Homebrew formula that `depends_on "weasyprint"` so the open-source path works out of the box. v0.5.0 closed the loop in the other direction with a rich-text importer converting RTF, DOCX, HTML, ODT, EPUB and related formats to Markdown.

## Highlights

- **New Go MCP server, v0.1.0 in six commits** — goldmark plus Prince with KaTeX, Mermaid and GitHub-flavoured CSS, shipped with full project scaffolding and CI. ([2026-04-12](../../reports/weekly-report-2026-04-12.md))
- **Atomic macOS clipboard delivery** — v0.2.0's `convert_to_clipboard` writes RTF, HTML and plain text in one NSPasteboard transaction, replacing a lossy `textutil` + `osascript` pipeline. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))
- **`Render` / `RenderFile` split** — callers can obtain the assembled HTML page without invoking Prince, which is what made in-process RTF derivation possible. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))
- **Shell wrapper supersedes the launchd service block** — v0.3.0 fixes `PATH` for terminal, MCP-client and `brew services` launches alike, where the service block covered only the last. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **v0.4.0 makes WeasyPrint the default** — a `convert.Backend` interface, a 13-field `convert.Style`, a `config/` package and per-call-over-config-over-default precedence, with Prince demoted to an opt-in. ([2026-05-17](../../reports/weekly-report-2026-05-17.md))
- **v0.5.0 rich-text import** — an importer converting RTF/DOCX/HTML/ODT/EPUB and friends to Markdown, with new MCP tools. ([2026-06-14](../../reports/weekly-report-2026-06-14.md))
- **v0.8.0 media-orthogonal `convert`** — four MCP tools collapse into one taking `from`/`to` media (file, content, clipboard, file reference), with legacy sugars expanding into the same router. ([2026-08-02](../../reports/weekly-report-2026-08-02.md))
- **A corpus that cannot verify its own producer** — import fixtures built from implementations with no pandoc lineage, enforced by a provenance test, which found a `.doc` binary being returned as Markdown content on its first run. ([2026-08-09](../../reports/weekly-report-2026-08-09.md))
- **AppKit's HTML importer is a launchd agent** — on macOS 26, `NSAttributedString` HTML init brokers to `com.apple.textkit.nsattributedstringagent`; vellum falls back to pandoc and names the route when that agent is unreachable. ([2026-08-16](../../reports/weekly-report-2026-08-16.md))

## Standouts

- **Three clipboard representations in one atomic transaction** — a single `declareTypes:` / `setData:forType:` pair puts RTF, HTML and plain text on the pasteboard together, with RTF and plain text derived in-process from the assembled HTML, replacing a `textutil` + `osascript` pipeline that was single-representation, lossy and gave no commit confirmation. ([2026-04-26](../../reports/weekly-report-2026-04-26.md))
- **One `PATH` fix for three launch contexts** — v0.3.0's install-time shell wrapper superseded the launchd service block, which had only ever covered `brew services`; terminal invocation and MCP clients with a stripped Aqua context now resolve node, mmdc and prince too. ([2026-05-03](../../reports/weekly-report-2026-05-03.md))
- **The commercial renderer demoted to opt-in** — v0.4.0 put WeasyPrint behind a new `convert.Backend` interface as the default, with a 13-field `convert.Style` and per-call-over-config-over-default precedence, so the open-source path works straight out of `brew install`. ([2026-05-17](../../reports/weekly-report-2026-05-17.md))
- **The importer is another process** — paired sandbox-exec oracles pin the clipboard failure to one mach service (deny TextKit → pandoc; deny WindowServer → still AppKit) and refute "AppKit needs a GUI session". ([2026-08-16](../../reports/weekly-report-2026-08-16.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 9 |
| Commits | ~34 |
| Human attention | ~5–11 h |
| Traditional equivalent | ~0.7–1.1 months |
| Multiplier | ~18–95× |

## Weekly reports

[04-12](../../reports/weekly-report-2026-04-12.md), [04-26](../../reports/weekly-report-2026-04-26.md), [05-03](../../reports/weekly-report-2026-05-03.md), [05-10](../../reports/weekly-report-2026-05-10.md), [05-17](../../reports/weekly-report-2026-05-17.md), [06-14](../../reports/weekly-report-2026-06-14.md), [07-27](../../reports/weekly-report-2026-08-02.md), [08-03](../../reports/weekly-report-2026-08-09.md), [08-10](../../reports/weekly-report-2026-08-16.md)

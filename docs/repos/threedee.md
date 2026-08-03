# [marcelocantos/threedee](https://github.com/marcelocantos/threedee)

A parametric 3D-printing and CAD project: physical parts modelled in Python and exported to printable and machinable formats.

## The journey

threedee's first appearance is a migration. A set of 3D-printable designs moved from [OpenSCAD](https://openscad.org/) to [build123d](https://build123d.readthedocs.io/) — a Python build123d project set up with VS Code OCP integration, then **12 designs ported** (the first three, followed by the remaining nine in a single commit), using [py_gearworks](https://github.com/meadiode/py_gearworks) for proper involute bevel gears in the triton lifter design. The following week added `ocp-vscode` `show()` calls so models render live in VS Code while being edited, closing the authoring loop.

In July the project appeared in the series as a newly tracked repository, landing as a single +1,053-line commit: OpenSCAD `.scad` models generated from Python under `projects/*.py`, with exported `.3mf`, `.stl`, `.step` and `.gcode` for a range of real parts — a baby-gate latch, a cat-flap Raspberry Pi mount, a router-bit rack, Starlock holders — brought under convergence tracking with a Makefile and a `bullseye.yaml`.

## Highlights

- **OpenSCAD to build123d** — a Python-first CAD toolchain with VS Code OCP integration and 12 designs ported. ([2026-04-05](../../reports/weekly-report-2026-04-05.md))
- **Involute bevel gears** — py_gearworks used for correct gear geometry in the triton lifter, rather than approximated profiles. ([2026-04-05](../../reports/weekly-report-2026-04-05.md))
- **Live preview in the editor** — `ocp-vscode` `show()` calls give real-time 3D preview while models are being written. ([2026-04-12](../../reports/weekly-report-2026-04-12.md))
- **Tracked as a convergence project** — the repo entered the series with a Makefile and `bullseye.yaml`, carrying exported `.3mf`/`.stl`/`.step`/`.gcode` for real household and workshop parts. ([2026-07-12](../../reports/weekly-report-2026-07-12.md))

## Metrics

| Metric | Value |
|--------|-------|
| Weeks active | 3 |
| Commits | 10 |
| Human attention | not broken out in report tables |
| Traditional equivalent | ~0.3–0.6 months |
| Multiplier | ~30–65× |

## Weekly reports

[04-05](../../reports/weekly-report-2026-04-05.md), [04-12](../../reports/weekly-report-2026-04-12.md), [07-12](../../reports/weekly-report-2026-07-12.md)

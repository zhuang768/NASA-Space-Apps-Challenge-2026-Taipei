# Presentation production

This directory contains the eight-slide Traditional Chinese speaker notes and the production scripts. The deck integrates fixed research results; the scripts do not fit temperature models, join instruments, recompute intersections, discover sites, or alter research dispositions.

## Inputs and editing

The exact PR heads and copied input hashes are in `../../../outputs/integration/presentation/manifest.json`. PR #7 advanced beyond the initially supplied SHA; the deck uses `8fa07afac4a98096958880f6a5ece16f35abc4db`. All scientific numbers come from these pinned research deliveries. MS-02 PR #6 has `handoff/verified-data-20261114` as its base, not `main`.

- `plot_figures.py`: replot four delivered UV ratios and sensitivity ranges; draw the delivered CTX corner footprints without recomputing coverage. The CTX image patch is unchanged.
- `build.mjs`: editable PowerPoint text, four native tables, scientific images, eight embedded notes pages, and per-slide PNG previews.
- `finalize.mjs`: package, layout, font declaration, native-table and first-party import validation. It intentionally refuses to overwrite a final file or receipt. Move previous task-generated outputs into a private revision folder before rerunning.
- `convert_pdf.mjs`: convert the validated PPTX using LibreOffice and a local fontconfig configuration. The final PDF contains selectable Chinese text.
- `package_metadata.py`: write the figure index, source manifest and validation summary; check the final files and copied inputs.

## Reproduction

Run from the repository root. Dependencies: Python with matplotlib and pypdf; Node with `@oai/artifact-tool`; installed presentation validation tools; LibreOffice; Poppler; Heiti TC font (the production machine has macOS's Heiti TC). Font files are not redistributed. On another platform install an appropriately licensed font and consciously revise the font policy and visual checks.

```sh
python3 docs/integration/presentation/plot_figures.py
node docs/integration/presentation/build.mjs
node docs/integration/presentation/finalize.mjs
node docs/integration/presentation/convert_pdf.mjs
python3 docs/integration/presentation/package_metadata.py
```

Set `ARTIFACT_NODE_MODULES` / `RUNTIME_NODE_MODULES`, `PRESENTATIONS_SKILL_DIR`, `RUNTIME_PYTHON`, and `SOFFICE` to your installed runtime locations as needed. `build.mjs` and `finalize.mjs` include the production runtime paths as defaults. Do not change bundled dependencies. On non-macOS systems supply `FONTCONFIG_FILE` instead of the generated macOS font directories.

Render every PDF page with Poppler, and inspect it together with the Artifact Tool PNGs in `.presentation-build/previews/`. Automated checks cannot replace visual or scientific review. `.presentation-build/` is private working material and is not part of the PR.

## Export fixes actually applied

The initial direct Artifact Tool PDF export failed with `Cannot find module '#standard-fonts/Helvetica'`. The default LibreOffice font discovery also omitted Chinese, and synthesized bold overlapped some Chinese glyphs. The delivered deck uses Heiti TC without synthesized bold; LibreOffice was supplied actual macOS font directories. All eight final PDF pages must be re-rendered and inspected after any typography change. No dependency was patched and no broken PDF is a deliverable.

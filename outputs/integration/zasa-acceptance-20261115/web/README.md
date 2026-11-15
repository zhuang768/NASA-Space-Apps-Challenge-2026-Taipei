# Rebuild / preview
The releasable static files are `index.html`, `style.css`, `app.js`, `mola.jpg`, `deployment.json`. Their exact values are fixed by the asset hash table in `deployment.json`; use a local HTTP server for verification (e.g. `python3 -m http.server 8000` in this folder).
Only these five files belong in the public document root. Source notes, internal records and private evidence are not public assets. R2 additionally restores keyboard focus after chart rendering. See R2-PASS.txt for actual browser checks and SOURCE_PROVENANCE.md for source/license attribution; its four original R1 asset hashes are historical rather than the R2 manifest.

## 2026-11-15 redesign
The four release assets were replaced by the dark editorial redesign (interactive MOLA globe, dot and line charts, unknowns section). Values come from `outputs/research/mars_reselection_20261114/final_candidates.csv`. `deployment.json` and the package `manifest.json` carry the new hashes. `CHECKLIST.txt`, `R2-PASS.txt` and `r4/` describe the earlier release and were not re-run for this one. Deployment to Cloudflare is a separate step.

## 2026-11-15 interactive version
Single-screen layout: clicking a region (marker or list) zooms the globe into it and opens tabs for terrain, heat, ice evidence, dust and unknowns. Sources open in a dialog. Page sections below the fold were removed.

# Rebuild / preview
The releasable static files are `index.html`, `style.css`, `app.js`, `mola.jpg`, `deployment.json`. Their exact values are fixed by the asset hash table in `deployment.json`; use a local HTTP server for verification (e.g. `python3 -m http.server 8000` in this folder).
Only these five files belong in the public document root. Source notes, internal records and private evidence are not public assets. R2 additionally restores keyboard focus after chart rendering. See [the archived browser checks](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/tree/f655d9c6d735f45a43844e5359ebe166e3106551/outputs/integration/zasa-acceptance-20261115/web) and SOURCE_PROVENANCE.md for source/license attribution; the original R1 asset hashes are historical.

## 2026-11-15 redesign
The four release assets were replaced by the dark editorial redesign (interactive MOLA globe, dot and line charts, unknowns section). Values come from `outputs/research/mars_reselection_20261114/final_candidates.csv`. `deployment.json` and the package `manifest.json` carry the new hashes. The archived browser checks and `r4/` describe earlier releases. Deployment to Cloudflare is a separate step.

## 2026-11-15 interactive version
Single-screen layout: clicking a region (marker or list) zooms the globe into it and opens tabs for terrain, heat, ice evidence, dust and unknowns. Sources open in a dialog. Page sections below the fold were removed.

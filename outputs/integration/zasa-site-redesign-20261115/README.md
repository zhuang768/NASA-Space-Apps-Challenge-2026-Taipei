# Site redesign draft (not deployed)

Static replacement for the Cloudflare Worker page. Files: `index.html`, `style.css`, `app.js`, `mola.jpg` (same MOLA map as the current site, NASA MGS/MOLA Science Team).

- Values in `app.js` come from `outputs/research/mars_reselection_20261114/final_candidates.csv` (native-cell means and review-area statistics).
- Geologic units (mAl for MS-01/MS-02, AHv for MS-03) come from the MS-02 local validation and MS-03 `geology_query.json`.
- Preview: `python3 -m http.server` in this folder. Fonts load from Google Fonts; system fonts are used if blocked.
- Deployment is not done here. The current site's source is `outputs/integration/zasa-acceptance-20261115/web/`; swap the asset directory only after review.

# Explorer evidence and usability refinement, 2026-11-15

The current UI uses source snapshot `25b0744ac3d2230803505e1679109c2c35b6204d`. Per-tab source links and scale notes, aligned comparison rows, progressive Earth-chart disclosure and responsive controls were added. Numeric source arrays and research files are unchanged. See `outputs/integration/site_polish_20261115/` for the local review record; historical handoffs below are retained.

---

# Current evidence-label correction, 2026-11-15

The current explorer keeps the same regional numerical values and source snapshots. Labels now use signed SWIM consistency, model-time-adjusted surface temperature and reconstructed dust percentiles. MS-03 fixed-window morphology remains unknown. The challenge/evidence ledger is linked from the overview.

Current code streams public NASA Trek terrain tiles at runtime and loads Google Fonts. The no-runtime-request statement and four hashes in the older handoff below describe that earlier payload only. Current asset fingerprints are in `deployment.json`; they identify files, not proof of a successful public deployment. Historical production notes are unchanged.

---

# TerraMatch static demo handoff

Public payload is exactly `web/index.html`, `web/style.css`, `web/app.js`, `web/mola.jpg`. Nothing contacts a server at runtime except explicit public source links. Do not upload the evidence snapshots, original image, or this handoff with the public assets without separate review. There are no secrets or private-output links in the four-file payload. The old production site was not modified.

## Inputs and provenance

- The site’s MOLA slope, TES thermal inertia and SWIM 0–1 m values are the native-cell means in `source-final-candidates.csv`, SHA-256 `83a03d1f4273fa7c45c0d22b5c29a8b8cfc0544e481d5f2bbca2c85812534c4e`. The input originates at `outputs/research/mars_reselection_20261114/final_candidates.csv`, main commit `1506ede572435588eb5e64f95f24639279b77e56`, Git blob `2371ade1c27087efaa165acb98b7541266eaa606`.
- Conditional depth values are from `source-model.csv`, SHA-256 `639e447ed2f074a162f73a2b804c198b7b2142945bb7530f7b3c253c780295fa`, the reproducibility supplement at draft PR #27 commit `3186fca5f968322a7bdaaed83c41d870a1d68c6f`, cross-site/model_source.csv. Its rows document original public model DOI, cell indexes, assumptions and missing uncertainty. This is a snapshot of re-indexed published output, not new validation.
- The MOLA cylindrical map is from https://marsoweb.nas.nasa.gov/globalData/images/fullscale/MOLA_cylin.jpg, NASA MGS/MOLA Science Team, linked from https://marsoweb.nas.nasa.gov/globalData/datamaps.html. Original SHA-256 `4be7f4347aca2d7273c123786744b02476c9a64ac89e6b76d7c1ba5978e6311b`. It was resized to 1800×900 with Pillow and JPEG quality 85; payload SHA-256 `72a590d14106909381ab65f86b4cc0e455670a6467431a441a84216d92e9e3bb`. Global equirectangular map, north up, longitude 0–360 E; marker positions computed from lon/360 and (90−lat)/180.

## Validation

Independent formula check confirmed marker coordinates against source CSV for all three. This source note does not attest to browser behavior in later releases.

Four deployment payload hashes:

```
66b07662549607a3093976b1513e38e8d8315f7ff75a6b58efb7c2f0c435e576  index.html
00f1407f47d9663c4664e4aafb742f2096b3cfa8e045c42abe0e8646e0dfb33f  app.js
7fb75254011e2d2ba848118fcc7bb3b4219cb969a6d5ba66dd506c2cbc52f9c5  style.css
72a590d14106909381ab65f86b4cc0e455670a6467431a441a84216d92e9e3bb  mola.jpg
```

## Deployment

Do not restore retired web workflow or activate a second deployment writer. Production operator should first verify current Cloudflare Worker and deployment configuration, stage these four files as the asset directory for that exact existing Worker, supply a separate deployment fingerprint identifying actual artifact and source snapshots, preview and smoke test, then deploy through the existing authorized route. Verify signed-out root, each asset, interactions, and fingerprint after release. A site update does not submit the NASA entry. This package does not modify Cloudflare settings or credentials.

# MS-01 CTX EDR product metadata (data notes only)

Source: ODE Mars Product Search web UI (Find by Location 56.5–57.0°N, 72.5–73.0°E; CTX EDR count 4), Meta Data tab of each product, read 2026-11-15.
File: `ctx_product_metadata.csv` (built by `ctx_product_metadata.py`). Product IDs match `ctx_nominal_intersections.geojson` (4/4).

| Product | Obs. (UTC) | Lat range | Lon range (°E) | m/px | Incidence | Ls |
|---|---|---|---|---|---|---|
| G23_027348_2388_XN_58N287W | 2012-05-27 | 55.96–61.17 | 71.63–74.05 | 6.09 | 48.4° | 116.3 |
| F02_036407_2378_XN_57N287W | 2014-05-03 | 54.73–60.34 | 71.08–73.33 | 6.07 | 51.2° | 125.2 |
| F23_044728_2356_XN_55N286W | 2016-02-10 | 53.08–57.55 | 72.54–73.94 | 6.02 | 44.8° | 107.3 |
| V17_086795_2355_XN_55N286W | 2025-01-31 | 52.63–57.85 | 72.40–74.45 | 6.08 | 50.8° | 37.8 |

Limits
- Bounding-box overlap only (strips are slanted); true pixel coverage of the 0.5°×0.5° box not computed.
- EDR is unprojected; registration needs ISIS/SPICE (not available here). Browse thumbnails are not data products.
- No morphology, material, cover or ice classification is made from these records.
- All four are ~6 m/px and incidence 45–51°; no HiRISE (count 0).

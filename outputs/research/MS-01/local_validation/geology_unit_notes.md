# MS-01 geologic unit (data notes only)

Result: unit **mAl** (Middle Amazonian lowland unit) at the MS-01 centre, over the whole 0.5°×0.5° box, and across the ±2° neighbourhood (SIM 3292, 1:20,000,000). Table: `geology_unit.csv`.

Limits
- Source is the ArcGIS feature-service copy of SIM 3292 (same layer MS-03 used), not the pubs.usgs.gov ZIP (shell cannot reach it). Not independently checked against the ZIP shapefile.
- Query responses were read through a fetch tool that summarises output; attributes only, OBJECTIDs and polygon geometry not retained.
- Map scale 1:20M: gives the regional map unit, not local material, cover or morphology.
- MS-02's unit at its cell is also mAl; the two sites share a map unit at this scale.

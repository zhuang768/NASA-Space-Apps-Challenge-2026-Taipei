# MS-03 T1811: production provenance boundary

Read-only investigation, 2026-11-14. Did not rerun the already established CAT-formula/second-stage argument; no residual or scientific candidate score recalculated.

## New verified evidence

| Evidence | Observation | Consequence |
|---|---|---|
| Actual T1811 AL/SU/DE detached labels, official MC03 archive | Product version 4; creation 2023-07-18T18:12:54; producer `crism_mapping_execute_flow`, software version **1.03.94** | Concrete production executable/version target, not a generic CAT version |
| Matching PDS4 XML labels | Preserve program version 1.03.94 and creation time; label version 1.0 denotes PDS4 conversion | Do not confuse PDS4 label version 1.0 with MRDR product v4 or processor 1.03.94 |
| AL/SU PDS3 label lines 57–62 | Photometric ON, atmospheric ON, ratio-shift ON, empirical geometry normalization OFF, empirical smile ON, sensor-space transform ON, all inside PDS comments | Documentary flag declarations, not a complete machine-readable run configuration or parameter log |
| Actual ENVI headers | AL 72 bands, SU 60 bands, 1091 samples × 1636 lines; equirectangular projection | Current tile is not the polar-stereographic case covered by CAT's published warning |
| Official `CAT_v7_4_codeonly.zip`, downloaded and hashed | Actual `.pro` source files present, including `atp_tile.pro`; configuration includes default volcano scan 61C4 | This is source code, but it is public CAT utility source, not demonstrated T1811 production source |
| Entire CAT ZIP filename/content search | No `crism_mapping_execute_flow` match in filename or content | This inspected release does not supply the named production driver; not proof it is nowhere public |
| Exact producer/version web search | Returned SIS documentation and examples, no verified executable release | Documentation must not be called source code |

Primary files are archived beside this note; `label_receipts.json` has exact URLs and SHA-256 for all nine retrieved labels/headers; `cat_archive_manifest.json` has complete ZIP inventory and SHA-256. `production_linkage_check.json` records the bounded negative source search. `atp_tile.pro` and `crismcat_unix_default.cfg` are actual extracted source/config, not a reconstructed algorithm.

Primary entry points:
- https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/mrdr/mc03/
- https://pds-geosciences.wustl.edu/missions/mro/CAT_v7_4_codeonly.zip
- https://pds-geosciences.wustl.edu/missions/mro/CAT74_release.txt
- https://pds-geosciences.wustl.edu/missions/mro/crism.htm

## Exact next evidence needed

1. **Executable/source identity:** `crism_mapping_execute_flow` **1.03.94**, its called spectral/summary processing modules, checksums or immutable revision, and runtime/library versions. Public CAT 7.4 cannot substitute without an explicit equivalence/linkage test.
2. **T1811 run recipe:** configuration and invocation associated with the 2023-07-18 product, not merely default CAT settings; concrete choices and coefficients for atmospheric/photometric/ratio-shift, smile, sensor-space transforms, spectral cleaning, and summary refinement; order of operations, masks, bad-band conventions, interpolation/edge treatment and numeric precision.
3. **Input identity:** source observation/strip list and spatial selection/overlap order; matched calibrated source products, calibration/atmospheric reference identities and versions; the AL-linked `T1811_MRRWV_60N243_0327_4.TAB` (named by actual label), masks, geometry/provenance records. DE may offer source-pixel traceability but was not decoded in this bounded task.
4. **Matched intermediates:** numerical arrays immediately before/after each relevant spectral correction and before/after summary refinement for identical pixels/bands, with checksums. Include pre-map or post-map stage identity so differences are not silently attributed across transformations.
5. **Reproduction test:** show processor 1.03.94 recreates delivered AL/SU values within documented tolerance; only then isolate one stage with controlled comparison to assign its numerical contribution.

## Decision

The archive establishes the producer name and exact version, and exposes coarse documented flags. It does **not** yet supply an executable-linked T1811 run recipe or matched intermediate arrays. A numerical residual may be reported only as an observed mismatch between precisely identified operands already computed elsewhere, not causally assigned to the production spectral stage. No new numerical residual is defensible from this task. Status: provenance narrowed; stage attribution remains blocked. No remote writes, outreach, official-report edits, software installation, or code execution occurred; code was read only.

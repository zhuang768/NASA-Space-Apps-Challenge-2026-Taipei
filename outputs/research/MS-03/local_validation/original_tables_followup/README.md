# Original-table acquisition follow-up

- Date: 2026-11-15, Asia/Taipei.
- Start: PR #7 branch `research/ms-03-earth-analogs`, SHA `778af696c654a191fe2a720f24d9f30ebd7d247b`.
- Working copy: isolated local clone; the original concurrent CRISM work was not edited.
- Publication history: initially retained locally at the user's request; the user later authorized pushing and direct merging. PR #7 had already merged, so this supplement uses a follow-up PR based on main `08d2740a23694a54bcc11cabf7120114d2e120fc`, branch `codex/ms03-original-tables-followup`. Check GitHub for actual publication and merge status.
- Fixed Mars cell: 57.50–58.00°N, 242.00–242.50°E, planetocentric/east-positive. It has not moved.

## Retained outputs

|File|Purpose|
|---|---|
|`table_acquisition.csv`|Three original-table identities, actual acquisition state, and remaining requirements. Blank hit counts mean not computed, never zero.|
|`source_column_notes.csv`|Table S4 field semantics extracted from the official USGS FGDC metadata; no observation rows.|
|`metadata/`|Actually acquired public DataCite records and the public author repository file inventory. These are metadata, not the target tables.|
|`requests_round*.json`|Exact public endpoints and why they were followed.|
|`requests_round*_retrievals.json`|UTC request times, HTTP responses, content types, sizes and SHA256 values. HTTP 200 is not an acceptance test.|
|`content_checks.json`|Content classification and bounded inspection results, including the sign-in response.|
|`validate_followup.py`, `validation.json`|Offline evidence, CSV, missing-value and unchanged-scope checks.|

## Status and use

- Cohen-Zada 2024: exact file DOIs for `Data Set 1.tab`, its header descriptions and `SI_Revised.pdf` are confirmed by the parent/child DataCite records. The actual tables were not obtained. The parent abstract mentions xlsx/docx while its format list advertises two TSV files and a PDF; this does not prove which bytes a future download will return.
- Levy 2009: the publisher lists TXT, XLS and PDF versions of Data Set S1. The TXT and alternate XLS download attempts did not return the table. The public author lab pages inspected here did not expose that original file.
- Dundas 2021: the USGS catalog and Asset Identifier Service were actually reachable, but supply the same FGDC metadata, not `TableS4.csv`. The exact catalog URL uses `USGS:...`; a separate attempted underscore URL returned 404. The data download and publisher attachment still returned challenge/error responses.
- No original table is marked acquired; no row count, point count or footprint intersection count was calculated. Fixed-cell membership remains unknown for all three tables.
- The Figshare exact-resource-DOI queries returned empty lists. That describes those queries only, not all repositories or all historical research.
- No new Mars geometry, ice detection, depth, abundance, Earth matching, or logger alignment is produced here. AD1 remains a general method reference and local morphology remains unknown.

## Resuming with actual files

1. Obtain the specified original tables, including the Cohen-Zada header descriptions. Keep download URL, date, version, bytes and checksum. An article PDF, a landing page, a metadata record, or an error page is not a substitute.
2. Read the actual coordinate and missing-value definitions before parsing. Preserve original values and IDs. Normalize longitude separately to 0–360 east only when supported by the definitions.
3. Query points in the inclusive fixed cell and record whether a point is merely an image center or an actual feature location. For image-based records, obtain the referenced official footprint and test intersection; center-only exclusion cannot establish a whole footprint is outside. Retain unknown geometry and boundary uncertainty separately.
4. Keep Table S4's `Yes (CTX)`, `Possible`, `Probable`, `Yes`, and `No` distinct. `CRISM ice? = x` means no appropriate data, not no ice. Any future membership match still requires observation-specific evidence; regional study coverage cannot establish local ice or morphology.
5. Record point hits and footprint hits separately. Even verified non-membership would exclude only that source table, not all prior work and not the existence of landforms or ice.

## Reproduce acquisition and validation

```sh
python3 outputs/research/MS-03/local_validation/original_tables_followup/collect.py outputs/research/MS-03/local_validation/original_tables_followup/requests_round1.json
python3 outputs/research/MS-03/local_validation/original_tables_followup/validate_followup.py
```

`finalize.py` reapplies the small evidence-table supplement, runs the offline checks and refreshes retained hashes. It performs no network, Git commit, push or merge. The existing CRISM files and observation inventory must remain byte-identical to the integration base.

Acquisition requires public network access and may return different responses later. Raw HTTP bodies are retained locally under ignored `responses/`; approved public metadata snapshots are copied under `metadata/`. Do not upload challenge tokens, error-page scripts, or large/raw scientific datasets as research results. No credentials or author messages were used.

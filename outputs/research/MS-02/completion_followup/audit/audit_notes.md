# MS-02 current structured-data reconciliation

Base: `521740108050ba16e406f8becb67a786179ff8bd`. This file is an evidence audit for the human report writer, not replacement report text.

The original root CSVs still contained statements superseded by the acquired primary-source review in `local_validation/`. Those contradictions were corrected without changing the fixed candidate IDs, original schemas, original scientific measurements, or formal report. Exact original and replacement cell text is retained in `reconciliation_log.json`, together with before/after hashes. Newly indexed records have new IDs.

| Record | Reconciliation | Evidence and limit |
|---|---|---|
| E01, EV-005/014/017/018 | Coarse MCS context is not local ground temperature; the 15 cm active layer is not all dry cover; 2560 h uses recorded temperature and calculated water activity | ME-10, AV-01, claim_corrections MCS-ORDER/UV-COVER/I06. No thermal-to-habitability transfer |
| E02, EV-029/062, PW-21 | A located Liu2018 thermal/material subcase is available; the original broad candidate remains pending | AV-06, primary DOI 10.1029/2017JF004535. Missing quantitative local terrain and original raw series remain explicit |
| E03, C1/C7, FP-01, EV-053/054 | CS-1 core date resolved to September 2019; August 2022 exposure remains a different support | AV-02 and Rasmussen §3.2 p5. No join to ADE or unlocated WISDOM lines |
| E04, EV-048, PW-22 | A Thomson2012 same-line core/GPR method subcase exists; original river-valley scope is separate | AV-07, primary DOI 10.1029/2012JE004053. Approximately 0.9 m wet overburden excavated; no intact-cover or SHARAD validation |
| EV-063–067 | Existing acquired Piqueux, SHARAD, CTX, CRISM and mAl results are now discoverable from the root evidence index | ME-12–15/17 and original product labels/locators. Conditional/modelled/unclassified quantities retain their limits |
| ME-13/14/15/17 | Evidence-type labels no longer say “not acquired” beside statuses documenting acquired products | Classification correction only; no new scientific measurement |
| FP-10/11/12, E03/E04 boundaries | W-station, Liu2018 and Thomson2012 subcases have separately indexed numeric source anchors; E03 distinguishes ADE scalar anchor from retained CS-1 | Arithmetic conversion of the published coordinates; original candidate scalar anchors retained. Thomson point does not imply known line endpoints/azimuth, intact cover or complete along-line ground truth |

`verify.py` checks unique IDs and preserved schemas, original-row retention, exact current cell values against the correction history, all four comparison facets for every Earth candidate, dates, retained unknowns, limited-use safeguards, arithmetic conversion of three published subcase anchors, separation of original candidate anchors from subcase footprints, current hashes, and byte-for-byte preservation of the formal report. Its success proves integrity of this reconciliation. It does not prove ice exists, establish a real 0.45 m ice table, provide local confidence intervals, or replace external raw/calibration/field observations.

Reproduce from the repository root:

```sh
python3 outputs/research/MS-02/completion_followup/audit/reconcile.py
python3 outputs/research/MS-02/completion_followup/audit/verify.py
```

The existing formal `docs/research/MS-02/report.md` was intentionally preserved for the user. It still contains historical claims already corrected by the current notes/tables; it must not be read as the current evidence-state authority. Prior historical verifier outputs were not rerun or relabelled as current science checks.

## New handoff consistency run

`current_handoff_check.py` was run independently against the base-commit files. It reads the historical verifier's section1 methodology but does not execute or import that historical script. It writes only `current_handoff_check.json`.

| Input/check | Observed result |
|---|---|
| Complete screened pool | 7,702,846 bytes; Git blob `f1563c4094487fe844d4e9beed0d806d1f7ad3c0`; 58,238 rows ×54 columns; exactly one52.75N168.25E target |
| Final/native/pool comparisons | All14 same-quantity checks passed with the original justified tolerances; current final/native file Git blobs were independently read from GitHub at the fixed base |
| Expected aggregation differences | TES TI coarse-minus-native0.032062139; MOLA slope0.000478962deg; SWIM1–5m−0.003508242. Different aggregation supports are not treated as failed equality checks |
| Historical integrated workbook | 23,035,176 bytes; Git blob `3cad1ffc711dbddeef6def24447e1bd1ff3fb5ba`; every ZIP member CRC passed; workbook XML lists **32 sheets**, superseding the old report's33-sheet statement |
| Historical verification artifacts | Before/after SHA-256 identical; no historical output was replaced or presented as a new science run |

The pool and workbook were checked against exact, read-only Desktop copies. The verified pool was copied into the isolated working path to support the run; it already exists byte-for-byte in the remote base, so no upload change is required. The workbook was inspected in place. These checks establish handoff-file consistency and workbook-container integrity. They do not recover missing original observational products or confirm ice.

On a complete repository checkout, reproduce with:

```sh
python3 outputs/research/MS-02/completion_followup/audit/current_handoff_check.py
python3 outputs/research/MS-02/completion_followup/audit/verify.py
```

For an isolated partial checkout, provide `--pool-source /path/to/screened_pool.csv.gz --workbook-source /path/to/NASA_Space_Apps_2026_All_Data.xlsx`. The script verifies the pinned Git blob identities before using or copying either supplied input.

## Final incoming-catalogue check

A source newly visible in the parallel MS-03 mainline update was checked for MS-02 before publication: the original Daubar2022 TableS1 author workbook, DOI `10.5281/zenodo.6604912`, 196,534 bytes, SHA-256 `393ed99a157a7e68a77fc3adf332939ea368a15f2b7ac2589cb701e4f82291f6`. Its MD5 matches the author-release value. `catalogue_roi_check.py/json` preserve all original headers and the source hash; the original workbook and other-site files were read only.

All1,203 finite coordinate rows were filtered against52.50–53.00N,168.00–168.50E using planetocentric latitude and east-positive longitude. Original headers contain conflicting parenthetical E/N suffixes; the variable names and centric qualifier were retained, with an independent official HiRISE `PSP_007561_1290` cardinal-orientation check. An image centre was not substituted for an impact point.

**Zero catalogued impact points fall in the fixed MS-02 cell**, including zero `y` or `possible` ice-exposing flags in that cell. This is a bounded catalogue-point result; it is not evidence of no ice, no impact/study, or no overlapping HiRISE image. Different catalogue selection rules and actual image footprints remain separate. The independent local ice-truth gap stays open.

```sh
python3 outputs/research/MS-02/completion_followup/audit/catalogue_roi_check.py --source /path/to/Daubar_2022_catalog_tableS1.xlsx
```

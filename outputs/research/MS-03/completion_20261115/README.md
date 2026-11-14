# MS-03 evidence-only integration

Technical evidence and reproducibility index, not a formal report or presentation.

- Source branch snapshot: PR #26, `ac39ed6810156feefd97f60647b95b754210a7da`.
- Accepted subset: 28 new files listed in [evidence_only_manifest.json](evidence_only_manifest.json). Original source blobs are retained exactly.
- `docs/research/MS-03/report.md` is not changed. The PR #26 replacement report, duplicate historical report, root candidates/evidence/prior-work/search/source tables, parent manifest and whole-package inventories/receipts are not included in this subset. They remain available only at the pinned PR snapshot.
- This directory does not assert that all 74 PR #26 paths were merged, that the original 26 structural checks apply to this subset, or that all scientific requirements are complete.
- Current evidence here: W short-file atmosphere tables and radar descriptive peak/scale diagnostics. Existing broader MS-03 evidence remains at its existing main paths.

## Reproduce

From the repository root:

```sh
python3 outputs/research/MS-03/completion_20261115/earth_atmosphere.py
python3 outputs/research/MS-03/completion_20261115/earth_validate.py
python3 outputs/research/MS-03/completion_20261115/radar_diagnostics/analyze.py
```

The first two use Python's standard library and the retained author-processed W gzip. The radar script requires NumPy and the pre-existing pinned `outputs/research/MS-03/local_validation/gap_completion/radar_local_arrays.npz`. No network calls or report-writing steps are required.

## Acceptance scope

- W source SHA-256 and provider MD5 verified against the pinned receipt; lossless gzip recreated and matched the exact PR blob.
- 17,705 source rows; the selected period is 16,032 half-hour records across January–November 2010, not a whole year. Five summary rows and 55 monthly rows reproduced byte-for-byte; an independent Decimal calculation passed.
- All 65 radar maxima independently checked; nine integrity/numerical checks passed. Both radar tables reproduced byte-for-byte.
- All 28 selected files were independently read and matched against their exact Git blob IDs. The retained radar manifest's file hashes and source input were checked locally.
- Source read/search records and original validation files retain their original provenance. They are not claims of a new literature search or new field measurement during this integration.

## Limits

Author-processed exports are not raw logger records. No clock correction, cross-logger alignment, temperature inversion, independent ice detection or Earth–Mars equivalence is established. Radar crop maxima are not accepted surface/subsurface picks; sample spacing is not bandwidth resolution. W remains a historical interface/data-QA reference, and AD1 remains a general geometry/method reference. Scientific completion remains false.


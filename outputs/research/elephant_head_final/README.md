# Elephant Head final data export - MR-20261114-v3-final

Published source observations, original parser and QA: McKay et al. (2019) supplementary table and Team2. This package is the mainline's export and reproduction of that work, not original field measurements, a new parser, or independent sensor calibration.

- Source: https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0954102019000269/resource/name/S0954102019000269sup001.pdf
- Original PDF: `elephant_head_2019_supplement.pdf`; SHA-256 `20fe70f574bc394f05f0c720809f80a9602ac73f6ede34d322ea816cf25590d9`.
- Team2 frozen evidence: `outputs/consolidated/research_main_20261114/sources/v2_14be2d5b/docs/research/team2_novelty_audit.md` and the EARTH-002 `executed_evidence_qa_json` in its companion CSV; source main `14be2d5b`.
- Fixed correspondence: EARTH-002 -> I-02 for research-question organization, not a physical-equivalence or ice-resource validation.

## Contents and reproduced results

`elephant_head_records.csv` contains all 8,922 printed records, one row per original record, with source PDF page/row and extraction-line number, both unchanged printed time strings/labels, nominal parsed times without timezone conversion, all nine original numeric tokens where printed, explicit 3 cm missingness, and retained RH flags. `data_dictionary.csv` documents every column, original header, units and nominal depth. Empty numeric fields mean absent source values, never zero.

The table spans 2017-11-28 00:00:00 to 2018-12-04 17:00:00 on the first printed time axis. The 3 cm group has 2,646 records and 6,276 missing records; its final printed record is 2018-03-18 05:00:00. No 3 cm annual mean or winter fill is produced.

The existing Team2 summer window is first printed time >= 2017-12-01 and < 2018-03-01: 2,160 same-row paired records (100.0% of the nominal hourly window), source rows 73--2232, PDF pages 1--27. Mean 3 cm temperature is -5.3553009259 degC; mean 49 cm temperature is -8.6301527778 degC; mean paired 3-minus-49 cm difference is +3.2748518519 degC. Both final PNGs show all paired hourly values, without smoothing or confidence bands.

The reference annual window is first printed time >= 2017-12-01 and < 2018-12-01: 8,760 records. Mean air is -20.2940171233 degC and mean 49 cm is -19.2370011416 degC. These and the summer means reproduce Team2's recorded QA; no target record count or mean is used to alter the extraction.

## Reproduction and checks

Run from the repository root:

```sh
python3 scripts/research/export_elephant_head_final.py --pdf outputs/research/elephant_head_final/elephant_head_2019_supplement.pdf
```

Dependencies: Python with `pypdfium2` and `matplotlib`. The row expression and six/nine-value interpretation are Team2's existing parser. Its already-used PDFium extraction path is selected because local pypdf 6.14.2 plain extraction concatenates rows. This export does not claim a fresh double-engine check. It verifies the exact source hash, contiguous original IDs, hourly first timestamps, 90-minute difference between printed times, all CSV numeric tokens/row/page/time fields after roundtrip, and dynamically compares its computed summary with the pinned Team2 QA JSON. `qa.json` contains the checks, values and limits; `manifest.json` contains final file hashes. Failed checks stop export rather than tuning data to expected totals.

## Limits

- Preserve `Time, GMT-07:00` and `Local Time GMT-5:30` exactly. A consistent 90-minute offset does not resolve UTC or local solar time; neither conversion is made.
- Published corrected 49 cm RH exceeds 100% in 2,807 records. All values remain unchanged and flagged. No clipping, new correction formula or water-activity inference is applied.
- The 3 cm and 49 cm temperatures are subsurface point observations, not satellite LST. Air sensor height is unspecified by this table header.
- Serial correlation is not modeled: record counts are not counts of independent replicates. No confidence interval or new causal effect is claimed.
- This package does not infer ice depth, TES thermal inertia, blind-detection accuracy, sample heating, ice mass loss, or Earth-to-Mars equipment performance. Agreement with earlier QA cannot exclude errors in the original published table.

Only the final two PNG figures are supplied: `summer_temperatures.png` and `summer_temperature_difference.png`. Original data remain attributed to the authors; project code licensing is not assigned to the publisher's supplementary data.

# Mars three-candidate reselection - 2026-11-14

Version: MARS-RESELECT-20261114-v1. Full-data inventory with six-objective exploratory screening, native-cell evidence and bounded prior-site checks. No scalar suitability score, global novelty clearance, landing approval or ice-resource validation.

## Read first

- [Chinese report, PDF](mars_three_candidates_report_zh.pdf): 8 pages, visually reviewed.
- [Chinese report, Markdown](report.md): includes full source links, reading scope and seasonal context.
- [Final three metrics](final_candidates.csv): MS-01=A, MS-02=D, MS-03=C. Native review and final selection statuses are separate.
- [Selected targets and footprints](selected_targets.json).
- [Every data product and its role](all_data_usage.csv).
- [Bounded prior-site audit](bounded_prior_site_audit.json), [published impact point table](known_ice_points_morgan2025.csv).

## Provenance and reproduction

- [Native candidate evidence](candidate_native_evidence.json): four inspected cells including B, held out near a known exposure without a duplicate ruling.
- [Method and protected inputs](method.json), [computational commands](COMPUTATION.md).
- [Numerical validation](numerical_validation.json), [report validation](report_validation.json), [old-deliverable preservation](preservation_check.json).
- [Artifact hashes](report_manifest.json).
- Reconstructed dust and populated MCS bin series are supplied as CSV.GZ; these retain their native support and missingness.

All three candidates are above 50N. They do not satisfy the latitude conditions used by MCOA2025 or the current SkyFall mission; no claim of compliance is made. The original Earth-analog discovery goal remains separate and unfinished. New outputs exist locally only; no commit, push, merge, deployment, registration or official submission was performed.

Original observations remain attributed to their authors/providers. AI assisted the code, checks and report. Actual computation used Mac CPU, not GPU or model training. Dust-derived parts retain the Montabone CC-BY-SA-3.0 attribution; other sources retain their own terms.

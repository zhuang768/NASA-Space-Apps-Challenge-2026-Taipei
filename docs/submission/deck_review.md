# Submission deck review, 15 November 2026

- Original native presentation: [Team ZASA mars research](https://docs.google.com/presentation/d/1gR2CjO5nO1_s5Aci4MeIxZWeSDTgK1VZyKbyME2TRgI/edit).
- Reviewed deliverable: [seven-page PDF](../../outputs/submission/team_zasa_demo.pdf).
- File and annotation checks: [verification record](../../outputs/submission/deck_verification.json).
- Repository evidence anchor: `42f55166c3a12d86b24757880c11d2be7eb2f20c`. The selected-source table is unchanged.

## Corrections in the delivered PDF

- Page 2: corrected “Trade-offs guide further review.”
- Page 3: replaced the unexplained 0–1 radar display with a six-field raw-value table for the three targets. Values are read directly from `final_candidates.csv`; SWIM consistency, slope, relief and reconstructed MY34/MY35 dust p95 retain their units and declared rounding. Removed the unsupported mission-envelope wording from the caption; landing suitability remains unestablished.
- Page 5: separated the subtitle from the MOLA chart and removed overlapping caption fragments. The original relief and thermal-inertia values are unchanged. Replaced the raster availability matrix with a vector table: “Available” means regional descriptors, not local confirmation. MS-03 morphology is explicitly “Unknown”; no qualified closed contours were accepted in the inspected windows.
- Page 7: fitted the heading inside the page, corrected “trade-offs,” and retained the unverified-ice statement.
- All seven pages have a clickable source-index footer. The final page adds a concise Team zasa / AI-assistance credit without inventing team-member names or model versions.

## Actual checks

- The seven-slide native presentation was read and exported. A structural checker reported zero issues; visual review independently found the overlaps and missing source links above.
- All seven edited pages were rendered and inspected. Missing font-subset glyphs and contaminated chart crops were corrected; the changed fifth page was rendered and inspected again.
- Final PDF: seven pages, 720 × 405 pt per page, 7,987,602 bytes, SHA-256 `c8982aff2f42b66b28ba19df866161baac1ee5faef50080218a61c977ec5cd77`.
- All seven source-link annotations point to the GitHub reference index. The file is below 10 MB.
- No site coordinates, scientific source values or original research files were changed. These are presentation checks, not confirmation of ice, analogue validity, novelty or completed competition submission.

## Delivery format and blocked native operations

The original Google Slides file is unchanged. Its edit request returned provider `403 PERMISSION_DENIED`. An attempted owned-copy fallback was rejected by automatic approval review because the persistent copy and destination ownership were not sufficiently authorized. No alternate cloud-copy or sharing operation was attempted after that rejection.

The delivered PDF is a local presentation correction. It retains rasterized 120-dpi views of the original slides and uses vector text/tables for the corrections, so the removed original labels are not hidden searchable text. Existing scientific graphics are reused as displayed; rendered pixels are not additional measurement resolution. Original typography remains in the retained backgrounds; correction overlays use Arial to avoid unsupported characters in the source font subsets. This is not an editable PPTX or a replacement native Google Slides deck.

The Slidesgo theme's applicable attribution and reuse terms remain a team check. Individual participant registration, form fields, team confirmation of original-code licensing and the final SUBMIT action are separate from this deck review.

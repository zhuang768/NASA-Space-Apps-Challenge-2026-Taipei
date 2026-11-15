# Challenge alignment and evidence checklist

Reviewed 2026-11-15. Starting main: `07dbe29203504ba0ccde5e379f42ecc16e4b1b4f`.

**Assessment: partial challenge response.** The retained work supplies Mars candidate screening, source-scale context, an interactive map and established Earth method references. It has not established a new, validated terrestrial analogue or a qualified common-scale MS-03/Earth contour comparison.

## Official information and its limits

The [official challenge](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/) is “Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars.” Its indexed synopsis asks teams to use open space-agency planetary/Earth data to identify and characterise terrestrial analogues and present the findings through a map, visualisation or tool.

On this review date, direct reads of the complete challenge page, its Resources tab, [general Resources](https://www.spaceappschallenge.org/resources/) and [Participant Terms](https://www.spaceappschallenge.org/legal/) failed. Search-indexed official text was available. It supports the broad task summary above, not a claim that every complete rule, resource or submission requirement has been checked. The team must confirm the current full Details/Resources and its account's submission form. No slide limit, format approval or eligibility ruling is inferred here.

Earth–Mars remains the team's chosen scope. No Moon analysis was added. That scope is declared rather than presented as formally approved by the organisers.

## What the repository supports

| Challenge component | Actual evidence | Status and limit |
|---|---|---|
| Use space-agency data | [Mars input manifest](../config/raw_inputs_manifest.json), MOLA/TES PDS products, SWIM and supporting temperature/dust records | Retained numerical products and exact source identities; NASA data use is supported. |
| Explain target conditions | [Three fixed regions](../outputs/research/mars_reselection_20261114/final_candidates.csv), native-grid evidence and four-theme records | Regional descriptions; no landing, base, local ice or resource-quantity validation. |
| Characterise Earth references | [Earth status ledger](earth_submission_status.csv) and existing candidate CSVs | Known method references with separate footprints and missing independent truth; not three validated matches. |
| Identify new Earth analogue candidates | Edson Hills, Bethel and Cape Blossom appear in the narrative | Proposed follow-up cases; corresponding source/calculation packages not found in the checked GitHub records. Novelty and validation remain open. |
| Quantitative MS-03 geometry comparison | [Repository-only audit](../outputs/research/MS-03/repository_validation_20261115/README.md) | 185 published AD1 closed source polygons can be remeasured; no accepted in-box Mars contours. Common-scale comparison remains insufficient. |
| Present findings | Existing TerraMatch explorer and source notes | Implemented regional viewer; map texture or display sampling does not supply high-resolution local truth. |
| Attribution and original-code reuse | [Data rights record](../DATA_LICENSES.md) | Third-party terms remain separate. Original-code licence requires the team's decision. |
| Evaluator access and submission | Existing public-site link and private-repository publication history | Current signed-out evidence access, registration, form completion and final SUBMIT are not certified by this repository update. |

The six screening objectives are exploratory choices, not official mission requirements. The four comparison themes are terrain, temperature/thermal properties, water/ice and atmosphere/dust. Missing comparable measurements remain unknown; they do not become an overall similarity percentage.

## Claims corrected in this update

| Previous draft or UI statement | Correction | Reason |
|---|---|---|
| Cape Blossom 1,927 centres and 400 offset calculations presented as completed | Retained as a proposed source; completed-result wording removed | Original centre records, coordinates, scripts and output tables not found across 42 searched branch heads, relevant retained archives and two Release inventories. |
| Samoylov numeric IoU experiment presented as completed | Withdrawn from the completed-results narrative | The closed annotation/raster/test package was not found. The audit does not assert that the external research is wrong. |
| New Earth field cases implicitly replace existing candidate tables | Existing IDs and dispositions remain authoritative | A narrative proposal does not revise a fixed candidate's identity, footprint or validation status. |
| SWIM displayed as 0 to 1 | Signed −1 to +1; maps share evidence | A consistency score is not ice abundance or probability. |
| MCS called air temperature | Model-time-adjusted surface temperature; separate populated-bin medians | Their difference is not a paired daily amplitude or a continuous weather record. |
| Dust p95 described as peak haze or clearest air | MY34 reconstructed column-opacity 95th percentile | It is not measured local visibility, wind or surface accumulation. |

The previous draft's proposed-source citations remain traceable: [Cape/Blueberry study](https://doi.org/10.5194/tc-19-6355-2025), [centre dataset](https://doi.org/10.5281/zenodo.14756139), [Samoylov inventory](https://doi.org/10.1594/PANGAEA.944071). A DOI destination was not acquired as data in this repository-only audit. These links do not certify the removed project calculations.

MS-01/02's newer narrative numbers were not silently recalculated or changed. Their source packages need to be handed over before they can be treated as repository-reproducible results. The team should review their interpretation in the final human-authored report.

## Before final submission

- [x] Declare Earth–Mars scope and preserve the fixed Mars boxes and candidate IDs.
- [x] Keep measured data, product estimates, project calculations and proposed tests distinct.
- [x] Publish the MS-03 scripts, source receipts, inspected windows, numerical checks and explicit NA geometry.
- [x] Correct SWIM, MCS and dust terminology without changing source numbers.
- [x] Distinguish current evidence checks from historical publication and deployment receipts.
- [ ] Deliver source files, spatial support, units, QA, methods and outputs for each newer Earth proposal before claiming its calculation as completed.
- [ ] Obtain qualified in-box Mars outlines and independent Earth image/outline truth before a common-scale geometry or IoU claim.
- [ ] Establish a defensible, use-specific Earth research difference; do not claim a first or globally new analogue from a limited search.
- [ ] Confirm full official Details/Resources and account-specific submission requirements.
- [ ] Confirm the team's original-code licence; do not apply a licence on behalf of an unconfirmed team decision.
- [ ] Check third-party attribution/terms and signed-out evaluator access to required evidence.
- [ ] Confirm registration/team details, final submission material and the actual SUBMIT action. These remain outside this code/data update.

## Verification scope

The independent MS-03 audit froze the starting main and PR #26 at `ac39ed6810156feefd97f60647b95b754210a7da`. It reran 70 numerical fields from checksum-equivalent GitHub archival inputs, checked retained image support, inspected eight fixed windows plus one CTX crop, and remeasured 185 published AD1 polygons. It did not prove local ice, a new analogue, independent annotation accuracy or equipment performance.

The root manifest now describes the explicitly listed current files. Its prior version is retained at [baseline_release_manifest.json](../outputs/integration/challenge_alignment_20261115/baseline_release_manifest.json). `PUBLICATION.json`, older report manifests and historical deployment notes retain their original verification scope; they are not fresh acceptance of this update. See [current verification](../outputs/integration/challenge_alignment_20261115/verification.json) for checks actually executed in this round.

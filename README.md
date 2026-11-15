# TerraMatch

TerraMatch is Team ZASA's NASA Space Apps 2026 project. We used public data to choose three regions on Mars for follow-up research on shallow ground ice. We then looked for places on Earth where we could test the methods we would use to study those regions.

## What the project shows

The [TerraMatch explorer](https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev/) lets you compare the three Mars regions. Start with the map, then look at slope, thermal inertia and the SWIM ice consistency index. The modeled depths have their own explanation because they depend on assumptions about the material below the surface.

We kept MS-01, MS-02 and MS-03 because they present different research questions. MS-01 has the highest mean thermal inertia of the three. MS-02 is farther south and has more complete thermal inertia coverage, but also higher relief and a higher dust percentile in Mars Year 34. MS-03 has the lowest mean regional slope and the highest shallow SWIM score of the three.

The retained Earth records are established method references: University Valley, Beacon Valley, Adventdalen AD1 and a bounded Haughton subcase. Their candidate tables preserve separate footprints and limits. Edson Hills, Bethel and Cape Blossom are proposed follow-up cases in the narrative; their corresponding source and calculation packages were not found in the checked GitHub version. We have not confirmed local Mars ice, validated an Earth match, or established a new terrestrial analogue.

## Challenge alignment and current evidence

The challenge asks for Earth analogue candidates and their characterisation, presented through a map, visualisation or tool. Our Mars screen and explorer support that investigation. The new-Earth-analogue component remains incomplete; a known Earth method reference is not a newly discovered analogue. The project keeps its Earth–Mars scope and does not claim lunar analysis or formal eligibility approval. Full official Details/Resources and submission-form requirements still need confirmation; a searchable synopsis is not the complete rules.

| Component | Current status |
|---|---|
| Space-agency Mars data and regional screening | completed outputs and provenance retained |
| Interactive regional visualisation | implemented; image sampling is not local hazard resolution |
| Earth environment/method references | limited, with location and independent-truth gaps |
| MS-03 image and AD1 geometry audit | 70 numeric checks reproduced; 185 closed Earth source polygons; Mars contours remain unqualified |
| New Earth analogue and common-scale comparison | not established |
| Global novelty and full submission eligibility | not verified |

See the [challenge/evidence checklist](docs/CHALLENGE_ALIGNMENT.md), [Earth data-status table](docs/earth_submission_status.csv) and [MS-03 executable audit](outputs/research/MS-03/repository_validation_20261115/README.md). The frozen audit reviewed main `07dbe29203504ba0ccde5e379f42ecc16e4b1b4f`, PR #26 and 42 branch heads; it distinguishes absent source packages from negative scientific findings.

The existing Earth candidate records are [MS-01](outputs/research/MS-01/candidates.csv), [MS-02](outputs/research/MS-02/candidates.csv) and [MS-03](outputs/research/MS-03/candidates.csv). Their IDs and dispositions remain authoritative over newer narrative proposals.

## Files

- [Final comparison results and replay instructions](outputs/research/final-comparison-20261115/README.md)
- [Selected targets](outputs/research/mars_reselection_20261114/final_candidates.csv) and [fixed study boundaries](outputs/research/mars_reselection_20261114/selected_targets.json)
- [Complete Mars screening results](outputs/research/mars_reselection_20261114/screened_pool.csv.gz)
- [Integrated data workbook](outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx)
- [Numerical rebuild instructions](docs/REPRODUCE.md), [Mars input manifest](config/raw_inputs_manifest.json) and [data attribution](DATA_LICENSES.md)

## Reproducing the Mars analysis

Use a fresh working copy with Python 3.12 and install the packages in `requirements.txt`. Follow the numerical section of the rebuild instructions and use `--skip-report` to avoid regenerating historical report files. The full rebuild checks 11 public source files before processing them and replaces local generated outputs. It reproduces the Mars screening, not the separate Earth literature review or field observations.

NASA, data publishers and the original investigators retain credit for their observations. TerraMatch is an independent team project.

## 2026-11-15 evidence-alignment update

Corrected unsupported completed-result wording for Cape Blossom/Samoylov, published the repository-only MS-03 check, and separated retained Earth references from proposals without source packages. Website labels now distinguish signed SWIM consistency, model-time-adjusted surface temperature and reconstructed dust percentiles. Original science values and candidate IDs are unchanged. Verification in this update checks the declared files and semantics; it does not establish ice, novelty, deployment or a completed NASA submission. Original-code licensing, evaluator access and final submission remain team actions in the checklist.

Later main `ec3f38fd018b55b993232151d441d84286676da3` added final comparison/replay tables and an Earth check tab. They are preserved. The stored AD1 grid-phase test can be replayed from repository inputs; it measures digital geometry sensitivity, not optical recognition or a Mars match. Other replay entry points explicitly require separately supplied team ZIPs.

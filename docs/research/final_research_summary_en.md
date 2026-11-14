# Mars ice investigation: what the evidence supports

Team zasa | 14 November 2026 (Asia/Taipei) | MR-20261114-v3-final

## Research question

How can published Earth ice-interface records help define the additional observations needed to investigate Mars candidates I-01 and I-02? This delivery documents source and data QA, reproduces descriptive thermal results, and states the limits of those results. It does not validate a new ice-detection method or a Mars resource.

## Why retain I-01 and I-02?

Both Mars candidates are retained as conditional research cases: their regional mean slopes and SWIM shallow-ice consistency descriptors are close, while TES thermal inertia differs. I-01 is at 54.25 N, 1.25 E; I-02 is at 53.75 N, 42.25 E (planetocentric latitude, east-positive longitude). They are not controlled experimental replicates or extraction recommendations.

| Mars descriptor | I-01 | I-02 |
|---|---|---|
| Mean slope (degrees) | 0.302596 | 0.305738 |
| Cell relief (m) | 76 | 88 |
| TES thermal inertia | 244.709671 | 160.666672 |
| SWIM shallow consistency | 0.354307 | 0.355086 |
| MY35 mean dust CDOD | 0.106878 | 0.112248 |

Rounded descriptors from the existing Mars records [P1]. Thermal inertia is in J m^-2 K^-1 s^-0.5; SWIM and CDOD are dimensionless. SWIM values are not ice percentages or probabilities. Scores are not confidence or landing approval.

## Three Earth roles

| Fixed pairing and role | What is supported |
|---|---|
| EARTH-002 / I-02<br>Elephant Head: main archival case | A published monitoring point with a historical 49 cm ice-cemented interface and an exportable hourly table. Selected for a tractable QA and reproduction task, not proven best physical equivalence to I-02. |
| EARTH-UV-001 / I-01<br>University Valley: known-use reference | W station has a historical 42 cm interface. Valley-scale Mars-analog drilling, short sampling intervals and temperature control have precedents. Their exact overlap with a new W plot is unverified. |
| EARTH-003 / I-02<br>Linnaeus Terrace: inactive backup | Historical multi-depth temperature data exist. Conflicting 25 cm and 45 cm interface citations remain unresolved; no single interface truth is adopted and no second analysis stream was activated. |

All three are already studied sites. Their published point anchors are not approved new test plots, and their different years, materials and measurement supports do not establish a controlled cross-site comparison. [P2]

## Elephant Head: observed data, bounded conclusions

Team2 supplied the existing parser and original full-table QA; this delivery reuses that method for export, reproduction and artifact checks. The final delivery independently re-extracted the publisher's 108-page supplement, checked its source hash, and exported 8,922 records with source-page/row provenance. The first printed timestamp spans 2017-11-28 00:00:00 to 2018-12-04 17:00:00. The two printed clocks are 90 minutes apart; their UTC/solar-time meaning is unresolved, so these are original-label windows. [P3, S1]

| Window / paired support | Air (deg C) | 3 cm (deg C) | 49 cm (deg C) |
|---|---|---|---|
| Annual: N=8,760 | -20.294 | Not computed | -19.237 |
| Summer: N=2,160 | -10.341 | -5.355 | -8.630 |

Annual: 2017-12-01 inclusive to 2018-12-01 exclusive. Summer: 2017-12-01 inclusive to 2018-03-01 exclusive, using the first printed timestamp. Summer 3 cm minus 49 cm mean difference: +3.275 deg C. N counts records, not independent samples.

The 3 cm channel has 2,646 records and ends at 2018-03-18 05:00:00; absent winter values remain missing. The 49 cm corrected-RH column has 2,807 values above 100%; values are retained and flagged, not clipped or treated as calibrated water activity. The 3 cm sensor measures subsurface temperature, not satellite land surface temperature. Reproduced means are not new field measurements.

## What these data cannot answer

These records cannot uniquely invert ice depth or TES thermal inertia, separate overburden causes from all confounders, validate blinded accuracy, or quantify drilling heating and sample ice loss. No new independent interface truth, material controls or initial/final ice mass were measured. Mars ice presence, depth, purity, continuity, quantity and extractability remain unconfirmed at I-01/I-02. Their nominal cells are about 30 x 17 km; dust retains native 3-degree reconstructed support, not local weather. TES thermal inertia is not temperature or hardness.

## Originality and completion

Novel Earth sites, novel uses and a distinct scientific contribution have not been demonstrated. Prior work includes monitoring, ice stability, drilling/sampling components and cross-site mechanism comparisons. Non-overlap with inspected Mars proposal footprints is a bounded catalog finding, not clearance against every proposal. This delivery completes traceable QA, descriptive reproduction and evidence requirements; completing the deliverables does not complete the original novelty goal. Blinded trials, controlled overburden experiments and Earth-to-Mars performance transfer remain future proposals, not open tasks in this delivery.

## Sources and reproducible project records

Paths below are relative to the project root. Original studies are linked for attribution; this summary adds no new literature search.

- [P1] Mars values and scale definitions: [docs/research/main_mars_research_cards.md](../../docs/research/main_mars_research_cards.md)
- [P2] Scope, site roles and prior-use findings: [docs/research/main_project_synthesis.md](../../docs/research/main_project_synthesis.md)
- [P3] Final records, QA, dictionary and figures: [outputs/research/elephant_head_final/README.md](../../outputs/research/elephant_head_final/README.md)
- [S1] [Elephant Head study (McKay et al., 2019)](https://doi.org/10.1017/S0954102019000269).
- [S2] [University Valley study (Marinova et al., 2022)](https://doi.org/10.1017/S0954102022000025).
- [S3] [Linnaeus study and GGD6 data](https://doi.org/10.1017/S0954102098000054).
- [S4] [GGD6 version 1](https://doi.org/10.7265/tjgd-wp08).

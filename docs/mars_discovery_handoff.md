# Mars discovery: Matching → Reporting handoff

Reviewed 2026-11-14 (Asia/Taipei), against commit `7df7f33`. Source: [discovery JSON](../outputs/mars_discovery/mars_site_discovery.json), SHA-256 `3c45d6af3c786394b856e36a726eada5cf00118e7a0cec39b24a88e8f992b7e9`. Selection principles: [user brief](site_discovery_brief.md).

## Decision for Reporting

| Purpose key | Recommended treatment | Picks |
|---|---|---|
| `isru_shallow_ice` | Keep **conditional research candidates** for shallow-ice characterization relevant to possible future ISRU. Neither is novelty-cleared or an extraction recommendation. | I-01 and I-02 |
| `dusty_flat_ops` | Keep two **context references** for comparing dust-column observations over regionally low-slope terrain. Drop the claim that these are validated dust-tolerance test sites or novel operational sites. | D-03 and D-04 |
| `firm_rocky_surface` | **Drop the firm-ground / construction / trafficability purpose claim.** Retain the original shortlist only as an unvalidated thermophysical diagnostic. | No operational recommendation |

**None of the 15 reviewed centers is cleared for “never studied,” “previously unproposed for this purpose,” or “understudied” claims.** Exact same-purpose proposals were not confirmed in the inspected sources; that is an unresolved check, not a novelty result. Two dust picks overlap a published operations-related dust study area. Regional precedents exist for several others. If a presentation requires verified new-site status, none can yet carry that headline.

I/D/F IDs below mean purpose initial plus **original JSON order**, not a new ranking. All coordinates are planetocentric latitude and east-positive longitude in degrees; negative latitude is south, negative longitude is west. No scores or scientific outputs were changed.

## What the numbers support

- The score measures closeness to manually specified descriptor targets, not monotonic maximization of ice, dust or firmness. Targets include ice consistency **0.35**, dust CDOD **0.20**, and thermal inertia **400**. They were design choices, not validated mission optima. Scores are not confidence, percent similarity or landing approval; do not compare scores across purposes.
- The stack has **0.5° spacing**, nominally about 29.6 km north–south and `29.6 × cos(latitude)` km east–west. MOLA slope is a cell mean of slopes calculated at approximately 3.7 km baseline; relief is cell elevation range, subsequently interpolated onto the common grid. These are not boulder-scale hazard measurements or the existing Earth search's 100 km-window statistics.
- TES thermal inertia (TI) has units **J m⁻² K⁻¹ s⁻½**. SWIM `ice_shallow` is an averaged consistency indicator, **−1 to +1**, associated with the <1 m product; it is neither an ice fraction nor a calibrated probability. The 2026 probabilistic study [S1] is separate from this SWIM 2.0 indicator.
- `dust_cdod` is the **MY35 annual mean, local total-column, 9.3 μm absorption optical depth**, dimensionless. Its reconstructed native support remains **3°**, despite the 0.5° display [S11]. It does not measure local deposition, abrasion, wind or event frequency. The discovery stack does not use MY34 for this score.
- The JSON contains no per-cell source-validity counts, landing ellipse, mechanical measurements, regional day/night surface temperature or Earth analog pairing. A finite layer value does not establish all of those checks.

## Review of each purpose's original top five

`unchecked` below means **exact candidate footprint + same intended purpose remains unverified**. Regional prior art is stated separately; neither a nearby named place nor a literal coordinate-search non-hit establishes duplication or novelty. Full-precision values, search strings and decisions are in [the 15-row audit](mars_discovery_novelty_checks.csv); broader query/access scope is in [the search log](mars_discovery_search_scope.json).

### Shallow ice / possible ISRU

| ID | Center (lat, lon) | Stored score | Purpose evidence | Same-purpose / known-site check |
|---|---|---:|---|---|
| I-01 | 54.25, 1.25 | 0.943774 | SWIM 0.354307; slope 0.302596° | **unchecked**. Northern-plains ice-resource screening is established [S1]; Acidalia has regional ice-landform research [S4]. Neither source verifies this cell as a proposed extraction site. Conditional follow-up. |
| I-02 | 53.75, 42.25 | 0.938846 | SWIM 0.355086; slope 0.305738° | **unchecked**. The actual Protonilus human/ISRU proposal is at 42.187°N, 48.062°E [S3], about 722.5 km away, not this cell. Regional purpose precedent is not exact overlap. Conditional follow-up. |
| I-03 | 54.75, 86.25 | 0.930799 | SWIM 0.351863; slope 0.279436° | **unchecked; hold**. Utopia ice deposits have substantial prior research [S2]. No overlap between this cell and that paper's deposit footprint was established; do not copy its ice-volume estimates here. |
| I-04 | 55.75, 61.75 | 0.925857 | SWIM 0.349633; slope 0.283747° | **unchecked; hold**. Broad midlatitude ice-resource work exists [S1], but no exact same-purpose site proposal was verified. No evidence that this is less studied than I-01/I-02. |
| I-05 | 53.75, 123.75 | 0.922164 | SWIM 0.356685; slope 0.264141° | **unchecked; hold**. Utopia regional ice work [S2] applies as prior-art context, not point validation. Being north of the excluded 40–50°N box does not make the wider region new. |

### Dust and low-slope terrain

| ID | Center (lat, lon) | Stored score | Purpose evidence | Same-purpose / known-site check |
|---|---|---:|---|---|
| D-01 | 35.75, 126.75 | 0.915908 | CDOD 0.199018; slope 0.229956° | **Regional operations-related prior-art overlap [S5].** Center is 1,521.7 km from the published Utopia monitoring-circle center, inside its 2,000 km radius. Exact equipment-test proposal remains unchecked. Exclude from a novelty-led recommendation. |
| D-02 | 37.75, 114.75 | 0.895832 | CDOD 0.198724; slope 0.221386° | **Same regional overlap [S5]**, distance 1,294.5 km. This is a dust-study footprint, not one of its approved/project landing sites. Exclude from a novelty-led recommendation. |
| D-03 | −46.25, 82.75 | 0.888348 | CDOD 0.206159; slope 0.232254° | **unchecked** for a specific operational site. Hellas dust storms are already documented [S7]; no claim of a newly discovered dusty region. Keep only as a contextual contrast. |
| D-04 | 7.75, 154.25 | 0.887477 | CDOD 0.199430; slope 0.240819° | **unchecked**. InSight supplies an Elysium dust-operations precedent [S6], but its center is about 1,098.2 km away [S13], not this cell. Keep as a contextual contrast. |
| D-05 | 5.75, 145.75 | 0.861298 | CDOD 0.194399; slope 0.263780° | **unchecked; hold**. Same regional precedent [S6]; about 586.2 km from InSight [S13]. Proximity alone does not make this its landing site, nor establish novelty. |

The [S5] check uses a Mars sphere of radius 3,396 km and great-circle center distances to **17°N, 107°E**. Both D-01 and D-02 are outside that paper's 17–30°N landing-latitude interval while inside its wider monitoring circle. This establishes prior regional dust analysis, **not an exact previously recommended landing ellipse**. Numerical checks are in the CSV; no rank was recomputed.

### Firm / rocky label

| ID | Center (lat, lon) | Stored score | Relevant evidence | Same-purpose / known-site check |
|---|---|---:|---|---|
| F-01 | 52.25, −19.75 | 0.910243 | TI 397.505371; SWIM 0.080129 | **unchecked** for mechanical use; Acidalia ice-landform research exists [S4]. TI alone cannot establish competent bedrock [S8,S9]. |
| F-02 | −59.75, 3.75 | 0.881735 | TI 403.109589; SWIM 0.499967 | **unchecked**. Coordinate searches did not yield a verified relevant proposal. Positive SWIM is an additional reason to investigate material ambiguity, not proof of ice at the surface. |
| F-03 | −54.75, 13.75 | 0.851686 | TI 410.146057; SWIM 0.297439 | **unchecked**. No exact same-purpose proposal verified; no cell-level geological or mechanical interpretation established. |
| F-04 | 52.25, −27.75 | 0.847944 | TI 396.183685; SWIM 0.038759 | **unchecked** for mechanical use; regional Acidalia research [S4] is not a bearing-strength measurement. |
| F-05 | −58.25, −52.25 | 0.812036 | TI 410.433319; SWIM 0.456089 | **unchecked**. Southern Argyre has proposed exploration/landing sites [S10]; exact overlap and the mechanical-use purpose were not confirmed. |

All five are withdrawn from **firm-ground recommendations**, independent of novelty. The provider describes multiple material mixtures yielding similar TI [S8]; published thermal models also distinguish intermediate-TI materials from continuous bedrock [S9]. Do not infer rock strength, low wheel sinkage, foundation capacity, low rock abundance, mineralogy or dust-mantle thickness from these values. Reporting may display the unchanged key under “thermophysical candidates—material unverified.”

## Four recommended reference cards

These are **editorial follow-up choices, not a reranked score product**. The pair per purpose provides different research context; it does not demonstrate superior novelty or mission suitability.

| ID | Intended follow-up | Slope ° | Relief m | TI | SWIM shallow | MY35 CDOD |
|---|---|---:|---:|---:|---:|---:|
| I-01: 54.25°N, 1.25°E | Characterize possible shallow ice over low regional slopes, then assess Earth permafrost/excavation analog requirements. | 0.302596 | 76 | 244.709671 | 0.354307 | 0.106878 |
| I-02: 53.75°N, 42.25°E | Independent longitude-sector follow-up for the same ice/terrain question. | 0.305738 | 88 | 160.666672 | 0.355086 | 0.112248 |
| D-03: 46.25°S, 82.75°E | Hellas-region reference for dust-column observation planning over low regional slopes. | 0.232254 | 66 | 187.494629 | 0.135669 | 0.206159 |
| D-04: 7.75°N, 154.25°E | Elysium-region contextual counterpart for that dust/terrain question. | 0.240819 | 83 | 176.020203 | −0.030731 | 0.199430 |

**I-01 weaknesses / prohibited claims:** High-latitude thermal and power requirements, actual ice depth/purity/continuity, overburden, excavation energy and hazards remain unassessed. Do not say “35.4% ice,” “94.4% suitable,” confirmed <1 m ice, extractable resource, safe landing or new ISRU site. Next: native-source validity, local imagery/radar evidence and an exact same-purpose proposal/footprint search.

**I-02 weaknesses / prohibited claims:** Same ISRU gaps; neither the Protonilus proposal's resources nor measurements transfer to this point. TI is a thermal descriptor, not drillability or a day/night temperature measurement. Do not identify this as Protonilus EZ, a validated alternative to it, or the less-studied winner. Next: local geological context, source coverage and point-specific literature.

**D-03 weaknesses / prohibited claims:** Regional Hellas dust activity is known; a coarse annual column value omits seasonal extremes and surface transport. Cell relief does not establish a safe work area. Do not say “new dust-storm hotspot,” “worst dust,” measured deposition, tested equipment suitability or predicted power loss. Next: season-resolved native dust, surface flux/wind observations or a justified model, then local terrain checks.

**D-04 weaknesses / prohibited claims:** InSight's observations are not measurements at this cell, and its optical depths are not directly interchangeable with the JSON's 9.3 μm absorption CDOD. Low TI does not prove a particular grain size or load-bearing behavior. Do not claim the first dust-operations site, InSight ground truth here, or an already matched Earth test location. Next: point-specific prior proposals and the same dust/terrain checks as D-03.

## Reporting contract and remaining novelty gate

1. Retain **Earth↔Mars only and all four themes**. These are Mars reference centers, not completed Earth–Mars analog matches. Pair an Earth location only after matching quantities, physical footprints, periods and QA; the older 100 km Earth-window features cannot be directly combined with these cell summaries.
2. Display terrain measurements, TI under thermal context, SWIM under water/ice, and CDOD under atmosphere/dust. **Regional surface temperature remains missing** in this discovery JSON. No new four-theme calibrated suitability score has been established.
3. Attach source links, source resolution, period and `novelty: unchecked_exact_site` to each reference card. No “new,” “understudied,” confidence or landing-approval badge. Do not promote D-01/D-02 as unexamined regions.
4. Preserve [the three original maps](../outputs/mars_discovery/README.md), order, scores and cyan-box meaning. Excluding boxes is not excluding whole named basins or every past proposal. Retain [dust-data attribution/license information](../outputs/mars_profiles/LICENSE-data.md) when reusing dust-derived products.
5. To clear novelty later, intersect actual candidate support with published same-purpose site/EZ/landing footprints, inspect native local evidence and relevant literature/supplements, then record exactly what is new (site, use, or combination). No exact-site clearance is inferred from an unreturned search hit. Do not invent another coordinate merely to claim novelty.

## Search scope and sources

This was a bounded public-web review of literal coordinate pairs and regional purpose terms, including NASA/LPI proposals, USGS records, provider documentation and accessible primary papers. Literal searches often returned unrelated numerical tables; those results were **not** treated as evidence of absence. It was not a systematic ADS/Scopus/non-English review or a complete spatial overlay of all proposals. The full 2015 abstract collection exceeded the web tool's size limit; its whole contents were not inspected. The IOP full text for [S1] was inaccessible; its author/institutional USGS abstract was used. Uninspected geological footprints remain unchecked.

| Ref | Primary source and inspected scope |
|---|---|
| S1 | Courville et al. (2026), [Subsurface water ice mapping on Mars: A probabilistic approach](https://www.usgs.gov/publications/subsurface-water-ice-mapping-mars-a-probabilistic-approach), [DOI](https://doi.org/10.3847/PSJ/ae8904). USGS author/institutional abstract: existing midlatitude ice-resource research; not the source of our consistency values. |
| S2 | Stuurman et al. (2016), [SHARAD detection and characterization of subsurface water ice deposits in Utopia Planitia](https://doi.org/10.1002/2016GL070138). Primary article: regional deposits, not a verified overlay with I-03/I-05. |
| S3 | Gallegos & Newsom (2015), [A human exploration zone in the Protonilus Mensae region of Mars, abstract 1053](https://www.hou.usra.edu/meetings/explorationzone2015/pdf/1053.pdf), pp. 1–2: center, ISRU motivation, approximately 100 km ROIs. |
| S4 | Orgel et al. (2019), [Grid mapping…water- and ice-related landforms in Acidalia Planitia](https://doi.org/10.1029/2018JE005664), §2.1: 300 km-wide study strip at 22.5°W. Regional precedent; exact cell overlap not asserted. |
| S5 | Tian et al. (2024), [Martian dust storm spatial-temporal analysis of tentative landing areas](https://doi.org/10.1029/2024EA003634), §2.1 and Figures 5–7: dust monitoring circles and separate candidate landing constraints. |
| S6 | Viúdez-Moreiras et al. (2020), [Effects of a large dust storm…InSight in Elysium Planitia](https://doi.org/10.1029/2020JE006493), abstract / §6: regional dust-operations precedent; observations at InSight. |
| S7 | NASA/JPL/USGS, [Hellas Planitia](https://www.jpl.nasa.gov/images/pia00416-hellas-planitia/): existing basin dust-storm context. Not a local operations-site certification. |
| S8 | Planetary Science Institute, [Thermal inertia](https://se.psi.edu/inertia/), interpretation and uncertainty sections: mixed surface materials; TI does not uniquely identify bedrock. |
| S9 | Cushing & Titus (2008), [MGS-TES thermal inertia study of the Arsia Mons Caldera](https://doi.org/10.1029/2007JE002910), §2.1 / Table 2: thermal/material ambiguity. Method context, not evidence collected at F-01–F-05. |
| S10 | Kargel & Dohm, [Proposed landing site for Mars Science Laboratory: Southern Argyre Planitia](https://marsoweb.nas.nasa.gov/landingsites/msl/workshops/1st_workshop/abstracts/Kargel_1st_MSL_workshop.pdf), primary workshop abstract: regional exploration precedent; no confirmed F-05 footprint overlap. |
| S11 | Montabone/LMD, [Climatologies of Martian atmospheric dust optical depth](https://www-mars.lmd.jussieu.fr/mars/dust_climatology/): reconstructed 3° dust scenarios, method and citations. Local processing/source hashes: [Mars profiles](../outputs/mars_profiles/profiles.json) and `analog/stack.py` (read only). |
| S12 | SWIM team, [SWIM overview](https://swim.psi.edu/about.php?section=overview): source-team mapping purpose. The local <1 m definition comes from the selected SWIM 2.0 product and stack metadata. |
| S13 | NASA/JPL, [InSight landing-site press kit](https://www.jpl.nasa.gov/news/press_kits/insight/landing/mission/landing-site/): approximately 4.5°N, 135.9°E center, used solely for context-distance checks. |

No new ranking, `analog/` edit, source-image download or Earth data processing was performed for this handoff. The supplied PNGs were visually inspected. Checks cover values copied from JSON, links, provenance and unchanged source files; they do not constitute physical site validation.

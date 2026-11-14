# Team 2: Same-purpose research and novelty audit

Team zasa. Review date: **2026-11-14, Asia/Taipei**. Phase 1 repository baseline: `3e3ffff`; Phase 2 main baseline: `263269a`. Scope: literature and proposal checks for I-01, I-02, D-03 and D-04, followed by the supplied Earth candidate EARTH-UV-001. No new site selection, Earth pairing, environmental validation or ranking.

## Decision for Team 1

**All four Mars candidates have related prior research. No exact-footprint, same-purpose Mars site proposal was verified in this bounded search. None is cleared as new or understudied.** These statements describe different checks: regional research is established; exact proposal overlap remains unresolved.

| ID | Classification | Exact-site / same-purpose result | Handoff |
|---|---|---|---|
| I-01 | Related research exists | No verified proposal hit; proposal inventory incomplete | Retain only as a conditional shallow-ice research candidate. Prior SWIM reconnaissance already covers this longitude/latitude sector. |
| I-02 | Related research exists | No verified proposal hit; proposal inventory incomplete | Same treatment. The inspected Deuteronilus and Protonilus exploration zones are geographically separate. |
| D-03 | Related research exists | No verified dust-observation or equipment-test site proposal in this nominal cell | Existing eastern Hellas geological mapping encompasses the nominal coordinates. Keep as a context reference; withdraw any unstudied-terrain claim. |
| D-04 | Related research exists | No verified exact-cell operations proposal; published dust-study footprints remain unresolved | Cerberus/Elysium dust sources, sinks and surface changes are established research topics. Keep as a context reference; withdraw any newly identified dusty-region claim. |

Classification vocabulary: `same_use_exists` = 已有相同用途, requiring both compatible footprint and explicit purpose; `related_research_exists` = 已有相關研究; `not_found_in_this_search` = 本次搜尋未找到, always bounded by the logged search; `insufficient_data` = 資料不足. A related-research classification does not establish an exact same-use proposal. The exact-site proposal status remains `insufficient_data` for the four Mars candidates. This is not a claim that no such proposals exist. The Earth review below distinguishes a verified valley-scale use precedent from an unresolved exact station/vicinity footprint.

**Phase 2: first supplied Earth candidate reviewed.** Git fetch found `outputs/research/team1_earth_analog_candidates.csv` on `team1/earth-analog-first-case-2026-11-14` at `5efa19766342a5a9ab24fcbbe3dbf02ed05805a6`, not on main. It contains only **EARTH-UV-001 → I-01**. University Valley already has Mars-analog drilling, depth-segmented sampling and thermal-control research. This is a material same-use precedent for Team 1 to assess. Exact overlap with station W and the complete proposed interface-detection/ice-loss protocol is unverified. Earth candidates for I-02, D-03 and D-04 are **waiting for Team 1's list additions**. No older Jezero/Gale/Arcadia Earth matches were substituted.

## Phase 2: EARTH-UV-001 → I-01

### Fixed input and source identity

Read both Team 1 files directly from the fetched commit, without checking out, merging or modifying that branch:

- [Candidate CSV at the reviewed commit](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/5efa19766342a5a9ab24fcbbe3dbf02ed05805a6/outputs/research/team1_earth_analog_candidates.csv), SHA-256 `4a901e4bc2625dc516018cb468a35fdecf5574736b378545448059020db12e8b`.
- [Team 1 research handoff at the reviewed commit](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/5efa19766342a5a9ab24fcbbe3dbf02ed05805a6/docs/research/team1_earth_analog_matching.md), SHA-256 `dc25c4d609ed5b9332567758c25680e14b1b1fb332cac4cb9c9ab6356ea9c5f4`.

ID **EARTH-UV-001**, associated Mars ID **I-01**. Site: **University Valley meteorological station W vicinity**, Antarctica. Earth anchor **−77.862150°, 160.710100°E**, retained exactly as supplied. This is a station reference, not a specified new borehole. No polygon or vicinity radius was supplied; the inspected coordinate passage does not state the horizontal datum.

Original CSV purpose, unchanged: `辨識乾覆土下冰膠結界面；驗證分段取樣升溫與冰損失。研究提議，尚未執行。` English reading: identify the ice-cemented interface below dry overburden and evaluate heating and ice loss during segmented sampling; proposed research, not performed. The handoff additionally proposes blind probe interpretation followed by physical sampling. No new pairing or replacement site is proposed here.

### Finding: substantial use precedent, exact joint protocol unresolved

**Anchor-level classification: related research exists. Valley-level component-use status: same use exists. Complete protocol at the W-station vicinity: insufficient data. Novelty is not cleared.**

| Part of Team 1's proposed use | Existing work actually supports | Spatial / methodological boundary |
|---|---|---|
| Dry overburden and an independently known ice interface | Marinova et al. (2022) locate the meteorological station at the supplied coordinate and instrument the 42 cm boundary [U1]. | Direct station-level study. This establishes earlier characterization, not blind interface-detection accuracy or current conditions. |
| Mars-analog segmented drilling and temperature control | Paulsen et al. (2011) report a 2010 University Valley field trial through dry soil into ice-cemented ground, using 10 cm sampling intervals and bit-temperature feedback [U2]. | Explicit same-use components at the named valley. Reported drill coordinates differ from W; no borehole overlap is inferred. |
| Sampling while limiting phase changes | Zacny et al. (2013) explicitly describe short sampling bites intended to prevent thawing/phase changes [U3]. | Publisher abstract supports the engineering purpose. Full paper access was restricted; this is not an exact-W experiment or a measured ice-loss curve. |
| Automated drilling and sample transfer | Glass et al. (2013) discuss University Valley among field sites and integrated operations [U4]. | Its detailed 2012 results are from Haughton; Antarctic repetition is described as planned in the Results section. Do not transfer those outcomes to W. |
| Delivery yield and sublimation-related sample handling | Steel et al.'s 2017 NASA Ames abstract uses University Valley soil in laboratory sample-delivery tests [U5]. | Prepared dry/frozen material in a chamber, not a W-station field test. Sublimation-related clogging is listed as further work, not a demonstrated completed ice-loss experiment. |

The original task is therefore partly an established experimental use of this valley. A new label or the association with I-01 does not establish a new site or first use. Conversely, the inspected literature does not prove that the full combination of blind interface detection, ground-truth depth error and a quantified sample ice-mass balance has already been executed at W. The correct result is a component-level use overlap with an unresolved complete-protocol check.

### Footprint and coordinate check

U2 reports its ice-cemented-ground drill at **77°51.891′S, 160°48.029′E**, converted to **−77.864850°, 160.800483°E**. The W anchor is **77°51.729′S, 160°42.606′E** [U1]. A spherical-Earth haversine check, **R = 6,371 km**, gives an approximate separation of **2.13 km**. This calculation uses the printed coordinates; it does not resolve their unreported datums, possible transcription issues, or field-survey accuracy.

This demonstrates that the published coordinate strings are different. It does not establish whether the earlier borehole is inside Team 1's undefined “vicinity,” nor whether a new experimental plot overlaps older work. Do not move EARTH-UV-001 to the U2 borehole or transfer the station's 42 cm interface to it. Formal footprint clearance requires Team 1 to define a plot/polygon or radius and prior studies' actual sampling extents.

### Research differences worth specifying, subject to Team 1's decision

These are proposed refinements within the supplied use, not established new methods:

1. Define the **blind detection protocol** and held-out ground truth: who predicts the boundary, which observations are withheld, and how depth errors and missed boundaries are measured. The station study is a reference dataset, not proof of this new protocol's accuracy.
2. Separate **bit temperature, recovered-sample temperature and ice mass loss**. An above-freezing limit or a subzero bit reading does not quantify retained ice. Specify initial/final ice measurements, handling time, repeatability and a closed mass balance before reporting ice-loss results. Review U3's full text and later sample-delivery work before calling this protocol novel.
3. State which unresolved **I-01 measurement requirement** the test would inform. No inspected source established a specific historical I-01 ↔ W pairing, but that bounded non-finding cannot establish novelty. Earth field results still require environmental modeling/chamber validation before any Mars performance inference.

**Team 1 action requested:** treat University Valley as a known Mars drilling/sampling analog. Decide whether to retain it as a validation/reference site with a precisely specified additional question, or propose a different candidate through Team 1's own process. Keep EARTH-UV-001 unchanged while that decision is pending. This audit does not select a replacement or certify the site unsuitable.

**Prohibited claims:** first Mars drilling analog in University Valley; previously unused dry-soil/ice-cemented site; first segmented thermal-control sampling; confirmed full-protocol novelty; previous field tests at the exact W borehole; measured ice loss or drilling performance at I-01. No number in Team 1's climate/environment extraction was reprocessed or independently validated by this literature audit.

### Earth sources and inspected scope

Search/access date: **2026-11-14, Asia/Taipei**. Source IDs U1–U5 belong to this audit; Team 1's E1/E5 labels are retained only in its own files.

| Ref | Original source | Material inspected / actual support |
|---|---|---|
| U1 | Marinova et al. (2022), [Climate and energy balance of the ground in University Valley, Antarctica](https://doi.org/10.1017/S0954102022000025) | Public full-text Introduction and Methods, meteorological measurements. Independently checked station coordinate and interface instrumentation. No claim of blind boundary testing. |
| U2 | Paulsen et al. (2011), [Field testing of the Icebreaker Mars drill in the Antarctic, LPSC 1901](https://www.lpi.usra.edu/meetings/lpsc2011/pdf/1901.pdf) | Both pages, especially the first field-test section. Explicit valley, drill location and thermal/segmented-sampling procedure. Includes a separate massive-ice trial; it is not the W plot. |
| U3 | Zacny et al. (2013), [Reaching 1 m Deep on Mars: The Icebreaker Drill](https://journals.sagepub.com/doi/10.1089/ast.2013.1038), doi:10.1089/ast.2013.1038 | Publisher abstract and contents only. Short bites and phase-change control are explicit; full text/PDF unavailable. Related to U2's hardware program, not an independent field campaign count. |
| U4 | Glass et al. (2013), [Planetary-prototype drilling and sample acquisition tests at analog sites, LPSC 1334](https://www.lpi.usra.edu/meetings/lpsc2013/pdf/1334.pdf) | Both pages, Field Test Sites and Results. Distinguishes Haughton results from planned Antarctic repetition. |
| U5 | Steel et al. (2017), **Testing A Sample Delivery System for Planetary Surface Missions**, [NASA Ames Jamboree 2017 abstract collection](https://ntrs.nasa.gov/api/citations/20200001147/downloads/20200001147.pdf?attachment=true), printed p. 92 / PDF page 93, PS.1 | Downloaded public NASA PDF and extracted this abstract locally after web-section requests timed out. Material provenance, sample handling and further-work section inspected. NTRS accession year 2020 is not the 2017 meeting year. University Valley material does not establish W provenance. |

### Earth search log and remaining scope

The following exact queries were submitted on 2026-11-14 (Asia/Taipei):

| Group | Queries | Outcome |
|---|---|---|
| Q07 | `University Valley Antarctica Icebreaker drilling ice sampling heating sublimation 2013`; `University Valley station W ice cemented soil drilling Icebreaker 42 cm` | U1/U2/U4 and the existing U3 lead. |
| Q08 | `"University Valley" "ice loss" drill`; `"University Valley" "drill" "77" "51"`; `"University Valley" "thermal" "probe" ice table drilling sample heating` | Located explicit field-drill context and further thermophysical work; no exact-W full protocol verified. |
| Q09 | `"Reaching 1 m Deep on Mars" PMC`; `"University Valley" "thermal probe" "ice" drilling`; `"University Valley" "sublimation" "Icebreaker" samples loss` | U3 publisher record and U5 laboratory-delivery precedent. |

Directly opened Team 1's U1/U3 DOI leads, U2/U4 abstracts, and U5 NASA PDF. U3 DOI/PDF requests timed out; its publisher HTML abstract was accessible. PubMed returned only a footer and supplied no usable abstract in this session. A snow/salt ice-stability lead at `PMC7430506` returned a browser check on direct access; it was not used to establish a completed sampling experiment. A separate NASA water-rich mission PDF returned 403. Search excerpts/secondary news were not used as proof of full-paper or exact-site inspection.

This is a bounded public-web review of one supplied candidate. No exhaustive ADS/Scopus search, full U3 methods/supplement review, later citation-chain review, or spatial intersection of every historical borehole was completed. The absence of a supplied vicinity polygon and a completed mass-balance protocol limits the exact-use conclusion. University Valley and Beacon Valley are related search contexts, not interchangeable experimental coordinates.

CSV schema update: four original Mars rows are retained; one Earth row is appended with `candidate_id=earth_candidate_id=EARTH-UV-001`, `mars_candidate_id=I-01`. Earth coordinates occupy the explicit `earth_lat_deg`/`earth_lon_east_deg` fields; Mars planetocentric and nominal-box fields are blank for that row. `site_level_same_use_status=same_use_exists` records the valley-level precedent, while `classification=related_research_exists` and `exact_site_same_use_status=insufficient_data` describe the unresolved W-vicinity footprint. `verified_same_use_hit_found` remains an exact-footprint flag, not the valley-level status.

## Inputs and completed checks reused

Read the current repository copies of [site_discovery_brief.md](../site_discovery_brief.md), [mars_discovery_handoff.md](../mars_discovery_handoff.md), [mars_discovery_novelty_checks.csv](../mars_discovery_novelty_checks.csv), and [mars_discovery_search_scope.json](../mars_discovery_search_scope.json). The original 15-row review already covered literal coordinate queries, regional precedents, Protonilus and InSight center distances, and the D-01/D-02 Utopia monitoring-circle overlap. Those are inherited checks, not new discoveries in this audit.

The requested filename `ice_candidate_followup_2026-11-14.md` was not found in the current checkout. The supplied `NASA_Space_Apps_2026_All_Data.xlsx` contains its apparent successor as an English rendering of **`docs/research/ice_candidate_followup/README.md`**, in `Report Text!A475:G505`, with supporting search records in `JSON Source Records!A20680:H20730`. Read all these records. They document native-grid QA, the nominal 2015 latitude/radius envelope, Luzzi et al.'s AP-1/AP-8/AP-9 checks, Protonilus ice-exposing craters, and unresolved actual proposal footprints. These checks were reused without rerunning data processing. The original Markdown is authoritative and is absent from this checkout; the workbook is a supplied snapshot, not a replacement original.

Workbook identity: snapshot `2026-11-14T15:42:59.879915+08:00` (`Overview!A4`); SHA-256 `a789fcdc9c0a7e780f85b63687ad54f05b87cd6e341ecf024375dcd6fcb3f731`. `Earth Candidates` contains 72 versioned rows: 36 for `earth_100km_sample4km` and 36 for `earth_100km_sample10km`. These are older Jezero/Gale/Arcadia results, not 72 independent new analog sites. The workbook was read only and was not copied into Git.

## Spatial interpretation

The stored Mars centers use planetocentric latitude and east-positive longitude. For the Mars audit, a **nominal cell** means center ±0.25° in both axes, inferred from the documented 0.5° grid. It is not a landing ellipse or a verified instrument footprint. The Earth anchor has separate coordinate fields and no assumed cell footprint.

| ID | Latitude bounds, degrees | East longitude bounds, degrees | Search labels, not certified site boundaries |
|---|---:|---:|---|
| I-01 | 54.00 to 54.50 | 1.00 to 1.50 | Northern plains / Vastitas Borealis; eastern Acidalia context; Ismenius Lacus context |
| I-02 | 53.50 to 54.00 | 42.00 to 42.50 | Northern plains / Ismenius Lacus; Lyot, Protonilus and Deuteronilus regional terms |
| D-03 | -46.50 to -46.00 | 82.50 to 83.00 | Eastern Hellas Planitia / basin floor and rim |
| D-04 | 7.50 to 8.00 | 154.00 to 154.50 | Elysium Planitia / Cerberus plains and classical Cerberus albedo feature |

Slope/relief cell support, interpolated SWIM support, and the dust layer's native 3° support are different. In particular, a dust study outside a nominal 0.5° cell may still overlap the broader atmospheric context. No native dust-contribution polygon was reconstructed here. No complete GIS overlay of study/ROI/landing polygons was completed.

Center distances below are geometric calculations, using a Mars sphere of radius **3,396 km** and the haversine formula `2R atan2(sqrt(a), sqrt(1-a))`, where `a = sin²(Δlat/2) + cos(lat1) cos(lat2) sin²(Δlon/2)`. They are rounded context checks; source datum differences were not rigorously transformed. They cannot exclude uninspected alternative sites or extended ROIs.

## Candidate findings

### I-01: 54.25°N, 1.25°E

- **Already observed/studied:** SWIM's published 2019 reconnaissance domain includes this sector [N1]. This establishes prior ice-resource mapping context, not a local independent ice detection. Reusing its product does not make this a newly discovered ice deposit.
- **Proposal check:** the inspected Deuteronilus exploration zone explicitly combines science and ice-resource use [N2]. Its center, 39.11°N, 23.199°E, is approximately **1,255.5 km** away; the stated primary circle has a 100 km radius. Its alternative EZs in Figure 2 were not digitized. The inherited Protonilus separation is approximately 1,939.6 km [N3].
- **Scope correction:** Orgel et al.'s Acidalia geomorphological survey is a 300 km strip centered on **22.5°W**, extending 20°N to 84°N [N4]. That regional citation does not establish imagery interpretation or ice landforms at 1.25°E. No local landform was assigned from it.
- **Possible research difference:** compare follow-up observations needed here with I-02, where the existing descriptors show similar ice consistency and slope but different TI. A documented comparison of missing evidence could add value. This is a proposed question, not a novelty finding or extraction-performance result.
- **Cannot claim:** first ice-resource proposal, an unstudied area, confirmed shallow ice, extractable water, or a suitable crewed base. The inherited nominal 2015 envelope exclusion also reflects historical latitude constraints [N5].

### I-02: 53.75°N, 42.25°E

- **Already observed/studied:** the same published SWIM reconnaissance domain applies [N1]. The specific candidate selection is a project interpretation of an existing reconnaissance product.
- **Proposal check:** the already reviewed Protonilus proposal is at **42.187°N, 48.062°E**, approximately **722.5 km** away, with resources/ROIs described around its habitation zone [N3]. The newly inspected primary Deuteronilus circle is approximately **1,158.2 km** away [N2]. These named proposals are not this nominal cell. Their existence establishes a related ice-resource use in the wider region, not exact duplication.
- **Remaining uncertainty:** no complete set of alternative Deuteronilus sites, later prospecting proposals or their actual ROI polygons was obtained. Nearby Lyot/Ismenius search terms did not establish an exact same-use proposal. The already checked Protonilus ice-exposing craters remain separate observations, not measurements at I-02.
- **Possible research difference:** test which observation would resolve the ambiguity between surface thermophysical context and the inferred subsurface ice resource at this specific cell, using I-01 as a comparison. Any Earth experiment must wait for Team 1's explicit pairing and use.
- **Cannot claim:** the Protonilus EZ, a validated alternative to it, first ice-prospecting site, independent confirmation from multiple SWIM depth maps, or demonstrated lower drilling cost.

### D-03: 46.25°S, 82.75°E

- **Already studied:** the USGS SIM 3096 publication record describes mapping of **37.5°S to 47.5°S, 270°W to 280°W** [N6], equivalent to 80°E to 90°E. The nominal candidate box is numerically inside that published extent. This is geological mapping coverage, not a dust-test recommendation. The full sheet/pamphlet could not be retrieved, so no unit or landform was assigned to this cell. Astropedia's indexed geometry appears to show only one northern quadrangle; it was not substituted for the publication's four-quadrangle extent.
- **Dust footprint check:** Szwast et al.'s Hellas dust/albedo ROI is **31°S to 53°S, 54°E to 82°E** [N7, §5.3/Figure 9]. The nominal cell begins at 82.5°E and is outside that particular ROI, despite sharing the basin name. The coarser atmospheric support may overlap; its seasonal result was not transferred to D-03.
- **Proposal check:** Rice et al.'s eastern Hellas human-exploration proposal has a **200 km diameter** zone near **40°S, 104°E**, approximately **987.3 km** away [N8]. Its purpose includes geological/ice-resource exploration, not an equipment dust-tolerance test at D-03.
- **Possible research difference:** define this eastern-basin cell as an explicit contrast in a seasonal dust-column/terrain comparison, then check the difference against local transport observations. Neither such a result nor an unclaimed prior use is established yet.
- **Cannot claim:** unstudied Hellas terrain, a new dust source/hotspot, locally measured deposition/abrasion, equipment suitability, or a safe operating surface.

### D-04: 7.75°N, 154.25°E

- **Already studied:** Geissler [N9, §4.4] examines dust deposition/erosion in classical Cerberus around **10°N, 205°W = 155°E**, approximately **140.4 km** from D-04. The study covers an extended feature, not just that center; a center mismatch cannot exclude overlap. Its actual changed-surface polygon was not obtained.
- **Closely related research purpose:** the 2018 Elysium study [N10] proposes relating dust sources/sinks to terrain types using thermal-image differences. Thus, comparing dust and terrain in Elysium already has methodological precedent. Its exact image/ROI overlap with D-04 remains unverified. This is an abstract describing work and next steps, not a completed validation of D-04.
- **Further prior work:** Wolfe et al. [N11] combine diurnal EMIRS temperatures and modeling to constrain dust redistribution over an Elysium ROI. The inspected text/Figure 2 caption does not provide a usable numeric D-04 polygon. None of its regional dust-thickness estimates is assigned to this point.
- **Operations-footprint check:** Yao et al.'s Tianwen-1 monitoring circle is centered at **17°N, 107°E**, radius **2,000 km** [N12]. D-04 is approximately **2,782.8 km** away, so its nominal cell is outside that circle. This excludes only that monitoring footprint, not all Elysium operations studies. The earlier InSight site separation is inherited from the handoff; its observations are not ground truth here.
- **Possible research difference:** explicitly separate atmospheric column dust from surface dust transport for this candidate and compare their seasonal behavior. That physical distinction is established in prior work; a contribution would require a new, reproducible candidate-specific result.
- **Cannot claim:** first dust/terrain study, newly discovered dusty region, InSight-validated conditions here, or proved absence of prior operational interest.

## Sources and what was actually inspected

All access/search dates below are 2026-11-14 (Asia/Taipei). References identify author research or official records, not agency endorsement of these candidates. Broadly relevant works found in search results were not treated as exact-site evidence.

| Ref | Source | Inspected material and supported scope |
|---|---|---|
| N1 | Putzig, Morgan & SWIM team (2022), [LPSC abstract 2443](https://www.hou.usra.edu/meetings/lpsc2022/pdf/2443.pdf) | Two-page abstract, Introduction/Motivation. Stated 2019 domain: 0 to 60°N and 0 to 225°E, 290 to 360°E; resource reconnaissance supports future missions. Domain membership is not local detection or a selected landed site. |
| N2 | Head et al. (2015), [Deuteronilus EZ, abstract 1033](https://www.hou.usra.edu/meetings/explorationzone2015/pdf/1033.pdf) | Both pages, primary EZ center and Figure 1 radius. Same broad resource purpose at a separate primary zone; Figure 2 alternatives remain unresolved. |
| N3 | Gallegos & Newsom (2015), [Protonilus EZ, abstract 1053](https://www.hou.usra.edu/meetings/explorationzone2015/pdf/1053.pdf) | Existing checked lead reopened for spatial comparison; both pages, proposed center and ROI discussion. No claim that its resources extend to either ice candidate. |
| N4 | Orgel et al. (2019), [doi:10.1029/2018JE005664](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2018JE005664) | §2.1 study-area definition. Narrows the geographic relevance of an inherited Acidalia citation. |
| N5 | Hoffman & Bussey (2016), [NASA NTRS 20160001040](https://ntrs.nasa.gov/citations/20160001040) | Official abstract reopened; full-paper nominal-envelope analysis inherited from the supplied follow-up. 47 workshop proposals, ±50° criterion and approximately 100 km EZ definition do not constitute a complete modern site inventory. |
| N6 | Bleamaster & Crown (2010), [USGS SIM 3096](https://doi.org/10.3133/sim3096), [publication record](https://pubs.usgs.gov/publication/sim3096), [Astropedia record](https://astrogeology.usgs.gov/search/map/mars_geologic_map_of_mtm_40277_45277_40272_and_45272_quadrangles_eastern_hellas_planitia_region) | Indexed official publication abstract/metadata returned the full stated extent and 1:1,000,000 map scale. Direct pages and attempted pamphlet access returned 403. Extent comparison only; full map and coordinate-reference details unverified. |
| N7 | Szwast, Richardson & Vasavada (2006), [doi:10.1029/2005JE002485](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2005JE002485) | Full-text abstract and Hellas §5.3/Figure 9 text. Explicit ROI bounds enable a nominal-box exclusion; basin-wide phenomena are not cell measurements. |
| N8 | Rice et al. (2015), [Eastern Hellas EZ, abstract 1038](https://www.hou.usra.edu/meetings/explorationzone2015/pdf/1038.pdf) | Entire one-page abstract; center, diameter and resource purpose. Regional proposal at a different location. |
| N9 | Geissler (2005), [doi:10.1029/2004JE002345](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2004JE002345) | §4.4/Figure 9 caption. Cerberus surface-change research near D-04; no digitized deposit or image polygon. |
| N10 | Kozdon et al. (2018), [LPSC abstract 2514](https://www.hou.usra.edu/meetings/lpsc2018/pdf/2514.pdf) | Both pages: Elysium ROI rationale, methods and proposed follow-up. Direct regional precedent for dust/terrain comparison; no numeric local polygon validated. |
| N11 | Wolfe et al. (2023), [doi:10.1029/2023JE007794](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023JE007794) | Abstract, §§2.2, 3.1, 4.1, Figure 2 caption and data-availability statement. Regional dust/thermal work, with uncertainties permitting zero net change. Exact D-04 support remains unchecked; original EMIRS products were not downloaded. |
| N12 | Yao et al. (2020), [doi:10.1029/2020EA001242](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020EA001242) | Figure 1 caption and §2.2: numeric monitoring circle, distinct from preferred landing areas. |

## Search log

Public-web search, 2026-11-14 (Asia/Taipei). Queries are grouped below but each string was submitted separately. Search output was screened for original papers, NASA/USGS records and formal abstracts. Commercial hits, games, Wikipedia, fictional Ares III material and unsupported aggregation pages were excluded. A failed literal query is not evidence of absence.

| Group | Candidate / purpose | Exact submitted queries |
|---|---|---|
| Q01 | I-01 and northern-plains resources | `Mars "54" "1" Acidalia ice exploration zone landing site`; `site:hou.usra.edu explorationzone2015 "Acidalia"`; `Mars "54" "0" "ice" landing site Acidalia`; `site:hou.usra.edu/meetings/explorationzone2015 "Acidalia" ice`; `Mars ice "Acidalia" "0" "55"`; `Mars Acidalia eastern northern plains ice ISRU landing exploration zone Cydnus`; `"54" "1" "ice" "Acidalia" ISRU`; `"Acidalia" "ice" "landing" "site" -site:wikipedia.org -site:researchgate.net` |
| Q02 | I-02 and regional ice proposals | `Mars "53" "42" ice exploration site Deuteronilus Protonilus`; `site:hou.usra.edu explorationzone2015 "ice" "Deuteronilus"`; `Mars "53.75" "42.25"`; `Mars "54" "42" "ice" Vastitas`; `Mars Lyot northern plains ice prospecting Ismenius human landing site`; `site:hou.usra.edu "Ismenius" "ice" "exploration"`; `"53" "42" "ice" "Mars" landing`; `"Ismenius" "ice" "landing" site:hou.usra.edu` |
| Q03 | Ice-method / proposal leads | `"Mars Water Ice Prospecting" "pdf" NASA`; `"Subsurface water ice mapping" "0" "60" "2021"` |
| Q04 | D-03, Hellas | `Mars Hellas "82" dust storms landing site`; `"Hellas" "explorationzone2015"`; `"Mars" "82.75" dust`; `Hellas basin dust monitoring terrain landing site study eastern floor`; `"Geologic map" "Eastern Hellas" "37.5" "47.5"`; `"Hellas" "dust" "46" "83" study`; `"Hellas" "dust" "82" "46" Mars operations` |
| Q05 | D-04, Elysium/Cerberus | `Mars "154" "8" Elysium dust landing site`; `"Elysium" "explorationzone2015"`; `"Mars" "154.25" dust`; `Elysium Cerberus plains dust monitoring deposition study landing site 150 east`; `"Elysium" "dust" "154" study` |
| Q06 | Explicit surrounding-area queries | `Mars northern plains Vastitas Borealis eastern Acidalia shallow ice prospecting site 50 60 north 0 10 east`; `Mars Lyot Ismenius Lacus northern plains 50 60 north 40 east ice resource landing proposal`; `Mars eastern Hellas Planitia dust column terrain operations 40 50 south 80 90 east site`; `Mars Cerberus Elysium Planitia 5 10 north 150 160 east dust monitoring operations proposal` |

Q01/Q02 returned regional leads, including N1/N2/N4 and a 2025 Acidalia rampart-crater abstract; no exact same-use site was verified. Q03 returned Phlegra-focused prospecting reports and SWIM; Phlegra reports were screened as different-region leads and were not used to assign a site overlap. Q04 returned N6/N7/N8. Q05/Q06 returned N9/N10/N11/N12. Literal coordinate results were often unrelated numerical matches. The source table records what was inspected beyond search output.

Additional bounded source inspection: Deuteronilus 1033, Protonilus 1053, Eastern Hellas 1038, Ismenius Cavus 1027 and Apollinaris Sulci 1043 abstracts were opened. The latter two did not establish overlap with these candidates. LPSC 2025 abstract 2282 was inspected as regional cryosphere research; its individual crater polygons were not checked. The 2024 Tianwen-3 paper `10.1029/2024EA003634` was reopened as a dust-operations precedent; no new exact candidate overlap was established. SWIM pilot and northern-hemisphere product pages were reviewed for domain context, without treating different releases as interchangeable. No complete workshop abstract inventory, ADS/Scopus search, non-English review, instrument-image catalog search or systematic citation chaining was performed.

Access limitations: the 2015 program page could not be retrieved; USGS SIM 3096 and Astropedia direct access returned 403; the 2011 USGS mapping abstract-volume request timed out; a NASA-hosted Cerberus landing abstract request timed out; a Hellas dust-dynamics publisher page returned 403. The USGS mirror of Geissler failed, but publisher full text was accessible. Wolfe publisher access initially failed and succeeded on retry. These failures were not interpreted as absent prior work. No conclusions depend on inaccessible full-map units or unseen supplements.

## Remaining work and handoff checklist

- [x] Reuse the prior 15-point review and supplied ice follow-up instead of presenting them as new work.
- [x] Check all four fixed Mars IDs with regional names, surrounding-area terms and use keywords.
- [x] Separate observations, regional research and explicit site proposals; record source scope and access failures.
- [x] Record nominal boxes and bounded spatial comparisons; no novelty clearance from center mismatch.
- [ ] Obtain actual alternative EZ/ROI, changed-surface and EMIRS ROI geometry where overlap is unresolved. Normalize coordinate conventions before formal intersections.
- [ ] Complete a broader modern same-use proposal inventory before any first-use or understudied claim.
- [ ] Team 1 to evaluate the regional purpose precedents, particularly the Elysium dust/terrain precedent. No exact duplicate requiring automatic replacement is established; keep/change decisions belong to Team 1.
- [x] Read Team 1's first candidate from its uploaded branch and audit EARTH-UV-001 under its original ID, coordinates and purpose.
- [ ] **Team 1 decision pending:** University Valley has existing drilling/segmented thermal-control use. Retain as a known reference with a precise additional protocol, or revise through Team 1's process. W-vicinity bounds and exact full-protocol overlap remain unresolved.
- [ ] **Waiting for Team 1 additions:** Earth candidates for I-02, D-03 and D-04 in `outputs/research/team1_earth_analog_candidates.csv`. Require fixed IDs, coordinates, footprints, intended tests and original evidence links.

Companion machine-readable file: [team2_novelty_audit.csv](../../outputs/research/team2_novelty_audit.csv), four Mars records and one Earth record. `novelty_cleared=false` is a research status, not a rejection of the candidate's future usefulness.

Verification: the original four Mars IDs/coordinates were checked against the repository novelty CSV and supplied workbook. Phase 2 checks cover the appended Earth record against the pinned Team 1 CSV, exact preservation of its purpose text, distinct Earth/Mars coordinate fields, unchanged prior Mars findings, CSV structure, source-reference completeness and local report links. Numeric distances were independently calculated as described above. Only the two Team 2 deliverables were written. No `analog/`, ranking, Team 1 file, total workbook, README or website change was made. OpenAI Codex assisted literature screening, geometric context calculations and reporting; every external scientific claim is tied to the inspected source scope above.

# Mars Analog Finder

### Earth–Mars analog research · NASA Space Apps 2026 Taipei · Team zasa

Search open terrain data for Earth candidate regions, compare them with Mars targets, and expose the supporting evidence, missing data and limits of each analogy.

[Methods](docs/README.md) · [Candidate results](outputs/analysis/candidate_handoff.md) · [Website handoff](outputs/matching_handoff/README.md) · [Mars data](outputs/mars_profiles/handoff.md) · [Data guide](data/README.md) · [Contributing](CONTRIBUTING.md)

> Research pipeline and candidate-analysis prototype. Regional terrain results are available; validated four-theme scoring is unfinished. A teammate has built a local prototype in `web/`; public deployment has not been verified in this work log. This repository does not establish NASA endorsement or completed competition submission. Earth–Mars-only scope is a locked team decision.

## Results

![Terrain candidate search, not overall Mars similarity](outputs/analysis/figures/candidate_map.png)

Candidates come from sparse regional terrain screening and require further environmental, geological and prior-literature verification. The map does not establish landing safety, novelty or mission success.

| Workstream | Status | Evidence |
|---|---|---|
| Common physical-scale terrain comparison | Actual results available | [Method](docs/earth_pipeline.md), [candidates and limits](outputs/analysis/candidate_handoff.md) |
| Mars MOLA / TES / SWIM / dust context | Integrated | [Method](docs/mars_pipeline.md), [sources and values](outputs/mars_profiles/profiles.json) |
| Regional day/night temperature context | New coarse MCS time-corrected derivative; unscored and metadata incomplete | [Source, extraction and remaining gaps](outputs/mars_regional_temperature/README.md) |
| Rover day/night brightness temperature | Exploratory; incomplete quality support | [MEDA method](docs/mars_temperature.md), [quality summary](outputs/mars_temperature/summary.json) |
| Multi-theme Earth raw data | Teammate inventory; complete batch not on this machine | [Inventory](docs/earth_inventory.csv), [handoff](docs/data_handoff.md) |
| Four-theme scoring and field-site validation | Unfinished | [Quantity comparison](docs/cross_reference.md) |
| Interactive workbench | Local prototype; public deployment unverified here | [web/](web/); latest Matching export not automatically integrated |
| English presentation and official submission | Drafts available; completion unverified | [Submission preparation](docs/submission/preparation.md) |

## Run locally

Python 3.11 or later is required; previous runs used Python 3.12. Run from the repository root:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m scripts.profile_mars --strict
.venv/bin/python -m scripts.process_mars_temperature
.venv/bin/python -m scripts.export_matching_handoff
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
```

Existing Mars inputs and outputs are versioned. Processing commands rebuild their outputs; use the linked files directly when reading results. `--strict` checks core grid inputs, not MEDA quality acceptance.

Earth screening additionally needs ETOPO and the land mask; see [Earth execution](docs/earth_pipeline.md). Some Earthdata products require an account. Never commit credentials. [requirements-lock.txt](requirements-lock.txt) records the tested environment; cross-platform installation still requires verification.

```text
analog/       Scientific readers, scale handling and analysis
scripts/      Download, processing, export and plotting entry points
tests/        Data and method checks
data/         Mars inputs and processed data; large Earth files handed off separately
outputs/      Candidates, provenance, sensitivity, profiles and figures
docs/         Methods, data contracts, submission drafts and historical records
web/          Reporting teammate's interactive prototype
```

See the [data guide](data/README.md), [output guide](outputs/README.md) and [file inventory](docs/repository_inventory.csv).

## Scientific boundaries

- Define comparison windows in kilometers using the appropriate planetary radius. Equal angular grids do not imply equal physical support; interpolation creates no new detail.
- MODIS kinetic LST, MEDA ground brightness temperature, POWER 2 m air temperature and TES thermal inertia are different quantities.
- SWIM consistency is not ice amount or probability. Permafrost fraction is not extractable ice. Low NDVI is not evidence of lifelessness.
- Earth 550 nm extinction AOT is not directly equivalent to Mars 9.3 µm absorption CDOD.
- Missing or quality-incomplete evidence cannot count as confirmed support. Similar terrain statistics do not establish matching geology, origin or mission suitability.

## Sources, rights and submission

Versions, units and processing are documented in the [method index](docs/README.md) and output manifests. Dust-derived material has [separate CC-BY-SA terms](outputs/mars_profiles/LICENSE-data.md). Other products retain their providers' terms. An original-code license remains pending team confirmation; Apache-2.0 is a proposal, not an adopted license.

[Official challenge](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/) · [Official terms](https://www.spaceappschallenge.org/legal/)

The official-repository Navigator reply supports preparing up to seven slides or a video of at most 30 seconds. The complete submission guide, account details and Taipei-specific requirements remain unverified. Drafts are not proof of submission. See the [remaining checklist](docs/submission/remaining_checklist.md). Historical scope questions are retained as audit records, not invitations to change the locked Earth–Mars focus.

## Work reports

Reports below preserve historical outcomes and limitations; a past status is not necessarily the latest status. Earlier source records and AI disclosures remain in the [pre-cleanup archive](docs/archive/README_before_cleanup_2026-11-14.md), [Earth work log](docs/work_report_2026-11-14.md) and [MEDA log](docs/mars_temperature.md). The six phase prompts were edited; that alone did not execute the six phases. Historical linked documents may still be in Chinese; this root README is English.

### 2026-11-14: Repository cleanup

Reorganized README and data/document/output navigation; created a file-purpose inventory and preserved history and AI disclosures in the archive. Removed rebuildable local caches without deleting scientific inputs, sensitivity comparisons, tests or provenance. The 10 km analysis remains a dependency of summary scripts.

At that point, the interface, four-theme selection and competition submission were unfinished. No reranking or scientific values changed. Outstanding items included licensing, complete rules, Earth handoff and MEDA flags. OpenAI Codex assisted inventory and documentation. Verification: 57 tests passed, eight existing warnings, Ruff passed, and new navigation/archive links checked.

### 2026-11-14: Three Earth candidate research records

Created the [research report](docs/research_report_three_analogs_2026-11-14.md) and [traceable evidence](outputs/research/three_candidate_evidence.json). The existing cases are Gale–39N,75E and Arcadia–29N,105W / 35N,57E: three Earth candidates and two Mars targets. Jezero candidates remain terrain references without claiming dry-environment suitability.

Recomputed three distances from stored features. Top-two retention across four tested configurations was 4/4, 3/4 and 2/4, not calibrated confidence. Geology, ice, novelty and logistics remained unresolved. No reranking or NASA certification. Reproduce with `python -m scripts.report_candidate_evidence`.

### 2026-11-14: Located sedimentary-rock evidence

Updated [report section 3](docs/research_report_three_analogs_2026-11-14.md). Three Bershaw et al. (2012) Oytag mudstone, sandstone and limestone sample points fell inside the eastern side of the 100 km candidate window. [Coordinates](outputs/research/oytag_literature_points.csv) and [spatial checks](outputs/research/oytag_overlap.json) are preserved.

This supports localized sedimentary-rock investigation. Gypsum was section-level evidence; exact outcrop, smectite and iron-oxide co-occurrence were unconfirmed. Marine/fluvial context cannot be equated to Gale's lake deposits. `python -m scripts.check_oytag_overlap` checked the three points against local ±50 km coordinates and the existing polygon. The source datum was unspecified, so the result is regional, not navigational. AI assisted literature review and calculations; no imagery or mineral measurements were fabricated.

### 2026-11-14: Teammate's local TerraMatch workbench

The Reporting teammate created `web/` with React 18, TypeScript and Vite. `web/scripts/build_workbench_data.py` and `web/src/data/adapter.ts` read the existing 4 km/10 km results, sensitivity, Mars profiles and MEDA summary without changing Matching inputs or rankings.

The teammate reported target switching with state reset, isolated Demo Mode, separate Earth/Mars coordinate diagrams, 12-candidate filtering and empty states, four-theme evidence views, source/hash drawers and four-configuration sensitivity. Displayed radii were Earth 6,371.0 km and Mars 3,396.0 km; approximate 100 km latitude spans were 0.90° and 1.69°. The lack of a Mars basemap was disclosed.

The teammate reported `npm run build:data`, TypeScript/Vite build and Ruff passing; browser checks at 1280×800 and 390×844 covered seven flows with no console errors or failed network requests. These are historical teammate-reported checks, not repeated by the later Matching export. Run locally with `npm install`, `npm run build:data`, `npm run build`, then Vite dev/preview. Antigravity assisted frontend work and testing. Ranks 3–12 lacked POWER context and regional Mars temperature remained missing.

### 2026-11-14: Approximate gypsum-bearing transect

[Report section 3.7](docs/research_report_three_analogs_2026-11-14.md) used Sun/Jiang (2013) Figures 2–3 to approximate an A–B transect. Endpoints and eight ±8-pixel diagnostic cases lay inside the candidate. This was map-based inference, not original gypsum GPS or precise geological overlay.

Preserved the [calculation](outputs/research/oytag_transect_check.json), [original schematic](outputs/research/oytag_transect_schematic.png) and [source audit](outputs/research/oytag_outcrop_source_audit.json). Thermomagnetic analysis, limestone Ca/Sr and nearby thin sections cannot substitute for same-outcrop gypsum XRD. Same-named sections cannot automatically be linked to one sample. The GPS–sample-ID–mineral chain and smectite co-occurrence remained unknown.

Executed overlap and transect checks and reviewed links/figures, without reranking or rerunning the full test suite. Codex assisted PDF interpretation and approximate spatial analysis; source PDFs were not redistributed.

### 2026-11-14: Original supplementary table

Obtained Bershaw (2012) `mmc1.xls` / Table DR1 and extracted ten PMR parent-rock coordinates and IDs inside the polygon. [Coordinates](outputs/research/oytag_supplement_coordinates.csv), [hashes](outputs/research/oytag_supplement_metadata.json) and [access log](outputs/research/oytag_supplement_access_log.json) are preserved; see [section 3.8](docs/research_report_three_analogs_2026-11-14.md).

The table is zircon-dating material, not gypsum GPS/XRD. Oytag sample `9412-1` concerns moraine and was excluded as same-outcrop evidence. Gypsum coordinates, unique ID, mineral analysis and Figure DR1 remained missing. Executed table decoding, unique-ID/coordinate/polygon and link checks. The optional reader was installed only temporarily; copyrighted Excel/PDF files were not redistributed. No reranking or full-suite rerun. Codex assisted source retrieval and extraction.

### 2026-11-14: Submission readiness audit

Created the [readiness report](docs/submission_readiness_2026-11-14.md), [53-item checklist](docs/submission_gap_checklist_2026-11-14.csv) and [snapshot](outputs/research/submission_audit_snapshot_2026-11-14.json): eight submission items, 31 quality priorities and 14 claim-dependent items, not 53 official requirements.

The teammate inventory contained 222 files / about 12.33 GB; the full raw batch was not available locally. Rankings remained terrain-only, with 12 candidates per target and POWER for the first two. The audit recommended an evidence-limited main case instead of an unsupported combined score. It identified research-bundle, local-verification wording and source-mapping issues for Reporting without editing the website; later teammate fixes must be assessed separately.

Read official annual/legal pages and the Navigator submission reply; complete challenge text, guide and Taipei details remained unverified. Tests: 57 passed, eight existing warnings; Ruff passed. No frontend, deployment or official submission check. Codex assisted the audit and documentation.

### 2026-11-14: Submission copy and research requirements

Prepared [official checks and English copy](docs/submission/preparation.md), [seven-slide text](docs/submission/slides_en.md) and [rights/AI/contribution forms](docs/submission/disclosures_and_rights.md). Account fields were left blank; Apache-2.0 remained a proposal. No login, message to organizers or submission occurred.

Added [one research question and five requirements](docs/research_scope.md), [CSV matrix](docs/research_requirements.csv), [literature review](docs/literature_review.md) and [claim ledger](docs/submission/claim_ledger.csv). Only terrain was quantitatively scored; environmental and same-outcrop conditions remained partial/unknown.

Executed `python -m scripts.validate_research_scope`: recomputed three Mars target signatures and Death Valley/Amazon reference windows from raw DEMs, matched stored Mars features and checked distance contributions. [Results and hashes](outputs/research/reference_terrain_check.json) show that Arcadia terrain can favor a low-relief contrast, illustrating that terrain distance does not establish complete environmental analogy. Two windows are not full external validation. No ranking, candidate geology or website changes.

English PDF/video, account checks, team licensing, systematic literature/reference validation, public access and SUBMIT remained unfinished. Tests: 57 passed, eight existing warnings; Ruff and nine-document local-link checks passed. No frontend/build/deployment/submission. Codex assisted specifications, checks and writing; text drafts were not final deliverables.

### 2026-11-14: Matching results and website handoff

Synced main before work. Exported [the English website handoff](outputs/matching_handoff/README.md) and [machine-readable matching data](outputs/matching_handoff/matching_data.json): 36 stored target–candidate records, six with POWER context, three Mars profiles, source hashes, scoring statuses and limitations. Added PNG/SVG figures explaining terrain-distance components and top-two sensitivity; existing maps and equal-scale terrain panels are linked with captions. No candidate reranking, geological investigation or website edits.

Verification: all 36 stored distances recomputed from stored features; component sums, unique IDs and footprint count checked. Both chart layouts visually inspected. Tests: 57 passed, eight existing warnings; Ruff passed. Reproduce with `python -m scripts.export_matching_handoff`. Website integration/build, browser testing, deployment and official submission were not performed.

Remaining dependencies: QA-controlled Earth feature handoff, compatible regional Mars day/night surface temperatures, and a defensible cross-theme comparison/weighting/missing-data definition before four-theme reranking. Unknown themes remain unscored; native dust, thermal inertia and ice consistency remain separate context. Original rankings unchanged. Codex assisted export code, checks, figures and English documentation.


### 2026-11-14: Regional Mars temperature source and English README

Synced main and located a new published MCS-derived surface-temperature grid, version DOI `10.5281/zenodo.17947556`, corrected to nominal 03:00 and 15:00 LTST. Downloaded 14,940,903 bytes, matched the provider MD5, recorded SHA-256/version/license, and extracted nearest native coordinates for Jezero, Gale and Arcadia over MY29–36. [The source report](outputs/mars_regional_temperature/README.md) documents methods, attribution and gaps; [context.json](outputs/mars_regional_temperature/context.json) contains reproducible series and counts.

Jezero/Gale/Arcadia have respectively 129/54/115 populated paired year–season bins out of 288. These are not same-sol pairs or raw observation counts. The native grid is 5° with 10° Ls spacing; all file attributes are empty and bin QA, counts, uncertainties and coordinate semantics remain unresolved. The product is model-adjusted observation-derived context, not a qualified 100 km kinetic-LST comparison. All target exports remain `scoring_eligible=false`; no existing ranking or formal temperature status was changed.

Integrated the separate context package into the Matching handoff exporter. Reporting can use the new key and caveats without recomputing science. Source and derived temperature data retain Wang/Jin attribution and CC-BY-4.0 terms. THEMIS BTR/PBT and TES routes were assessed but not substituted with uncalibrated mosaics. No candidate geological investigation, website edits, email query or account action occurred.

Translated the entire root README to English while preserving historical findings, linked evidence and the distinction between teammate-reported checks and this run. Remaining work: grid/quantity metadata and method verification, original quality/count support, compatible regional thermal support, Earth QA-controlled LST/time handoff, and a justified temperature-scoring definition. OpenAI Codex assisted source research, extraction code, tests and English documentation.

Verification for this temperature update: 62 Python tests passed (eight existing warnings), Ruff passed, provider checksum and export context equality checked, root README checked for remaining Chinese text, and local links checked. Formal regional temperature remains missing and the new context remains unscored. No website build, browser or deployment tests were run.

### 2026-11-14：研究輸出資料結構整理（數值不變）

已整理 `outputs/research/` 三份研究 JSON 的結構，供前端串接；所有科學數值、排名、足跡與 Top-2 結果均與原檔逐項比對一致。

- **統一驗證等級**：新增 `analog/evidence_status.py`，以 `VERIFIED`／`INFERRED`／`EXTERNAL`／`UNVERIFIED` 加說明取代自由文字前綴；等級表示支持方式，不是信賴度。
- **`three_candidate_evidence.json`**：以 `candidate_id` 為主鍵（Tarim/Oytag 候選為 `gale-01`，非 `gale-02`）；`coarse_shortlist_rank` 改名為 `scale10km_rank`（`null` 表示不在 10 km 執行的 12 名內）；`recalculated_distance` 改為 `distance_check`；重複的火星剖面移至頂層 `mars_profiles`；新增 `schema_version`、`generated_utc`、`field_notes`（含足跡 `[lon, lat]` 軸序）。
- **文獻狀態**：`gale-01` 的 `prior_analog_literature_status` 由 `not_checked` 更新為 `checked_partial`，並附上 Oytag 樣點與剖面的逐項主張；石膏 GPS、同露頭 XRD 及石膏／黏土／氧化鐵共現仍為 `UNVERIFIED`。
- **`oytag_overlap.json`**：樣點經緯度改為數值；標明 Table 1 岩性樣點與 Table DR1 鋯石母岩座標為兩組不重疊的點集（無共用樣品 ID）。
- **`oytag_transect_check.json`**：TLS 未驗證的下載改為結構化 `source_transport`（獨立雜湊核對：待辦）。

已執行三支產生腳本、輸入 SHA-256 鏈核對、`ruff check` 及新增的 `tests/test_research_outputs.py`（3 項通過）。剖面腳本重跑結果與原檔僅有約 1e-12 km 浮點差，保留原數值。本輪未重新排名、未修改 `web/`。Claude 協助本輪結構整理與中文紀錄。

### 2026-11-14：三個深入研究候選與 Oytag 文獻點接入前端

已將整理後的 `outputs/research/` 接入 `web/`：`build_workbench_data.py` 新增 `research` 區塊（深入研究候選、Oytag 樣點與 A–B 剖面、逐項主張與檔案 SHA-256）；其餘資料包內容與原本逐項相同。

- **候選清單**：新增 `Deep-dive (n)` 篩選；`gale-01`、`arcadia-01`、`arcadia-02` 顯示 Top-2 保留次數（4/4、3/4、2/4，明標非機率或信賴度）；`gale-01` 分類改為 `Literature checked (partial)`。
- **地圖**：全球圖以青色虛線環標示深入研究候選；選取 `gale-01` 的 `100 km Footprint` 時，在足跡內標出 3 個 Bershaw（2012）樣點，並以放大插圖顯示樣點、近似 A–B 含石膏剖面與窗口東界，註明石膏 GPS／XRD 未驗證。順帶修正足跡圖比例尺與範圍文字重疊。
- **證據矩陣與抽屜**：新增「Published Lithology & Prior Analog Literature」列（Contextual／Provisional；火星端標明未載入礦物層，不做礦物比對）；`EvidenceDrawer` 逐項顯示 `VERIFIED`／`INFERRED`／`EXTERNAL`／`UNVERIFIED` 主張與限制。完整度仍為 1/4，文獻背景不計入評分。

已執行 `npm ci`、`tsc -b`、`vite build` 及資料包重建（本機 stdlib Python 重建結果逐位元相同）；以 Chrome 實測 1440 px 與 390 px：Gale／Arcadia／Jezero 切換、篩選、足跡插圖與證據抽屜，0 個 console 錯誤、0 個失敗請求。既有問題：390 px 下任務列統計格造成水平捲動（914 px，修改前即存在）。未重新排名、未修改科學數值。Claude 協助本輪前端串接與中文紀錄。

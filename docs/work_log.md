# Work log (full reports)

Detailed work reports moved from the root README, which now keeps a short summary. Add new detailed entries at the end of this file and one summary line to the README.

Reports below preserve historical outcomes and limitations; a past status is not necessarily the latest status. Earlier source records and AI disclosures remain in the [pre-cleanup archive](../docs/archive/README_before_cleanup_2026-11-14.md), [Earth work log](../docs/work_report_2026-11-14.md) and [MEDA log](../docs/mars_temperature.md). The six phase prompts were edited; that alone did not execute the six phases. Historical linked documents may still be in Chinese; this root README is English.

### 2026-11-14: Repository cleanup

Reorganized README and data/document/output navigation; created a file-purpose inventory and preserved history and AI disclosures in the archive. Removed rebuildable local caches without deleting scientific inputs, sensitivity comparisons, tests or provenance. The 10 km analysis remains a dependency of summary scripts.

At that point, the interface, four-theme selection and competition submission were unfinished. No reranking or scientific values changed. Outstanding items included licensing, complete rules, Earth handoff and MEDA flags. OpenAI Codex assisted inventory and documentation. Verification: 57 tests passed, eight existing warnings, Ruff passed, and new navigation/archive links checked.

### 2026-11-14: Three Earth candidate research records

Created the [research report](../docs/research_report_three_analogs_2026-11-14.md) and [traceable evidence](../outputs/research/three_candidate_evidence.json). The existing cases are Gale–39N,75E and Arcadia–29N,105W / 35N,57E: three Earth candidates and two Mars targets. Jezero candidates remain terrain references without claiming dry-environment suitability.

Recomputed three distances from stored features. Top-two retention across four tested configurations was 4/4, 3/4 and 2/4, not calibrated confidence. Geology, ice, novelty and logistics remained unresolved. No reranking or NASA certification. Reproduce with `python -m scripts.report_candidate_evidence`.

### 2026-11-14: Located sedimentary-rock evidence

Updated [report section 3](../docs/research_report_three_analogs_2026-11-14.md). Three Bershaw et al. (2012) Oytag mudstone, sandstone and limestone sample points fell inside the eastern side of the 100 km candidate window. [Coordinates](../outputs/research/oytag_literature_points.csv) and [spatial checks](../outputs/research/oytag_overlap.json) are preserved.

This supports localized sedimentary-rock investigation. Gypsum was section-level evidence; exact outcrop, smectite and iron-oxide co-occurrence were unconfirmed. Marine/fluvial context cannot be equated to Gale's lake deposits. `python -m scripts.check_oytag_overlap` checked the three points against local ±50 km coordinates and the existing polygon. The source datum was unspecified, so the result is regional, not navigational. AI assisted literature review and calculations; no imagery or mineral measurements were fabricated.

### 2026-11-14: Teammate's local TerraMatch workbench

The Reporting teammate created `web/` with React 18, TypeScript and Vite. `web/scripts/build_workbench_data.py` and `web/src/data/adapter.ts` read the existing 4 km/10 km results, sensitivity, Mars profiles and MEDA summary without changing Matching inputs or rankings.

The teammate reported target switching with state reset, isolated Demo Mode, separate Earth/Mars coordinate diagrams, 12-candidate filtering and empty states, four-theme evidence views, source/hash drawers and four-configuration sensitivity. Displayed radii were Earth 6,371.0 km and Mars 3,396.0 km; approximate 100 km latitude spans were 0.90° and 1.69°. The lack of a Mars basemap was disclosed.

The teammate reported `npm run build:data`, TypeScript/Vite build and Ruff passing; browser checks at 1280×800 and 390×844 covered seven flows with no console errors or failed network requests. These are historical teammate-reported checks, not repeated by the later Matching export. Run locally with `npm install`, `npm run build:data`, `npm run build`, then Vite dev/preview. Antigravity assisted frontend work and testing. Ranks 3–12 lacked POWER context and regional Mars temperature remained missing.

### 2026-11-14: Approximate gypsum-bearing transect

[Report section 3.7](../docs/research_report_three_analogs_2026-11-14.md) used Sun/Jiang (2013) Figures 2–3 to approximate an A–B transect. Endpoints and eight ±8-pixel diagnostic cases lay inside the candidate. This was map-based inference, not original gypsum GPS or precise geological overlay.

Preserved the [calculation](../outputs/research/oytag_transect_check.json), [original schematic](../outputs/research/oytag_transect_schematic.png) and [source audit](../outputs/research/oytag_outcrop_source_audit.json). Thermomagnetic analysis, limestone Ca/Sr and nearby thin sections cannot substitute for same-outcrop gypsum XRD. Same-named sections cannot automatically be linked to one sample. The GPS–sample-ID–mineral chain and smectite co-occurrence remained unknown.

Executed overlap and transect checks and reviewed links/figures, without reranking or rerunning the full test suite. Codex assisted PDF interpretation and approximate spatial analysis; source PDFs were not redistributed.

### 2026-11-14: Original supplementary table

Obtained Bershaw (2012) `mmc1.xls` / Table DR1 and extracted ten PMR parent-rock coordinates and IDs inside the polygon. [Coordinates](../outputs/research/oytag_supplement_coordinates.csv), [hashes](../outputs/research/oytag_supplement_metadata.json) and [access log](../outputs/research/oytag_supplement_access_log.json) are preserved; see [section 3.8](../docs/research_report_three_analogs_2026-11-14.md).

The table is zircon-dating material, not gypsum GPS/XRD. Oytag sample `9412-1` concerns moraine and was excluded as same-outcrop evidence. Gypsum coordinates, unique ID, mineral analysis and Figure DR1 remained missing. Executed table decoding, unique-ID/coordinate/polygon and link checks. The optional reader was installed only temporarily; copyrighted Excel/PDF files were not redistributed. No reranking or full-suite rerun. Codex assisted source retrieval and extraction.

### 2026-11-14: Submission readiness audit

Created the [readiness report](../docs/submission_readiness_2026-11-14.md), [53-item checklist](../docs/submission_gap_checklist_2026-11-14.csv) and [snapshot](../outputs/research/submission_audit_snapshot_2026-11-14.json): eight submission items, 31 quality priorities and 14 claim-dependent items, not 53 official requirements.

The teammate inventory contained 222 files / about 12.33 GB; the full raw batch was not available locally. Rankings remained terrain-only, with 12 candidates per target and POWER for the first two. The audit recommended an evidence-limited main case instead of an unsupported combined score. It identified research-bundle, local-verification wording and source-mapping issues for Reporting without editing the website; later teammate fixes must be assessed separately.

Read official annual/legal pages and the Navigator submission reply; complete challenge text, guide and Taipei details remained unverified. Tests: 57 passed, eight existing warnings; Ruff passed. No frontend, deployment or official submission check. Codex assisted the audit and documentation.

### 2026-11-14: Submission copy and research requirements

Prepared [official checks and English copy](../docs/submission/preparation.md), [seven-slide text](../docs/submission/slides_en.md) and [rights/AI/contribution forms](../docs/submission/disclosures_and_rights.md). Account fields were left blank; Apache-2.0 remained a proposal. No login, message to organizers or submission occurred.

Added [one research question and five requirements](../docs/research_scope.md), [CSV matrix](../docs/research_requirements.csv), [literature review](../docs/literature_review.md) and [claim ledger](../docs/submission/claim_ledger.csv). Only terrain was quantitatively scored; environmental and same-outcrop conditions remained partial/unknown.

Executed `python -m scripts.validate_research_scope`: recomputed three Mars target signatures and Death Valley/Amazon reference windows from raw DEMs, matched stored Mars features and checked distance contributions. [Results and hashes](../outputs/research/reference_terrain_check.json) show that Arcadia terrain can favor a low-relief contrast, illustrating that terrain distance does not establish complete environmental analogy. Two windows are not full external validation. No ranking, candidate geology or website changes.

English PDF/video, account checks, team licensing, systematic literature/reference validation, public access and SUBMIT remained unfinished. Tests: 57 passed, eight existing warnings; Ruff and nine-document local-link checks passed. No frontend/build/deployment/submission. Codex assisted specifications, checks and writing; text drafts were not final deliverables.

### 2026-11-14: Matching results and website handoff

Synced main before work. Exported [the English website handoff](../outputs/matching_handoff/README.md) and [machine-readable matching data](../outputs/matching_handoff/matching_data.json): 36 stored target–candidate records, six with POWER context, three Mars profiles, source hashes, scoring statuses and limitations. Added PNG/SVG figures explaining terrain-distance components and top-two sensitivity; existing maps and equal-scale terrain panels are linked with captions. No candidate reranking, geological investigation or website edits.

Verification: all 36 stored distances recomputed from stored features; component sums, unique IDs and footprint count checked. Both chart layouts visually inspected. Tests: 57 passed, eight existing warnings; Ruff passed. Reproduce with `python -m scripts.export_matching_handoff`. Website integration/build, browser testing, deployment and official submission were not performed.

Remaining dependencies: QA-controlled Earth feature handoff, compatible regional Mars day/night surface temperatures, and a defensible cross-theme comparison/weighting/missing-data definition before four-theme reranking. Unknown themes remain unscored; native dust, thermal inertia and ice consistency remain separate context. Original rankings unchanged. Codex assisted export code, checks, figures and English documentation.


### 2026-11-14: Regional Mars temperature source and English README

Synced main and located a new published MCS-derived surface-temperature grid, version DOI `10.5281/zenodo.17947556`, corrected to nominal 03:00 and 15:00 LTST. Downloaded 14,940,903 bytes, matched the provider MD5, recorded SHA-256/version/license, and extracted nearest native coordinates for Jezero, Gale and Arcadia over MY29–36. [The source report](../outputs/mars_regional_temperature/README.md) documents methods, attribution and gaps; [context.json](../outputs/mars_regional_temperature/context.json) contains reproducible series and counts.

Jezero/Gale/Arcadia have respectively 129/54/115 populated paired year–season bins out of 288. These are not same-sol pairs or raw observation counts. The native grid is 5° with 10° Ls spacing; all file attributes are empty and bin QA, counts, uncertainties and coordinate semantics remain unresolved. The product is model-adjusted observation-derived context, not a qualified 100 km kinetic-LST comparison. All target exports remain `scoring_eligible=false`; no existing ranking or formal temperature status was changed.

Integrated the separate context package into the Matching handoff exporter. Reporting can use the new key and caveats without recomputing science. Source and derived temperature data retain Wang/Jin attribution and CC-BY-4.0 terms. THEMIS BTR/PBT and TES routes were assessed but not substituted with uncalibrated mosaics. No candidate geological investigation, website edits, email query or account action occurred.

Translated the entire root README to English while preserving historical findings, linked evidence and the distinction between teammate-reported checks and this run. Remaining work: grid/quantity metadata and method verification, original quality/count support, compatible regional thermal support, Earth QA-controlled LST/time handoff, and a justified temperature-scoring definition. OpenAI Codex assisted source research, extraction code, tests and English documentation.

Verification for this temperature update: 62 Python tests passed (eight existing warnings), Ruff passed, provider checksum and export context equality checked, root README checked for remaining Chinese text, and local links checked. Formal regional temperature remains missing and the new context remains unscored. No website build, browser or deployment tests were run.

### 2026-11-14: Teammate research-schema cleanup

The teammate standardized three research JSON outputs for frontend use, preserving numerical values, ranks, footprints and top-two results. `analog/evidence_status.py` introduced VERIFIED / INFERRED / EXTERNAL / UNVERIFIED levels with explanations; these describe evidence support, not confidence.

`three_candidate_evidence.json` now uses candidate IDs (Oytag is `gale-01`, not `gale-02`), renames `coarse_shortlist_rank` to `scale10km_rank` (null means absent from that run's 12-item shortlist), and replaces `recalculated_distance` with `distance_check`. Shared profiles moved to top-level `mars_profiles`; schema version, generation time and field notes include footprint axis order `[lon,lat]`. Gale literature status became `checked_partial`, with individual claims; gypsum GPS, same-outcrop XRD and gypsum/clay/iron-oxide co-occurrence remain unverified. Overlap coordinates became numeric, with no shared IDs between Table 1 lithology points and Table DR1 zircon parent-rock points. Transect transport information now records unverified TLS and pending independent hash confirmation.

The teammate reported three generator runs, source SHA-256 checks, Ruff and three research-output tests passing. Approximately 1e-12 km rerun differences were handled by retaining original values. No reranking or website edits in that schema task. Claude assisted schema cleanup and documentation.

### 2026-11-14: Teammate research integration into the website

The teammate added a `research` section to the web data builder: three deep-dive cases, Oytag literature samples, approximate A–B transect, claims and file hashes. Other bundle content remained unchanged.

Candidate filtering gained Deep-dive, with retention counts 4/4, 3/4 and 2/4 explicitly not confidence. Gale's partial literature classification is visible. The map highlights deep-dive candidates; Gale's footprint includes three Bershaw points and an inset with the approximate gypsum-bearing transect and eastern boundary. Gypsum GPS/XRD remain unverified. A previous scale-label overlap was corrected.

The evidence matrix/drawer includes published lithology and prior-literature claims as contextual/provisional, with no loaded Mars mineral layer or mineral score. Scored-theme count remains one of four. The teammate reported npm installation, TypeScript/Vite build and bit-identical stdlib data regeneration, plus Chrome checks at 1440 and 390 px for targets, filters, footprint inset and drawer, without console/network failures. A pre-existing 390 px horizontal overflow (914 px document width) in the header statistics was noted. No scientific values or rankings changed. Claude assisted frontend integration and documentation.

### 2026-11-14: Website information organization

Synced main and reorganized the existing workbench into three views: Overview & map, Evidence & sources, and Sensitivity & gaps. The default view now introduces the task and shows one selected-region summary before the spatial comparison. Candidate selection remains available across views; inactive cards are compact, while the selected candidate retains its support and gap details. Method, timing, search settings and source provenance remain accessible in a collapsed disclosure instead of occupying the initial screen. Removed misleading numbered panel headings and repeated per-candidate completion bars; the one-of-four scored status remains explicit.

Selection clears any open evidence drawer to prevent showing a previous candidate's source context. Demo preview retains its warning and isolated synthetic state. Scientific values, ranking, evidence records, geology and source datasets were not changed. Root README entries appended by teammates were translated to English with their facts and attribution preserved.

Validation: TypeScript/Vite production build passed. Headless Chromium checked default overview, target switching, evidence/sensitivity navigation, Demo-to-real reset and mobile overflow with method details closed and open. At 390 px the document width was 390 px. No page errors were observed in these flows. Desktop/mobile screenshots were captured for review. These local checks do not establish public deployment or official submission. OpenAI Codex assisted information hierarchy, React/CSS changes, browser checks and English documentation.

Additional browser checks passed: evidence drawer opens and closes with Escape, all three targets update the selected summary, and selecting Gale rank 2 updates the summary without changing stored ranks. A first smoke-test attempt used an incorrect accessible button name; the selector was corrected to the existing evidence-specific label and the complete flow passed. Browser-test dependencies and screenshots stayed outside the repository.


### 2026-11-14: Public deployment diagnosis

Opened the public Cloudflare Pages URL in headless Chromium at desktop 1440×1000 and mobile 390×844. HTTP 200 and initial asset requests succeeded with no observed page errors, but the site still served the old all-panels layout (`index-BVqdeinh.js`), with no new three-view navigation. Mobile document width was 916 px at a 390 px viewport. The latest organized layout is therefore **not verified as deployed**.

GitHub Actions for `f0cdd59` failed at upload with an invalid header value. Added masked token normalization/validation and reran deployment; `fb10a3c` failed validation because the configured token still contains unsupported characters after trimming. Five synthetic format checks passed. Requested that the repository owner replace the token secret and configure the missing account-ID secret, without sharing credentials in chat. [Full evidence and next checks](../docs/deployment_check_2026-11-14.md).

The workflow repair is pushed; publication remains blocked on valid Cloudflare configuration. Public desktop/mobile verification of the new layout will resume after the owner updates secrets. No science or site-content changes were made in this diagnostic task. OpenAI Codex assisted CI diagnosis, browser checks and English reporting.


### 2026-11-14: Local website fallback

The user could not access Cloudflare and chose local operation. Started the latest organized workbench at `http://127.0.0.1:4178/` and opened it in the in-app browser. The rendered page showed the three-view navigation, selected-candidate summary and maps. The development server remains running for this session. Restart from the repository root with `npm run dev --prefix web -- --host 127.0.0.1 --port 4178 --strictPort` if it stops. This address is local to this computer, not a public competition demo link. Cloudflare deployment remains blocked and was not represented as complete. No scientific data or rankings changed.


### 2026-11-14: Push-triggered deployment recheck

At the user's request, pushed `f47c72c` with web run/deployment documentation to exercise the reported GitHub integration. [Run 43563444490](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/actions/runs/43563444490) passed data generation and web build, then failed credential-format validation before upload. The previously checked Pages URL still served `index-BVqdeinh.js`, not the organized layout. No alternative deployment check or repository homepage URL was reported by GitHub at this check. Requested the teammate's actual public URL if a separate hosting integration is in use. Local operation remains available; successful deployment is not claimed.


### 2026-11-14: Public organized-layout verification passed

After syncing the teammate's manual-upload record, independently opened the public site and verified the organized layout served `index-C1XZWWZv.js`. Public Chromium checks passed at desktop 1440×1000 and mobile 390×844: default overview, three-view navigation, all three targets, candidate selection, evidence drawer opening/Escape closure and Demo-to-real reset. Mobile document width stayed 390 px with method details closed and open. No JavaScript page errors occurred in these tested flows. The public Gale comparison figure returned HTTP 200. No layout fixes were needed after these checks.

The public organized-layout release is now verified. Automatic GitHub Actions deployment remains a separate unresolved configuration issue; successful manual upload does not repair it. No scientific results or website code changed in this verification. OpenAI Codex assisted browser checks and English reporting.


### 2026-11-14: Automatic deployment workflow repair

Changed the Pages workflow to run on every push to main, including documentation-only pushes, with manual dispatch retained. Configuration is validated before building: both token and account ID are required, surrounding whitespace is normalized, invalid input fails clearly, and an unavailable upload can no longer produce a misleading successful run. Credentials remain in GitHub secrets; no secret values were read into the workspace.

Added a release stamp containing the commit/run identifiers to the built site and a post-upload verifier that checks the public commit stamp plus referenced application assets. An old public version or missing assets cannot pass. Three targeted tests for current release, stale release and missing assets passed; Ruff passed for the new verification code. The existing organized public layout remains available.

Owner action is still needed: replace the malformed CLOUDFLARE_API_TOKEN with a Pages-edit token scoped to the existing project's account and configure CLOUDFLARE_ACCOUNT_ID. End-to-end automatic publication is pending those settings and a successful real workflow run; workflow edits alone are not reported as completed automatic deployment. OpenAI Codex assisted CI changes, verification tests and English documentation.

Validation correction: the first targeted test invocation failed during import and linting; corrected standalone-script loading and context-manager formatting, then reran successfully (3 passed; Ruff passed). The earlier stated test outcome applies to this corrected run.

### 2026-11-14: Official site moved to the team Cloudflare Worker

The team chose the Worker `nasa-space-apps-challenge-2026-taipei` in the team (zizi) Cloudflare account as the only official site (https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev). Its first upload held unbuilt source and rendered blank; it was redeployed from a local build of `main` and checked in the browser (three-view layout, no console errors). Added root `wrangler.jsonc`, retargeted the GitHub Actions workflow from the personal Pages project to `wrangler deploy` with release verification at the new URL, and retired the `pages.dev` link. Pending: set `CLOUDFLARE_ACCOUNT_ID` to the team account ID and replace `CLOUDFLARE_API_TOKEN` with a team-account Workers token. Claude Code assisted.

### 2026-11-14: Participant-guide review

Read the English Project Submission, Judging & Awards and Team Formation guide copies in the user-provided Drive collection, plus relevant FAQ/Connect sections. [The English rules digest](docs/submission/official_rules_digest.md) now records the actual submission fields, separate demo/final-project links, English requirements, 7-slide/30-second limits, SI disclosure/marking, five judging criteria, eligibility and award dates. This supersedes earlier statements that no complete general submission guide had been obtained; the challenge-specific full text and local event instructions are separate checks.

The Chinese PDFs identify themselves as unofficial translations. The official explainer video's exported transcript was Japanese auto-generated/translated captions, so exact rules were grounded in the English PDFs. The Chinese-dubbed MP4 was identified by metadata, not independently watched. Direct canonical web pages remained inaccessible; the provided guide copies were not independently matched against a fresh official download. Older 2023/2024 organizer materials were excluded from 2026 timing/rules. No documents were republished in full, no team declarations accepted and no submission made. OpenAI Codex assisted source review and English documentation.


### 2026-11-14: Printable participant-guide PDF

Created a four-page Traditional Chinese internal preparation PDF with requirements tables, bullet points, judging/SI guidance, 14 printable checklist boxes and six clickable source links. [Download the PDF](output/pdf/spaceapps_2026_team_checklist_zh-TW.pdf). This is an internal reference summary, not the final English competition demo. Preserved source-access limitations and distinguished official requirements from project recommendations. Verified four pages and extracted key text/source annotations, rendered all pages and inspected layout; corrected a narrow checklist header before final export. No scientific outputs or website code changed. OpenAI Codex assisted document layout and verification.


### 2026-11-14: Team Worker and automatic deployment recheck

Confirmed the official team Worker URL serves the organized layout. Public Chromium checks passed at 1440×1000 and 390×844 for overview, evidence/sensitivity navigation, three targets, candidate selection, drawer/Escape and Demo reset. Mobile document width remained 390 px, including open method details; no page errors in these flows.

Manually dispatched [run 43567297561](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/actions/runs/43567297561) against current main. Account-ID format validation no longer reports an error, but CLOUDFLARE_API_TOKEN still fails format validation. The site is publicly available; automatic upload is not yet working. Owner must replace the token secret with the pure value of a token authorized for Workers deployment in the team account. No credential values were read or published; no scientific or website changes were needed.

### 2026-11-14：Matching 火星用途候選文獻查核交接

已完成 [Reporting 交接](docs/mars_discovery_handoff.md)、[15 點逐項查核／原始數值表](docs/mars_discovery_novelty_checks.csv)與[搜尋範圍及來源雜湊紀錄](docs/mars_discovery_search_scope.json)。檢視三類用途各前五名與三張原圖；I-01／I-02 僅保留淺冰研究候選，D-03／D-04 僅作沙塵／地形脈絡參考，建議暫停 firm-ground 承載與通行性主張。所有點的精確位置／相同用途新穎性仍標示未確認，沒有宣稱從未研究。D-01／D-02 的中心位於既有 Utopia 沙塵研究監測圈內，與實際推薦登陸區分開說明。

核對：15 筆座標、既有分數與五層值均與來源 JSON 一致；四組卡片數值及本機引用連結通過檢查。來源 JSON、三張 PNG、analog/ 與 discovery 程式維持原樣；未重排候選、未處理地球原始資料、未執行前端或整套測試。狀態同步工具新增 `--handoff`，預覽與 Ruff 通過；桌面原檔仍受本工作階段寫入限制，需在 Mac 終端機執行 `python3 scripts/sync_desktop_ai_status.py --handoff` 才會更新原檔的 GPT 欄。本輪未修改 Cursor 欄。

OpenAI Codex 協助公開一手來源檢索、有限範圍新穎性查核、研究文字與引用整理、數值轉錄與地理監測圈核對。文件已存於本機儲存庫，本輪未提交或推送 Git。

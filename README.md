# Mars Analog Finder

### Earth–Mars analog research · NASA Space Apps 2026 Taipei · Team zasa

Search open terrain data for Earth candidate regions, compare them with Mars targets, and expose the supporting evidence, missing data and limits of each analogy.

**[Live dashboard → nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev](https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev)** · [Methods](docs/README.md) · [Candidate results](outputs/analysis/candidate_handoff.md) · [Website handoff](outputs/matching_handoff/README.md) · [Mars data](outputs/mars_profiles/handoff.md) · [Data guide](data/README.md) · [Contributing](CONTRIBUTING.md)

> Research pipeline and candidate-analysis prototype. Regional terrain results are available; validated four-theme scoring is unfinished. The official public dashboard is https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev (team Cloudflare account); automatic deploys from GitHub Actions need the team API token, see the deployment report. This repository does not establish NASA endorsement or completed competition submission. Earth–Mars-only scope is a locked team decision.

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
| Interactive workbench | Official site on the team Cloudflare Worker; auto-deploy from `main` waits for the team API token | [Live dashboard](https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev) (official, team Cloudflare), [deployment check](docs/deployment_check_2026-11-14.md) |
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

## Public site (Cloudflare)

| Item | Value |
|---|---|
| Official URL | [nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev](https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev) |
| Cloudflare account | Team account "zizi" (`Ziz81503@gmail.com's Account`) |
| Account ID | `5a215a2a3ffc384e958ae5bcb53687d0` (not a secret) |
| Service | Workers & Pages → Worker `nasa-space-apps-challenge-2026-taipei` (static assets only) |
| Config | Root [`wrangler.jsonc`](wrangler.jsonc): Worker name, assets from `web/dist`, single-page-app fallback |
| Auto-deploy | [`.github/workflows/cloudflare-pages.yml`](.github/workflows/cloudflare-pages.yml): every push to `main` builds `web/dist`, stamps `deployment.json`, runs `wrangler deploy`, then checks the live URL serves that commit |
| Retired | `terramatch-mission-lab.pages.dev` (personal account) is no longer updated; do not share it |

**Repository secrets** (Settings → Secrets and variables → Actions; values are pasted in GitHub only, never committed):

- `CLOUDFLARE_ACCOUNT_ID` = the team account ID above.
- `CLOUDFLARE_API_TOKEN` = a token created in the team account (My Profile → API Tokens → Create Token → *Edit Cloudflare Workers* template, scoped to the team account). Paste the token value only, with no quotes, spaces or command text.

Until both secrets are set, the workflow stops at "Validate deployment configuration" and the site changes only through a manual deploy. Use either GitHub Actions or Cloudflare's own Git build for this Worker, not both.

**Manual deploy** (needs Workers access to the team account):

```bash
python3 web/scripts/build_workbench_data.py
(cd web && npm ci && npm run build)
CLOUDFLARE_ACCOUNT_ID=5a215a2a3ffc384e958ae5bcb53687d0 npx wrangler deploy
```

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

GitHub Actions for `f0cdd59` failed at upload with an invalid header value. Added masked token normalization/validation and reran deployment; `fb10a3c` failed validation because the configured token still contains unsupported characters after trimming. Five synthetic format checks passed. Requested that the repository owner replace the token secret and configure the missing account-ID secret, without sharing credentials in chat. [Full evidence and next checks](docs/deployment_check_2026-11-14.md).

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


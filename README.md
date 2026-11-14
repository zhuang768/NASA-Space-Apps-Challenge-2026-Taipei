# Mars Analog Finder

### Earth–Mars analog research · NASA Space Apps 2026 Taipei · Team zasa

Search open terrain data for Earth candidate regions, compare them with Mars targets, and expose the supporting evidence, missing data and limits of each analogy.

**[Live dashboard → nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev](https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev)** · [Methods](docs/README.md) · [Candidate results](outputs/analysis/candidate_handoff.md) · [Website handoff](outputs/matching_handoff/README.md) · [Mars data](outputs/mars_profiles/handoff.md) · [Data guide](data/README.md) · [Contributing](CONTRIBUTING.md)

> **Status:** research pipeline and candidate-analysis prototype. Regional terrain results are available; validated four-theme scoring is unfinished. Not NASA-endorsed, and the competition submission is not complete. Earth–Mars-only scope is a locked team decision.

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
| Interactive workbench | Official site on the team Cloudflare Worker; auto-deploy from `main` waits for the team API token | [Public site](#public-site-cloudflare), [deployment check](docs/deployment_check_2026-11-14.md) |
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

Website (`web/`, Node 22):

```bash
python3 web/scripts/build_workbench_data.py   # rebuild the data bundle from outputs/
cd web && npm ci && npm run dev               # http://127.0.0.1:5173
```

Earth screening additionally needs ETOPO and the land mask; see [Earth execution](docs/earth_pipeline.md). Some Earthdata products require an account. Never commit credentials. [requirements-lock.txt](requirements-lock.txt) records the tested environment; cross-platform installation still requires verification.

```text
analog/       Scientific readers, scale handling and analysis
scripts/      Download, processing, export and plotting entry points
tests/        Data and method checks
data/         Mars inputs and processed data; large Earth files handed off separately
outputs/      Candidates, provenance, sensitivity, profiles and figures
docs/         Methods, data contracts, submission drafts and historical records
web/          TerraMatch Mission Lab: React + Vite workbench built from outputs/
```

See the [data guide](data/README.md), [output guide](outputs/README.md) and [file inventory](docs/repository_inventory.csv).

## Public site (Cloudflare)

| Item | Value |
|---|---|
| Official URL | [nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev](https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev) |
| Cloudflare account | Team account "zizi" |
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

The official-repository Navigator reply supports preparing up to seven slides or a video of at most 30 seconds. The complete submission guide, account details and Taipei-specific requirements remain unverified. Drafts are not proof of submission. See the [remaining checklist](docs/submission/remaining_checklist.md).

## Work log

All entries are from 2026-11-14. Full reports with verification details and per-entry AI disclosures are in the [work log](docs/work_log.md); earlier records are in the [pre-cleanup archive](docs/archive/README_before_cleanup_2026-11-14.md), [Earth work log](docs/work_report_2026-11-14.md) and [MEDA log](docs/mars_temperature.md). A past status is not necessarily the latest. Some linked documents are still in Chinese.

- **Cleanup:** reorganized docs, data and output navigation; added a [file inventory](docs/repository_inventory.csv). No scientific values changed.
- **Candidate research:** [three evidence records](outputs/research/three_candidate_evidence.json) for `gale-01` (39°N 75°E), `arcadia-01` (29°N 105°W) and `arcadia-02` (35°N 57°E). Top-2 retention across four configurations was 4/4, 3/4 and 2/4, which is not confidence. See the [report](docs/research_report_three_analogs_2026-11-14.md).
- **Oytag literature (`gale-01`):** three Bershaw et al. (2012) rock samples, an approximate Sun et al. (2013) gypsum-bearing transect and ten Table DR1 zircon parent-rock coordinates fall inside the window. Gypsum GPS, same-outcrop XRD and gypsum/clay/iron-oxide co-occurrence remain unverified.
- **Research schema:** candidate-ID keys, shared evidence levels (`VERIFIED` / `INFERRED` / `EXTERNAL` / `UNVERIFIED`, which describe support, not confidence) and numeric coordinates. Values unchanged.
- **Matching handoff:** [36 target–candidate records](outputs/matching_handoff/README.md) with figures. No reranking.
- **Regional Mars temperature:** MCS-derived day/night context (DOI `10.5281/zenodo.17947556`) for Jezero, Gale and Arcadia; unscored, metadata incomplete. See the [source report](outputs/mars_regional_temperature/README.md).
- **Submission preparation:** [readiness audit](docs/submission_readiness_2026-11-14.md) (53 checklist items, not official requirements), [English copy and slide text](docs/submission/preparation.md), [research scope](docs/research_scope.md) and a two-window [reference check](outputs/research/reference_terrain_check.json), which is not full validation. Account fields are blank and nothing has been submitted.
- **Website:** candidates, dual maps, evidence drawer and sensitivity views; deep-dive candidates and the Oytag overlay; three views (Overview & map, Evidence & sources, Sensitivity & gaps). Browser-checked at 1440 px and 390 px.
- **Participant guides:** [English rules digest](docs/submission/official_rules_digest.md) with submission fields, 7-slide / 30-second limits, judging criteria and dates, plus a printable [Chinese team checklist PDF](output/pdf/spaceapps_2026_team_checklist_zh-TW.pdf) for internal use.
- **Mars discovery handoff:** literature checks on the top five sites per use (handoff files not yet committed); novelty of exact locations remains unconfirmed.
- **Deployment:** official site moved to the team Cloudflare Worker; the workflow now runs `wrangler deploy` with release verification. The team site passed public desktop and mobile checks; automatic deploys wait for a valid team API token (see [Public site](#public-site-cloudflare)).

Open: team Cloudflare API token, original-code license, challenge-specific and Taipei event details, Earth QA-controlled data handoff, qualified regional Mars temperature, and four-theme scoring.

AI assistance (OpenAI Codex, Antigravity, Claude) is disclosed per entry in the full log.

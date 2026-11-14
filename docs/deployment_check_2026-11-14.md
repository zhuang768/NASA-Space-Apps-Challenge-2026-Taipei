# Public deployment verification

Checked 2026-11-14, Taipei. Public URL: https://terramatch-mission-lab.pages.dev . The public site is reachable, but the organized layout is not deployed successfully yet.

## Observed public version

Headless Chromium loaded the public URL without authentication and received HTTP 200. The loaded JavaScript asset was `/assets/index-BVqdeinh.js`. The page still showed the old numbered candidate/map headings, all analysis panels together, and no “Overview & map” button. This differs from the locally verified organized layout in commit `f0cdd59`.

| Check | Desktop 1440 × 1000 | Mobile 390 × 844 |
|---|---|---|
| Public page loaded | Yes | Yes |
| Organized three-view layout present | No | No |
| Document width | 1440 px | 916 px |
| Horizontal page overflow | None observed | Present |
| JavaScript page errors / failed requests in initial load | None observed | None observed |

Screenshots were captured outside the repository. The organized layout's earlier local mobile checks passed at 390 px; those checks must not be described as public verification. The current public mobile overflow is an outdated-release symptom, not proof the new layout fix failed.

## Deployment diagnosis and attempted repair

- [Run 43562804847](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/actions/runs/43562804847), for `f0cdd59`, built successfully but failed during Cloudflare upload with an invalid HTTP header value.
- Added a credential-format validation step: trim surrounding whitespace; reject remaining whitespace, control characters or non-ASCII characters; mask the normalized value before passing it to Wrangler. Actual credentials are never printed by this step.
- [Run 43563055949](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/actions/runs/43563055949), for `fb10a3c`, failed that validation. Trimming alone cannot repair the configured token.
- GitHub secret-name inventory shows `CLOUDFLARE_API_TOKEN`; `CLOUDFLARE_ACCOUNT_ID` is not configured. No secret values were retrieved or copied into project files.
- Five synthetic cases verified normal token acceptance, surrounding-whitespace trimming, and rejection of an internal newline, empty value and invisible non-ASCII character.

## Required owner action

In repository Settings → Secrets and variables → Actions, replace `CLOUDFLARE_API_TOKEN` with the token value only and configure `CLOUDFLARE_ACCOUNT_ID`. Do not paste credentials into chat or the repository. Cloudflare's [CI deployment instructions](https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/) describe these variables and required Pages access.

After the owner updates the secrets, rerun the workflow, confirm successful upload, and load the public URL again. Verify the three-view layout, candidate/target selection, evidence drawer, Demo reset, figure requests and mobile width with method details open and closed. These public organized-layout checks remain pending.

No new candidate research, scientific values or rankings changed in this deployment task. Successful build and HTTP 200 are not reported as successful deployment of the latest version.

## Manual upload of the organized layout

Later on 2026-11-14 the current `main` (`9d865d7`) was rebuilt locally (`build_workbench_data.py`, `npm ci`, `npm run build`) and uploaded with Wrangler direct upload to the `terramatch-mission-lab` Pages project, production branch `main`. The public URL then served `/assets/index-C1XZWWZv.js` and showed the “Overview & map”, “Evidence & sources” and “Sensitivity & gaps” views, with no console errors on desktop load. Public mobile-width checks were not repeated.

This was a one-off manual upload. Pushes to `main` will not update the site automatically until the owner replaces `CLOUDFLARE_API_TOKEN` and adds `CLOUDFLARE_ACCOUNT_ID` as described above.


## Subsequent public desktop and mobile verification

The organized public release was independently checked after the manual upload. Desktop 1440×1000 and mobile 390×844 passed overview/navigation, target and candidate selection, evidence drawer/Escape closure, and Demo reset. The mobile document remained exactly 390 px wide with method details closed and open. No JavaScript page errors were observed. The Gale terrain-comparison image returned HTTP 200. The served JavaScript was `index-C1XZWWZv.js`. No new layout defect requiring a code change was found in these flows. Earlier failure/overflow findings above describe the previous release, not the current public layout. Automatic deployment credentials remain unresolved.

## Official site moved to the team Cloudflare account

The team chose the Worker `nasa-space-apps-challenge-2026-taipei` in the team (zizi) Cloudflare account as the single official site: https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev . Its first upload contained unbuilt source (`/src/main.tsx`) and rendered blank; it was redeployed from a local build of `main` and then showed the three-view layout with no console errors.

- Root `wrangler.jsonc` names the Worker and serves `web/dist` as static assets.
- The GitHub Actions workflow now runs `wrangler deploy` to that Worker and verifies `deployment.json` at the new URL.
- Repository secret `CLOUDFLARE_ACCOUNT_ID` must hold the team account ID; `CLOUDFLARE_API_TOKEN` must be a team-account token with Workers Scripts edit permission. Until the token is replaced, the workflow stops at validation and the site only changes through manual deploys.
- The older `terramatch-mission-lab.pages.dev` site (personal account) is retired and no longer updated.

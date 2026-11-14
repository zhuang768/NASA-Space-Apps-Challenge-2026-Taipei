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

# TerraMatch: deployment repair preview

**Local technical handoff only.** Opening `index.html` loads no external resources. The page is not the official site, competition submission, formal report, or deck.

## Reproduce

Run `python3 build_preview.py`. The standard-library-only generator verifies the source Git blob before emitting a self-contained static page. It views three rows from current main's existing screening CSV; it neither reranks candidates nor incorporates later unmerged follow-ups. To use a different source, deliberately review and update both the pinned commit and blob.

- Main observed: `1506ede572435588eb5e64f95f24639279b77e56`.
- Input: `outputs/research/mars_reselection_20261114/final_candidates.csv` at that commit.
- Input Git blob: `2371ade1c27087efaa165acb98b7541266eaa606`.
- Input SHA-256: `83a03d1f4273fa7c45c0d22b5c29a8b8cfc0544e481d5f2bbca2c85812534c4e`.

## Why production is stale

The signed-out Worker responds with `deployment.json` for `e84da75d905ad43f260e74307752946862200dae`, workflow `43597448313`. Main commit `3408648` intentionally removed `web/`, `wrangler.jsonc` and the deploy workflow by design while retaining them in the old tree and archive. The current external Workers Builds check reports failure; Cloudflare's detailed external log is not accessible from GitHub alone. Passing historical or no-op GitHub Actions checks do not establish that production reflects the present commit.

## Safe repair sequence (not executed in production)

1. Keep production unchanged while the team approves a frozen evidence commit. Baseline `1506ede...` is reproducible for a preview but is not a scientific completion gate: MS-02 PR #22 and #25 remain open. Their changed paths do not intersect at time of check, but they cover overlapping scientific concepts. Resolve claim precedence explicitly, then reconcile audit/synthesis entries (#9/#10); do not blanket-merge or use older #2/#5.
2. Add the standalone static supplement on a reviewed site branch rooted in the freeze, or adapt the archival workbench to the current evidence schema. Do not restore the legacy builder unmodified: it explicitly requires retired Gale/Oytag files and labels. Keep private source items, attribution details that identify minors, and credentials out of the public build.
3. Choose one already-authorized production release mechanism. The previous Actions workflow built static assets, validated and masked existing credentials, stamped the commit/run and verified the signed-out result. The externally triggered Cloudflare Workers build is a separate route. Don't re-enable two deployment writers simultaneously; if existing Cloudflare authority is unavailable, keep the local preview and seek the account operator, with no settings changes.
4. Run a no-secret local build and inspect offline and mobile. Only after an authorized deploy, fetch the production URL and deployment stamp signed out, matching expected commit. Compare rendered cards and labels against the source. Keep distinct public demo, final app, private research source, and official submission receipt. A GitHub commit or a web deployment is not a submission receipt.

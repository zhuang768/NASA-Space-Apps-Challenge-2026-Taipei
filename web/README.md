# TerraMatch Mission Lab web app

The workbench presents stored scientific outputs in three views: Overview & map, Evidence & sources, and Sensitivity & gaps. Candidate selection is shared across views. Only terrain is ranked; other themes retain their source-specific context and missing-data status.

## Local use

From the repository root:

```bash
npm ci --prefix web
npm run dev --prefix web -- --host 127.0.0.1 --port 4178 --strictPort
```

Build with `npm run build --prefix web`; the static output is `web/dist`. The data builder is `python3 web/scripts/build_workbench_data.py`. Rebuilding the web bundle does not rerank scientific outputs.

## Deployment

The repository includes a Cloudflare Pages workflow. Every push to `main` triggers its build/deploy path. A separately configured Cloudflare Git integration may also deploy main. A successful push or build alone does not establish that the public site is current; check the actual public page for the three-view navigation and latest asset bundle.

The previously checked URL is https://terramatch-mission-lab.pages.dev . Deployment credentials belong in service/repository settings, never source files. See the root README for verification history and outstanding configuration issues.

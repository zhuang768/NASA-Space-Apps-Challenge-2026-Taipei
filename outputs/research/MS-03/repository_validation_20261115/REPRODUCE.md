# Reproduce the audit

Software versions actually used are in `environment.json`. No research data from another local project checkout were used. All input bytes came from the frozen audit clone or exact Git blobs.

Use a disposable checkout with full history. The following network operations read only GitHub:

```sh
git clone --no-checkout https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei.git repo
git -C repo fetch origin '+refs/heads/*:refs/remotes/audit/*'
git -C repo fetch origin refs/pull/26/head:refs/remotes/origin/pr26
git -C repo checkout --detach 07dbe29203504ba0ccde5e379f42ecc16e4b1b4f
python numeric_audit/recompute_ms03.py --repo "$PWD/repo" --out "$PWD/rerun/numeric"
python earth_audit/audit_ad1.py --repo "$PWD/repo" --out "$PWD/rerun/earth"
python mars_audit/verify_mars.py --repo "$PWD/repo" --out "$PWD/rerun/mars"
python mars_audit/verify_catalogue.py --repo "$PWD/repo" --out "$PWD/rerun/mars"
python make_support_figure.py --repo "$PWD/repo" --out "$PWD/rerun/mars"
```

The numeric script extracts 11 exact source blobs from archive commit `8f666d878fe0a3d97e41daa64fab43660174652f`. It checks every file against main's expected byte count and SHA-256 before using it. Extracted originals are written only under the output directory. No external server is called by the analysis scripts. About 383.5 MB of temporary raw inputs is required for this step.

The `audit/*` heads must match `github_metadata/branches.json` to reproduce the original 42-head search inventory. Newer heads constitute a new audit. Keep or restore refs to the snapshot SHAs recorded in that file.

The retained version-search and Release tables record the bounded audit snapshot. Large Release payloads were not verified. The three small Release metadata files and their retrieval receipts remain in the independently delivered audit package; they are not duplicated here.

Manual image review is separate from calculation. Open every source path in `mars_audit/windows.csv`, using `protocol.json` and full windows. No blinded second-reader test was performed. A program rerun cannot certify polygon recognition by itself.

CSV structure and GeoJSON were checked, and delivered files are hashed in `manifest.json`. There is no Mars GeoJSON. The Earth GeoJSON is a source-preserving re-encoding of the published AD1 contours with source-row IDs, not a new independent accuracy assessment.

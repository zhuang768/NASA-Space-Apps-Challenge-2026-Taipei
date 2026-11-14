# Retained W short Campbell author export

Creator/data collector: **Margarita Marinova**. Dataset: *Data from NASA project to study ice-cemented ground in and around University Valley Antarctica*, Zenodo v1, 2024-01-23, DOI [10.5281/zenodo.10553882](https://doi.org/10.5281/zenodo.10553882). Associated article: Marinova et al. 2022, DOI [10.1017/S0954102022000025](https://doi.org/10.1017/S0954102022000025).

License: **CC0 1.0**, [public-domain dedication](https://creativecommons.org/publicdomain/zero/1.0/). The fixed repository source metadata records `U4.license` as “CC0 per version metadata”; exact evidence link and scope are in `provenance.json`. This task rechecked the official file listing and provider MD5; a fresh API read was blocked, so this is not represented as a new API license verification.

Official file: [UniversityV_09_10_Campbell_data_good_only_calibrated.txt](https://zenodo.org/records/10553882/files/UniversityV_09_10_Campbell_data_good_only_calibrated.txt?download=1).

| Item | Value |
|---|---|
| Original bytes | 2,673,975 |
| Original MD5 / provider MD5 | `ae2133eac5c92c695c5f6ef93bcbbd25` |
| Original SHA256 | `c46d93e3dd07c6c91d700a814214716f00caa0d5cc3a520f8969ce0af63ecafd` |
| Gzip bytes | 506,804 |
| Gzip SHA256 | `f2ab00f49fdfa9f64cb2e6fe15df3d32599f382292ba7b2e4b916f75c5f311f1` |
| Compression | Gzip level9, `mtime=0`, empty stored filename |

Only lossless compression was applied. Decompression reproduces the exact source bytes, including line endings and printed timestamps. This is the **author-processed/calibrated export**, not unprocessed logger output. No rows, values, time labels or calibration were changed.

The adjacent `earth_atmosphere.py` and `earth_validate.py` default to this retained gzip and verify compressed SHA256 plus decompressed SHA256/MD5. They need no network or other local raw file. An explicit original path remains supported; when the retained gzip is absent they can fall back to the original repository `data/raw/earth/university_valley/` path.

# ZASA Earth source index — 2026-11-14

Research handoff for MS-01 / MS-02 / MS-03. This index is **not** a mirror of 12.33 GB. The exact original paths, byte sizes, and SHA-256 hashes for **222 science files** are in [earth_inventory.csv](earth_inventory.csv). All 222 original files were independently hash-verified on the source computer. The three notebooks/notes in [historical](historical) are archived planning snapshots, not current assignments, results, or download status; do not treat their stale claims as current.

## Start here
- [23 MB integrated workbook](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/f7076c9fdc77e00244ed5d6863aad2bf78cfa28f/outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx)
- [Full Mars screening CSV archive](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/f7076c9fdc77e00244ed5d6863aad2bf78cfa28f/outputs/research/mars_reselection_20261114/screened_pool.csv.gz)
- [Earlier terrain-only raw-data release](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/releases/tag/terrain-inputs-2026-11-14), separate sources (ETOPO/MOLA/Natural Earth/NASA POWER), not a substitute for this Earth inventory.

## Obtain the original data
In [NASA Earthdata Search](https://search.earthdata.nasa.gov/), find the collection by its short name below, select the listed version, and search Granule by the exact filenames from the CSV (or the filename without the extension when the granule ID omits it). Confirm the downloaded basename, byte length and SHA-256 against the inventory. Use your own Earthdata Login; apply for provider access if prompted. Start with your candidate's relevant products, rather than downloading all data to begin. The archived source plan documents variables and interpretation limits; exact catalog/download identities of original SRTM tiles must be matched by checksum rather than inferred from the filename.

| Folder | Source / collection | Version / periods |
|---|---|---|
| terrain | [SRTMGL30](https://cmr.earthdata.nasa.gov/search/collections.umm_json?short_name=SRTMGL30) | catalog 002; exact tiles in manifest |
| terrain/landcover | [MCD12C1](https://doi.org/10.5067/MODIS/MCD12C1.061) | 061; 2024 |
| temperature | [MOD11C3](https://doi.org/10.5067/MODIS/MOD11C3.061) | 061; 2023–24 monthly |
| temperature/radiation | [M2TMNXRAD](https://data.nasa.gov/dataset/merra-2-tavgm-2d-rad-nx-2dmonthly-meantime-averagedsingle-levelassimilationradiation-diagn-ab39c) | 5.12.4; 2023–24 monthly |
| water_ice/gpm | [GPM_3IMERGM](https://doi.org/10.5067/GPM/IMERG/3B-MONTH/07) | V07B files; 2023–24 monthly |
| water_ice/gldas | [GLDAS_NOAH025_M](https://doi.org/10.5067/SXAVCZFAQLNO) | 2.1; 2023–24 monthly |
| water_ice/ndvi | [MOD13C2](https://doi.org/10.5067/MODIS/MOD13C2.061) | 061; 2023–24 monthly |
| water_ice/permafrost | [ESA CCI via CEDA](https://catalogue.ceda.ac.uk/uuid/93444bc1c4364a59869e004bf9bfd94a/) | 4.0; 2021 exact file; cite DOI 10.5285/93444bc1c4364a59869e004bf9bfd94a, the ESA CCI, Permafrost CCI and dataset providers |
| air | [M2TMNXAER](https://data.nasa.gov/dataset/merra-2-tavgm-2d-aer-nx-2dmonthly-meantime-averagedsingle-levelassimilationaerosol-diagnos-596e4) | 5.12.4; 2023–24 monthly |
| air/viirs | [AERDB_M3_VIIRS_SNPP](https://cmr.earthdata.nasa.gov/search/collections.umm_json?short_name=AERDB_M3_VIIRS_SNPP) | 002; 2022-12 to 2024-12; exclude A2022335 from 2023–24 statistics |
| air/wind_pressure | [M2TMNXSLV](https://data.nasa.gov/dataset/merra-2-tavgm-2d-slv-nx-2dmonthly-meantime-averagedsingle-levelassimilationsingle-level-di-892ac) | 5.12.4; 2023–24 monthly |

### Restore exact files
Put the downloaded files and the inventory in a staging folder. Run `python3 docs/earth-source-handoff/restore_earth.py /path/to/staging data/raw/earth` from the repository root. The script copies only checksum-matching files and never overwrites a different file. It also prints a list of remaining missing files. For a single input without copying, use `shasum -a 256 path/to/file` and compare with the CSV. Original files and source terms/attributions are not relicensed by this handoff.

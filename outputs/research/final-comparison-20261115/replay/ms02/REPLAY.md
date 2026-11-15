# MS-02 reproducibility

## SHARAD and Adventdalen cores from the repository

In the commands below, use the checkout containing the published replay script and point `--repo` to a checkout of pinned input commit `07dbe29203504ba0ccde5e379f42ecc16e4b1b4f`. A newer checkout also works if its inputs match the six embedded SHA-256 checks. Run in Python 3 with NumPy. Tested with Python 3.12.14 and NumPy 2.3.5.

```sh
python3 -I outputs/research/final-comparison-20261115/replay/ms02/replay.py \
    --repo /path/to/input-checkout --out /path/to/new-output
```

The script reads existing versioned NPZs, two Adventdalen core CSVs, and the Mars candidate CSV. No source data are downloaded or duplicated. It regenerates:

- `sharad_echo_fwhm.csv`: 194 widths from the strongest linear-power peak per column and contiguous half-power crossings, plus two comparison conventions. The nominal half-power result has minimum/median/maximum 3.0782/4.0478/10.7064 samples. This is an empirical echo-shape statistic, not a known-ice response or an instrument bandwidth measurement.
- `adventdalen_core_ice_replay.csv`: 12 cores and intact-sample excess-ice aggregation. Positive excess ice does not identify a wedge. These samples are not registered to any available radar line. Data credit: Lotte Wendt (2024), *Ground ice contents and InSAR displacements from Adventdalen, Svalbard*, [Zenodo](https://doi.org/10.5281/zenodo.11187360), CC BY 4.0; changes: selected intact samples and summarized adjoining positive intervals per core.
- `mars_cell_pinned_extraction.csv`: candidate-row fields and geometry checks, not a reprocessing of native global rasters.
- `modeled_velocity_and_orbital_scale.csv`: resolution and hypothetical interface-delay scenarios. They are not direct measurements.
- `replay_summary.json`: result summary including posting from the pinned latitude/longitude arrays.

## Askja, separate inputs

The standard-library scripts in `askja/` use the author-released USGS data [DOI 10.5066/P9QATARQ](https://doi.org/10.5066/P9QATARQ), CC0 1.0. Those rights describe the **USGS data**, not the independently assembled script packages. Raw inputs are not in this folder. Use either the supplied replay ZIPs, or the original USGS archives listed with sizes and hashes in `askja/usgs_source_checksums.csv`. With the original downloads, place each extracted archive into the directory named after that ZIP (without `.zip`), so filenames are immediately below the expected subdirectories. For the alignment and sensitivity scripts the required subdirectories are `Askja_GPR_2019_raw` (lines ICE192__030 and ICE192__031, with extensions as supplied) and `Ice_Thickness_2019_Picks_csv` (matching `_pk_es.csv` files). GIS needs the separately extracted `GPR_Locations_2019_2021_shp` subdirectory with the named DBF/SHP files.

```sh
python3 -I outputs/research/final-comparison-20261115/replay/ms02/askja/recompute_alignment.py /path/to/input-root /path/to/output/alignment
python3 -I outputs/research/final-comparison-20261115/replay/ms02/askja/recompute_sensitivity.py /path/to/input-root /path/to/output/sensitivity
python3 -I outputs/research/final-comparison-20261115/replay/ms02/askja/recompute_gis.py /path/to/input-root /path/to/output/gis
```

For the supplied ZIPs, `MS02_Askja_reproducibility/inputs` supports alignment and sensitivity. GIS ran on the extracted `ZASA_independent_validation_20261115/ms02/inputs`; it can also use the unpacked shapefile source from the Askja package. The evidence verifies navigation, candidate registration hypotheses, and a uniquely matching GIS line ID. It does **not** register B7 to a raw trace, label independent test examples, or establish detector accuracy.

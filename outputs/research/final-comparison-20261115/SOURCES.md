# Source attribution

This directory contains derived comparisons only. Source rights are not
changed and are not replaced by the repository's license. No third-party
raw workbooks, radar files, polygon geometries, or images are redistributed here.

- MS-01: [Victoria Valley and Bull Pass historical observation archive](https://doi.org/10.7931/pa29-rs07)
  (publisher license CC BY-NC 4.0); [USDA NRCS soil climate data](https://www.nrcs.usda.gov/resources/data-and-reports/soil-climate-research-stations);
  [Seybold et al., site context](https://doi.org/10.1017/S0954102010000696).
  Tables contain harmonic and sensitivity calculations, not individual sensor records.
- MS-02: [Shoemaker et al., USGS Askja GPR data](https://doi.org/10.5066/P9QATARQ)
  (CC0 1.0), [field interpretation](https://doi.org/10.1029/2023JE007834),
  and [Jones et al., Bethel measurements](https://doi.org/10.18739/A24B2X68B).
  SHARAD uses the NASA PDS products identified in the pinned repository inputs
  under `outputs/research/MS-02/local_validation/radar_roi/`. Echo widths are
  derived from those stored power columns. Scenarios label their assumptions.
- MS-03: Ulrich, M.; Härtel, S.; Hauber, E. (2020), [Mapped polygon pattern
  geomorphometry from HRSC-AX, 2009, Adventdalen, Svalbard](https://doi.org/10.1594/PANGAEA.921087),
  PANGAEA, CC BY 4.0. Changes: selected the AD1 subset of 185 polygons and
  calculated gridding and overlap metrics at four spacings and 16 origins.
  Cape Blossom contrast results in the overview use the [20 cm flight](https://doi.org/10.1594/PANGAEA.962594)
  and [10 cm flight](https://doi.org/10.1594/PANGAEA.962647).

- MS-02 core summary: Lotte Wendt (2024), [Ground ice contents and InSAR displacements from Adventdalen, Svalbard](https://doi.org/10.5281/zenodo.11187360), Zenodo, CC BY 4.0. Calculations summarize excess ice in intact samples per core; this is separate from the PANGAEA polygon dataset.

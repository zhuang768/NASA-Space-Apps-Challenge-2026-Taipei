# TerraMatch

TerraMatch is Team ZASA's NASA Space Apps 2026 project. We used public data to choose three regions on Mars for follow-up research on shallow ground ice. We then looked for places on Earth where we could test the methods we would use to study those regions.

## What the project shows

The [TerraMatch explorer](https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev/) lets you compare the three Mars regions. Start with the map, then look at slope, thermal inertia and the SWIM ice consistency index. The modeled depths have their own explanation because they depend on assumptions about the material below the surface.

We kept MS-01, MS-02 and MS-03 because they present different research questions. MS-01 has the highest mean thermal inertia of the three. MS-02 is farther south and has more complete thermal inertia coverage, but also higher relief and a higher dust percentile in Mars Year 34. MS-03 has the lowest mean regional slope and the highest shallow SWIM score of the three.

The Earth work gave us specific tests. At Edson Hills we can ask how much of a thermal contrast is due to terrain rather than ice. At Bethel we can ask whether a surface radar separates an ice wedge from the thaw boundary. At Cape Blossom we can test how much polygon geometry is lost at the scale of Mars imagery. We have not confirmed ice at the three Mars sites or established three validated Earth matches.

## Files

- [Selected targets](outputs/research/mars_reselection_20261114/final_candidates.csv) and [fixed study boundaries](outputs/research/mars_reselection_20261114/selected_targets.json)
- [Complete Mars screening results](outputs/research/mars_reselection_20261114/screened_pool.csv.gz)
- [Integrated data workbook](outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx)
- [Numerical rebuild instructions](docs/REPRODUCE.md), [Mars input manifest](config/raw_inputs_manifest.json) and [data attribution](DATA_LICENSES.md)

## Reproducing the Mars analysis

Use a fresh working copy with Python 3.12 and install the packages in `requirements.txt`. Follow the numerical section of the rebuild instructions and use `--skip-report` to avoid regenerating historical report files. The full rebuild checks 11 public source files before processing them and replaces local generated outputs. It reproduces the Mars screening, not the separate Earth literature review or field observations.

NASA, data publishers and the original investigators retain credit for their observations. TerraMatch is an independent team project.

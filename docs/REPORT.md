# Three Mars reconnaissance candidates

Team zasa · MARS-RESELECT-20261114-v1 · selected 14 November 2026

## Research purpose

Identify regional cases worth closer investigation of dry cover and possible shallow subsurface ice, using all Mars products already available to the project. The targets are analysis cells, not boreholes, tested field sites, proven ice resources or approved landing ellipses.

## Selection and footprint

| Target | Center | Nominal footprint | Approximate size, north-south × east-west |
|---|---|---|---|
| MS-01 | 56.75°N, 72.75°E | 56.50-57.00°N, 72.50-73.00°E | 29.64 × 16.25 km |
| MS-02 | 52.75°N, 168.25°E | 52.50-53.00°N, 168.00-168.50°E | 29.64 × 17.94 km |
| MS-03 | 57.75°N, 242.25°E | 57.50-58.00°N, 242.00-242.50°E | 29.64 × 15.81 km |

Coordinates use Mars planetocentric latitude and east-positive longitude. Reported digits identify a grid center; they do not imply surveyed positioning accuracy.

## Method

The new run examined 172,800 nominal 0.5° cells within the available SWIM latitude support in both hemispheres. There were 172,581 cells with finite core descriptors. Requiring positive values in both related SWIM depth-zone descriptors, excluding the eight previous ice-candidate cells and the earlier project exclusion boxes, produced an exploratory pool of 58,238 cells.

The sign condition is a declared research choice, not calibrated proof of ice. Six unweighted objectives compared higher shallow/deeper ice consistency with lower regional slope, relief and MY34/MY35 dust p95. The 453 non-dominated cells are a trade-off set, not a mission-optimal ranking or probability. Twenty-two geographically dispersed cases were selected for review; four received native-cell extraction, and A/D/C were retained as MS-01/MS-02/MS-03. B was held out because it is near an already studied exposure and the full study footprint was unavailable; B was not declared a duplicate.

TES thermal inertia, absolute elevation, coarse temperature, dust seasons/extremes and reliability were explicitly considered as context. There is no justified universal target value for these quantities. Correlated MOLA variables and shared-source SWIM layers do not become independent confirmations simply because they occupy separate columns.

## Native-cell comparison

| Descriptor | MS-01 | MS-02 | MS-03 |
|---|---:|---:|---:|
| Mean slope at approximately 3.7 km baseline (degrees) | 0.287207 | 0.301845 | 0.162753 |
| Cell relief (m) | 76 | 117 | 76 |
| Mean elevation relative to areoid (m) | -3700.9 | -3898.7 | -2548.3 |
| TES thermal inertia, non-infilled | 325.1557 | 217.2690 | 152.8077 |
| TES finite non-infilled cells / 100 | 73 | 93 | 79 |
| SWIM 0-1 m consistency | 0.639225 | 0.692987 | 0.910904 |
| SWIM 1-5 m consistency | 0.647482 | 0.622499 | 0.509972 |
| MY34 mean dust CDOD | 0.119264 | 0.125384 | 0.098215 |
| MY34 dust p95 | 0.222456 | 0.240015 | 0.173362 |
| MY35 mean dust CDOD | 0.107535 | 0.110066 | 0.088660 |
| MY35 dust p95 | 0.180147 | 0.173120 | 0.140962 |
| MCS paired populated MY/Ls bins / 288 | 69 | 75 | 60 |

TES units are J m^-2 K^-1 s^-0.5. SWIM and CDOD are dimensionless. MOLA 64/64 finite cells does not mean every cell contains direct laser observations: the MEGDR contains interpolation and no track-density mask was used. Native-cell values differ from coarsened/interpolated screening-stack values; they are kept separate in the evidence files.

## Why each target is useful

**MS-01:** positive, relatively strong consistency in both ice depth zones occurs together with low regional relief. Its higher thermal inertia provides a contrasting case for follow-up observations that could separate surface materials from subsurface-ice effects. TES interpolation was excluded, leaving 73 valid cells. No hardness, drilling or ice-content inference is supported.

**MS-02:** it is the most equatorward case in this set and has 93 valid non-infilled TES cells. Its ice descriptors are positive while MY34 dust p95 and regional relief are larger. It supports a transparent latitude, thermal-background and dust trade-off question. The wider Phlegra region has substantial prior research; the selected cell must not be presented as an unexplored region.

**MS-03:** regional slope and both years' reconstructed mean/p95 dust are the lowest of this set, while the shallow SWIM descriptor is stronger. Its lower, more variable thermal inertia supplies a different background for investigating interpretation ambiguity. The deeper ice descriptor is lower, TES support is partial, and the nearest MCS coordinate is north of the research cell.

These are reasons to prioritize additional observations, not demonstrated controlled causes or equipment performance.

## Prior-site checks

The bounded review considered the previously inspected NASA EMC EZMars snapshot (381 ROI and 51 EZ polygons), released SWIM4MIM reconnaissance zones, Mashal et al.'s 2025 preferred regions, published ice-exposing impact point tables, existing landing-site coordinates and named proposals including SkyFall AP-105 and Phlegra proposals.

The inherited EZMars geometry snapshot reaches less than 48°N and the inspected SWIM4MIM geometry reaches 51.217655°N. All three candidate footprints lie farther north. Mashal et al.'s 23 preferred regions are restricted to ±50°. These findings apply to those named snapshots, not every past or unpublished proposal. The published Morgan et al. 2025 Table 2 contains 26 impact points; no listed point falls in the three nominal cells. Center distances are context and do not replace complete study-footprint intersections.

Exact-coordinate, regional-alias and intended-use searches found no confirmed same-cell duplicate in the inspected sources. Full Dundas2021 supporting tables, some historical alternative-zone geometries and unpublished proposals remain outside complete exclusion. Therefore **global novelty is not established**. General satellite or geological mapping coverage is not automatically a previously selected or developed site.

Full queries, reading scopes, source links and limitations are in [the audit register](../outputs/research/mars_reselection_20261114/bounded_prior_site_audit.json) and [the Chinese report](../outputs/research/mars_reselection_20261114/report.md).

## Data and engineering limits

Dust remains a native 3° observation-constrained reconstruction, with 669 sols per year. It does not measure local wind or surface deposition. MCS is a 5° model-time-adjusted temperature product; missing QA, bin observation counts and uncertainties preclude qualified local-temperature claims. Populated-bin medians are not annual means, same-sol pairs or daily extremes. Jezero MEDA records are local and failed the project's complete quality filter, so they are not transferred to these targets.

Ice existence, depth, purity, continuity, quantity and extractability; local wind/pressure; material strength; and fine terrain remain unknown. No equipment-specific thresholds or new experiments were established. All three targets are above 50°N and outside the latitude conditions used by MCOA2025 and current SkyFall. They are **conditional ice-investigation targets**, not validated base or landing recommendations.

## Reproducibility and attribution

See [reproduction instructions](REPRODUCE.md), the numerical validation, source hashes and native evidence in the result package. The earlier Earth-analog objective is retained as historical project context and is not completed by finding new Mars targets. Original data retain their providers' attribution and terms; see [data terms](../DATA_LICENSES.md).

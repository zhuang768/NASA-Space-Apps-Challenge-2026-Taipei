# MS-03 evidence replay: AD1 grid-phase geometry

Reproduce the geometry-only grid-phase test on the 185 published polygons from the
Adventdalen Active Ice-Wedge Site (AD1), Svalbard. This is a supporting Earth
method control, not a Cape Blossom analysis or a Mars boundary-detection test.

## Source and run

Ulrich, Härtel & Hauber (2020), [Mapped polygon pattern geomorphometry from HRSC-AX,
2009, Adventdalen, Svalbard](https://doi.org/10.1594/PANGAEA.921087), CC BY 4.0.
Use the unchanged file already tracked in the repository:
`outputs/research/MS-03/polygons_Act-IWS_source.zip`.
The program checks SHA-256
`c75e7568c9fbfc67898f64e9c18681e5dc7e24a1ec272ceafa12c51377b8054e`
before processing. The calculation uses the source shapefile's EPSG:32633
coordinates in metres, not its WGS84 export.

Use CPython 3.12. In the commands below, `REPLAY_DIR` is the directory
containing this README. Run from the repository root and choose a fresh output
directory each time; it is not part of the repository inputs.

```sh
REPLAY_DIR=outputs/research/final-comparison-20261115/replay/ms03
python3.12 -m venv /tmp/zasa-ad1-venv
/tmp/zasa-ad1-venv/bin/python -m pip install -r "$REPLAY_DIR/requirements.txt"
MPLCONFIGDIR=/tmp/zasa-ad1-mpl /tmp/zasa-ad1-venv/bin/python \
  "$REPLAY_DIR/replay_ad1_grid_phases.py" \
  --repo . \
  --output-dir /tmp/zasa-ad1-grid-phase-run
```

## Expected results

Each polygon is rasterized separately at 16 deterministic grid origins per
spacing using cell-center occupancy, then compared to its original vector
outline by intersection over union (IoU). Expect 11,840 trials and:

| Grid spacing | Median IoU across cases | Polygons with IoU ≥ 0.80 at all 16 offsets |
| --- | ---: | ---: |
| 0.50 m | 0.971650 | 185 / 185 |
| 1.00 m | 0.944232 | 185 / 185 |
| 3.00 m | 0.843474 | 118 / 185 |
| 6.11 m | 0.709662 | 8 / 185 |

On the tested stack the three result CSVs are byte-identical to the original
replay: `phase_results.csv` SHA-256
`5072707ff4e21d734b5fcdc76110b03264e90d67275cf4a7e208687d59bf1644`;
`phase_summary.csv` SHA-256
`351d1f87dd66e048176c73c3330123acb42c248d40a640b7e2af0c73b2177b16`;
`per_polygon_phase_summary.csv` SHA-256
`e5e6be55ea4c6be9f1f2afb638d2c554b0ca8ce0d1860db8d6dee00b2a90e96e`.
The timestamped execution receipt and PNG are not byte-reproducibility targets.

Grid offsets are sensitivity cases, not independent observations. The 0.80
threshold is an exploratory geometry test. Neither the threshold nor the
nominal grid spacings model optical blur, crack visibility or interpreter
accuracy. This result does not establish polygons, ice, or a physical
Earth–Mars analogy in the MS-03 footprint.

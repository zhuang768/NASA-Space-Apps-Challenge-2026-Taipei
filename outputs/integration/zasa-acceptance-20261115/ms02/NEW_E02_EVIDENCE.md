# E02: new acquisition/geographic audit only

No generic candidate upgrade. Main already contains the Liu2018 material subcase (AV-06/PW-21), so it is not new evidence here. No repository, report, slides, outreach, or other-site edits.

## New result

[Liu2018 §§4.1.2,5.4, Acknowledgments](https://doi.org/10.1029/2017JF004535) adds an important boundary caveat: the disturbed 0.02 m probe was not the model's top boundary; measured 0.10 m temperature was used. The 30 m bottom boundary came from another lower-Beacon borehole. Deeper temperatures may be influenced by lateral heat flow. These are not an independently measured complete surface-to-30-m column. The paper names the GCMD archive below, but no original hourly series was acquired.

The exact legacy archive was recovered in [NASA CMR](https://cmr.earthdata.nasa.gov/search/concepts/C1214591010-SCIOPS.umm_json). It describes five Dry Valley sites, has no spatial support, no collection-level data URL, and online-access=false. Its granule query returns zero indexed granules. This establishes a metadata route, not global nonexistence of data. The legacy GCMD URL errors; author contact remains a possible route but no outreach was made.

[GTN-P middle Beacon pt/678](https://data.gtn-p.org/view/pt/678) supplies a 19.6 m borehole, −23.1°C reported MAGT over 1999–2008, at −77.84864°,160.60186°, elevation1273m. It has zero downloadable datasets and no related-publication link. [Lower Beacon pt/681](https://data.gtn-p.org/view/pt/681) is 30.62m deep, at −77.80318°,160.71384°, elevation1000m; it also has zero datasets. These are catalogue metadata, not recovered temperature records.

## Bounded coordinate comparison

`coordinate_comparison.csv` and `reproduce.py` convert the already-recorded Liu printed coordinate (77°49′S,160°39′E) and calculate spherical Earth distances:

- Printed anchor to GTN-P middle: **3.730 km**.
- Printed anchor to GTN-P lower: **2.120 km**.
- Middle to lower: **5.696 km**.

These separations are not location errors, common-footprint evidence or proof that either catalogue entry is a specific Liu borehole. The printed coordinate is coarse; datum, survey and registration are missing. Matching depth and investigator do not establish identity. Do not transfer either point to Kowalewski2004/Heldmann2013, or substitute the separate LTER station.

## Decision and exact blocker

Retain E02 only as the already-established, scoped dry-cover/massive-ice thermal-method literature subcase. Independent reanalysis and geographic matching remain **blocked**.

Highest-value missing artefact: original Liu1999–2011 hourly temperatures with channel names, timestamps/time standard, calibration/disturbance flags and actual deployed depths. Also needed: surveyed coordinates/IDs and offsets tying the shallow profile, adjacent19.6m borehole and separate lower-Beacon30m boundary to their deployment records. Only then can the existing material/interface evidence be tested independently. A catalogue summary or published model-fit statistic does not close this gap.

`python reproduce.py` passes11 metadata/coordinate assertions and hashes retained raw metadata. It does not validate ice inference, fit a thermal model, or compare/merge loggers.

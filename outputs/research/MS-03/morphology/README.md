# MS-03 morphology audit — 2026-11-15

Starting SHA: `7b3c865e85ffeb4db81277ef34e9c3f4a318fc9f` on `research/ms-03-earth-analogs`, PR #7. Fixed ROI: 57.50–58.00°N, 242.00–242.50°E, Mars planetocentric/east-positive. No new sites or clock alignment.

**Decision: insufficient evidence; downgrade MS-03-E02 (AD1) to a general method reference, outside the currently supported specific MS-03 pair.** This is not evidence that polygons or fractures are absent. No Mars polygon boundaries or size/shape distributions were measured.

## Evidence supplement and handoff — 2026-11-15

The front of [the research report](../../../../docs/research/MS-03/report.md) now contains separate main-research/GPU handoffs. AD1 remains downgraded;no new Mars polygons were detected or measured. The following supplements supersede the earlier statements below that the2011paper had not yet been obtained or that its nominal HRSC-AX sampling was unverified:

- Mission archive [RDR cumulative index](https://hirise-pds.lpl.arizona.edu/PDS/INDEX/RDRCUMINDEX.TAB):168675271bytes,actual205451rows;204836valid bounding rectangles give zero ROI intersections;615invalid rectangles retained as unknown. The downloaded label declares205302rows,so release consistency is unresolved. Source response last-modified2026-11-03. This independent interface strengthens the bounded catalogue check but does not exclude unlocated/unreleased observations or establish feature absence. [Result](evidence_followup/HiRISE_independent_index_check.json),[invalid rows](evidence_followup/HiRISE_invalid_bbox_rows.csv),[download record](evidence_followup/index_download_manifest.json).
- [Ulrich et al2011 author copy](https://awi-test.eprints-hosting.org/24005/1/Ulr2011a.pdf) actually obtained and focused reading completed at printedpp199–201,203–204. Table3 AD1N185 and13rounded Table4statistics agree with our GIS recomputation. This checks provenance/reproduction,not independent ground truth. Section3.2 states20cm orthoimage sampling,2008image acquisition and1mMarsDEM;raw HRSC raster remains unacquired. Fieldwork2009 and catalogue campaign names are separate metadata contexts. [Reading/hash record](evidence_followup/author_paper_reading.json),[numeric crosscheck](evidence_followup/AD1_published_table_crosscheck.csv).
- Paper§3.2 restricts Mars analysis toPSP_001938_2265 andPSP_002439_2265. [Actual mission-index rows](evidence_followup/published_Mars_image_index_rows.csv) place them around46N92E,outsideMS03. This only resolves that named paper's image scope;no global novelty claim. Apparent switchedN/E numbers in paperp200are not used as valid coordinates.

Full168.7MBindex and copyrighted author PDF remain local,not inGit. Reproduce the supplement after downloading the stated index:

```sh
curl --fail --location https://hirise-pds.lpl.arizona.edu/PDS/INDEX/RDRCUMINDEX.TAB --output /tmp/ms03_HiRISE_RDRCUMINDEX.TAB
/tmp/ms03geo/bin/python scripts/research/MS-03/supplement_ad1_evidence.py --index /tmp/ms03_HiRISE_RDRCUMINDEX.TAB
```

Use the recorded SHA when comparing releases;later downloads may change. Do not reconcile the label/table count difference silently. Published values are transcribed in the script with source locators and checked at printed precision. MRR L/W is still not the paperW/L from largest/smallest diameters. No numerical Earth geometry or image product from the earlier audit was changed by this supplement.

## Deliverables

- [Coverage/interpretation figure](MS03_AD1_coverage_interpretation.png), [PDF](MS03_AD1_coverage_interpretation.pdf).
- [Geometry/observability comparison](observability_comparison.csv).
- [Image inventory: IDs,UTC dates,sampling,angles,footprints,quality,links](image_inventory.csv).
- [AD1 185 per-polygon metrics](AD1_recomputed_geometry.csv), [summary](AD1_geometry_summary.json).
- [Acquisition provenance and hashes](acquisition_manifest.json), [coverage calculation](coverage_summary.json), [native crop provenance](native_crop_provenance.json).

## What was actually accessed

ODE `target=mars,ihid=MRO,minlat=57.5,maxlat=58,westernlon=242,easternlon=242.5,limit=1000` queried CTX/EDR and HiRISE/RDRV11 and RDR. Three CTX products returned; each processed HiRISE query returned zero. This is a bounded catalogue result, not guaranteed complete instrument coverage. The saved server query date differs from the local review date; both are retained. A USGS independent footprint endpoint returned403. Attempts with invalid `RDR_V11` and unlocated EDR are retained as error responses, never counted as no coverage.

All three CTX archive JPEG browses were downloaded. G01 and D01 browses are505×5222 versus5056×52224 source pixels: roughly tenfold sampling reduction (about61m/display pixel), not6m detail. V17 JPEG has full source dimensions but inspected pixels show strong block/quantization artifacts. Native dimensions alone are insufficient quality assurance.

For D01, an HTTP206 byte range retrieved1024 native EDR rows (36000–37023,zero-based;5056samples each), retaining exact bytes in `D01_native_rows.bin.gz`. Its source IMG has5056-byte records,one label record,^IMAGE=2,8-bit unsigned SQROOT DN. No calibration,destriping,interpolation or orthorectification was performed. Samples600–1623 were saved unchanged to `D01_native_crop_DN.png`; display-only1–99% linear stretch usesDN88–104. Visual inspection of that patch found tonal mottling,small crater-like features and striping; no reliably traceable closed fracture network at AD1 scale. This is neither complete ROI inspection nor an absence result. Compressed V17 and older browses do not fill that gap.

A four-corner bilinear locator places the D01 patch roughly at242.201–242.423°E,57.664–57.779°N; this is an approximate locator, not a calibrated camera solution. CTX source index corner latitudes are **areographic**; the locator uses their **ODE planetocentric equivalents**, preserving corner order from the archived index definition. No geodetic inference or precise Mars area/shape measurement is made from the image patch. The centre/east-positive convention is never treated as Earth WGS84.

The tempting nearby HiRISE PSP_006864_2380_RED label was actually downloaded:2008-01-13,0.5m/map pixel,bounding limits57.243063929–57.775298752°N and241.518180244–241.837518391°E. Its easternmost bound lies west of242°E, so it cannot supply pixels inside MS-03. The figure shows its **bounding box**, not a reconstructed footprint. No HiRISE scene outside the ROI substitutes for an inside observation.

## Geometry method and limits

Read only `polygons_Act-IWS.*` from the existing source ZIP; explicitly exclude similarly named `polylines_Act-IWS.*`. ZIP SHA256 `c75e7568c9fbfc67898f64e9c18681e5dc7e24a1ec272ceafa12c51377b8054e`. PRJ gives WGS84 UTM33N (EPSG32633),metres;185 geometries valid. Compute planar A,P,equivalent-circle diameter sqrt(4A/π),circularity4πA/P² and minimum-rotated-rectangle length,width,L/W. These rectangle edges are not the paper's largest/smallest polygon diameters. Vector precision is not image resolution or boundary accuracy;original selection/edge truncation was not re-audited.

AD1 median A=268.361m²,equivalent diameter18.485m (range8.054–50.828m),circularity0.8066,rectangleL/W1.2768. At6.09m/pixel,the diameters would span1.32–8.35pixels,median3.04. These are hypothetical sampling ratios,not a validated detection threshold or measured Mars sizes. No morphology similarity score,test or ranking is reported.

Intersect CTX catalogue corner polygons with the ROI; estimate area via spherical Mars LAEA (R=3389500m,origin57.75N242.25E). If the union covers the entire lon/lat ROI,the coverage fraction is exactly1 by that containment check;this avoids projection vertex-density artifacts. Per-product fractions are approximate:45.5%,82.5%,55.0%;their union covers the nominal cell in the catalogue. This does not mean cloud-free,valid-pixel or sub-AD1-resolution coverage. Footprint JSON coordinates are explicitly Mars,not Earth GeoJSON distances.

## Prior use and next evidence

Source [Ulrich,Härtel,Hauber2020,PANGAEA921087](https://doi.org/10.1594/PANGAEA.921087),CC BY4.0;associated [Ulrich et al.2011,Geomorphology](https://doi.org/10.1016/j.geomorph.2011.07.002). Dataset metadata explicitly identifies Act-IWS=AD1 and prior Svalbard–western Utopia Planitia size/shape comparison. This round read the metadata and actual GIS;full2011paper was not obtained. Do not claim the first AD1 Mars analogy or exclude an earlier MS-03-specific comparison without reading its image/site list.

New project-specific work: fixed-cell CTX/HiRISE catalogue audit, exclusion of a misleading nearby HiRISE scene,recomputed AD1 vector metrics,sampling/quality audit and an explicit downgrade. This is a reproducible applicability check,not new Mars polygon detection or a demonstrated new analogy.

Even confirmed similar shapes would require registered higher-resolution/stereo images,repeat-season observations,material/stratigraphic context and independent subsurface constraints (e.g.co-located radar with penetration/dielectric ambiguities accounted for,or in situ thermal/drill truth) to discuss genesis and ice. Shape,SWIM andlow slope alone cannot establish thermal contraction,ice wedges,depth,purity or resource volume.

## Reproduce

Use Python3.9+ and the pinned environment in `requirements-lock.txt`:

```sh
python3 -m venv /tmp/ms03geo
/tmp/ms03geo/bin/pip install -r outputs/research/MS-03/morphology/requirements-lock.txt
# Optional network reacquisition;stops if CTX catalogue count changes:
/tmp/ms03geo/bin/python scripts/research/MS-03/acquire_morphology.py
/tmp/ms03geo/bin/python scripts/research/MS-03/morphology_geometry.py
/tmp/ms03geo/bin/python scripts/research/MS-03/plot_morphology.py
/tmp/ms03geo/bin/python scripts/research/MS-03/validate_morphology.py
```

The6m sampling is nominal;no newly created high-frequency information. NASA/JPL/MSSS image credits retained;official PDS data are cited as research sources,not a NASA endorsement. AD1 source attribution and CC BY4.0 remain applicable to the vector-derived panel/metrics. Campbell/HOBO files and all timing restrictions remain unchanged.

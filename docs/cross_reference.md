# Earth and Mars data cross-reference

This is a research plan for four topics. The Earthdata collection below was reported by a teammate; its original files and validation logs have not been shared through this repository. Product specifications, reported downloads and executed analyses are separate claims. The completed analysis currently uses ETOPO/MOLA terrain and NASA POWER context, as described in [earth_pipeline.md](earth_pipeline.md).

## Physical scale

Use each body's coordinates and radius to compare windows in kilometres. Mars 1 degree is about 59 km and Earth 1 degree about 111 km along a meridian; longitude distance also varies with latitude. A fixed Earth 0.5-degree grid is not a universal equivalent of a Mars 1-degree grid. The current implementation uses 100 km windows and 4 km sampling, with a 10 km sensitivity run. Sampling does not improve source resolution.

The pipeline convention is `(lat, lon)`, north-to-south latitude, east-positive longitude from -180 to 180. Reprojection, missing data, quality flags, scaling, units and effective resolution must be checked per product.

## Research matrix

| Topic | Mars product | Reported Earth product | Earth quantity and sampling | Supported use and limits |
|---|---|---|---|---|
| Terrain | MOLA elevation; slope and local relief | SRTMGL30, official collection **002**; 27 reported `.dem.zip` tiles | 30 arcsec elevation; reported tile set 60 S to 90 N | Compare slope and relief at compatible physical scales, not absolute elevation. Confirm the actual collection ID and tile metadata before use. Regional DEMs do not establish rover-scale traversability or landing safety. |
| Terrain (land cover) | No direct Mars land-cover class | MCD12C1.061, 1 annual file (2024) | `Majority_Land_Cover_Type_1`; 0.05-degree CMG (3600×7200) | Isolates barren/desert/rock surfaces vs. vegetated or urban land; does not distinguish Mars rock mineralogy. |
| Temperature | TES nighttime thermal inertia, J m^-2 K^-1 s^-0.5; MEDA TIRS ground brightness temp (Jezero sols 700–702, provisional) | MOD11C3.061, 24 reported months in 2023-2024 | Day/night land surface temperature, K; 0.05-degree CMG | The difference of monthly day/night composites is thermal context, not thermal inertia or a calibrated measure of soil hardness. Keep MODIS LST distinct from TES thermal inertia and rover MEDA brightness temp. |
| Temperature (solar/albedo) | TES albedo & solar insolation context | M2TMNXRAD, 24 months in 2023-2024 | `SWGDN` (shortwave radiation), `ALBEDO`, `LWGNT`; 0.5°×0.625° (361×576) | MERRA-2 reanalysis; provides solar-power & surface-albedo context alongside LST. |
| Aridity | Mars surface-environment context; SWIM is a separate subsurface-ice product | GPM_3IMERGM.07, 24 reported months | Precipitation rate, mm/hr; 0.1-degree grid | Characterize Earth precipitation and aridity. Convert rates to accumulated precipitation using elapsed hours where required. Low precipitation does not establish ice consistency or preservation of particular materials. |
| Soil moisture | SWIM shallow/deep ice consistency, -1 to +1 | GLDAS_NOAH025_M.2.1, 24 reported months | SoilMoi0_10cm_inst, kg m^-2; 0.25-degree grid | GLDAS is land-surface model output, not direct satellite observation. Describe Earth surface soil water separately; it is not equivalent to buried ice at 1-5 m or the SWIM score. |
| Vegetation | No cross-planet NDVI score has been defined | MOD13C2.061, 24 reported months | Monthly NDVI with quality flags; 0.05-degree CMG | Screen vegetation after QA. Low or negative NDVI may also reflect water, snow or poor retrievals. It does not demonstrate absence of life or biosignatures. |
| Permafrost | SWIM subsurface-ice evidence | ESA CCI Permafrost v4.0; teammate reports one 2021 file | PFR and PFR_uncertainty, percent; reported 0.01-degree grid, 25 N to 85 N | PFR is model-derived permafrost area fraction, not volumetric ice content, depth, purity or extractability. The product series spans 1997-2021; only the 2021 selection is reported locally. Check valid-data masks within the nominal grid. This supports frozen-ground context, not a direct ISRU water-resource match. |
| Air and dust | Montabone MY34/MY35 CDOD | M2TMNXAER (24 months) + AERDB_M3_VIIRS_SNPP (25 months) + M2TMNXSLV (24 months) | `DUEXTTAU` (0.5°×0.625° reanalysis), VIIRS 550 nm land AOD (1°, `180×360`), `U10M`/`V10M`/`PS` (wind & pressure) | VIIRS provides direct satellite AOD alongside MERRA-2 `DUEXTTAU` reanalysis; `M2TMNXSLV` quantifies Earth ~101 kPa vs. Mars ~0.6 kPa atmospheric limit. Align wavelength, pressure normalization, and seasons before quantitative comparison. |

Geology, minerals, caves and field operations require independent evidence. Copernicus/Sentinel, CSA RADARSAT, JAXA ALOS, Worldview and Mars Trek are potential sources; listing them does not mean relevant imagery or measurements have been acquired.

## Inventory and reading

The reported counts imply **27 + 5 x 24 + 1 = 148 files**. Earlier notes reported 145 files opened. This discrepancy remains unresolved; 148 is an inventory expectation, not a newly verified download or successful-read count. Require filenames, byte sizes, hashes, product IDs, periods and read logs before claiming completeness. The approximate 7.6 GB total is teammate-reported.

- GPM HDF5: start with `xr.open_dataset(path, group="Grid")`, then verify dimension order, fill values, units and QA.
- GLDAS/MERRA-2/permafrost NetCDF: inspect coordinate orientation, masks and metadata before combining files.
- MODIS HDF4-EOS: `netCDF4.Dataset` works only when the linked netCDF-C library was built with HDF4 SD support. The teammate reported successful reads in their environment; this is not a guarantee for another wheel or machine. If unavailable, use an HDF4-capable reader or convert with a verified tool. Preserve scale factors, offsets, fill values and quality flags.
- For standard global MODIS CMG files of 3600 by 7200 cells, verify the file's extent and ordering before assigning centres at latitudes 89.975 to -89.975 and longitudes -179.975 to 179.975.
- The teammate reports raw big-endian SRTM `.DEM` tiles without `.HDR` files. Verify tile dimensions and bounds from metadata and byte counts; filenames alone are not sufficient proof of the product version.

## Evidence and scoring

There is no validated four-topic combined score yet. Unknown conditions stay unknown. Permafrost outside coverage is not zero; no NDVI is not evidence of no life. SWIM consistency is not ice probability or quantity. Candidate novelty, mineralogy, co-occurring conditions and logistics need separate checks.

## Sources checked on 2026-11-14

- [NASA CMR SRTMGL30 collection metadata](https://cmr.earthdata.nasa.gov/search/collections.umm_json?short_name=SRTMGL30): collection 002; not updated for the SRTM V3 release. Actual teammate files remain unverified.
- [MODIS LST product](https://doi.org/10.5067/MODIS/MOD11C3.061) and [NDVI product](https://doi.org/10.5067/MODIS/MOD13C2.061).
- [NASA GPM IMERG](https://gpm.nasa.gov/data/imerg) and [GLDAS monthly product](https://doi.org/10.5067/SXAVCZFAQLNO).
- [ESA/CEDA permafrost extent v4.0](https://catalogue.ceda.ac.uk/uuid/93444bc1c4364a59869e004bf9bfd94a/): thermal-model derivation, PFR meaning and temporal extent.
- [Unidata HDF4 build requirements](https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html).

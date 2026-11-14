"""Public Earth terrain and explicit Earthdata product discovery/download.

No credentials are stored in the project. Earthdata login is non-interactive.
"""

import zipfile
from pathlib import Path

import numpy as np
import rasterio
import xarray as xr
from rasterio.enums import Resampling

from analog.mars import _fetch
from analog.provenance import source_record, write_json

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data/raw/earth"
ETOPO_URL = (
    "https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO2022/data/60s/"
    "60s_surface_elev_gtif/ETOPO_2022_v1_60s_N90W180_surface.tif"
)
LAND_URL = "https://naciscdn.org/naturalearth/110m/physical/ne_110m_land.zip"
# A bounded discovery/download plan, not a claim that every source is accessible.
PRODUCTS = {
    "lst": {
        "short_name": "MOD11C3",
        "version": "061",
        "native_resolution": "0.05 degree",
        "role": "Earth day/night LST context; not equal to TES thermal inertia",
    },
    "ndvi": {
        "short_name": "MOD13C2",
        "version": "061",
        "native_resolution": "0.05 degree",
        "role": "vegetation context; not a subsurface ice measure",
    },
    "precipitation": {
        "short_name": "GPM_3IMERGM",
        "version": "07",
        "native_resolution": "0.1 degree",
        "role": "Earth precipitation context",
    },
    "aod": {
        "short_name": "MOD08_M3",
        "version": "6.1",
        "native_resolution": "1 degree",
        "role": "550 nm aerosol context; no uncalibrated subtraction from Mars CDOD",
    },
    "soil_moisture": {
        "short_name": "SPL3SMP_E",
        "version": None,
        "native_resolution": "9 km EASE-Grid 2.0",
        "role": "daily regional follow-up only; not a monthly global product",
    },
}


def download_public(raw_dir=RAW_DIR):
    records = []
    for url, metadata in [
        (
            ETOPO_URL,
            {
                "dataset": "ETOPO 2022",
                "version": "v1",
                "units": "m",
                "resolution": "60 arcsec native; averaged to 120 arcsec for screening",
                "crs": "source GeoTIFF geographic CRS",
                "vertical_datum": "EGM2008",
                "period": "static composite, 2022 release",
            },
        ),
        (
            LAND_URL,
            {
                "dataset": "Natural Earth land",
                "version": "4.1.0",
                "resolution": "1:110 million cartographic polygons",
                "crs": "EPSG:4326",
                "units": "polygon mask",
                "period": "static",
            },
        ),
    ]:
        path = _fetch(url, Path(raw_dir) / url.rsplit("/", 1)[1])
        if url == LAND_URL:
            with zipfile.ZipFile(path) as archive:
                name = next(n for n in archive.namelist() if n.endswith("VERSION.txt"))
                metadata["version"] = archive.read(name).decode().strip()
        else:
            with rasterio.open(path) as src:
                metadata["crs"] = str(src.crs)
                metadata["native_dimensions"] = [src.height, src.width]
        records.append(source_record(path, url, **metadata))
    write_json(Path(raw_dir) / "public_sources.json", records)
    return records


def load_terrain(path=None):
    """Area-average 60 arcsec terrain into 120 arcsec cells (no new detail)."""
    path = path or RAW_DIR / ETOPO_URL.rsplit("/", 1)[1]
    with rasterio.open(path) as src:
        height, width = src.height // 2, src.width // 2
        data = (
            src.read(1, out_shape=(height, width), resampling=Resampling.average, masked=True)
            .filled(np.nan)
            .astype("float32")
        )
        transform = src.transform * src.transform.scale(src.width / width, src.height / height)
        lat = transform.f + (np.arange(height) + 0.5) * transform.e
        lon = transform.c + (np.arange(width) + 0.5) * transform.a
        return xr.DataArray(
            data,
            dims=("lat", "lon"),
            coords={"lat": lat, "lon": lon},
            attrs={
                "units": "m",
                "source_crs": str(src.crs),
                "vertical_datum": "EGM2008",
                "aggregation": "2x2 mean",
            },
        )


def discover_monthly(product, start="2023-01-01", end="2024-12-31"):
    import earthaccess

    if product not in PRODUCTS or product == "soil_moisture":
        raise ValueError("Choose a monthly product: lst, ndvi, precipitation, aod")
    spec = PRODUCTS[product]
    # Discovery is public; downloading data can require Earthdata Login.
    found = earthaccess.search_data(
        short_name=spec["short_name"], version=spec["version"], temporal=(start, end), count=-1
    )
    # CMR intersects intervals: exclude a preceding month's granule ending on start day.
    return [
        item
        for item in found
        if start <= item["umm"]["TemporalExtent"]["RangeDateTime"]["BeginningDateTime"][:10] <= end
    ]


def download_monthly(product, start="2023-01-01", end="2024-12-31", download=False):
    granules = discover_monthly(product, start, end)
    records = [
        {
            "concept_id": item["meta"]["concept-id"],
            "granule_id": item["umm"]["GranuleUR"],
            "urls": item.data_links(),
            "temporal_extent": item["umm"]["TemporalExtent"],
        }
        for item in granules
    ]
    manifest = {
        "product": PRODUCTS[product],
        "start": start,
        "end": end,
        "granules": records,
        "status": "discovered_not_downloaded",
    }
    if download:
        import earthaccess

        if not (Path.home() / ".netrc").is_file():
            raise RuntimeError(
                "No local .netrc found; discovery works without login, download needs it"
            )
        auth = earthaccess.login(strategy="netrc", persist=False)
        if not auth.authenticated:
            raise RuntimeError(
                "Earthdata login unavailable; configure locally, never commit credentials"
            )
        paths = earthaccess.download(granules, RAW_DIR / product)
        if len(paths) != len(granules) or not all(Path(p).is_file() for p in paths):
            raise RuntimeError("Incomplete Earthdata download; no completed manifest written")
        manifest["files"] = [source_record(path, "see granule URLs") for path in paths]
        manifest["status"] = "downloaded_not_processed"
    write_json(RAW_DIR / f"{product}_manifest.json", manifest)
    return manifest

"""Martian airborne-dust climatology (Montabone et al., v2.x).

Column dust optical depth (CDOD) gridded from NASA TES, THEMIS and MCS
observations, distributed as netCDF at www-mars.lmd.jussieu.fr. These are the
dust scenarios used by the Mars Climate Database. Direct download, no login.

MY34 (2017-2019) contains a global dust storm; MY35 is a more typical year.
"""

from __future__ import annotations

from pathlib import Path

import xarray as xr

from analog.mars import RAW_DIR, _fetch

_BASE = "https://www-mars.lmd.jussieu.fr/mars/dust_climatology/dataset_v2"

PRODUCTS = {
    # Kriged regular daily maps of column dust optical depth, one Mars year each.
    "dust_my35": f"{_BASE}/dustscenario_MY35_v2-5.nc",
    "dust_my34": f"{_BASE}/dustscenario_MY34_v2-5.nc",
}


def open_dataset(path: Path):
    """Use SciPy for the provider's classic NetCDF files; retain a fallback for NetCDF4."""
    with Path(path).open("rb") as stream:
        classic = stream.read(4) in (b"CDF\x01", b"CDF\x02")
    return xr.open_dataset(path, engine="scipy" if classic else "netcdf4", decode_times=False)


def download(name: str, raw_dir: Path = RAW_DIR) -> Path:
    url = PRODUCTS[name]
    return _fetch(url, raw_dir / url.rsplit("/", 1)[1])


def load_mean_cdod(name: str = "dust_my35", raw_dir: Path = RAW_DIR) -> xr.DataArray:
    """Annual-mean column dust optical depth as a (lat, lon) DataArray.

    The file stores daily kriged maps (time, latitude, longitude); averaging
    over the Mars year gives a 'how dusty is it here' climatology.
    """
    url = PRODUCTS[name]
    path = raw_dir / url.rsplit("/", 1)[1]
    if not path.exists():
        raise FileNotFoundError(f"{path} is missing; run scripts/download_mars.py first")
    with open_dataset(path) as ds:
        # cdodtot is the local total column; cdod610 is normalized to 610 Pa.
        # cdodrel is a reliability value, NOT a pressure-normalised optical depth.
        cdod = ds["cdodtot"].mean(dim="Time").load()
    rename = {}
    for dim in cdod.dims:
        if dim.lower().startswith("lat"):
            rename[dim] = "lat"
        elif dim.lower().startswith("lon"):
            rename[dim] = "lon"
    cdod = cdod.rename(rename).sortby("lat", ascending=False).rename("mean_cdod")
    if cdod.lon.max() > 180:
        cdod = cdod.assign_coords(lon=((cdod.lon + 180) % 360) - 180).sortby("lon")
    return cdod


def load_site_series(lat: float, lon: float, name: str = "dust_my35", raw_dir: Path = RAW_DIR):
    """Nearest native 3-degree cell, preserving time, season and source metadata.

    These are complete-coverage kriged scenarios, not direct local measurements.
    No conversion from 9.3-micron absorption to visible extinction is applied.
    """
    import numpy as np

    if not -90 <= lat <= 90 or not np.isfinite(lon):
        raise ValueError("A finite Mars latitude/longitude is required")
    path = raw_dir / PRODUCTS[name].rsplit("/", 1)[1]
    with open_dataset(path) as ds:
        if "latitude" not in ds.coords or "longitude" not in ds.coords:
            raise ValueError("Expected native dust latitude/longitude coordinates")
        yi = int(np.abs(ds.latitude.values - lat).argmin())
        delta = (ds.longitude.values - lon + 180) % 360 - 180
        xi = int(np.abs(delta).argmin())
        site = (
            ds[["cdodtot", "cdod610", "cdodrel", "Ls", "SOY"]]
            .isel(latitude=yi, longitude=xi)
            .load()
        )
        site.attrs = dict(ds.attrs)
        site.attrs.update(
            extraction="nearest native cell; no spatial upsampling",
            wavelength_micron=9.3,
            optical_quantity="infrared absorption optical depth",
            reconstruction="iterative weighted binning and kriging",
        )
    return site

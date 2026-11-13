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
    with xr.open_dataset(path) as ds:
        # cdodtot is the actual total column; cdod610 and cdodrel are
        # pressure-normalised variants used for atmospheric modelling.
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

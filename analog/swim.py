"""SWIM 2.0 subsurface water-ice consistency maps for Mars.

Direct GeoTIFF downloads from the NASA-funded SWIM project (swim.psi.edu),
no login needed. Values are ice-consistency scores from -1 (evidence against
ice) to +1 (strong evidence for ice); the maps cover roughly 60S to 60N.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import rasterio
import xarray as xr

from analog.mars import RAW_DIR, _fetch

_BASE = "https://swim.psi.edu/output/SWIM2/Global/Composite"

PRODUCTS = {
    # Composite ice consistency for ice shallower than about 1 m.
    "ice_consistency_shallow": f"{_BASE}/SWIM2_c0_1.tif",
    # Composite ice consistency for depths of about 1 to 5 m.
    "ice_consistency_deep": f"{_BASE}/SWIM2_c1_5.tif",
}


def download(name: str, raw_dir: Path = RAW_DIR) -> Path:
    url = PRODUCTS[name]
    return _fetch(url, raw_dir / url.rsplit("/", 1)[1])


def load(name: str, raw_dir: Path = RAW_DIR) -> xr.DataArray:
    """Load a SWIM map as a (lat, lon) DataArray in degrees, NaN outside coverage."""
    url = PRODUCTS[name]
    path = raw_dir / url.rsplit("/", 1)[1]
    if not path.exists():
        raise FileNotFoundError(f"{path} is missing; run scripts/download_mars.py first")
    with rasterio.open(path) as src:
        data = src.read(1).astype("float32")
        if src.nodata is not None:
            data[data == src.nodata] = np.nan
        transform = src.transform
        # Mars equirectangular: convert projected metres to degrees if needed.
        to_degrees = 1.0
        if src.crs and src.crs.is_projected:
            spheroid = re.search(r'SPHEROID\["[^"]*",\s*([\d.]+)', src.crs.to_wkt())
            if not spheroid:
                raise ValueError(f"{path.name}: cannot find the body radius in the CRS")
            to_degrees = 180.0 / (np.pi * float(spheroid.group(1)))
        cols = np.arange(src.width) + 0.5
        rows = np.arange(src.height) + 0.5
        lon = (transform.c + cols * transform.a) * to_degrees
        lat = (transform.f + rows * transform.e) * to_degrees
    grid = xr.DataArray(data, dims=("lat", "lon"), coords={"lat": lat, "lon": lon}, name=name)
    if grid.lon.max() > 180:
        grid = grid.assign_coords(lon=((grid.lon + 180) % 360) - 180).sortby("lon")
    return grid

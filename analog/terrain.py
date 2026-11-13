"""Terrain measures that can be compared between planets.

Elevation itself is not comparable (different datums), but slope and local
relief are, as long as both planets are sampled at a similar ground distance.
"""

from __future__ import annotations

import numpy as np
import xarray as xr


def slope_deg(dem: xr.DataArray, radius_m: float) -> xr.DataArray:
    """Slope in degrees from a (lat, lon) elevation grid in metres.

    Uses centred differences. Longitude wraps around when the grid is global.
    """
    lat = np.deg2rad(dem.lat.values)
    lon = np.deg2rad(dem.lon.values)
    dlat = abs(lat[1] - lat[0])
    dlon = abs(lon[1] - lon[0])
    z = dem.values.astype("float64")

    dz_dy = np.gradient(z, axis=0) / (radius_m * dlat)
    is_global = np.isclose(dlon * lon.size, 2 * np.pi)
    if is_global:
        dz_dlon = (np.roll(z, -1, axis=1) - np.roll(z, 1, axis=1)) / 2
    else:
        dz_dlon = np.gradient(z, axis=1)
    dz_dx = dz_dlon / (radius_m * dlon * np.cos(lat)[:, None])

    slope = np.degrees(np.arctan(np.hypot(dz_dx, dz_dy)))
    return xr.DataArray(slope, dims=dem.dims, coords=dem.coords, name="slope_deg")


def block_stats(grid: xr.DataArray, factor: int) -> xr.Dataset:
    """Summarise ``factor`` x ``factor`` blocks of cells: mean, std and relief (max - min)."""
    blocks = grid.coarsen(lat=factor, lon=factor, boundary="trim")
    return xr.Dataset(
        {
            "mean": blocks.mean(),
            "std": blocks.std(),
            "relief": blocks.max() - blocks.min(),
        }
    )

"""Assemble the Mars comparison layers on one global 0.5-degree grid.

0.5 degrees is about 30 km on Mars and 55 km on Earth; fine enough to keep
regional character, coarse enough that the global grids stay small.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import xarray as xr

from analog import dust, mars, swim
from analog.terrain import block_stats, slope_deg

GRID_STEP = 0.5
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


def target_grid() -> tuple[np.ndarray, np.ndarray]:
    """Cell-centre latitudes (north to south) and longitudes of the common grid."""
    lat = np.arange(90 - GRID_STEP / 2, -90, -GRID_STEP)
    lon = np.arange(-180 + GRID_STEP / 2, 180, GRID_STEP)
    return lat, lon


def _onto_grid(grid: xr.DataArray) -> xr.DataArray:
    """Interpolate a (lat, lon) grid onto the common grid (NaN outside coverage)."""
    lat, lon = target_grid()
    return grid.interp(lat=lat, lon=lon, method="linear")


def _coarsen_factor(grid: xr.DataArray) -> int:
    per_degree = round(grid.lat.size / 180)
    factor = round(per_degree * GRID_STEP)
    if factor < 1:
        raise ValueError("source grid is coarser than the target grid")
    return factor


def build_mars_stack() -> xr.Dataset:
    """Compute all Mars layers on the common grid. Needs the downloaded raw data."""
    topo = mars.load("mola_topography").astype("float32")
    factor = _coarsen_factor(topo)
    slope = block_stats(slope_deg(topo, mars.MARS_RADIUS_M), factor)["mean"]
    relief = block_stats(topo, factor)["relief"]

    inertia = mars.load_thermal_inertia()
    inertia = block_stats(inertia, _coarsen_factor(inertia))["mean"]

    ice = swim.load("ice_consistency_shallow")
    ice = ice.coarsen(lat=_coarsen_factor(ice), lon=_coarsen_factor(ice), boundary="trim").mean()

    stack = xr.Dataset(
        {
            "slope": _onto_grid(slope),
            "relief": _onto_grid(relief),
            "thermal_inertia": _onto_grid(inertia),
            "ice_shallow": _onto_grid(ice),
            "dust_cdod": _onto_grid(dust.load_mean_cdod("dust_my35")),
        }
    )
    stack.slope.attrs.update(units="deg", description="mean slope at 3.7 km baseline (MOLA)")
    stack.relief.attrs.update(units="m", description="elevation range within the cell (MOLA)")
    stack.thermal_inertia.attrs.update(
        units="J m-2 K-1 s-0.5", description="TES nightside thermal inertia"
    )
    stack.ice_shallow.attrs.update(
        units="-1..1", description="SWIM 2.0 ice consistency, <1 m depth, +-60 lat only"
    )
    stack.dust_cdod.attrs.update(
        units="optical depth", description="MY35 mean column dust optical depth (Montabone v2)"
    )
    # Polar rows come from coordinate singularities, not measurements.
    return stack.where((stack.lat < 87) & (stack.lat > -87))


def save(stack: xr.Dataset, name: str = "mars_stack_0p5deg.nc") -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / name
    stack.to_netcdf(path)
    return path


def load_stack(name: str = "mars_stack_0p5deg.nc") -> xr.Dataset:
    path = PROCESSED_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"{path} is missing; run scripts/build_mars_stack.py first")
    return xr.open_dataset(path)

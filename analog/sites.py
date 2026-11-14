"""Mars reference sites and their multi-layer signatures."""

from __future__ import annotations

from dataclasses import dataclass

import xarray as xr


@dataclass(frozen=True)
class Box:
    """A lat/lon box; latitudes in degrees north, longitudes in degrees east."""

    south: float
    north: float
    west: float
    east: float


# Candidate human-landing and science regions.
SITES = {
    # Flat northern plains with shallow ice; leading human-landing candidate.
    "arcadia_planitia": Box(south=38, north=48, west=-180, east=-160),
    # Perseverance landing site: ancient lake and delta.
    "jezero_crater": Box(south=17.5, north=19.5, west=76.5, east=78.5),
    # Viking 2 / ice-rich plains, another landing-study region.
    "utopia_planitia": Box(south=40, north=50, west=110, east=130),
}


def select(stack: xr.Dataset, box: Box) -> xr.Dataset:
    """Cells of the stack inside the box (latitude is stored north to south)."""
    return stack.sel(lat=slice(box.north, box.south), lon=slice(box.west, box.east))


def signature(stack: xr.Dataset, box: Box) -> xr.Dataset:
    """Median and robust spread (IQR) of every layer inside the box."""
    cells = select(stack, box)
    quartiles = cells.quantile([0.25, 0.5, 0.75], dim=("lat", "lon"))
    return xr.Dataset(
        {
            "median": quartiles.sel(quantile=0.5, drop=True).to_dataarray("layer"),
            "iqr": (
                quartiles.sel(quantile=0.75, drop=True) - quartiles.sel(quantile=0.25, drop=True)
            ).to_dataarray("layer"),
        }
    )

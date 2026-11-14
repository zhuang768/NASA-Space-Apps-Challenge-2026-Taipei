"""Common physical sampling of Earth and Mars DEMs for regional screening.

A 100 km square is sampled at 4 km spacing in local spherical azimuthal
 equidistant coordinates. Bilinear sampling is an approximation, not new detail.
"""

import zipfile

import numpy as np
import shapefile
from scipy.ndimage import map_coordinates
from shapely import contains_xy
from shapely.geometry import shape
from shapely.ops import unary_union

EARTH_RADIUS_M = 6371008.8
TARGETS = {
    "jezero": {
        "lat": 18.44,
        "lon": 77.45,
        "label": "Jezero regional terrain",
        "coordinate_source": "https://ntrs.nasa.gov/citations/20230016428",
    },
    "gale": {
        "lat": -4.59,
        "lon": 137.44,
        "label": "Gale regional terrain",
        "coordinate_source": "https://doi.org/10.1002/2013JE004576",
    },
    "arcadia": {
        "lat": 40.0,
        "lon": -170.0,
        "label": "Arcadia design target (not a selected landing site)",
        "coordinate_source": "project design assumption",
    },
}
# Explicit broad exclusions requested by the team; not a literature novelty test.
EXCLUDED = [
    (-81, -65, -31, -17, "Atacama search exclusion"),
    (-26, -12, 62, 68, "Iceland"),
    (-161, -154, 18, 23, "Hawaii"),
]


def land_geometry(path):
    with zipfile.ZipFile(path) as archive:
        base = next(name[:-4] for name in archive.namelist() if name.endswith(".shp"))
        reader = shapefile.Reader(
            shp=archive.open(base + ".shp"),
            shx=archive.open(base + ".shx"),
            dbf=archive.open(base + ".dbf"),
        )
        return unary_union([shape(item.__geo_interface__) for item in reader.shapes()])


def local_coordinates(lat, lon, radius_m, spacing_km=4.0, window_km=100.0):
    if (
        spacing_km <= 0
        or window_km <= 0
        or not np.isclose(window_km / spacing_km, round(window_km / spacing_km))
    ):
        raise ValueError("Window must contain an integer number of positive sampling intervals")
    # Both edges are included: 26 samples for 25 intervals of 4 km.
    axis = np.linspace(-window_km / 2, window_km / 2, round(window_km / spacing_km) + 1)
    x, y = np.meshgrid(axis * 1000, axis * 1000)
    distance = np.hypot(x, y) / radius_m
    bearing = np.arctan2(x, y)
    phi = np.deg2rad(lat)
    phi2 = np.arcsin(
        np.clip(
            np.sin(phi) * np.cos(distance) + np.cos(phi) * np.sin(distance) * np.cos(bearing), -1, 1
        )
    )
    lam2 = np.deg2rad(lon) + np.arctan2(
        np.sin(bearing) * np.sin(distance) * np.cos(phi),
        np.cos(distance) - np.sin(phi) * np.sin(phi2),
    )
    return np.rad2deg(phi2), (np.rad2deg(lam2) + 180) % 360 - 180


def sample_patch(grid, lat, lon, radius_m, spacing_km=4.0, window_km=100.0):
    qlat, qlon = local_coordinates(lat, lon, radius_m, spacing_km, window_km)
    dlat = float(grid.lat[1] - grid.lat[0])
    dlon = float(grid.lon[1] - grid.lon[0])
    if dlat >= 0 or dlon <= 0 or not np.isclose(dlon * grid.lon.size, 360):
        raise ValueError("Expected north-to-south global east-positive regular grid")
    rows = (qlat - float(grid.lat[0])) / dlat
    centre_col = (lon - float(grid.lon[0])) / dlon
    cols = centre_col + ((qlon - lon + 180) % 360 - 180) / dlon
    r0 = max(0, int(np.floor(rows.min())) - 1)
    r1 = min(grid.lat.size, int(np.ceil(rows.max())) + 2)
    c0, c1 = int(np.floor(cols.min())) - 1, int(np.ceil(cols.max())) + 2
    indices = np.arange(c0, c1) % grid.lon.size
    data = grid.values[r0:r1, :][:, indices]
    patch = map_coordinates(data, [rows - r0, cols - c0], order=1, mode="nearest", prefilter=False)
    patch[(rows < 0) | (rows > grid.lat.size - 1)] = np.nan
    return patch, qlat, qlon


def patch_features(patch, spacing_km=4.0):
    if not np.isfinite(patch).all():
        return np.full(3, np.nan)
    dy, dx = np.gradient(patch, spacing_km * 1000)
    # Interior centred differences: 8 km stencil when spacing is 4 km.
    slopes = np.rad2deg(np.arctan(np.hypot(dx[1:-1, 1:-1], dy[1:-1, 1:-1])))
    return np.array([np.median(slopes), np.percentile(slopes, 90), np.ptp(patch)])


def search_centres(land, step=2.0):
    if step <= 0 or step > 10:
        raise ValueError("Search step must be in (0, 10] degrees")
    lon, lat = np.meshgrid(
        np.arange(-180 + step / 2, 180, step), np.arange(-60 + step / 2, 60, step)
    )
    keep = contains_xy(land, lon, lat)
    for west, east, south, north, _ in EXCLUDED:
        keep &= ~((lon >= west) & (lon <= east) & (lat >= south) & (lat <= north))
    return lat[keep], lon[keep]

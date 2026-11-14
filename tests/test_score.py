import numpy as np
import xarray as xr

from analog.score import similarity, top_cells
from analog.sites import Box, signature


def toy_stack():
    lat = np.arange(89.75, -90, -0.5)[:40]  # 89.75 .. 70.25
    lon = np.arange(-179.75, 180, 0.5)[:40]
    lon2d, lat2d = np.meshgrid(lon, lat)
    # Layer a: gradient west to east; layer b: gradient north to south.
    a = xr.DataArray(lon2d, dims=("lat", "lon"), coords={"lat": lat, "lon": lon})
    b = xr.DataArray(lat2d, dims=("lat", "lon"), coords={"lat": lat, "lon": lon})
    return xr.Dataset({"a": a, "b": b})


def test_signature_median_matches_box_centre():
    stack = toy_stack()
    box = Box(south=75, north=80, west=-170, east=-165)
    sig = signature(stack, box)
    assert abs(float(sig["median"].sel(layer="a")) - (-167.5)) < 0.5
    assert abs(float(sig["median"].sel(layer="b")) - 77.5) < 0.5


def test_similarity_peaks_inside_target_box():
    stack = toy_stack()
    box = Box(south=75, north=80, west=-170, east=-165)
    score = similarity(stack, signature(stack, box))
    assert float(score.max()) <= 1.0
    best = top_cells(score, n=1)[0]
    assert box.south <= best["lat"] <= box.north
    assert box.west <= best["lon"] <= box.east


def test_similarity_scores_cells_with_partial_data():
    stack = toy_stack()
    stack["a"][:, :20] = np.nan  # western half has only layer b
    box = Box(south=75, north=80, west=-170, east=-165)
    score = similarity(stack, signature(stack, box))
    west = score.sel(lat=77.75, lon=-175.25)
    assert np.isfinite(float(west))


def test_top_cells_keeps_separation():
    stack = toy_stack()
    box = Box(south=75, north=80, west=-170, east=-165)
    picks = top_cells(similarity(stack, signature(stack, box)), n=3, separation_deg=5)
    for i, p in enumerate(picks):
        for q in picks[i + 1 :]:
            assert abs(p["lat"] - q["lat"]) >= 5 or abs(p["lon"] - q["lon"]) >= 5

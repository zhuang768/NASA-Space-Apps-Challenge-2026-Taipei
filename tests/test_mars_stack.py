import numpy as np
import pytest
import xarray as xr

from analog.mars_profiles import validate_targets
from analog.score import similarity, top_cells
from analog.stack import _coarsen_factor, _onto_grid


def test_partial_latitude_grid_uses_coordinate_spacing():
    lat = np.arange(59.975, -60, -0.05)
    g = xr.DataArray(
        np.zeros((len(lat), 2)), dims=("lat", "lon"), coords={"lat": lat, "lon": [0, 0.05]}
    )
    assert _coarsen_factor(g) == 10


def test_coarse_dust_context_keeps_native_values_and_wraps():
    lat = np.arange(88.5, -90, -3)
    lon = np.arange(-178.5, 180, 3)
    values = np.broadcast_to(np.arange(len(lon)), (len(lat), len(lon))).astype(float)
    g = xr.DataArray(values, dims=("lat", "lon"), coords={"lat": lat, "lon": lon})
    out = _onto_grid(g, method="nearest")
    assert np.isfinite(out.sel(lat=0.25).values).all()
    assert set(np.unique(out.values[np.isfinite(out.values)])) == set(range(120))


def example():
    ds = xr.Dataset(
        {"a": (("lat", "lon"), [[2.0]]), "b": (("lat", "lon"), [[np.nan]])},
        coords={"lat": [0.0], "lon": [0.0]},
    )
    sig = xr.Dataset(
        {"median": ("layer", [0.0, 0.0]), "iqr": ("layer", [1.0, 1.0])},
        coords={"layer": ["a", "b"]},
    )
    return ds, sig


def test_default_similarity_does_not_reward_missing_layers():
    ds, sig = example()
    out = similarity(ds, sig)
    assert np.isnan(float(out))
    assert float(out.evidence_fraction) == 0.5


def test_partial_similarity_normalizes_available_weights():
    ds, sig = example()
    out = similarity(ds, sig, weights={"a": 3.0, "b": 1.0}, min_valid_fraction=0.5)
    assert float(out) == pytest.approx(np.exp(-2.0))


def test_constant_matching_layer_scores_one():
    ds = xr.Dataset({"a": (("lat", "lon"), [[1.0, 1.0]])}, coords={"lat": [0.0], "lon": [0.0, 1.0]})
    sig = xr.Dataset({"median": ("layer", [1.0]), "iqr": ("layer", [0.0])}, coords={"layer": ["a"]})
    np.testing.assert_allclose(similarity(ds, sig), 1.0)


def test_negative_weights_rejected():
    ds, sig = example()
    with pytest.raises(ValueError):
        similarity(ds, sig, weights={"a": -1.0})


def test_angular_exclusion_wraps_longitude():
    score = xr.DataArray(
        [[1.0, 0.99, 0.5]], dims=("lat", "lon"), coords={"lat": [0.0], "lon": [179.0, -179.0, 0.0]}
    )
    picks = top_cells(score, n=2, separation_deg=5)
    assert [p["lon"] for p in picks] == [179.0, 0.0]


def test_earth_coordinates_cannot_be_mislabeled_mars():
    with pytest.raises(ValueError):
        validate_targets({"x": {"body": "Earth", "lat": 0.0, "lon": 0.0}})

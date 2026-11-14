import numpy as np
import pytest
import xarray as xr
from shapely.geometry import box

from analog.matching import great_circle_km
from analog.screening import local_coordinates, patch_features, sample_patch, search_centres


@pytest.mark.parametrize("radius", [6371008.8, 3396000.0])
def test_physical_scale_uses_body_radius(radius):
    lat, lon = local_coordinates(30, 45, radius)
    assert lat.shape == (26, 26)
    # On an east/west centre line, inverse great-circle distance recovers physical offsets.
    expected = np.hypot(50000, 2000) / 1000
    assert great_circle_km(30, 45, lat[12, 0], lon[12, 0], radius) == pytest.approx(expected)


def test_local_flat_and_known_ramp_features():
    _y, x = np.meshgrid(np.arange(26) * 4000.0, np.arange(26) * 4000.0, indexing="ij")
    np.testing.assert_allclose(patch_features(np.zeros_like(x)), 0)
    expected_slope = np.degrees(np.arctan(0.1))
    result = patch_features(0.1 * x)
    np.testing.assert_allclose(result, [expected_slope, expected_slope, 10000])


def test_missing_dem_does_not_produce_features():
    p = np.zeros((26, 26))
    p[0, 0] = np.nan
    assert np.isnan(patch_features(p)).all()


def test_sampling_wraps_dateline_without_false_cliff():
    lat = np.arange(89.5, -90, -1)
    lon = np.arange(-179.5, 180, 1)
    values = np.cos(np.deg2rad(lon))[None, :] * np.ones((180, 1))
    g = xr.DataArray(values, dims=("lat", "lon"), coords={"lat": lat, "lon": lon})
    a, _, _ = sample_patch(g, 0, 179.9, 6371008.8)
    b, _, _ = sample_patch(g, 0, -179.9, 6371008.8)
    assert np.isfinite(a).all()
    np.testing.assert_allclose(a, b[:, ::-1], atol=1e-10)


def test_exclusions_and_polar_search_limit():
    lat, lon = search_centres(box(-180, -90, 180, 90), 2)
    assert lat.min() >= -60 and lat.max() <= 60
    assert not (((lon >= -26) & (lon <= -12) & (lat >= 62) & (lat <= 68)).any())
    assert not (((lon >= -81) & (lon <= -65) & (lat >= -31) & (lat <= -17)).any())


def test_invalid_physical_grid_rejected():
    with pytest.raises(ValueError):
        local_coordinates(0, 0, 6371008.8, spacing_km=0)

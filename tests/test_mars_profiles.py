import numpy as np
import pytest
import rasterio
import xarray as xr
from rasterio.transform import from_origin

from analog import dust, mars, swim
from analog.mars_profiles import describe_native, native_window, summarize_dust, validate_targets


def grid():
    lat = np.arange(2, -2.01, -0.1)
    lon = np.arange(-2, 2.01, 0.1)
    return xr.DataArray(
        np.ones((len(lat), len(lon))), dims=("lat", "lon"), coords={"lat": lat, "lon": lon}
    )


def test_missing_native_values_stay_unknown():
    result = describe_native(grid() * np.nan, 0, 0)
    assert result["native_cells_in_window"] > 0
    assert result["valid_native_cells"] == 0 and result["mean"] is None
    assert result["status"] == "unknown"


def test_coverage_is_not_clamped_to_nearest_edge():
    result = describe_native(grid(), 70, 0)
    assert result["native_cells_in_window"] == 0 and result["status"] == "unknown"


def test_native_stats_do_not_invent_cells():
    g = grid()
    g.values[:] = np.nan
    g.loc[{"lat": g.lat[20], "lon": g.lon[20]}] = 0.25
    result = describe_native(g, 0, 0)
    assert result["valid_native_cells"] == 1 and result["mean"] == 0.25
    assert 0 < result["valid_fraction"] < 1


def test_native_window_crosses_date_line():
    g = xr.DataArray(
        np.ones((3, 4)),
        dims=("lat", "lon"),
        coords={"lat": [0.1, 0, -0.1], "lon": [-179.9, -179.8, 179.8, 179.9]},
    )
    result = native_window(g, 0, 180, 100)
    assert result.notnull().sum() == 12


def test_thermal_inertia_mask_excludes_infilled_and_invalid(monkeypatch):
    g = xr.DataArray(
        [[100, 200, 0, 6000]], dims=("lat", "lon"), coords={"lat": [0], "lon": [0, 1, 2, 3]}
    )
    mask = g.copy(data=np.array([[1, 0, 1, 1]]))
    monkeypatch.setattr(mars, "load", lambda name, raw_dir: mask if name.endswith("_mask") else g)
    values = mars.load_thermal_inertia(keep_interpolated=False).values
    np.testing.assert_allclose(values, [[100, np.nan, np.nan, np.nan]], equal_nan=True)


def make_dust(tmp_path):
    values = np.array([1, 2, 3, 4], float)[:, None, None] * np.ones((4, 2, 2))
    ds = xr.Dataset(
        {
            "cdodtot": (("Time", "latitude", "longitude"), values),
            "cdod610": (("Time", "latitude", "longitude"), values * 2),
            "cdodrel": (("Time", "latitude", "longitude"), values * 0 + 0.7),
            "Ls": ("Time", [0, 90, 180, 270]),
            "SOY": ("Time", [1, 2, 3, 4]),
        },
        coords={
            "Time": [0.5, 1.5, 2.5, 3.5],
            "latitude": [-1.5, 1.5],
            "longitude": [-178.5, 178.5],
        },
    )
    ds.to_netcdf(tmp_path / "dustscenario_MY35_v2-5.nc", engine="scipy")


def test_dust_extracts_native_cell_and_keeps_reliability(tmp_path):
    make_dust(tmp_path)
    site = dust.load_site_series(0.1, 179.8, raw_dir=tmp_path)
    assert float(site.longitude) == 178.5
    result = summarize_dust(site)
    assert result["mean_cdodtot"] == 2.5
    assert result["max_cdodtot"] == 4 and result["peak_sol_of_year"] == 4
    assert result["reliability_mean"] == pytest.approx(0.7)
    assert result["seasons_by_Ls"]["180_270"]["mean_cdodtot"] == 3
    assert result["reconstructed"] is True


def test_dust_irregular_time_not_silently_averaged(tmp_path):
    make_dust(tmp_path)
    site = dust.load_site_series(0, 0, raw_dir=tmp_path).assign_coords(Time=[0, 1, 5, 6])
    with pytest.raises(ValueError, match="equally spaced"):
        summarize_dust(site)


def test_swim_normalizes_western_overflow_and_masks_invalid(tmp_path):
    path = tmp_path / "SWIM2_c0_1.tif"
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        width=2,
        height=2,
        count=1,
        dtype="float32",
        crs="+proj=eqc +R=3396190 +units=m",
        transform=from_origin(-np.pi * 3396190 - 1000, 1000, 2964, 2964),
        nodata=-100,
    ) as dst:
        dst.write(np.array([[-0.2, 0], [1, -100]], dtype="float32"), 1)
    result = swim.load("ice_consistency_shallow", tmp_path)
    assert float(result.lon.min()) >= -180 and float(result.lon.max()) < 180
    assert np.isnan(result.values).sum() == 1
    assert 0 in result.values


@pytest.mark.parametrize("lat,lon", [(np.nan, 0), (0, 181), (86, 0)])
def test_invalid_target_coordinates_rejected(lat, lon):
    with pytest.raises(ValueError):
        validate_targets({"target": {"lat": lat, "lon": lon}})

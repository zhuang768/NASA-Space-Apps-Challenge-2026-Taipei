import numpy as np
import xarray as xr

from analog.terrain import block_stats, slope_deg

RADIUS_M = 3_396_000.0


def global_grid(values_of_lat_lon, step=1.0):
    lat = np.arange(90 - step / 2, -90, -step)
    lon = np.arange(-180 + step / 2, 180, step)
    lon2d, lat2d = np.meshgrid(lon, lat)
    return xr.DataArray(
        values_of_lat_lon(lat2d, lon2d), dims=("lat", "lon"), coords={"lat": lat, "lon": lon}
    )


def test_slope_of_flat_surface_is_zero():
    dem = global_grid(lambda lat, lon: np.full(lat.shape, 1234.0))
    np.testing.assert_allclose(slope_deg(dem, RADIUS_M), 0)


def test_slope_of_north_south_ramp():
    metres_per_degree = 1000.0
    dem = global_grid(lambda lat, lon: metres_per_degree * lat)
    ground_metres_per_degree = RADIUS_M * np.deg2rad(1.0)
    expected = np.degrees(np.arctan(metres_per_degree / ground_metres_per_degree))
    np.testing.assert_allclose(slope_deg(dem, RADIUS_M), expected)


def test_slope_of_east_west_wave_including_the_date_line():
    # sin(lon) is steepest at +-180, so the edge columns only come out right
    # if the grid wraps and the east-west distance shrinks with cos(lat).
    amplitude = 1000.0
    dem = global_grid(lambda lat, lon: amplitude * np.sin(np.deg2rad(lon)))
    lon2d, lat2d = np.meshgrid(np.deg2rad(dem.lon), np.deg2rad(dem.lat))
    expected = np.degrees(np.arctan(amplitude * np.abs(np.cos(lon2d)) / (RADIUS_M * np.cos(lat2d))))
    np.testing.assert_allclose(slope_deg(dem, RADIUS_M), expected, rtol=1e-3, atol=1e-9)


def test_block_stats_shape_and_values():
    grid = global_grid(lambda lat, lon: lat)
    stats = block_stats(grid, 10)
    assert stats["mean"].shape == (18, 36)
    np.testing.assert_allclose(stats["relief"], 9.0)
    np.testing.assert_allclose(stats["mean"].isel(lat=0, lon=0), 85.0)

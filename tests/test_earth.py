import numpy as np
import rasterio
from rasterio.transform import from_origin

from analog.earth import load_terrain


def test_real_raster_aggregation_keeps_coordinates_and_metres(tmp_path):
    p = tmp_path / "terrain.tif"
    z = np.arange(16, dtype="float32").reshape(4, 4)
    with rasterio.open(
        p,
        "w",
        driver="GTiff",
        width=4,
        height=4,
        count=1,
        dtype="float32",
        crs="EPSG:4326",
        transform=from_origin(-2, 2, 1, 1),
    ) as dst:
        dst.write(z, 1)
    grid = load_terrain(p)
    np.testing.assert_allclose(grid, [[2.5, 4.5], [10.5, 12.5]])
    np.testing.assert_allclose(grid.lat, [1, -1])
    np.testing.assert_allclose(grid.lon, [-1, 1])
    assert grid.attrs["units"] == "m"


def test_cmr_interval_overlap_does_not_include_preceding_month(monkeypatch):
    from analog.earth import discover_monthly

    def granule(date):
        return {"umm": {"TemporalExtent": {"RangeDateTime": {"BeginningDateTime": date}}}}

    monkeypatch.setattr(
        "earthaccess.search_data",
        lambda **kwargs: [granule("2022-12-01T00:00:00Z"), granule("2023-01-01T00:00:00Z")],
    )
    assert len(discover_monthly("aod", "2023-01-01", "2023-01-31")) == 1

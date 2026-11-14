import numpy as np
import pytest
import xarray as xr

from analog.regional_temperature import extract_context


def grid():
    return xr.Dataset(
        {"tsurf_correct": (("MY", "Ls", "ltst", "Lat", "Lon"), np.full((2, 2, 2, 2, 2), np.nan))},
        coords={
            "MY": [29.0, 30.0],
            "Ls": [0.0, 10.0],
            "ltst": [3.0, 15.0],
            "Lat": [-5.0, 0.0],
            "Lon": [-180.0, -175.0],
        },
    )


def test_no_pair_across_year_or_season():
    ds = grid()
    ds.tsurf_correct.loc[{"MY": 29, "Ls": 0, "ltst": 3, "Lat": -5, "Lon": -180}] = 180
    ds.tsurf_correct.loc[{"MY": 30, "Ls": 0, "ltst": 15, "Lat": -5, "Lon": -180}] = 260
    result = extract_context(ds, -5, 180)
    assert result["paired_bins"] == 0
    assert result["paired_contrast_median_K"] is None
    assert result["valid_day_bins"] == result["valid_night_bins"] == 1


def test_paired_values_and_metadata_remain_unscored():
    ds = grid()
    ds.tsurf_correct.loc[{"MY": 29, "Ls": 0, "ltst": 3, "Lat": -5, "Lon": -180}] = 180
    ds.tsurf_correct.loc[{"MY": 29, "Ls": 0, "ltst": 15, "Lat": -5, "Lon": -180}] = 260
    result = extract_context(ds, -5, 179.9)
    assert result["selected_grid_coordinate"]["lon"] == -180
    assert result["paired_bins"] == 1
    assert result["paired_contrast_median_K"] == 80
    assert result["scoring_eligible"] is False
    assert result["quality_flags"] is None


def test_nonpositive_temperature_is_missing():
    ds = grid()
    ds.tsurf_correct[:] = 0
    assert extract_context(ds, -5, -180)["paired_bins"] == 0


def test_reject_wrong_local_times():
    ds = grid().assign_coords(ltst=[2.0, 14.0])
    with pytest.raises(ValueError, match="LTST"):
        extract_context(ds, 0, 0)


def test_reject_unexpected_grid_and_invalid_target():
    ds = grid().assign_coords(Lat=[-5.0, 2.0])
    with pytest.raises(ValueError, match="grid"):
        extract_context(ds, 0, 0)
    with pytest.raises(ValueError, match="target"):
        extract_context(grid(), np.nan, 0)

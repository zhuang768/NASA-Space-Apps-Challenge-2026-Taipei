"""Conservative context extraction from the published MCS time-corrected grid."""

import numpy as np

REQUIRED_DIMS = ("MY", "Ls", "ltst", "Lat", "Lon")


def validate_grid(ds):
    if "tsurf_correct" not in ds or ds.tsurf_correct.dims != REQUIRED_DIMS:
        raise ValueError("Unexpected MCS variable or dimensions")
    for dim in REQUIRED_DIMS:
        coord = ds[dim].values
        if coord.ndim != 1 or not np.isfinite(coord).all() or len(np.unique(coord)) != len(coord):
            raise ValueError(f"Invalid {dim} coordinate")
    if set(ds.ltst.values) != {3.0, 15.0}:
        raise ValueError("Expected nominal 03:00 and 15:00 LTST")
    if not np.allclose(np.diff(ds.Lat), 5) or not np.allclose(np.diff(ds.Lon), 5):
        raise ValueError("Expected native 5 degree grid")
    if not np.allclose(np.diff(ds.Ls), 10) or (ds.Ls.min() < 0) or (ds.Ls.max() >= 360):
        raise ValueError("Unexpected seasonal grid")
    if ds.Lat.min() < -90 or ds.Lat.max() > 90 or ds.Lon.min() < -180 or ds.Lon.max() >= 180:
        raise ValueError("Unexpected coordinate range")


def extract_context(ds, lat, lon):
    validate_grid(ds)
    if not np.isfinite([lat, lon]).all() or abs(lat) > 90:
        raise ValueError("Invalid target")
    lon = (lon + 180) % 360 - 180
    # Circular longitude distance avoids treating -180 and +180 as far apart.
    ilon = int(np.argmin(np.abs((ds.Lon.values - lon + 180) % 360 - 180)))
    ilat = int(np.argmin(np.abs(ds.Lat.values - lat)))
    selected = ds.tsurf_correct.isel(Lat=ilat, Lon=ilon).sel(MY=slice(29, 36))
    rows = []
    for year in selected.MY.values:
        for season in selected.Ls.values:
            night = float(selected.sel(MY=year, Ls=season, ltst=3))
            day = float(selected.sel(MY=year, Ls=season, ltst=15))
            # Reject non-positive temperatures but never replace missing data.
            night = night if np.isfinite(night) and night > 0 else None
            day = day if np.isfinite(day) and day > 0 else None
            rows.append(
                {
                    "mars_year": int(year),
                    "Ls_coordinate_deg": float(season),
                    "night_03_K": night,
                    "day_15_K": day,
                    "sampled_contrast_K": day - night
                    if day is not None and night is not None
                    else None,
                }
            )
    pairs = [r["sampled_contrast_K"] for r in rows if r["sampled_contrast_K"] is not None]
    return {
        "status": "context_only_metadata_incomplete",
        "scoring_eligible": False,
        "quantity": "MCS-derived surface temperature corrected with model-based local-time adjustment",
        "units": "K",
        "unit_basis": "publication and author plotting code; NetCDF units attribute absent",
        "requested_center": {"lat": lat, "lon": lon},
        "selected_grid_coordinate": {"lat": float(ds.Lat[ilat]), "lon": float(ds.Lon[ilon])},
        "grid_spacing_deg": [5, 5],
        "season_coordinate_spacing_deg": 10,
        "extraction": "nearest coordinate; no interpolation or 100 km mean",
        "mars_years": [29, 36],
        "expected_year_season_pairs": len(rows),
        "valid_night_bins": sum(r["night_03_K"] is not None for r in rows),
        "valid_day_bins": sum(r["day_15_K"] is not None for r in rows),
        "paired_bins": len(pairs),
        "paired_contrast_median_K": float(np.median(pairs)) if pairs else None,
        "sample_count_per_bin": None,
        "uncertainty": None,
        "quality_flags": None,
        "coordinate_datum": "not encoded in the distributed NetCDF; requires confirmation",
        "limitations": [
            "Grid spacing exceeds the 100 km terrain window",
            "Grid-coordinate center/edge semantics and observation footprints unconfirmed",
            "No per-bin count, uncertainty or QA flags distributed",
            "Same MY/Ls coordinate is not a same-sol observation pair",
            "No daily extremes, Earth comparison or ranking implied",
            "Event seasons retained; no undocumented storm removal",
        ],
        "series": rows,
    }

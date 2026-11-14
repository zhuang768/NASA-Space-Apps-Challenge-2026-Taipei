"""Mars target descriptors with native-scale evidence and explicit missing data."""

import numpy as np
import xarray as xr

from analog import dust, mars, swim, temperature
from analog.matching import FEATURES
from analog.screening import TARGETS, local_coordinates, patch_features, sample_patch

TI_UNITS = "J m-2 K-1 s-0.5"


def validate_targets(targets):
    if not isinstance(targets, dict) or not targets:
        raise ValueError("Targets must be a nonempty object keyed by target ID")
    for target in targets.values():
        if target.get("body", "Mars") != "Mars":
            raise ValueError("Only Mars targets are supported")
        lat, lon = target["lat"], target["lon"]
        if not np.isfinite([lat, lon]).all() or not -85 <= lat <= 85 or not -180 <= lon <= 180:
            raise ValueError("Use finite Mars latitude [-85,85], east longitude [-180,180]")


def native_window(grid, lat, lon, window_km=100.0):
    """Native cell centres inside a square in a local spherical AEQD plane.

    No interpolation, and no latitude clipping to invent coverage.
    """
    qlat, qlon = local_coordinates(lat, lon, mars.MARS_RADIUS_M, window_km=window_km)
    delta = (grid.lon.values - lon + 180) % 360 - 180
    qdelta = (qlon - lon + 180) % 360 - 180
    yi = np.where((grid.lat.values >= qlat.min()) & (grid.lat.values <= qlat.max()))[0]
    xi = np.where((delta >= qdelta.min()) & (delta <= qdelta.max()))[0]
    if not len(yi) or not len(xi):
        return xr.DataArray(np.empty((0, 0)), dims=("lat", "lon"), coords={"lat": [], "lon": []})
    sub = grid.isel(lat=yi, lon=xi)
    ph, dl = np.meshgrid(np.deg2rad(sub.lat), np.deg2rad(delta[xi]), indexing="ij")
    p0 = np.deg2rad(lat)
    cosine = np.clip(np.sin(p0) * np.sin(ph) + np.cos(p0) * np.cos(ph) * np.cos(dl), -1, 1)
    angle = np.arccos(cosine)
    factor = np.ones_like(angle)
    np.divide(angle, np.sin(angle), out=factor, where=np.abs(angle) > 1e-12)
    east = mars.MARS_RADIUS_M * factor * np.cos(ph) * np.sin(dl)
    north = (
        mars.MARS_RADIUS_M
        * factor
        * (np.cos(p0) * np.sin(ph) - np.sin(p0) * np.cos(ph) * np.cos(dl))
    )
    inside = (np.abs(east) <= window_km * 500) & (np.abs(north) <= window_km * 500)
    result = sub.where(xr.DataArray(inside, dims=sub.dims, coords=sub.coords))
    result.attrs["native_cells_in_window"] = int(inside.sum())
    return result


def describe_native(grid, lat, lon, window_km=100.0):
    sub = native_window(grid, lat, lon, window_km)
    total = int(sub.attrs.get("native_cells_in_window", 0))
    values = sub.values
    valid = np.isfinite(values)
    result = {
        "native_cells_in_window": total,
        "valid_native_cells": int(valid.sum()),
        "valid_fraction": float(valid.sum() / total) if total else None,
        "aggregation": "native-cell cosine-latitude weighted mean; no interpolation",
    }
    if not valid.any():
        return {
            **result,
            "status": "unknown",
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
        }
    weights = np.broadcast_to(np.cos(np.deg2rad(sub.lat.values))[:, None], sub.shape)
    return {
        **result,
        "status": "available",
        "mean": float(np.average(values[valid], weights=weights[valid])),
        "median": float(np.median(values[valid])),
        "min": float(values[valid].min()),
        "max": float(values[valid].max()),
    }


def summarize_dust(site):
    values = np.asarray(site.cdodtot.values, float)
    times = np.asarray(site.Time.values, float)
    if len(times) < 2 or not np.allclose(np.diff(times), 1.0, rtol=0, atol=1e-6):
        raise ValueError("Expected one equally spaced model sample per sol")
    valid = np.isfinite(values) & (values >= 0)
    if not valid.any():
        return {"status": "unknown", "valid_reconstructed_sols": 0}
    index = int(np.where(valid)[0][np.argmax(values[valid])])
    result = {
        "status": "available",
        "mean_cdodtot": float(values[valid].mean()),
        "p95_cdodtot": float(np.percentile(values[valid], 95)),
        "max_cdodtot": float(values[index]),
        "peak_sol_of_year": float(site.SOY.values[index]),
        "peak_Ls_deg": float(site.Ls.values[index]),
        "valid_reconstructed_sols": int(valid.sum()),
        "expected_reconstructed_sols": len(values),
        "units": "1",
        "wavelength_micron": 9.3,
        "optical_quantity": "absorption, local total column",
        "native_cell_lat": float(site.latitude),
        "native_cell_lon": float(site.longitude),
        "native_grid_degrees": [3, 3],
        "reconstructed": True,
        "reliability_interpretation": "cdodrel is provider reliability, not a calibrated probability",
        "seasons_by_Ls": {},
    }
    reliability = np.asarray(site.cdodrel.values, float)
    good = np.isfinite(reliability)
    result["reliability_mean"] = float(reliability[good].mean()) if good.any() else None
    for a, b in [(0, 90), (90, 180), (180, 270), (270, 360)]:
        take = valid & (site.Ls.values >= a) & (site.Ls.values < b)
        result["seasons_by_Ls"][f"{a}_{b}"] = {
            "valid_sols": int(take.sum()),
            "mean_cdodtot": float(values[take].mean()) if take.any() else None,
        }
    return result


def build_profiles(targets=None, raw_dir=mars.RAW_DIR, window_km=100.0, spacing_km=4.0):
    targets = TARGETS if targets is None else targets
    validate_targets(targets)
    grids = {}
    inventory = {}
    errors = {}
    loaders = {
        "terrain": lambda: mars.load("mola_topography", raw_dir).astype("float32"),
        "thermal_inertia": lambda: mars.load_thermal_inertia(raw_dir, keep_interpolated=False),
        "thermal_inertia_infilled": lambda: mars.load_thermal_inertia(raw_dir),
        "ice_shallow": lambda: swim.load("ice_consistency_shallow", raw_dir),
        "ice_deep": lambda: swim.load("ice_consistency_deep", raw_dir),
    }
    for key, load in loaders.items():
        try:
            grids[key] = load()
            inventory[key] = {"status": "loaded", "shape": list(grids[key].shape)}
        except FileNotFoundError:
            inventory[key] = {"status": "missing"}
        except (ValueError, OSError) as exc:
            inventory[key] = {"status": "invalid", "error_type": type(exc).__name__}
            errors[key] = str(exc)
    profiles = {}
    series = {}
    for name, target in targets.items():
        lat, lon = target["lat"], target["lon"]
        p = {
            **target,
            "body": "Mars",
            "window_km": window_km,
            "terrain": {"status": "unknown"},
            "thermal_inertia": {"status": "unknown"},
            "ice": {},
            "dust": {},
            "surface_temperature": {
                "status": "missing",
                "reason": "TES thermal inertia is not temperature",
            },
        }
        if "terrain" in grids:
            patch, _, _ = sample_patch(
                grids["terrain"], lat, lon, mars.MARS_RADIUS_M, spacing_km, window_km
            )
            vector = patch_features(patch, spacing_km)
            p["terrain"] = {
                "status": "available" if np.isfinite(vector).all() else "unknown",
                **{k: float(v) if np.isfinite(v) else None for k, v in zip(FEATURES, vector)},
                "sample_spacing_km": spacing_km,
                "slope_stencil_km": 2 * spacing_km,
                "radius_m": mars.MARS_RADIUS_M,
            }
        if "thermal_inertia" in grids:
            p["thermal_inertia"] = {
                **describe_native(grids["thermal_inertia"], lat, lon, window_km),
                "units": TI_UNITS,
                "infilled_pixels_excluded": True,
                "is_temperature": False,
                "is_hardness_measurement": False,
            }
            if "thermal_inertia_infilled" in grids:
                p["thermal_inertia"]["with_infilled_pixels"] = describe_native(
                    grids["thermal_inertia_infilled"], lat, lon, window_km
                )
        for depth, key in [("0_1m", "ice_shallow"), ("1_5m", "ice_deep")]:
            p["ice"][depth] = {"status": "unknown"}
            if key in grids:
                summary = describe_native(grids[key], lat, lon, window_km)
                p["ice"][depth] = {
                    **summary,
                    "units": "1",
                    "quantity": "SWIM ice consistency",
                    "is_ice_amount": False,
                    "is_probability": False,
                    "source_crs": grids[key].attrs.get("source_crs"),
                }
        for year in ("dust_my34", "dust_my35"):
            try:
                site = dust.load_site_series(lat, lon, year, raw_dir)
                series[(name, year)] = site
                p["dust"][year] = summarize_dust(site)
                inventory[year] = {
                    "status": "loaded",
                    "native_grid": [60, 120],
                    "reconstructed_sols": len(site.Time),
                }
            except FileNotFoundError:
                p["dust"][year] = {"status": "unknown", "reason": "missing_file"}
                inventory[year] = {"status": "missing"}
            except (ValueError, OSError, KeyError) as exc:
                p["dust"][year] = {"status": "unknown", "reason": "invalid_file"}
                inventory[year] = {"status": "invalid", "error_type": type(exc).__name__}
                errors[year] = str(exc)
        profiles[name] = p
    try:
        temperature_context, _ = temperature.build_context(raw_dir)
    except (ValueError, OSError, KeyError) as exc:
        temperature_context = {"status": "invalid", "error": str(exc)}
        errors["temperature_context"] = str(exc)
    return {
        "rover_temperature_context": temperature_context,
        "profiles": profiles,
        "inventory": inventory,
        "errors": errors,
        "analysis_type": "Mars target descriptors, not Earth analog ranking",
        "schema_version": "1.0",
        "body": "Mars",
        "longitude_convention": "east-positive [-180,180)",
        "missing_requirements": [
            "Comparable Mars surface day/night temperature and temporal definition",
            "Mission-specific material, mineral and operational thresholds",
            "Site-level ground validation and finer terrain where needed",
        ],
        "earth_team_handoff": [
            "Match terrain at the declared physical scale.",
            "Keep MODIS LST distinct from TES thermal inertia.",
            "Keep Earth precipitation/moisture/permafrost distinct from SWIM ice consistency.",
            "Keep 550 nm extinction AOT distinct from 9.3 micron Mars absorption CDOD.",
        ],
    }, series

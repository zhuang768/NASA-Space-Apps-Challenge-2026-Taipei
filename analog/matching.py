"""Transparent terrain-only distance and spatially separated candidate selection."""

import numpy as np

FEATURES = ("slope_median_deg", "slope_p90_deg", "relief_m")
# Explicit design tolerances, not empirically calibrated probabilities.
TOLERANCES = np.array([1.0, 2.0, 500.0])
WEIGHTS = np.array([0.25, 0.25, 0.5])


def terrain_distance(features, target, weights=WEIGHTS, tolerances=TOLERANCES):
    features = np.asarray(features, dtype=float)
    target = np.asarray(target, dtype=float)
    weights = np.asarray(weights, dtype=float)
    tolerances = np.asarray(tolerances, dtype=float)
    if features.shape[-1] != 3 or target.shape != (3,):
        raise ValueError("Expected three terrain features")
    if weights.shape != (3,) or not np.isfinite(weights).all() or (weights < 0).any():
        raise ValueError("Invalid weights")
    if weights.sum() <= 0 or tolerances.shape != (3,) or (tolerances <= 0).any():
        raise ValueError("Positive weight total and tolerances required")
    if not np.isfinite(tolerances).all() or not np.isfinite(target).all():
        raise ValueError("Finite target and tolerances required")
    distances = np.sum(np.abs(features - target) / tolerances * weights / weights.sum(), axis=-1)
    return np.where(np.isfinite(features).all(axis=-1), distances, np.inf)


def great_circle_km(lat, lon, other_lat, other_lon, radius_m=6371008.8):
    lat1, lat2 = np.deg2rad(lat), np.deg2rad(other_lat)
    dlat = lat2 - lat1
    dlon = np.deg2rad(other_lon - lon)
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * radius_m / 1000 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def select_separated(lat, lon, distances, limit=12, separation_km=300):
    if limit < 1 or separation_km < 0:
        raise ValueError("Positive candidate limit and nonnegative separation required")
    selected = []
    for index in np.argsort(distances, kind="stable"):
        if not np.isfinite(distances[index]):
            continue
        if all(
            great_circle_km(lat[index], lon[index], lat[j], lon[j]) >= separation_km
            for j in selected
        ):
            selected.append(int(index))
            if len(selected) == limit:
                break
    return selected

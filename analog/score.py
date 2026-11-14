"""Experimental within-Mars descriptor similarity.

The score is exp(-weighted mean standardized absolute difference). Scales use
maximum(target IQR, scale_floor * scored-grid IQR); both are design choices.
All requested positive-weight layers are required by default. Explicit partial
scores expose evidence_fraction and normalize the available weights per cell.
This is not a probability, calibrated confidence or task-success estimate.
"""

from __future__ import annotations

import numpy as np
import xarray as xr


def robust_scale(stack: xr.Dataset) -> xr.DataArray:
    """Global IQR of each layer in the stack (indexed by 'layer')."""
    quartiles = stack.quantile([0.25, 0.75], dim=("lat", "lon"))
    return (
        quartiles.sel(quantile=0.75, drop=True) - quartiles.sel(quantile=0.25, drop=True)
    ).to_dataarray("layer")


def similarity(
    stack: xr.Dataset,
    signature: xr.Dataset,
    weights: dict[str, float] | None = None,
    scale_floor: float = 0.1,
    min_valid_fraction: float = 1.0,
) -> xr.DataArray:
    """Experimental descriptor similarity, not confidence or mission success.

    By default all positive-weight target layers must be available at a cell.
    Opt-in partial scores carry their evidence_fraction coordinate. Weight
    normalization uses the available positive weights at that cell.
    """
    if not 0 <= min_valid_fraction <= 1 or not np.isfinite(scale_floor) or scale_floor < 0:
        raise ValueError("Invalid coverage or scale floor")
    layers = [str(v) for v in signature.layer.values if v in stack.data_vars]
    if not layers:
        raise ValueError("signature and stack share no layers")
    if weights and set(weights) - set(layers):
        raise ValueError("Weights contain unknown layer names")
    w = np.array([1.0 if weights is None else weights.get(name, 1.0) for name in layers])
    if not np.isfinite(w).all() or (w < 0).any() or w.sum() <= 0:
        raise ValueError("Finite nonnegative weights with a positive total required")
    weight = xr.DataArray(w, dims="layer", coords={"layer": layers})
    values = stack[layers].to_dataarray("layer")
    target = signature["median"].sel(layer=layers)
    target_iqr = signature["iqr"].sel(layer=layers)
    floor = scale_floor * robust_scale(stack[layers])
    scale = xr.where(target_iqr > floor, target_iqr, floor)
    difference = np.abs(values - target)
    z = xr.where(scale > 0, difference / scale, xr.where(difference == 0, 0.0, np.inf))
    valid = np.isfinite(values) & np.isfinite(target) & np.isfinite(scale) & (weight > 0)
    total = weight.where(valid, 0.0).sum("layer")
    fraction = valid.sum("layer") / int((w > 0).sum())
    distance = (z * weight).where(valid, 0.0).sum("layer") / total.where(total > 0)
    score = np.exp(-distance).where((total > 0) & (fraction >= min_valid_fraction))
    return (
        score.assign_coords(evidence_fraction=fraction)
        .rename("similarity")
        .assign_attrs(
            interpretation="experimental descriptor score, not probability or confidence",
            min_valid_fraction=min_valid_fraction,
        )
    )


def top_cells(score: xr.DataArray, n: int = 10, separation_deg: float = 5.0) -> list[dict]:
    """The n best-scoring cells using an explicit angular exclusion box.

    This is not a fixed physical separation. Longitude differences wrap.
    """
    if n < 1 or separation_deg < 0:
        raise ValueError("Positive n and nonnegative separation required")
    frame = score.to_dataframe(name="score").dropna().sort_values("score", ascending=False)
    picks: list[dict] = []
    for (lat, lon), row in frame.iterrows():
        if any(
            abs(lat - p["lat"]) < separation_deg
            and abs((lon - p["lon"] + 180) % 360 - 180) < separation_deg
            for p in picks
        ):
            continue
        picks.append({"lat": float(lat), "lon": float(lon), "score": float(row["score"])})
        if len(picks) == n:
            break
    return picks

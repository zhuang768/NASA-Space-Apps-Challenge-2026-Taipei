"""Similarity between a target signature and every cell of a layer stack.

The score of a cell is exp(-mean_k |x_k - m_k| / s_k) over the layers k that
have data: 1 means every layer sits exactly on the target median, and each
scale s_k of difference costs a factor e. The scale is the larger of the
target IQR and a floor taken from the scored stack itself, so that a very
uniform target region does not make the score needlessly sharp.
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
) -> xr.DataArray:
    """Score every cell of the stack against the signature; result in 0..1.

    Layers are matched by name. Cells missing every layer get NaN; cells
    missing some layers are scored on the layers they have.
    """
    layers = [str(v) for v in signature.layer.values if v in stack.data_vars]
    if not layers:
        raise ValueError("signature and stack share no layers")
    values = stack[layers].to_dataarray("layer")
    target = signature["median"].sel(layer=layers)
    target_iqr = signature["iqr"].sel(layer=layers)
    floor = scale_floor * robust_scale(stack[layers])
    scale = xr.where(target_iqr > floor, target_iqr, floor)

    z = np.abs(values - target) / scale
    if weights:
        weight = xr.DataArray([weights.get(name, 1.0) for name in layers], coords={"layer": layers})
        z = z * weight * (len(layers) / float(weight.sum()))
    return np.exp(-z.mean("layer", skipna=True)).where(values.notnull().any("layer"))


def top_cells(score: xr.DataArray, n: int = 10, separation_deg: float = 5.0) -> list[dict]:
    """The n best-scoring cells, keeping at least separation_deg between picks."""
    frame = score.to_dataframe(name="score").dropna().sort_values("score", ascending=False)
    picks: list[dict] = []
    for (lat, lon), row in frame.iterrows():
        if any(
            abs(lat - p["lat"]) < separation_deg and abs(lon - p["lon"]) < separation_deg
            for p in picks
        ):
            continue
        picks.append({"lat": float(lat), "lon": float(lon), "score": float(row["score"])})
        if len(picks) == n:
            break
    return picks

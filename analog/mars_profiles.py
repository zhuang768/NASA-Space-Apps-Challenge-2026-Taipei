"""Native dust-series summaries retained from the tested Mars pipeline."""

import numpy as np


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

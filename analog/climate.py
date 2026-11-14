"""NASA POWER monthly context, kept separate from terrain ranking."""

import calendar
from pathlib import Path
from urllib.parse import urlencode

import numpy as np
import requests

from analog.mars import _fetch
from analog.provenance import source_record

BASE = "https://power.larc.nasa.gov/api/temporal/monthly/point"
PARAMETERS = ("T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR", "WS10M")


def fetch_context(lat, lon, directory, start=2023, end=2024):
    import json

    query = {
        "parameters": ",".join(PARAMETERS),
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON",
    }
    url = BASE + "?" + urlencode(query)
    path = Path(directory) / f"power_{lat:+.3f}_{lon:+.3f}_{start}_{end}.json"
    _fetch(url, path)
    data = json.loads(path.read_text())
    params = data["properties"]["parameter"]
    fill = data["header"].get("fill_value", -999)
    dates = [
        (f"{year}{month:02d}", calendar.monthrange(year, month)[1])
        for year in range(start, end + 1)
        for month in range(1, 13)
    ]
    summary = {}
    for name in PARAMETERS:
        values = np.array([params.get(name, {}).get(key, np.nan) for key, _ in dates], float)
        valid = np.isfinite(values) & (values != fill)
        days = np.array([n for _, n in dates])
        # Partial records stay unknown; never silently average around missing months.
        summary[name] = {
            "value": float(np.average(values, weights=days)) if valid.all() else None,
            "valid_months": int(valid.sum()),
            "expected_months": len(dates),
            "unit": data.get("parameters", {}).get(name, {}).get("units", "unknown"),
            "meaning": "day-weighted mean of monthly reported values",
        }
    return {
        "status": "context_only_not_ranked",
        "summary": summary,
        "header": data["header"],
        "parameters": data.get("parameters", {}),
        "geometry": data.get("geometry"),
        "source": source_record(
            path,
            url,
            dataset="NASA POWER monthly API",
            period=f"{start}-01 to {end}-12",
            resolution="0.5 degree latitude x 0.625 degree longitude meteorology grid",
            resolution_source="https://power.larc.nasa.gov/docs/services/",
            crs="geographic longitude/latitude",
        ),
    }


NETWORK_ERRORS = (requests.RequestException, ValueError, KeyError)

import calendar
import json

from analog.climate import PARAMETERS, fetch_context


def fixture_response(missing=False):
    months = {f"2024{m:02d}": float(m) for m in range(1, 13)}
    if missing:
        months["202402"] = -999.0
    return {
        "properties": {"parameter": {key: months.copy() for key in PARAMETERS}},
        "header": {"fill_value": -999, "sources": ["test_fixture"]},
        "parameters": {key: {"units": "fixture_unit"} for key in PARAMETERS},
        "geometry": {"type": "Point", "coordinates": [0, 0]},
    }


def test_monthly_mean_is_day_weighted_in_leap_year(tmp_path, monkeypatch):
    p = tmp_path / "power_+0.000_+0.000_2024_2024.json"
    p.write_text(json.dumps(fixture_response()))
    monkeypatch.setattr("analog.climate._fetch", lambda url, dest: p)
    result = fetch_context(0, 0, tmp_path, start=2024, end=2024)
    expected = sum(m * calendar.monthrange(2024, m)[1] for m in range(1, 13)) / 366
    assert result["summary"]["T2M"]["value"] == expected
    assert result["status"] == "context_only_not_ranked"


def test_one_fill_month_keeps_climate_unknown(tmp_path, monkeypatch):
    p = tmp_path / "power_+0.000_+0.000_2024_2024.json"
    p.write_text(json.dumps(fixture_response(missing=True)))
    monkeypatch.setattr("analog.climate._fetch", lambda url, dest: p)
    result = fetch_context(0, 0, tmp_path, start=2024, end=2024)
    assert result["summary"]["T2M"]["value"] is None
    assert result["summary"]["T2M"]["valid_months"] == 11

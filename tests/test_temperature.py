import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from analog.temperature import FLAGS, NS, build_context, read_product, summarize

LABEL = Path(
    "data/raw/mars/temperature/meda_calibrated/WE__0700___________CAL_TIRS________________P01.xml"
)


def fixture_product(tmp_path):
    root = ET.parse(LABEL)
    table = root.find(".//p:Table_Delimited", NS)
    table.find("p:records", NS).text = "4"
    path = tmp_path / LABEL.name
    root.write(path)
    frame = pd.read_csv(LABEL.with_suffix(".CSV"), nrows=4)
    frame.LTST = ["0700 00:01:00", "0700 01:01:00", "0700 12:01:00", "0700 13:01:00"]
    frame.GROUND_TEMP = [200, 202, 260, 264]
    frame.loc[:, list(FLAGS)] = 1
    frame.to_csv(path.with_suffix(".CSV"), index=False)
    return path


def test_same_sol_windows_and_unknown_flags(tmp_path):
    path = fixture_product(tmp_path)
    frame, sources = read_product(path)
    daily, _ = summarize(frame)
    assert daily[0]["sampled_day_night_contrast_K"] == 61
    assert sources[0]["quantity"] == "ground_brightness_temperature"
    frame = pd.read_csv(path.with_suffix(".CSV"))
    frame.loc[0, FLAGS[0]] = np.nan
    frame.to_csv(path.with_suffix(".CSV"), index=False)
    frame, _ = read_product(path)
    assert not frame.quality_supported.iloc[0]
    daily, _ = summarize(frame)
    assert daily[0]["sampled_day_night_contrast_K"] is None


def test_never_pair_different_sols(tmp_path):
    path = fixture_product(tmp_path)
    frame = pd.read_csv(path.with_suffix(".CSV"))
    frame.loc[2:, "LTST"] = ["0701 12:01:00", "0701 13:01:00"]
    frame.to_csv(path.with_suffix(".CSV"), index=False)
    frame, _ = read_product(path)
    daily, _ = summarize(frame)
    assert len(daily) == 2
    assert all(d["sampled_day_night_contrast_K"] is None for d in daily)


def test_label_units_and_record_count_enforced(tmp_path):
    path = fixture_product(tmp_path)
    root = ET.parse(path)
    for f in root.findall(".//p:Field_Delimited", NS):
        if f.findtext("p:name", namespaces=NS) == "GROUND_TEMP":
            f.find("p:unit", NS).text = "celsius"
    root.write(path)
    with pytest.raises(ValueError, match="kelvin"):
        read_product(path)
    path = fixture_product(tmp_path)
    frame = pd.read_csv(path.with_suffix(".CSV")).iloc[:2]
    frame.to_csv(path.with_suffix(".CSV"), index=False)
    with pytest.raises(ValueError, match="record count"):
        read_product(path)


def test_missing_products_remain_missing(tmp_path):
    context, hourly = build_context(tmp_path)
    assert context["status"] == "missing" and hourly.empty


def test_real_product_unknown_flags_do_not_become_confirmed():
    frame, _ = read_product(LABEL)
    assert len(frame) == 47774
    assert frame.quality_supported.sum() == 0
    assert frame[FLAGS[0]].isna().all()


def test_hourly_medians_are_not_weighted_by_sampling_cadence():
    frame = pd.DataFrame(
        {
            "ltst_sol": [700] * 104,
            "ltst_hour": [0] * 100 + [1, 12, 12, 13],
            "GROUND_TEMP": [200] * 100 + [220, 260, 260, 280],
            "GROUND_TEMP_UNCERTAINTY": [1] * 104,
            "valid_measurement": [True] * 104,
            "quality_supported": [True] * 104,
        }
    )
    daily, _ = summarize(frame)
    assert daily[0]["night"]["brightness_temperature_K"] == 210
    assert daily[0]["day"]["brightness_temperature_K"] == 270
    assert daily[0]["sampled_day_night_contrast_K"] == 60


def test_invalid_time_and_temperature_do_not_enter_windows(tmp_path):
    path = fixture_product(tmp_path)
    frame = pd.read_csv(path.with_suffix(".CSV"))
    frame.loc[0, "LTST"] = "0700 24:00:00"
    frame.loc[1, "GROUND_TEMP"] = -9999
    frame.loc[2, "GROUND_TEMP_UNCERTAINTY"] = -1
    frame.loc[3, FLAGS[0]] = 0
    frame.to_csv(path.with_suffix(".CSV"), index=False)
    frame, _ = read_product(path)
    assert frame.valid_measurement.sum() == 1
    assert frame.quality_supported.sum() == 0

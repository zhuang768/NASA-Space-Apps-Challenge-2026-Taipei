"""MEDA TIRS rover-local brightness temperatures, with explicit quality gaps."""

import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd

from analog.provenance import source_record

BASE = (
    "https://atmos.nmsu.edu/PDS/data/PDS4/Mars2020/mars2020_meda/data_calibrated_env/sol_0660_0779/"
)
FLAGS = (
    "WHEEL_OUTSIDE_TIRS_DOWNWARD_LOOKING_FOV",
    "ROVER_LOW_TILT",
    "TIRS_GROUND_FOOTPRINT_NOT_IN_SHADOW",
    "ROVER_HGA_OFF",
    "SKYCAM_OFF",
    "ROVER_STILL",
)
NS = {"p": "http://pds.nasa.gov/pds4/pds/v1"}


def read_product(label):
    """Validate a PDS4 label and retain unknown flags as unknown."""
    label = Path(label)
    root = ET.parse(label).getroot()
    table = root.find(".//p:Table_Delimited", NS)
    fields = table.findall(".//p:Field_Delimited", NS)
    definitions = {f.findtext("p:name", namespaces=NS): f for f in fields}
    ground = definitions["GROUND_TEMP"]
    if (
        ground.findtext("p:unit", namespaces=NS) != "kelvin"
        or "brightness" not in ground.findtext("p:description", default="", namespaces=NS).lower()
    ):
        raise ValueError("Expected labelled ground brightness temperature in kelvin")
    filename = root.findtext(".//p:File/p:file_name", namespaces=NS)
    if Path(filename).name != filename:
        raise ValueError("Expected a local PDS data filename")
    path = label.parent / filename
    frame = pd.read_csv(path)
    names = [f.findtext("p:name", namespaces=NS) for f in fields]
    if list(frame.columns) != names or len(frame) != int(
        table.findtext("p:records", namespaces=NS)
    ):
        raise ValueError("CSV columns/record count differ from PDS label")
    for name, field in definitions.items():
        for constants in field.findall("p:Special_Constants", NS):
            for constant in constants:
                frame[name] = frame[name].replace(float(constant.text), np.nan)
    for name in ["GROUND_TEMP", "GROUND_TEMP_UNCERTAINTY", *FLAGS]:
        frame[name] = pd.to_numeric(frame[name], errors="coerce")
    times = frame.LTST.str.extract(r"^(\d+) (\d{2}):(\d{2}):(\d{2})$").astype(float)
    valid_time = times.notna().all(axis=1) & times[1].lt(24) & times[2].lt(60) & times[3].lt(60)
    frame["ltst_sol"] = times[0]
    frame["ltst_hour"] = times[1]
    valid_value = (
        np.isfinite(frame.GROUND_TEMP)
        & frame.GROUND_TEMP.gt(0)
        & np.isfinite(frame.GROUND_TEMP_UNCERTAINTY)
        & frame.GROUND_TEMP_UNCERTAINTY.ge(0)
    )
    frame["valid_measurement"] = valid_time & valid_value
    frame["quality_supported"] = frame.valid_measurement & frame[list(FLAGS)].eq(1).all(axis=1)
    sol = int(label.name.split("_")[2])
    if sol not in (700, 701, 702):
        raise ValueError("This bounded pilot accepts MEDA sols 700–702 only")
    url = BASE + f"sol_{sol:04d}/"
    metadata = {
        "logical_identifier": root.findtext(".//p:logical_identifier", namespaces=NS),
        "version": root.findtext(".//p:Identification_Area/p:version_id", namespaces=NS),
        "utc_start": root.findtext(".//p:start_date_time", namespaces=NS),
        "utc_stop": root.findtext(".//p:stop_date_time", namespaces=NS),
        "quantity": "ground_brightness_temperature",
        "units": "K",
        "spatial_support": "rover-local TIRS footprint; no gridded CRS or regional representativeness",
        "records": len(frame),
        "temporal_support": "SCLK-indexed instrument samples; analysis uses hourly LTST bins",
        "spatial_resolution": "Instrument footprint dimensions not established in this pilot",
    }
    sources = [
        source_record(path, url + filename, **metadata),
        source_record(label, url + label.name, product="PDS4 label"),
    ]
    return frame, sources


def summarize(frame, qualified=True):
    """Equal-weight hourly medians; paired windows must share an LTST sol."""
    selected = frame[frame.quality_supported if qualified else frame.valid_measurement]
    hourly = (
        selected.groupby(["ltst_sol", "ltst_hour"])
        .agg(
            temperature_K=("GROUND_TEMP", "median"),
            reported_uncertainty_K=("GROUND_TEMP_UNCERTAINTY", "median"),
            samples=("GROUND_TEMP", "size"),
        )
        .reset_index()
    )
    result = []
    # Include observed sols with no eligible measurements as explicit unknowns.
    for sol in sorted(frame.loc[frame.valid_measurement, "ltst_sol"].unique()):
        item = {"ltst_sol": int(sol)}
        for name, a, b in [("night", 0, 3), ("day", 12, 15)]:
            hours = hourly[
                (hourly.ltst_sol == sol) & hourly.ltst_hour.ge(a) & hourly.ltst_hour.lt(b)
            ]
            enough = len(hours) >= 2
            item[name] = {
                "status": "available" if enough else "insufficient",
                "hour_bins": len(hours),
                "samples": int(hours.samples.sum()),
                "brightness_temperature_K": float(hours.temperature_K.median()) if enough else None,
            }
        day, night = (
            item["day"]["brightness_temperature_K"],
            item["night"]["brightness_temperature_K"],
        )
        item["sampled_day_night_contrast_K"] = (
            day - night if day is not None and night is not None else None
        )
        result.append(item)
    return result, hourly


def build_context(raw_dir):
    labels = sorted((Path(raw_dir) / "temperature/meda_calibrated").glob("*CAL_TIRS*.xml"))
    if not labels:
        return {
            "status": "missing",
            "reason": "No local calibrated MEDA TIRS products",
        }, pd.DataFrame()
    frames, sources = [], []
    for label in labels:
        frame, provenance = read_product(label)
        frames.append(frame)
        sources.extend(provenance)
    frame = pd.concat(frames, ignore_index=True)
    if frame.SCLK.duplicated().any():
        raise ValueError("Overlapping MEDA products: duplicate spacecraft clock samples")
    accepted, _ = summarize(frame)
    provisional, hourly = summarize(frame, qualified=False)
    qa = {
        flag: {
            "good": int(frame[flag].eq(1).sum()),
            "bad": int(frame[flag].eq(0).sum()),
            "unknown": int((~frame[flag].isin([0, 1])).sum()),
        }
        for flag in FLAGS
    }
    return {
        "status": "quality_supported" if frame.quality_supported.any() else "quality_incomplete",
        "quantity": "ground_brightness_temperature",
        "units": "K",
        "scope": "Jezero rover-local observations; not a 100 km target mean or global grid",
        "global_kinetic_surface_temperature_available": False,
        "records": len(frame),
        "quality_supported_records": int(frame.quality_supported.sum()),
        "quality_flags": qa,
        "sources": sources,
        "method": "LTST day [12,15), night [0,3); median of hourly medians; minimum 2 hour bins per window",
        "window_basis": "Project design assumption; fixed clock windows, not solar illumination classification",
        "qualified_windows": accepted,
        "provisional_unqualified_windows": provisional,
        "provisional_warning": "Exploratory observed values include failed/unknown flags; excluded from scoring and confirmed evidence",
        "same_ground_patch_confirmed": False,
        "limitations": [
            "Not kinetic surface temperature or full daily extrema",
            "Short sample is not a seasonal climatology",
            "Rover motion/footprint changes across windows are not resolved",
            "Reported uncertainty is instrument standard deviation, not window confidence",
        ],
    }, hourly

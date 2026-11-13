"""Read map-projected PDS3 images (simple cylindrical) into xarray."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import xarray as xr

_DTYPES = {
    ("MSB_INTEGER", 8): "i1",
    ("MSB_INTEGER", 16): ">i2",
    ("MSB_INTEGER", 32): ">i4",
    ("LSB_INTEGER", 16): "<i2",
    ("LSB_INTEGER", 32): "<i4",
    ("MSB_UNSIGNED_INTEGER", 8): "u1",
    ("UNSIGNED_INTEGER", 8): "u1",
    ("IEEE_REAL", 32): ">f4",
    ("PC_REAL", 32): "<f4",
}

_KEY_VALUE = re.compile(r"^\s*([\w:^]+)\s*=\s*(.+?)\s*$")


def parse_label(path: str | Path) -> dict[str, str]:
    """Return the KEY = VALUE pairs of a PDS3 label, keeping the first value of each key.

    Quotes and trailing units such as ``<KM>`` are removed.
    """
    label: dict[str, str] = {}
    for line in Path(path).read_text(errors="replace").splitlines():
        match = _KEY_VALUE.match(line)
        if not match:
            continue
        key, value = match.groups()
        value = re.sub(r"\s*<[^>]*>$", "", value).strip().strip('"').strip()
        label.setdefault(key, value)
    return label


def read_image(image_path: str | Path, label_path: str | Path | None = None) -> xr.DataArray:
    """Read a global simple-cylindrical PDS3 image as a (lat, lon) DataArray.

    Coordinates are cell centres in degrees. Latitude runs north to south and
    longitude runs from -180 to 180 east, whatever the source convention was.
    """
    image_path = Path(image_path)
    label_path = Path(label_path) if label_path else image_path.with_suffix(".lbl")
    label = parse_label(label_path)

    projection = label.get("MAP_PROJECTION_TYPE", "")
    if projection != "SIMPLE CYLINDRICAL":
        raise ValueError(f"{label_path.name}: unsupported projection {projection!r}")
    if label.get("POSITIVE_LONGITUDE_DIRECTION", "EAST") != "EAST":
        raise ValueError(f"{label_path.name}: only east-positive longitude is supported")

    lines = int(label["LINES"])
    samples = int(label["LINE_SAMPLES"])
    sample_key = (label["SAMPLE_TYPE"], int(label["SAMPLE_BITS"]))
    if sample_key not in _DTYPES:
        raise ValueError(f"{label_path.name}: unsupported sample type {sample_key}")
    dtype = np.dtype(_DTYPES[sample_key])

    expected = lines * samples * dtype.itemsize
    actual = image_path.stat().st_size
    if actual != expected:
        raise ValueError(f"{image_path.name}: size {actual} bytes, label implies {expected}")

    resolution = float(label["MAP_RESOLUTION"])  # pixels per degree
    north = float(label["MAXIMUM_LATITUDE"])
    west = float(label["WESTERNMOST_LONGITUDE"])

    data = np.fromfile(image_path, dtype=dtype).reshape(lines, samples)
    lat = north - (np.arange(lines) + 0.5) / resolution
    lon = west + (np.arange(samples) + 0.5) / resolution

    image = xr.DataArray(
        data.astype(dtype.newbyteorder("=")),
        dims=("lat", "lon"),
        coords={"lat": lat, "lon": lon},
        name=label.get("PRODUCT_ID", image_path.stem).lower(),
    )
    if lon.max() > 180:
        image = image.assign_coords(lon=((image.lon + 180) % 360) - 180).sortby("lon")
    return image

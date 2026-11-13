"""Download and load the global Mars grids used in this project.

All products come from the NASA PDS Geosciences Node and need no login.
"""

from __future__ import annotations

from pathlib import Path

import requests
import xarray as xr

from analog.pds import read_image

MARS_RADIUS_M = 3_396_000.0
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "mars"

_PDS = "https://pds-geosciences.wustl.edu"
_MOLA = f"{_PDS}/mgs/urn-nasa-pds-mgs_mola_topography_derived/meg016"
_TES = f"{_PDS}/mgs/mgs-m-tes-5-timap-v1/mgst_9001/data"

# name -> image URL; the detached label sits next to it with a .lbl suffix.
PRODUCTS = {
    # MGS MOLA topography above the areoid, metres, 16 pixels/degree (3.7 km).
    "mola_topography": f"{_MOLA}/megt90n000eb.img",
    # MGS TES nightside thermal inertia, J/(m^2 K s^0.5), 20 pixels/degree (3.0 km).
    "tes_thermal_inertia_night": f"{_TES}/global_ti_night_2007.img",
    # 0 where the thermal inertia map was filled in by interpolation.
    "tes_thermal_inertia_night_mask": f"{_TES}/global_ti_msk_night_2007.img",
}


def _fetch(url: str, dest: Path) -> Path:
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    partial = dest.with_suffix(dest.suffix + ".part")
    with requests.get(url, stream=True, timeout=60, headers={"User-Agent": "mars-analog"}) as r:
        r.raise_for_status()
        with open(partial, "wb") as f:
            f.writelines(r.iter_content(chunk_size=1 << 20))
    partial.rename(dest)
    return dest


def download(name: str, raw_dir: Path = RAW_DIR) -> Path:
    """Download one product (image and label) unless already present. Returns the image path."""
    url = PRODUCTS[name]
    image = _fetch(url, raw_dir / url.rsplit("/", 1)[1])
    label_url = url.rsplit(".", 1)[0] + ".lbl"
    _fetch(label_url, raw_dir / label_url.rsplit("/", 1)[1])
    return image


def load(name: str, raw_dir: Path = RAW_DIR) -> xr.DataArray:
    """Load a downloaded product as a (lat, lon) DataArray."""
    url = PRODUCTS[name]
    image = raw_dir / url.rsplit("/", 1)[1]
    if not image.exists():
        raise FileNotFoundError(f"{image} is missing; run scripts/download_mars.py first")
    return read_image(image).rename(name)


def load_thermal_inertia(raw_dir: Path = RAW_DIR, keep_interpolated: bool = True) -> xr.DataArray:
    """Nightside thermal inertia as floats, NaN where no value was derived.

    The archive derives values only between 5 and 5000; anything else is fill.
    """
    ti = load("tes_thermal_inertia_night", raw_dir).astype("float32")
    ti = ti.where((ti >= 5) & (ti <= 5000))
    if not keep_interpolated:
        mask = load("tes_thermal_inertia_night_mask", raw_dir)
        ti = ti.where(mask.values != 0)
    return ti

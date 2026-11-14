"""Export Mars-only target descriptors, availability inventory and dust time series."""

import argparse
import json
from pathlib import Path

import pandas as pd
import rasterio

from analog import dust, mars, swim
from analog.mars_profiles import build_profiles
from analog.pds import parse_label
from analog.provenance import source_record, write_json


def source_manifest(raw_dir):
    sources = []
    for module in (mars, swim, dust):
        for key, url in module.PRODUCTS.items():
            path = raw_dir / url.rsplit("/", 1)[1]
            if not path.exists():
                sources.append({"product": key, "url": url, "status": "missing"})
                continue
            metadata = {"product": key, "status": "available", "body": "Mars"}
            if module is mars:
                label = path.with_suffix(".lbl")
                if label.exists():
                    spec = parse_label(label)
                    metadata.update(
                        dataset_id=spec.get("DATA_SET_ID"),
                        observation_start=spec.get("START_TIME"),
                        observation_end=spec.get("STOP_TIME"),
                        creation_date=spec.get("PRODUCT_CREATION_TIME"),
                        map_resolution_px_per_degree=float(spec["MAP_RESOLUTION"]),
                        map_radius_m=float(spec["A_AXIS_RADIUS"]) * 1000,
                        coordinate_system=spec.get("COORDINATE_SYSTEM_NAME"),
                        map_projection=spec.get("MAP_PROJECTION_TYPE"),
                        longitude_direction=spec.get("POSITIVE_LONGITUDE_DIRECTION"),
                    )
                    sources.append(
                        source_record(
                            label,
                            url.rsplit(".", 1)[0] + ".lbl",
                            product=key + "_label",
                            status="available",
                        )
                    )
                metadata["units"] = (
                    "m above areoid"
                    if key == "mola_topography"
                    else (
                        "interpolation mask: 0 means infilled"
                        if key.endswith("_mask")
                        else "J m-2 K-1 s-0.5"
                    )
                )
            elif module is swim:
                with rasterio.open(path) as src:
                    metadata.update(
                        crs=src.crs.to_wkt(),
                        native_pixel_size_m=[src.transform.a, -src.transform.e],
                        native_shape=[src.height, src.width],
                        nodata=src.nodata,
                        version="SWIM 2.0",
                        units="ice consistency, dimensionless",
                        observation_period="composite; no single acquisition period in GeoTIFF",
                    )
            else:
                with dust.open_dataset(path) as ds:
                    metadata.update(
                        version=ds.attrs.get("version"),
                        creation_date=ds.attrs.get("creation_date"),
                        units="dimensionless absorption optical depth",
                        wavelength_micron=9.3,
                        native_grid_degrees=[3, 3],
                        native_shape=dict(ds.sizes),
                        period=key,
                        license="CC-BY-SA-3.0",
                        citation="https://doi.org/10.1029/2019JE006111",
                        source_instruments="MRO MCS; see individual file title",
                        interpretation="observation-constrained kriged scenario, not direct site measurement",
                    )
            sources.append(source_record(path, url, **metadata))
    return sources


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--targets",
        type=Path,
        help="JSON keyed by target ID, with Mars lat/lon and coordinate source",
    )
    p.add_argument("--raw-dir", type=Path, default=mars.RAW_DIR)
    p.add_argument("--output", type=Path, default=Path("outputs/mars_profiles"))
    p.add_argument(
        "--strict", action="store_true", help="Exit nonzero if any source missing/invalid"
    )
    args = p.parse_args()
    targets = json.loads(args.targets.read_text()) if args.targets else None
    result, series = build_profiles(targets, args.raw_dir)
    result["sources"] = source_manifest(args.raw_dir)
    result["dust_data_license"] = "CC-BY-SA-3.0; see LICENSE-data.md"
    write_json(args.output / "profiles.json", result)
    for (target, year), ds in series.items():
        # Keep only per-sol data, not source contact details or redundant global attributes.
        table = pd.DataFrame(
            {key: ds[key].values for key in ["Time", "SOY", "Ls", "cdodtot", "cdod610", "cdodrel"]}
        )
        table.to_csv(args.output / f"{target}_{year}_series.csv", index=False)
    lines = [
        "# 火星端資料交接",
        "",
        "本輪只處理火星資料。地球端下載、QA、特徵處理與配對交由隊友。",
        "profiles.json 保留單位、缺值、來源及方法；這些描述值不是綜合相似度或任務成功率。",
        "",
        "| 目標 | 火星 lat, lon | 地形 | TES 排除插值後有效比例 | SWIM 0–1 m 平均一致性 | MY34 / MY35 平均 CDOD |",
        "|---|---|---|---|---|---|",
    ]

    def number(v):
        return "unknown" if v is None else f"{v:.4f}"

    for name, v in result["profiles"].items():
        ti = v["thermal_inertia"]
        ice = v["ice"]["0_1m"]
        yrs = v["dust"]
        lines.append(
            f"| {name} | {v['lat']}, {v['lon']} | {v['terrain']['status']} | {number(ti.get('valid_fraction'))} | {number(ice.get('mean'))} | {number(yrs['dust_my34'].get('mean_cdodtot'))} / {number(yrs['dust_my35'].get('mean_cdodtot'))} |"
        )
    lines += ["", "## 接軌規則", ""] + [f"- {s}" for s in result["earth_team_handoff"]]
    lines += ["", "## 仍缺的火星資料／定義", ""] + [
        f"- {s}" for s in result["missing_requirements"]
    ]
    lines += [
        "",
        "沙塵以最近的原始 3° 網格呈現，並附 669-sol 序列與 Ls 分季摘要；不能說是 100 km 場址內的細尺度觀測。",
        "TES 熱慣量排除原始遮罩為 0 的插值填補值，另列包含填補的摘要。SWIM 值不是冰含量或機率；0 不能當作未知或證明有冰。",
        "Arcadia 目標中心是專案設計假設，不是官方選定登陸點。所有目標仍需任務需求與地面證據查證。",
        "",
    ]
    (args.output / "handoff.md").write_text("\n".join(lines))
    (args.output / "LICENSE-data.md").write_text("""# Mars dust-derived data terms

The Montabone MY34/MY35 NetCDF sources specify Creative Commons Attribution-ShareAlike 3.0 Unported (https://creativecommons.org/licenses/by-sa/3.0/).

The exported dust time-series CSV files, dust-derived portions of profiles.json and handoff.md, the dust_cdod layer of data/processed/mars_stack_0p5deg.nc, and the dust-derived similarity figure outputs/figures/mars_selftest_arcadia.png are distributed under those same terms. Changes: native-cell extraction, statistical summaries and seasonal grouping. Credit Montabone et al. (2020), https://doi.org/10.1029/2019JE006111, and Montabone et al. (2015), https://doi.org/10.1016/j.icarus.2014.12.034. Source URLs and SHA-256 are in profiles.json.

No warranties are provided. This notice does not assign a licence to the repository's program code or change the terms of MOLA, TES or SWIM source products; consult their providers. Earth datasets and Earth-team work are not part of this export.
""")
    print(json.dumps(result["inventory"], indent=2))
    print(args.output / "handoff.md")
    if result["errors"] or (
        args.strict and any(i["status"] != "loaded" for i in result["inventory"].values())
    ):
        raise SystemExit(2)


if __name__ == "__main__":
    main()

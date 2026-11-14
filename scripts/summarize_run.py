"""Export handoff tables and explicit weight/scale sensitivity from completed runs."""

import csv
import json
import shutil
from pathlib import Path

import pandas as pd

from analog.earth import RAW_DIR
from analog.matching import FEATURES
from analog.provenance import write_json


def main():
    root = Path(__file__).resolve().parents[1]
    folder = root / "outputs/analysis"
    data = json.loads((folder / "results_with_context.json").read_text())
    coarse = json.loads((root / "outputs/analysis_scale10km/results.json").read_text())
    sensitivity = {}
    rows = []
    lines = [
        "# 候選交接表",
        "",
        "本表來自實際資料運算。只代表區域地形距離排名；所有候選均為本專案提出、尚待驗證。",
        "地形差異越小越接近所定義的三項統計特徵，不代表形態、地質或整體火星相似度。",
        "",
        "| 火星目標 | 地形排名 | 地球中心 (lat, lon) | 地形距離 | 2023–2024 氣溫 °C | 降水 mm/day |",
        "|---|---:|---|---:|---:|---:|",
    ]
    for target, items in data["candidates"].items():
        base = {(i["lat"], i["lon"]) for i in items[:2]}
        alt = {(i["lat"], i["lon"]) for i in coarse["candidates"][target][:2]}
        sensitivity[target] = {
            "base_4km_top2": sorted(base),
            "alternative_10km_top2": sorted(alt),
            "top2_overlap_count": len(base & alt),
            "interpretation": "sampling-scale sensitivity; not confidence",
        }
        full = pd.read_csv(folder / f"{target}_all_ranked.csv")
        sensitivity[target]["weight_variants"] = {}
        # Recompute separated top two fairly on the SAME eligible windows and target.
        from analog.matching import select_separated, terrain_distance

        vector = [data["targets"][target][k] for k in FEATURES]
        for name, weights in [
            ("slope_emphasis", [0.4, 0.4, 0.2]),
            ("relief_emphasis", [0.1, 0.1, 0.8]),
        ]:
            d = terrain_distance(full[list(FEATURES)].values, vector, weights=weights)
            ix = select_separated(full.lat.values, full.lon.values, d, 2, 300)
            selected = {(float(full.iloc[i].lat), float(full.iloc[i].lon)) for i in ix}
            sensitivity[target]["weight_variants"][name] = {
                "weights": weights,
                "separated_top2": sorted(selected),
                "top2_overlap_count": len(base & selected),
            }
        for item in items:
            context = item.get("earth_climate_context", {})
            summary = context.get("summary", {})
            temp = summary.get("T2M", {}).get("value")
            rain = summary.get("PRECTOTCORR", {}).get("value")
            row = {
                k: v
                for k, v in item.items()
                if k not in ("footprint", "earth_climate_context", "sensitivity_raw_ranks")
            }
            row.update(
                {
                    "earth_T2M_C_2023_2024": temp,
                    "earth_precip_mm_day_2023_2024": rain,
                    "climate_role": "context_only_not_ranked" if summary else "unknown",
                }
            )
            rows.append(row)
            if item["rank"] <= 2:
                t = "unknown" if temp is None else f"{temp:.2f}"
                r = "unknown" if rain is None else f"{rain:.3f}"
                lines.append(
                    f"| {target} | {item['rank']} | {item['lat']:.1f}, {item['lon']:.1f} | {item['terrain_distance']:.4f} | {t} | {r} |"
                )
    write_json(folder / "sensitivity.json", sensitivity)
    with (folder / "shortlist.csv").open("w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=list(rows[0]) if rows else ["candidate_id"], lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    lines += [
        "",
        "每一候選代表 100 × 100 km 區域；完整足跡見 candidates.geojson。火星目標座標見 results.json。",
        "氣溫為 POWER 的 2 m 氣溫，不是 MODIS 地表溫度；降水為月資料依天數加權的 24 個月平均日降水。",
        "Arcadia (40°N, 170°W) 是專案設計目標，不是官方確定登陸點；沒有確認地下冰或冰資源可採性。",
        "",
        "## 敏感度",
        "",
    ]
    for target, s in sensitivity.items():
        overlaps = {k: v["top2_overlap_count"] for k, v in s["weight_variants"].items()}
        lines.append(
            f"- {target}: 改用 10 km 取樣，前兩名保留 {s['top2_overlap_count']}/2；權重變動保留數 {overlaps}。"
        )
    lines += [
        "",
        "4 km 與 10 km 的視窗合格數不同，陸地遮罩取樣會使合格集合略變；這是整體流程敏感度，不能解讀為單純數值精度比較。",
        "",
        "## 建議接手工作",
        "",
        "- Jezero 前兩名的氣候並不支持乾旱類比，應保留為地形參照，先不要當作整體推薦。",
        "- 若要先查乾燥候選，可研究 Arcadia 地形清單的 29°N, 105°W 與 35°N, 57°E；這是後續查證優先順序，未改動原地形排名。",
        "- 查證各候選既有類比研究、地質與礦物、冰與季節、可實作測試及進入許可。不能把非熱門地區直接當成新發現。",
        "- 不可宣稱前兩名穩定、整體四面向相似，或可直接用來判定著陸安全。",
        "",
    ]
    (folder / "candidate_handoff.md").write_text("\n".join(lines))
    meta = folder / "source_metadata"
    meta.mkdir(exist_ok=True)
    for p in RAW_DIR.glob("*_manifest.json"):
        shutil.copyfile(p, meta / p.name)
    shutil.copyfile(RAW_DIR / "public_sources.json", meta / "public_sources.json")
    from analog.mars import RAW_DIR as MARS_RAW

    (meta / "megt90n000eb.lbl").write_text((MARS_RAW / "megt90n000eb.lbl").read_text())
    for p in (RAW_DIR / "power").glob("*.json"):
        if p.name.startswith("power_+33.000_+87.000"):
            continue  # connection probe, not a ranked candidate
        shutil.copyfile(p, meta / p.name)
    print(folder / "candidate_handoff.md")


if __name__ == "__main__":
    main()

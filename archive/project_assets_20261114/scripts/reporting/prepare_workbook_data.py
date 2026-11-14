"""Prepare a loss-aware scientific-data bundle for the consolidated workbook.

Standard-library only. Run from any directory with Python 3.10+:
    python scripts/reporting/prepare_workbook_data.py

Reads scientific CSVs in outputs/docs, the three MEDA calibrated CSVs,
JSON/GeoJSON in outputs/docs/data, and non-website project Markdown reports.
Writes only outputs/consolidated/support/workbook_data.json. It does not score,
rank, filter observations, modify source data, or author the Excel workbook.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
SUPPORT = ROOT / "outputs/consolidated/support"
MAX_CELL_UNITS = 32000
NUMBER = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")
TEXT_KEYS = {
    "candidate_id", "sample_id", "parent_sample_id", "id", "LMST", "LTST", "sha256",
    "source_doi", "source_locator", "coordinate_datum", "source_file", "period_key",
}
LABELS = {
    "run_id": "分析版本", "candidate_key": "版本＋候選識別碼", "candidate_id": "候選ID",
    "source_file": "來源檔案", "source_row": "來源起始行號", "source_pointer": "來源JSON pointer",
    "lat": "緯度（度）", "lon": "東經（度）", "mars_target": "火星參照區",
    "window_km": "視窗大小（km）", "sample_spacing_km": "採樣間距（km）",
    "slope_stencil_km": "坡度差分尺度（km）", "terrain_distance": "地形描述距離（越小越近）",
    "descriptor_score": "實驗性描述分數（非信心）", "original_order": "原始候選順序",
    "GROUND_TEMP": "GROUND_TEMP 亮溫（K）", "AIR_TEMP": "AIR_TEMP 氣溫（K）",
    "GROUND_TEMP_UNCERTAINTY": "GROUND_TEMP 不確定度（K）",
    "AIR_TEMP_UNCERTAINTY": "AIR_TEMP 不確定度（K）",
    "json_pointer": "JSON pointer", "value_type": "原值型別", "number_value": "數值原值",
    "boolean_value": "布林原值", "text_value": "文字原值／JSON字面值",
    "part": "分片序號", "parts": "總分片數", "start_line": "原始起始行",
    "end_line": "原始結束行", "paragraph": "段落序號", "content": "完整段落文字",
}
EXCLUDED_DIRS = {
    "web", "node_modules", "__pycache__", "venv", ".venv", "dist", "build",
    ".git", ".codex", ".agents", ".aws", ".ssh", ".cache", ".pytest_cache",
}
SECRET_FILE = re.compile(
    r"(?:^|[_.-])(?:credentials?|secrets?|tokens?|passwords?)(?:[_.-]|$)", re.IGNORECASE
)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def safe_file(path: Path) -> bool:
    if not path.is_file() or path.name.startswith(".") or SECRET_FILE.search(path.name):
        return False
    try:
        path.resolve().relative_to(ROOT.resolve())
    except ValueError:
        return False
    return True


def walk_files(base: Path, suffixes: set[str]) -> list[Path]:
    result = []
    for parent, directories, filenames in os.walk(base, followlinks=False):
        directories[:] = sorted(
            d for d in directories
            if d not in EXCLUDED_DIRS and not d.startswith(".")
            and not (Path(parent) / d).is_symlink()
            and relative(Path(parent) / d) != "outputs/consolidated"
        )
        for name in sorted(filenames):
            path = Path(parent) / name
            if path.suffix.lower() in suffixes and safe_file(path):
                result.append(path)
    return sorted(result)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def text_parts(value: str, max_units: int = MAX_CELL_UNITS) -> list[str]:
    """Excel's limit is UTF-16 units; never split a Unicode character."""
    if len(value) * 2 <= max_units:
        return [value]
    chunks, buffer, units = [], [], 0
    for char in value:
        size = 2 if ord(char) > 0xFFFF else 1
        if units + size > max_units:
            chunks.append("".join(buffer))
            buffer, units = [], 0
        buffer.append(char)
        units += size
    chunks.append("".join(buffer))
    return chunks


def scalar(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    return value


def csv_value(value: str | None, key: str) -> Any:
    if value is None or value == "":
        return None
    if key in TEXT_KEYS or key.endswith(("_id", "_sha256", "_doi")):
        return value
    stripped = value.strip()
    if not NUMBER.fullmatch(stripped):
        return value
    integer_part = stripped.lstrip("+-").split(".")[0]
    if len(integer_part) > 1 and integer_part.startswith("0") and "." not in stripped:
        return value  # identifiers and clock-like values with leading zeroes stay textual
    if "." not in stripped and "e" not in stripped.lower():
        if len(stripped.lstrip("+-")) > 15:
            return value  # Excel cannot preserve longer integer identifiers as numbers
        return int(stripped)
    parsed = float(stripped)
    return parsed if math.isfinite(parsed) else value


def numeric_key(key: str) -> bool:
    return key in {
        "lat", "lon", "rank", "original_rank", "source_row", "bytes", "score",
        "Time", "SOY", "Ls", "cdodtot", "cdod610", "cdodrel", "SCLK", "samples",
        "window_km", "sample_spacing_km", "slope_stencil_km", "original_order",
        "year", "month", "number_value", "part", "parts", "start_line", "end_line",
        "paragraph", "valid_months", "expected_months",
    } or key.endswith(("_deg", "_km", "_m", "_K", "_C", "_fraction", "_rank", "_distance"))


def column(key: str, values: list[Any]) -> dict:
    nonblank = [v for v in values if v is not None]
    if nonblank and all(isinstance(v, bool) for v in nonblank):
        kind = "boolean"
    elif (nonblank and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in nonblank)) or (
        not nonblank and numeric_key(key)
    ):
        kind = "number"
    else:
        kind = "text"
    if kind == "number":
        integer = nonblank and all(isinstance(v, int) or float(v).is_integer() for v in nonblank)
        fmt = "0" if integer else "0.000000"
        return {"key": key, "label": LABELS.get(key, key), "type": kind, "width": 17, "format": fmt}
    width = 15 if kind == "boolean" else 25
    if key in {"source_file", "path", "source_urls", "url", "evidence", "weaknesses", "content",
               "text_value", "source_pointer", "json_pointer", "interpretation", "note"}:
        width = 65
    if key in {"source_row", "source_record", "part", "parts", "start_line", "end_line"}:
        width = 12
    return {"key": key, "label": LABELS.get(key, key), "type": kind, "width": width}


class Bundle:
    def __init__(self) -> None:
        self.tables: list[dict] = []
        self.coverage: list[dict] = []
        self.long_cells: list[list[Any]] = []
        self.hashes: dict[str, str] = {}

    def add_coverage(self, path: Path, rows: int, sheet: str, method: str) -> None:
        rel = relative(path)
        if rel not in self.hashes:
            self.hashes[rel] = digest(path)
        self.coverage.append({
            "path": rel, "rows": rows, "sheet": sheet, "method": method,
            "sha256": self.hashes[rel],
        })

    def table(self, name: str, title: str, note: str, kind: str,
              keys: list[str], rows: list[list[Any]]) -> None:
        if len(name) >= 31 or name in {t["name"] for t in self.tables}:
            raise ValueError(f"Invalid or duplicate sheet name: {name}")
        if any(len(row) != len(keys) for row in rows):
            raise ValueError(f"Row-width mismatch in {name}")
        for row_index, row in enumerate(rows, start=2):
            for col_index, value in enumerate(row):
                if isinstance(value, str):
                    parts = text_parts(value)
                    if len(parts) > 1:
                        for part_no, part in enumerate(parts, start=1):
                            self.long_cells.append([name, row_index, keys[col_index], part_no,
                                                    len(parts), part])
                        row[col_index] = parts[0]
        columns = [column(key, [r[i] for r in rows]) for i, key in enumerate(keys)]
        self.tables.append({"name": name, "title": title, "note": note, "kind": kind,
                            "columns": columns, "rows": rows})

    def records(self, name: str, title: str, note: str, kind: str,
                records: list[dict], preferred: list[str] | None = None) -> None:
        keys = list(preferred or [])
        for record in records:
            for key in record:
                if key not in keys:
                    keys.append(key)
        self.table(name, title, note, kind, keys,
                   [[scalar(record.get(key)) for key in keys] for record in records])


def load_json(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def run_metadata(path: Path) -> dict:
    if relative(path).startswith("outputs/analysis_scale10km/"):
        return {"run_id": "earth_100km_sample10km", "window_km": 100,
                "sample_spacing_km": 10, "slope_stencil_km": 20}
    return {"run_id": "earth_100km_sample4km", "window_km": 100,
            "sample_spacing_km": 4, "slope_stencil_km": 8}


def scientific_csvs(bundle: Bundle) -> dict[str, list[dict]]:
    paths = walk_files(ROOT / "outputs", {".csv"}) + walk_files(ROOT / "docs", {".csv"})
    paths += sorted((ROOT / "data/raw/mars/temperature/meda_calibrated").glob("*.CSV"))
    groups: OrderedDict[str, dict] = OrderedDict()
    raw_lookup: dict[str, list[dict]] = {}
    notes = {
        "地球視窗全量": "兩版皆為100 km視窗；4/10 km是採樣間距。完整CSV列，非新增評分。",
        "地球排序明細": "保留原始target與距離欄名；terrain_distance越小越近，不是信心或百分比。",
        "地球候選CSV": "原始shortlist CSV完整保留；與JSON主候選視圖重複，不作獨立樣本加總。",
        "火星塵埃序列": "MY34/MY35、9.3μm吸收CDOD。cdodtot/cdod610/cdodrel保留各自意義。",
        "漫遊車暫定溫度": "原始72行provisional資料，未完成品質資格確認；非全球或候選區溫度。",
        "MEDA原始紀錄": "三份完整校準CSV；GROUND_TEMP=地表亮溫(K)，AIR_TEMP=氣溫(K)；原始旗標不合格列仍保留，未據此認證可用。"
                       "LMST/LTST保留文字；filename sol不等於每筆LTST sol；8個狀態欄與不確定度完整保留。",
        "既有檔案清單": "原始清單是當時快照，非目前磁碟完整性結論；list_origin區分原始來源。",
        "火星新穎性查核": "15點的既有查核紀錄；無命中不證明新穎性，所有精確同用途查核仍有範圍限制。",
    }
    mapped = {
        "research_requirements.csv": "研究需求", "claim_ledger.csv": "報告主張",
        "submission_gap_checklist_2026-11-14.csv": "提交缺口",
        "oytag_literature_points.csv": "Oytag文獻座標",
        "oytag_supplement_coordinates.csv": "Oytag補充座標",
        "mars_discovery_novelty_checks.csv": "火星新穎性查核",
    }
    unknown = 0
    for path in sorted(set(paths)):
        rel = relative(path)
        raw = "meda_calibrated/" in rel
        additions: dict[str, Any] = {}
        if path.name == "earth_terrain_features.csv":
            group = "地球視窗全量"
            additions.update(run_metadata(path))
        elif path.name.endswith("_all_ranked.csv"):
            group = "地球排序明細"
            additions.update(run_metadata(path))
            target = path.name.removesuffix("_all_ranked.csv")
            additions.update(mars_target=target, source_distance_column=f"{target}_terrain_distance")
        elif path.name == "shortlist.csv":
            group = "地球候選CSV"
            additions.update(run_metadata(path))
        elif raw:
            group = "MEDA原始紀錄"
        elif re.fullmatch(r"(?:jezero|gale|arcadia)_dust_my\d+_series\.csv", path.name):
            group = "火星塵埃序列"
            target, _, year, _ = path.stem.split("_", 3)
            additions.update(mars_target=target, mars_year=int(year.removeprefix("my")))
        elif path.name == "provisional_hourly.csv":
            group = "漫遊車暫定溫度"
        elif path.name in {"earth_inventory.csv", "repository_inventory.csv"}:
            group = "既有檔案清單"
            additions["list_origin"] = path.name
        elif path.name in mapped:
            group = mapped[path.name]
        else:
            unknown += 1
            group = f"其他CSV_{unknown:02d}"
        content = groups.setdefault(group, {"keys": [], "rows": [], "kind": "raw" if raw else "data"})
        row_count = 0
        saved_records = []
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            fields = reader.fieldnames or []
            if not fields or len(set(fields)) != len(fields):
                raise ValueError(f"Missing/duplicate CSV headings in {rel}")
            keys = list(additions) + fields + ["source_file", "source_row"]
            if group == "地球排序明細":
                keys.insert(len(additions), "terrain_distance")
            for key in keys:
                if key not in content["keys"]:
                    content["keys"].append(key)
                    for old in content["rows"]:
                        old.append(None)
            previous_line = reader.line_num
            for raw_record in reader:
                source_line = previous_line + 1
                previous_line = reader.line_num
                if None in raw_record or any(v is None for v in raw_record.values()):
                    raise ValueError(f"CSV field count mismatch: {rel}:{source_line}")
                record = {**additions,
                          **{key: csv_value(value, key) for key, value in raw_record.items()},
                          "source_file": rel, "source_row": source_line}
                if group == "地球排序明細":
                    record["terrain_distance"] = record[record["source_distance_column"]]
                content["rows"].append([record.get(key) for key in content["keys"]])
                row_count += 1
                if group == "火星新穎性查核":
                    saved_records.append(record)
        if group == "火星新穎性查核":
            raw_lookup["novelty"] = saved_records
        bundle.add_coverage(path, row_count, group,
                            "Complete CSV; original columns retained; source_row is physical start line")
    for name, content in groups.items():
        bundle.table(name, name, notes.get(name, "原始CSV全部行；保留原欄與來源行號，空欄為null。"),
                     content["kind"], content["keys"], content["rows"])
    return raw_lookup


def primary_candidates(bundle: Bundle) -> None:
    records = []
    available_runs = 0
    for path, primary in [("outputs/matching_handoff/matching_data.json", True),
                          ("outputs/analysis_scale10km/results.json", False)]:
        if not (ROOT / path).is_file():
            continue  # Retired terrain rankings are not required by new research.
        available_runs += 1
        data = load_json(path)
        candidates = data["candidates"]
        pointer_records = []
        if primary:
            pointer_records = [(f"/candidates/{i}", c) for i, c in enumerate(candidates)]
        else:
            for target, values in candidates.items():
                pointer_records += [(f"/candidates/{target}/{i}", c) for i, c in enumerate(values)]
        for pointer, candidate in pointer_records:
            meta = run_metadata(ROOT / path)
            record = {**meta, "candidate_key": meta["run_id"] + ":" + candidate["candidate_id"]}
            for key, value in candidate.items():
                if not isinstance(value, (dict, list)):
                    record[key] = value
            record["footprint_json"] = scalar(candidate.get("footprint"))
            ranks = candidate.get("sensitivity_raw_ranks", {})
            record["slope_emphasis_raw_rank"] = ranks.get("slope_emphasis")
            record["relief_emphasis_raw_rank"] = ranks.get("relief_emphasis")
            context = candidate.get("earth_climate_context", {})
            record["earth_climate_status"] = context.get("status", "not_present_in_this_run")
            for key in ["T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR", "WS10M"]:
                summary = context.get("summary", {}).get(key, {})
                for field in ["value", "unit", "valid_months", "expected_months"]:
                    record[f"power_{key}_{field}"] = summary.get(field)
            record.update(source_file=path, source_pointer=pointer)
            records.append(record)
        bundle.add_coverage(ROOT / path, len(pointer_records), "地球候選",
                            "Primary 36 enriched + sensitivity 36; detailed source JSON separately archived")
    keys = [r["candidate_key"] for r in records]
    if len(keys) != len(set(keys)) or len(records) != available_runs * 36:
        raise ValueError("Expected 36 candidates per available run with unique keys")
    if not records:
        return
    bundle.records("地球候選", "地球候選：主分析與尺度敏感度", "兩版各36點；ID必須連同分析版本使用。"
                   "POWER為2023–2024氣候背景，未參與地形排名。全部JSON細節另存JSON原值。", "data", records)


def mars_discovery(bundle: Bundle, csv_lookup: dict[str, list[dict]]) -> None:
    path = "outputs/mars_discovery/mars_site_discovery.json"
    data = load_json(path)
    card_file = "outputs/mars_discovery/reporting_cards.json"
    cards = {c["id"]: c for c in load_json(card_file)["cards"]}
    novelty = {r["candidate_id"]: r for r in csv_lookup.get("novelty", [])}
    initials = {"isru_shallow_ice": "I", "dusty_flat_ops": "D", "firm_rocky_surface": "F"}
    records = []
    for purpose, spec in data["purposes"].items():
        for index, pick in enumerate(spec["picks"]):
            ident = f"{initials[purpose]}-{index + 1:02d}"
            review, card = novelty.get(ident), cards.get(ident)
            if review and (review["latitude_deg"] != pick["lat"] or
                           review["longitude_east_signed_deg"] != pick["lon"]):
                raise ValueError(f"Discovery/novelty coordinate mismatch for {ident}")
            records.append({
                "candidate_id": ident, "purpose": purpose, "purpose_label": spec.get("label"),
                "original_order": index + 1, "lat": pick["lat"], "lon": pick["lon"],
                "descriptor_score": pick["score"], **pick["layers"],
                "review_status": review["same_purpose_exact_site_status"] if review else "未查",
                "editorial_recommendation": review.get("editorial_recommendation") if review else None,
                "review_note": review.get("review_note") if review else None,
                "reporting_card_status": "保留研究／背景卡片" if card else "未入保留卡片",
                "intended_use": card.get("intended_use") if card else None,
                "treatment": card.get("treatment") if card else None,
                "weaknesses": card.get("weaknesses") if card else None,
                "prohibited_claims": scalar(card.get("prohibited_claims")) if card else None,
                "novelty_status": card.get("novelty_status") if card else
                    (review.get("same_purpose_exact_site_status") if review else "未查"),
                "source_file": path, "source_pointer": f"/purposes/{purpose}/picks/{index}",
                "review_source": "docs/mars_discovery_novelty_checks.csv" if review else None,
                "card_source": card_file if card else None,
            })
    if len(records) != 24:
        raise ValueError("Expected all 24 original discovery picks")
    bundle.records("火星發現候選", "火星用途候選：完整24點與查核狀態", "原始順序與分數完整保留；15點有初查、4點有Reporting卡片。"
                   "分數非信心或落地許可，未查者明示未查，firm-ground工程用途證據不足。", "data", records)
    bundle.add_coverage(ROOT / path, len(records), "火星發現候選", "All picks, original order; join existing review/card status only")
    bundle.add_coverage(ROOT / card_file, len(cards), "火星發現候選", "Existing four reporting cards joined by stable I/D/F ID")


def flatten_scalars(data: dict, prefix: str = "") -> dict:
    result = {}
    for key, value in data.items():
        name = prefix + key
        if isinstance(value, dict):
            result.update(flatten_scalars(value, name + "."))
        elif not isinstance(value, list):
            result[name] = value
    return result


def mars_profiles(bundle: Bundle) -> None:
    path = "outputs/mars_profiles/profiles.json"
    data = load_json(path)
    records = []
    for target, profile in data["profiles"].items():
        # These are only three complete profile summaries; all nested source values are archived too.
        record = {"mars_target": target, **flatten_scalars(profile), "source_file": path,
                  "source_pointer": "/profiles/" + target}
        records.append(record)
    bundle.records("火星參照區", "既有三個火星參照區的100 km摘要", "Jezero/Gale/Arcadia既有參照。"
                   "熱慣量不是溫度／硬度；SWIM不是含冰量；塵埃是3°背景。不可與發現候選0.5°單元混用。", "data", records)
    bundle.add_coverage(ROOT / path, len(records), "火星參照區", "Three known reference-region profiles; flattened scalar summaries")


def ice_qa(bundle: Bundle) -> None:
    path = "outputs/research/ice_candidate_followup/native_audit.json"
    data = load_json(path)
    records = []
    for index, candidate in enumerate(data["candidates"]):
        record = {"candidate_id": candidate["id"], "lat": candidate["center_lat_lon"][0],
                  "lon": candidate["center_lat_lon"][1], **candidate["stored_layers"],
                  "stored_score_unchanged": candidate["stored_score_unchanged"],
                  "nominal_NS_km": candidate["nominal_size_km_NS_EW_at_center"][0],
                  "nominal_EW_km": candidate["nominal_size_km_NS_EW_at_center"][1],
                  "source_file": path, "source_pointer": f"/candidates/{index}"}
        for key in ["mola_native_cell", "mola_native_cell_slopes", "tes_native_non_infilled_cell",
                    "nominal_2015_EZ_screen", "native_recomputed_minus_stored"]:
            for field, value in candidate[key].items():
                if not isinstance(value, (list, dict)):
                    record[key + "." + field] = value
        record["tes_mask_zero_pixels_excluded"] = candidate["tes_mask_zero_pixels_excluded"]
        for key in ["swim_0_1m", "swim_1_5m_context_only"]:
            record[key + ".coarsened_then_interpolated"] = candidate[key]["coarsened_then_interpolated"]
            for field, value in candidate[key]["nominal_cell_native_stats"].items():
                if not isinstance(value, (list, dict)):
                    record[key + ".native." + field] = value
        records.append(record)
    bundle.records("冰候選原生QA", "I-01／I-02 原生資料查核", "兩點未重新評分或排序。"
                   "深淺SWIM共用輸入；通過缺值檢查不證明有可挖冰。2015名義區域檢查不是完整新穎性證明。", "data", records)
    bundle.add_coverage(ROOT / path, len(records), "冰候選原生QA", "Two original QA summaries; all interpolation details also archived")


def regional_temperature(bundle: Bundle) -> None:
    path = "outputs/mars_regional_temperature/context.json"
    data = load_json(path)
    records = []
    for target, profile in data["profiles"].items():
        for index, sample in enumerate(profile["series"]):
            records.append({"mars_target": target,
                            "requested_lat": profile["requested_center"]["lat"],
                            "requested_lon": profile["requested_center"]["lon"],
                            "selected_lat": profile["selected_grid_coordinate"]["lat"],
                            "selected_lon": profile["selected_grid_coordinate"]["lon"],
                            **sample, "status": profile["status"],
                            "scoring_eligible": profile["scoring_eligible"],
                            "quantity": profile["quantity"], "units": profile["units"],
                            "source_file": path, "source_pointer": f"/profiles/{target}/series/{index}"})
    if len(records) != 864:
        raise ValueError("Expected 864 regional-temperature year/season bins including nulls")
    bundle.records("火星區域溫度背景", "火星區域溫度背景：完整864個季節格", "5°格網、MY29–36、每年36個Ls格；"
                   "缺值保留null。03/15時取樣不是同一sol日極值；metadata incomplete、scoring_eligible=false。", "data", records)
    bundle.add_coverage(ROOT / path, len(records), "火星區域溫度背景", "All target/year/Ls bins; missing values preserved")


def power_context(bundle: Bundle) -> None:
    records = []
    for path in sorted((ROOT / "outputs/analysis/source_metadata").glob("power_*.json")):
        data = json.loads(path.read_text())
        coordinates = data["geometry"]["coordinates"]
        parameters = data["properties"]["parameter"]
        periods = sorted(set().union(*(set(v) for v in parameters.values())))
        for period in periods:
            year, month = int(period[:4]), int(period[4:])
            if month not in set(range(1, 14)):
                raise ValueError(f"Unexpected NASA POWER period: {period}")
            record = {"lat": coordinates[1], "lon": coordinates[0], "period_key": period,
                      "period_type": "annual" if month == 13 else "monthly", "year": year,
                      "month": None if month == 13 else month,
                      "source_fill_value": data["header"].get("fill_value"),
                      "time_standard": data["header"].get("time_standard"),
                      "source_file": relative(path)}
            for parameter, values in parameters.items():
                record[parameter] = values.get(period)
                record[parameter + "_unit"] = data["parameters"][parameter]["units"]
            records.append(record)
        bundle.add_coverage(path, len(periods), "地球POWER氣候", "All 24 monthly + 2 annual periods; no averaging or fill deletion")
    if len(records) != 156:
        raise ValueError("Expected six POWER locations x 26 period keys")
    bundle.records("地球POWER氣候", "NASA POWER 2023–2024月值與年值", "YYYY13是年值，month留空，不是第13個月，"
                   "不能與月值混合平均。T2M是2m氣溫，不是MODIS地表溫度。原始fill值保留並列source_fill_value。", "data", records)


def pointer_component(key: str) -> str:
    return key.replace("~", "~0").replace("/", "~1")


def json_leaves(value: Any, pointer: str = ""):
    if isinstance(value, dict) and value:
        for key, child in value.items():
            yield from json_leaves(child, pointer + "/" + pointer_component(key))
    elif isinstance(value, list) and value:
        for index, child in enumerate(value):
            yield from json_leaves(child, pointer + "/" + str(index))
    else:
        yield pointer, value


def archive_json(bundle: Bundle) -> None:
    rows = []
    paths = []
    for base in ["outputs", "docs", "data"]:
        paths.extend(walk_files(ROOT / base, {".json", ".geojson"}))
    for path in sorted(set(paths)):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        count = 0
        for pointer, value in json_leaves(data):
            if value is None:
                kind, number, boolean, text = "null", None, None, "null"
            elif isinstance(value, bool):
                kind, number, boolean, text = "boolean", None, value, "true" if value else "false"
            elif isinstance(value, (float, int)):
                number = value if not isinstance(value, float) or math.isfinite(value) else None
                # Preserve the exact parsed numeric representation as text too (Excel has 15-digit precision).
                kind, boolean, text = "number", None, json.dumps(value, allow_nan=True)
            elif isinstance(value, str):
                kind, number, boolean, text = "string", None, None, value
            elif isinstance(value, list):
                kind, number, boolean, text = "empty_array", None, None, "[]"
            elif isinstance(value, dict):
                kind, number, boolean, text = "empty_object", None, None, "{}"
            else:
                raise TypeError(type(value))
            parts = text_parts(text)
            for index, part in enumerate(parts, start=1):
                rows.append([relative(path), pointer, kind, number, boolean, part, index, len(parts)])
                count += 1
        bundle.add_coverage(path, count, "JSON原值", "Every scalar/null/empty-container leaf; RFC6901 pointer; long strings split")
    bundle.table("JSON原值", "全部科學JSON／GeoJSON原值", "包含outputs/docs/data的全部純量葉值、null、空物件與空陣列；"
                 "排除consolidated避免遞迴。number_value是數值，text_value同時保留數字字面值。"
                 "字串分片須按source_file/json_pointer/part重組。不是獨立樣本表，不能跨檔相加。", "archive",
                 ["source_file", "json_pointer", "value_type", "number_value", "boolean_value",
                  "text_value", "part", "parts"], rows)


def markdown_paragraphs(text: str):
    buffer, start, paragraph = [], 1, 0
    for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
        if not buffer:
            start = line_number
        buffer.append(line)
        if not line.strip():
            paragraph += 1
            yield paragraph, start, line_number, "".join(buffer)
            buffer = []
    if buffer:
        paragraph += 1
        yield paragraph, start, line_number, "".join(buffer)


def archive_markdown(bundle: Bundle) -> None:
    rows = []
    for path in walk_files(ROOT, {".md"}):
        # All non-website project Markdown, including reports, readmes, and method notes.
        text = path.read_bytes().decode("utf-8-sig")
        count = 0
        for paragraph, start, end, content in markdown_paragraphs(text):
            parts = text_parts(content, 600)
            for index, part in enumerate(parts, start=1):
                rows.append([relative(path), paragraph, start, end, index, len(parts), part])
                count += 1
        bundle.add_coverage(path, count, "報告內容", "All Markdown paragraphs with physical source lines; long text split; website/dependencies excluded")
    bundle.table("報告內容", "非網站專案Markdown完整段落", "保留原始文件路徑、段落順序與行號；"
                 "每片不超過600個UTF-16字元單位，依文件/paragraph/part重組。含歷史報告與限制，不代表所有舊狀態都是最新狀態。", "archive",
                 ["source_file", "paragraph", "start_line", "end_line", "part", "parts", "content"], rows)


def finish_long_cells(bundle: Bundle) -> None:
    if bundle.long_cells:
        saved = bundle.long_cells
        bundle.long_cells = []
        bundle.table("長欄位完整分片", "其他表超長欄位完整分片", "其他表若超過Excel單格上限，其第一片留在原表，"
                     "完整內容按sheet/data_row/column_key/part重組；data_row含第1列欄名。", "archive",
                     ["sheet", "data_row", "column_key", "part", "parts", "content"], saved)
        if bundle.long_cells:
            raise ValueError("Unexpected recursive text split")


def main() -> None:
    bundle = Bundle()
    csv_lookup = scientific_csvs(bundle)
    primary_candidates(bundle)
    mars_discovery(bundle, csv_lookup)
    mars_profiles(bundle)
    ice_qa(bundle)
    regional_temperature(bundle)
    power_context(bundle)
    archive_json(bundle)
    archive_markdown(bundle)
    finish_long_cells(bundle)
    preferred = ["火星發現候選", "冰候選原生QA", "地球候選", "火星新穎性查核", "火星參照區",
                 "地球視窗全量", "地球排序明細", "地球POWER氣候", "火星塵埃序列", "火星區域溫度背景",
                 "漫遊車暫定溫度", "研究需求", "報告主張", "提交缺口", "Oytag文獻座標", "Oytag補充座標",
                 "地球候選CSV", "既有檔案清單", "MEDA原始紀錄", "JSON原值", "報告內容", "長欄位完整分片"]
    bundle.tables.sort(key=lambda table: preferred.index(table["name"]) if table["name"] in preferred else 99)
    counts = {table["name"]: len(table["rows"]) for table in bundle.tables}
    expected = {"MEDA原始紀錄": 159418,
                "火星發現候選": 24, "冰候選原生QA": 2,
                "火星新穎性查核": 15, "火星塵埃序列": 4014, "火星區域溫度背景": 864,
                "地球POWER氣候": 156, "漫遊車暫定溫度": 72}
    for name, count in {"地球視窗全量": 5212, "地球排序明細": 15636,
                        "地球候選": 72}.items():
        if name in counts:
            expected[name] = count
    for name, count in expected.items():
        if counts.get(name) != count:
            raise ValueError(f"Coverage mismatch for {name}: {counts.get(name)} != {count}")
    for table in bundle.tables:
        if len(table["rows"]) + 1 > 1048576:
            raise ValueError(f"Excel row limit exceeded: {table['name']}")
        if len(table["columns"]) > 16384:
            raise ValueError(f"Excel column limit exceeded: {table['name']}")
    counts.update(
        tables=len(bundle.tables), rows_all_tables=sum(len(t["rows"]) for t in bundle.tables),
        source_files=len(bundle.hashes), coverage_entries=len(bundle.coverage),
        raw_rows=sum(len(t["rows"]) for t in bundle.tables if t["kind"] == "raw"),
    )
    result = {
        "generated_taipei": datetime.now(ZoneInfo("Asia/Taipei")).isoformat(),
        "tables": bundle.tables, "coverage": bundle.coverage, "counts": counts,
        "limitations": [
            "整併既存資料，不新增評分、不重新排序、不推論新穎性、冰量或落地安全性。",
            "同一來源的CSV、JSON、交接與歷史報告可能重複，不可把多個視圖當成獨立樣本加總。",
            "地球兩版皆為100km視窗，採樣間距4/10km，坡度尺度8/20km；candidate_id須連同run_id使用。",
            "火星發現0.5°單元、既有火星100km參照區與地球視窗不是相同支持範圍。",
            "分數和距離不是機率／信心；SWIM不是含冰量；TES熱慣量不是溫度／硬度。",
            "地球T2M氣溫、地表溫度、火星亮溫、校正區域背景溫度等不同觀測量不可直接混用。",
            "POWER YYYY13為年值，不是第13月；原始fill值保留，使用分析前須按來源規則識別。",
            "MEDA原始CSV全部159418列完整保留，不因QA旗標刪列；GROUND_TEMP為亮溫。",
            "MEDA LMST/LTST為火星時鐘文字；檔名sol與LTST行內容可能跨日，未轉成地球日曆。",
            "JSON null、空容器及CSV空欄保留；空欄不是0。超長文字用part/parts分片保留。",
            "JSON數值同時存數值與文字表示；Excel約15位有效數字的限制不改變原始來源檔。",
            "大型NC/HDF/TIFF/影像/ZIP只由主工作表檔案索引列出，不展開到本bundle。",
            "網站、依賴、Git、隱藏設定與秘密檔案不讀取；outputs/consolidated排除避免遞迴。",
            "來源與報告為產生此bundle時的快照，未驗證所有舊報告結論或重新執行科學管線。",
        ],
    }
    SUPPORT.mkdir(parents=True, exist_ok=True)
    destination = SUPPORT / "workbook_data.json"
    temporary = SUPPORT / "workbook_data.json.tmp"
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
        stream.write("\n")
    temporary.replace(destination)
    print(json.dumps({"bundle": relative(destination), "bytes": destination.stat().st_size,
                      "counts": counts, "sheets": [
                          {"name": t["name"], "kind": t["kind"], "rows": len(t["rows"]),
                           "columns": len(t["columns"])} for t in bundle.tables]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

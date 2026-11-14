"""Stream the complete MEDA worksheet into the Artifact Tool-authored workbook.

Capacity fallback only: Artifact Tool still authors every other worksheet, all
styles, formulas, layout, and the raw header/table. Its full-raw export exceeded
the Node heap. This module replaces the seven-row raw preview with ALL bundle
rows through the standard XLSX ZIP/XML format; it does not create another book.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import posixpath
import re
import shutil
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
RAW_NAME = "MEDA原始紀錄"
OVERVIEW_NAME = "總覽"


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def attr(tag: bytes, name: str) -> str | None:
    match = re.search(rb"\b" + name.encode() + rb"\s*=\s*([\"'])(.*?)\1", tag)
    return match.group(2).decode() if match else None


def set_attr(tag: bytes, name: str, value: str) -> bytes:
    pattern = rb"\b" + name.encode() + rb"\s*=\s*([\"'])(.*?)\1"
    replacement = name.encode() + b"=" + quoteattr(value).encode()
    if re.search(pattern, tag):
        return re.sub(pattern, lambda _: replacement, tag, count=1)
    return re.sub(rb"(/?>)$", lambda m: b" " + replacement + m.group(1), tag, count=1)


def resolve_part(parent: str, target: str) -> str:
    result = posixpath.normpath(target.lstrip("/") if target.startswith("/") else
                               posixpath.join(posixpath.dirname(parent), target))
    if result.startswith("../") or result == "..":
        raise ValueError("Relationship points outside the XLSX package")
    return result


def relations(archive: zipfile.ZipFile, part: str) -> dict[str, str]:
    rel_part = posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")
    tree = ET.fromstring(archive.read(rel_part))
    return {item.attrib["Id"]: resolve_part(part, item.attrib["Target"])
            for item in tree if local(item.tag) == "Relationship"
            and item.attrib.get("TargetMode") != "External"}


def workbook_parts(archive: zipfile.ZipFile) -> tuple[str, bytes, dict[str, str]]:
    root_rels = ET.fromstring(archive.read("_rels/.rels"))
    target = next(item.attrib["Target"] for item in root_rels
                  if item.attrib.get("Type", "").endswith("/officeDocument"))
    workbook_part = resolve_part("", target)
    xml = archive.read(workbook_part)
    rels = relations(archive, workbook_part)
    sheets = {}
    for item in ET.fromstring(xml).iter():
        if local(item.tag) == "sheet":
            sheets[item.attrib["name"]] = rels[item.attrib[f"{{{RNS}}}id"]]
    return workbook_part, xml, sheets


def expand_dimension(prefix: bytes, ref: str) -> bytes:
    match = re.search(rb"<(?:[\w.-]+:)?dimension\b[^>]*?/?>", prefix)
    if match:
        return prefix[:match.start()] + set_attr(match.group(), "ref", ref) + prefix[match.end():]
    root = re.search(rb"<(?P<prefix>[\w.-]+:)?worksheet\b[^>]*>", prefix)
    if not root:
        raise ValueError("Raw worksheet root opening tag missing")
    namespace_prefix = root.group("prefix") or b""
    dimension = b"<" + namespace_prefix + b"dimension ref=" + quoteattr(ref).encode() + b"/>"
    position = root.end()
    properties = re.search(rb"<(?P<prefix>[\w.-]+:)?sheetPr\b[^>]*?/?>", prefix[root.end():])
    if properties:
        properties_start = root.end() + properties.start()
        properties_end = root.end() + properties.end()
        if properties.group().endswith(b"/>"):
            position = properties_end
        else:
            property_prefix = properties.group("prefix") or b""
            closing = re.search(rb"</" + re.escape(property_prefix) + rb"sheetPr\s*>",
                                prefix[properties_end:])
            if not closing:
                raise ValueError(f"Raw sheetPr at byte {properties_start} has no closing tag")
            position = properties_end + closing.end()
    return prefix[:position] + dimension + prefix[position:]


def sheet_template(xml: bytes, ref: str) -> tuple[bytes, bytes, bytes, str, dict[int, str]]:
    opening = re.search(rb"<(?P<prefix>[\w.-]+:)?sheetData\b[^>]*>", xml)
    if not opening or opening.group().endswith(b"/>"):
        raise ValueError("Expected header plus seven raw preview rows")
    prefix_name = (opening.group("prefix") or b"").decode()
    closing = re.search(rb"</" + re.escape(prefix_name.encode()) + rb"sheetData\s*>", xml[opening.end():])
    if not closing:
        raise ValueError("Raw sheetData closing tag missing")
    end = opening.end() + closing.start()
    body = xml[opening.end():end]
    row_open = re.search(rb"<(?P<prefix>[\w.-]+:)?row\b[^>]*>", body)
    if not row_open or attr(row_open.group(), "r") != "1":
        raise ValueError("Raw header is not the first worksheet row")
    row_prefix = row_open.group("prefix") or b""
    row_close = re.search(rb"</" + re.escape(row_prefix) + rb"row\s*>", body[row_open.end():])
    if not row_close:
        raise ValueError("Raw header closing tag missing")
    header_end = row_open.end() + row_close.end()
    header = body[row_open.start():header_end]
    tree = ET.fromstring(xml)  # Only the small Artifact Tool preview, never the expanded raw XML.
    styles = {}
    for row in tree.iter():
        if local(row.tag) == "row" and row.attrib.get("r") == "2":
            for cell in row:
                if "s" in cell.attrib:
                    letters = re.match(r"[A-Z]+", cell.attrib["r"]).group()
                    styles[column_index(letters)] = cell.attrib["s"]
    prefix = expand_dimension(xml[:opening.end()], ref)
    return prefix, header, xml[end:], row_prefix.decode(), styles


def column_name(index: int) -> str:
    result = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def column_index(letters: str) -> int:
    result = 0
    for letter in letters:
        result = result * 26 + ord(letter) - 64
    return result


def expand_table(xml: bytes, ref: str, columns: int) -> bytes:
    tree = ET.fromstring(xml)
    table_columns = next(item for item in tree if local(item.tag) == "tableColumns")
    if len(table_columns) != columns:
        raise ValueError("Raw table column count differs from the bundle")
    opening = re.search(rb"<(?:[\w.-]+:)?table\b[^>]*>", xml)
    if not opening:
        raise ValueError("Raw table root tag missing")
    xml = xml[:opening.start()] + set_attr(opening.group(), "ref", ref) + xml[opening.end():]
    filtering = re.search(rb"<(?:[\w.-]+:)?autoFilter\b[^>]*?/?>", xml)
    if not filtering:
        raise ValueError("Raw table autoFilter missing")
    return xml[:filtering.start()] + set_attr(filtering.group(), "ref", ref) + xml[filtering.end():]


def recalculate_on_open(xml: bytes) -> bytes:
    match = re.search(rb"<(?:[\w.-]+:)?calcPr\b[^>]*?/?>", xml)
    if match:
        tag = set_attr(set_attr(match.group(), "fullCalcOnLoad", "1"), "forceFullCalc", "1")
        return xml[:match.start()] + tag + xml[match.end():]
    root = re.search(rb"<(?P<prefix>[\w.-]+:)?workbook\b[^>]*>", xml)
    prefix = root.group("prefix") or b""
    calc = b"<" + prefix + b'calcPr fullCalcOnLoad="1" forceFullCalc="1"/>'
    # Preserve workbook schema order if any elements normally following calcPr exist.
    later = re.search(rb"<(?:[\w.-]+:)?(?:oleSize|customWorkbookViews|pivotCaches|smartTagPr|"
                      rb"smartTagTypes|webPublishing|fileRecoveryPr|webPublishObjects|extLst)\b", xml)
    closing = re.search(rb"</" + re.escape(prefix) + rb"workbook\s*>", xml)
    position = later.start() if later else closing.start()
    return xml[:position] + calc + xml[position:]


def repair_count_cache(xml: bytes, row_count: int, last_row: int) -> tuple[bytes, str]:
    for opening in re.finditer(rb"<(?P<prefix>[\w.-]+:)?c\b[^>]*>", xml):
        if attr(opening.group(), "r") != "B11":
            continue
        prefix = opening.group("prefix") or b""
        closing = re.search(rb"</" + re.escape(prefix) + rb"c\s*>", xml[opening.end():])
        if not closing:
            raise ValueError("Overview B11 closing tag missing")
        end = opening.end() + closing.end()
        cell = xml[opening.start():end]
        parsed = ET.fromstring(b'<root xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                              b'xmlns:r="' + RNS.encode() + b'">' + cell + b"</root>") if not prefix else None
        if parsed is not None:
            formula = next((node.text or "" for node in parsed.iter() if local(node.tag) == "f"), "")
        else:
            f = re.search(rb"<(?:[\w.-]+:)?f\b[^>]*>(.*?)</(?:[\w.-]+:)?f>", cell, re.DOTALL)
            formula = (f.group(1).decode() if f else "")
        expected = f"COUNTA('{RAW_NAME}'!A2:A{last_row})"
        if formula.lstrip("=").replace(" ", "") != expected.replace(" ", ""):
            raise ValueError(f"Overview B11 formula changed unexpectedly: {formula}")
        cache = re.search(rb"<(?:[\w.-]+:)?v\b[^>]*(?:/>|>.*?</(?:[\w.-]+:)?v>)", cell, re.DOTALL)
        new_cache = b"<" + prefix + b"v>" + str(row_count).encode() + b"</" + prefix + b"v>"
        if cache:
            cell = cell[:cache.start()] + new_cache + cell[cache.end():]
        else:
            closing_cell = cell.rfind(b"</" + prefix + b"c")
            cell = cell[:closing_cell] + new_cache + cell[closing_cell:]
        new_opening = set_attr(opening.group(), "t", "n")
        cell = new_opening + cell[len(opening.group()):]
        return xml[:opening.start()] + cell + xml[end:], formula
    raise ValueError("Overview B11 raw count cell missing")


def write_raw(stream, template: tuple, rows: list[list], columns: int) -> dict:
    prefix, header, tail, namespace_prefix, styles = template
    stream.write(prefix)
    stream.write(header)
    nonempty_a, written_cells, text_cells = 0, 0, 0
    for row_number, row in enumerate(rows, start=2):
        if len(row) != columns:
            raise ValueError(f"Raw row {row_number} column mismatch")
        nonempty_a += int(row[0] is not None and row[0] != "")
        pieces = [f'<{namespace_prefix}row r="{row_number}">']
        for index, value in enumerate(row, start=1):
            reference = column_name(index) + str(row_number)
            style = f' s="{styles[index]}"' if index in styles else ""
            opening = f'<{namespace_prefix}c r="{reference}"{style}'
            if value is None:
                pieces.append(opening + "/>")
            elif isinstance(value, bool):
                pieces.append(opening + f' t="b"><{namespace_prefix}v>{int(value)}</{namespace_prefix}v></{namespace_prefix}c>')
            elif isinstance(value, (int, float)):
                if isinstance(value, float) and not math.isfinite(value):
                    raise ValueError("Nonfinite numeric value in raw bundle")
                pieces.append(opening + f'><{namespace_prefix}v>{value}</{namespace_prefix}v></{namespace_prefix}c>')
            elif isinstance(value, str):
                pieces.append(opening + f' t="inlineStr"><{namespace_prefix}is><{namespace_prefix}t '
                              f'xml:space="preserve">{escape(value)}</{namespace_prefix}t>'
                              f'</{namespace_prefix}is></{namespace_prefix}c>')
                text_cells += 1
            else:
                raise TypeError(f"Unsupported raw value type: {type(value)}")
            written_cells += 1
        pieces.append(f"</{namespace_prefix}row>")
        stream.write("".join(pieces).encode("utf-8"))
    stream.write(tail)
    return {"raw_rows": len(rows), "raw_cells": written_cells,
            "raw_text_cells_inline_string": text_cells, "nonempty_A_count": nonempty_a}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="outputs/consolidated/support/workbook_base.xlsx")
    parser.add_argument("--bundle", default="outputs/consolidated/support/workbook_data.json")
    parser.add_argument("--output", default="outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx")
    args = parser.parse_args()
    base, bundle_path, output = [Path(value) if Path(value).is_absolute() else ROOT / value
                                 for value in [args.base, args.bundle, args.output]]
    if base.resolve() == output.resolve():
        raise ValueError("Base and final workbook must be different paths")
    with bundle_path.open(encoding="utf-8") as stream:
        bundle = json.load(stream)
    raw = next(table for table in bundle["tables"] if table["name"] == RAW_NAME)
    rows, columns = raw["rows"], len(raw["columns"])
    if len(rows) != 159418 or columns != 23 or raw["kind"] != "raw":
        raise ValueError("Expected complete 159418 x 23 MEDA bundle")
    nonempty_count = sum(row[0] is not None and row[0] != "" for row in rows)
    last_row = len(rows) + 1
    full_ref = f"A1:{column_name(columns)}{last_row}"
    output.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=output.stem + "_", suffix=".tmp", dir=output.parent)
    os.close(handle)
    temporary = Path(temp_name)
    try:
        with zipfile.ZipFile(base) as source:
            workbook_part, workbook_xml, sheets = workbook_parts(source)
            raw_part, overview_part = sheets[RAW_NAME], sheets[OVERVIEW_NAME]
            raw_xml = source.read(raw_part)
            template = sheet_template(raw_xml, full_ref)
            raw_relationships = relations(source, raw_part)
            table_ids = [node.attrib[f"{{{RNS}}}id"] for node in ET.fromstring(raw_xml).iter()
                         if local(node.tag) == "tablePart"]
            if len(table_ids) != 1:
                raise ValueError("Expected one complete raw-data Excel Table")
            table_part = raw_relationships[table_ids[0]]
            overview_xml, formula = repair_count_cache(source.read(overview_part), nonempty_count, last_row)
            replacements = {workbook_part: recalculate_on_open(workbook_xml),
                            overview_part: overview_xml,
                            table_part: expand_table(source.read(table_part), full_ref, columns)}
            raw_stats = {}
            unchanged_parts = 0
            with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED,
                                 compresslevel=6, allowZip64=True) as target:
                target.comment = source.comment
                for info in source.infolist():
                    info_copy = copy.copy(info)
                    if info.filename == raw_part:
                        with target.open(info_copy, "w", force_zip64=True) as stream:
                            raw_stats = write_raw(stream, template, rows, columns)
                    elif info.filename in replacements:
                        target.writestr(info_copy, replacements[info.filename])
                    else:
                        with source.open(info) as src, target.open(info_copy, "w", force_zip64=True) as dst:
                            shutil.copyfileobj(src, dst, length=1024 * 1024)
                        unchanged_parts += 1
            if raw_stats.get("raw_rows") != 159418 or raw_stats.get("nonempty_A_count") != nonempty_count:
                raise ValueError("Raw stream count mismatch")
        with zipfile.ZipFile(temporary) as check:
            bad = check.testzip()
            if bad:
                raise ValueError(f"ZIP CRC check failed: {bad}")
        os.replace(temporary, output)
        report = {
            "generated_taipei": datetime.now(ZoneInfo("Asia/Taipei")).isoformat(),
            "method": "Capacity-limited fallback: preserve Artifact Tool workbook; stream complete raw worksheet XML",
            "reason": "Artifact Tool full-MEDA export exceeded Node 4GB heap; no raw records omitted",
            "base": str(base.relative_to(ROOT)), "output": str(output.relative_to(ROOT)),
            "raw_sheet_name": RAW_NAME, "raw_sheet_part": raw_part, "raw_table_part": table_part,
            "dimension_and_table_ref": full_ref, **raw_stats,
            "original_raw_columns": 21, "source_columns": 2,
            "string_preservation": "All raw strings use inlineStr; LMST/LTST/source_file preserved exactly",
            "numeric_and_boolean_types_preserved": True, "null_cells_left_blank": True,
            "overview_formula_unchanged": formula, "overview_B11_cached_value": nonempty_count,
            "fullCalcOnLoad": True, "forceFullCalc": True,
            "other_zip_parts_copied_unchanged": unchanged_parts,
            "modified_parts": [raw_part, workbook_part, overview_part, table_part],
            "xlsx_bytes": output.stat().st_size,
            "xlsx_sha256": hashlib.sha256(output.read_bytes()).hexdigest(), "zip_crc_check": "PASS",
        }
        review = ROOT / "outputs/consolidated/review"
        review.mkdir(parents=True, exist_ok=True)
        (review / "stream_export.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(report, ensure_ascii=False, indent=2))
    finally:
        if temporary.exists():
            temporary.unlink()


if __name__ == "__main__":
    main()

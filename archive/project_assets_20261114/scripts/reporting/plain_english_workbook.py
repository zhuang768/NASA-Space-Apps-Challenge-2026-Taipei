"""Plain-white English workbook editing through streaming XLSX XML.

The existing Artifact Tool-authored book contains over four million cells; its
full-object re-export exceeded the 4 GB Node heap. This capacity fallback edits
that existing package, without loading the complete workbook into a sheet model.
Original raw files and the original-workbook backup are never modified.

Translation schema: source_strings.json has entries [{id, text, contexts}];
translations_merged.json is {id: EnglishString}. Run --apply only after approval
of that complete map. --verify is read-only except its JSON evidence report.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import posixpath
import re
import shutil
import tempfile
import xml.etree.ElementTree as ET
import xml.sax
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from xml.sax.handler import ContentHandler, feature_external_ges, feature_external_pes
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesImpl
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "outputs/consolidated/review/plain_english"
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
ET.register_namespace("x", NS)
ET.register_namespace("r", RNS)
CJK = re.compile(r"[\u3400-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]")
SHEET_NAMES = {
    "總覽": "Overview", "火星發現候選": "Mars Discovery", "冰候選原生QA": "Ice Candidate QA",
    "地球候選": "Earth Candidates", "火星新穎性查核": "Mars Novelty Review",
    "火星參照區": "Mars Reference Regions", "地球視窗全量": "Earth Terrain Windows",
    "地球排序明細": "Earth Terrain Ranks", "地球POWER氣候": "Earth POWER Climate",
    "火星塵埃序列": "Mars Dust Series", "火星區域溫度背景": "Mars Regional Temp",
    "漫遊車暫定溫度": "Rover Temp Provisional", "研究需求": "Research Requirements",
    "報告主張": "Report Claims", "提交缺口": "Submission Gaps", "Oytag文獻座標": "Oytag Literature Points",
    "Oytag補充座標": "Oytag Supplement Points", "地球候選CSV": "Earth Shortlist CSV",
    "既有檔案清單": "Legacy File Inventories", "MEDA原始紀錄": "MEDA Raw Records",
    "JSON原值": "JSON Source Records", "報告內容": "Report Text", "檔案索引": "File Index",
    "匯入對照": "Source Crosswalk",
}
OVERRIDES = {
    ("總覽", "D42"): "Numeric values preserved; explanatory source text translated into English. Original files retain verbatim text.",
    ("總覽", "D43"): "English rendering of report text; source paths and paragraph/part fields retained. Original Markdown files remain authoritative.",
    ("JSON原值", "F1"): "Text value (English rendering)",
}
TECHNICAL_HEADERS = {
    "來源檔案", "來源檔", "專案相對路徑", "JSON pointer", "source_file", "source_pointer", "json_pointer",
    "candidate_id", "候選ID", "版本＋候選識別碼", "sample_id", "parent_sample_id", "id", "sha256",
    "source_doi", "source_locator", "source_sheet", "LMST", "LTST", "SCLK", "period_key", "file", "folder", "path",
    "Source File", "Source file", "Source Path", "Project Relative Path", "JSON Pointer",
}


def local(name: str) -> str:
    return name.rsplit("}", 1)[-1].rsplit(":", 1)[-1]


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def part_target(parent: str, target: str) -> str:
    result = posixpath.normpath(target.lstrip("/") if target.startswith("/") else
                               posixpath.join(posixpath.dirname(parent), target))
    if result.startswith("../"):
        raise ValueError("Invalid XLSX relationship target")
    return result


def sheet_parts(archive: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = "xl/workbook.xml"
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {node.attrib["Id"]: part_target(workbook, node.attrib["Target"])
               for node in rels if node.attrib.get("TargetMode") != "External"}
    tree = ET.fromstring(archive.read(workbook))
    return [(node.attrib["name"], targets[node.attrib[f"{{{RNS}}}id"]])
            for node in tree.iter() if local(node.tag) == "sheet"]


def is_header(sheet: str, row: int) -> bool:
    return row == 1 or (sheet == "總覽" and row in {6, 15, 22})


def literal_identifier(text: str) -> bool:
    if any(delimiter in text for delimiter in ["\n", "\r", "；", ";", "，", "："]):
        return False
    if re.fullmatch(r"https?://\S+", text):
        return True
    return bool(re.fullmatch(r"(?:\.{0,2}/|(?:data|docs|outputs|scripts|analog|tests)/).+\.[A-Za-z0-9]{1,12}", text))


class Translations:
    def __init__(self, source_strings: Path, translations: Path) -> None:
        self.source = json.loads(source_strings.read_text())
        mapping = json.loads(translations.read_text())
        if not isinstance(mapping, dict):
            raise TypeError("translations_merged.json must be {id: EnglishString}")
        missing, bad = [], []
        self.by_text = {}
        for entry in self.source["entries"]:
            value = mapping.get(entry["id"])
            if value is None:
                missing.append(entry["id"])
            elif not isinstance(value, str) or not value or CJK.search(value):
                bad.append(entry["id"])
            else:
                self.by_text[entry["text"]] = value
        if missing or bad:
            raise ValueError(f"Incomplete English map: missing={missing[:30]}, invalid={bad[:30]}")
        self.by_text.update(SHEET_NAMES)
        self.by_text["文字原值／JSON字面值"] = "Text value (English rendering)"
        self.technical_headers = TECHNICAL_HEADERS | {
            self.by_text.get(header, header) for header in TECHNICAL_HEADERS
        }
        self.count = len(mapping)

    def text(self, value: str, sheet: str, coordinate: str, header: str | None = None) -> str:
        override = OVERRIDES.get((sheet, coordinate))
        if override is not None:
            return override
        row = int(re.search(r"\d+$", coordinate).group()) if coordinate else 0
        if row != 1 and (header in self.technical_headers or literal_identifier(value)):
            return value
        return self.by_text.get(value, value)

    def formula(self, value: str) -> str:
        result = value
        for old, new in SHEET_NAMES.items():
            result = result.replace("'" + old.replace("'", "''") + "'!", "'" + new + "'!")
            result = result.replace(old + "!", "'" + new + "'!")
        # Only literal display labels are translated. External file/URL targets stay exact.
        def quoted(match: re.Match) -> str:
            literal = match.group()[1:-1].replace('""', '"')
            translated = self.by_text.get(literal, literal)
            return '"' + translated.replace('"', '""') + '"'
        result = re.sub(r'"(?:[^"]|"")*"', quoted, result)
        for old, new in self.by_text.items():
            if CJK.search(old):
                result = result.replace("[" + old + "]", "[" + new + "]")
        return result


def serialize(root: ET.Element) -> bytes:
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def plain_styles(xml: bytes) -> tuple[bytes, dict[int, int], int]:
    root = ET.fromstring(xml)
    def child(tag: str, parent: ET.Element = root) -> ET.Element:
        return next(node for node in parent if local(node.tag) == tag)
    def font_plain(font: ET.Element) -> None:
        for tag, attributes in [("name", {"val": "Arial"}), ("sz", {"val": "11"}),
                                ("color", {"rgb": "FF000000"})]:
            for node in list(font):
                if local(node.tag) == tag:
                    font.remove(node)
            ET.SubElement(font, f"{{{NS}}}{tag}", attributes)
    for font in child("fonts"):
        font_plain(font)
    fills = child("fills")
    # Standard reserved none/gray125 fills remain unused; all active styles use explicit solid white.
    for index, fill in enumerate(fills):
        if index >= 2:
            fill.clear()
            pattern = ET.SubElement(fill, f"{{{NS}}}patternFill", {"patternType": "solid"})
            ET.SubElement(pattern, f"{{{NS}}}fgColor", {"rgb": "FFFFFFFF"})
            ET.SubElement(pattern, f"{{{NS}}}bgColor", {"rgb": "FFFFFFFF"})
    white = len(fills)
    fill = ET.SubElement(fills, f"{{{NS}}}fill")
    pattern = ET.SubElement(fill, f"{{{NS}}}patternFill", {"patternType": "solid"})
    ET.SubElement(pattern, f"{{{NS}}}fgColor", {"rgb": "FFFFFFFF"})
    ET.SubElement(pattern, f"{{{NS}}}bgColor", {"rgb": "FFFFFFFF"})
    fills.set("count", str(len(fills)))
    xfs = child("cellXfs")
    original = list(xfs)
    header_map = {}
    def style_plain(xf: ET.Element, wrap: bool) -> None:
        xf.set("fillId", str(white))
        xf.set("applyFill", "1")
        xf.set("applyFont", "1")
        xf.set("applyAlignment", "1")
        alignment = next((n for n in xf if local(n.tag) == "alignment"), None)
        if alignment is None:
            alignment = ET.SubElement(xf, f"{{{NS}}}alignment")
        alignment.set("wrapText", "1" if wrap else "0")
        alignment.set("shrinkToFit", "0")
        alignment.set("vertical", "center")
    for index, xf in enumerate(original):
        style_plain(xf, False)
        header = copy.deepcopy(xf)
        style_plain(header, True)
        header_map[index] = len(xfs)
        xfs.append(header)
    xfs.set("count", str(len(xfs)))
    for xf in child("cellStyleXfs"):
        style_plain(xf, False)
    for dxf in child("dxfs"):
        for font in [n for n in dxf if local(n.tag) == "font"]:
            font_plain(font)
        for fill in [n for n in dxf if local(n.tag) == "fill"]:
            fill.clear()
            pattern = ET.SubElement(fill, f"{{{NS}}}patternFill", {"patternType": "solid"})
            ET.SubElement(pattern, f"{{{NS}}}fgColor", {"rgb": "FFFFFFFF"})
    return serialize(root), header_map, len(original)


def workbook_xml(xml: bytes, translations: Translations) -> bytes:
    root = ET.fromstring(xml)
    for node in root.iter():
        if local(node.tag) == "sheet":
            node.set("name", SHEET_NAMES[node.attrib["name"]])
        elif local(node.tag) == "definedName":
            if CJK.search(node.attrib.get("name", "")):
                raise ValueError("CJK defined-name identifier needs explicit naming review")
            if node.text:
                node.text = translations.formula(node.text)
    return serialize(root)


def table_xml(xml: bytes, translations: Translations) -> bytes:
    root = ET.fromstring(xml)
    names = []
    for node in root.iter():
        if local(node.tag) == "tableColumn":
            old = node.attrib["name"]
            new = translations.by_text.get(old, old)
            node.set("name", new)
            names.append(new)
        elif local(node.tag) in {"calculatedColumnFormula", "totalsRowFormula"} and node.text:
            node.text = translations.formula(node.text)
    if len(names) != len({name.casefold() for name in names}):
        raise ValueError(f"Translated table headers are not unique: {names}")
    info = next((n for n in root if local(n.tag) == "tableStyleInfo"), None)
    if info is None:
        info = ET.SubElement(root, f"{{{NS}}}tableStyleInfo")
    info.attrib.update(name="TableStyleLight1", showFirstColumn="0", showLastColumn="0",
                       showRowStripes="0", showColumnStripes="0")
    return serialize(root)


def digest_record(hasher, value: object) -> None:
    hasher.update(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    hasher.update(b"\n")


class SheetStream(ContentHandler):
    """SAX transformer and bounded-memory semantic verifier; no cell graph."""
    def __init__(self, sheet: str, translations: Translations, transform: bool,
                 output=None, header_map: dict[int, int] | None = None) -> None:
        super().__init__()
        self.sheet, self.translations, self.transform = sheet, translations, transform
        self.generator = XMLGenerator(output, encoding="utf-8", short_empty_elements=True) if output else None
        self.header_map = header_map or {}
        self.skip = 0
        self.capture = None
        self.buffer: list[str] = []
        self.cell = None
        self.row = 0
        self.headers: dict[str, str] = {}
        self.stats = Counter()
        self.row_heights = Counter()
        self.hashes = {key: hashlib.sha256() for key in ["rows", "cells", "numeric_boolean_null", "text", "formulas"]}
        self.cjk = []

    def startDocument(self) -> None:
        if self.generator:
            self.generator.startDocument()

    def endDocument(self) -> None:
        if self.generator:
            self.generator.endDocument()

    def startElement(self, name, attributes) -> None:
        tag = local(name)
        if self.skip:
            self.skip += 1
            return
        if self.transform and tag in {"conditionalFormatting", "tabColor"}:
            self.skip = 1
            self.stats["removed_" + tag] += 1
            return
        attrs = dict(attributes.items())
        if tag == "row":
            self.row = int(attrs["r"])
            self.stats["rows"] += 1
            digest_record(self.hashes["rows"], attrs["r"])
            if self.transform:
                attrs.update(ht="48" if is_header(self.sheet, self.row) else "20", customHeight="1")
            self.row_heights[attrs.get("ht", "default")] += 1
        elif tag == "c":
            if attrs.get("t") == "s":
                raise ValueError("Shared-string cell encountered; original capacity fallback uses str/inlineStr")
            self.cell = {"r": attrs["r"], "t": attrs.get("t"), "value": None,
                         "value_present": False, "text": [], "formula": None}
            if self.transform:
                old_style = int(attrs.get("s", "0"))
                attrs["s"] = str(self.header_map.get(old_style, old_style) if is_header(self.sheet, self.row) else old_style)
        elif tag in {"v", "t", "f"} and self.cell is not None:
            self.capture, self.buffer = tag, []
        if self.transform:
            if tag == "sheetView":
                attrs["showGridLines"] = "1"
            elif tag == "sheetFormatPr":
                attrs["defaultRowHeight"] = "20"
        if self.generator:
            self.generator.startElement(name, AttributesImpl(attrs))

    def characters(self, content) -> None:
        if self.skip:
            return
        if self.capture is not None:
            self.buffer.append(content)
        elif self.generator:
            self.generator.characters(content)

    def endElement(self, name) -> None:
        tag = local(name)
        if self.skip:
            self.skip -= 1
            return
        if self.capture == tag:
            value = "".join(self.buffer)
            coordinate = self.cell["r"]
            column = re.match(r"[A-Z]+", coordinate).group()
            if tag == "f":
                if self.transform:
                    value = self.translations.formula(value)
                self.cell["formula"] = value
            elif tag == "t" or (tag == "v" and self.cell["t"] == "str"):
                if self.row == 1:
                    self.headers[column] = value
                if self.transform:
                    value = self.translations.text(value, self.sheet, coordinate, self.headers.get(column))
                self.cell["text"].append(value)
            else:
                self.cell["value"], self.cell["value_present"] = value, True
            if self.generator:
                self.generator.characters(value)
            self.capture, self.buffer = None, []
        if tag == "c":
            cell = self.cell
            ident = [cell["r"], cell["t"]]
            self.stats["cells"] += 1
            digest_record(self.hashes["cells"], ident)
            if cell["t"] in {"str", "inlineStr"}:
                value = "".join(cell["text"])
                digest_record(self.hashes["text"], ident + [value])
                if CJK.search(value):
                    column = re.match(r"[A-Z]+", cell["r"]).group()
                    protected = (self.row != 1 and self.headers.get(column) in self.translations.technical_headers) or literal_identifier(value)
                    self.cjk.append({"sheet": SHEET_NAMES[self.sheet], "cell": cell["r"],
                                     "value": value, "allowed_source_identifier": protected})
            else:
                digest_record(self.hashes["numeric_boolean_null"], ident + [cell["value_present"], cell["value"]])
            if cell["formula"] is not None:
                digest_record(self.hashes["formulas"], [cell["r"], cell["formula"]])
                self.stats["formulas"] += 1
            self.cell = None
        if self.generator:
            self.generator.endElement(name)

    def report(self) -> dict:
        return {"rows": self.stats["rows"], "cells": self.stats["cells"],
                "formulas": self.stats["formulas"], "row_heights": dict(self.row_heights),
                "hashes": {key: value.hexdigest() for key, value in self.hashes.items()},
                "cjk_remaining": self.cjk, "headers": self.headers}


def parse_sheet(stream, handler: SheetStream) -> dict:
    parser = xml.sax.make_parser()
    for feature in [feature_external_ges, feature_external_pes]:
        try:
            parser.setFeature(feature, False)
        except xml.sax.SAXNotSupportedException:
            pass
    parser.setContentHandler(handler)
    parser.parse(stream)
    return handler.report()


def misc_xml(xml: bytes, translations: Translations) -> bytes:
    root = ET.fromstring(xml)
    changed = False
    for node in root.iter():
        if node.text:
            target = translations.by_text.get(node.text, node.text)
            if target != node.text:
                node.text, changed = target, True
    return serialize(root) if changed else xml


def verify(source: Path, output: Path, translations: Translations, report_path: Path) -> dict:
    reports, failures, exceptions = [], [], []
    sheet_headers = {}
    with zipfile.ZipFile(source) as old, zipfile.ZipFile(output) as new:
        before, after = sheet_parts(old), sheet_parts(new)
        if [(SHEET_NAMES[name], part) for name, part in before] != after:
            raise ValueError("Sheet names/order/parts changed beyond the approved mapping")
        for (name, part), (english, _) in zip(before, after, strict=True):
            with old.open(part) as stream:
                expected = parse_sheet(stream, SheetStream(name, translations, True))
            with new.open(part) as stream:
                actual = parse_sheet(stream, SheetStream(name, translations, False))
            sheet_headers[name] = actual["headers"]
            for key in ["rows", "cells", "formulas", "hashes"]:
                if expected[key] != actual[key]:
                    failures.append({"sheet": english, "check": key})
            if set(actual["row_heights"]) - {"20", "48"}:
                failures.append({"sheet": english, "check": "compact row heights", "actual": actual["row_heights"]})
            for item in actual["cjk_remaining"]:
                (exceptions if item["allowed_source_identifier"] else failures).append(item)
            reports.append({"sheet": english, "source_name": name, "rows": actual["rows"],
                            "cells": actual["cells"], "formulas": actual["formulas"],
                            "row_heights": actual["row_heights"], "semantic_hashes_match": expected["hashes"] == actual["hashes"]})
            print(f"Verified {english}: {actual['rows']} rows / {actual['cells']} cells", flush=True)
        # Preserve all native table columns and refs; translated headers must match the worksheet row 1.
        headers_by_part = {}
        for name, part in before:
            rel_part = posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")
            if rel_part not in new.namelist():
                continue
            rels = ET.fromstring(new.read(rel_part))
            for rel in rels:
                if rel.attrib.get("Type", "").endswith("/table"):
                    headers_by_part[part_target(part, rel.attrib["Target"])] = name
        for table_part, sheet_name in headers_by_part.items():
            a, b = ET.fromstring(old.read(table_part)), ET.fromstring(new.read(table_part))
            if a.attrib.get("ref") != b.attrib.get("ref"):
                failures.append({"part": table_part, "check": "table range"})
            original_columns = [node for node in a.iter() if local(node.tag) == "tableColumn"]
            actual_columns = [node for node in b.iter() if local(node.tag) == "tableColumn"]
            expected_names = [translations.by_text.get(node.attrib["name"], node.attrib["name"]) for node in original_columns]
            actual_names = [node.attrib["name"] for node in actual_columns]
            if expected_names != actual_names or len(actual_names) != len({s.casefold() for s in actual_names}):
                failures.append({"part": table_part, "check": "translated table columns"})
            row_headers = list(sheet_headers[sheet_name].values())
            if row_headers != actual_names:
                failures.append({"part": table_part, "check": "table columns differ from worksheet row 1"})
            info = next((n for n in b if local(n.tag) == "tableStyleInfo"), None)
            if info is None or info.attrib.get("name") != "TableStyleLight1" or any(
                info.attrib.get(key) != "0" for key in ["showRowStripes", "showColumnStripes"]
            ):
                failures.append({"part": table_part, "check": "plain table style"})
        styles = ET.fromstring(new.read("xl/styles.xml"))
        fonts = next(n for n in styles if local(n.tag) == "fonts")
        for font in fonts:
            properties = {local(n.tag): n.attrib for n in font}
            if properties.get("name", {}).get("val") != "Arial" or properties.get("sz", {}).get("val") != "11" or properties.get("color", {}).get("rgb") != "FF000000":
                failures.append({"check": "black Arial 11 font"})
        fills = next(n for n in styles if local(n.tag) == "fills")
        xfs = next(n for n in styles if local(n.tag) == "cellXfs")
        for xf in xfs:
            fill = fills[int(xf.attrib.get("fillId", "0"))]
            foreground = next((n for n in fill.iter() if local(n.tag) == "fgColor"), None)
            if foreground is None or foreground.attrib.get("rgb") != "FFFFFFFF":
                failures.append({"check": "explicit white active cell fill"})
    result = {"checked_taipei": datetime.now(ZoneInfo("Asia/Taipei")).isoformat(),
              "status": "PASS" if not failures else "FAIL", "source": str(source), "output": str(output),
              "source_sha256": sha256(source), "output_sha256": sha256(output),
              "sheets": reports, "sheet_count": len(reports),
              "all_numeric_boolean_null_and_types_preserved": not any(f.get("check") in {"cells", "hashes"} for f in failures),
              "all_untranslated_English_date_clock_strings_preserved": not any(f.get("check") == "hashes" for f in failures),
              "authorized_overrides": [{"source_sheet": s, "cell": c, "english": v} for (s, c), v in OVERRIDES.items()],
              "cjk_source_identifier_exceptions": exceptions, "failures": failures,
              "capacity_fallback": "Streaming edit of Artifact Tool-authored existing workbook; full object-model export exceeded 4GB Node heap"}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    if failures:
        raise ValueError(f"Plain English verification failed; see {report_path} ({len(failures)} checks)")
    return result


def apply(source: Path, output: Path, translations: Translations, report_path: Path) -> dict:
    source_hash = sha256(source)
    if source_hash != translations.source["source_sha256"]:
        raise ValueError("Backup hash differs from the source-string inventory")
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix="plain_english_", suffix=".xlsx.tmp", dir=output.parent)
    os.close(descriptor)
    temporary = Path(temp_name)
    try:
        with zipfile.ZipFile(source) as old, zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED,
                                                         compresslevel=6, allowZip64=True) as new:
            parts = sheet_parts(old)
            if [name for name, _ in parts] != list(SHEET_NAMES):
                raise ValueError("Original 24-sheet order differs from the approved inventory")
            part_names = {part: name for name, part in parts}
            styles, header_map, _ = plain_styles(old.read("xl/styles.xml"))
            new.comment = old.comment
            for info in old.infolist():
                metadata = copy.copy(info)
                if info.filename in part_names:
                    name = part_names[info.filename]
                    with old.open(info) as src, new.open(metadata, "w", force_zip64=True) as dst:
                        parse_sheet(src, SheetStream(name, translations, True, dst, header_map))
                    print(f"Edited {SHEET_NAMES[name]}", flush=True)
                elif info.filename == "xl/styles.xml":
                    new.writestr(metadata, styles)
                elif info.filename == "xl/workbook.xml":
                    new.writestr(metadata, workbook_xml(old.read(info), translations))
                elif info.filename.startswith("xl/tables/") and info.filename.endswith(".xml"):
                    new.writestr(metadata, table_xml(old.read(info), translations))
                elif info.filename.startswith("docProps/") and info.filename.endswith(".xml"):
                    new.writestr(metadata, misc_xml(old.read(info), translations))
                else:
                    with old.open(info) as src, new.open(metadata, "w", force_zip64=True) as dst:
                        shutil.copyfileobj(src, dst, length=1024 * 1024)
        with zipfile.ZipFile(temporary) as check:
            if check.testzip():
                raise ValueError("Output ZIP CRC test failed")
        result = verify(source, temporary, translations, report_path)
        os.replace(temporary, output)
        result["output"] = str(output)
        result["atomic_replace"] = True
        report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        return result
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--apply", action="store_true")
    modes.add_argument("--verify", action="store_true")
    parser.add_argument("--source", type=Path, default=REVIEW / "original_workbook.xlsx.bak")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx")
    parser.add_argument("--source-strings", type=Path, default=REVIEW / "source_strings.json")
    parser.add_argument("--translations", type=Path, default=REVIEW / "translations_merged.json")
    parser.add_argument("--report", type=Path, default=REVIEW / "verification.json")
    args = parser.parse_args()
    translations = Translations(args.source_strings, args.translations)
    if args.source.resolve() == args.output.resolve():
        raise ValueError("The authoritative backup cannot be overwritten")
    result = (apply if args.apply else verify)(args.source, args.output, translations, args.report)
    print(json.dumps({"status": result["status"], "sheets": result["sheet_count"],
                      "output": result["output"], "exceptions": len(result["cjk_source_identifier_exceptions"]),
                      "report": str(args.report)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

"""Prepare and safely merge the final research update into the archival workbook.

The original 4M-cell workbook exceeded Artifact Tool's 4 GiB export heap.
New worksheets are authored with Artifact Tool; this capacity fallback copies
all existing worksheet XML bytes intact, retaining raw records and native parts.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import posixpath
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/consolidated"
REVIEW = OUT / "review/main_v3"
SUPPORT = OUT / "support"
EH = ROOT / "outputs/research/elephant_head_final"
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
N = {"x": NS}
ET.register_namespace("x", NS)
ET.register_namespace("r", REL)
VERSION = "MR-20261114-v3-final"
BASE_SHA = "a789fcdc9c0a7e780f85b63687ad54f05b87cd6e341ecf024375dcd6fcb3f731"
BACKUP = OUT / "backups/All_Data_before_MR_v3_a789fcdc9c0a.xlsx.bak"
FINAL = OUT / "NASA_Space_Apps_2026_All_Data.xlsx"
CJK = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def table(name, headers, rows, widths=None, notes=None):
    return {"name": name, "headers": headers, "rows": rows,
            "widths": widths or [max(18, min(42, len(h)+3)) for h in headers],
            "notes": notes or []}


def prepare():
    if sha(BACKUP) != BASE_SHA:
        raise ValueError("Archival backup hash changed")
    evidence = json.loads((OUT / "research_main_20261114/evidence.json").read_text())
    qa = json.loads((EH / "qa.json").read_text())
    records = read_csv(EH / "elephant_head_records.csv")
    dictionary = read_csv(EH / "data_dictionary.csv")
    requirements = read_csv(ROOT / "docs/research/main_research_requirements.csv")
    tables = []
    overview_rows = [
        ["Version", VERSION, "2026-11-14", "Earth-Mars research. Four themes retained."],
        ["Main case", "I-02 / EARTH-002", "Elephant Head", "Priority archival method reference, not a similarity winner."],
        ["Comparison", "I-01 / EARTH-UV-001", "University Valley W", "Known-use reference. No new field plot established."],
        ["Backup", "EARTH-003", "Linnaeus Terrace", "Not activated. Historical 25/45 cm claims remain unresolved."],
        ["Other Mars references", "D-03 / D-04", "Context only", "No new Earth pairing or purpose reassignment."],
        ["Current question", "Describe common valid EH observations at 3 and 49 cm.", "Source time axis", "Source, depths, units and missingness checked before summaries."],
        ["Interpretation", "Descriptive archival evidence", "No causal experiment", "No blind accuracy, ice-loss or Mars performance result."],
        ["Novelty", "Not demonstrated", "Scoped review", "No first, new, under-studied or novelty-cleared site claim."],
        ["Candidate temperature", None, "I-01 / I-02", "Qualified local surface-temperature series not obtained."],
        ["Candidate ice depth", None, "I-01 / I-02", "SWIM consistency is not ice depth or ice fraction."],
        ["Scores", "Experimental descriptors only", "Historical values retained", "No confidence, landing approval or re-ranking."],
        ["EH records", len(records), "Original printed records", "Full page/row lineage and missing values retained."],
        ["MEDA records retained", 159418, "Historical raw observations", "GROUND_TEMP is brightness temperature (K), not air temperature."],
        ["Archive snapshot", "2026-11-14 16:36 Asia/Taipei", BASE_SHA[:16], "All 24 original worksheets retained. Original Overview renamed Archive Overview."],
        ["Historical Earth rankings", "Retired, not current selections", "Archive worksheets", "Earth Candidates, Terrain Windows/Ranks and Shortlist are historical only."],
        ["Temperature context", "Historical / separate spatial support", "Archive worksheets", "Other Mars regions and rover records do not fill I-01/I-02 gaps."],
        ["Reading long descriptions", "Select the cell and read the formula bar.", "Compact rows", "No observations were removed to reduce row height."],
    ]
    new_roles = [
        ["Overview", "Current scope and navigation", "Current", "MR-v3-final"],
        ["Mars Research Cards", "Two candidate cards and explicit nulls", "Current", "I-02 main / I-01 comparison"],
        ["Earth Research Roles", "Three archival site roles", "Current", "EH main / UV reference / LT inactive"],
        ["Sources and Novelty", "Product scope and known-use status", "Current", "No novelty clearance"],
        ["EH Summary", "Accepted archival counts and summaries", "Current", "Source printed-time axis"],
        ["EH Records", "Full row-level publisher-table transcription", "Current source export", "Not sensor recalibration"],
        ["EH Dictionary", "Column meanings, units and missingness", "Current source metadata", "Original clocks retained"],
        ["Current Requirements", "27 stable requirements and final disposition", "Current scope / historical request", "Thresholds remain undefined"],
    ]
    old = json.loads((REVIEW / "before_inventory.json").read_text())["sheets"]
    for entry in old:
        name = "Archive Overview" if entry["name"] == "Overview" else entry["name"]
        role = "Historical source snapshot"
        if name in {"Earth Candidates", "Earth Terrain Windows", "Earth Terrain Ranks", "Earth Shortlist CSV"}:
            role = "Historical / retired ranking. Not current selection"
        if name == "MEDA Raw Records":
            role = "Historical raw temperature records, all 159418 retained"
        if name in {"File Index", "Source Crosswalk", "JSON Source Records", "Report Text"}:
            role = "Historical source index/archive. Original cells retained"
        new_roles.append([name, role, "Unchanged archival cells", "Source snapshot 16:36, not refreshed"])
    tables.append(table("Overview", ["Item", "Value", "Period or support", "Scope"], overview_rows + [[None]*4] + [["Worksheet", "Role", "Status", "Scope"]] + new_roles, [31, 68, 45, 85]))

    cards = []
    cands = {c["id"]: c for c in evidence["candidates"]}
    fields = [
        ("Role", "Main case", "Comparison / known-use reference", "", "Current scope"),
        ("Earth research reference", "EARTH-002 Elephant Head", "EARTH-UV-001 University Valley W", "", "Research correspondence, not quantitative equivalence"),
        ("Latitude", cands["I-02"]["center_lat_lon"][0], cands["I-01"]["center_lat_lon"][0], "degree north", "Mars Discovery!E3 / E2"),
        ("East longitude", cands["I-02"]["center_lat_lon"][1], cands["I-01"]["center_lat_lon"][1], "degree east", "Mars Discovery!F3 / F2"),
        ("Nominal latitude bounds", "53.50 to 54.00", "54.00 to 54.50", "degree north", "0.5 degree screening cell, not a drill site"),
        ("Nominal longitude bounds", "42.00 to 42.50", "1.00 to 1.50", "degree east", "Actual product footprints differ"),
    ]
    metrics = [("Regional mean slope", "slope", "degree", "H"), ("Cell relief", "relief", "m", "I"),
               ("TES thermal inertia", "thermal_inertia", "J m-2 K-1 s-0.5", "J"),
               ("Shallow-ice consistency", "ice_shallow", "unitless, -1 to 1", "K"),
               ("MY35 annual CDOD", "dust_cdod", "unitless, 9.3 um absorption", "L")]
    for label, key, unit, col in metrics:
        fields.append((label, cands["I-02"]["stored_layers"][key], cands["I-01"]["stored_layers"][key], unit, f"Mars Discovery!{col}3 / {col}2"))
    for label, key, unit in [("Candidate surface temperature", "candidate_temperature", "not available"), ("Candidate ice depth", "candidate_ice_depth", "not available"), ("Candidate ice content", "candidate_ice_content", "not available")]:
        fields.append((label, cands["I-02"].get(key), cands["I-01"].get(key), unit, "Null retained. No replacement from other regions or Earth."))
    fields += [
        ("Known feature", "Lower TES thermal inertia than I-01", "Higher TES thermal inertia than I-02", "Descriptive comparison", "Similar regional slope and SWIM indicators"),
        ("Unverified hypothesis", "Cover, material or ice may affect the signal.", "Cover, material or ice may affect the signal.", "Unverified", "No controlled causal separation or ice inversion"),
        ("Research question", "What can valid EH 3/49 cm records describe?", "Which probe requirements follow from the existing layers?", "Archival / planning", "No direct calibration of Mars TES with ground temperatures"),
        ("Reason", "Existing EH source table and prior QA can be reused.", "Provides a second longitude sector and known-use reference.", "Evidence availability", "Not a similarity optimum"),
        ("Same-place same-purpose review", "insufficient_data", "insufficient_data", "Scoped search", "Sources and Novelty. Not novelty-cleared."),
        ("Required new evidence", "Independent local ice and material constraints", "Independent local ice and material constraints", "Future", "Qualified temperature, footprint, uncertainty and local hazards"),
        ("Must not claim", "More ice, easier drilling or safe landing", "Confirmed mineable ice or safe landing", "Prohibited inference", "No first/new/under-studied or validated-analog claim"),
        ("Measurement uncertainty", None, None, "not provided", "Pixel standard deviations are not confidence intervals."),
        ("Grid sample caveat", "MOLA64 / TES96 of100 / SWIM100", "MOLA64 / TES93 of100 / SWIM100", "Product pixels", "Not independent observations. Ice Candidate QA rows3 /2"),
    ]
    cards.extend([list(x) for x in fields])
    tables.append(table("Mars Research Cards", ["Field", "I-02", "I-01", "Unit or status", "Evidence / limit"], cards, [35, 64, 64, 38, 80]))

    earth = []
    pair = {p["earth_candidate_id"]: p for p in evidence["earth_pairings"]}
    for key, name, role, purpose, limit in [
        ("EARTH-002", "Elephant Head", "Main archival method reference", "Describe same-row 3/49 cm thermal observations.", "Historical49 cm interface, not current truth. No ice-depth inversion."),
        ("EARTH-UV-001", "University Valley W", "Known-use reference / comparison", "Use known station and sampling precedent with its scope.", "Historical42 cm interface. W-vicinity new plot undefined."),
        ("EARTH-003", "Linnaeus Terrace", "Inactive archival backup", "Retain source/depth discrepancy as an explicit limit.", "25/45 cm claims unresolved. Adopted interface truth is null."),
    ]:
        p = pair[key]
        rows = [("Site", name), ("Role", role), ("Mars research correspondence", p["mars_candidate_id"]),
                ("Latitude (degree north)", p["anchor_lat_lon"][0]), ("Longitude (degree east)", p["anchor_lat_lon"][1]),
                ("Purpose", purpose), ("Historical station interface (cm)", p.get("historical_station_interface_cm")),
                ("Current interface truth (cm)", None), ("New plot footprint", None),
                ("Known-use status", p.get("team2_component_status", p.get("team2_site_level_same_use_status"))),
                ("Complete protocol / exact new footprint", "insufficient_data"), ("Novelty cleared", False),
                ("Key limit", limit)]
        for field, value in rows:
            earth.append([key, field, value, "Point anchor only, not an approved experimental area."])
    tables.append(table("Earth Research Roles", ["Earth ID", "Field", "Value", "Spatial / interpretation limit"], earth, [23, 43, 82, 78]))

    sources = [
        ["MOLA", "Regional terrain", "1997-09-15 to 2001-06-30", "Created2003-04-03", "16 pixels/degree", "m / degree", "Regional support only", "data-supported", "outputs/mars_profiles/profiles.json"],
        ["TES", "Nighttime thermal inertia", "Observation start/end N/A", "Created2007-01-30", "20 pixels/degree", "J m-2 K-1 s-0.5", "Not surface temperature, hardness or direct ice evidence", "data-supported", "outputs/mars_profiles/profiles.json"],
        ["SWIM2.0 shallow", "Composite ice consistency", "Multiple inputs; no single observation period", "Page updated2021-02-24", "Projected grid spacing2964.119 m", "unitless", "10x10 coarsening then0.5degree interpolation; not ice fraction/depth", "data-supported", "outputs/mars_profiles/profiles.json"],
        ["MY35 CDOD", "Annual column dust context", "Mars Year35", "Created2021-11-25", "Native reconstructed3degree", "unitless,9.3um absorption", "Not local deposition/abrasion or550nm Earth AOD", "data-supported", "outputs/mars_profiles/profiles.json"],
        ["I-01 / I-02", "Exact same-place same-purpose review", "Team2 scoped review", "No new search this round", "Nominal0.5degree cells", "not applicable", "Catalog non-overlap does not exclude every proposal", "insufficient_data", "outputs/consolidated/research_main_20261114/evidence.json"],
        ["University Valley", "Known-use station / method reference", "Published historical studies", "Inherited scoped evidence", "Point anchor, new footprint unknown", "not applicable", "Same-use precedent exists; no new/under-studied claim", "same_use_exists", "docs/research/main_mars_research_cards.md"],
        ["Elephant Head", "Archival thermal records / method precedent", "2017-2018 records;2020 nearby sampling", "New row export from existing parser", "Station vs nearbySite3 kept separate", "degreeC / RHpercent / cm", "10cm dry-soil spoon increments are not controlled10cm ice drilling", "related_research_exists", "outputs/research/elephant_head_final/README.md"],
        ["Linnaeus Terrace", "Inactive backup / depth source trace", "Historical25cm and45cm source claims", "No additional search", "Anchor only", "cm", "No adopted interface depth; no subsurfaceRH substitute", "insufficient_data", "docs/research/main_project_synthesis.md"],
    ]
    tables.append(table("Sources and Novelty", ["Source / site", "Quantity or use", "Observation period", "Publication / processing date", "Spatial support", "Unit", "Limit", "Scoped status", "Source file"], sources, [25, 44, 47, 40, 45, 36, 93, 30, 76]))

    # QA is delivered by the extractor. Flatten its actual values, without
    # substituting inherited estimates or inventing statistics.
    flat = []
    def flatten(value, pointer=""):
        if isinstance(value, dict) and value:
            for key, item in value.items():
                flatten(item, pointer + "/" + str(key).replace("~", "~0").replace("/", "~1"))
        elif isinstance(value, list) and value:
            for index, item in enumerate(value):
                flatten(item, pointer + "/" + str(index))
        else:
            flat.append([pointer or "/", json.dumps(value) if isinstance(value, (dict, list)) else value, "outputs/research/elephant_head_final/qa.json"])
    flatten(qa)
    summary_rows = [
        ["Scope", "Publisher-table recovery and descriptive statistics", "No sensor recalibration or causal test"],
        ["Clock", "Original printed axes retained", "No UTC/solar-time conversion"],
        ["Temperature", "Air /3cm /49cm in degreeC", "3cm subsurface temperature is not LST"],
        ["Missingness", "Source blanks retained", "No zero fill, interpolation or annual3cm mean"],
        ["Humidity", "Raw/corrected values kept separate", "Values above100 retained and flagged, not clipped"],
        ["Interpretation", "Paired-depth observations", "No unique ice-depth/TI inversion or ice-loss result"],
        ["Summer temperatures figure", "outputs/research/elephant_head_final/summer_temperatures.png", "Repository index. Link valid after final main delivery."],
        ["Temperature difference figure", "outputs/research/elephant_head_final/summer_temperature_difference.png", "Same-row pairing. See actual QA period and N below."],
    ] + flat
    tables.append(table("EH Summary", ["Quantity / JSON pointer", "Actual value", "Source or limit"], summary_rows, [68, 88, 93]))

    # Preserve all CSV columns and all observed values. The extractor's dictionary
    # decides numeric typing; timestamps/IDs retain their literal text.
    headers = list(records[0])
    numeric = set()
    for row in dictionary:
        key = row.get("column") or row.get("field") or row.get("column_name") or row.get("name")
        dtype = " ".join(str(v) for k, v in row.items() if "type" in k.lower()).lower()
        if key and any(t in dtype for t in ["float", "integer", "number", "numeric"]):
            numeric.add(key)
    for key in headers:
        if key in {"source_page", "source_row", "row_id", "record_id", "record_number", "source_row_on_page", "source_extracted_line_on_page", "source_numeric_count", "ice49_depth_cm", "soil3_depth_cm"}:
            numeric.add(key)
        if re.search(r"(?:temp|temperature|rh|humidity).*?(?:_c|_pct|_percent|_raw|_corrected)$", key.lower()) and not re.search(r"flag|missing|above|time|label", key.lower()):
            numeric.add(key)
    def scalar(key, value):
        if value == "":
            return None
        if key in numeric:
            number = float(value)
            return int(number) if number.is_integer() and abs(number) < 2**53 else number
        if value in {"True", "False", "true", "false"}:
            return value.lower() == "true"
        return value
    rows = [[scalar(k, r[k]) for k in headers] for r in records]
    tables.append(table("EH Records", headers, rows, [max(18, min(40, len(k)+3)) for k in headers]))
    tables.append(table("EH Dictionary", list(dictionary[0]), [list(r.values()) for r in dictionary], [38] * len(dictionary[0])))
    reqkeys = ["version", "requirement_id", "mars_candidate_ids", "earth_candidate_id", "requirement_en", "execution_category", "final_disposition", "current_status", "unit", "threshold_value", "threshold_status", "current_qa_rule", "requirement_history_ref", "final_evidence"]
    reqrows = [[r.get(k) or None for k in reqkeys] for r in requirements]
    for row in reqrows:
        for index, value in enumerate(row):
            if isinstance(value, str) and CJK.search(value):
                # Preserve source paths where exact. Do not silently translate
                # arbitrary text or expose internal Chinese notes.
                raise ValueError(f"English requirements field has CJK: {reqkeys[index]}")
    tables.append(table("Current Requirements", ["Version", "Requirement ID", "Mars IDs", "Earth ID", "Historical request (English)", "Execution category (v2 history)", "Final disposition", "Current source status", "Unit", "Threshold value", "Threshold status", "QA rule", "Requirement history", "Final evidence"], reqrows, [30, 21, 24, 24, 94, 34, 42, 64, 30, 22, 25, 110, 90, 100]))
    sources_paths = [
        "docs/research/main_mars_research_cards.md", "docs/research/main_project_synthesis.md", "docs/research/main_research_requirements.csv",
        "outputs/consolidated/research_main_20261114/evidence.json",
    ] + [str(p.relative_to(ROOT)) for p in sorted(EH.iterdir()) if p.is_file()]
    manifest = [{"path": p, "bytes": (ROOT / p).stat().st_size, "sha256": sha(ROOT / p)} for p in sources_paths]
    write_json(SUPPORT / "main_v3_data.json", {"version": VERSION, "tables": tables, "source_manifest": manifest, "EH_numeric_columns": sorted(numeric)})
    write_json(REVIEW / "source_mapping.json", {"version": VERSION, "archival_backup_sha256": BASE_SHA, "sources": manifest, "new_sheets": [{"name": t["name"], "rows": len(t["rows"]), "columns": len(t["headers"])} for t in tables]})
    print(json.dumps({"tables": [{"name": t["name"], "rows": len(t["rows"]), "cols": len(t["headers"])} for t in tables], "numeric": sorted(numeric)}, indent=2))


def xmlbytes(root):
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def sheet_parts(z):
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    targets = {r.get("Id"): r.get("Target") for r in rels}
    parts = []
    for s in wb.find(f"{{{NS}}}sheets"):
        target = targets[s.get(f"{{{REL}}}id")]
        part = target.lstrip("/") if target.startswith("/") else posixpath.normpath("xl/" + target)
        parts.append((s.get("name"), part, s))
    return wb, rels, parts


def merge():
    donor = SUPPORT / "main_v3_new_sheets.xlsx"
    if sha(BACKUP) != BASE_SHA:
        raise ValueError("Archival source changed")
    with zipfile.ZipFile(BACKUP) as base, zipfile.ZipFile(donor) as new:
        wb, rels, old_sheets = sheet_parts(base)
        _, _, new_sheets = sheet_parts(new)
        style = ET.fromstring(base.read("xl/styles.xml"))
        ds = ET.fromstring(new.read("xl/styles.xml"))
        num_map = {}
        nf = style.find(f"{{{NS}}}numFmts")
        if nf is None:
            nf = ET.Element(f"{{{NS}}}numFmts", {"count": "0"})
            style.insert(0, nf)
        bycode = {e.get("formatCode"): int(e.get("numFmtId")) for e in nf}
        nextnum = max([163] + list(bycode.values())) + 1
        dnf = ds.find(f"{{{NS}}}numFmts")
        for elem in [] if dnf is None else dnf:
            old_id = int(elem.get("numFmtId"))
            code = elem.get("formatCode")
            if code not in bycode:
                bycode[code] = nextnum
                nextnum += 1
                copied = copy.deepcopy(elem)
                copied.set("numFmtId", str(bycode[code]))
                nf.append(copied)
            num_map[old_id] = bycode[code]
        nf.set("count", str(len(nf)))
        offsets = {}
        for section in ["fonts", "fills", "borders", "cellStyleXfs", "cellXfs", "dxfs"]:
            src = ds.find(f"{{{NS}}}{section}")
            dst = style.find(f"{{{NS}}}{section}")
            if src is None or len(src) == 0:
                offsets[section] = len(dst) if dst is not None else 0
                continue
            if dst is None:
                raise ValueError(f"Existing styles missing supported section {section}")
            offsets[section] = len(dst)
            for elem in src:
                elem = copy.deepcopy(elem)
                if section in {"cellStyleXfs", "cellXfs"}:
                    for attr, component in [("fontId", "fonts"), ("fillId", "fills"), ("borderId", "borders")]:
                        if attr in elem.attrib:
                            elem.set(attr, str(int(elem.get(attr)) + offsets[component]))
                    if "numFmtId" in elem.attrib:
                        value = int(elem.get("numFmtId"))
                        elem.set("numFmtId", str(num_map.get(value, value)))
                    if "xfId" in elem.attrib:
                        elem.set("xfId", str(int(elem.get("xfId")) + offsets["cellStyleXfs"]))
                dst.append(elem)
            dst.set("count", str(len(dst)))
        # The fixed archival hash still contains the four previously diagnosed
        # invalid extLst/alignment orders. Repair only child order, preserving
        # every style property and every original worksheet byte.
        schema_repairs = []
        for section in ["cellStyleXfs", "cellXfs"]:
            for index, xf in enumerate(style.find(f"{{{NS}}}{section}")):
                order = [{"alignment": 1, "protection": 2, "extLst": 3}.get(x.tag.split("}")[-1], 0) for x in xf]
                if order != sorted(order):
                    children = list(xf)
                    for child in children:
                        xf.remove(child)
                    for child in sorted(children, key=lambda x: {"alignment": 1, "protection": 2, "extLst": 3}.get(x.tag.split("}")[-1], 0)):
                        xf.append(child)
                    schema_repairs.append({"section": section, "index": index, "before": order, "after": sorted(order)})
        feature = "xl/featurePropertyBag/featurePropertyBag.xml"
        if feature in new.namelist() and new.read(feature) != base.read(feature):
            raise ValueError("New checkbox metadata differs; cannot reuse original feature bag")
        # Copy all new worksheet relationships recursively under a collision-free
        # prefix. Artifact Tool currently emits tables; no drawing is introduced.
        newparts = {}
        content = ET.fromstring(base.read("[Content_Types].xml"))
        donor_content = ET.fromstring(new.read("[Content_Types].xml"))
        donor_types = {c.get("PartName").lstrip("/"): c.get("ContentType") for c in donor_content if c.tag.endswith("Override")}
        copied_parts = {}
        old_table_ids = []
        for name in base.namelist():
            if name.startswith("xl/tables/") and name.endswith(".xml"):
                old_table_ids.append(int(ET.fromstring(base.read(name)).get("id", "0")))
        next_table_id = max(old_table_ids or [0]) + 1
        shared = []
        if "xl/sharedStrings.xml" in new.namelist():
            shared = ["".join(q.itertext()) for q in ET.fromstring(new.read("xl/sharedStrings.xml"))]

        def copy_part(part):
            nonlocal next_table_id
            if part in copied_parts:
                return copied_parts[part]
            directory, basename = posixpath.split(part)
            target = f"{directory}/mr_v3_{basename}"
            if target in base.namelist() or target in newparts:
                raise ValueError(f"Part collision {target}")
            copied_parts[part] = target
            root = ET.fromstring(new.read(part))
            if part.startswith("xl/worksheets/"):
                for cell in root.findall(".//x:sheetData/x:row/x:c", N):
                    if cell.get("s") is not None:
                        cell.set("s", str(int(cell.get("s")) + offsets["cellXfs"]))
                    if cell.get("t") == "s":
                        v = cell.find(f"{{{NS}}}v")
                        text = shared[int(v.text)]
                        cell.remove(v)
                        cell.set("t", "inlineStr")
                        t = ET.SubElement(ET.SubElement(cell, f"{{{NS}}}is"), f"{{{NS}}}t")
                        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                        t.text = text
                for elem in root.findall(".//x:row", N) + root.findall(".//x:col", N):
                    attr = "s" if elem.tag.endswith("row") else "style"
                    if elem.get(attr) is not None:
                        elem.set(attr, str(int(elem.get(attr)) + offsets["cellXfs"]))
            elif part.startswith("xl/tables/"):
                root.set("id", str(next_table_id))
                next_table_id += 1
                tsi = root.find(f"{{{NS}}}tableStyleInfo")
                if tsi is not None:
                    tsi.set("name", "TableStyleLight1")
                    tsi.set("showRowStripes", "0")
                    tsi.set("showColumnStripes", "0")
            relpart = f"{directory}/_rels/{basename}.rels"
            if relpart in new.namelist():
                rr = ET.fromstring(new.read(relpart))
                for rel in rr:
                    if rel.get("TargetMode") == "External":
                        continue
                    old_target = rel.get("Target")
                    resolved = old_target.lstrip("/") if old_target.startswith("/") else posixpath.normpath(posixpath.join(directory, old_target))
                    renamed = copy_part(resolved)
                    rel.set("Target", posixpath.relpath(renamed, directory))
                newparts[f"{directory}/_rels/mr_v3_{basename}.rels"] = xmlbytes(rr)
            newparts[target] = xmlbytes(root)
            if part in donor_types:
                ET.SubElement(content, f"{{{CT}}}Override", {"PartName": "/"+target, "ContentType": donor_types[part]})
            return target

        sheets = wb.find(f"{{{NS}}}sheets")
        old_elements = list(sheets)
        for elem in old_elements:
            sheets.remove(elem)
            if elem.get("name") == "Overview":
                elem.set("name", "Archive Overview")
        existing_ids = {r.get("Id") for r in rels}
        next_sheet_id = max(int(s.get("sheetId")) for s in old_elements) + 1
        for index, (name, part, _) in enumerate(new_sheets):
            relid = f"rIdMRv3_{index+1}"
            if relid in existing_ids:
                raise ValueError("Relationship ID collision")
            target = copy_part(part)
            ET.SubElement(rels, f"{{{PKG}}}Relationship", {"Id": relid, "Type": REL+"/worksheet", "Target": posixpath.relpath(target, "xl")})
            ET.SubElement(sheets, f"{{{NS}}}sheet", {"name": name, "sheetId": str(next_sheet_id+index), f"{{{REL}}}id": relid})
        for elem in old_elements:
            sheets.append(elem)
        for view in wb.findall("x:bookViews/x:workbookView", N):
            view.set("activeTab", "0")
            view.set("firstSheet", "0")
        # Existing localSheetIds shift with the eight prepended sheets.
        for defined in wb.findall("x:definedNames/x:definedName", N):
            if defined.get("localSheetId") is not None:
                defined.set("localSheetId", str(int(defined.get("localSheetId"))+len(new_sheets)))
            if defined.text:
                defined.text = defined.text.replace("'Overview'!", "'Archive Overview'!")
        calc = wb.find(f"{{{NS}}}calcPr")
        if calc is not None:
            calc.set("fullCalcOnLoad", "1")
            calc.set("forceFullCalc", "1")
        updates = {"xl/workbook.xml": xmlbytes(wb), "xl/_rels/workbook.xml.rels": xmlbytes(rels), "xl/styles.xml": xmlbytes(style), "[Content_Types].xml": xmlbytes(content)}
        temp = FINAL.with_suffix(".tmp.xlsx")
        with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as out:
            for info in base.infolist():
                out.writestr(info, updates.get(info.filename, base.read(info.filename)))
            for name, data in newparts.items():
                out.writestr(name, data)
        with zipfile.ZipFile(temp) as check:
            if check.testzip() is not None:
                raise ValueError("ZIP CRC failure")
        temp.replace(FINAL)
        write_json(REVIEW / "merge_manifest.json", {"version": VERSION, "method": "Artifact Tool authors new sheets; capacity-limited ZIP/XML merge retains original 4M-cell worksheets", "prior_capacity_evidence": "outputs/consolidated/review/export_notes.json", "archival_backup_sha256": BASE_SHA, "donor_sha256": sha(donor), "output_bytes": FINAL.stat().st_size, "output_sha256": sha(FINAL), "existing_worksheet_parts_copied_byte_identically": [p for _, p, _ in old_sheets], "old_overview_renamed_only": True, "new_sheets": [n for n, _, _ in new_sheets], "modified_package_parts": list(updates), "new_package_parts": list(newparts), "style_xf_order": "PASS", "archival_style_schema_repairs": schema_repairs, "checkbox_feature_bag": "byte-identical and reused"})
        print(json.dumps({"output": str(FINAL), "bytes": FINAL.stat().st_size, "sha256": sha(FINAL), "new_sheets": len(new_sheets)}))


def values(z, part):
    """Yield cell representation without loading the multi-million-cell raw sheet."""
    for _, cell in ET.iterparse(z.open(part), events=("end",)):
        if cell.tag == f"{{{NS}}}c":
            typ = cell.get("t", "n")
            v = cell.find(f"{{{NS}}}v")
            if typ == "inlineStr":
                value = "".join(cell.find(f"{{{NS}}}is").itertext())
            else:
                value = v.text if v is not None else None
            f = cell.find(f"{{{NS}}}f")
            yield cell.get("r"), typ, value, f.text if f is not None else None
            cell.clear()
        elif cell.tag == f"{{{NS}}}row":
            cell.clear()


def verify():
    bundle = json.loads((SUPPORT / "main_v3_data.json").read_text())
    result = {"version": VERSION, "output_sha256": sha(FINAL), "output_bytes": FINAL.stat().st_size, "preservation": [], "new_sheet_counts": [], "CJK": [], "formula_errors": [], "exceptions": []}
    with zipfile.ZipFile(BACKUP) as base, zipfile.ZipFile(FINAL) as final:
        _, _, olds = sheet_parts(base)
        _, _, allparts = sheet_parts(final)
        byname = {name: p for name, p, _ in allparts}
        for name, part, _ in olds:
            identical = hashlib.sha256(base.read(part)).digest() == hashlib.sha256(final.read(part)).digest()
            result["preservation"].append({"original_sheet": name, "part": part, "all_cells_and_native_parts_byte_identical": identical})
            if not identical:
                raise ValueError(f"Original worksheet modified: {name}")
        for tab in bundle["tables"]:
            part = byname[tab["name"]]
            got = {}
            for address, typ, value, formula in values(final, part):
                got[address] = (typ, value, formula)
            cols = len(tab["headers"])
            rows = len(tab["rows"])+1
            expected = [tab["headers"]] + tab["rows"]
            mismatches = []
            for ri, row in enumerate(expected, 1):
                for ci, exp in enumerate(row, 1):
                    col = ""
                    index = ci
                    while index:
                        index, rem = divmod(index-1, 26)
                        col = chr(65+rem)+col
                    addr = f"{col}{ri}"
                    typ, val, formula = got.get(addr, ("n", None, None))
                    if formula is not None:
                        continue
                    okay = (val is None) if exp is None else (typ == "b" and val == str(int(exp))) if isinstance(exp, bool) else (typ in {"n", ""} and val is not None and float(val) == exp) if isinstance(exp, (float, int)) else ((val or "") == str(exp) if typ in {"str", "inlineStr", "s"} else val == str(exp))
                    if not okay:
                        mismatches.append({"cell": addr, "expected": exp, "actual": [typ, val]})
            result["new_sheet_counts"].append({"sheet": tab["name"], "rows_including_header": rows, "columns": cols, "mismatches": mismatches[:20], "verified_expected_cells": rows*cols})
            if mismatches:
                raise ValueError(f"New sheet mismatches: {tab['name']} {mismatches[:3]}")
        # Scan all worksheet cell text, including historical archives. Exact paths
        # and JSON pointers may contain source-literal Chinese; never alter them.
        for name, part, _ in allparts:
            for address, typ, value, formula in values(final, part):
                if typ == "e":
                    result["formula_errors"].append({"sheet": name, "cell": address, "value": value})
                if value and CJK.search(value):
                    entry = {"sheet": name, "cell": address, "value": value[:500]}
                    if (value.startswith(("outputs/", "docs/", "data/", "/")) and not re.search(r"[\n；。]", value)):
                        result["exceptions"].append(entry)
                    else:
                        result["CJK"].append(entry)
        styles = ET.fromstring(final.read("xl/styles.xml"))
        badfonts = []
        for i, font in enumerate(styles.find(f"{{{NS}}}fonts")):
            color = font.find(f"{{{NS}}}color")
            if color is not None and color.get("rgb") not in {"FF000000", "000000", None}:
                badfonts.append(i)
        badfills = []
        for i, fill in enumerate(styles.find(f"{{{NS}}}fills")):
            for color in fill.findall(".//x:fgColor", N):
                if color.get("rgb") not in {"FFFFFFFF", "FFFFFF", None}:
                    badfills.append(i)
        result["nonblack_font_definitions"] = badfonts
        result["nonwhite_fill_definitions"] = badfills
        result["all_original_worksheet_cells_preserved"] = all(q["all_cells_and_native_parts_byte_identical"] for q in result["preservation"])
        result["sheet_count"] = len(allparts)
        result["status"] = "PASS" if not result["CJK"] and not result["formula_errors"] and not badfonts and not badfills else "REVIEW"
        write_json(REVIEW / "verification.json", result)
        print(json.dumps({k: v for k, v in result.items() if k not in {"preservation", "new_sheet_counts", "exceptions"}}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "merge", "verify"])
    args = parser.parse_args()
    {"prepare": prepare, "merge": merge, "verify": verify}[args.mode]()

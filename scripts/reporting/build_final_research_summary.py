#!/usr/bin/env python3
"""Build the English two-page final research summary from accepted EH exports.

Read-only inputs: project research cards, frozen teammate records, and the final
Elephant Head QA JSON. This script writes only the summary Markdown and PDF.
Run with the bundled Python that provides reportlab and pypdf.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from html import escape
from pathlib import Path

import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
VERSION = "MR-20261114-v3-final"
MD_PATH = ROOT / "docs/research/final_research_summary_en.md"
PDF_PATH = ROOT / "outputs/research/final_research_summary_en.pdf"
EXPORT_DIR = ROOT / "outputs/research/elephant_head_final"


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
        + ["| " + " | ".join(row) + " |" for row in rows]
    )


def make_content(summary: dict, accepted: bool) -> dict:
    required = [
        "records", "records_with_3cm", "last_3cm", "annual_n",
        "summer_paired_n", "annual_air_mean_C", "annual_ice49_mean_C",
        "summer_air_mean_C", "summer_ice49_mean_C", "summer_soil3_mean_C",
        "summer_soil3_minus_ice49_mean_C", "RH_ice49_corrected_above100_n",
        "first", "last", "second_timestamp_offset_minutes",
    ]
    missing = [key for key in required if key not in summary]
    if missing:
        raise ValueError(f"Final QA summary missing fields: {missing}")
    if not accepted:
        raise ValueError("Final independent export must be accepted before final publication")

    def num(key: str) -> str:
        return f"{int(summary[key]):,}"

    def temp(key: str) -> str:
        return f"{float(summary[key]):+.3f}"

    return {
        "title": "Mars ice investigation: what the evidence supports",
        "subtitle": f"Team zasa | 14 November 2026 (Asia/Taipei) | {VERSION}",
        "question": (
            "How can published Earth ice-interface records help define the additional "
            "observations needed to investigate Mars candidates I-01 and I-02? This "
            "delivery documents source and data QA, reproduces descriptive thermal "
            "results, and states the limits of those results. It does not validate "
            "a new ice-detection method or a Mars resource."
        ),
        "retain": (
            "Both Mars candidates are retained as conditional research cases: their "
            "regional mean slopes and SWIM shallow-ice consistency descriptors are "
            "close, while TES thermal inertia differs. I-01 is at 54.25 N, 1.25 E; "
            "I-02 is at 53.75 N, 42.25 E (planetocentric latitude, east-positive longitude). "
            "They are not controlled experimental replicates or extraction recommendations."
        ),
        "mars_headers": ["Mars descriptor", "I-01", "I-02"],
        "mars_rows": [
            ["Mean slope (degrees)", "0.302596", "0.305738"],
            ["Cell relief (m)", "76", "88"],
            ["TES thermal inertia", "244.709671", "160.666672"],
            ["SWIM shallow consistency", "0.354307", "0.355086"],
            ["MY35 mean dust CDOD", "0.106878", "0.112248"],
        ],
        "mars_note": (
            "Rounded descriptors from the existing Mars records [P1]. Thermal inertia "
            "is in J m^-2 K^-1 s^-0.5; SWIM and CDOD are dimensionless. SWIM values "
            "are not ice percentages or probabilities. Scores are not confidence or landing approval."
        ),
        "earth_headers": ["Fixed pairing and role", "What is supported"],
        "earth_rows": [
            [
                "EARTH-002 / I-02\nElephant Head: main archival case",
                "A published monitoring point with a historical 49 cm ice-cemented "
                "interface and an exportable hourly table. Selected for a tractable QA "
                "and reproduction task, not proven best physical equivalence to I-02.",
            ],
            [
                "EARTH-UV-001 / I-01\nUniversity Valley: known-use reference",
                "W station has a historical 42 cm interface. Valley-scale Mars-analog "
                "drilling, short sampling intervals and temperature control have precedents. "
                "Their exact overlap with a new W plot is unverified.",
            ],
            [
                "EARTH-003 / I-02\nLinnaeus Terrace: inactive backup",
                "Historical multi-depth temperature data exist. Conflicting 25 cm and "
                "45 cm interface citations remain unresolved; no single interface truth "
                "is adopted and no second analysis stream was activated.",
            ],
        ],
        "earth_note": (
            "All three are already studied sites. Their published point anchors are "
            "not approved new test plots, and their different years, materials and "
            "measurement supports do not establish a controlled cross-site comparison. [P2]"
        ),
        "data_title": "Elephant Head: observed data, bounded conclusions",
        "data_intro": (
            "Team2 supplied the existing parser and original full-table QA; this "
            "delivery reuses that method for export, reproduction and artifact checks. "
            f"The final delivery independently re-extracted the publisher's 108-page "
            f"supplement, checked its source hash, and exported {num('records')} records "
            f"with source-page/row provenance. The first printed timestamp spans "
            f"{summary['first']} to {summary['last']}. The two printed clocks are "
            f"{int(summary['second_timestamp_offset_minutes'])} minutes apart; their "
            "UTC/solar-time meaning is unresolved, so these are original-label windows. [P3, S1]"
        ),
        "stats_headers": ["Window / paired support", "Air (deg C)", "3 cm (deg C)", "49 cm (deg C)"],
        "stats_rows": [
            [f"Annual: N={num('annual_n')}", temp("annual_air_mean_C"), "Not computed", temp("annual_ice49_mean_C")],
            [f"Summer: N={num('summer_paired_n')}", temp("summer_air_mean_C"), temp("summer_soil3_mean_C"), temp("summer_ice49_mean_C")],
        ],
        "window_note": (
            "Annual: 2017-12-01 inclusive to 2018-12-01 exclusive. Summer: "
            "2017-12-01 inclusive to 2018-03-01 exclusive, using the first printed "
            f"timestamp. Summer 3 cm minus 49 cm mean difference: "
            f"{temp('summer_soil3_minus_ice49_mean_C')} deg C. N counts records, not independent samples."
        ),
        "data_limits": (
            f"The 3 cm channel has {num('records_with_3cm')} records and ends at "
            f"{summary['last_3cm']}; absent winter values remain missing. "
            f"The 49 cm corrected-RH column has {num('RH_ice49_corrected_above100_n')} "
            "values above 100%; values are retained and flagged, not clipped or treated "
            "as calibrated water activity. The 3 cm sensor measures subsurface temperature, "
            "not satellite land surface temperature. Reproduced means are not new field measurements."
        ),
        "cannot": (
            "These records cannot uniquely invert ice depth or TES thermal inertia, "
            "separate overburden causes from all confounders, validate blinded accuracy, "
            "or quantify drilling heating and sample ice loss. No new independent "
            "interface truth, material controls or initial/final ice mass were measured. "
            "Mars ice presence, depth, purity, continuity, quantity and extractability "
            "remain unconfirmed at I-01/I-02. Their nominal cells are about 30 x 17 km; "
            "dust retains native 3-degree reconstructed support, not local weather. "
            "TES thermal inertia is not temperature or hardness."
        ),
        "originality": (
            "Novel Earth sites, novel uses and a distinct scientific contribution have "
            "not been demonstrated. Prior work includes monitoring, ice stability, "
            "drilling/sampling components and cross-site mechanism comparisons. "
            "Non-overlap with inspected Mars proposal footprints is a bounded catalog "
            "finding, not clearance against every proposal. This delivery completes "
            "traceable QA, descriptive reproduction and evidence requirements; "
            "completing the deliverables does not complete the original novelty goal. "
            "Blinded trials, controlled overburden experiments and Earth-to-Mars "
            "performance transfer remain future proposals, not open tasks in this delivery."
        ),
    }


PROJECT_REFS = [
    ("P1", "Mars values and scale definitions", "docs/research/main_mars_research_cards.md"),
    ("P2", "Scope, site roles and prior-use findings", "docs/research/main_project_synthesis.md"),
    ("P3", "Final records, QA, dictionary and figures", "outputs/research/elephant_head_final/README.md"),
]
PRIMARY_REFS = [
    ("S1", "Elephant Head study (McKay et al., 2019)", "https://doi.org/10.1017/S0954102019000269"),
    ("S2", "University Valley study (Marinova et al., 2022)", "https://doi.org/10.1017/S0954102022000025"),
    ("S3", "Linnaeus study and GGD6 data", "https://doi.org/10.1017/S0954102098000054"),
    ("S4", "GGD6 version 1", "https://doi.org/10.7265/tjgd-wp08"),
]


def markdown(c: dict) -> str:
    refs = "\n".join(
        f"- [{key}] {label}: [{path}](../../{path})" for key, label, path in PROJECT_REFS
    )
    primary = "\n".join(
        f"- [{key}] [{label}]({url})." for key, label, url in PRIMARY_REFS
    )
    out = f"""# {c['title']}

{c['subtitle']}

## Research question

{c['question']}

## Why retain I-01 and I-02?

{c['retain']}

{md_table(c['mars_headers'], c['mars_rows'])}

{c['mars_note']}

## Three Earth roles

{md_table(c['earth_headers'], [[v.replace(chr(10), '<br>') for v in row] for row in c['earth_rows']])}

{c['earth_note']}

## {c['data_title']}

{c['data_intro']}

{md_table(c['stats_headers'], c['stats_rows'])}

{c['window_note']}

{c['data_limits']}

## What these data cannot answer

{c['cannot']}

## Originality and completion

{c['originality']}

## Sources and reproducible project records

Paths below are relative to the project root. Original studies are linked for attribution; this summary adds no new literature search.

{refs}
{primary}
"""
    return out


def pdf(c: dict) -> None:
    font_dir = Path(reportlab.__file__).parent / "fonts"
    pdfmetrics.registerFont(TTFont("SummarySans", str(font_dir / "Vera.ttf")))
    pdfmetrics.registerFont(TTFont("SummarySans-Bold", str(font_dir / "VeraBd.ttf")))
    ink = colors.HexColor("#14212B")
    muted = colors.HexColor("#45525B")
    rule = colors.HexColor("#CAD2D8")
    style = {
        "title": ParagraphStyle("FinalTitle", fontName="SummarySans-Bold", fontSize=23, leading=26.5, textColor=ink, spaceAfter=9),
        "subtitle": ParagraphStyle("FinalSubtitle", fontName="SummarySans", fontSize=8.5, leading=11.5, textColor=muted, spaceAfter=12),
        "h2": ParagraphStyle("FinalHeading", fontName="SummarySans-Bold", fontSize=11.4, leading=14, textColor=ink, spaceBefore=10, spaceAfter=5),
        "body": ParagraphStyle("FinalBody", fontName="SummarySans", fontSize=9.6, leading=12.6, textColor=ink, spaceAfter=7),
        "small": ParagraphStyle("FinalSmall", fontName="SummarySans", fontSize=8.1, leading=10.4, textColor=muted, spaceAfter=6),
        "cell": ParagraphStyle("FinalCell", fontName="SummarySans", fontSize=9.1, leading=11.6, textColor=ink),
        "th": ParagraphStyle("FinalTH", fontName="SummarySans-Bold", fontSize=8.7, leading=11.2, textColor=ink),
        "ref": ParagraphStyle("FinalRef", fontName="SummarySans", fontSize=7.25, leading=9.3, textColor=muted, spaceAfter=2),
    }

    def p(text: str, key: str = "body") -> Paragraph:
        return Paragraph(escape(text).replace("\n", "<br/>"), style[key])

    def table(headers: list[str], rows: list[list[str]], widths: list[float]) -> Table:
        cells = [[p(x, "th") for x in headers]] + [[p(x, "cell") for x in row] for row in rows]
        t = Table(cells, colWidths=widths, hAlign="LEFT", repeatRows=1)
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF1F3")),
            ("LINEBELOW", (0, 0), (-1, 0), 0.6, rule),
            ("LINEBELOW", (0, 1), (-1, -1), 0.35, colors.HexColor("#DCE2E6")),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return t

    width = A4[0] - 88
    story = [p(c["title"], "title"), p(c["subtitle"], "subtitle")]
    story.append(HRFlowable(width="100%", thickness=0.8, color=ink, spaceAfter=4))
    for title, body in [("Research question", c["question"]), ("Why retain I-01 and I-02?", c["retain"])]:
        story.extend([p(title, "h2"), p(body)])
    story.extend([
        table(c["mars_headers"], c["mars_rows"], [width * 0.50, width * 0.25, width * 0.25]),
        Spacer(1, 6), p(c["mars_note"], "small"),
        p("Three Earth roles", "h2"),
        table(c["earth_headers"], c["earth_rows"], [width * 0.35, width * 0.65]),
        Spacer(1, 6), p(c["earth_note"], "small"), PageBreak(),
        p(c["data_title"], "title"), p(c["data_intro"]),
        table(c["stats_headers"], c["stats_rows"], [width * 0.43, width * 0.19, width * 0.19, width * 0.19]),
        Spacer(1, 6), p(c["window_note"], "small"), p(c["data_limits"]),
        p("What these data cannot answer", "h2"), p(c["cannot"]),
        p("Originality and completion", "h2"), p(c["originality"]),
        p("Sources and reproducible project records", "h2"),
    ])
    for key, label, path in PROJECT_REFS:
        href = "../../" + path
        text = f"[{key}] {escape(label)}: <link href='{escape(href)}' color='#244F70'>{escape(path)}</link>"
        story.append(Paragraph(text, style["ref"]))
    for key, label, url in PRIMARY_REFS:
        text = f"[{key}] <link href='{escape(url)}' color='#244F70'>{escape(label)}</link> - {escape(url)}"
        story.append(Paragraph(text, style["ref"]))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(rule)
        canvas.setLineWidth(0.4)
        canvas.line(44, 34, A4[0] - 44, 34)
        canvas.setFont("SummarySans", 7.3)
        canvas.setFillColor(muted)
        canvas.drawString(44, 22, VERSION + " | Published-data reproduction; no new field experiment")
        canvas.drawRightString(A4[0] - 44, 22, str(doc.page))
        canvas.restoreState()

    doc = SimpleDocTemplate(str(PDF_PATH), pagesize=A4, leftMargin=44, rightMargin=44,
                            topMargin=39, bottomMargin=44, title=c["title"], author="Team zasa",
                            subject=VERSION, allowSplitting=1, pageCompression=1)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    reader = PdfReader(PDF_PATH)
    if len(reader.pages) > 2:
        raise ValueError(f"Summary exceeded two pages: {len(reader.pages)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qa", type=Path, default=EXPORT_DIR / "qa.json")
    parser.add_argument("--accepted-export", action="store_true")
    args = parser.parse_args()
    qa = json.loads(args.qa.read_text())
    required_checks = ["source_hash_matches", "source_literals_roundtrip_all_records",
                       "original_row_page_and_both_times_roundtrip", "all_summary_comparisons_match"]
    if not all(qa["validation"].get(key) is True for key in required_checks):
        raise ValueError("Final EH export QA has not passed the required source/roundtrip checks")
    content = make_content(qa["summary"], args.accepted_export)
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    MD_PATH.write_text(markdown(content))
    pdf(content)
    print(json.dumps({
        "version": VERSION,
        "pages": len(PdfReader(PDF_PATH).pages),
        "files": [{"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size,
                   "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in [MD_PATH, PDF_PATH]],
    }, indent=2))


if __name__ == "__main__":
    main()

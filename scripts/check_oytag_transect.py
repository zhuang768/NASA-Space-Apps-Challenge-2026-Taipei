"""Approximate a published transect from its graticule; never a gypsum GPS."""

import hashlib
import json
from pathlib import Path

import matplotlib
import numpy as np
from shapely.geometry import Point, Polygon

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analog import evidence_status as es
from analog.provenance import write_json
from analog.screening import EARTH_RADIUS_M


def local(lat, lon):
    p0, p, dl = np.deg2rad([39, lat, lon - 75])
    c = np.arccos(np.clip(np.sin(p0) * np.sin(p) + np.cos(p0) * np.cos(p) * np.cos(dl), -1, 1))
    k = c / np.sin(c) if c else 1
    return [
        float(EARTH_RADIUS_M * k * np.cos(p) * np.sin(dl) / 1000),
        float(
            EARTH_RADIUS_M
            * k
            * (np.cos(p0) * np.sin(p) - np.sin(p0) * np.cos(p) * np.cos(dl))
            / 1000
        ),
    ]


def main():
    root = Path(__file__).resolve().parents[1]
    source = root / "outputs/analysis/results_with_context.json"
    candidate = next(
        c
        for c in json.loads(source.read_text())["candidates"]["gale"]
        if c["candidate_id"] == "gale-01"
    )
    polygon = Polygon(candidate["footprint"])
    # Manually read graticule intersections in a Poppler 200 dpi crop:
    # page 2, crop x=100 y=1100 W=730 H=1000; pixel origin top left.
    controls = [
        [90, 689, 75 + 20 / 60, 39],
        [82, 333, 75 + 20 / 60, 39 + 20 / 60],
        [357, 689, 75 + 40 / 60, 39],
        [352, 333, 75 + 40 / 60, 39 + 20 / 60],
    ]
    gcp = np.array(controls, float)
    matrix = np.column_stack([gcp[:, :2], np.ones(4)])
    coefficients = np.linalg.lstsq(matrix, gcp[:, 2:], rcond=None)[0]
    rows = []
    stress_inside = []
    for label, pixel in [("A", [224, 731]), ("B", [262, 686])]:
        lon, lat = np.r_[pixel, 1] @ coefficients
        east, north = local(lat, lon)
        inside = bool(polygon.covers(Point(lon, lat)))
        corners = []
        # Sensitivity envelope is a project assumption, not calibrated map accuracy.
        for dx in (-8, 8):
            for dy in (-8, 8):
                qlon, qlat = np.array([pixel[0] + dx, pixel[1] + dy, 1]) @ coefficients
                x, y = local(qlat, qlon)
                okay = bool(abs(x) <= 50 and abs(y) <= 50 and polygon.covers(Point(qlon, qlat)))
                stress_inside.append(okay)
                corners.append({"east_km": x, "north_km": y, "inside": okay})
        rows.append(
            {
                "label": label,
                "pixel": pixel,
                "approx_lon_deg": float(lon),
                "approx_lat_deg": float(lat),
                "east_km": east,
                "north_km": north,
                "inside": inside,
                "pixel_offset_scenarios": corners,
            }
        )
        print(label, f"approx lat={lat:.4f}, lon={lon:.4f}, east={east:.2f}km north={north:.2f}km")
    write_json(
        root / "outputs/research/oytag_transect_check.json",
        {
            "schema_version": es.SCHEMA_VERSION,
            "generated_utc": es.generated_utc(),
            "candidate_id": candidate["candidate_id"],
            "source_doi": "10.1016/j.tecto.2012.11.031",
            "source_figures": "Fig.2 p28 and Fig.3 p29",
            "source_url": "https://www.igg.cas.cn/zhuantilanmu/solid_earth/solid_earth_research/201307/W020130705569854459276.pdf",
            "source_pdf_sha256": "a9a5fb373a03a15e3ff1c3556f65a587643769f117ea693ed3b9204c361e4d90",
            "source_transport": {
                "tls_certificate_validation": False,
                "independent_hash_check": "pending",
                "note": "Official institute public PDF retrieved with certificate validation disabled after local SSL error; verify DOI and hash independently",
            },
            "candidate_input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "render_command": "pdftoppm -f 2 -l 2 -r 200 -x 100 -y 1100 -W 730 -H 1000 -png -singlefile INPUT.pdf OUTPUT",
            "pixel_origin": "top-left of rendered crop",
            "gcp_columns": ["x_px", "y_px", "longitude_deg", "latitude_deg"],
            "gcp": controls,
            "affine_coefficients": coefficients.tolist(),
            "control_fit_residual_deg": (matrix @ coefficients - gcp[:, 2:]).tolist(),
            "sensitivity": "Endpoint coordinates varied by +/-8 pixels independently; arbitrary diagnostic envelope, not confidence or true georeferencing accuracy",
            "all_8_endpoint_offset_scenarios_inside": all(stress_inside),
            "claims": [
                es.claim(
                    "transect_inside_window",
                    "Mapped A-B transect lies inside the candidate window",
                    es.INFERRED,
                    "Approximate digitization of a published figure; not survey GPS",
                    source="doi:10.1016/j.tecto.2012.11.031 Fig.2",
                ),
                es.claim(
                    "gypsum_on_transect",
                    "A gypsum-bearing layer occurs along this transect",
                    es.EXTERNAL,
                    "Section-level assignment by the paper; no sample-level location",
                    source="doi:10.1016/j.tecto.2012.11.031 Fig.3",
                ),
                es.claim(
                    "gypsum_gps",
                    "Exact gypsum outcrop coordinates",
                    es.UNVERIFIED,
                    "Not located in any retrieved source",
                ),
                es.claim(
                    "same_outcrop_xrd",
                    "XRD of the same gypsum outcrop",
                    es.UNVERIFIED,
                    "No sample-ID/location/mineral chain located",
                ),
                es.claim(
                    "gypsum_clay_iron_oxide_cooccurrence",
                    "Gypsum, clay (smectite) and iron oxide co-occur at one outcrop",
                    es.UNVERIFIED,
                    "Required for a Gale mineral-assemblage analog claim; not established",
                ),
                es.claim(
                    "geology_polygons",
                    "Georeferenced geology polygons",
                    es.UNVERIFIED,
                    "None available",
                ),
            ],
            "endpoints": rows,
        },
    )
    assert all(r["inside"] for r in rows) and all(stress_inside)
    fig, ax = plt.subplots(figsize=(9, 6))
    fig.subplots_adjust(bottom=0.20, top=0.90, left=0.12, right=0.96)
    samples = json.loads((root / "outputs/research/oytag_overlap.json").read_text())["samples"]
    ax.scatter(
        [s["east_km"] for s in samples],
        [s["north_km"] for s in samples],
        color="#b25d19",
        label="2012 rock sample coordinates",
    )
    for s in samples:
        ax.annotate(
            s["sample_id"],
            (s["east_km"], s["north_km"]),
            xytext=(5, -12),
            textcoords="offset points",
            fontsize=9,
        )
    ax.plot(
        [r["east_km"] for r in rows],
        [r["north_km"] for r in rows],
        color="#087f8c",
        marker="o",
        label="2013 A-B (approximate figure digitization)",
    )
    for r in rows:
        ax.annotate(
            r["label"], (r["east_km"], r["north_km"]), xytext=(7, 3), textcoords="offset points"
        )
        corners = r["pixel_offset_scenarios"]
        ax.scatter(
            [c["east_km"] for c in corners],
            [c["north_km"] for c in corners],
            marker="+",
            color="#087f8c",
            s=25,
        )
    ax.axvline(50, color="#555", linestyle="--", label="100 km window east boundary")
    ax.set(
        xlim=(35, 52),
        ylim=(-9, 4),
        xlabel="Local east from (39N,75E), km",
        ylabel="Local north, km",
        title="Oytag: nearby evidence is not the same outcrop",
    )
    ax.set_aspect("equal")
    ax.grid(alpha=0.2)
    ax.legend(loc="lower left", fontsize=8)
    fig.text(
        0.5,
        0.025,
        "Original coordinate schematic. + marks: assumed +/-8 pixel scenarios; not survey accuracy.\nNo gypsum GPS or same-outcrop mineral identification.",
        ha="center",
        fontsize=8,
    )
    fig.savefig(root / "outputs/research/oytag_transect_schematic.png", dpi=160)
    plt.close(fig)
    print(
        "Base endpoints and all 8 diagnostic scenarios inside; exact gypsum point remains unknown"
    )


if __name__ == "__main__":
    main()

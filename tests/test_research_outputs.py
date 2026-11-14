"""Structural checks for outputs/research JSON; no values are recomputed."""

import csv
import json
from pathlib import Path

from analog.evidence_status import LEVELS

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "outputs/research"


def load(name):
    return json.loads((RESEARCH / name).read_text())


def test_claim_levels_use_shared_vocabulary():
    for name in ["oytag_overlap.json", "oytag_transect_check.json"]:
        claims = load(name)["claims"]
        assert claims and all(c["level"] in LEVELS for c in claims)
    audit = load("oytag_outcrop_source_audit.json")
    for key in ["gypsum_position_status", "same_outcrop_mineralogy_status"]:
        assert audit[key]["level"] in LEVELS


def test_evidence_records_keyed_by_canonical_ids():
    data = load("three_candidate_evidence.json")
    base = json.loads((ROOT / "outputs/analysis/results_with_context.json").read_text())
    ids = {c["candidate_id"] for cands in base["candidates"].values() for c in cands}
    for record in data["records"]:
        assert record["candidate_id"] == record["candidate"]["candidate_id"] in ids
        assert record["mars_target"] in data["mars_profiles"]
        assert record["scale10km_rank"] is None or isinstance(record["scale10km_rank"], int)
        status = record["prior_analog_literature"]["status"]
        assert record["candidate"]["prior_analog_literature_status"] == status


def test_oytag_points_numeric_and_disjoint_from_supplement():
    overlap = load("oytag_overlap.json")
    assert overlap["candidate_id"] == "gale-01"
    for s in overlap["samples"]:
        assert isinstance(s["latitude_deg"], float) and isinstance(s["longitude_deg"], float)
    with open(RESEARCH / "oytag_supplement_coordinates.csv") as stream:
        supplement = {r["parent_sample_id"] for r in csv.DictReader(stream)}
    assert not supplement & {s["sample_id"] for s in overlap["samples"]}

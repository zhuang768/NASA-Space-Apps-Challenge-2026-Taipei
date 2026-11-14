"""Shared verification vocabulary for research outputs.

Every claim in outputs/research/*.json carries one of these levels plus a free-text
note. The level says how the claim is supported, never how likely it is to be true;
it is not a confidence score.
"""

SCHEMA_VERSION = "1.0"

VERIFIED = "VERIFIED"  # reproduced by a project script from hashed inputs
INFERRED = "INFERRED"  # derived by the project from figures/maps; approximate
EXTERNAL = "EXTERNAL"  # stated by a cited publication; not re-measured here
UNVERIFIED = "UNVERIFIED"  # looked for, no evidence chain located

LEVELS = (VERIFIED, INFERRED, EXTERNAL, UNVERIFIED)


def claim(claim_id, statement, level, note, source=None):
    """One verification claim with a fixed shape."""
    assert level in LEVELS, level
    record = {"id": claim_id, "statement": statement, "level": level, "note": note}
    if source:
        record["source"] = source
    return record


def generated_utc():
    from datetime import UTC, datetime

    return datetime.now(UTC).replace(microsecond=0).isoformat()

"""Conditional identifiability diagnostic; no Earth/Mars ice fraction retrieval.

Two-component, low-loss modified CRIM from Thomson et al. (2012), eq. 7.
Fixing effective permittivity does not fix ice fraction without host permittivity.
All values below are stated assumptions, not new measurements.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    ice_permittivity = 3.0
    effective_permittivity = 3.2
    rows = []
    for host in (2.8, 3.2, 3.57, 5.8):
        fraction = ((math.sqrt(effective_permittivity) - math.sqrt(host)) /
                    (math.sqrt(ice_permittivity) - math.sqrt(host)))
        admissible = 0.0 <= fraction <= 1.0
        reconstructed = (fraction * math.sqrt(ice_permittivity) +
                         (1.0-fraction) * math.sqrt(host)) ** 2
        assert math.isclose(reconstructed, effective_permittivity, abs_tol=1e-12)
        rows.append(dict(
            scenario_id=f"CRIM-KS-{host:g}",
            effective_permittivity_assumed=effective_permittivity,
            ice_permittivity_assumed=ice_permittivity,
            host_permittivity_assumed=host,
            algebraic_ice_fraction=fraction,
            physically_admissible_in_this_model=admissible,
            reconstructed_effective_permittivity=reconstructed,
            result_type="conditional_synthetic_identifiability_check",
            observation_site="none",
            source_equation="https://doi.org/10.1029/2012JE004053; equation 7",
        ))
    with (ROOT / "crim_identifiability.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    feasible = [r for r in rows if r["physically_admissible_in_this_model"]]
    # Distinct ice fractions reproduce the same assumed effective permittivity.
    assert len(feasible) == 3
    assert len({round(r["algebraic_ice_fraction"], 8) for r in feasible}) == 3
    result = {
        "calculation_status": "pass",
        "scientific_scope": "algebraic non-uniqueness only, not field validation",
        "formula": "Ke=(fi*sqrt(Ki)+(1-fi)*sqrt(Ks))**2",
        "assumptions": ["two components: ice and host sediment",
                        "low loss; no liquid water, air, temperature or frequency dependence",
                        "Ki=3 and Ke=3.2 fixed for illustration",
                        "Ks scenarios are assumed; no MS-02 host material measurement"],
        "feasible_scenarios": len(feasible),
        "admissible_ice_fractions": [r["algebraic_ice_fraction"] for r in feasible],
        "rejected_scenarios": [r["scenario_id"] for r in rows if not r["physically_admissible_in_this_model"]],
        "cannot_conclude": ["actual MS-02 ice presence or fraction",
                            "actual Earth-line ice fraction",
                            "validation of any WISDOM model permittivity",
                            "reproduction of Thomson original radar/core analysis"],
    }
    (ROOT / "crim_identifiability.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

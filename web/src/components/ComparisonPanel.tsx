import React from "react";
import { AlertTriangle, ExternalLink, FileSearch, ShieldAlert } from "lucide-react";
import type {
  CandidateItem,
  ComparabilityLevel,
  ComparisonRow,
  EvidenceStatus,
  TargetBundle,
  TopicDomain,
} from "../types/workbench";

interface ComparisonPanelProps {
  target: TargetBundle;
  candidate: CandidateItem | null;
  rows: ComparisonRow[];
  onInspectEvidence: (row: ComparisonRow) => void;
}

const DOMAIN_ORDER: TopicDomain[] = [
  "Terrain",
  "Temperature",
  "Water/Ice",
  "Air/Dust",
];

function comparabilityClass(level: ComparabilityLevel): string {
  switch (level) {
    case "Direct":
      return "badge badge-cyan";
    case "Modeled proxy":
      return "badge badge-amber";
    case "Contextual":
      return "badge badge-neutral";
    case "Not comparable":
      return "badge badge-danger";
  }
}

function statusClass(status: EvidenceStatus): string {
  switch (status) {
    case "Supported":
      return "badge badge-cyan";
    case "Mismatch":
      return "badge badge-danger";
    case "Provisional":
    case "Provisional observations":
    case "Failed quality checks":
    case "Analysis incomplete":
      return "badge badge-amber";
    case "Source access failed":
    case "Stale results":
      return "badge badge-danger";
    case "Unknown":
    case "Not checked":
    case "Missing data":
    case "Outside coverage":
    default:
      return "badge badge-neutral";
  }
}

export const ComparisonPanel: React.FC<ComparisonPanelProps> = ({
  target,
  candidate,
  rows,
  onInspectEvidence,
}) => {
  if (!candidate) {
    return (
      <section className="panel comparison-panel" aria-label="Earth to Mars Comparison">
        <div className="panel-header">
          <div>
            <h2 className="panel-title">Earth ↔ Mars Evidence Matrix</h2>
            <p className="panel-subtitle">
              Select a candidate from the shortlist to inspect domain-level evidence for{" "}
              <strong>{target.title}</strong>.
            </p>
          </div>
        </div>
        <div className="empty-state">
          <FileSearch size={24} aria-hidden="true" />
          <p>No candidate selected. Choose a site from the Candidate List to compare metrics.</p>
        </div>
      </section>
    );
  }

  return (
    <section className="panel comparison-panel" aria-label="Earth to Mars Comparison">
      <div className="panel-header">
        <div>
          <h2 className="panel-title">
            Earth ↔ Mars Evidence Matrix — {candidate.candidate_id} (Rank #{candidate.rank})
          </h2>
          <p className="panel-subtitle">
            {candidate.lat.toFixed(2)}°, {candidate.lon.toFixed(2)}° ·{" "}
            {candidate.evidenceCompleteness.label} · {candidate.classification}
          </p>
        </div>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", alignItems: "center" }}>
          <span className="badge badge-amber" title="Only Terrain domain is currently scored">
            Analysis incomplete (3/4 domains unscored)
          </span>
          {target.id === "jezero" ? (
            <span className="badge badge-amber" title="MEDA TIRS sols 700-702 have 0/159,418 qualified records">
              Provisional observations · Failed quality checks
            </span>
          ) : (
            <span className="badge badge-neutral" title="No rover TIRS coverage at this target">
              Outside coverage (Rover TIRS)
            </span>
          )}
          <span className="badge badge-neutral" title="Missing values are never coerced to 0">
            Missing data ≠ 0
          </span>
          {candidate.featured && (
            <span
              className="badge badge-neutral"
              title="Number of tested configurations keeping this candidate in Top-2; not probability or confidence"
            >
              Deep-dive · Top-2 in {candidate.featured.top2_count}/{candidate.featured.configurations_count} configs
            </span>
          )}
          {candidate.oytagOverlay && (
            <span
              className="badge badge-cyan"
              title="Published lithology points inside the window; gypsum location and same-outcrop mineralogy unverified"
            >
              Literature: lithology overlap (partial)
            </span>
          )}
        </div>
      </div>

      <div className="guardrail-banner" role="note">
        <ShieldAlert size={18} aria-hidden="true" />
        <div>
          <strong>Physical Non-Comparability Guardrails:</strong> Identical units do not imply
          direct comparability. Do not combine or subtract MODIS/POWER T2M vs. TES thermal inertia,
          SWIM ice consistency vs. precipitation/soil moisture, 550 nm AOT vs. 9.3 μm CDOD, or
          provisional MEDA brightness temperature vs. regional LST. Evidence completeness is not
          confidence.
        </div>
      </div>

      <div className="domain-groups">
        {DOMAIN_ORDER.map((domain) => {
          const domainRows = rows.filter((r) => r.domain === domain);
          if (domainRows.length === 0) return null;

          return (
            <div key={domain} className="domain-section">
              <div className="domain-header">
                <h3>{domain}</h3>
                <span className="domain-count">
                  {domainRows.length} {domainRows.length === 1 ? "metric" : "metrics"}
                </span>
              </div>

              <div className="table-scroll">
                <table className="comparison-table">
                  <thead>
                    <tr>
                      <th scope="col">Quantity / Metric</th>
                      <th scope="col">Earth Candidate</th>
                      <th scope="col">Mars Target ({target.title})</th>
                      <th scope="col">Period &amp; Support</th>
                      <th scope="col">Method &amp; Threshold</th>
                      <th scope="col">Comparability &amp; Status</th>
                      <th scope="col">Provenance</th>
                    </tr>
                  </thead>
                  <tbody>
                    {domainRows.map((row) => (
                      <tr key={row.id}>
                        <td>
                          <div className="metric-name">{row.metricName}</div>
                          <div className="metric-sub">
                            {row.comparability === "Not comparable" && (
                              <span className="inline-warn">
                                <AlertTriangle size={12} aria-hidden="true" /> Not directly
                                comparable
                              </span>
                            )}
                          </div>
                        </td>
                        <td>
                          <div className="value-main">{row.earthValue}</div>
                          <div className="value-qty">{row.earthQuantity}</div>
                        </td>
                        <td>
                          <div className="value-main">{row.marsValue}</div>
                          <div className="value-qty">{row.marsQuantity}</div>
                        </td>
                        <td>
                          <div className="cell-text">{row.periodAndSupport}</div>
                        </td>
                        <td>
                          <div className="cell-text">{row.methodAndThreshold}</div>
                        </td>
                        <td>
                          <div className="badge-stack">
                            <span className={comparabilityClass(row.comparability)}>
                              {row.comparability}
                            </span>
                            <span className={statusClass(row.status)}>{row.status}</span>
                          </div>
                        </td>
                        <td>
                          <button
                            type="button"
                            className="btn-evidence"
                            onClick={() => onInspectEvidence(row)}
                            aria-label={`Inspect evidence for ${row.metricName}`}
                          >
                            <span>Inspect</span>
                            <ExternalLink size={13} aria-hidden="true" />
                          </button>
                          <div className="source-label">{row.sourcePortalLabel}</div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

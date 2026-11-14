import { useEffect, useMemo, useState } from "react";
import { AlertCircle, BookOpen, MapPin } from "lucide-react";
import type { CandidateItem } from "../types/workbench";

interface Props {
  candidates: CandidateItem[];
  selectedCandidate: CandidateItem | null;
  onSelectCandidate: (c: CandidateItem) => void;
}

type FilterMode = "all" | "with_climate" | "featured";

export function CandidateList({
  candidates,
  selectedCandidate,
  onSelectCandidate,
}: Props) {
  const [filter, setFilter] = useState<FilterMode>("all");

  useEffect(() => {
    setFilter("all");
  }, [candidates]);

  const featuredCount = candidates.filter((c) => c.featured).length;

  const filtered = useMemo(() => {
    if (filter === "with_climate") {
      return candidates.filter((c) => c.earth_climate_context?.status === "context_only_not_ranked");
    }
    if (filter === "featured") {
      return candidates.filter((c) => c.featured);
    }
    return candidates;
  }, [candidates, filter]);

  return (
    <aside className="panel" aria-label="Earth candidate shortlist">
      <div className="panel-header" style={{ marginBottom: 8 }}>
        <div>
          <h2 className="panel-title">3. Candidate Shortlist</h2>
          <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: 2 }}>
            Ranked within 60°S–60°N (≥300 km separation, terrain D only)
          </div>
        </div>
      </div>

      <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 12 }}>
        <button
          type="button"
          className={`btn ${filter === "all" ? "btn-active" : ""}`}
          onClick={() => setFilter("all")}
          style={{ padding: "4px 9px", fontSize: "0.75rem" }}
        >
          All ({candidates.length})
        </button>
        <button
          type="button"
          className={`btn ${filter === "with_climate" ? "btn-active" : ""}`}
          onClick={() => setFilter("with_climate")}
          style={{ padding: "4px 9px", fontSize: "0.75rem" }}
        >
          With POWER (Top 2)
        </button>
        <button
          type="button"
          className={`btn ${filter === "featured" ? "btn-active" : ""}`}
          onClick={() => setFilter("featured")}
          style={{ padding: "4px 9px", fontSize: "0.75rem" }}
          title="Candidates with a research deep-dive in outputs/research/"
        >
          Deep-dive ({featuredCount})
        </button>
      </div>

      {filtered.length === 0 ? (
        <div
          role="status"
          style={{
            padding: 16,
            borderRadius: 8,
            border: "1px dashed var(--border-strong)",
            background: "var(--bg-subtle)",
            color: "var(--text-secondary)",
            fontSize: "0.82rem",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 6, fontWeight: 600, color: "#fbbf24" }}>
            <AlertCircle size={15} aria-hidden="true" />
            No qualifying candidates
          </div>
          <p style={{ margin: "6px 0 0", color: "var(--text-muted)" }}>
            {filter === "featured"
              ? "No research deep-dive exists for this Mars target in outputs/research/."
              : "No candidates for this Mars target match the selected filter."}
          </p>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 8, maxHeight: 680, overflowY: "auto", paddingRight: 2 }}>
          {filtered.map((c) => {
            const isSel = selectedCandidate?.candidate_id === c.candidate_id;
            return (
              <button
                key={c.candidate_id}
                type="button"
                onClick={() => onSelectCandidate(c)}
                aria-pressed={isSel}
                style={{
                  textAlign: "left",
                  width: "100%",
                  padding: "10px 12px",
                  borderRadius: 8,
                  border: `1px solid ${isSel ? "var(--cyan)" : "var(--border)"}`,
                  background: isSel ? "rgba(34, 211, 238, 0.08)" : "var(--bg-elevated)",
                  cursor: "pointer",
                  display: "flex",
                  flexDirection: "column",
                  gap: 6,
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 }}>
                  <span className="mono" style={{ fontWeight: 700, fontSize: "0.86rem", color: isSel ? "var(--cyan)" : "var(--text-primary)" }}>
                    #{c.rank} · {c.candidate_id}
                  </span>
                  <span
                    className={`badge ${c.classification === "Literature checked (partial)" ? "badge-cyan" : "badge-amber"}`}
                  >
                    {c.classification}
                  </span>
                </div>

                <div className="mono" style={{ fontSize: "0.78rem", color: "var(--text-secondary)", display: "flex", alignItems: "center", gap: 5 }}>
                  <MapPin size={12} aria-hidden="true" />
                  {c.lat.toFixed(1)}°, {c.lon.toFixed(1)}°
                  <span style={{ color: "var(--text-muted)", marginLeft: "auto" }}>
                    D = {c.terrain_distance.toFixed(4)}
                  </span>
                </div>

                <div>
                  <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.72rem", color: "var(--text-muted)", marginBottom: 3 }}>
                    <span>Evidence completeness (not confidence)</span>
                    <span className="mono">{c.evidenceCompleteness.scoredDomains}/{c.evidenceCompleteness.totalDomains}</span>
                  </div>
                  <div style={{ height: 5, borderRadius: 999, background: "#090e1a", overflow: "hidden" }}>
                    <div
                      style={{
                        width: `${(c.evidenceCompleteness.scoredDomains / c.evidenceCompleteness.totalDomains) * 100}%`,
                        height: "100%",
                        background: "var(--cyan)",
                      }}
                    />
                  </div>
                </div>

                {c.featured && (
                  <div
                    style={{ display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap", fontSize: "0.72rem" }}
                  >
                    <span className="badge badge-neutral" style={{ display: "inline-flex", alignItems: "center", gap: 4 }}>
                      <BookOpen size={11} aria-hidden="true" /> Deep-dive
                    </span>
                    <span
                      className="mono"
                      style={{ color: "var(--text-muted)" }}
                      title="Configurations keeping this candidate in Top-2; not probability or confidence"
                    >
                      Top-2 in {c.featured.top2_count}/{c.featured.configurations_count} configs
                      {c.oytagOverlay ? ` · ${c.oytagOverlay.samples.length} lit. samples in window` : ""}
                    </span>
                  </div>
                )}

                <div style={{ fontSize: "0.75rem", color: "var(--text-secondary)" }}>
                  <strong style={{ color: "#34d399" }}>Support:</strong> {c.keySupport}
                </div>
                <div style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                  <strong style={{ color: "#fbbf24" }}>Gap:</strong> {c.mainGap}
                </div>
              </button>
            );
          })}
        </div>
      )}
    </aside>
  );
}

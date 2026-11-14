import { AlertTriangle, Compass, Layers, Radio } from "lucide-react";
import type { TargetBundle, TargetId } from "../types/workbench";
import { WORKBENCH_META } from "../data/adapter";

interface Props {
  targetIds: TargetId[];
  activeTargetId: TargetId;
  target: TargetBundle | null;
  demoMode: boolean;
  onSelectTarget: (id: TargetId) => void;
  onToggleDemoMode: () => void;
}

export function TargetMissionBar({
  targetIds,
  activeTargetId,
  target,
  demoMode,
  onSelectTarget,
  onToggleDemoMode,
}: Props) {
  const params = WORKBENCH_META.parameters ?? {};
  const counts = WORKBENCH_META.counts ?? {};

  return (
    <header className="panel" aria-label="Target and mission configuration">
      {demoMode && (
        <div className="notice-banner demo-banner" role="alert" style={{ marginBottom: 12 }}>
          <span>
            <AlertTriangle size={16} style={{ verticalAlign: "text-bottom", marginRight: 6 }} />
            DEMO DATA — Not scientific results (synthetic preview mode active; switch back to Real Results for verified outputs)
          </span>
          <button className="btn" onClick={onToggleDemoMode}>
            Return to Real Results
          </button>
        </div>
      )}

      <div className="panel-header" style={{ marginBottom: 10 }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
            <Compass size={20} color="#22d3ee" aria-hidden="true" />
            <h1 style={{ margin: 0, fontSize: "1.2rem", fontWeight: 700, letterSpacing: "-0.01em" }}>
              TerraMatch Mission Lab
            </h1>
            <span className="badge badge-cyan">Earth–Mars Analog Workbench</span>
            <span className="badge badge-amber">
              Terrain screening
            </span>
          </div>
          <p className="header-description">Find Earth regions for Mars research. Trace what matches and what is still unknown.</p>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <label htmlFor="target-select" style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
            Mars Target:
          </label>
          <select
            id="target-select"
            value={activeTargetId}
            onChange={(e) => onSelectTarget(e.target.value as TargetId)}
            style={{
              background: "var(--bg-elevated)",
              border: "1px solid var(--border-strong)",
              borderRadius: 6,
              padding: "6px 10px",
              fontSize: "0.86rem",
              fontWeight: 600,
              color: "var(--cyan)",
            }}
          >
            {targetIds.map((id) => (
              <option key={id} value={id}>
                {id === "jezero"
                  ? "Jezero Crater (18.44°N, 77.45°E)"
                  : id === "gale"
                  ? "Gale Crater (4.59°S, 137.44°E)"
                  : "Arcadia Design Target (40.0°N, 170.0°W)"}
              </option>
            ))}
          </select>

          <button
            type="button"
            className={`btn ${demoMode ? "btn-active" : ""}`}
            onClick={onToggleDemoMode}
            title="Toggle isolated demo preview mode"
          >
            <Radio size={14} aria-hidden="true" />
            {demoMode ? "Demo preview on" : "Preview synthetic demo"}
          </button>
        </div>
      </div>

      {target ? (
        <details className="method-details">
        <summary>Research question, method & data provenance</summary>
        <p className="provenance-line">NASA Space Apps 2026 · Team zasa · Analysis commit <span className="mono">{WORKBENCH_META.base_commit ?? "unknown"}</span> · Generated {WORKBENCH_META.generated_utc ?? "unknown"}</p>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(min(220px, 100%), 1fr))",
            gap: 12,
            paddingTop: 10,
            borderTop: "1px solid var(--border)",
            fontSize: "0.82rem",
          }}
        >
          <div>
            <div style={{ color: "var(--text-muted)", fontSize: "0.74rem", textTransform: "uppercase" }}>
              Research Question
            </div>
            <div style={{ color: "var(--text-primary)", marginTop: 2 }}>{target.researchQuestion}</div>
            <div style={{ color: "var(--text-muted)", fontSize: "0.75rem", marginTop: 3 }}>
              Coordinate source: <span className="mono">{target.summary.coordinate_source}</span>
            </div>
          </div>

          <div>
            <div style={{ color: "var(--text-muted)", fontSize: "0.74rem", textTransform: "uppercase" }}>
              Physical Window
            </div>
            <div className="mono" style={{ fontWeight: 600, marginTop: 2 }}>
              {params.window_km ?? 100} × {params.window_km ?? 100} km
            </div>
            <div style={{ color: "var(--text-muted)", fontSize: "0.75rem" }}>
              {params.sample_spacing_km ?? 4} km spacing ({params.slope_stencil_km ?? 8} km stencil)
            </div>
          </div>

          <div>
            <div style={{ color: "var(--text-muted)", fontSize: "0.74rem", textTransform: "uppercase" }}>
              Search Bounds
            </div>
            <div className="mono" style={{ fontWeight: 600, marginTop: 2 }}>
              {params.earth_search_latitude_bounds?.[0] ?? -60}° to +{params.earth_search_latitude_bounds?.[1] ?? 60}°
            </div>
            <div style={{ color: "var(--text-muted)", fontSize: "0.75rem" }}>
              {counts.valid_windows ?? "—"} valid / {counts.land_centres_before_window_filter ?? "—"} land centres
            </div>
          </div>

          <div>
            <div style={{ color: "var(--text-muted)", fontSize: "0.74rem", textTransform: "uppercase" }}>
              Data Period
            </div>
            <div className="mono" style={{ fontWeight: 600, marginTop: 2 }}>
              2023–2024 (Earth)
            </div>
            <div style={{ color: "var(--text-muted)", fontSize: "0.75rem" }}>
              MOLA / TES / SWIM 2.0 / MY34–35
            </div>
          </div>

          <div>
            <div style={{ color: "var(--text-muted)", fontSize: "0.74rem", textTransform: "uppercase" }}>
              Pipeline Status
            </div>
            <div style={{ marginTop: 4, display: "flex", gap: 6, flexWrap: "wrap" }}>
              <span className="badge badge-amber">
                <Layers size={11} aria-hidden="true" />
                Terrain Scored Only
              </span>
            </div>
            <div style={{ color: "var(--text-muted)", fontSize: "0.75rem", marginTop: 2 }}>
              Atacama, Iceland, Hawaii excluded
            </div>
          </div>
        </div>
        </details>
      ) : (
        <div className="notice-banner" role="status">
          Target data unavailable. Select another Mars target.
        </div>
      )}
    </header>
  );
}

import { useState } from "react";
import { Globe2, Info, ZoomIn, ZoomOut } from "lucide-react";
import type { CandidateItem, TargetBundle } from "../types/workbench";
import { WORKBENCH_META } from "../data/adapter";

interface Props {
  target: TargetBundle;
  selectedCandidate: CandidateItem | null;
  onSelectCandidate: (c: CandidateItem) => void;
}

function projectEq(lat: number, lon: number, w: number, h: number): [number, number] {
  const x = ((lon + 180) / 360) * w;
  const y = ((90 - lat) / 180) * h;
  return [x, y];
}

export function DualSideMap({ target, selectedCandidate, onSelectCandidate }: Props) {
  const [earthView, setEarthView] = useState<"global" | "local">("global");
  const [marsZoomKm, setMarsZoomKm] = useState<number>(100);
  const [showFigures, setShowFigures] = useState<boolean>(false);

  const W = 520;
  const H = 260;
  const excludedBoxes: [number, number, number, number, string][] =
    WORKBENCH_META.parameters?.excluded_boxes ?? [];

  const mLat = target.summary.lat;
  const mLon = target.summary.lon;
  const [mx, my] = projectEq(mLat, mLon, W, H);

  // Earth physical 100 km box angular span at R=6371 km vs Mars at R=3396 km
  const earthWindowLatDeg = (100 / 6371.0) * (180 / Math.PI);
  const marsWindowLatDeg = (marsZoomKm / 3396.0) * (180 / Math.PI);

  // Mars physical box half-size in degrees (~100 km at R=3396 km)
  const marsHalfLatDeg = ((marsZoomKm / 2) / 3396) * (180 / Math.PI);
  const marsHalfLonDeg = marsHalfLatDeg / Math.max(0.2, Math.cos((mLat * Math.PI) / 180));

  return (
    <section className="panel" aria-label="Dual-side planetary map">
      <div className="panel-header">
        <div>
          <h2 className="panel-title">2. Dual-Side Spatial Context (Independent Planetary Projections)</h2>
          <p style={{ margin: "2px 0 0", fontSize: "0.78rem", color: "var(--text-muted)" }}>
            Earth (R = 6,371.0 km, Δlat ≈ {earthWindowLatDeg.toFixed(2)}° per 100 km) vs. Mars (R = 3,396.0 km, IAU2000 planetocentric, Δlat ≈ {((100 / 3396.0) * (180 / Math.PI)).toFixed(2)}° per 100 km).
            Physical 100×100 km windows — never synced by raw zoom level or Web Mercator.
          </p>
        </div>
        <button
          type="button"
          className={`btn ${showFigures ? "btn-active" : ""}`}
          onClick={() => setShowFigures((v) => !v)}
          style={{ fontSize: "0.76rem", padding: "5px 10px" }}
        >
          {showFigures ? "Hide Diagnostic Figures" : "View Pipeline Figures (2)"}
        </button>
      </div>

      <div className="dual-map-grid">
        {/* LEFT: EARTH */}
        <div
          style={{
            background: "var(--bg-subtle)",
            border: "1px solid var(--border)",
            borderRadius: 8,
            padding: 12,
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8, gap: 8, flexWrap: "wrap" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <Globe2 size={15} color="#22d3ee" aria-hidden="true" />
              <strong style={{ fontSize: "0.85rem" }}>Earth — Search & Candidate Footprints</strong>
            </div>
            <div style={{ display: "flex", gap: 6 }}>
              <button
                type="button"
                className={`btn ${earthView === "global" ? "btn-active" : ""}`}
                onClick={() => setEarthView("global")}
                style={{ padding: "3px 8px", fontSize: "0.74rem" }}
              >
                Global 60°S–60°N
              </button>
              <button
                type="button"
                className={`btn ${earthView === "local" ? "btn-active" : ""}`}
                onClick={() => setEarthView("local")}
                disabled={!selectedCandidate}
                style={{ padding: "3px 8px", fontSize: "0.74rem" }}
              >
                100 km Footprint
              </button>
            </div>
          </div>

          {earthView === "global" ? (
            <svg
              viewBox={`0 0 ${W} ${H}`}
              width="100%"
              role="img"
              aria-label="Earth equirectangular candidate distribution map"
              style={{ display: "block", background: "#070c16", borderRadius: 6, border: "1px solid var(--border)" }}
            >
              {/* Search bounds 60S-60N */}
              <rect
                x={0}
                y={projectEq(60, -180, W, H)[1]}
                width={W}
                height={projectEq(-60, -180, W, H)[1] - projectEq(60, -180, W, H)[1]}
                fill="rgba(34, 211, 238, 0.04)"
              />
              {/* Graticule */}
              {[-60, -30, 0, 30, 60].map((lat) => {
                const [, y] = projectEq(lat, 0, W, H);
                return (
                  <g key={`elat-${lat}`}>
                    <line x1={0} y1={y} x2={W} y2={y} stroke="#1e293b" strokeDasharray={lat === 0 ? undefined : "3 3"} />
                    <text x={4} y={y - 3} fill="#64748b" fontSize="9" fontFamily="monospace">
                      {lat}°
                    </text>
                  </g>
                );
              })}
              {[-120, -60, 0, 60, 120].map((lon) => {
                const [x] = projectEq(0, lon, W, H);
                return <line key={`elon-${lon}`} x1={x} y1={0} x2={x} y2={H} stroke="#1e293b" strokeDasharray="3 3" />;
              })}

              {/* Excluded boxes (Atacama, Iceland, Hawaii) */}
              {excludedBoxes.map(([wLon, eLon, sLat, nLat, label]) => {
                const [x1, y1] = projectEq(nLat, wLon, W, H);
                const [x2, y2] = projectEq(sLat, eLon, W, H);
                return (
                  <g key={label}>
                    <rect
                      x={x1}
                      y={y1}
                      width={Math.max(4, x2 - x1)}
                      height={Math.max(4, y2 - y1)}
                      fill="rgba(251, 113, 133, 0.16)"
                      stroke="#fb7185"
                      strokeWidth={1}
                      strokeDasharray="2 2"
                    />
                  </g>
                );
              })}

              {/* All 12 candidates */}
              {target.candidates.map((c) => {
                const [cx, cy] = projectEq(c.lat, c.lon, W, H);
                const isSel = selectedCandidate?.candidate_id === c.candidate_id;
                return (
                  <g
                    key={c.candidate_id}
                    role="button"
                    tabIndex={0}
                    aria-label={`Select candidate #${c.rank} ${c.candidate_id} at ${c.lat.toFixed(1)}°, ${c.lon.toFixed(1)}°`}
                    onClick={() => onSelectCandidate(c)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" || e.key === " ") {
                        e.preventDefault();
                        onSelectCandidate(c);
                      }
                    }}
                    style={{ cursor: "pointer" }}
                  >
                    <circle
                      cx={cx}
                      cy={cy}
                      r={isSel ? 7 : 4.5}
                      fill={isSel ? "#22d3ee" : "#94a3b8"}
                      fillOpacity={isSel ? 0.95 : 0.7}
                      stroke={isSel ? "#ffffff" : "#0f172a"}
                      strokeWidth={isSel ? 1.8 : 1}
                    />
                    {isSel && (
                      <text x={cx + 9} y={cy + 3} fill="#22d3ee" fontSize="10" fontWeight="bold" fontFamily="monospace">
                        #{c.rank} {c.candidate_id}
                      </text>
                    )}
                  </g>
                );
              })}
            </svg>
          ) : selectedCandidate ? (
            <svg
              viewBox={`0 0 ${W} ${H}`}
              width="100%"
              role="img"
              aria-label={`Local 100x100 km footprint for ${selectedCandidate.candidate_id}`}
              style={{ display: "block", background: "#070c16", borderRadius: 6, border: "1px solid var(--border)" }}
            >
              {/* 100x100 km local polygon normalized into box */}
              <rect x={175} y={45} width={170} height={170} fill="rgba(34,211,238,0.12)" stroke="#22d3ee" strokeWidth={2} />
              <circle cx={260} cy={130} r={4} fill="#22d3ee" />
              <text x={260} y={118} textAnchor="middle" fill="#f1f5f9" fontSize="11" fontFamily="monospace">
                {selectedCandidate.lat.toFixed(2)}°, {selectedCandidate.lon.toFixed(2)}°
              </text>
              <text x={260} y={148} textAnchor="middle" fill="#94a3b8" fontSize="10" fontFamily="monospace">
                100 × 100 km · 4 km grid (26×26 pts)
              </text>
              {/* Scale bar */}
              <line x1={20} y1={235} x2={105} y2={235} stroke="#22d3ee" strokeWidth={2} />
              <text x={20} y={228} fill="#cbd5e1" fontSize="10" fontFamily="monospace">
                Scale: 50 km (R_earth = 6,371.0 km · Δlat = {earthWindowLatDeg.toFixed(2)}° / 100 km)
              </text>
              {selectedCandidate.footprint?.length >= 4 && (() => {
                const lons = selectedCandidate.footprint.map((p) => p[0]);
                const lats = selectedCandidate.footprint.map((p) => p[1]);
                const minLat = Math.min(...lats);
                const maxLat = Math.max(...lats);
                const minLon = Math.min(...lons);
                const maxLon = Math.max(...lons);
                return (
                  <text x={W - 16} y={228} textAnchor="end" fill="#94a3b8" fontSize="9.5" fontFamily="monospace">
                    Bounds: [{minLat.toFixed(2)}°..{maxLat.toFixed(2)}° lat, {minLon.toFixed(2)}°..{maxLon.toFixed(2)}° lon]
                  </text>
                );
              })()}
            </svg>
          ) : null}

          <div style={{ marginTop: 8, fontSize: "0.74rem", color: "var(--text-muted)", display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: 6 }}>
            <span>CRS: EPSG:4326 equirectangular · Excluded: Atacama, Iceland, Hawaii (rose dashed)</span>
            <span className="mono">Layer: ETOPO 2022 + Natural Earth 110m</span>
          </div>
        </div>

        {/* RIGHT: MARS */}
        <div
          style={{
            background: "var(--bg-subtle)",
            border: "1px solid var(--border)",
            borderRadius: 8,
            padding: 12,
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8, gap: 8, flexWrap: "wrap" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <Globe2 size={15} color="#f59e0b" aria-hidden="true" />
              <strong style={{ fontSize: "0.85rem" }}>Mars — {target.title} Extent</strong>
            </div>
            <div style={{ display: "flex", gap: 6 }}>
              <button
                type="button"
                className={`btn ${marsZoomKm === 100 ? "btn-active" : ""}`}
                onClick={() => setMarsZoomKm(100)}
                style={{ padding: "3px 8px", fontSize: "0.74rem" }}
                title="100 km physical window"
              >
                <ZoomIn size={12} aria-hidden="true" /> 100 km
              </button>
              <button
                type="button"
                className={`btn ${marsZoomKm === 300 ? "btn-active" : ""}`}
                onClick={() => setMarsZoomKm(300)}
                style={{ padding: "3px 8px", fontSize: "0.74rem" }}
                title="300 km regional context"
              >
                <ZoomOut size={12} aria-hidden="true" /> 300 km
              </button>
            </div>
          </div>

          <svg
            viewBox={`0 0 ${W} ${H}`}
            width="100%"
            role="img"
            aria-label={`Mars coordinate and extent map for ${target.title}`}
            style={{ display: "block", background: "#120c0a", borderRadius: 6, border: "1px solid var(--border)" }}
          >
            {/* SWIM +-60 deg coverage band */}
            <rect
              x={0}
              y={projectEq(60, -180, W, H)[1]}
              width={W}
              height={projectEq(-60, -180, W, H)[1] - projectEq(60, -180, W, H)[1]}
              fill="rgba(245, 158, 11, 0.05)"
            />
            {[-60, -30, 0, 30, 60].map((lat) => {
              const [, y] = projectEq(lat, 0, W, H);
              return (
                <g key={`mlat-${lat}`}>
                  <line x1={0} y1={y} x2={W} y2={y} stroke="#2c1d18" strokeDasharray={lat === 0 ? undefined : "3 3"} />
                  <text x={4} y={y - 3} fill="#a88b7d" fontSize="9" fontFamily="monospace">
                    {lat}°
                  </text>
                </g>
              );
            })}
            {[-120, -60, 0, 60, 120].map((lon) => {
              const [x] = projectEq(0, lon, W, H);
              return <line key={`mlon-${lon}`} x1={x} y1={0} x2={x} y2={H} stroke="#2c1d18" strokeDasharray="3 3" />;
            })}

            {/* Target window footprint */}
            <rect
              x={mx - (marsHalfLonDeg / 360) * W}
              y={my - (marsHalfLatDeg / 180) * H}
              width={Math.max(10, ((2 * marsHalfLonDeg) / 360) * W)}
              height={Math.max(10, ((2 * marsHalfLatDeg) / 180) * H)}
              fill="rgba(245, 158, 11, 0.2)"
              stroke="#f59e0b"
              strokeWidth={1.8}
            />
            <circle cx={mx} cy={my} r={5} fill="#f59e0b" stroke="#fff" strokeWidth={1.4} />
            <text x={mx + 9} y={my + 3} fill="#fbbf24" fontSize="10" fontWeight="bold" fontFamily="monospace">
              {target.id.toUpperCase()} ({mLat.toFixed(2)}°, {mLon.toFixed(2)}°)
            </text>

            {/* Explicit no-basemap notice */}
            <rect x={10} y={H - 30} width={W - 20} height={22} rx={4} fill="rgba(15, 23, 42, 0.88)" stroke="#475569" />
            <text x={20} y={H - 15} fill="#cbd5e1" fontSize="9.5" fontFamily="monospace">
              No Mars raster basemap loaded — coordinate & extent view only (R_mars = 3,396 km · Δlat = {marsWindowLatDeg.toFixed(2)}° / {marsZoomKm} km)
            </text>
          </svg>

          <div style={{ marginTop: 8, fontSize: "0.74rem", color: "var(--text-muted)", display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: 6 }}>
            <span>
              <Info size={12} style={{ verticalAlign: "text-bottom", marginRight: 4 }} />
              CRS: IAU2000 planetocentric · SWIM 2.0 valid ±60° · Montabone Dust 3° native
            </span>
            <span className="mono">Layer: MOLA MEGDR 16 px/deg</span>
          </div>
        </div>
      </div>

      {showFigures && (
        <div
          style={{
            marginTop: 14,
            paddingTop: 12,
            borderTop: "1px solid var(--border)",
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
            gap: 12,
          }}
        >
          {[
            {
              src: "/figures/candidate_map.png",
              title: "Global Candidate Screening Map",
              caption: "outputs/analysis/figures/candidate_map.png (ETOPO 2022 4 km windows)",
            },
            {
              src: `/figures/${target.id}_terrain_comparison.png`,
              title: `${target.title} — Earth vs. Mars Terrain Metric Distributions`,
              caption: `outputs/analysis/figures/${target.id}_terrain_comparison.png (Slope & local relief)`,
            },
          ].map((fig) => (
            <figure
              key={fig.src}
              style={{
                margin: 0,
                padding: 10,
                borderRadius: 8,
                border: "1px solid var(--border)",
                background: "var(--bg-subtle)",
              }}
            >
              <img
                src={fig.src}
                alt={fig.title}
                style={{ width: "100%", height: "auto", borderRadius: 4, display: "block" }}
              />
              <figcaption style={{ marginTop: 6, fontSize: "0.75rem", color: "var(--text-secondary)" }}>
                <strong>{fig.title}</strong>
                <div className="mono" style={{ fontSize: "0.7rem", color: "var(--text-muted)" }}>
                  {fig.caption}
                </div>
              </figcaption>
            </figure>
          ))}
        </div>
      )}
    </section>
  );
}

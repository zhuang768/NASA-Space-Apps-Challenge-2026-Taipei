import React, { useMemo, useState } from "react";
import { AlertCircle, BarChart3, CheckCircle2, HelpCircle } from "lucide-react";
import {
  MARS_MISSING_REQUIREMENTS,
  SCALE10KM_COUNTS,
  SENSITIVITY,
} from "../data/adapter";
import type { CandidateItem, TargetBundle } from "../types/workbench";

interface RobustnessPanelProps {
  target: TargetBundle;
  selectedCandidate: CandidateItem | null;
}

type ConfigKey = "base_4km" | "scale_10km" | "slope_emphasis" | "relief_emphasis";

interface ConfigOption {
  key: ConfigKey;
  label: string;
  weights: string;
  spacing: string;
}

const CONFIG_OPTIONS: ConfigOption[] = [
  {
    key: "base_4km",
    label: "Base (4 km)",
    weights: "0.25 / 0.25 / 0.50",
    spacing: "4 km (2,611 valid windows)",
  },
  {
    key: "scale_10km",
    label: "Coarser Scale (10 km)",
    weights: "0.25 / 0.25 / 0.50",
    spacing: `10 km (${SCALE10KM_COUNTS.valid_windows ?? 2601} valid windows)`,
  },
  {
    key: "slope_emphasis",
    label: "Slope Emphasis",
    weights: "0.40 / 0.40 / 0.20",
    spacing: "4 km (2,611 valid windows)",
  },
  {
    key: "relief_emphasis",
    label: "Relief Emphasis",
    weights: "0.10 / 0.10 / 0.80",
    spacing: "4 km (2,611 valid windows)",
  },
];

interface Top2Entry {
  lat: number;
  lon: number;
  D: number | null;
}

function normalizeTupleList(
  tuples: [number, number][] | undefined,
  lookup?: { lat: number; lon: number; terrain_distance: number }[]
): Top2Entry[] {
  if (!Array.isArray(tuples)) return [];
  return tuples.map(([lat, lon]) => {
    const match = lookup?.find(
      (c) => Math.abs(c.lat - lat) < 0.05 && Math.abs(c.lon - lon) < 0.05
    );
    return {
      lat,
      lon,
      D: match ? match.terrain_distance : null,
    };
  });
}

export const RobustnessPanel: React.FC<RobustnessPanelProps> = ({
  target,
  selectedCandidate,
}) => {
  const [activeConfig, setActiveConfig] = useState<ConfigKey>("base_4km");
  const sens = SENSITIVITY[target.id];

  const configData = useMemo(() => {
    if (!sens) return null;

    const baseTop2 = normalizeTupleList(sens.base_4km_top2, target.candidates);
    const alt10kmTop2 = normalizeTupleList(
      sens.alternative_10km_top2,
      target.candidates_10km_top2
    );
    const slopeTop2 = normalizeTupleList(
      sens.weight_variants?.slope_emphasis?.separated_top2
    );
    const reliefTop2 = normalizeTupleList(
      sens.weight_variants?.relief_emphasis?.separated_top2
    );

    const byKey: Record<
      ConfigKey,
      { entries: Top2Entry[]; overlapWithBase: number; denom: number }
    > = {
      base_4km: { entries: baseTop2, overlapWithBase: baseTop2.length, denom: 2 },
      scale_10km: {
        entries: alt10kmTop2,
        overlapWithBase: sens.top2_overlap_count ?? 0,
        denom: 2,
      },
      slope_emphasis: {
        entries: slopeTop2,
        overlapWithBase: sens.weight_variants?.slope_emphasis?.top2_overlap_count ?? 0,
        denom: 2,
      },
      relief_emphasis: {
        entries: reliefTop2,
        overlapWithBase: sens.weight_variants?.relief_emphasis?.top2_overlap_count ?? 0,
        denom: 2,
      },
    };

    // Compute Top-2 frequency across the 4 tested configurations by rounded (lat, lon)
    const freqMap = new Map<
      string,
      { lat: number; lon: number; count: number; configs: string[] }
    >();
    const allConfigs: { name: string; list: Top2Entry[] }[] = [
      { name: "Base 4 km", list: baseTop2 },
      { name: "10 km", list: alt10kmTop2 },
      { name: "Slope", list: slopeTop2 },
      { name: "Relief", list: reliefTop2 },
    ];

    for (const cfg of allConfigs) {
      const seenInCfg = new Set<string>();
      for (const item of cfg.list) {
        const key = `${item.lat.toFixed(2)},${item.lon.toFixed(2)}`;
        if (seenInCfg.has(key)) continue;
        seenInCfg.add(key);
        const existing = freqMap.get(key);
        if (existing) {
          existing.count += 1;
          existing.configs.push(cfg.name);
        } else {
          freqMap.set(key, {
            lat: item.lat,
            lon: item.lon,
            count: 1,
            configs: [cfg.name],
          });
        }
      }
    }

    const frequencies = Array.from(freqMap.values()).sort((a, b) => b.count - a.count);

    return { byKey, frequencies };
  }, [sens, target.candidates, target.candidates_10km_top2]);

  return (
    <section className="panel robustness-panel" aria-label="Robustness and Data Gaps">
      <div className="panel-header">
        <div>
          <h2 className="panel-title">Sensitivity, Robustness &amp; Verification Gaps</h2>
          <p className="panel-subtitle">
            Pre-computed sensitivity runs for <strong>{target.title}</strong> across 4
            configurations (no synthetic re-ranking).
          </p>
        </div>
      </div>

      {!sens || !configData ? (
        <div className="empty-state">
          <AlertCircle size={22} aria-hidden="true" />
          <p>Analysis not available for this target.</p>
        </div>
      ) : (
        <div className="robustness-grid">
          <div className="robustness-col">
            <div className="subpanel-header">
              <h3>
                <BarChart3 size={15} aria-hidden="true" /> Tested Configurations (n = 4)
              </h3>
              <span className="muted-note">Select a real run to inspect its Top-2 rankings</span>
            </div>

            <div className="config-tabs" role="tablist" aria-label="Sensitivity configurations">
              {CONFIG_OPTIONS.map((opt) => (
                <button
                  key={opt.key}
                  type="button"
                  role="tab"
                  aria-selected={activeConfig === opt.key}
                  className={`config-tab ${activeConfig === opt.key ? "active" : ""}`}
                  onClick={() => setActiveConfig(opt.key)}
                >
                  <span className="config-name">{opt.label}</span>
                  <span className="config-meta">{opt.weights}</span>
                </button>
              ))}
            </div>

            <div className="config-detail-card">
              <div className="config-detail-meta">
                <span>
                  Spacing:{" "}
                  <strong>
                    {CONFIG_OPTIONS.find((c) => c.key === activeConfig)?.spacing}
                  </strong>
                </span>
                <span>
                  Overlap with Base 4 km Top-2:{" "}
                  <strong>
                    {configData.byKey[activeConfig].overlapWithBase} /{" "}
                    {configData.byKey[activeConfig].denom}
                  </strong>
                </span>
              </div>

              <table className="mini-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Center (Lat, Lon)</th>
                    <th>Distance D</th>
                    <th>Matches Selected?</th>
                  </tr>
                </thead>
                <tbody>
                  {configData.byKey[activeConfig].entries.map((entry, idx) => {
                    const isSelected =
                      selectedCandidate &&
                      Math.abs(selectedCandidate.lat - entry.lat) < 0.05 &&
                      Math.abs(selectedCandidate.lon - entry.lon) < 0.05;
                    return (
                      <tr key={idx} className={isSelected ? "row-highlight" : ""}>
                        <td>#{idx + 1}</td>
                        <td className="mono">
                          {entry.lat.toFixed(2)}°, {entry.lon.toFixed(2)}°
                        </td>
                        <td className="mono">
                          {entry.D !== null ? entry.D.toFixed(3) : "—"}
                        </td>
                        <td>
                          {isSelected ? (
                            <span className="badge badge-cyan">
                              <CheckCircle2 size={11} aria-hidden="true" /> Selected
                            </span>
                          ) : (
                            <span className="muted-text">—</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>

              {selectedCandidate?.sensitivity_raw_ranks && (
                <div className="candidate-rank-shifts">
                  <strong>
                    Selected Candidate ({selectedCandidate.candidate_id}) Weight Ranks:
                  </strong>{" "}
                  Base #{selectedCandidate.rank} · Slope emphasis #
                  {selectedCandidate.sensitivity_raw_ranks.slope_emphasis ?? "N/A"} · Relief
                  emphasis #{selectedCandidate.sensitivity_raw_ranks.relief_emphasis ?? "N/A"}
                </div>
              )}

              <p className="interpretation-note">
                <strong>Sensitivity driver:</strong> {sens.interpretation}
              </p>
            </div>
          </div>

          <div className="robustness-col">
            <div className="subpanel-header">
              <h3>Top-2 Frequency Across 4 Configurations</h3>
              <span className="badge badge-amber">Not probability or confidence</span>
            </div>

            <table className="mini-table">
              <thead>
                <tr>
                  <th>Site (Lat, Lon)</th>
                  <th>Top-2 Frequency</th>
                  <th>Configurations</th>
                </tr>
              </thead>
              <tbody>
                {configData.frequencies.map((freq, idx) => (
                  <tr key={idx}>
                    <td className="mono">
                      {freq.lat.toFixed(2)}°, {freq.lon.toFixed(2)}°
                    </td>
                    <td>
                      <div className="freq-bar-wrap">
                        <span className="mono">{freq.count}/4</span>
                        <div className="freq-bar">
                          <div
                            className="freq-bar-fill"
                            style={{ width: `${(freq.count / 4) * 100}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="muted-text">{freq.configs.join(", ")}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="gaps-card">
              <h3>
                <HelpCircle size={15} aria-hidden="true" /> Prioritized Unknowns &amp; Verification
                Gaps
              </h3>
              <ul>
                <li>
                  <strong>P1 — Field &amp; Orbital Climate Coverage:</strong> NASA POWER context
                  only retrieved for Top-2 sites per target; Ranks #3–#12 remain unretrieved.
                </li>
                <li>
                  <strong>P2 — Mars Thermal &amp; Dust Gaps:</strong>{" "}
                  {MARS_MISSING_REQUIREMENTS.slice(0, 2).join(" ")}
                </li>
                <li>
                  <strong>P3 — Scale &amp; Weight Instability:</strong> Top-2 overlap drops to{" "}
                  {sens.top2_overlap_count ?? 0}/2 at 10 km spacing and{" "}
                  {sens.weight_variants?.relief_emphasis?.top2_overlap_count ?? 0}/2 under
                  relief emphasis.
                </li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

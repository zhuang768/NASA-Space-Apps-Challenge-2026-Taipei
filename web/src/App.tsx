import { useMemo, useState } from "react";
import {
  buildComparisonRows,
  getTargetBundle,
  getTargetIds,
} from "./data/adapter";
import type {
  CandidateItem,
  ComparisonRow,
  TargetBundle,
  TargetId,
} from "./types/workbench";
import { TargetMissionBar } from "./components/TargetMissionBar";
import { DualSideMap } from "./components/DualSideMap";
import { CandidateList } from "./components/CandidateList";
import { ComparisonPanel } from "./components/ComparisonPanel";
import { EvidenceDrawer } from "./components/EvidenceDrawer";
import { RobustnessPanel } from "./components/RobustnessPanel";

type MobileTab = "all" | "maps" | "candidates" | "comparison" | "robustness";

function buildDemoTargetBundle(base: TargetBundle): TargetBundle {
  const demoCandidate: CandidateItem = {
    candidate_id: `DEMO-${base.id.toUpperCase()}-01`,
    mars_target: base.id,
    rank: 1,
    lat: 24.5,
    lon: -68.2,
    land_fraction: 1.0,
    slope_median_deg: 2.1,
    slope_p90_deg: 7.4,
    relief_m: 310,
    terrain_distance: 0.142,
    status: "demo_preview",
    temperature_status: "not_checked",
    water_ice_status: "not_checked",
    air_status: "not_checked",
    logistics_status: "not_checked",
    prior_analog_literature_status: "unverified",
    footprint: [
      [-68.7, 24.0],
      [-67.7, 24.0],
      [-67.7, 25.0],
      [-68.7, 25.0],
    ],
    evidenceCompleteness: {
      scoredDomains: 1,
      totalDomains: 4,
      label: "1/4 scored (DEMO)",
    },
    keySupport: "Synthetic demo candidate — NOT scientific output",
    mainGap: "DEMO DATA — Not scientific results",
    classification: "Project-proposed",
  };
  return {
    ...base,
    candidates: [demoCandidate],
  };
}

export function App() {
  const targetIds = useMemo(() => getTargetIds(), []);
  const [activeTargetId, setActiveTargetId] = useState<TargetId>(
    targetIds[0] ?? "jezero"
  );
  const [demoMode, setDemoMode] = useState(false);
  const [mobileTab, setMobileTab] = useState<MobileTab>("all");

  const realBundle = useMemo(
    () => getTargetBundle(activeTargetId),
    [activeTargetId]
  );

  const activeBundle = useMemo(() => {
    if (!realBundle) return null;
    return demoMode ? buildDemoTargetBundle(realBundle) : realBundle;
  }, [realBundle, demoMode]);

  const [selectedCandidateId, setSelectedCandidateId] = useState<string | null>(
    () => realBundle?.candidates[0]?.candidate_id ?? null
  );
  const [inspectedRowId, setInspectedRowId] = useState<string | null>(null);

  const selectedCandidate = useMemo(() => {
    if (!activeBundle || activeBundle.candidates.length === 0) return null;
    return (
      activeBundle.candidates.find(
        (c) => c.candidate_id === selectedCandidateId
      ) ?? activeBundle.candidates[0]
    );
  }, [activeBundle, selectedCandidateId]);

  const comparisonRows = useMemo(() => {
    if (!activeBundle) return [];
    return buildComparisonRows(activeBundle, selectedCandidate);
  }, [activeBundle, selectedCandidate]);

  const inspectedRow: ComparisonRow | null = useMemo(() => {
    if (!inspectedRowId) return null;
    return comparisonRows.find((r) => r.id === inspectedRowId) ?? null;
  }, [comparisonRows, inspectedRowId]);

  const handleSelectTarget = (nextId: TargetId) => {
    setActiveTargetId(nextId);
    // Clear previous target's candidate selection & open evidence drawer immediately
    setInspectedRowId(null);
    const nextBundle = getTargetBundle(nextId);
    const firstId = nextBundle?.candidates[0]?.candidate_id ?? null;
    setSelectedCandidateId(demoMode ? `DEMO-${nextId.toUpperCase()}-01` : firstId);
  };

  const handleToggleDemoMode = () => {
    const nextDemo = !demoMode;
    setDemoMode(nextDemo);
    setInspectedRowId(null);
    if (nextDemo) {
      setSelectedCandidateId(`DEMO-${activeTargetId.toUpperCase()}-01`);
    } else {
      setSelectedCandidateId(realBundle?.candidates[0]?.candidate_id ?? null);
    }
  };

  const handleSelectCandidate = (candidate: CandidateItem) => {
    setSelectedCandidateId(candidate.candidate_id);
  };

  const showSection = (section: Exclude<MobileTab, "all">) =>
    mobileTab === "all" || mobileTab === section;

  return (
    <div className="app-shell">
      <TargetMissionBar
        targetIds={targetIds}
        activeTargetId={activeTargetId}
        target={activeBundle}
        demoMode={demoMode}
        onSelectTarget={handleSelectTarget}
        onToggleDemoMode={handleToggleDemoMode}
      />

      {!activeBundle ? (
        <main className="panel" role="main">
          <h2 className="panel-title">No Target Results Available</h2>
          <p style={{ color: "var(--text-muted)", marginBottom: 0 }}>
            No verified output bundle was found for target{" "}
            <span className="mono">{activeTargetId}</span>. Previous target state
            has been cleared.
          </p>
        </main>
      ) : (
        <>
          <nav className="mobile-tabs" aria-label="Narrow viewport sections">
            {(
              [
                ["all", "All Panels"],
                ["maps", "Maps"],
                ["candidates", "Candidates"],
                ["comparison", "Comparison"],
                ["robustness", "Robustness"],
              ] as [MobileTab, string][]
            ).map(([tab, label]) => (
              <button
                key={tab}
                type="button"
                className={`btn ${mobileTab === tab ? "btn-active" : ""}`}
                onClick={() => setMobileTab(tab)}
              >
                {label}
              </button>
            ))}
          </nav>

          <div className="workbench-grid">
            {showSection("candidates") && (
              <CandidateList
                candidates={activeBundle.candidates}
                selectedCandidate={selectedCandidate}
                onSelectCandidate={handleSelectCandidate}
              />
            )}

            <main className="main-column">
              {showSection("maps") && (
                <DualSideMap
                  target={activeBundle}
                  selectedCandidate={selectedCandidate}
                  onSelectCandidate={handleSelectCandidate}
                />
              )}

              {showSection("comparison") && (
                <ComparisonPanel
                  target={activeBundle}
                  candidate={selectedCandidate}
                  rows={comparisonRows}
                  onInspectEvidence={(row) => setInspectedRowId(row.id)}
                />
              )}

              {showSection("robustness") && (
                <RobustnessPanel
                  target={activeBundle}
                  selectedCandidate={selectedCandidate}
                />
              )}
            </main>
          </div>
        </>
      )}

      <EvidenceDrawer
        row={inspectedRow}
        onClose={() => setInspectedRowId(null)}
      />
    </div>
  );
}

export default App;

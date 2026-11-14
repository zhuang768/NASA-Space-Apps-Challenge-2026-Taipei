import { useMemo, useState } from "react";
import {
  buildComparisonRows,
  getMarsDiscovery,
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
import { MarsDiscoveryPanel } from "./components/MarsDiscoveryPanel";

type WorkspaceMode = "discovery" | "workbench";
type MobileTab = "maps" | "comparison" | "robustness";

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
  const discovery = useMemo(() => getMarsDiscovery(), []);
  const targetIds = useMemo(() => getTargetIds(), []);
  const [workspaceMode, setWorkspaceMode] = useState<WorkspaceMode>(
    discovery ? "discovery" : "workbench"
  );
  const [discoveryId, setDiscoveryId] = useState(
    () => discovery?.cards[0]?.id ?? "I-01"
  );
  const [activeTargetId, setActiveTargetId] = useState<TargetId>(
    targetIds[0] ?? "jezero"
  );
  const [demoMode, setDemoMode] = useState(false);
  const [mobileTab, setMobileTab] = useState<MobileTab>("maps");

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
    setInspectedRowId(null);
  };

  const showSection = (section: MobileTab) => mobileTab === section;

  return (
    <div className="app-shell">
      <nav className="workspace-mode-nav" aria-label="Workspace mode">
        <button
          type="button"
          className={`btn ${workspaceMode === "discovery" ? "btn-active" : ""}`}
          aria-pressed={workspaceMode === "discovery"}
          onClick={() => setWorkspaceMode("discovery")}
          disabled={!discovery}
        >
          Mars research candidates
        </button>
        {targetIds.length > 0 && (
          <button
            type="button"
            className={`btn ${workspaceMode === "workbench" ? "btn-active" : ""}`}
            aria-pressed={workspaceMode === "workbench"}
            onClick={() => setWorkspaceMode("workbench")}
          >
            Earth analog search
          </button>
        )}
      </nav>

      {workspaceMode === "discovery" && discovery ? (
        <>
          <header className="panel" aria-label="Mars discovery header">
            <div className="panel-header" style={{ marginBottom: 0 }}>
              <div>
                <h1 style={{ margin: 0, fontSize: "1.2rem", fontWeight: 700 }}>
                  TerraMatch · Mars Site Discovery
                </h1>
                <p className="header-description">
                  Explore provisional Mars locations by research purpose. Select a candidate for its map, evidence and open questions.
                </p>
              </div>
              <span className="badge badge-amber">Novelty unchecked</span>
            </div>
          </header>
          <MarsDiscoveryPanel
            discovery={discovery}
            selectedId={discoveryId}
            onSelectId={setDiscoveryId}
          />
        </>
      ) : (
        <>
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
              <section className="reading-guide" aria-label="How to use this workbench">
                <div>
                  <span className="eyebrow">Research workflow</span>
                  <h2>Find a region. Understand the evidence.</h2>
                  <p>
                    Choose a Mars target and an Earth region. Open evidence when you need the details.
                  </p>
                </div>
                <span className="scope-note">Terrain ranked · 3 other themes unscored</span>
              </section>
              <nav className="workspace-nav" aria-label="Analysis views">
                {(
                  [
                    ["maps", "Overview & map"],
                    ["comparison", "Evidence & sources"],
                    ["robustness", "Sensitivity & gaps"],
                  ] as [MobileTab, string][]
                ).map(([tab, label]) => (
                  <button
                    key={tab}
                    type="button"
                    className={`btn ${mobileTab === tab ? "btn-active" : ""}`}
                    aria-pressed={mobileTab === tab}
                    onClick={() => setMobileTab(tab)}
                  >
                    {label}
                  </button>
                ))}
              </nav>

              <div className="workbench-grid">
                <CandidateList
                  candidates={activeBundle.candidates}
                  selectedCandidate={selectedCandidate}
                  onSelectCandidate={handleSelectCandidate}
                />

                <main className="main-column" id="analysis-content">
                  <section
                    className="panel selection-summary"
                    aria-label="Selected candidate summary"
                  >
                    <div className="selection-heading">
                      <div>
                        <span className="eyebrow">Selected Earth region</span>
                        <h2>{selectedCandidate?.candidate_id ?? "No candidate selected"}</h2>
                        <p className="mono">
                          {selectedCandidate
                            ? `${selectedCandidate.lat.toFixed(2)}°, ${selectedCandidate.lon.toFixed(2)}° · terrain rank #${selectedCandidate.rank}`
                            : "Select an available candidate to continue."}
                        </p>
                      </div>
                      {selectedCandidate && mobileTab !== "maps" && (
                        <div className="distance-readout">
                          <span className="mono">
                            {selectedCandidate.terrain_distance.toFixed(4)}
                          </span>
                          <small>Terrain distance · lower is closer</small>
                        </div>
                      )}
                    </div>
                    {selectedCandidate && (
                      <div className="selection-findings">
                        <div>
                          <h3>What supports this match</h3>
                          <p>{mobileTab === "maps" ? "Ranked using regional slope and relief statistics. Other themes do not contribute to this ranking." : selectedCandidate.keySupport}</p>
                        </div>
                        <div>
                          <h3>What remains unresolved</h3>
                          <p>{selectedCandidate.mainGap}</p>
                        </div>
                      </div>
                    )}
                    <p className="summary-limit">
                      {demoMode
                        ? "Synthetic preview only. Return to real results before interpreting any values."
                        : "A regional terrain candidate, not a validated complete Mars analog or landing-safety assessment."}
                    </p>
                    {mobileTab === "maps" && selectedCandidate && (
                      <button className="btn" onClick={() => setMobileTab("comparison")}>
                        Inspect evidence and sources →
                      </button>
                    )}
                  </section>
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

          <EvidenceDrawer row={inspectedRow} onClose={() => setInspectedRowId(null)} />
        </>
      )}
    </div>
  );
}

export default App;

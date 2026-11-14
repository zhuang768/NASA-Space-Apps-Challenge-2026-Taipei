import React, { useEffect, useRef } from "react";
import { ExternalLink, FileCode2, ShieldCheck, X } from "lucide-react";
import type { ComparisonRow } from "../types/workbench";

interface EvidenceDrawerProps {
  row: ComparisonRow | null;
  onClose: () => void;
}

export const EvidenceDrawer: React.FC<EvidenceDrawerProps> = ({ row, onClose }) => {
  const closeBtnRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!row) return;
    closeBtnRef.current?.focus();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [row, onClose]);

  if (!row) return null;

  const { evidence } = row;
  // A row may cite several sources joined with " | "; render each http(s) URL as its own link.
  const sourceParts = (evidence.sourceUrl || "").split(" | ").map((s) => s.trim()).filter(Boolean);
  const isHttp = (s: string) => s.startsWith("http://") || s.startsWith("https://");
  const hasValidUrl = sourceParts.length > 0 && sourceParts.every(isHttp);

  return (
    <div
      className="drawer-backdrop"
      role="presentation"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <aside
        className="evidence-drawer"
        role="dialog"
        aria-modal="true"
        aria-labelledby="evidence-drawer-title"
      >
        <div className="drawer-header">
          <div>
            <span className="badge badge-cyan">{evidence.domain}</span>
            <h2 id="evidence-drawer-title" className="drawer-title">
              {evidence.title}
            </h2>
          </div>
          <button
            ref={closeBtnRef}
            type="button"
            className="btn-icon"
            onClick={onClose}
            aria-label="Close evidence drawer"
          >
            <X size={18} aria-hidden="true" />
          </button>
        </div>

        <div className="drawer-body">
          <div className="drawer-summary-grid">
            <div className="summary-box">
              <span className="summary-label">Earth Observation</span>
              <p>{evidence.earthSummary}</p>
            </div>
            <div className="summary-box">
              <span className="summary-label">Mars Reference</span>
              <p>{evidence.marsSummary}</p>
            </div>
          </div>

          <dl className="evidence-dl">
            <div className="dl-row">
              <dt>Source URL</dt>
              <dd>
                {hasValidUrl ? (
                  sourceParts.map((url) => (
                    <div key={url}>
                      <a href={url} target="_blank" rel="noreferrer" className="external-link">
                        {url} <ExternalLink size={12} aria-hidden="true" />
                      </a>
                    </div>
                  ))
                ) : (
                  <span className="untraced">{evidence.sourceUrl || "Unverified / Not traced"}</span>
                )}
              </dd>
            </div>
            <div className="dl-row">
              <dt>Product ID</dt>
              <dd>{evidence.productId}</dd>
            </div>
            <div className="dl-row">
              <dt>Version</dt>
              <dd>{evidence.version}</dd>
            </div>
            <div className="dl-row">
              <dt>Period</dt>
              <dd>{evidence.period}</dd>
            </div>
            <div className="dl-row">
              <dt>Units</dt>
              <dd>{evidence.units}</dd>
            </div>
            <div className="dl-row">
              <dt>Native Resolution</dt>
              <dd>{evidence.nativeResolution}</dd>
            </div>
            <div className="dl-row">
              <dt>Analysis Scale</dt>
              <dd>{evidence.analysisScale}</dd>
            </div>
            <div className="dl-row">
              <dt>Processing Method</dt>
              <dd>{evidence.processingMethod}</dd>
            </div>
            <div className="dl-row">
              <dt>QA &amp; Sample Coverage</dt>
              <dd>{evidence.qaAndCoverage}</dd>
            </div>
            <div className="dl-row">
              <dt>Measurement Kind</dt>
              <dd>{evidence.measurementKind}</dd>
            </div>
            <div className="dl-row">
              <dt>Local Source File</dt>
              <dd className="mono">
                <FileCode2 size={13} aria-hidden="true" /> {evidence.localFile}
              </dd>
            </div>
            <div className="dl-row">
              <dt>SHA-256 Checksum</dt>
              <dd className="mono break-all">
                <ShieldCheck size={13} aria-hidden="true" /> {evidence.checksumSha256}
              </dd>
            </div>
          </dl>

          <div className="limitations-box">
            <h3>Limitations &amp; Verification Needs</h3>
            <ul>
              {evidence.limitations.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      </aside>
    </div>
  );
};

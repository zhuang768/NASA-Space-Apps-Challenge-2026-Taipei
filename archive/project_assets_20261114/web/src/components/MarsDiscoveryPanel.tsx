import { AlertTriangle, ExternalLink, MapPinned } from "lucide-react";
import type { MarsDiscoveryBundle, MarsDiscoveryCard } from "../types/workbench";

interface Props {
  discovery: MarsDiscoveryBundle;
  selectedId: string;
  onSelectId: (id: string) => void;
}

function fmtLatLon(lat: number, lon: number): string {
  const latHem = lat >= 0 ? "N" : "S";
  const lonHem = lon >= 0 ? "E" : "W";
  return `${Math.abs(lat).toFixed(2)}°${latHem}, ${Math.abs(lon).toFixed(2)}°${lonHem}`;
}

function roleLabel(role: string): string {
  if (role === "shallow_ice_research_candidate") return "淺冰研究候選";
  if (role === "dust_terrain_context_reference") return "沙塵／地形對照參考";
  return role;
}

function noveltyLabel(status: string): string {
  if (status === "unchecked_exact_site") return "新穎性尚未確認";
  return status;
}

function Unknown({ children = "未知" }: { children?: string }) {
  return <span className="discovery-unknown">{children}</span>;
}

function ThemeCell({
  label,
  status,
  value,
}: {
  label: string;
  status: string;
  value: string | null;
}) {
  return (
    <div className="discovery-theme-cell">
      <span className="eyebrow">{label}</span>
      {value === null || status === "unknown" ? (
        <Unknown />
      ) : (
        <p className="mono">{value}</p>
      )}
      {status === "partial" && <small>部分資料 · 其餘未知</small>}
    </div>
  );
}

function CardDetail({
  card,
  discovery,
}: {
  card: MarsDiscoveryCard;
  discovery: MarsDiscoveryBundle;
}) {
  const layers = card.layers;
  const themes = card.themes;
  const figureSrc = `/${card.map_figure.replace(/^figures\//, "figures/")}`;

  return (
    <article className="discovery-detail" aria-labelledby={`discovery-${card.id}`}>
      <div className="discovery-detail-header">
        <div>
          <span className="eyebrow">Mars reference · {card.id}</span>
          <h2 id={`discovery-${card.id}`}>{fmtLatLon(card.lat, card.lon)}</h2>
          <p className="mono">
            {card.lat.toFixed(2)}°, {card.lon.toFixed(2)}° · {roleLabel(card.role)}
          </p>
        </div>
        <div className="discovery-badges">
          <span className="badge badge-amber">{noveltyLabel(card.novelty_status)}</span>
          <span className="badge badge-neutral">Earth analog: 未知</span>
          <span className="badge badge-rose">分數 ≠ 信心／登陸批准</span>
        </div>
      </div>

      <div className="discovery-findings">
        <div>
          <h3>研究用途</h3>
          <p>{card.intended_use}</p>
          <p className="summary-limit">{card.treatment}</p>
        </div>
        <div>
          <h3>缺點與限制</h3>
          <p>{card.weaknesses}</p>
          <p className="summary-limit">下一步：{card.next_checks}</p>
        </div>
      </div>

      <section aria-label="Four themes for this reference">
        <h3 className="panel-title" style={{ marginBottom: 10 }}>
          四大面向（實驗性描述指標）
        </h3>
        <div className="discovery-theme-grid">
          <ThemeCell
            label="Terrain"
            status={themes.terrain.status}
            value={`slope ${themes.terrain.slope_deg.toFixed(2)}° · relief ${Math.round(themes.terrain.relief_m)} m`}
          />
          <ThemeCell
            label="Temperature"
            status={themes.temperature.status}
            value={`TI ${themes.temperature.thermal_inertia.toFixed(0)} · 區域地表溫：未知`}
          />
          <ThemeCell
            label="Water/Ice"
            status={themes.water_ice.status}
            value={`SWIM 0–1 m consistency ${themes.water_ice.ice_shallow.toFixed(3)}（非含冰量％）`}
          />
          <ThemeCell
            label="Air/Dust"
            status={themes.atmosphere_dust.status}
            value={`MY35 CDOD ${themes.atmosphere_dust.dust_cdod_my35.toFixed(3)}`}
          />
        </div>
      </section>

      <section className="discovery-metrics" aria-label="Layer values">
        <h3 className="panel-title">資料數值（0.5° stack）</h3>
        <dl className="discovery-metric-list">
          <div>
            <dt>Descriptor score</dt>
            <dd className="mono">{card.descriptor_score.toFixed(4)}</dd>
          </div>
          <div>
            <dt>Slope</dt>
            <dd className="mono">{layers.slope.toFixed(3)}°</dd>
          </div>
          <div>
            <dt>Relief</dt>
            <dd className="mono">{Math.round(layers.relief)} m</dd>
          </div>
          <div>
            <dt>Thermal inertia</dt>
            <dd className="mono">{layers.thermal_inertia.toFixed(1)}</dd>
          </div>
          <div>
            <dt>Ice shallow (SWIM)</dt>
            <dd className="mono">{layers.ice_shallow.toFixed(4)}</dd>
          </div>
          <div>
            <dt>Dust CDOD MY35</dt>
            <dd className="mono">{layers.dust_cdod.toFixed(4)}</dd>
          </div>
          <div>
            <dt>區域地表溫度</dt>
            <dd>
              <Unknown />
            </dd>
          </div>
          <div>
            <dt>Earth 類比配對</dt>
            <dd>
              <Unknown>尚未完成</Unknown>
            </dd>
          </div>
        </dl>
        <p className="summary-limit">
          此分數僅為實驗性描述指標，不是信心、成功率或登陸批准。「堅固地面／可承載」用途已暫停宣稱。
        </p>
      </section>

      <section aria-label="Sources and map">
        <h3 className="panel-title">來源與地圖</h3>
        <ul className="discovery-source-list">
          {card.sources.map((sid) => {
            const src = discovery.source_index[sid];
            if (!src) {
              return (
                <li key={sid}>
                  <span className="mono">{sid}</span> — <Unknown />
                </li>
              );
            }
            return (
              <li key={sid}>
                <a href={src.url} target="_blank" rel="noopener noreferrer">
                  <span className="mono">{sid}</span> {src.label}{" "}
                  <ExternalLink size={12} aria-hidden="true" />
                </a>
              </li>
            );
          })}
        </ul>
        <figure className="discovery-figure">
          <img
            src={figureSrc}
            alt={`Map context for ${card.id} (${card.purpose_key})`}
            loading="lazy"
          />
          <figcaption className="mono">{card.map_figure}</figcaption>
        </figure>
      </section>

      <section aria-label="Prohibited claims">
        <h3 className="panel-title">禁止宣稱</h3>
        <ul className="discovery-prohibit-list">
          {card.prohibited_claims.map((claim) => (
            <li key={claim}>{claim}</li>
          ))}
        </ul>
      </section>
    </article>
  );
}

export function MarsDiscoveryPanel({ discovery, selectedId, onSelectId }: Props) {
  const selected =
    discovery.cards.find((c) => c.id === selectedId) ?? discovery.cards[0];

  return (
    <div className="discovery-layout">
      <aside className="panel discovery-list" aria-label="Mars discovery references">
        <div className="panel-header">
          <div>
            <h2 className="panel-title">Mars discovery references</h2>
            <p className="panel-subtitle">
              I-01 / I-02 淺冰 · D-03 / D-04 沙塵對照 · 非舊地球排名
            </p>
          </div>
        </div>

        <div className="guardrail-banner" role="note">
          <AlertTriangle size={16} aria-hidden="true" />
          <span>
            {discovery.novelty_policy}. Earth analog pairing:{" "}
            <strong>{discovery.earth_analog_pairing}</strong>. Firm-rocky claim:{" "}
            {discovery.firm_rocky_status}.
          </span>
        </div>

        <ul className="discovery-card-list">
          {discovery.cards.map((card: MarsDiscoveryCard) => {
            const active = card.id === selected.id;
            return (
              <li key={card.id}>
                <button
                  type="button"
                  className={`discovery-card-btn ${active ? "btn-active" : ""}`}
                  aria-pressed={active}
                  onClick={() => onSelectId(card.id)}
                >
                  <span className="discovery-card-id mono">{card.id}</span>
                  <span className="discovery-card-meta">
                    <MapPinned size={14} aria-hidden="true" />
                    {fmtLatLon(card.lat, card.lon)}
                  </span>
                  <span className="discovery-card-role">{roleLabel(card.role)}</span>
                  <span className="badge badge-amber">{noveltyLabel(card.novelty_status)}</span>
                </button>
              </li>
            );
          })}
        </ul>

        {discovery.limitations.length > 0 && (
          <details className="discovery-limits">
            <summary>Stack limitations</summary>
            <ul>
              {discovery.limitations.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </details>
        )}
      </aside>

      <main className="panel discovery-main" role="main">
        {selected ? (
          <CardDetail card={selected} discovery={discovery} />
        ) : (
          <p className="empty-state">No discovery cards available.</p>
        )}
      </main>
    </div>
  );
}

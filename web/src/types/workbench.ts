export type TargetId = "jezero" | "gale" | "arcadia";

export type TopicDomain = "Terrain" | "Temperature" | "Water/Ice" | "Air/Dust";

export type ComparabilityLevel =
  | "Direct"
  | "Modeled proxy"
  | "Contextual"
  | "Not comparable";

export type EvidenceStatus =
  | "Supported"
  | "Mismatch"
  | "Unknown"
  | "Provisional"
  | "Provisional observations"
  | "Failed quality checks"
  | "Analysis incomplete"
  | "Source access failed"
  | "Stale results"
  | "Missing data"
  | "Outside coverage"
  | "Not checked";

export interface SourceRecord {
  file?: string;
  url?: string;
  bytes?: number;
  sha256?: string;
  recorded_utc?: string;
  dataset?: string;
  product?: string;
  version?: string;
  units?: string;
  resolution?: string;
  crs?: string;
  vertical_datum?: string;
  period?: string;
  notes?: string;
  license?: string;
}

export interface EvidenceRecord {
  id: string;
  title: string;
  domain: TopicDomain;
  earthSummary: string;
  marsSummary: string;
  sourceUrl: string;
  productId: string;
  version: string;
  period: string;
  units: string;
  nativeResolution: string;
  analysisScale: string;
  processingMethod: string;
  qaAndCoverage: string;
  measurementKind: "Direct observation" | "Derived / Reanalysis" | "Model / Composite" | "Design assumption / Missing";
  limitations: string[];
  localFile: string;
  checksumSha256: string;
}

export interface ComparisonRow {
  id: string;
  domain: TopicDomain;
  metricName: string;
  earthValue: string;
  earthQuantity: string;
  marsValue: string;
  marsQuantity: string;
  periodAndSupport: string;
  methodAndThreshold: string;
  comparability: ComparabilityLevel;
  status: EvidenceStatus;
  sourcePortalLabel: string;
  evidence: EvidenceRecord;
}

export interface CandidateItem {
  candidate_id: string;
  mars_target: TargetId;
  rank: number;
  lat: number;
  lon: number;
  land_fraction: number;
  slope_median_deg: number;
  slope_p90_deg: number;
  relief_m: number;
  terrain_distance: number;
  sensitivity_raw_ranks?: {
    slope_emphasis?: number;
    relief_emphasis?: number;
  };
  status: string;
  temperature_status: string;
  water_ice_status: string;
  air_status: string;
  logistics_status: string;
  prior_analog_literature_status: string;
  footprint: [number, number][];
  earth_climate_context?: {
    status: string;
    summary?: Record<
      string,
      {
        value: number | null;
        valid_months: number;
        expected_months: number;
        unit: string;
        meaning: string;
      }
    >;
    source?: SourceRecord;
  };
  evidenceCompleteness: {
    scoredDomains: number;
    totalDomains: number;
    label: string;
  };
  keySupport: string;
  mainGap: string;
  classification: "Project-proposed" | "Established reference" | "Prior use unverified";
}

export interface TargetBundle {
  id: TargetId;
  title: string;
  researchQuestion: string;
  summary: {
    lat: number;
    lon: number;
    label: string;
    coordinate_source: string;
    slope_median_deg: number;
    slope_p90_deg: number;
    relief_m: number;
  };
  mars_profile: any;
  candidates: CandidateItem[];
  candidates_10km_top2: {
    candidate_id: string;
    lat: number;
    lon: number;
    rank: number;
    terrain_distance: number;
  }[];
}

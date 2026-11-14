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

/** Support type of a research claim; not confidence. Mirrors analog/evidence_status.py. */
export type ClaimLevel = "VERIFIED" | "INFERRED" | "EXTERNAL" | "UNVERIFIED";

export interface ResearchClaim {
  id: string;
  statement: string;
  level: ClaimLevel;
  note: string;
  source?: string;
}

export type LiteratureStatus = "not_checked" | "checked_partial" | "checked";

export interface FeaturedEvidence {
  candidate_id: string;
  mars_target: TargetId;
  top2_in_tested_configurations: Record<string, boolean>;
  top2_count: number;
  configurations_count: number;
  /** Rank in the 10 km run; null = not among that run's 12 candidates. */
  scale10km_rank: number | null;
  prior_analog_literature: {
    status: LiteratureStatus;
    evidence_files: string[];
    claims: ResearchClaim[];
  };
  interpretation: string;
}

export interface OytagSample {
  sample_id: string;
  latitude_deg: number;
  longitude_deg: number;
  reported_rock_type: string;
  source_doi: string;
  source_locator: string;
  coordinate_datum: string;
  east_km: number;
  north_km: number;
  inside_local_100km_square: boolean;
}

export interface OytagOverlay {
  candidate_id: string;
  center: { lat: number; lon: number };
  window_km: number;
  local_axes: string;
  coordinate_caveat: string;
  evidence_scope: string;
  samples: OytagSample[];
  transect: {
    source_doi: string;
    source_figures: string;
    source_url: string;
    source_pdf_sha256: string;
    source_transport: { tls_certificate_validation: boolean; independent_hash_check: string; note: string };
    sensitivity: string;
    endpoints: {
      label: string;
      approx_lat_deg: number;
      approx_lon_deg: number;
      east_km: number;
      north_km: number;
      inside: boolean;
    }[];
  };
  claims: ResearchClaim[];
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
  claims?: ResearchClaim[];
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
  classification:
    | "Project-proposed"
    | "Established reference"
    | "Prior use unverified"
    | "Literature checked (partial)";
  featured?: FeaturedEvidence;
  oytagOverlay?: OytagOverlay;
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

/** GPT handoff reporting cards — Mars reference points, not Earth rankings. */
export interface MarsDiscoverySource {
  label: string;
  url: string;
}

export interface MarsDiscoveryLayers {
  slope: number;
  relief: number;
  thermal_inertia: number;
  ice_shallow: number;
  dust_cdod: number;
}

export interface MarsDiscoveryCard {
  id: string;
  purpose_key: string;
  role: string;
  lat: number;
  lon: number;
  intended_use: string;
  treatment: string;
  novelty_status: string;
  prohibited_claims: string[];
  weaknesses: string;
  next_checks: string;
  map_figure: string;
  sources: string[];
  descriptor_score: number;
  json_order: number;
  layers: MarsDiscoveryLayers;
  excluded_known_sites: string[];
  earth_analog: { status: string; note: string };
  themes: {
    terrain: { status: string; slope_deg: number; relief_m: number };
    temperature: {
      status: string;
      thermal_inertia: number;
      regional_surface_temperature: string;
    };
    water_ice: { status: string; ice_shallow: number };
    atmosphere_dust: { status: string; dust_cdod_my35: number };
  };
}

export interface MarsDiscoveryBundle {
  schema_version: string;
  earth_analog_pairing: string;
  novelty_policy: string;
  firm_rocky_status: string;
  limitations: string[];
  excluded_boxes: Record<string, unknown>;
  source_index: Record<string, MarsDiscoverySource>;
  files: { path: string; sha256: string }[];
  cards: MarsDiscoveryCard[];
}

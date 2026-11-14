import rawBundle from "./workbenchData.json";
import type {
  CandidateItem,
  ComparisonRow,
  FeaturedEvidence,
  OytagOverlay,
  ResearchClaim,
  TargetBundle,
  TargetId,
} from "../types/workbench";

const bundle: any = rawBundle;

export const WORKBENCH_META = bundle.meta;
export const EARTH_SOURCES = bundle.earth_sources as any[];
// profiles.json stores Mars sources as a list of {file, url, sha256, version}.
export const MARS_SOURCES = (bundle.mars_sources ?? []) as Array<{
  file?: string;
  url?: string;
  sha256?: string;
  version?: string;
}>;

/** Look up a Mars source record by its file name (exact match from outputs/). */
export function marsSource(file: string) {
  return MARS_SOURCES.find((s) => s.file === file);
}

const UNTRACED = "Unverified / Not traced in outputs/";
export const SENSITIVITY = bundle.sensitivity as Record<string, any>;
export const ROVER_TEMP_CONTEXT = bundle.rover_temperature_context as any;
export const MARS_MISSING_REQUIREMENTS = (bundle.mars_missing_requirements ?? []) as string[];
export const SCALE10KM_COUNTS = bundle.scale10km_counts as {
  land_centres_before_window_filter?: number;
  water_window_exclusions?: number;
  valid_windows?: number;
};

export const RESEARCH = (bundle.research ?? {}) as {
  schema_version?: string;
  source_commit?: string;
  files?: { path: string; sha256: string }[];
  featured?: Record<string, FeaturedEvidence>;
  oytag_overlays?: Record<string, OytagOverlay>;
};

function researchFile(suffix: string) {
  return RESEARCH.files?.find((f) => f.path.endsWith(suffix));
}

/** Short label for a claim list: counts per level, e.g. "1 VERIFIED · 2 UNVERIFIED". */
export function claimLevelSummary(claims: ResearchClaim[]): string {
  const order = ["VERIFIED", "INFERRED", "EXTERNAL", "UNVERIFIED"] as const;
  return order
    .map((lvl) => [lvl, claims.filter((c) => c.level === lvl).length] as const)
    .filter(([, n]) => n > 0)
    .map(([lvl, n]) => `${n} ${lvl}`)
    .join(" · ");
}

const TARGET_METADATA: Record<TargetId, { title: string; researchQuestion: string }> = {
  jezero: {
    title: "Jezero Crater",
    researchQuestion:
      "Which non-traditional Earth regions match Jezero's 100 km regional slope/relief, and do their climate/water-ice regimes support paleolake or rover ops testing?",
  },
  gale: {
    title: "Gale Crater",
    researchQuestion:
      "Which arid, high-relief Earth regions share Gale's 100 km terrain profile while preserving low-precipitation, dusty conditions?",
  },
  arcadia: {
    title: "Arcadia Planitia (Design Target)",
    researchQuestion:
      "Which flat, dry Earth plains match Arcadia's 100 km terrain profile as potential precursors for mid-latitude buried-ice and landing-ops studies?",
  },
};

export function getTargetIds(): TargetId[] {
  return (["jezero", "gale", "arcadia"] as TargetId[]).filter(
    (id) => Boolean(bundle.targets?.[id])
  );
}

export function getTargetBundle(targetId: TargetId): TargetBundle | null {
  const raw = bundle.targets?.[targetId];
  if (!raw) return null;

  const candidates: CandidateItem[] = (raw.candidates ?? []).map((c: any) => {
    const hasPower = c.earth_climate_context?.status === "context_only_not_ranked";
    const precip = c.earth_climate_context?.summary?.PRECTOTCORR?.value;
    const t2m = c.earth_climate_context?.summary?.T2M?.value;

    const keySupport = `D=${c.terrain_distance.toFixed(4)} (slope ${c.slope_median_deg.toFixed(2)}°, relief ${Math.round(c.relief_m)} m)`;
    let mainGap = "No climate, temperature, ice, or mineral comparison scored yet";
    if (hasPower && typeof precip === "number") {
      // No aridity threshold is defined in outputs/, so report the value without a wet/arid verdict.
      mainGap = `POWER context only (${precip.toFixed(2)} mm/day${typeof t2m === "number" ? `, T2M ${t2m.toFixed(1)} °C` : ""}); terrain-only match, no climate scoring`;
    }

    const featured = RESEARCH.featured?.[c.candidate_id];
    const oytagOverlay = RESEARCH.oytag_overlays?.[c.candidate_id];
    const litStatus = featured?.prior_analog_literature.status ?? c.prior_analog_literature_status;
    if (oytagOverlay) {
      mainGap = "Lithology overlap only; gypsum location and same-outcrop mineralogy unverified";
    }

    return {
      ...c,
      prior_analog_literature_status: litStatus,
      featured,
      oytagOverlay,
      evidenceCompleteness: {
        scoredDomains: 1,
        totalDomains: 4,
        label: hasPower ? "1/4 scored + POWER context" : "1/4 scored (Terrain only)",
      },
      keySupport,
      mainGap,
      classification:
        litStatus === "checked_partial" || litStatus === "checked"
          ? "Literature checked (partial)"
          : "Prior use unverified",
    } as CandidateItem;
  });

  return {
    id: targetId,
    title: TARGET_METADATA[targetId].title,
    researchQuestion: TARGET_METADATA[targetId].researchQuestion,
    summary: raw.summary,
    mars_profile: raw.mars_profile,
    candidates,
    candidates_10km_top2: raw.candidates_10km_top2 ?? [],
  };
}

function fmtNum(val: number | null | undefined, digits = 2, unit = ""): string {
  if (val === null || val === undefined || Number.isNaN(val)) return "Missing / Unknown";
  return `${val.toFixed(digits)}${unit ? ` ${unit}` : ""}`;
}

export function buildComparisonRows(
  target: TargetBundle,
  candidate: CandidateItem | null
): ComparisonRow[] {
  if (!candidate) return [];

  const molaSrc = EARTH_SOURCES.find((s) => s.dataset?.includes("MOLA")) ?? {};
  const etopoSrc = EARTH_SOURCES.find((s) => s.dataset?.includes("ETOPO")) ?? {};
  const powerSrc = candidate.earth_climate_context?.source;
  const powerSummary = candidate.earth_climate_context?.summary;

  const mp = target.mars_profile ?? {};
  const mTerrain = mp.terrain ?? {};
  const mTi = mp.thermal_inertia ?? {};
  // profiles.json keys SWIM layers as "0_1m" and "1_5m".
  const mIceShallow = mp.ice?.["0_1m"];
  const mIceDeep = mp.ice?.["1_5m"];
  const iceAvailable = mIceShallow?.status === "available" || mIceDeep?.status === "available";
  const swimShallowSrc = marsSource("SWIM2_c0_1.tif");
  const swimDeepSrc = marsSource("SWIM2_c1_5.tif");
  const tesSrc = marsSource("global_ti_night_2007.img");
  const dust34Src = marsSource("dustscenario_MY34_v2-5.nc");
  const dust35Src = marsSource("dustscenario_MY35_v2-5.nc");
  const t2mMonths =
    powerSummary?.T2M?.valid_months !== undefined && powerSummary?.T2M?.expected_months !== undefined
      ? `${powerSummary.T2M.valid_months}/${powerSummary.T2M.expected_months} valid months`
      : "valid-month count not recorded";
  const mDust34 = mp.dust?.dust_my34 ?? {};
  const mDust35 = mp.dust?.dust_my35 ?? {};

  const isJezero = target.id === "jezero";
  const medaSol700 = ROVER_TEMP_CONTEXT?.provisional_unqualified_windows?.find(
    (w: any) => w.ltst_sol === 700
  );

  const rows: ComparisonRow[] = [
    // 1. TERRAIN
    {
      id: "terrain-slope-relief",
      domain: "Terrain",
      metricName: "100 km Slope & Local Relief",
      earthQuantity: "Median slope, P90 slope, relief (m)",
      earthValue: `${candidate.slope_median_deg.toFixed(2)}° med · ${candidate.slope_p90_deg.toFixed(2)}° p90 · ${Math.round(candidate.relief_m)} m`,
      marsQuantity: "Median slope, P90 slope, relief (m)",
      marsValue: `${mTerrain.slope_median_deg !== undefined && mTerrain.slope_median_deg !== null ? mTerrain.slope_median_deg.toFixed(2) : "Missing"}° med · ${mTerrain.slope_p90_deg !== undefined && mTerrain.slope_p90_deg !== null ? mTerrain.slope_p90_deg.toFixed(2) : "Missing"}° p90 · ${mTerrain.relief_m !== undefined && mTerrain.relief_m !== null ? `${Math.round(mTerrain.relief_m)} m` : "Missing"}`,
      periodAndSupport: "Static DEMs · 100×100 km window (4 km spacing)",
      methodAndThreshold: `D = ${candidate.terrain_distance.toFixed(4)} (0.25·Δmed/1° + 0.25·Δp90/2° + 0.50·Δrelief/500m)`,
      comparability: "Direct",
      status: "Supported",
      sourcePortalLabel: "NOAA ETOPO 2022 ↔ NASA PDS MOLA",
      evidence: {
        id: "ev-terrain-dem",
        title: "100×100 km Regional Terrain (ETOPO 2022 ↔ MOLA MEGDR)",
        domain: "Terrain",
        earthSummary: `ETOPO 2022 surface v1 (averaged to 120 arcsec), land fraction ${(candidate.land_fraction * 100).toFixed(0)}%.`,
        marsSummary: `MGS MOLA 16 px/deg MEGDR, spherical R = 3,396 km, areoid elevation.`,
        sourceUrl: `${etopoSrc.url ?? "Unavailable"} | ${molaSrc.url ?? "Unavailable"}`,
        productId: "ETOPO_2022_v1_60s / megt90n000eb",
        version: `${etopoSrc.version ?? "v1"} / MOLA ${molaSrc.version ?? "2.0"}`,
        period: "Static composite (2022 release / MGS mission)",
        units: "degrees (slope), metres (relief)",
        nativeResolution: "Earth 60 arcsec (~1.85 km) | Mars 16 px/deg (~3.7 km)",
        analysisScale: "100×100 km azimuthal equidistant window, 4 km sampling (8 km stencil)",
        processingMethod: "Bilinear resampling on equal-area local grids; absolute elevation not compared",
        qaAndCoverage: `Land mask >= 95% (candidate: ${(candidate.land_fraction * 100).toFixed(0)}%); MOLA equatorial gaps up to ~12 km`,
        measurementKind: "Direct observation",
        limitations: [
          "4 km sampling does not resolve boulders, tire-scale hazards, or landing safety",
          "Statistical slope similarity does not prove shared geological origin",
        ],
        localFile: `${etopoSrc.file ?? "ETOPO_2022"} | ${molaSrc.file ?? "megt90n000eb.img"}`,
        checksumSha256: `Earth: ${etopoSrc.sha256 ?? "Unverified"} | Mars: ${molaSrc.sha256 ?? "Unverified"}`,
      },
    },
    {
      id: "terrain-landcover-geology",
      domain: "Terrain",
      metricName: "Land Cover, Mineralogy & Subsurface",
      earthQuantity: "MCD12C1 Land Cover (downloaded, not yet scored)",
      earthValue: "Not yet integrated",
      marsQuantity: "Mineralogy & Caves (MGC³ / CRISM)",
      marsValue: "Missing data",
      periodAndSupport: "2024 annual (Earth local) · Not queried (Mars)",
      methodAndThreshold: "Qualitative verification required in site deep-dive",
      comparability: "Not comparable",
      status: "Analysis incomplete",
      sourcePortalLabel: "NASA Earthdata (MCD12C1) / USGS",
      evidence: {
        id: "ev-terrain-geology",
        title: "Surface Materials, Mineralogy & Caves",
        domain: "Terrain",
        earthSummary: "MCD12C1 2024 HDF4 downloaded locally (data/raw/earth/terrain/landcover/), awaiting pipeline integration.",
        marsSummary: "CRISM/HiRISE/MGC³ intentionally excluded from automated global scoring per 48h scope.",
        sourceUrl: "Unverified / Not traced in results.json",
        productId: "MCD12C1.061 (local only)",
        version: "061",
        period: "2024 annual",
        units: "IGBP Land Cover class",
        nativeResolution: "0.05° CMG (3600×7200)",
        analysisScale: "Not yet integrated",
        processingMethod: "Pending",
        qaAndCoverage: "Not yet decoded into candidate scoring",
        measurementKind: "Design assumption / Missing",
        limitations: [
          "Regional DEMs cannot distinguish basalt, clays, sulfates, or caves",
          candidate.oytagOverlay
            ? "Published lithology points exist (see Prior Literature row) but no mineral polygons"
            : "Prior analog literature for this candidate has not been checked",
        ],
        localFile: "data/raw/earth/terrain/landcover/MCD12C1.A2024001.061.2025216131527.hdf",
        checksumSha256: "Not recorded in results.json",
      },
    },
    buildLiteratureRow(target, candidate),

    // 2. TEMPERATURE
    {
      id: "temp-regional-lst",
      domain: "Temperature",
      metricName: "Regional Dynamic Surface Temperature (100 km LST)",
      earthQuantity: "MODIS MOD11C3 v061 Day/Night LST (2023–2024)",
      earthValue: "Analysis incomplete (24 HDF4 files local, pending QA/scale decode)",
      marsQuantity: "Regional Dynamic Surface Temperature (surface_temperature)",
      marsValue:
        mp.surface_temperature?.status === "missing"
          ? "Missing data (status: missing in profiles.json)"
          : "Missing data",
      periodAndSupport: "Earth: 2023–2024 monthly (0.05° CMG) · Mars: No regional LST product loaded",
      methodAndThreshold: "Requires emissivity-corrected kinetic LST on both planets; do NOT substitute TES TI or rover TIRS",
      comparability: "Direct",
      status: "Missing data",
      sourcePortalLabel: "NASA LP DAAC (MOD11C3) ↔ Mars Regional LST Gap",
      evidence: {
        id: "ev-temp-lst",
        title: "Regional 100×100 km Kinetic Land Surface Temperature (MOD11C3 vs. Mars Gap)",
        domain: "Temperature",
        earthSummary:
          "24 monthly MOD11C3.061 HDF4 granules (2023–2024) stored under data/raw/earth/temperature/ on the data-collection machine (not in the repo; per-file SHA-256 in docs/earth_inventory.csv). Readable with netCDF4.Dataset; QA mask and 0.02 K scale factor not yet applied.",
        marsSummary: `Regional surface temperature is status='missing' in outputs/mars_profiles/profiles.json${mp.surface_temperature?.reason ? ` (reason: ${mp.surface_temperature.reason})` : ""}.`,
        sourceUrl: "https://lpdaac.usgs.gov/products/mod11c3v061/",
        productId: "MOD11C3.061 / Mars surface_temperature (missing)",
        version: "061 / N/A",
        period: "Earth: 2023-01 to 2024-12 | Mars: Missing",
        units: "K (kinetic surface temperature)",
        nativeResolution: "Earth: 0.05° (~5.6 km) | Mars: Missing",
        analysisScale: "100×100 km target window (not yet scored)",
        processingMethod: "Not yet integrated; missing values explicitly preserved as Missing data (never 0)",
        qaAndCoverage: "Earth: 24/24 files opened in local check (docs/earth_inventory.csv) | Mars: no regional LST product (missing)",
        measurementKind: "Design assumption / Missing",
        limitations: [
          "Mars TES thermal inertia (J m⁻² K⁻¹ s⁻⁰·⁵) and rover-local MEDA brightness temperature cannot replace regional LST",
          "Earth MOD11C3 requires mandatory cloud/emissivity QA filtering before computing 100 km window means",
        ],
        localFile: "data/raw/earth/temperature/MOD11C3.A202*.hdf (24 files) | outputs/mars_profiles/profiles.json",
        checksumSha256: "Earth: per-file SHA-256 in docs/earth_inventory.csv | Mars: not applicable (missing)",
      },
    },
    {
      id: "temp-thermal-inertia",
      domain: "Temperature",
      metricName: "Air Temp Context vs. TES Thermal Inertia",
      earthQuantity: "NASA POWER 2m Air Temp (T2M, 2023–2024)",
      earthValue: powerSummary?.T2M
        ? `${fmtNum(powerSummary.T2M.value, 2, "°C")} (min ${fmtNum(powerSummary.T2M_MIN?.value, 1)} / max ${fmtNum(powerSummary.T2M_MAX?.value, 1)} °C)`
        : "Missing data (only Top-2 queried)",
      marsQuantity: "MGS TES Nighttime Thermal Inertia (ex-infill)",
      marsValue:
        mTi.status === "available"
          ? `${fmtNum(mTi.mean, 1, "J m⁻² K⁻¹ s⁻⁰·⁵")} (valid ${mTi.valid_fraction !== undefined && mTi.valid_fraction !== null ? `${(mTi.valid_fraction * 100).toFixed(1)}%` : "Unknown"})`
          : "Missing data",
      periodAndSupport: "Earth: 2023–2024 (0.5°×0.625°) · Mars: TES 2007 release (20 px/deg)",
      methodAndThreshold: "STRICTLY SEPARATE — never subtract air/LST temp from thermal inertia",
      comparability: "Not comparable",
      status: powerSummary?.T2M ? "Mismatch" : "Missing data",
      sourcePortalLabel: "NASA POWER ↔ NASA PDS TES",
      evidence: {
        id: "ev-temp-ti",
        title: "Earth 2m Air Temperature vs. Mars TES Nighttime Thermal Inertia",
        domain: "Temperature",
        earthSummary: powerSummary?.T2M
          ? `NASA POWER MERRA2/POWER monthly mean T2M = ${fmtNum(powerSummary.T2M.value, 2, "°C")} (${t2mMonths}).`
          : "NASA POWER was only queried for Ranks #1–#2 per target.",
        marsSummary: `TES Nighttime Thermal Inertia mean = ${mTi.mean?.toFixed(1) ?? "—"} J m⁻² K⁻¹ s⁻⁰·⁵ (infilled pixels excluded; with-infill mean = ${mTi.with_infilled_pixels?.mean?.toFixed(1) ?? "—"}).`,
        sourceUrl: [powerSrc?.url, tesSrc?.url].filter(Boolean).join(" | ") || UNTRACED,
        productId: "POWER Monthly API / global_ti_night_2007",
        version: "POWER v2.10.0 / TES v1",
        period: "Earth: 2023-01 to 2024-12 | Mars: TES archive (2007 release, obs. dates unlisted)",
        units: "Earth: °C (2m air) | Mars: J m⁻² K⁻¹ s⁻⁰·⁵ (thermal inertia)",
        nativeResolution: "Earth: 0.5°×0.625° | Mars: 20 px/deg (~3.0 km)",
        analysisScale: "Earth: point query | Mars: 100×100 km cos(lat)-weighted native cell mean",
        processingMethod: "Kept physically separate; MOD11C3 LST (0.05°) downloaded locally but not yet integrated",
        qaAndCoverage: `TES valid fraction: ${mTi.valid_fraction !== undefined && mTi.valid_fraction !== null ? `${(mTi.valid_fraction * 100).toFixed(1)}%` : "Unknown"} (infilled mask=0 excluded)`,
        measurementKind: "Derived / Reanalysis",
        limitations: [
          "Thermal inertia is NOT surface temperature and NOT a direct measure of soil hardness",
          "MOD11C3 (2023–2024) is collected locally but not yet decoded with QA/scale factors",
        ],
        localFile: `Earth: ${powerSrc?.file ?? "not queried for this candidate"} | Mars: data/raw/mars/${tesSrc?.file ?? "global_ti_night_2007.img"}`,
        checksumSha256: `Earth: ${powerSrc?.sha256 ?? "not queried"} | Mars: ${tesSrc?.sha256 ?? "Unverified"}`,
      },
    },
    {
      id: "temp-meda-rover",
      domain: "Temperature",
      metricName: "Rover-Local Ground Brightness Temp (MEDA TIRS)",
      earthQuantity: "MOD11C3 0.05° LST (downloaded locally, pending)",
      earthValue: "Pending integration",
      marsQuantity: "Perseverance MEDA TIRS (LTST sol 700–702)",
      marsValue: isJezero
        ? `Provisional only: Day ${medaSol700?.day?.brightness_temperature_K ?? "—"} K / Night ${medaSol700?.night?.brightness_temperature_K ?? "—"} K (Δ ${medaSol700?.sampled_day_night_contrast_K?.toFixed(1) ?? "—"} K)`
        : "Outside coverage (Jezero rover only)",
      periodAndSupport: isJezero
        ? "UTC 2023-02-07 to 2023-02-10 (3 sols, rover-local footprint)"
        : "Not available for Gale or Arcadia",
      methodAndThreshold: "Excluded from scoring (quality_supported_records = 0)",
      comparability: "Contextual",
      status: isJezero ? "Failed quality checks" : "Outside coverage",
      sourcePortalLabel: "NASA PDS4 Mars2020 MEDA",
      evidence: {
        id: "ev-temp-meda",
        title: "Perseverance MEDA Calibrated TIRS Ground Brightness Temperature",
        domain: "Temperature",
        earthSummary: "MOD11C3 (24 HDF4 files, 2023–2024) stored locally, awaiting QA/scale decoding.",
        marsSummary: isJezero
          ? "159,418 records across sols 700–702; 0 quality-supported records because 3 rover flags (wheel FOV, HGA, SkyCam) are unknown."
          : "No rover-local MEDA data exists at Gale or Arcadia; REMS (Gale) not yet integrated.",
        sourceUrl: "https://atmos.nmsu.edu/PDS/data/PDS4/Mars2020/mars2020_meda/data_calibrated_env/sol_0660_0779/",
        productId: "urn:nasa:pds:mars2020_meda:data_calibrated_env:we__0700..0702",
        version: "1.0",
        period: "2023-02-07 to 2023-02-10 (sols 700–702)",
        units: "K (IR brightness temperature, not kinetic LST)",
        nativeResolution: "Rover-local TIRS footprint (not a 100 km regional mean)",
        analysisScale: "Hourly LTST bins: Day [12,15), Night [0,3)",
        processingMethod: "Median of hourly medians; provisional unqualified values flagged separately",
        qaAndCoverage: isJezero
          ? "status = quality_incomplete (0/159,418 fully qualified records)"
          : "No coverage at this target",
        measurementKind: "Direct observation",
        limitations: [
          "Provisional observations include unknown/failed flags and are excluded from scoring",
          "Brightness temperature is not directly equivalent to MODIS kinetic LST without emissivity/geometry correction",
          "3 sols cannot represent a Mars seasonal climatology",
        ],
        localFile: "outputs/mars_temperature/summary.json",
        checksumSha256: ROVER_TEMP_CONTEXT?.sources?.[0]?.sha256 ?? "Unverified",
      },
    },

    // 3. WATER / ICE
    {
      id: "water-aridity-swim",
      domain: "Water/Ice",
      metricName: "Precipitation Context vs. SWIM 2.0 Ice Consistency",
      earthQuantity: "NASA POWER Precipitation (2023–2024)",
      earthValue: powerSummary?.PRECTOTCORR
        ? `${fmtNum(powerSummary.PRECTOTCORR.value, 3, "mm/day")}`
        : "Missing data (only Top-2 queried)",
      marsQuantity: "SWIM 2.0 Consistency (0–1 m / 1–5 m)",
      marsValue: iceAvailable
        ? `0–1m: ${fmtNum(mIceShallow?.mean, 3)} | 1–5m: ${fmtNum(mIceDeep?.mean, 3)} (−1..+1)`
        : "Missing / Outside ±60°",
      periodAndSupport: "Earth: 2023–2024 · Mars: SWIM 2.0 composite (±60° lat)",
      methodAndThreshold: "SWIM score is NOT ice content, purity, or probability; 0 ≠ unknown",
      comparability: "Contextual",
      // Contextual only: no aridity threshold or water/ice scoring exists in outputs/.
      status:
        powerSummary?.PRECTOTCORR?.value !== undefined && powerSummary.PRECTOTCORR.value !== null
          ? "Not checked"
          : "Missing data",
      sourcePortalLabel: "NASA POWER ↔ SWIM 2.0 (PSI)",
      evidence: {
        id: "ev-water-swim",
        title: "Earth Precipitation Context vs. Mars SWIM 2.0 Subsurface Ice Consistency",
        domain: "Water/Ice",
        earthSummary: powerSummary?.PRECTOTCORR
          ? `POWER 2023–2024 precipitation = ${powerSummary.PRECTOTCORR.value?.toFixed(3)} mm/day. GPM_3IMERGM & GLDAS downloaded locally for full grid.`
          : "POWER not queried for Ranks #3–#12; GPM_3IMERGM & GLDAS downloaded locally.",
        marsSummary: `SWIM 2.0 mean consistency in 100 km window: 0–1m = ${fmtNum(mIceShallow?.mean, 4)} (median ${fmtNum(mIceShallow?.median, 4)}), 1–5m = ${fmtNum(mIceDeep?.mean, 4)} (median ${fmtNum(mIceDeep?.median, 4)}). Not ice amount or probability.`,
        sourceUrl: [swimShallowSrc?.url, swimDeepSrc?.url].filter(Boolean).join(" | ") || UNTRACED,
        productId: "SWIM2_c0_1 / SWIM2_c1_5",
        version: "2.0",
        period: "Earth: 2023–2024 | Mars: SWIM 2.0 multi-dataset composite",
        units: "Earth: mm/day | Mars: dimensionless consistency (−1 to +1)",
        nativeResolution: "Earth: 0.5°×0.625° (POWER) | Mars: 20 px/deg (~±60° lat)",
        analysisScale: "100×100 km cos(lat)-weighted mean on Mars",
        processingMethod: "Kept separate; positive SWIM favors ice presence but is not extractable resource volume",
        qaAndCoverage: `SWIM valid fraction: 0–1m ${typeof mIceShallow?.valid_fraction === "number" ? `${(mIceShallow.valid_fraction * 100).toFixed(1)}% (${mIceShallow.valid_native_cells}/${mIceShallow.native_cells_in_window} cells)` : "Unknown"} · 1–5m ${typeof mIceDeep?.valid_fraction === "number" ? `${(mIceDeep.valid_fraction * 100).toFixed(1)}%` : "Unknown"}`,
        measurementKind: "Model / Composite",
        limitations: [
          "SWIM covers roughly 60°S–60°N only",
          "No aridity threshold is defined in outputs/; precipitation is shown as context, not as a pass/fail test",
          "Martian ice sublimates rather than melting under ~0.6 kPa CO₂",
        ],
        localFile: "data/raw/mars/SWIM2_c0_1.tif | data/raw/mars/SWIM2_c1_5.tif",
        checksumSha256: `0–1m: ${swimShallowSrc?.sha256 ?? "Unverified"} | 1–5m: ${swimDeepSrc?.sha256 ?? "Unverified"}`,
      },
    },
    {
      id: "water-permafrost-ndvi",
      domain: "Water/Ice",
      metricName: "Permafrost, Soil Moisture & NDVI (Local Only)",
      earthQuantity: "ESA Permafrost (2021), GLDAS, MOD13C2 NDVI",
      earthValue: "Downloaded locally, not yet scored",
      marsQuantity: "No Mars NDVI / no direct permafrost match",
      marsValue: "Not applicable (Mars assumed barren)",
      periodAndSupport: "Earth: 2021 (ESA PFR) / 2023–2024 (GLDAS, NDVI)",
      methodAndThreshold: "PFR is modeled area fraction (%), not ice volume; NDVI requires QA masking",
      comparability: "Not comparable",
      status: "Analysis incomplete",
      sourcePortalLabel: "ESA CCI / NASA Earthdata",
      evidence: {
        id: "ev-water-esa",
        title: "ESA CCI Permafrost v4.0, GLDAS Soil Moisture & MODIS NDVI",
        domain: "Water/Ice",
        earthSummary: "Downloaded to data/raw/earth/water_ice/ (permafrost/, gldas/, ndvi/), awaiting pipeline integration.",
        marsSummary: "Mars has no vegetation; low Earth NDVI can also reflect water, snow, or bad QA.",
        sourceUrl: UNTRACED,
        productId: "ESACCI-PERMAFROST-L4-PFR / GLDAS_NOAH025_M / MOD13C2",
        version: "ESA v4.0 / GLDAS v2.1 / MODIS v061",
        period: "2021 (ESA) | 2023–2024 (GLDAS, MODIS)",
        units: "PFR %, kg m⁻², NDVI",
        nativeResolution: "0.01° (25°N–85°N) / 0.25° / 0.05°",
        analysisScale: "Pending integration",
        processingMethod: "Pending",
        qaAndCoverage: "Pending QA mask verification",
        measurementKind: "Model / Composite",
        limitations: [
          "Even hyper-arid Earth deserts host microbes; NDVI ≈ 0 does not prove lifelessness",
          "ESA CCI Permafrost covers Northern Hemisphere 25°N–85°N only",
        ],
        localFile: "data/raw/earth/water_ice/permafrost/ESACCI-PERMAFROST-L4-PFR-MODISLST_CRYOGRID-AREA4_PP-2021-fv04.0.nc",
        checksumSha256: "Not recorded in results.json",
      },
    },

    // 4. AIR / DUST
    {
      id: "air-dust-wind",
      domain: "Air/Dust",
      metricName: "Wind Speed vs. Mars Dust Climatology (CDOD)",
      earthQuantity: "NASA POWER 10m Wind (WS10M, 2023–2024)",
      earthValue: powerSummary?.WS10M ? fmtNum(powerSummary.WS10M.value, 2, "m/s") : "Missing data (only Top-2 queried)",
      marsQuantity: "Montabone v2.5 CDOD (9.3 μm, MY34 / MY35)",
      marsValue: mDust34.status === "available"
        ? `MY34 ${fmtNum(mDust34.mean_cdodtot, 3)} (max ${fmtNum(mDust34.max_cdodtot, 2)}) · MY35 ${fmtNum(mDust35.mean_cdodtot, 3)}`
        : "Missing data",
      periodAndSupport: "Earth: 2023–2024 (0.5°×0.625°) · Mars: MY34/MY35 (native 3° grid)",
      methodAndThreshold: "Do NOT subtract 550 nm Earth AOT from 9.3 μm Mars absorption CDOD",
      comparability: "Not comparable",
      status: "Missing data",
      sourcePortalLabel: "NASA POWER / LMD Montabone v2.5",
      evidence: {
        id: "ev-air-dust",
        title: "Earth Dust/Wind (POWER, MERRA-2, VIIRS) vs. Mars Montabone Dust Climatology",
        domain: "Air/Dust",
        earthSummary: "POWER WS10M queried for Top-2; MERRA-2 DUEXTTAU (24 files) & VIIRS Deep Blue 550nm AOD (25 files) + M2TMNXSLV (wind/pressure) downloaded locally.",
        marsSummary: `Montabone v2.5 3° nearest cell (${mDust34.native_cell_lat ?? "—"}°, ${mDust34.native_cell_lon ?? "—"}°): MY34 storm year mean CDOD = ${mDust34.mean_cdodtot?.toFixed(4) ?? "—"}, MY35 typical = ${mDust35.mean_cdodtot?.toFixed(4) ?? "—"}.`,
        sourceUrl: [dust34Src?.url, dust35Src?.url].filter(Boolean).join(" | ") || UNTRACED,
        productId: "dustscenario_MY34_v2-5 / dustscenario_MY35_v2-5",
        version: "v2.5 (CC BY-SA 3.0)",
        period: "MY34 (2017–2019 global storm) & MY35 (669 sols each)",
        units: "CDOD (dimensionless, 9.3 μm absorption) | Earth WS10M (m/s)",
        nativeResolution: "Mars: 3°×3° (~177 km, NOT a 100 km local observation)",
        analysisScale: "Nearest native 3° cell; 669-sol time series",
        processingMethod: "Kriged MRO/MCS & TES/THEMIS climatology; Earth AOT alignment pending",
        qaAndCoverage: "669/669 reconstructed sols available",
        measurementKind: "Derived / Reanalysis",
        limitations: [
          "Earth 550 nm extinction AOT and Mars 9.3 μm absorption CDOD measure different optical regimes",
          "Earth surface air (~101 kPa) is ~100× denser than Mars (~0.6 kPa CO₂), so wind forces are not equivalent",
        ],
        localFile: "data/raw/mars/dustscenario_MY34_v2-5.nc | data/raw/mars/dustscenario_MY35_v2-5.nc",
        checksumSha256: `MY34: ${dust34Src?.sha256 ?? "Unverified"} | MY35: ${dust35Src?.sha256 ?? "Unverified"}`,
      },
    },
  ];

  return rows;
}

function buildLiteratureRow(target: TargetBundle, candidate: CandidateItem): ComparisonRow {
  const overlay = candidate.oytagOverlay;
  const lit = candidate.featured?.prior_analog_literature;
  if (!overlay || !lit) {
    return {
      id: "terrain-prior-literature",
      domain: "Terrain",
      metricName: "Published Lithology & Prior Analog Literature",
      earthQuantity: "Published sample points inside the 100 km window",
      earthValue: "Not checked",
      marsQuantity: `${target.title} mineral assemblage`,
      marsValue: "No Mars mineral layer loaded",
      periodAndSupport: "Not applicable",
      methodAndThreshold: "No literature overlap check recorded in outputs/research/",
      comparability: "Contextual",
      status: "Not checked",
      sourcePortalLabel: "Not checked",
      evidence: {
        id: "ev-prior-literature",
        title: "Prior Analog Literature",
        domain: "Terrain",
        earthSummary: "No published sample or prior-analog check exists for this candidate.",
        marsSummary: "CRISM/CheMin mineralogy is not integrated into this workbench.",
        sourceUrl: UNTRACED,
        productId: "Not applicable",
        version: "Not applicable",
        period: "Not applicable",
        units: "Not applicable",
        nativeResolution: "Not applicable",
        analysisScale: "Not applicable",
        processingMethod: "Not performed",
        qaAndCoverage: "Not performed",
        measurementKind: "Design assumption / Missing",
        limitations: ["Absence of a check is not evidence of absence of prior analog use"],
        localFile: "None",
        checksumSha256: "Not applicable",
      },
    };
  }

  const samples = overlay.samples;
  const rocks = samples.map((s) => `${s.reported_rock_type} (${s.sample_id})`).join(", ");
  const overlapFile = researchFile("oytag_overlap.json");
  const transectFile = researchFile("oytag_transect_check.json");
  const tr = overlay.transect;
  return {
    id: "terrain-prior-literature",
    domain: "Terrain",
    metricName: "Published Lithology & Prior Analog Literature",
    earthQuantity: "Bershaw et al. (2012) Table 1 sample points",
    earthValue: `${samples.length} published samples in window: ${rocks}`,
    marsQuantity: `${target.title} mineral assemblage`,
    marsValue: "No Mars mineral layer loaded",
    periodAndSupport: "Published coordinates (datum not stated) · approximate overlap",
    methodAndThreshold: "Point-in-window check (azimuthal equidistant + stored polygon); no mineral matching",
    comparability: "Contextual",
    status: "Provisional",
    sourcePortalLabel: "J. Asian Earth Sci. (2012) / Tectonophysics (2013)",
    evidence: {
      id: "ev-prior-literature",
      title: "Oytag Sedimentary Literature Overlap (Bershaw et al. 2012; Sun et al. 2013)",
      domain: "Terrain",
      earthSummary: `${samples.length} published rock samples (${rocks}) fall inside the 100×100 km window, ${Math.min(...samples.map((s) => s.east_km)).toFixed(0)}–${Math.max(...samples.map((s) => s.east_km)).toFixed(0)} km east of centre. A gypsum-bearing section (Sun et al. 2013, ${tr.source_figures}) is approximately digitized inside the window.`,
      marsSummary: `No Mars mineralogy is loaded; lithology is not compared against ${target.title}.`,
      sourceUrl: `https://doi.org/${samples[0].source_doi} | https://doi.org/${tr.source_doi}`,
      productId: `${samples[0].source_locator} / ${tr.source_figures}`,
      version: `Research schema ${RESEARCH.schema_version ?? "unknown"} (source commit ${RESEARCH.source_commit?.slice(0, 7) ?? "unknown"})`,
      period: "Published field samples (collection dates per source)",
      units: "Reported rock type (categorical); local east/north (km)",
      nativeResolution: "Point coordinates; transect digitized from a figure",
      analysisScale: `${overlay.window_km}×${overlay.window_km} km window centred ${overlay.center.lat.toFixed(1)}°, ${overlay.center.lon.toFixed(1)}°`,
      processingMethod: "Spherical azimuthal equidistant projection and independent stored-polygon containment",
      qaAndCoverage: `${samples.filter((s) => s.inside_local_100km_square).length}/${samples.length} samples inside; transect ${tr.endpoints.every((e) => e.inside) ? "inside" : "partly outside"}; claims: ${claimLevelSummary(lit.claims)}`,
      measurementKind: "Direct observation",
      limitations: [
        overlay.coordinate_caveat,
        "Gypsum is section-level evidence only: no gypsum GPS or sample ID",
        "Smectite/iron-oxide pairing with gypsum at one outcrop is unconfirmed",
        "Not a verified Gale lacustrine or mineral-assemblage analog",
        tr.source_transport.tls_certificate_validation
          ? "Transect source retrieved with TLS validation"
          : `Transect source PDF fetched without TLS validation; independent hash check: ${tr.source_transport.independent_hash_check}`,
      ],
      localFile: [overlapFile?.path, transectFile?.path].filter(Boolean).join(" | ") || UNTRACED,
      checksumSha256: `overlap: ${overlapFile?.sha256 ?? "Unverified"} | transect: ${transectFile?.sha256 ?? "Unverified"} | source PDF: ${tr.source_pdf_sha256}`,
      claims: lit.claims,
    },
  };
}

import rawBundle from "./workbenchData.json";
import type {
  CandidateItem,
  ComparisonRow,
  TargetBundle,
  TargetId,
} from "../types/workbench";

const bundle: any = rawBundle;

export const WORKBENCH_META = bundle.meta;
export const EARTH_SOURCES = bundle.earth_sources as any[];
export const MARS_SOURCES = bundle.mars_sources as Record<string, any>;
export const SENSITIVITY = bundle.sensitivity as Record<string, any>;
export const ROVER_TEMP_CONTEXT = bundle.rover_temperature_context as any;
export const MARS_MISSING_REQUIREMENTS = (bundle.mars_missing_requirements ?? []) as string[];
export const SCALE10KM_COUNTS = bundle.scale10km_counts as {
  land_centres_before_window_filter?: number;
  water_window_exclusions?: number;
  valid_windows?: number;
};

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
      mainGap =
        precip > 1.5
          ? `Wet POWER climate (${precip.toFixed(2)} mm/day, T2M ${t2m?.toFixed(1)} °C); terrain-only match`
          : `Arid POWER context (${precip.toFixed(2)} mm/day); lacks geology, LST, & dust scoring`;
    }

    return {
      ...c,
      evidenceCompleteness: {
        scoredDomains: 1,
        totalDomains: 4,
        label: hasPower ? "1/4 scored + POWER context" : "1/4 scored (Terrain only)",
      },
      keySupport,
      mainGap,
      classification: "Prior use unverified",
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
  const mIce = mp.ice ?? {};
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
          "Prior analog literature for this candidate has not been checked",
        ],
        localFile: "data/raw/earth/terrain/landcover/MCD12C1.A2024001.061.2025216131527.hdf",
        checksumSha256: "Not recorded in results.json",
      },
    },

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
          "24 monthly MOD11C3.061 HDF4 granules (2023–2024) verified on disk under data/raw/earth/temperature/lst/, awaiting pyhdf QA mask and 0.02 K scale-factor integration.",
        marsSummary:
          mp.surface_temperature?.note ??
          "Regional dynamic surface temperature (diurnal/seasonal) is marked status='missing' in outputs/mars_profiles/profiles.json.",
        sourceUrl: "https://lpdaac.usgs.gov/products/mod11c3v061/",
        productId: "MOD11C3.061 / Mars surface_temperature (missing)",
        version: "061 / N/A",
        period: "Earth: 2023-01 to 2024-12 | Mars: Missing",
        units: "K (kinetic surface temperature)",
        nativeResolution: "Earth: 0.05° (~5.6 km) | Mars: Missing",
        analysisScale: "100×100 km target window (not yet scored)",
        processingMethod: "Not yet integrated; missing values explicitly preserved as Missing data (never 0)",
        qaAndCoverage: "Earth: 24/24 files local | Mars: 0% regional LST coverage",
        measurementKind: "Design assumption / Missing",
        limitations: [
          "Mars TES thermal inertia (J m⁻² K⁻¹ s⁻⁰·⁵) and rover-local MEDA brightness temperature cannot replace regional LST",
          "Earth MOD11C3 requires mandatory cloud/emissivity QA filtering before computing 100 km window means",
        ],
        localFile: "data/raw/earth/temperature/lst/MOD11C3.A2024*.hdf | outputs/mars_profiles/profiles.json",
        checksumSha256: "Not recorded in results.json (unscored)",
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
          ? `NASA POWER MERRA2/POWER monthly mean T2M = ${powerSummary.T2M.value?.toFixed(2)} °C (24/24 valid months).`
          : "NASA POWER was only queried for Ranks #1–#2 per target.",
        marsSummary: `TES Nighttime Thermal Inertia mean = ${mTi.mean?.toFixed(1) ?? "—"} J m⁻² K⁻¹ s⁻⁰·⁵ (infilled pixels excluded; with-infill mean = ${mTi.with_infilled_pixels?.mean?.toFixed(1) ?? "—"}).`,
        sourceUrl: powerSrc?.url ?? "https://pds-geosciences.wustl.edu/mgs/mgs-m-tes-5-timap-v1/mgst_9001/data/global_ti_night_2007.lbl",
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
        localFile: powerSrc?.file ?? "data/raw/mars/global_ti_night_2007.img",
        checksumSha256: powerSrc?.sha256 ?? (MARS_SOURCES.tes_thermal_inertia_night?.sha256 ?? "Unverified"),
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
      marsValue: mIce?.shallow_0_1m
        ? `0–1m: ${fmtNum(mIce.shallow_0_1m.mean, 3)} | 1–5m: ${fmtNum(mIce.deep_1_5m?.mean, 3)} (−1..+1)`
        : "Missing / Outside ±60°",
      periodAndSupport: "Earth: 2023–2024 · Mars: SWIM 2.0 composite (±60° lat)",
      methodAndThreshold: "SWIM score is NOT ice content, purity, or probability; 0 ≠ unknown",
      comparability: "Contextual",
      status:
        powerSummary?.PRECTOTCORR?.value !== undefined && powerSummary.PRECTOTCORR.value !== null
          ? powerSummary.PRECTOTCORR.value > 1.5
            ? "Mismatch"
            : "Supported"
          : "Missing data",
      sourcePortalLabel: "NASA POWER ↔ SWIM 2.0 (PSI)",
      evidence: {
        id: "ev-water-swim",
        title: "Earth Precipitation Context vs. Mars SWIM 2.0 Subsurface Ice Consistency",
        domain: "Water/Ice",
        earthSummary: powerSummary?.PRECTOTCORR
          ? `POWER 2023–2024 precipitation = ${powerSummary.PRECTOTCORR.value?.toFixed(3)} mm/day. GPM_3IMERGM & GLDAS downloaded locally for full grid.`
          : "POWER not queried for Ranks #3–#12; GPM_3IMERGM & GLDAS downloaded locally.",
        marsSummary: `SWIM 2.0 mean consistency in 100 km window: 0–1m = ${mIce?.shallow_0_1m?.mean?.toFixed(4) ?? "—"}, 1–5m = ${mIce?.deep_1_5m?.mean?.toFixed(4) ?? "—"}.`,
        sourceUrl: "https://swim.psi.edu/output/SWIM2/Global/Composite/SWIM2_c0_1.tif",
        productId: "SWIM2_c0_1 / SWIM2_c1_5",
        version: "2.0",
        period: "Earth: 2023–2024 | Mars: SWIM 2.0 multi-dataset composite",
        units: "Earth: mm/day | Mars: dimensionless consistency (−1 to +1)",
        nativeResolution: "Earth: 0.5°×0.625° (POWER) | Mars: 20 px/deg (~±60° lat)",
        analysisScale: "100×100 km cos(lat)-weighted mean on Mars",
        processingMethod: "Kept separate; positive SWIM favors ice presence but is not extractable resource volume",
        qaAndCoverage: `SWIM valid fraction: ${mIce?.shallow_0_1m?.valid_fraction !== undefined && mIce?.shallow_0_1m?.valid_fraction !== null ? `${(mIce.shallow_0_1m.valid_fraction * 100).toFixed(1)}%` : "Unknown"}`,
        measurementKind: "Model / Composite",
        limitations: [
          "SWIM covers roughly 60°S–60°N only",
          "Precipitation >1.5 mm/day (e.g. Jezero #1/#2) disqualifies site as an arid Mars analog",
          "Martian ice sublimates rather than melting under ~0.6 kPa CO₂",
        ],
        localFile: "data/raw/mars/SWIM2_c0_1.tif",
        checksumSha256: MARS_SOURCES.ice_consistency_shallow?.sha256 ?? "Unverified",
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
        sourceUrl: "https://dap.ceda.ac.uk/neodc/esacci/permafrost/data/permafrost_extent/L4/area4/pp/v04.0/",
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
        sourceUrl: "https://www-mars.lmd.jussieu.fr/mars/dust_climatology/dataset_v2/dustscenario_MY34_v2-5.nc",
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
        localFile: "data/raw/mars/dustscenario_MY34_v2-5.nc",
        checksumSha256: MARS_SOURCES.dust_my34?.sha256 ?? "Unverified",
      },
    },
  ];

  return rows;
}

"""Write the MS-02 CSV tables (candidates, evidence, prior_work, search_log) and manifest.json.

Every row records what was actually read; see the 'read_scope' / 'locator' columns.
Run from repo root AFTER verify_ms02.py and after docs/research/MS-02/report.md exists:
    python3 -I scripts/research/ms02_earth_analogs/build_tables.py
"""
import csv, hashlib, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "outputs/research/MS-02"
OUT.mkdir(parents=True, exist_ok=True)
DATE = "2026-11-14"

BASE_SHA = "f7076c9fdc77e00244ed5d6863aad2bf78cfa28f"   # handoff/verified-data-20261114
MAIN_SHA = "3cc8488577535e2fa4d146021fde51f8ff6cc667"   # origin/main at start

# ------------------------------------------------------------------ sources
SRC = {
    "SWIM": "https://swim.psi.edu/SWIM2Products.php",
    "MORGAN": "https://doi.org/10.1038/s41550-020-01290-z",
    "HAUBER": "https://doi.org/10.1144/SP356.7",
    "MARINOVA": "https://doi.org/10.1017/S0954102022000025",
    "HELDMANN": "https://doi.org/10.1016/j.pss.2013.05.019",
    "BANNISTER": "https://doi.org/10.5281/zenodo.1154854",
    "BRIGHI": "https://meetingorganizer.copernicus.org/EPSC-DPS2025/EPSC-DPS2025-710.html",
    "RASMUSSEN": "https://doi.org/10.1016/j.quascirev.2023.108137",
    "ROTEM": "https://doi.org/10.5194/tc-17-3363-2023",
    "ANDRES": "https://core.ac.uk/download/364350841.pdf",
    "HIBBARD": "https://ir.lib.uwo.ca/etd/8120",
    "PANGAEA_921087": "https://doi.pangaea.de/10.1594/PANGAEA.921087",
    "UNISCALM_AGU2016": "https://ui.adsabs.harvard.edu/abs/2016AGUFMGC31H1202S",
    "SESS2018": "https://doi.org/10.5281/zenodo.4777825",
    "NIETO_STEWART2003": "https://www.crewes.org/Documents/ResearchReports/2003/2003-08.pdf",
    "CSEG_STEWART": "https://csegrecorder.com/articles/view/mars-in-canada-the-nasa-haughton-mars-project-devon-island-nunavut",
    "KOWALEWSKI2006": "https://doi.org/10.1017/S0954102006000460",
    "MCKAY2009": "https://doi.org/10.1017/S0954102008001508",
    "ELSTON1979_USGS_IMAP1140": "https://pubs.usgs.gov/publication/i1140",
    "CEBRENIA_QUADRANGLE": "https://en.wikipedia.org/wiki/Cebrenia_quadrangle",
    "HANDOFF": "outputs/research/mars_reselection_20261114/",
}
HF = "final_candidates.csv (row MS-02)"
HN = "candidate_native_evidence.json (record D)"

# ------------------------------------------------------------------ candidates
cand_cols = ["candidate_id", "name", "lat_deg", "lon_deg_east", "research_extent", "boundary_basis",
             "available_data", "testable_physical_processes", "main_environment_differences",
             "disposition", "disposition_reason", "cannot_extrapolate", "next_verification_step"]
cands = [
 ["MS-02-E01", "University Valley, Quartermain Mountains, McMurdo Dry Valleys (Antarctica)",
  -77.8667, 160.75,
  "Valley floor around the met/ground-temperature station cluster (1661-1697 m a.s.l.); polygon outline NOT obtained",
  "Marinova 2022 p.145 (valley 77°52'S 160°45'E, ~1700 m) and p.146 (stations 77°51.729'S 160°42.606'E, 1661-1697 m); boundary = station cluster, not a surveyed polygon",
  "Air T/RH 1.2 m, wind 1.08 m, ground T at surface/10/42/49 cm, 2009-12 to 2013-01 (Marinova Table II p.153); ice-table depth 10-60 cm (Heldmann 2013 abstract)",
  "Dry cover over ice-cemented ground: how ice-table depth, cover and seasonal heating couple; sublimation/vapour exchange; whether a thermal signal is separable from cover",
  "Latitude 77.9°S vs 52.75°N; MAAT -23.4 °C measured vs Mars MCS 03/15 LTST surface medians (not annual mean); atmosphere, pressure, dust, insolation all differ; ice in dry soil at 42 cm vs MS-02 ice depth unknown",
  "保留",
  "Only candidate with a measured multi-depth temperature series that brackets an ice table and a published energy-balance model; directly addresses 'cover + season + ice' hypotheses H1/H2",
  "Not a proof that MS-02 has ice; no extrapolation of 42 cm ice-table depth, temperatures or water activity to MS-02",
  "Obtain Table II/Fig. 6 series from the paper/supplement; get soil density and heat capacity (only conductivity and diffusivity were read, so thermal inertia is not derived); find wind-speed values; test what TES-scale (3 km) thermal inertia could/couldn't see for a 42 cm ice table"],
 ["MS-02-E02", "Middle Beacon Valley, Quartermain Mountains (Antarctica)",
  None, None,
  "Not defined: coordinates not extracted; only valley name and Heldmann 2013 / Bannister 2007 abstracts read",
  "Heldmann 2013 abstract (middle Beacon Valley massive ground ice); Kowalewski 2006 abstract (central Beacon Valley); McKay 2009 abstract; Bannister 2007 abstract (1.3 km transect)",
  "Heldmann 2013 (ice 10-60 cm, abstract); Kowalewski 2006 (ice under 40-80 cm sublimation till; net loss ~0.017 mm over 18 Nov-29 Dec 2004, HOBO loggers; abstract); McKay 2009 (snow recurrence >10 yr implied on Beacon floor; abstract); Bannister 2007 undergraduate thesis (buried massive ice reported >100 m deep)",
  "Massive buried ice beneath thin dry cover; sublimation-rate and humidity/temperature sensitivity of buried ice; snow recurrence control on ice depth; geophysical detection of massive vs cemented ice",
  "Same latitude/climate mismatch as E01; ice type differs (massive ice vs ice-cemented); all evidence is abstract-level; site coordinates still not found; Heldmann (10-60 cm) and Kowalewski (40-80 cm) depth ranges differ by site/definition and were not reconciled",
  "待補證據",
  "Now has two peer-reviewed abstracts with numbers (sublimation, till depth) and a snow-recurrence link, but no coordinates, no temperature tables, and no full text read",
  "Sublimation of 0.017 mm over 6 weeks and 40-80 cm till depth are Beacon Valley values; Bannister 100 m depth is not peer-reviewed and not cross-checked",
  "Read Kowalewski 2006 and McKay 2009 full text for site coordinates and instrument/depth details; read Marchant & Head 2007 (not yet read)"],
 ["MS-02-E03", "Adventdalen, central Spitsbergen, Svalbard (Norway)",
  78.1722, 16.0613,
  "Valley floor/terraces of Adventdalen (~40 km long, up to ~3 km wide); point anchor = ADE terrace site; HRSC-AX polygon sites span 78.182-78.206°N, 15.79-16.559°E (8 sites); polygon troughs surveyed by WISDOM team",
  "Hauber 2011 p.113 (valley dimensions, no coordinates); Rotem 2023 (ADE 78.1722°N 16.0613°E, 23 m a.s.l.; valley centre 78.110°N 16.180°E); PANGAEA 921087 site table (bounding box and 8 site coordinates, CC BY 4.0)",
  "Svalbard Airport climate 1912-1993 (Hauber Table 1 p.114); Adventdalen 'Polygons' MAAT -5.8 °C (Rotem 2023); HRSC-AX DEMs 0.5-1 m (Hauber pp.112-113); WISDOM GPR Mar 2022 (Brighi 2025); loess OSL record (Rasmussen 2023); PANGAEA polygon geomorphometry dataset (site table read; polygon values are in zip files that could not be downloaded); UNISCALM CALM active-layer series on a loess terrace (since 2000; AGU 2016 abstract)",
  "Ice-wedge polygons and mantled ground ice; aeolian silt cover (loess) building syngenetic permafrost; radar detection of ice beneath an active layer; polygon geometry vs Mars (Hauber)",
  "Latitude 78°N; thicker, wetter, vegetated-valley setting not described in what I read; MAAT -5.8 °C; saline/epigenetic permafrost part (Rotem); polygons 10-20 m vs Mars example 5-10 m (Hauber Fig 4)",
  "保留",
  "Best-documented case for the 'mantle + wind + ice detection' questions (H2, H3): measured loess accumulation rate, polygon-trough GPR ice reflector, and a published Mars mid-latitude landform comparison",
  "Svalbard loess accumulation rates and active-layer depth cannot be transferred to Mars dust deposition or MS-02 cover thickness; GPR ε values are for Earth materials",
  "Download the polygon zip files (PANGAEA 10.1594/PANGAEA.921087; blocked from this sandbox) and read Hauber Section 3 for polygon statistics; read the SESS 2018 report PDF (Zenodo 4777825; unreadable via the fetch tool) for Adventdalen borehole temperatures"],
 ["MS-02-E04", "Haughton River Valley, Haughton impact structure, Devon Island, Nunavut (Canada)",
  75.37, -89.53,
  "Nine LiDAR grids (0.1-0.5 m/px) within ~3.9 km N-S x ~4.0 km E-W (this-study calc from Table 3.1 UTM 16N); valley ~1.5 km wide, elevation 75-151 m a.s.l.",
  "Andres 2020 Table 3.1 (UTM 16N grids converted to 75.359-75.394°N, 89.510-89.655°W) and Fig 1.8 p.20 (75.37, -89.53); the structure centre 75°22'N 89°41'W (p.6) is a different anchor ~4.3 km away",
  "MAAT ~-16 °C Devon / ~-15 °C valley (cited, Andres p.1,6); LiDAR 2016 (36 DEMs, 9 analysed); thaw depth 0.52-0.67 m (2019, Andres pp.102-106); polygon/stripe diameters 5-31 m (pp.114-115); GPR 250 MHz and seismic at the Haughton base camp/landing strip (Nieto & Stewart 2003; CSEG article) giving permafrost top ~0.6-0.9 m; no Haughton ground-ice quantity",
  "Polar-desert patterned-ground geometry (polygons, stripes, stone circles) and active-layer thaw depth at LiDAR scale; Arcadia-class comparison only via Hibbard thesis (abstract)",
  "Impact structure setting at 75°N, MAAT ~-15 to -16 °C; ground-ice content (10-20%) is a Canadian High Arctic generality, not Haughton data; Axel Heiberg GPR/ice-wedge volume is a different site; author states nine grids in a very small locale may not generalise (p.115)",
  "待補證據",
  "Measured thaw depth (2019), polygon geometry, and GPR/seismic permafrost-top depths (~0.6-0.9 m) exist, but no Haughton ground-ice quantity, no borehole temperature series (a '-17 °C crater average' is stated without period or depth), and no Mars-point comparison were found",
  "Thaw depth (0.52-0.67 m, July 2019) and GPR permafrost-top depth are snapshots from different sites in the valley; the 10-20% ice content must not be applied to Haughton or MS-02",
  "Find a Haughton borehole/ground-temperature series (searches so far found none); the Hibbard dissertation text does not name Devon/Haughton in its abstract, so its body would need to be read from the repository PDF"],
]

# ------------------------------------------------------------------ evidence
ev_cols = ["evidence_id", "candidate_id", "facet", "variable", "value", "unit", "evidence_type",
           "observation_period", "depth_or_height", "resolution_or_representative_extent",
           "source", "locator", "limitation_or_comparability"]
E = []
def ev(cid, facet, var, val, unit, typ, per, dep, res, src, loc, lim):
    E.append([f"EV-{len(E)+1:03d}", cid, facet, var, val, unit, typ, per, dep, res, src, loc, lim])

M = "MS-02"
ev(M, "地形", "MOLA elevation mean (min/max)", "-3898.7 (-3956 / -3839)", "m relative to areoid", "產品推估(MOLA MEGDR gridded)",
   "MGS mapping; exact dates in PDS labels (not extracted)", "surface", "64/64 native cells in 0.5° nominal cell (~29.6 x 17.9 km)",
   SRC["HANDOFF"] + HF + " cols mola_elevation_m_*; " + HN, "MS-02 row", "MEGDR interpolates between tracks; no laser-density mask obtained (hand-off report p.40 statement)")
ev(M, "地形", "MOLA slope mean (median / max)", "0.302 (0.207 / 0.925)", "degrees", "產品推估",
   "MGS mapping", "surface", "~3.7 km baseline", SRC["HANDOFF"] + HF, "col mola_slope_deg_*", "Regional slope, not local traversability or hazard")
ev(M, "地形", "MOLA relief within nominal cell", "117", "m", "產品推估", "MGS mapping", "surface", "0.5° cell", SRC["HANDOFF"] + HF, "col mola_relief_m",
   "Regional relief only; says nothing about meter-scale hazards")
ev(M, "熱性質", "TES nighttime thermal inertia mean (median; min-max; valid cells)", "217.27 (213; 177-276; 93/100)", "J m-2 K-1 s-0.5", "產品推估(TES TI map, infill mask excluded)",
   "Not given in PDS label (2007 = product creation, not observation year)", "diurnal skin depth (not a stated depth)", "~3 km, 100 native cells",
   SRC["HANDOFF"] + HF + "; " + HN, "cols TES_TI_*", "Thermal inertia is not temperature or hardness; no ice-depth inversion implied; 7 infill cells excluded")
ev(M, "熱性質", "MCS surface temp median at 03 / 15 LTST; paired contrast", "171.27 / 246.31; 66.83", "K", "產品推估(model time-adjusted MCS; author-code)",
   "MY29-36; 75 paired year-season bins of 288 possible", "surface (brightness temp; depth n/a)", "5° bin centred (55.0N,170.0E), ~146.7 km from MS-02 (this-study calc)",
   SRC["HANDOFF"] + HF, "cols MCS_*", "Populated-bin medians, not annual mean or amplitude; QA, counts, uncertainty absent; not comparable to Earth MAAT")
ev(M, "水/冰", "SWIM 0-1 m consistency mean (min-max)", "0.693 (0.665-0.784)", "dimensionless consistency (not %, not probability)", "產品推估(SWIM2 composite 2021)",
   "multi-instrument composite; no single period", "0-1 m zone", "100/100 native cells; provider gives no composite resolution on product page",
   SRC["SWIM"] + " ; " + SRC["HANDOFF"] + HF, "cols SWIM_0_1m_*", "Consistency with ice, not abundance or probability; 0-1 m inputs: neutron, thermal, shallow geomorphology, radar surface power")
ev(M, "水/冰", "SWIM 1-5 m consistency mean (median; max)", "0.622 (0.5; 1.0)", "dimensionless consistency", "產品推估",
   "multi-instrument composite", "1-5 m zone", "100/100 native cells", SRC["SWIM"] + " ; " + SRC["HANDOFF"] + HF, "cols SWIM_1_5m_*",
   "Shares inputs with 0-1 m (geomorphology, radar); not independent confirmation; median at the 0.5 floor value")
ev(M, "大氣/沙塵", "MY34 CDOD (9.3 µm abs, column) mean / p95 / max", "0.1254 / 0.2400 / 0.4525", "dimensionless optical depth", "產品推估(Montabone reconstruction v2.5)",
   "MY34, 669 reconstructed sols; max at Ls 327.5°", "local total column", "3°x3° cell centred (52.5N,168.0E), ~17.3 km from MS-02 (this-study calc)",
   SRC["HANDOFF"] + HF + "; " + HN, "cols dust_my34_*", "Not wind speed, deposition rate or surface pressure; reliability is provider index, not a probability")
ev(M, "大氣/沙塵", "MY35 CDOD mean / p95 / max", "0.1101 / 0.1731 / 0.3152", "dimensionless optical depth", "產品推估",
   "MY35, 669 sols; max at Ls 41.9°", "local total column", "same 3° cell", SRC["HANDOFF"] + HF, "cols dust_my35_*", "Same limits as MY34; MY35 differs from MY34 in season of max")
ev(M, "大氣/沙塵", "Seasonal CDOD means Ls 0-90/90-180/180-270/270-360", "MY34 0.129/0.109/0.153/0.113; MY35 0.141/0.107/0.090/0.093", "dimensionless", "產品推估",
   "MY34, MY35", "local column", "3° cell", SRC["HANDOFF"] + HN, "dust_my34/35 seasons_by_Ls", "Season dust opacity cannot be converted to aeolian transport")
ev(M, "地形", "Chart/quadrangle containing MS-02", "Cebrenia quadrangle MC-7: 30-65°N, 120-180°E (includes parts of Utopia Planitia and Arcadia Planitia, and Phlegra Montes)", "n/a", "文獻(圖幅範圍)", "n/a", "n/a", "quadrangle scale",
   "https://en.wikipedia.org/wiki/Cebrenia_quadrangle ; https://pubs.usgs.gov/publication/i1140", "extent and feature list; USGS IMAP 1140 (Elston 1979) abstract",
   "52.75°N, 168.25°E lies inside MC-7 (this-study check); the quadrangle only includes PART of Arcadia, so this does NOT establish that MS-02 is in Arcadia Planitia; geologic unit at MS-02 not read from the plate")
ev(M, "水/冰", "Regional context: Arcadia Planitia highlighted as high ice-consistency", "qualitative", "n/a", "文獻(摘要)",
   "SWIM composite basis (Morgan 2021)", "SWIM depth zones", "northern mid-latitudes", SRC["MORGAN"], "abstract",
   "Abstract names Arcadia and Deuteronilus; no numeric latitude range or depths; MS-02 is not shown to be inside the Arcadia area Morgan et al. describe")

U = "MS-02-E01"
ev(U, "地形", "Elevation (valley / met station)", "~1700 / 1677", "m a.s.l.", "實測", "station coordinates", "n/a", "valley floor site", SRC["MARINOVA"], "p.145-146",
   "Slope, relief, local DEM not read: 未知")
ev(U, "熱性質", "Mean annual air temperature (max/min)", "-23.4 (0.4 / -45.5) = 249.75 K (this-study conversion)", "°C", "實測", "2010-2013 average (station from 11 Dec 2009 to 31 Jan 2013)", "air 1.2 m", "single met station",
   SRC["MARINOVA"], "Table II p.153", "Air temperature, not comparable with Mars MCS 03/15 LTST surface medians")
ev(U, "熱性質", "Ground temperature mean at 10 / 42 (ice table) / 49 cm", "-24.3 / -24.1 / -24.0", "°C", "實測", "2010-2013 average", "10, 42, 49 cm", "single profile",
   SRC["MARINOVA"], "Table II p.153; sensors p.146-147", "Surface sensors can be covered by thin soil wind may remove (p.146,151); thermal inertia of soil not read: 未知")
ev(U, "水/冰", "Depth to ice-cemented ground at met station; spatial range", "42 cm; ~0 to >100 cm along valley floor", "cm", "實測", "3 summer field visits + station", "0-100+ cm", "valley floor",
   SRC["MARINOVA"], "p.145-146, p.152", "Ice-cemented ground, not massive ice; one station value")
ev(U, "水/冰", "Active layer thickness", "~15 (mean 13.2 ± 2.2 over four summers)", "cm", "實測", "four summers", "0-~15 cm", "station", SRC["MARINOVA"], "p.152", "Dry permafrost cover, no melt observed at surface in 3 summers (p.156)")
ev(U, "水/冰", "Time at 42 cm ice table with a_w>0.6 and T>-18 °C", "~2560 h (~29-30% of year; 2560/8760 = 0.292 this-study calc)", "h per year", "實測+模式(energy-balance model)", "2010-2013", "42 cm", "station",
   SRC["MARINOVA"], "p.161, Fig. 6", "Special Region criteria (Rummel 2014); model tuned to a 10-day warm period (p.153-154)")
ev(U, "水/冰", "Ice depth range in University and Middle Beacon valleys", "10-60", "cm", "文獻(摘要)", "n/a", "10-60 cm", "two valleys", SRC["HELDMANN"], "abstract (truncated excerpt)", "Abstract only")
ev(U, "熱性質", "Soil thermal conductivity: dry soil / ice-cemented ground (literature values used by Marinova)", "0.6 ± 0.1 / 2.5 ± 0.5", "W m-1 K-1", "文獻(引用 McKay et al. 1998)", "n/a", "dry soil; ice-cemented ground", "Linnaeus Terrace samples (as cited)",
   SRC["MARINOVA"], "Appendix p.165", "Conductivity, not thermal inertia; density and heat capacity not read, so thermal inertia is NOT derived; Marinova's own diffusivity estimates are method-dependent (p.167-171)")
ev(U, "熱性質", "Thermal diffusivity of ice-cemented ground", "1.0e-6", "m2 s-1", "本文推導(由 k=2.5 W m-1 K-1 與 McKay 密度、熱容)", "n/a", "ice-cemented ground", "n/a", SRC["MARINOVA"], "Appendix p.171",
   "Assumes properties from McKay et al.; Fourier method assumes constant properties with depth, which fails for dry soil over ice (p.165-171)")
ev(U, "大氣/沙塵", "Snow recurrence control on depth of ice (windblown snow from plateau creates a depth gradient to ice-cemented ground in University Valley)", "qualitative; Linnaeus Terrace: ~2 yr recurrence fits ice at 25 cm under 12.5 cm dry permafrost", "yr; cm", "文獻(摘要,模式推論)", "n/a", "ice at 25 cm (Linnaeus Terrace)", "valley scale",
   "https://doi.org/10.1017/S0954102008001508", "abstract", "Abstract only; Linnaeus Terrace is not University Valley; proposed Mars relevance is a possibility, not shown")
ev(U, "大氣/沙塵", "Wind speed", "not reported in the portions of the paper read", "n/a", "未知", "2009-2013", "1.08 m (sensor)", "station", SRC["MARINOVA"], "p.146 sensor list; text 0-121,921 chars read", "Sensor exists; wind-speed values not found in text read: 未知; optical-depth analog not available")

B = "MS-02-E02"
ev(B, "水/冰", "Ground ice type and depth, middle Beacon Valley", "massive ground ice; 10-60", "cm", "文獻(摘要)", "n/a", "10-60 cm", "valley", SRC["HELDMANN"], "abstract", "Abstract only; no table read")
ev(B, "水/冰", "Buried massive ice depth range (geophysics)", ">100 m (deeper than previously thought)", "m", "文獻(大學部論文摘要)", "survey (2007 thesis)", ">100 m", "1.3 km transect", SRC["BANNISTER"], "abstract", "Undergraduate thesis; not peer-reviewed; not cross-checked; interpretation not verified")
ev(B, "水/冰", "Depth of sublimation till over buried glacier ice, central Beacon Valley", "40-80", "cm", "實測(文獻摘要)", "2004-11-18 to 2004-12-29", "40-80 cm", "central Beacon Valley (coordinates not given in abstract)",
   "https://doi.org/10.1017/S0954102006000460", "abstract", "Abstract only; differs from Heldmann (10-60 cm) - not reconciled")
ev(B, "水/冰", "Net summertime loss of buried ice", "~0.017 (over the interval)", "mm", "實測(HOBO loggers)", "2004-11-18 to 2004-12-29", "ice surface under till", "central Beacon Valley",
   "https://doi.org/10.1017/S0954102006000460", "abstract", "Net loss falls to zero if air T drops 5.5 °C (-7 to -12 °C), mean RH rises 22% (~36 to 58%), or snowmelt infiltration ~0.002 mm/day; abstract only")
ev(B, "大氣/沙塵", "Snow recurrence implication on Beacon Valley floor", "dry permafrost without ice-cemented ground implies recurrence >10 yr; massive ice not stable", "yr", "文獻(摘要,模式推論)", "n/a", "valley floor", "valley",
   "https://doi.org/10.1017/S0954102008001508", "abstract", "Inference from a model; abstract only")
ev(B, "熱性質", "Temperatures, thermal properties", "not found", "n/a", "未知", "n/a", "n/a", "n/a", "n/a", "n/a", "No primary temperature table read")

S = "MS-02-E03"
ev(S, "地形", "Valley dimensions", "~40 km long, up to ~3 km wide", "km", "文獻", "n/a", "n/a", "valley", SRC["HAUBER"], "p.113", "No coordinates in paper; ADE terrace elevation 23 m a.s.l. (Rotem 2023)")
ev(S, "地形", "Polygon diameter (Adventdalen vs Mars example)", "10-20 vs 5-10", "m", "文獻(測量+影像)", "HRSC-AX flights Jul-Aug 2008; field 2008-2009", "surface", "HRSC-AX DEM grid 0.5-1 m", SRC["HAUBER"], "Fig 4 p.115, pp.112-113", "Morphology alone does not identify polygon type (equifinality p.121)")
ev(S, "熱性質", "Mean annual air temperature", "Svalbard Airport -6.3 (SD 1.7), 1912-1993; Adventdalen 'Polygons' -5.8 = 267.35 K (this-study conversion)", "°C", "實測", "1912-1993; 'current' (Rotem, year not stated)", "air", "airport/valley station", SRC["HAUBER"] + " ; " + SRC["ROTEM"], "Table 1 p.114; Rotem text", "Not same period for both values; Rotem value not period-specific")
ev(S, "水/冰", "Active-layer thickness, valley bottom", "60-100", "cm", "文獻(引用先前研究)", "present-day typical", "0-100 cm", "valley bottom sediments", SRC["ROTEM"], "text (cited studies)", "Secondary citation, not a direct measurement by Rotem")
ev(S, "水/冰", "Permafrost thickness in major valleys", "~100", "m", "文獻", "n/a", "to ~100 m", "regional", SRC["HAUBER"], "p.113", "Regional estimate")
ev(S, "水/冰", "GPR ice-like reflector in polygon trough: depth, permittivity (ice vs active layer)", "~1.5 m; ε≈3.2 vs ε≥7", "m; dimensionless", "實測+模擬", "March 2022", "~1.5 m", "4 parallel lines over 2 troughs; 0.5-3 GHz; cm resolution",
   SRC["BRIGHI"], "abstract", "Abstract only; purpose was ExoMars WISDOM validation, not MS-02")
ev(S, "大氣/沙塵", "Loess deposition rate / mass accumulation rate (max)", "up to 0.35 cm/yr; ~2900 g m-2 yr-1", "cm/yr; g m-2 yr-1", "實測(OSL core, 136 ages)", "last ~3000 years", "core", "single core, Adventdalen",
   SRC["RASMUSSEN"], "abstract", "Earth dust source/wind regime; cannot be converted to Mars deposition; ice content increases with depth (syngenetic permafrost)")
ev(S, "大氣/沙塵", "Annual precipitation, Svalbard Airport", "180.7 (SD 49.8; 86.4-317.0)", "mm", "實測", "1912-1993", "gauge", "airport", SRC["HAUBER"], "Table 1 p.114", "Atmosphere/pressure/humidity regime differ from Mars: 未知 for direct comparison")

ev(S, "水/冰", "Active-layer thickness at UNISCALM (CALM site on a loess-covered terrace): early vs later period", "<1 m for the first six years (min 74 cm in 2005); ≥1 m since 2006; increasing over 17 years", "cm / m", "實測(機械探測+地溫內插)", "2000-2016 (abstract Dec 2016)", "active layer", "single CALM grid, Adventdalen",
   "https://ui.adsabs.harvard.edu/abs/2016AGUFMGC31H1202S", "abstract (authors not shown on page; bibcode 2016AGUFMGC31H1202S)",
   "Newer than the 60-100 cm values cited by Rotem 2023; interannual variability reported as large; abstract only")
ev(S, "熱性質", "Permafrost thermal state, Adventdalen: 11 boreholes across five Svalbard sites, hydrological year 2016-2017", "values not extracted (report PDF unreadable via fetch)", "°C", "未知", "2016-2017", "depths not stated on the record page", "five sites incl. Adventdalen",
   "https://doi.org/10.5281/zenodo.4777825", "record page (Christiansen et al. 2019, SESS report 2018, ch.1)", "Dataset exists; Adventdalen temperatures not read: 未知")
ev(S, "地形", "HRSC-AX polygon-pattern sites (8) with mapped geometry parameters", "bbox 78.182-78.206°N, 15.79-16.559°E; parameters: area, perimeter, length, width, thickness ratio, circularity", "m2; m; ratios 0-1", "實測(航空立體影像製圖)", "2009 campaign", "surface", "polygon networks, shapefiles",
   "https://doi.pangaea.de/10.1594/PANGAEA.921087", "dataset page, Ulrich, Härtel & Hauber 2020, CC BY 4.0", "Polygon values are in zip files that could not be downloaded here; resolution and polygon counts not stated on the page")

H = "MS-02-E04"
ev(H, "地形", "Coordinates: impact-structure centre vs Haughton River Valley study area", "75°22'N 89°41'W (structure, p.6) vs 75.37°N, 89.53°W (study area, Fig 1.8 p.20); separation ~4.3 km (this-study calc)", "degrees", "文獻+本次計算", "n/a", "n/a", "structure (23 km diameter) / valley ~1.5 km wide",
   SRC["ANDRES"], "sec 1.2.2 p.6; Fig 1.8 p.20; sec 3.2", "Two different anchors, not an error; the nine LiDAR grids of Table 3.1 convert (UTM 16N, this-study calc) to 75.359-75.394°N, 89.510-89.655°W")
ev(H, "地形", "LiDAR coverage: grids, resolution, elevation", "9 grids analysed of 36 DEMs; 0.1 m/px (7 grids) and 0.5 m/px (2 grids); grid elevations 93-198 m; valley 75-151 m a.s.l.", "m", "實測(LiDAR 2016)", "summer 2016 campaign (4 weeks)", "surface", "0.1-0.5 m",
   SRC["ANDRES"], "sec 3.3.1; Table 3.1; pp.112,116", "Nine grids in a very small locale (author, p.115); elevation range includes stone-stripe and plateau grids")
ev(H, "水/冰", "Thaw depth (active layer) in July 2019", "0.67 (grid 16N); 0.52 (16AD); 0.55 (Stone Stripes, 25 Jul); 0.59 (East Camp Polygons, 19 Jul); >1.0 estimated at stone-circle grids", "m", "實測(探針/挖掘)", "July 2019", "0-0.67 m", "per grid",
   SRC["ANDRES"], "pp.95, 102, 105, 106", "Single-season snapshot; stone-circle sites unreachable because of coarse substrate; not a ground-ice measurement")
ev(H, "熱性質", "Mean annual air temperature (Devon Island; Haughton River valley)", "~-16 (Lev & King 1999 cited); ~-15 (valley)", "°C", "文獻(引用)", "n/a", "air", "regional", SRC["ANDRES"], "p.6; p.1", "Secondary citations; no period given")
ev(H, "水/冰", "Ground ice content, upper 10-20 m, Canadian High Arctic", "10-20", "%", "文獻(一般)", "n/a", "0-20 m", "regional generality", SRC["ANDRES"], "p.29", "General High Arctic range, NOT Haughton-specific")
ev(H, "地形", "Patterned-ground geometry at Haughton River Valley", "polygons and stripes 5-31 m diameter; stone circles and mud boils 0.5-1.2 m; East Camp Polygons mean area 983.86 ± 451.71 m2; trough intersection ~4.00 m wide, ~0.30 m high", "m; m2", "實測(LiDAR 0.5 m/px 解析)", "2016 LiDAR; 2019 field", "surface", "East Camp Polygons grid",
   SRC["ANDRES"], "pp.106-107, 114-115", "Table 2.1 in the thesis is Strand Fiord (Axel Heiberg), not Haughton; cannot be mixed")
ev(H, "水/冰", "Polygon width range (general, from thesis background table)", "0.5-10", "m", "文獻(一般)", "n/a", "surface", "general", SRC["ANDRES"], "Table 1.1 p.12", "General background range, not Haughton data")
ev(H, "水/冰", "Haughton ground-ice quantity, GPR, borehole temperatures", "not found in text read", "n/a", "未知", "n/a", "n/a", "n/a", SRC["ANDRES"], "chapter 3 (extracted text, 3 chunks; some tables absent); no Haughton GPR; 43.28 m3 ice-wedge volume is Strand Fiord (p.123)", "The 10-20% ice content is a Canadian High Arctic generality; Axel Heiberg values cannot be used for Haughton")
ev(H, "水/冰", "GPR depth to frozen ground (top of permafrost), Haughton base camp 3D and landing strip", "0.60-0.78 (base camp 3D; ~0.65 on p.11); 0.7-0.9 (landing strip quasi-3D)", "m", "實測(GPR 250 MHz)", "Devon Island field survey (report vol. 15, 2003)", "0.6-0.9 m", "3D grids near base camp / landing strip; no site coordinates",
   "https://www.crewes.org/Documents/ResearchReports/2003/2003-08.pdf", "Nieto & Stewart 2003: abstract p.1; p.11; conclusions p.14-15", "Thawed-layer velocity ~0.065 m/ns from rebar test; diffractions interpreted as ice lenses or cobbles at the permafrost top; no ice thickness quantified (pp.1,3,11)")
ev(H, "水/冰", "Seismic P/S velocity: near-surface silt vs permafrost", "silt Vp 260 / Vs 168; permafrost Vp 3100 / Vs 2060", "m/s", "實測(多分量地震)", "2002 survey", "top ~0.6 m is silt", "Haughton base area",
   "https://csegrecorder.com/articles/view/mars-in-canada-the-nasa-haughton-mars-project-devon-island-nunavut", "CSEG Recorder article (R. R. Stewart; year not stated on page), Fig. 9", "Preliminary interpretation; article swaps latitude/longitude labels in its coordinate sentence")
ev(H, "熱性質", "'Crater average' temperature stated in the article summary", "-17", "°C", "文獻(未註明量與期間)", "not stated", "not stated", "crater", "https://csegrecorder.com/articles/view/mars-in-canada-the-nasa-haughton-mars-project-devon-island-nunavut", "Summary section",
   "Not stated whether air or ground, nor the period; not used in comparisons; Andres cites about -16 °C (Devon) and about -15 °C (valley)")
ev(H, "大氣/沙塵", "Dust / wind / loess", "not found", "n/a", "未知", "n/a", "n/a", "n/a", "n/a", "n/a", "Not covered in text read")

# ------------------------------------------------------------------ prior work
pw_cols = ["prior_id", "candidate_id", "work", "venue_doi_or_url", "site_covered", "purpose", "classification_vs_MS02_use",
           "read_scope", "difference_in_question", "difference_in_scope", "difference_in_data", "difference_in_method", "note"]
P = [
 ["PW-01", "MS-02-E01;MS-02-E02", "Heldmann et al. 2013, The high elevation Dry Valleys in Antarctica as analog sites for subsurface ice on Mars", SRC["HELDMANN"],
  "University Valley; middle Beacon Valley", "Mars subsurface-ice analog; compare surface features with Phoenix site", "部分重疊",
  "Abstract only (truncated excerpt)", "Asks whether surface features indicate ground ice (Phoenix, 68.2°N); MS-02 asks cover/season/wind effects on ice detection at 52.75°N",
  "Two valleys; no MS-02 or mid-latitude plains target", "Not read beyond abstract", "Not read", "Same site, Mars shallow-ice purpose; does not use MS-02 data"],
 ["PW-02", "MS-02-E01", "Marinova et al. 2022, Climate and energy balance of the ground in University Valley, Antarctica", SRC["MARINOVA"],
  "University Valley", "Ground energy balance; compare Special Region criteria; cites Phoenix 68.2°N", "部分重疊",
  "Extracted text characters 0-121,921 (two reads): body pp.145-162 and thermal-property appendix pp.165-171", "Energy-balance/habitability question; MS-02 asks ice detectability given cover/dust/season",
  "One valley, one station cluster", "Air/ground T, RH, wind; 2009-2013", "Surface energy-balance model tuned to a 10-day window", "Only Mars site cited is Phoenix"],
 ["PW-03", "MS-02-E02", "Bannister 2007, Polygonal patterned ground and ancient buried ice on Mars and in Antarctica (undergraduate thesis)", SRC["BANNISTER"],
  "Victoria Valley; Beacon Valley", "Geophysical survey of polygons and buried ice for Mars interpretation", "部分重疊", "Abstract only",
  "Geophysics of ice depth; not cover/season effects on orbital-scale ice indicators", "1.3 km transects", "Resistivity, GPR, TDEM, magnetics", "Ground survey", "Low evidence tier"],
 ["PW-04", "MS-02-E03", "Hauber et al. 2011, Landscape evolution in Martian mid-latitude regions: insights from analogous periglacial landforms in Svalbard", SRC["HAUBER"],
  "Adventdalen (main), Brøgger Peninsula and others", "Analog for Mars mid-latitude (30-60°) periglacial landforms", "部分重疊 (same site, related mid-latitude Mars purpose; no MS-02/Arcadia)",
  "Whole paper text provided by fetch (pp.111-131 summarized)", "Landform genesis; MS-02 asks ice detection under mantle and season",
  "Mars examples at 34.6°S, 38.5°S, 71.9°N, others; Arcadia/Acidalia not mentioned", "HRSC-AX 0.5-1 m DEM, CTX, HiRISE, climate table", "Morphological comparison, qualitative scenarios", "Authors state scenarios are not expected to represent Mars exactly (p.125)"],
 ["PW-05", "MS-02-E03", "Brighi et al. 2025, Performance validation of WISDOM GPR on a Martian analogue dataset in Svalbard", SRC["BRIGHI"],
  "Adventdalen (polygon troughs, ice cave, sandstone)", "Validate ExoMars GPR processing", "部分重疊 (method), 用途不同 (target: Oxia Planum)", "Abstract only",
  "Instrument validation vs MS-02 hypothesis testing", "Oxia Planum, 2 m drill target", "WISDOM FDTD, polarimetry, bandwidth extrapolation", "GPR simulation", "Shows ice-like reflector detectable in troughs at Adventdalen"],
 ["PW-06", "MS-02-E03", "Rasmussen et al. 2023, High-resolution OSL dating of loess in Adventdalen", SRC["RASMUSSEN"], "Adventdalen", "Loess/dust history and permafrost development", "用途不同",
  "Abstract only", "No Mars question", "Single core", "OSL ages every 2 cm", "OSL + Bayesian age model", "Provides Earth dust-accumulation rates"],
 ["PW-07", "MS-02-E04", "Andres 2020, A Periglacial Landsystem Analysis in the Canadian High Arctic (MSc thesis)", SRC["ANDRES"], "Devon Island/Haughton; Axel Heiberg", "Landsystem tool for planetary geomorphology", "部分重疊",
  "Extracted text characters 0-257,352 in three reads (some tables absent, e.g., Table 3.3)", "Landsystem mapping and thaw depth vs MS-02 ice-detection questions", "Haughton River Valley (9 grids) and Strand Fiord (Axel Heiberg); Mars discussion mentions Oxia Planum/Jezero, not Arcadia", "LiDAR 0.1-0.5 m, thaw depth 2019, GPR only at Strand Fiord", "Landsystem analysis", "Author: nine grids in a very small locale may not generalise (p.115)"],
 ["PW-08", "MS-02-E04", "Hibbard (PhD, Western), Surface Morphology and Subsurface Ice Content Relationships in Arcadia Planitia, Mars and the Canadian High Arctic", SRC["HIBBARD"],
  "Arcadia Planitia; unnamed Canadian High Arctic sites", "Ice-related features for ISRU landing-site ice access", "證據不足 (same-site match unknown; closest regional-class precedent)",
  "Abstract pages (two repository records); year 2021 per the second record, authorship inferred from the PDF file name", "Feature/ice-access mapping vs MS-02 cover/season/wind questions", "No coordinates or named Arctic sites on page", "Orbital data, GPR, LiDAR", "Morphology-ice relationship", "Must read body before claiming relation to MS-02"],
 ["PW-09", "MS-02", "Morgan et al. 2021, Availability of subsurface water-ice resources in the northern mid-latitudes of Mars", SRC["MORGAN"], "Northern mid-latitudes (Arcadia, Deuteronilus)", "SWIM composite ice-consistency maps", "用途不同 (Mars-side context)",
  "Abstract page", "Defines the ice-consistency scoring MS-02 uses", "Mars only", "Orbital datasets", "Composite consistency", "Not an Earth-analog precedent"],
 ["PW-11", "MS-02-E02", "Kowalewski, Marchant, Levy & Head 2006, Quantifying low rates of summertime sublimation for buried glacier ice in Beacon Valley, Antarctica", "https://doi.org/10.1017/S0954102006000460",
  "Central Beacon Valley", "Sublimation rate of buried glacier ice under sublimation till", "用途不同 (no Mars use in abstract)", "Abstract only",
  "Ice-loss rate vs MS-02 detectability question", "One valley, 6-week summer interval", "HOBO temperature/humidity loggers", "Energy/vapour sensitivity analysis", "Gives till depth 40-80 cm and net loss ~0.017 mm"],
 ["PW-12", "MS-02-E01;MS-02-E02", "McKay 2009, Snow recurrence sets the depth of dry permafrost at high elevations in the McMurdo Dry Valleys of Antarctica", "https://doi.org/10.1017/S0954102008001508",
  "Linnaeus Terrace; University Valley; Beacon Valley floor", "Model of snow recurrence controlling ice-cemented-ground depth; Mars possibility proposed", "部分重疊", "Abstract only",
  "Snow/wind control on ice depth vs MS-02 cover/dust question", "Dry Valleys; no Mars site", "Model with field depth constraints", "Snow recurrence model", "Proposes Mars relevance as possible, not demonstrated (abstract)"],
 ["PW-13", "MS-02", "Elston 1979, Geologic map of the Cebrenia quadrangle of Mars (USGS IMAP 1140)", "https://pubs.usgs.gov/publication/i1140",
  "Cebrenia quadrangle MC-7 (30-65°N, 120-180°E)", "Regional geologic context for MS-02", "用途不同 (Mars-side context)", "USGS abstract only; plate not read",
  "Geologic mapping, not ice detection", "Quadrangle scale (1:4,336,000)", "Viking-era map", "Geologic mapping", "Abstract mentions circumpolar plains with wind, glacial and periglacial processes; formal units at MS-02 not read"],
 ["PW-14", "MS-02-E04", "Nieto & Stewart 2003, Geophysical experiments in periglacial environments: Devon Island, Nunavut (CREWES Research Report vol. 15)", "https://www.crewes.org/Documents/ResearchReports/2003/2003-08.pdf",
  "Haughton base camp, Greenhouse and landing strip (no coordinates)", "GPR survey of permafrost top at a Mars-like site", "部分重疊", "Text of the report as extracted by the fetch tool (summary-level)",
  "Method test and permafrost-top depth vs MS-02 cover/dust/season ice-detection questions", "Local 3D grids near camp", "GPR 250 MHz; velocity calibration", "Geophysical survey", "Calls Haughton one of the most Mars-like places on Earth; no direct GPR-Mars comparison"],
 ["PW-15", "MS-02-E04", "Stewart (CSEG Recorder), Mars in Canada: the NASA Haughton-Mars Project, Devon Island, Nunavut", "https://csegrecorder.com/articles/view/mars-in-canada-the-nasa-haughton-mars-project-devon-island-nunavut",
  "Haughton structure", "Overview of HMP geophysical surveys", "用途不同", "Article text via fetch; year not stated", "Overview vs hypothesis testing", "Haughton", "GPR, seismic", "Geophysical survey", "Gives seismic velocities and permafrost top ~60 cm; mentions Mars only generally"],
 ["PW-16", "MS-02-E03", "Ulrich, Härtel & Hauber 2020, Mapped polygon pattern geomorphometry from HRSC-AX, 2009, Adventdalen (PANGAEA dataset)", "https://doi.pangaea.de/10.1594/PANGAEA.921087",
  "Adventdalen (8 sites)", "Polygon geometry data supporting Mars-analog comparison", "部分重疊", "Dataset page only (values in zip files not obtained)",
  "Geometry of polygons vs MS-02 ice-detection question", "8 sites in a ~25 km reach", "HRSC-AX 2009 mapped polygons", "Photogrammetric mapping", "CC BY 4.0"],
 ["PW-17", "MS-02-E03", "UNISCALM CALM monitoring, Adventdalen (AGU Fall Meeting 2016 abstract 2016AGUFMGC31H1202S) and Christiansen et al. 2019 SESS permafrost snapshot", "https://ui.adsabs.harvard.edu/abs/2016AGUFMGC31H1202S ; https://doi.org/10.5281/zenodo.4777825",
  "Adventdalen loess terrace; five Svalbard sites", "Permafrost thermal state and active-layer monitoring", "用途不同", "Abstract and record page only", "Climate monitoring, no Mars question", "Regional", "Active-layer probing, boreholes", "Monitoring", "Provides active-layer time series context"],
 ["PW-10", "MS-02-E01;MS-02-E02;MS-02-E03;MS-02-E04", "MS-02-specific Earth-analog precedent search (see search_log S02-S06, S12-S14, S19-S21, S30-S31, S37)", "see search_log.csv", "n/a",
  "Same Mars point + same Earth site + same use", "證據不足", "Search results listing only for most items", "n/a", "n/a", "n/a", "n/a",
  "No MS-02-specific precedent was found within searched platforms/terms; this is NOT proof it was never studied"],
]

# ------------------------------------------------------------------ search log
sl_cols = ["search_id", "date_taipei", "platform", "query_or_url", "purpose", "candidate", "records_used", "read_scope", "outcome"]
S_ = []
def sl(plat, q, purpose, cand, used, scope, out):
    S_.append([f"S{len(S_)+1:02d}", DATE, plat, q, purpose, cand, used, scope, out])
sl("WebFetch", SRC["SWIM"], "Confirm SWIM composite meaning", "MS-02", "SWIM2 products page", "page text", "Consistency, not abundance/probability; no resolution/units on page")
sl("WebSearch(standard)", "Beacon Valley buried ice Mars analog sublimation till", "E02 precedents", "E02", "Heldmann 2013; Bannister (via later query)", "titles/URLs only", "leads")
sl("WebSearch(standard)", "University Valley Antarctica ice-cemented ground Mars analog", "E01 precedents", "E01", "Marinova 2022; Heldmann 2013", "titles/URLs only", "leads")
sl("WebSearch(standard)", "Devon Island Haughton crater ground ice polygons Mars analog", "E04 precedents", "E04", "Andres thesis", "titles/URLs only", "leads")
sl("WebSearch(standard)", "Svalbard Adventdalen ice-wedge polygons loess Mars analog", "E03 precedents", "E03", "Hauber 2011; PANGAEA polygons dataset", "titles/URLs only", "leads")
sl("WebSearch(standard)", "Arcadia Planitia ground ice mid-latitude northern plains SHARAD thermal inertia", "Mars-side context", "MS-02", "Morgan 2021; SWIM abstracts", "titles/URLs only", "leads")
sl("WebFetch", "https://epic2-clone.awi.de/23057/1/Hau2010f.pdf", "Read Hauber 2011", "E03", "Hauber 2011", "pp.111-131 summary", "site list, Table 1, Fig 4, limits")
sl("WebFetch", "https://cambridge.org/core/services/aop-cambridge-core/content/view/S0954102022000025", "Read Marinova 2022", "E01", "Marinova 2022", "first 100,000 of 121,921 chars", "Table II, ice table, a_w, limits")
sl("WebFetch", "https://vufind-test.katalog.k.utb.cz/SummonRecord/FETCH-LOGICAL-c363t-2a3c1825fd50152c8509f6e9560ebde48abb9293d7fa6231df07c840826deaeb3", "Record for Heldmann 2013", "E01;E02", "Heldmann 2013", "abstract only", "10-60 cm ice depth")
sl("WebFetch", SRC["ANDRES"], "Read Andres thesis", "E04", "Andres 2020", "first 100,000 of 257,352 chars", "coordinates, MAAT, ground ice general values, limits")
sl("WebFetch", "https://link.springer.com/article/10.1038/s41550-020-01290-z", "Check Morgan 2021 page", "MS-02", "Morgan 2021", "page text (paywall)", "regions, no depths")
sl("WebSearch(standard)", "Beacon Valley Mars analog massive ground ice Heldmann OR Marchant OR Sugden", "More E02 precedents", "E02", "Bannister 2007 thesis; depth-to-ice paper lead", "titles/URLs only", "leads")
sl("WebSearch(standard)", "Morgan 2021 Arcadia Planitia ice consistency Nature Astronomy mid-latitude Mars subsurface ice", "Find Morgan 2021 open record", "MS-02", "USGS pubs record", "titles/URLs only", "lead")
sl("WebSearch(standard)", "Svalbard Mars analog ground ice radar GPR Adventdalen permafrost mid-latitude", "E03 GPR precedents", "E03", "Brighi 2025 EPSC-DPS abstract; SPLAM lead", "titles/URLs only", "leads")
sl("WebFetch", "https://pubs.usgs.gov/publication/70226786", "Morgan 2021 abstract", "MS-02", "Morgan 2021", "abstract", "Arcadia/Deuteronilus; no depths")
sl("WebFetch", "Cambridge Core via ezproxy (depth-to-ice-cemented soils)", "Tried to read Antarctic Science depth-to-ice paper", "E01;E02", "none", "not read", "Denied by access control (proxy URL); not retried or bypassed")
sl("WebFetch", SRC["BRIGHI"], "Read Brighi 2025 abstract", "E03", "Brighi 2025", "abstract", "March 2022, ε≈3.2 vs ≥7 at ~1.5 m")
sl("WebFetch", "https://openpolar.no/Record/ftzenodo:oai:zenodo.org:1154854", "Bannister 2007 record", "E02", "Bannister 2007", "abstract", "Beacon Valley >100 m ice (undergrad thesis)")
sl("WebSearch(standard)", "Adventdalen loess aeolian silt deposition permafrost active layer", "E03 aeolian evidence", "E03", "Rasmussen 2023; Rotem 2023", "titles/URLs only", "leads")
sl("WebSearch(standard)", "terrestrial analog for Arcadia Planitia Mars ground ice Earth analogue site", "Find Arcadia-class Earth analog precedents", "E04;MS-02", "Hibbard thesis", "titles/URLs only", "lead")
sl("WebSearch(standard)", "Haughton-Mars Project Devon Island permafrost active layer thickness ground temperature borehole", "E04 ground-temperature data", "E04", "none usable", "titles/URLs only", "No Haughton-specific borehole data found")
sl("WebFetch", SRC["HIBBARD"], "Read Hibbard thesis page", "E04", "Hibbard", "abstract page", "Arcadia + Canadian High Arctic; no coordinates/sites")
sl("WebFetch", "https://openpolar.no/Record/ftdtupubl:oai:pure.atira.dk:publications%2F600f63b0-8ab2-4bad-abef-3c49df1c8bea", "Rasmussen 2023 record", "E03", "Rasmussen 2023", "abstract", "0.35 cm/yr; 2900 g m-2 yr-1")
sl("WebFetch", "https://tc.copernicus.org/articles/17/3363/2023/", "Rotem 2023", "E03", "Rotem 2023", "first 100,000 of 114,191 chars", "ADE coordinates, MAAT, active layer")
sl("git/bash", "clone origin main; ls-remote; fetch handoff/verified-data-20261114", "Data availability", "MS-02", "repo", "tree + files", "xlsx 23,035,176 B and screened_pool 7,702,846 B present on handoff branch only")
sl("curl", "HEAD https://swim.psi.edu/output/SWIM2/Global/Composite/SWIM2_c0_1.tif", "Test raw-source access", "MS-02", "none", "n/a", "403 from sandbox proxy; raw products not recomputed")
sl("WebFetch", "Marinova 2022 text, offset 100000", "Finish reading Marinova", "E01", "Marinova 2022", "chars 100,000-121,921 (appendix pp.165-171)", "soil conductivity, diffusivity, limits; no wind values")
sl("WebFetch", SRC["ANDRES"] + " offset 100000", "Haughton-specific values", "E04", "Andres 2020", "chars 100,000-200,000", "Table 3.1 UTM grids, LiDAR 2016, climate; no thaw/ice values in this chunk")
sl("WebFetch", SRC["ANDRES"] + " offset 200000", "Haughton thaw depth, polygons, Mars comparison", "E04", "Andres 2020", "chars 200,000-257,352", "thaw depths 0.52-0.67 m, polygon geometry, no Arcadia mention")
sl("WebSearch(standard)", "Cebrenia quadrangle Mars 30-65N 120-180E Phlegra Montes Utopia Planitia", "Locate MS-02 quadrangle", "MS-02", "Wikipedia; USGS IMAP 1140", "titles/URLs only", "leads")
sl("WebSearch(standard)", "Marchant Head 2007 Antarctic Dry Valleys microclimate zonation Mars Beacon Valley buried ice", "E02 primary literature", "E02", "McKay 2009; Kowalewski 2006", "titles/URLs only", "Marchant & Head 2007 not returned; leads to two Antarctic Science papers")
sl("WebFetch", "https://en.wikipedia.org/wiki/Cebrenia_quadrangle", "Quadrangle extent and features", "MS-02", "Cebrenia quadrangle page", "page text", "MC-7 30-65N 120-180E; includes parts of Utopia and Arcadia Planitia; MS-02 inside extent")
sl("WebFetch", "https://pubs.usgs.gov/publication/i1140", "USGS geologic map record", "MS-02", "Elston 1979", "abstract", "circumpolar plains; formal units not named on page")
sl("WebFetch", "https://cambridge.org/core/journals/antarctic-science/article/snow-recurrence-sets-the-depth-of-dry-permafrost-at-high-elevations-in-the-mcmurdo-dry-valleys-of-antarctica/CF01B0520168E3A900CD4BD360049E2F", "Read McKay 2009 abstract", "E01;E02", "McKay 2009", "abstract", "snow recurrence ~2 yr fits 25 cm ice; >10 yr on Beacon floor")
sl("WebFetch", "https://cambridge.org/core/journals/antarctic-science/article/quantifying-low-rates-of-summertime-sublimation-for-buried-glacier-ice-in-beacon-valley-antarctica/5D51C5CAD844F98485B008634A1EF5E6", "Read Kowalewski 2006 abstract", "E02", "Kowalewski 2006", "abstract", "till 40-80 cm; net loss ~0.017 mm; no coordinates")
sl("python", "scripts/research/ms02_earth_analogs/verify_ms02.py (UTM 16N inverse of Andres Table 3.1)", "Convert Haughton LiDAR grids to lat/lon", "E04", "Andres Table 3.1", "this-study calculation", "grids 75.359-75.394N, 89.510-89.655W; ~3.9 x 4.0 km")
sl("WebSearch(standard)", "Tanaka 2014 geologic map of Mars SIM 3292 Vastitas Borealis Arcadia Planitia units", "Find geologic unit at MS-02", "MS-02", "USGS SIM 3292 page", "titles/URLs only", "lead")
sl("WebSearch(standard)", "Adventdalen active layer thickness ground temperature borehole CALM Svalbard permafrost", "E03 ground temperature/active layer", "E03", "UNISCALM AGU abstract; Christiansen 2019 SESS", "titles/URLs only", "leads")
sl("WebFetch", "https://doi.pangaea.de/10.1594/PANGAEA.921087", "Polygon dataset record", "E03", "Ulrich et al. 2020", "dataset page", "8 sites, bbox, parameters, CC BY 4.0")
sl("WebSearch(standard)", "Marchant Head 2007 Antarctic Dry Valleys microclimate zonation variable geomorphic processes implications assessing climate change on Mars Icarus", "Find Marchant & Head 2007", "E02", "none new", "titles/URLs only", "Paper not returned by this search")
sl("WebSearch(standard)", "Haughton impact structure Devon Island ground penetrating radar permafrost ice active layer", "E04 GPR/ground temperature", "E04", "CREWES reports; CSEG article", "titles/URLs only", "leads")
sl("WebFetch", "https://doi.pangaea.de/10.1594/PANGAEA.921087?format=textfile", "Polygon values", "E03", "PANGAEA", "page text", "Site table only; polygon values in zip files")
sl("WebFetch", "https://zenodo.org/records/4777825", "SESS 2018 permafrost snapshot record", "E03", "Christiansen et al. 2019", "record page", "Adventdalen among 5 sites; values not on page")
sl("WebFetch", "https://www.crewes.org/Documents/ResearchReports/2003/2003-08.pdf", "Haughton GPR report", "E04", "Nieto & Stewart 2003", "report text (extracted)", "permafrost top 0.60-0.9 m by GPR")
sl("WebFetch", "https://csegrecorder.com/articles/view/mars-in-canada-the-nasa-haughton-mars-project-devon-island-nunavut", "Haughton seismic/GPR overview", "E04", "Stewart article", "article text", "Vp 260/3100 m/s; permafrost top ~60 cm; '-17 C crater average' unspecified")
sl("WebFetch", "https://pubs.usgs.gov/sim/3292", "Tanaka 2014 map record", "MS-02", "SIM 3292", "page text", "No shapefile/geodatabase link on page; units at MS-02 not determined")
sl("WebFetch", "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0954102006000460", "Kowalewski 2006 full text", "E02", "Kowalewski 2006", "abstract only (full text unavailable)", "Coordinates/instrument depths not obtainable")
sl("WebFetch", "https://zenodo.org/records/4777825/files/SESS2018_PermaSval.pdf?download=1", "Adventdalen borehole values", "E03", "none", "binary PDF unreadable by fetch tool", "No values extracted")
sl("WebFetch", "https://ui.adsabs.harvard.edu/abs/2016AGUFMGC31H1202S", "UNISCALM abstract", "E03", "AGU 2016 abstract", "abstract", "ALT <1 m first 6 yr (min 74 cm 2005); >=1 m since 2006")
sl("curl", "zenodo SESS2018 PDF; PANGAEA polygons_AD3.zip", "Try to download data files directly", "E03", "none", "n/a", "403 from sandbox proxy; not retried")
sl("WebFetch", "https://openpolar.no/Record/ftunivwestonta:oai:ir.lib.uwo.ca:etd-10632", "Hibbard dissertation record", "E04", "Hibbard 2021", "abstract record", "Year 2021; no named Arctic sites")
sl("python", "scripts/research/ms02_earth_analogs/make_figures.py; dataviz validate_palette (blue/orange/aqua, light, all-pairs)", "Two context figures", "MS-02", "final_candidates.csv", "this-study", "Palette passes; aqua contrast WARN handled with visible value labels")


def write_csv(name, cols, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(cols); w.writerows(rows)

P.sort(key=lambda r: r[0])
write_csv("candidates.csv", cand_cols, cands)
write_csv("evidence.csv", ev_cols, E)
write_csv("prior_work.csv", pw_cols, P)
write_csv("search_log.csv", sl_cols, S_)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

files = ["docs/research/MS-02/report.md",
         "outputs/research/MS-02/candidates.csv", "outputs/research/MS-02/evidence.csv",
         "outputs/research/MS-02/prior_work.csv", "outputs/research/MS-02/search_log.csv",
         "outputs/research/MS-02/verification.json",
         "outputs/research/MS-02/figures/fig1_team_targets_context.png",
         "outputs/research/MS-02/figures/fig2_latitude_context.png",
         "scripts/research/ms02_earth_analogs/verify_ms02.py", "scripts/research/ms02_earth_analogs/build_tables.py",
         "scripts/research/ms02_earth_analogs/make_figures.py"]
manifest = {
    "task": "MS-02 Earth analog research, Team zasa, NASA Space Apps 2026",
    "mars_point": {"id": "MS-02", "lat_deg_N": 52.75, "lon_deg_E": 168.25,
                   "nominal_bounds": {"lat": [52.5, 53.0], "lon": [168.0, 168.5]}},
    "created_taipei": DATE,
    "branch": "research/ms-02-earth-analogs",
    "base_commit_sha": BASE_SHA,
    "base_commit_ref": "origin/handoff/verified-data-20261114 (adds the verified workbook and full screening data to main)",
    "origin_main_sha_at_start": MAIN_SHA,
    "base_choice_note": "No common SHA was specified. The hand-off branch is the only remote version containing both large files, so it was used as base; main's SHA is recorded as well.",
    "common_data_check": {
        "outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx": {"bytes": 23035176, "sha256": "157a108a08b8ca32ca52b40f3e9e80536431125cecfb838aa21223a933ac1175", "opened": "zip test OK; 33 sheets listed via openpyxl read-only"},
        "outputs/research/mars_reselection_20261114/screened_pool.csv.gz": {"bytes": 7702846, "sha256": "7c5559e40fca9fa304b7799e4490bfb4ff0d55ea0a02819c53f432377462ff92", "opened": "gzip -t OK; 58,238 rows x 54 columns; MS-02 cell found"},
        "ms02_value_cross_check": "outputs/research/MS-02/verification.json (14 consistency checks, all pass)"},
    "files": [{"path": p, "bytes": (ROOT / p).stat().st_size, "sha256": sha(ROOT / p)} for p in files if (ROOT / p).exists()],
    "sources": [{"id": k, "ref": v} for k, v in SRC.items()],
    "disposition_summary": {c[0]: c[9] for c in cands},
    "unresolved_gaps": [
        "docs/TEAM_START.md does not exist on main or the hand-off branch.",
        "scripts/restore_team_data.py does not exist on main or the hand-off branch (data are committed directly on the hand-off branch, so no restore step was needed).",
        "Raw PDS/SWIM/Montabone/Zenodo products could not be downloaded in the sandbox (HTTP 403 via proxy); MS-02 values were cross-checked among three hand-off files, not recomputed from raw rasters.",
        "MS-02 lies inside Cebrenia quadrangle MC-7 (30-65N, 120-180E; includes parts of Utopia and Arcadia Planitia and Phlegra Montes) but the formal geologic unit and whether MS-02 is in Arcadia Planitia were NOT determined (USGS IMAP 1140 plate not read).",
        "No Earth-site thermal inertia (only soil conductivity/diffusivity for E01), slope/relief or wind-speed values were obtained for any candidate (marked 未知).",
        "E02 rests on four abstracts (no coordinates, no temperature table; Kowalewski 2006 full text unavailable); E03 evidence is mostly abstracts plus Hauber 2011; E04 has thaw depth, polygon geometry and GPR/seismic permafrost-top depths but no ground-ice quantity and no borehole temperature series; only Hauber 2011, Marinova 2022, Andres 2020 and the CREWES report were read beyond abstracts (extracted text, some tables absent).",
        "Adventdalen borehole temperatures (SESS 2018 PDF) and polygon values (PANGAEA zip files) could not be read or downloaded from this environment.",
        "Hibbard (2021) dissertation body was not read; its abstract names no Arctic sites.",
        "USGS SIM 3292 (Tanaka 2014) page offers no shapefile or geodatabase link in the fetched content, so the unit at MS-02 could not be looked up here.",
        "Haughton: p.6 coordinate is the impact-structure centre and Fig 1.8 is the river-valley study area (~4.3 km apart); Table 3.1 LiDAR grids were converted from UTM 16N by a pure-Python inverse (this-study calc; no independent library cross-check, but results agree with Fig 1.8 within ~0.1 deg).",
        "One literature page (Antarctic Science depth-to-ice paper via proxy URL) was access-denied and not read.",
        "SWIM composite resolution/units are not stated on the provider page.",
        "Marchant & Head 2007 and Sugden 1995 were not found or read.",
        "Beacon Valley depth ranges differ between sources (10-60 cm Heldmann; 40-80 cm Kowalewski) and were not reconciled.",
        "No figure produced."],
    "not_claimed": ["No ice amount or probability for MS-02", "No Mars-likeness score/percentage", "No claim that any pairing was never studied"],
}
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print("rows:", len(cands), len(E), len(P), len(S_), "| files in manifest:", len(manifest["files"]))

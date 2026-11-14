# Earth ↔ Mars Data Cross-Reference (4 Core Topics)

This table cross-references every **Earth dataset collected** (NASA + partner space agencies) with **Teammate A's Mars modules** (`analog/`), including exact variable names, resolutions, scale alignment, and compatibility notes.

**Spatial Alignment Rule:**
- Mars `1° ≈ 59 km` · Earth `1° ≈ 111 km` → compare at equal physical ground distance (**Mars 1° ≈ Earth 0.5°**).
- Target grid convention (`analog/pds.py`): `(lat, lon)`, latitude North → South, longitude `-180` to `+180`.

---

## 1. Cross-Reference Matrix (Earth ↔ Mars)

| Topic | Mars Dataset (`analog/`) | Mars Variable & Grid | Earth Dataset (`data/raw/earth/`) | Agency | Earth Variable & Grid | How They Compare |
| --- | --- | --- | --- | --- | --- | --- |
| **1. Terrain** | **MGS MOLA** (`mars.py` + `terrain.py`) | Elevation (m) → `slope_deg`, `relief`<br>16 px/deg (~3.7 km), global | **`SRTMGL30`** (`terrain/`, 27 `.dem.zip`) | **NASA / NGA** | Elevation (m) → `slope_deg`, `relief`<br>30 arc-sec (~900 m), global | Aggregate Earth to ~3–4 km ground scale, then compute `slope_deg` and `block_stats` (`std`, `relief`) — never compare raw elevation |
| **1. Terrain** *(subtopic / partner)* | MOLA + HiRISE / MGC³ caves | Landforms, skylights | **Copernicus DEM / Sentinel-1 SAR** · **CSA RADARSAT** · **JAXA ALOS AW3D30** | **ESA / CSA / JAXA** | High-res DEM & radar roughness | Used qualitatively on Slide 4 for Top 1–2 site landforms, craters, and lava-tube/cave context |
| **2. Temperature** | **MGS TES** (`mars.py`) | Nighttime thermal inertia (`5–5000 J m⁻² K⁻¹ s⁻⁰·⁵`)<br>20 px/deg (~3.0 km), global | **`MOD11C3`** (`temperature/`, 24 `.hdf`, 2023–2024) | **NASA** | `LST_Day_CMG`, `LST_Night_CMG` (K)<br>0.05° (~5.6 km), global | Compute diurnal range `ΔT = LST_Day − LST_Night` and annual min/max; low thermal inertia ↔ high `ΔT` (loose sand/dust vs. exposed bedrock) |
| **3. Water / Ice** *(Aridity)* | **SWIM 2.0** (`swim.py`) | Subsurface ice consistency (`-1` to `+1`, `<1 m` & `1–5 m`)<br>20 px/deg, **±60° lat only** | **`GPM_3IMERGM`** (`water_ice/gpm/`, 24 `.HDF5`) | **NASA / JAXA** | `precipitation` (mm/hr)<br>0.1° (`1800×3600`), global | Lower Earth precipitation = hyper-arid Mars-like surface preservation |
| **3. Water / Ice** *(Moisture)* | SWIM 2.0 (`swim.py`) | Ice consistency | **`GLDAS_NOAH025_M`** (`water_ice/gldas/`, 24 `.nc4`) | **NASA** | `SoilMoi0_10cm_inst` (kg m⁻²)<br>0.25° (`600×1440`), -60° to +90° | Replaces 467 GB daily SMAP; lower soil moisture = closer to hyper-arid Mars |
| **3. Water / Ice** *(Lifelessness)* | *(Mars has no vegetation)* | Assumed 0 vegetation | **`MOD13C2`** (`water_ice/ndvi/`, 24 `.hdf`) | **NASA** | `CMG 0.05 Deg Monthly NDVI`<br>0.05° (~5.6 km), global | Near-zero/negative NDVI = barren, near-lifeless surface (plus biology subtopic) |
| **3. Water / Ice** *(Permafrost)* | **SWIM 2.0** (`swim.py`) | Buried water ice (`<1 m`, `1–5 m`) | **`ESA CCI Permafrost v4.0`** (`water_ice/permafrost/`, 2021 `.nc`) | **ESA** | `PFR` (permafrost fraction %)<br>Northern Hemisphere (~1 km / polar grid) | Direct physical partner-agency match for buried mid/high-latitude Mars ground ice (ISRU) |
| **4. Air** | **Montabone v2.5** (`dust.py`) | `mean_cdod` (`cdodtot`, MY34 storm & MY35 typical)<br>3° (~177 km), global | **`M2TMNXAER`** (`air/`, 24 `.nc4`, 2023–2024) | **NASA** | `DUEXTTAU` (dust-only AOT 550nm), `TOTEXTTAU`<br>0.5° × 0.625° (`361×576`), global | Direct dust-to-dust comparison (`DUEXTTAU` isolates mineral dust from smoke/urban aerosols) |

---

## 2. Format & Integration Notes for the Pipeline

1. **Ready in `xarray` out of the box:**
   - `GPM_3IMERGM` (`xr.open_dataset(path, group="Grid")`)
   - `GLDAS_NOAH025_M` (`xr.open_dataset(path)`)
   - `M2TMNXAER` (`xr.open_dataset(path)`)
   - `ESA CCI Permafrost` (`xr.open_dataset(path)`)
2. **Requires `pyhdf` (or HDF4 conversion):**
   - `MOD11C3` (`.hdf`) and `MOD13C2` (`.hdf`) use NASA HDF4-EOS; `rasterio`'s default pip wheel lacks HDF4 support.
3. **Binary tile format:**
   - `SRTMGL30` (27 `.dem.zip` files) contains raw 16-bit signed big-endian `.DEM` tiles (standard SRTM30 grid).
4. **Coverage & Limits:**
   - Mars `SWIM 2.0` only covers **±60° latitude**; global scoring outside ±60° cannot use SWIM directly.
   - All 5 non-replicable Mars conditions (`0.38 g`, `~0.6 kPa CO₂`, radiation, perchlorates, MY34 global dust storms) are documented separately in `docs/mars_limits.md`.

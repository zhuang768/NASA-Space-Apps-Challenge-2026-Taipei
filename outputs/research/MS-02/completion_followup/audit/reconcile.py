"""Reconcile stale MS-02 structured records against acquired primary-source audit.

Does not edit docs/research/MS-02/report.md. Original cell text, source files,
identity, and every modification are preserved in reconciliation_log.json.
No measured Mars ice truth or generic Earth-candidate upgrade is introduced.
"""
from pathlib import Path
import csv
import hashlib
import json

HERE = Path(__file__).resolve().parent
SITE = HERE.parents[1]
REPO = SITE.parents[2]
REPORT = REPO / 'docs/research/MS-02/report.md'
BASE = '521740108050ba16e406f8becb67a786179ff8bd'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

changes = []
def patch(file, key, record_id, field, value, authority, locator):
    changes.append(dict(file=file, key=key, record_id=record_id, field=field,
                        new=value, authority=authority, locator=locator))

AV = 'local_validation/analog_validation.csv'
ME = 'local_validation/mars_ice_evidence.csv'
CC = 'local_validation/claim_corrections.csv'

patch('candidates.csv','candidate_id','MS-02-E01','main_environment_differences',
      'Latitude 77.9S vs 52.75N; measured Earth MAAT -23.4 degC is not comparable with model-time-adjusted, coarse-bin MCS context (quantity/QA not independently reprocessed; not local ground temperature). Atmosphere, pressure, dust and insolation differ. W-station ice-cemented interface is 42 cm; approximately 15 cm is the 0 degC active layer, not total dry-cover thickness. Actual MS-02 ice depth remains unknown.', CC,'MCS-ORDER;UV-COVER')
patch('candidates.csv','candidate_id','MS-02-E01','disposition_reason',
      'Retained for the specifically documented W-station ice-cemented interface and multi-depth seasonal thermal response. This is an identifiability/method reference; independently separating ice from local cover/material/boundary effects has not been demonstrated. Do not reuse deprecated H2/H3 radar-chain claims.', AV,'AV-01')
patch('candidates.csv','candidate_id','MS-02-E01','next_verification_step',
      'Link raw W-station channels to serial/deployment metadata and preserve unresolved original clock/coordinate issues; obtain co-located density, heat capacity, conductivity and an independent ice profile plus matched ice-free/boundary controls before a unique ice or blind-accuracy claim. Table II/Fig.6 have been read; their publication summaries are not the raw series.', AV,'AV-01; shared_validation/gap_status.csv earth_controls and uv_identity_clock')

patch('candidates.csv','candidate_id','MS-02-E02','research_extent',
      'Original middle/central Beacon Valley records retain their separate, incompletely located scopes. A limited Liu2018 thermal/material subcase is located at 77deg49S,160deg39E; shallow sensors near a ~30 cm dry-cover/ice interface and an adjacent-polygon deep borehole are separate supports. No valley-wide surveyed boundary has been obtained.', AV,'AV-06')
patch('candidates.csv','candidate_id','MS-02-E02','boundary_basis',
      'Keep earlier Heldmann2013/Kowalewski2006/McKay2009/Bannister2007 records separate. Added primary Liu2018 sections2-3.3/Table1/Fig2 locates only its thermal subcase (77deg49S160deg39E); the adjacent deep borehole is not the same vertical column.', AV,'AV-06')
patch('candidates.csv','candidate_id','MS-02-E02','available_data',
      'Historical abstract-level depth/sublimation records remain separately sourced in evidence.csv. Liu2018 primary sections2-3.3/Table1/Fig2 now read: shallow temperatures, ~30 cm cover/interface, laboratory heat capacity, semiempirical conductivity, adjacent-polygon deep borehole. Original Liu raw time series has not been acquired; no independent rerun or generic valley-wide promotion.', AV,'AV-06')
patch('candidates.csv','candidate_id','MS-02-E02','main_environment_differences',
      'Polar latitude/climate/pressure mismatch with MS-02; massive-ice versus ice-cemented distinction is site-specific. Liu2018 is a located primary-literature thermal/material subcase, while older 10-60 cm and 40-80 cm ranges remain different sites/definitions and are not reconciled. Missing raw series prevents independent time-series reanalysis.', AV,'AV-06')
patch('candidates.csv','candidate_id','MS-02-E02','disposition',
      '待補證據（原整體候選）；Liu2018具名熱學/材料子案例可作限定文獻參照', AV,'AV-06')
patch('candidates.csv','candidate_id','MS-02-E02','disposition_reason',
      'The older whole-valley candidate is not upgraded. Latest primary-source review establishes a located ~30 cm interface/material thermal subcase (Liu2018); laboratory heat capacity and semiempirical conductivity are distinguished. Raw observations and co-located boundary/material controls remain missing.', AV,'AV-06')
patch('candidates.csv','candidate_id','MS-02-E02','next_verification_step',
      'Acquire the original Liu2018 raw thermal series and sensor/depth/spatial metadata before independent reanalysis; preserve its adjacent deep borehole as a separate support. Resolve older study-specific depth ranges with original footprints, not a valley-name join.', AV,'AV-06')

patch('candidates.csv','candidate_id','MS-02-E03','testable_physical_processes',
      'Retain CS-1 aeolian-silt accumulation and syngenetic-ice co-evolution as a specific measured core subprocess. ADE chemistry/structure and Hauber polygon geometry are separate references. WISDOM polygon-trough radar remains general-method context without located same-line independent ice truth; no combined cover-plus-radar validation chain.', AV,'AV-02;AV-03;AV-04;AV-09')
patch('candidates.csv','candidate_id','MS-02-E03','research_extent',
      'Group of separate Adventdalen evidence footprints, not a single validated site. Scalar coordinates78.1722N16.0613E retain the ADE historical anchor (FP-03); retained aeolian-cover/syngenetic-ice subprocess is CS-1 at78.201N15.840E (FP-01), about5.97km away. HRSC-AX8-site bounding box and unlocated WISDOM polygon-trough lines remain separate supports; no overlap or same-site truth assumed.', AV,'AV-02;AV-03;AV-04;AV-09')
patch('candidates.csv','candidate_id','MS-02-E03','next_verification_step',
      'CS-1 coring date is resolved: September2019; August2022 exposure is ~20 m NE. Wendt core coordinates/values have been acquired separately and cannot be joined to unlocated WISDOM lines. Obtain actual WISDOM line geometry and same-line independent ice observations before overlap/truth claims; keep CALM and older active-layer periods separate.', AV,'AV-02;AV-04;AV-05;AV-09')

patch('candidates.csv','candidate_id','MS-02-E04','research_extent',
      'Keep original Haughton River Valley nine-LiDAR-grid scope separate. A limited Thomson2012 plateau GPR/core subcase is at 75.368333N,-89.525833E with a 3 m line and a core at its 1.5 m CMP focus; approximately 0.9 m wet overburden was excavated. Do not merge this line with river/gully or 2003 base-camp evidence by place name.', AV,'AV-07')
patch('candidates.csv','candidate_id','MS-02-E04','boundary_basis',
      'Original scalar anchor75.37N,-89.53E and nine-grid extent remain Andres2020 Table3.1/Fig1.8 p20 (UTM16N grids; impact-structure centre is different). Separate Thomson2012 primary DOI10.1029/2012JE004053 sections2.3,3.1-3.3 locates plateau subcase75deg22min06secN89deg31min33secW (FP-12):3m line, core at1.5m CMPfocus, ~0.9m overburden excavated. This point anchor is not a full line polygon or an automatic match to Andres/2003 footprints.', AV,'AV-07')
patch('candidates.csv','candidate_id','MS-02-E04','available_data',
      'Original Andres2020 LiDAR/thaw-depth and Nieto2003 GPR/seismic records retain their own footprints. Added primary Thomson2012 sections2.3,3.1-3.3: 450 MHz GPR on a 3 m line and a ~1 m core, diameter0.10m, at CMP focus1.5m after ~0.9m overburden excavation. Raw radar/core profiles are not acquired; no whole-valley ice quantity or ground-temperature series.', AV,'AV-07')
patch('candidates.csv','candidate_id','MS-02-E04','disposition',
      '待補證據（原河谷候選）；Thomson2012挖除覆土後同線GPR/岩芯子案例可作限定方法參照', AV,'AV-07')
patch('candidates.csv','candidate_id','MS-02-E04','disposition_reason',
      'Original river-valley candidate is not upgraded. A distinct primary study supplies independent core evidence at one point on a 3 m GPR line, but the wet active layer had been excavated. It does not validate intact aeolian-cover detection, spatially exhaustive ground truth or orbital SHARAD, and Table1 aggregate material classes do not give this point a local ice fraction.', AV,'AV-07')
patch('candidates.csv','candidate_id','MS-02-E04','next_verification_step',
      'Acquire original Thomson2012 GPR/core profiles, field date, calibration and exact spatial linkage; retain core location and excavated-cover state. Independent undisturbed-cover controls are required for that broader use. Do not substitute Canadian High Arctic ice percentages or other sites.', AV,'AV-07')

patch('evidence.csv','evidence_id','EV-005','variable',
      'MCS-derived model-time-adjusted coarse-bin temperature context at 03/15 LTST; paired-bin contrast', ME,'ME-10')
patch('evidence.csv','evidence_id','EV-005','depth_or_height',
      'Quantity/QA not independently reprocessed; do not assign local surface, ground or subsurface sensitivity', ME,'ME-10')
patch('evidence.csv','evidence_id','EV-005','limitation_or_comparability',
      'Populated-bin medians: night171.2721K/day246.3053K. Median paired-bin contrast66.8305K is not the difference of those medians. Neighbouring5deg support, not candidate-local or annual ground temperature; QA/counts/uncertainty unprocessed; no Earth MAAT subtraction.', ME,'ME-10')
patch('evidence.csv','evidence_id','EV-006','limitation_or_comparability',
      'Consistency with ice, not abundance or probability; thermal/neutron/geomorphology/radar-source dependencies prohibit independent-vote counting. A mean and extrema do not establish a binary cell distribution or an ice-bearing-cell fraction. Preserve missing values; no SWIM-to-WEH conversion.', CC,'SWIM-BINARY; shared_validation/dependency_edges.csv')
patch('evidence.csv','evidence_id','EV-011','source',
      'https://pubs.usgs.gov/imap/1140/plate-1.pdf ; https://doi.org/10.3133/sim3292 ; https://planetarynames.wr.usgs.gov/Feature/348', ME,'ME-17;ME-18')
patch('evidence.csv','evidence_id','EV-011','limitation_or_comparability',
      'MC-7 extent confirmed from original USGS plate. Separate SIM3292 original-shapefile intersection places entire ROI in mAl (Middle Amazonian lowland unit); global1:20,000,000 unit is not local composition/ice truth. Arcadia MDIM2.1 polygon does not intersect ROI; approximate gap7.69km is geometric, not a precise geomorphic boundary.', ME,'ME-17;ME-18')
patch('evidence.csv','evidence_id','EV-014','limitation_or_comparability',
      'Earth air temperature; do not compare directly with model-time-adjusted neighbouring5deg MCS context, whose quantity/QA was not independently reprocessed and is not candidate-local ground temperature.', ME,'ME-10')
patch('evidence.csv','evidence_id','EV-017','limitation_or_comparability',
      'Approximately15cm is the local0degC active layer estimate; it is not total dry-cover thickness. W-station ice-cemented interface is42cm; no surface melt observed in three summers. Do not transfer either depth to MS-02.', CC,'UV-COVER')
patch('evidence.csv','evidence_id','EV-018','variable',
      'Annualized time near42cm ice interface above the recorded-temperature threshold; water activity calculated from ice/water saturation-vapour-pressure ratio', CC,'I06/EV-018')
patch('evidence.csv','evidence_id','EV-018','evidence_type',
      '溫度紀錄統計＋水活度熱力學計算（不是兩變量直接量測或能量模型時數）', CC,'I06/EV-018')
patch('evidence.csv','evidence_id','EV-018','observation_period',
      'Annualized in Marinova2022 Fig6/p162; underlying station record2009-2013; no single complete calendar year assigned by this audit', AV,'AV-01')
patch('evidence.csv','evidence_id','EV-018','locator','p.162 Fig.6; AV-01', AV,'AV-01')
patch('evidence.csv','evidence_id','EV-018','limitation_or_comparability',
      'Approximately2560h/year is a published annualized temperature-threshold duration; aw is calculated, not independently measured. Separate from the10-day energy-balance-model tuning period. No MS-02 habitability, biological activity or annual coverage inference.', CC,'I06/EV-018')
patch('evidence.csv','evidence_id','EV-029','value',
      'Original abstract-era search found no table. Superseding located Liu2018 primary thermal/material subcase has ~30cm dry cover and measured heat capacity/semiempirical conductivity; numerical property values and original raw series not transcribed/acquired in this root row.', AV,'AV-06')
patch('evidence.csv','evidence_id','EV-029','source',
      'https://doi.org/10.1029/2017JF004535 ; local_validation/analog_validation.csv AV-06', AV,'AV-06')
patch('evidence.csv','evidence_id','EV-029','locator','Liu2018 sections2-3.3;Table1;Fig2', AV,'AV-06')
patch('evidence.csv','evidence_id','EV-029','limitation_or_comparability',
      'A specific primary-literature subcase is now available; no whole-Beacon coordinate/depth unification. Adjacent deep borehole is a different support; raw-series availability and exact material/boundary controls remain unresolved.', AV,'AV-06')
patch('evidence.csv','evidence_id','EV-048','variable',
      'Scope-limited search result for Andres2020 and later Thomson2012 GPR/core evidence', AV,'AV-07')
patch('evidence.csv','evidence_id','EV-048','value',
      'Andres2020 text did not supply Haughton ground-ice quantity/GPR/temperature series. Later primary Thomson2012 identifies independent core at one3m GPR-line focus after ~0.9m overburden excavation; see AV-07. No whole-valley ice content or borehole-temperature series is established.', AV,'AV-07')
patch('evidence.csv','evidence_id','EV-048','limitation_or_comparability',
      'Absence from the original thesis text is not absence of Haughton GPR/core studies. Thomson2012 plateau line is separate from original river/gully scope. Canadian High Arctic10-20% and Axel Heiberg values cannot be substituted; aggregate Table1 is not a local ice fraction.', AV,'AV-07')
for eid in ['EV-053','EV-054']:
    patch('evidence.csv','evidence_id',eid,'observation_period',
          'September2019 cores; August2022 exposure ~20m NE is separate', AV,'AV-02')
patch('claims.csv','claim_id','C1','site_year_depth_of_direct_evidence',
      'CS-1 78.201N15.840E; cores September2019; 0-3.2m; August2022 exposure20mNE separately located', AV,'AV-02')
patch('claims.csv','claim_id','C7','direct_evidence',
      'CS-1 and ADE are ~5.97km apart; WISDOM polygon lines have no coordinates; dates differ (CS-1 Sep2019, ADE Mar2017, WISDOM Mar2022). ADE lies ~1.1km south of the cited polygon-site bounding box. Same valley is not a co-located chain.', AV,'AV-09')
patch('footprint.csv','footprint_id','FP-01','survey_or_sample_year',
      'September2019 cores; August2022 exposure20mNE separate (record spans~3000yr)', AV,'AV-02')

patch('prior_work.csv','prior_id','PW-02','read_scope',
      'Earlier partial-text extraction retained in reconciliation log; superseding local_validation review acquired/read the full primary Marinova2022 PDF, including TableII, rendered Fig6/p162 and Appendix.', AV,'AV-01')
patch('prior_work.csv','prior_id','PW-02','difference_in_method',
      'Published surface-energy-balance model tuned to10-day window; separately, approximately2560h/year is an annualized recorded-temperature threshold statistic with calculated aw, not modelled annual hours or two measured variables.', AV,'AV-01')
patch('prior_work.csv','prior_id','PW-05','note',
      'Author-interpreted ~1.5m polygon-trough reflector supported by radar/FDTD; no located same-line independent ice truth obtained. The stated3D truth belongs to a Longyearbreen glacier cave and cannot validate the separate polygon troughs.', AV,'AV-04')
patch('prior_work.csv','prior_id','PW-06','read_scope',
      'Earlier partial extraction superseded by local_validation full22-page primary-PDF acquisition/review; section3.2/p5 establishes September2019 cores and August2022 exposure20mNE separately.', AV,'AV-02')
patch('prior_work.csv','prior_id','PW-13','read_scope',
      'Original USGS I-1140 plate extent checked in later local_validation; this map supplies MC-7 context. Separate SIM3292 original shapefile, not I-1140 alone, supplies whole-ROI mAl unit.', ME,'ME-17;ME-18')
patch('prior_work.csv','prior_id','PW-13','note',
      'MC-7 confirmed. SIM3292 original-shapefile intersection establishes mAl at global-map scale; no local composition or independent ice truth. Approximate Arcadia MDIM2.1 named-feature geometry does not intersect ROI.', ME,'ME-17;ME-18')

for mid,kind in [
    ('ME-13','直接觀測（雷達power）；冰解釋未驗證'),
    ('ME-14','已取得目錄/足跡與browse；未校正EDR'),
    ('ME-15','已取得校準I/F與DDR；成分解釋未驗證'),
    ('ME-17','已取得全球地質圖；映射解釋非局部實測')]:
    patch(ME,'evidence_id',mid,'evidence_type',kind,
          'docs/research/MS-02/local_validation/research_notes.md','section2; acquired product statuses and labels')

new_prior_rows = [
 dict(prior_id='PW-21', candidate_id='MS-02-E02',
      work='Liu et al.2018 (DOI-defined primary Beacon Valley thermal/material study)',
      venue_doi_or_url='https://doi.org/10.1029/2017JF004535',
      site_covered='Specific Beacon thermal site77deg49S160deg39E; adjacent-polygon deep borehole separate',
      purpose='Thermal/material interpretation of dry cover and known massive-ice interface',
      classification_vs_MS02_use='直接先例（限定地球熱學/材料子流程）；非MS-02配對驗證',
      read_scope='Inherited verified primary review: sections2-3.3/Table1/Fig2; AV-06; original raw time series not acquired',
      difference_in_question='Known Earth ice-interface/material response versus conditional MS-02 ice interpretation',
      difference_in_scope='Specific~30cm dry-cover/interface site; no whole-valley or Mars footprint equivalence',
      difference_in_data='Shallow thermal sensors, laboratory heat capacity; conductivity semiempirical; adjacent deep borehole separate',
      difference_in_method='Primary material/thermal study; no independent reanalysis of raw time series in this delivery',
      note='Limited subcase only. Missing original series and co-located controls prohibit a full-candidate upgrade or unique ice attribution.'),
 dict(prior_id='PW-22', candidate_id='MS-02-E04',
      work='Thomson et al.2012 (DOI-defined primary Haughton GPR/core study)',
      venue_doi_or_url='https://doi.org/10.1029/2012JE004053',
      site_covered='Specific plateau site75.368333N,-89.525833E;3m GPR line and CMPfocus1.5m',
      purpose='Same-line radar/core dielectric-method comparison',
      classification_vs_MS02_use='直接先例（限定挖除覆土後GPR/岩芯子流程）；非未擾動覆土或軌道雷達驗證',
      read_scope='Inherited verified primary review: sections2.3,3.1-3.3,4,5.2; AV-07; raw profiles not acquired',
      difference_in_question='Earth co-located dielectric method versus MS-02 orbital ice/interface interpretation',
      difference_in_scope='Core truth at one focus, not spatially exhaustive line truth; separate from original river/gully candidate',
      difference_in_data='450MHz GPR;~1m length0.10m diameter core;~0.9m wet active layer excavated',
      difference_in_method='Known excavation and point-core linkage; no intact-cover or SHARAD performance transfer',
      note='Table1 aggregate site classes are not this point ice fraction; field-date/raw-profile/calibration and undisturbed controls remain required for broader validation.')
]

new_footprint_rows = [
 dict(footprint_id='FP-10', evidence_set='D University Valley thermal-interface subcase',
      location='W-station thermal profile (specific anchor; not valley centre or S/D stations)',
      lat_deg='-77.86215',lon_deg_east='160.7101',geometry_type='point anchor; no surveyed profile polygon',
      stated_extent='W thermal/ice-interface station area; approximately42cm ice-cemented interface and approximately15cm0degC active layer; no radar line',
      survey_or_sample_year='Station record2009-2013 as described in Marinova2022; channel-specific metadata and original clock issues preserved',
      depth_range_m='0.10/0.42/0.49m thermal channels;0.42m ice-interface reference;0.15m active layer is not total cover',
      measured_quantity='Multi-depth temperatures and documented ice-cemented interface; not local bulk-material truth or blind ice detection',
      source='https://doi.org/10.1017/S0954102022000025',
      locator='TableI station location;TableII;AV-01;77deg51.729minS160deg42.606minE converted to decimal degrees',
      geometry_status='Published W-station point anchor converted arithmetically; no inferred footprint; S/D identity ambiguity is not resolved'),
 dict(footprint_id='FP-11',evidence_set='E Beacon thermal/material subcase',
      location='Liu2018 shallow thermal site; adjacent deep borehole separate',
      lat_deg='-77.8166666667',lon_deg_east='160.65',geometry_type='point anchor; no surveyed local terrain polygon',
      stated_extent='Primary coordinate77deg49S160deg39E; shallow sensors and ~0.30m dry-cover/ice interface; adjacent-polygon deep borehole is a separate column',
      survey_or_sample_year='Primary publication2018; instrument-specific observation periods not transcribed in this footprint index; raw series not acquired',
      depth_range_m='~0.30m dry-cover/interface; shallow thermal depths documented separately; no merge with adjacent deep borehole',
      measured_quantity='Literature thermal/material subcase: recorded temperatures, laboratory heat capacity, semiempirical conductivity',
      source='https://doi.org/10.1029/2017JF004535',locator='Sections2-3.3;Table1;Fig2;AV-06;77deg49S160deg39E arithmetic conversion',
      geometry_status='Published coordinate anchor, minute precision; no whole-valley boundary or automatic location for older Beacon records'),
 dict(footprint_id='FP-12',evidence_set='F Haughton excavated-cover GPR/core subcase',
      location='Thomson2012 plateau GPR line and CMP-focus core; not Andres river/gully grids',
      lat_deg='75.3683333333',lon_deg_east='-89.5258333333',geometry_type='published site point anchor;3m line endpoints/azimuth not encoded',
      stated_extent='450MHz GPR3m line; core at along-line1.5m CMPfocus; core~1m long and0.10m diameter; ~0.9m wet active layer excavated before method comparison',
      survey_or_sample_year='Primary publication2012; field year not extracted in AV-07; no inference from publication year',
      depth_range_m='Core length~1m after~0.9m overburden excavation; original depth datum not imposed by this index',
      measured_quantity='Same-line GPR/dielectric comparison with independent core at one focus; not exhaustive line truth or intact-cover detection',
      source='https://doi.org/10.1029/2012JE004053',
      locator='Section2.3;sections3.1-3.3;AV-07;75deg22min06secN89deg31min33secW arithmetic conversion',
      geometry_status='Source-backed site anchor and stated line/core extents; do not merge with original Haughton River Valley, base-camp or landing-strip supports')
]

new_evidence_rows = [dict(
    evidence_id='EV-062',candidate_id='MS-02-E02',facet='地形',
    variable='Located Beacon thermal subcase versus unmeasured local terrain',
    value='77deg49S160deg39E (approximately-77.816667N,160.650000E); quantitative slope/relief/DEM and a surveyed polygon remain unknown',
    unit='degrees; slope/relief unknown',evidence_type='Primary-literature location; terrain geometry unknown',
    observation_period='Site as described by Liu2018; exact terrain survey period not supplied here',
    depth_or_height='surface location',
    resolution_or_representative_extent='Specific shallow thermal-site anchor; adjacent deep borehole separate; no valley-wide polygon',
    source='https://doi.org/10.1029/2017JF004535',locator='Sections2-3.3;Fig2;local_validation/analog_validation.csv AV-06',
    limitation_or_comparability='Coordinate is the Liu2018 subcase, not an automatic location for Heldmann/Kowalewski/Bannister data. No quantitative Mars-versus-Earth terrain difference is computed; unknown is not zero.'
)]
# Surface new acquired products in the original evidence index, retaining the
# complete authoritative local table and dependencies instead of inventing data.
with (SITE / ME).open(encoding='utf-8-sig',newline='') as f:
    local_mars={r['evidence_id']:r for r in csv.DictReader(f)}
for eid,mid,facet,kind in [
    ('EV-063','ME-12','熱性質','Conditional thermal-model product'),
    ('EV-064','ME-13','水/冰','Observed radar power; ice interpretation unvalidated'),
    ('EV-065','ME-14','地形','Acquired nominal footprints and browse imagery'),
    ('EV-066','ME-15','水/冰','Acquired calibrated I/F; no accepted compositional interpretation'),
    ('EV-067','ME-17','地形','Global mapped geologic interpretation')]:
    m=local_mars[mid]
    new_evidence_rows.append(dict(evidence_id=eid,candidate_id='MS-02',facet=facet,
        variable=m['variable'],value=m['value'],unit=m['unit'],evidence_type=kind,
        observation_period=m['period'],depth_or_height=m['depth_or_sensitivity'],
        resolution_or_representative_extent=m['resolution_or_extent'],
        source=m['source_url_or_doi'],locator=m['locator']+'; local_validation/mars_ice_evidence.csv '+mid,
        limitation_or_comparability=m['limitation_or_unknown']+' Source dependence: '+m['source_dependency']))

def main():
    log_path = HERE / 'reconciliation_log.json'
    old_log = json.loads(log_path.read_text()) if log_path.exists() else None
    report_before = sha(REPORT)
    by_file = {}
    for c in changes: by_file.setdefault(c['file'], []).append(c)
    log = {'base_commit': BASE, 'scope': 'structured record correction only; formal report untouched',
           'formal_report_sha256': report_before, 'files': {}, 'changes': [], 'inserted_rows': []}
    for name, edits in by_file.items():
        path = SITE / name
        with path.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f); rows = list(reader); fields = reader.fieldnames
        log['files'][name] = {'sha256_before':sha(path), 'row_count':len(rows), 'fields':fields}
        touched = False
        for c in edits:
            matched = [r for r in rows if r[c['key']] == c['record_id']]
            assert len(matched) == 1, c
            row = matched[0]
            assert c['field'] in row, c
            if row[c['field']] == c['new']: continue
            log['changes'].append({**c, 'old':row[c['field']]})
            row[c['field']] = c['new']; touched = True
        if name in ['prior_work.csv','evidence.csv','footprint.csv']:
            insertions = {'prior_work.csv':new_prior_rows,'evidence.csv':new_evidence_rows,
                          'footprint.csv':new_footprint_rows}[name]
            identity = {'prior_work.csv':'prior_id','evidence.csv':'evidence_id',
                        'footprint.csv':'footprint_id'}[name]
            for new in insertions:
                existing = [r for r in rows if r[identity] == new[identity]]
                if existing:
                    assert len(existing) == 1 and existing[0] == new, new[identity]
                    continue
                assert set(new) == set(fields)
                rows.append(new); touched = True
                log['inserted_rows'].append({'file':name,'row':new,'authority':AV,
                                            'locator':'AV-01;AV-06;AV-07' if name=='footprint.csv' else 'AV-06;AV-07'})
        if touched:
            with path.open('w',encoding='utf-8-sig',newline='') as f:
                writer=csv.DictWriter(f, fieldnames=fields);writer.writeheader();writer.writerows(rows)
        log['files'][name]['sha256_after'] = sha(path)
        log['files'][name]['row_count_after'] = len(rows)
    assert sha(REPORT) == report_before, 'Formal report changed unexpectedly'
    if old_log is not None:
        assert old_log['formal_report_sha256'] == report_before
        old_log['changes'].extend(log['changes'])
        old_log.setdefault('inserted_rows', []).extend(log['inserted_rows'])
        for name, state in log['files'].items():
            if name in old_log['files']:
                old_log['files'][name]['sha256_after'] = state['sha256_after']
                old_log['files'][name]['row_count_after'] = state['row_count_after']
            else: old_log['files'][name] = state
        result = old_log
    else: result = log
    if log['changes'] or log['inserted_rows'] or old_log is None:
        log_path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'changed_cells_this_run':len(log['changes']), 'new_rows_this_run':len(log['inserted_rows']), 'total_changed_cells':len(result['changes']), 'formal_report_unchanged':True}))

if __name__ == '__main__': main()

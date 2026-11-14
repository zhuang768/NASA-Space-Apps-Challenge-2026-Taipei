"""Independent stdlib checks of exported native thermal support and summaries."""
import csv
import json
import math
from pathlib import Path
from statistics import median

HERE=Path(__file__).resolve().parent
CHECKS=[]
def check(name, condition):
    CHECKS.append({'check':name,'pass':bool(condition)})
    assert condition, name

rows=list(csv.DictReader((HERE/'native_cells_9x9.csv').open()))
summaries=list(csv.DictReader((HERE/'spatial_support_summary.csv').open()))
audit=json.loads((HERE/'support_audit.json').read_text())
check('81 unique native cells', len(rows)==81 and len({(r['row_zero_based'],r['column_zero_based']) for r in rows})==81)
check('81 valid numeric pairs',all(r['both_valid']=='True' and float(r['conditional_depth_m'])!=-32768 for r in rows))
centre=[r for r in rows if r['chebyshev_cell_radius']=='0']
check('exact fixed centre one row',len(centre)==1 and float(centre[0]['latitude_deg_N'])==52.75 and float(centre[0]['longitude_deg_E'])==168.25)
check('centre depth matches independently inherited source table',float(centre[0]['conditional_depth_m'])==0.4499824941)
check('centre TI matches inherited source table',float(centre[0]['dry_layer_TI_J_m_minus2_K_minus1_s_minushalf'])==188.2415009)
for s in summaries:
    side=int(s['window_side_cells'])
    selected=[r for r in rows if int(r['chebyshev_cell_radius'])<=(side-1)//2]
    values=[float(r[s['quantity']]) for r in selected]
    w=[float(r['spherical_cell_area_m2']) for r in selected]
    m=math.fsum(v*ww for v,ww in zip(values,w))/math.fsum(w)
    check(f'{side}x{side} {s["quantity"]} count',len(values)==int(s['valid_N'])==side**2)
    check(f'{side}x{side} {s["quantity"]} extrema median',min(values)==float(s['minimum']) and max(values)==float(s['maximum']) and median(values)==float(s['median']))
    check(f'{side}x{side} {s["quantity"]} weighted mean',math.isclose(m,float(s['area_weighted_mean']),rel_tol=1e-14))
    check(f'{side}x{side} {s["quantity"]} no error claim','NOT error/CI' in s['interpretation'])
# Numerically integrate the latitude strip rather than reuse the sine-difference formula.
n=1000
a,b=map(math.radians,(52.5,53.0)); step=(b-a)/n
integral=step/3*(math.cos(a)+math.cos(b)+math.fsum((4 if i%2 else 2)*math.cos(a+i*step) for i in range(1,n)))
independent_area=3396190.0**2*math.radians(.5)*integral/1e6
check('spherical area independently quadrature verified',math.isclose(independent_area,audit['exact_spherical_cell_area_km2'],rel_tol=1e-11))
for r in rows:
    depth=float(r['conditional_depth_m'])
    expected=1 if depth<=.3 else 0 if depth>=.5 else 1-(depth-.3)/.2
    check(f'2026 publication rule cell {r["row_zero_based"]},{r["column_zero_based"]}',math.isclose(expected,float(r['PQ19_component_by_published_2026_rule']),abs_tol=1e-14))
check('MS02 component scalar independently checked',math.isclose(audit['PQ19_component_by_published_2026_rule'],0.2500875295,abs_tol=1e-12))
check('unknown diagnostics stay null',all(audit[k] is None for k in ('local_observation_count','local_RMS_K','local_depth_CI_m','combined_thermal_consistency')))
check('5 original decoded source checksums checked',audit['source_md5_pass_N']==audit['source_md5_total_N']==5)
result={'checks':CHECKS,'all_pass':all(c['pass'] for c in CHECKS),'scope':'numerical reproducibility and support QA only; no ice truth, residual CI, version transformation or SWIM raster validation'}
(HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'pass_N':sum(x['pass'] for x in CHECKS),'total_N':len(CHECKS),'scope':result['scope']}))

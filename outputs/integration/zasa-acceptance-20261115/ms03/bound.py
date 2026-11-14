import csv,json,math,hashlib,pathlib
p=pathlib.Path(__file__).parent
source=pathlib.Path('/workspace/shared/zasa-finish/integration/ms03-evidence-only/outputs/research/MS-03/completion_20261115/earth_four_dimensions.csv')
rows=list(csv.DictReader(source.open()))
row=next(r for r in rows if '18.484785' in str(r))
d=18.48478542881041
mocmap=3.000339463
# Ground spacing for conformal north polar stereographic on sphere: p_map / k
# k = 2/(1+sin(latitude)). This is sampling, not effective optical resolution.
out=[]
for name,spacing in [('CTX_nominal_not_window_calibration',6.),('MOC_ground_at_57.5N',mocmap*(1+math.sin(math.radians(57.5)))/2),('MOC_ground_at_58N',mocmap*(1+math.sin(math.radians(58)))/2)]:
 out.append(dict(sampling_case=name,ground_sampling_m=spacing,AD1_median_diameter_m=d,samples_across_diameter=d/spacing,illustrative_two_edge_diameter_error_m=2*spacing,illustrative_relative_diameter_error=2*spacing/d))
with (p/'sampling_bound.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=out[0]);w.writeheader();w.writerows(out)
(p/'receipt.json').write_text(json.dumps(dict(input_csv=str(source),input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),AD1_row=row,warning='AD1 median inherited from retained repository calculation; not independently recomputed from vectors in this bounded task',illustrative_sampling_needed_m_for_20pct_diameter_error=d*.2/2,illustrative_sampling_needed_m_for_10pct_diameter_error=d*.1/2,results=out),indent=2))
print(json.dumps(out,indent=2))

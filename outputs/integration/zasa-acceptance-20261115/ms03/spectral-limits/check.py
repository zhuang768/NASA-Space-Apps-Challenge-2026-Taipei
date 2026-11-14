import json,csv,io,pathlib
p=pathlib.Path(__file__).parent
x=json.loads((p/'inputs.json').read_text())
a=list(csv.DictReader(io.StringIO(x['anchors'].lstrip('\ufeff'))))
r=[]
for z in a:
 if z['requested_nm']=='1525':
  r.append({'product_id':z['product_id'],'anchor_requested_nm':1525,'actual_median_nm':float(z['nearest_nm_median']),'median_offset_nm':float(z['nearest_nm_median'])-1525,'maximum_absolute_offset_nm':max(abs(float(z[k])-1525) for k in ['nearest_nm_min','nearest_nm_max'])})
out={'diagnostic':'sampling adequacy QC, NOT ice detection or a material classifier','anchor_mismatch':r,'coincident_nir_visible_IRR1_not_available_in_selected_L_only_inputs':True,'quantitative_frost_cloud_material_discrimination_executed':False,'detection_limit':None,'reason':'No calibrated noise/residual model, validated alternative discrimination, full seasonal sampling or matched footprints. Do not turn numeric valid counts into sensitivity.'}
(p/'sampling_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

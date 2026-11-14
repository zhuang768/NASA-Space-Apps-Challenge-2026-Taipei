from pathlib import Path
import json,csv,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).resolve().parent;P=O.parent/'official_resources';z=np.load(P/'mrdr_selected_arrays.npz');d=np.load(O/'diagnostic_arrays.npz');m=d['source_inside'];q=json.loads((O/'results.json').read_text());sources=list(csv.DictReader((O/'source_group_residuals.csv').open(encoding='utf-8-sig')))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
f,axs=plt.subplots(2,2,figsize=(14,10),dpi=180);f.subplots_adjust(left=.09,right=.97,top=.86,bottom=.22,wspace=.35,hspace=.65)
a=axs[0,0];a.scatter(z['official_BD1500_2'][m],z['recalculated_BD1500_2'][m],s=2,alpha=.25,color='#007f8b');lo=min(z['official_BD1500_2'][m].min(),z['recalculated_BD1500_2'][m].min());hi=max(z['official_BD1500_2'][m].max(),z['recalculated_BD1500_2'][m].max());a.plot([lo,hi],[lo,hi],color='#c17c43',ls='--',label='Equality reference, not ground truth');a.set(title='A. Existing calculation follows disclosed CAT formula',xlabel='Official MRDR BD1500_2 (dimensionless)',ylabel='Reference-formula calculation (dimensionless)');a.legend(fontsize=8)
a=axs[0,1];x=np.arange(len(sources));med=np.array([float(s['BD1500_recalculated_minus_official_median']) for s in sources]);low=np.array([float(s['BD1500_difference_p05']) for s in sources]);high=np.array([float(s['BD1500_difference_p95']) for s in sources]);a.vlines(x,low,high,color='#93b4bf',lw=3);a.scatter(x,med,color='#007f8b');a.axhline(0,color='#b4b4b4',lw=1);a.set(title='B. Source-group differences; not a causal attribution',ylabel='Calculated minus official (dimensionless)',xticks=x,xticklabels=[s['source_product'].split('_')[0][-8:]+'\nn='+s['strict_pixels'] for s in sources]);a.tick_params(axis='x',labelsize=8)
a=axs[1,0]
for key,label,color in [('cat64_minus_official','Production-product difference','#007f8b'),('float32_minus_float64','Float32 perturbation only','#c17c43')]:
 v=np.abs(d[key][m]);v=v[v>0];a.hist(np.log10(v),bins=45,histtype='step',lw=1.6,label=label,color=color)
a.set(title='C. Float precision cannot explain the full difference',xlabel='log10(abs(difference)); exact zeros omitted',ylabel='Map-centre count');a.legend(fontsize=8)
a=axs[1,1];a.hist(d['ICER_identity_minus_official'][m],bins=60,color='#62778d');a.axvline(0,color='#c17c43',ls='--');a.set(title='D. Official summary bands do not preserve CAT identity',xlabel='[1-(1-BD1435)/(1-BD1500_2)] - ICER1_2',ylabel='Map-centre count');a.ticklabel_format(axis='x',style='sci',scilimits=(0,0))
f.suptitle('MS-03 BD1500_2 version / arithmetic audit\nProduction cause remains unknown; no scientific values corrected',fontsize=16,y=.97)
f.text(.09,.14,'Inputs: CRISM MRDR v4 T1811, software1.03.94, product2023-07-18; five source observations2006–2014.\n13,169 map centres also have source DDR centres in the fixed cell; no claim of independent detector samples.\nCAT7.4 disclosed multispectral equation ported to Python; original IDL and MRDR production runtime were not executed.\nSource-group ranges are spatial5th–95th percentiles, not confidence intervals. Float tests are arithmetic diagnostics.\nOfficial values, original formula outputs and ice unknowns are retained; no fitted gain/offset or ice-detection threshold.',ha='left',va='top',fontsize=10)
f.savefig(O/'F-BD01_version_and_arithmetic_audit.png',facecolor='white');plt.close(f)

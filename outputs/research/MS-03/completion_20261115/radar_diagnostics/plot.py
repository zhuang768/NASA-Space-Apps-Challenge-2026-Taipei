from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).resolve().parent
rows=list(csv.DictReader((O/'radar_pick_diagnostic.csv').open(encoding='utf-8-sig')))
x=[int(r['column_1based']) for r in rows]
fig,ax=plt.subplots(2,1,figsize=(10,6.5),sharex=True,gridspec_kw={'height_ratios':[2,1]},layout='constrained')
for field,label,color in [('observed_crop_max_row_0based','Observed crop argmax (not a reflector pick)','#b64d40'),('model_nadir_row_0based','Model nadir (not independent truth)','#176a7b'),('simulated_crop_max_row_0based','Simulated crop argmax','#777777')]:
 ax[0].plot(x,[int(r[field]) for r in rows],label=label,color=color,lw=1.6)
ax[0].set_ylabel('Original range-row index (0 based)');ax[0].invert_yaxis();ax[0].legend(loc='upper left',fontsize=8)
ax[0].set_title('MS-03: S_04624502_RGRAM peak-index diagnostic',loc='left',weight='bold')
j=[int(r['max_row_change_from_previous_column_samples']) for r in rows[1:]]
ax[1].plot(x[1:],j,'.-',color='#b64d40',lw=.9);ax[1].axhline(0,color='#777777',lw=.6)
ax[1].set_ylabel('Adjacent argmax jump\n(samples)');ax[1].set_xlabel('Original radargram column (1 based)')
for a in ax:a.grid(alpha=.2);a.spines[['top','right']].set_visible(False)
fig.suptitle('65 in-cell centres; 2016-06-07 UTC. Delay indices are not local ice depth.',fontsize=10)
fig.savefig(O/'F-RAD01_peak_index_diagnostic.png',dpi=180)

"""Documentation schematic, not a reconstructed production execution."""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

O=Path(__file__).resolve().parent
fig,ax=plt.subplots(figsize=(12,6.6));fig.patch.set_facecolor('white')
ax.set(xlim=(0,12),ylim=(0,6.6));ax.axis('off')
ax.text(.25,6.2,'Why formula-only AL evaluation need not equal delivered SU',fontsize=18,weight='bold',color='#142638')
ax.text(.25,5.78,'Documented MRDR v4 stages | Historical SIS 1.3.7.6, Appendix P3',fontsize=11,color='#465a69')

def box(x,y,w,h,title,body,color='#e7f1f3'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.08',facecolor=color,edgecolor='#738894',linewidth=1))
    ax.text(x+.16,y+h-.30,title,fontsize=11,weight='bold',va='top',color='#142638')
    ax.text(x+.16,y+h-.72,body,fontsize=10.5,va='top',linespacing=1.5,color='#253e4e')
box(.3,3.35,3.25,1.8,'1. Reflectance adjustment','Interstrip optimization\nAL product basis\nP3 section 6')
box(4.2,3.35,3.25,1.8,'2. Parameter evaluation','Surface summary formulas\nMapping channel selection\nP3 section 7')
box(8.1,3.35,3.25,1.8,'3. Summary adjustment','Second optimization\nIncludes BD1500_2\nP3 section 8',color='#fff0dc')
for x1,x2 in [(3.6,4.1),(7.5,8.0)]:ax.annotate('',xy=(x2,4.22),xytext=(x1,4.22),arrowprops=dict(arrowstyle='->',color='#465a69',lw=1.5))
ax.text(.35,2.83,'2022 snapshot predates T1811 production (2023-07-18); section 8 text matches the current SIS.',fontsize=10.5,color='#253e4e')
box(.3,1.10,11.05,1.2,'Not recovered: exact build 1.03.94 execution','Source/build, run options, coefficients and paired pre/post arrays remain unknown.\nNo numerical correction applied.',color='#f1f3f5')
ax.text(.3,.66,'Schematic of published documentation, not an observed run trace. Projection/assembly follows (P3 sections 10-11).',fontsize=9,color='#465a69')
ax.text(.3,.32,'Sources: production_history/source_audit.csv (PH-S01 to PH-S04). MS-03 ice presence, depth and content remain unknown.',fontsize=9,color='#465a69')
fig.savefig(O/'F-PH01_documented_processing.png',dpi=180,bbox_inches='tight',facecolor='white')
plt.close(fig)

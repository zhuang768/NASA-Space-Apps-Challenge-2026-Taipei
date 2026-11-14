"""Plot nominal footprint support and existing model cells;no ice-confirmation map."""
from pathlib import Path
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle
import numpy as np
HERE=Path(__file__).resolve().parent
def main():
    g=json.loads((HERE/'ctx_nominal_intersections.geojson').read_text());rows=list(csv.DictReader((HERE/'piqueux_model_patch.csv').open()))
    fig,axes=plt.subplots(1,2,figsize=(12,5.8));fig.subplots_adjust(left=.07,right=.94,bottom=.24,top=.82,wspace=.32)
    colors=['#4878b6','#e88436','#50a47d','#aa6ba6']
    for feature,color in zip(g['features'],colors):
        geom=feature['geometry'];coords=[geom['coordinates']] if geom['type']=='Polygon' else geom['coordinates']
        label=feature['properties']['product_id'].split('_')[0]+' '+feature['properties']['observation_start_utc'][:10]
        for n,poly in enumerate(coords):axes[0].add_patch(Polygon(poly[0],facecolor=color,edgecolor=color,alpha=.28,label=label if n==0 else None))
    axes[0].add_patch(Rectangle((72.5,56.5),.5,.5,fill=False,lw=1.8,color='#222'));axes[0].plot(72.75,56.75,'k+',ms=11,mew=1.8)
    axes[0].set(xlim=(72.47,73.03),ylim=(56.47,57.03),xlabel='East longitude (degrees)',ylabel='Planetocentric north latitude (degrees)',title='CTX: 4 nominal footprints intersect ROI')
    axes[0].legend(loc='upper left',ncol=1,fontsize=8,frameon=True,facecolor='white',framealpha=.9);axes[0].grid(alpha=.2)
    grid=np.array([float(r['depth_model_m']) for r in rows]).reshape(3,3)
    im=axes[1].imshow(grid,extent=(72,73.5,56,57.5),origin='upper',cmap='Blues',vmin=.30,vmax=.80,aspect='auto')
    for r in rows:axes[1].text(float(r['longitude_e']),float(r['latitude_n']),f"{float(r['depth_model_m']):.3f}",ha='center',va='center',fontsize=10,color='#111')
    axes[1].add_patch(Rectangle((72.5,56.5),.5,.5,fill=False,lw=2,color='#d45828'))
    axes[1].set(xlabel='East longitude (degrees)',ylabel='Planetocentric north latitude (degrees)',title='Published thermal model: ROI cell = 0.427 m')
    fig.colorbar(im,ax=axes[1],fraction=.045,pad=.03,label='Conditional model depth (m)')
    fig.suptitle('MS-01: observation support and an inherited model estimate',fontsize=15,y=.96)
    fig.text(.07,.075,'Left: catalogue polygons clipped to the fixed ROI; geometric coverage is not valid-pixel QA or ice detection.\nRight: Piqueux et al. 2019 / CaltechDATA D1.1316 v1.0, 2 ppd. Lower-layer ice is a model assumption.\nNeither panel confirms local ice, measures its fraction, or validates a Mars depth using University Valley.',fontsize=9,linespacing=1.5)
    fig.savefig(HERE/'local_support_and_model.png',dpi=160);fig.savefig(HERE/'local_support_and_model.svg');plt.close(fig)
    print('Saved local_support_and_model.png/.svg')
if __name__=='__main__':main()

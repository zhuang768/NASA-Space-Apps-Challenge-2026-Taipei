"""One coverage/interpretation figure and observability table;no traced Mars polygons."""
from pathlib import Path
import csv,gzip,json,io,math,zipfile
import numpy as np
from PIL import Image
import shapefile
from shapely.geometry import shape,box
from shapely import wkt
from shapely.ops import unary_union
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R=Path(__file__).resolve().parents[3];O=R/'outputs/research/MS-03/morphology'
Image.MAX_IMAGE_PIXELS=300000000 # exact expected archive dimensions5056x52224
# Native source rows36000..37023, samples600..1623;preserve bytes and stretch separately.
a=np.frombuffer(gzip.decompress((O/'D01_native_rows.bin.gz').read_bytes()),dtype='u1').reshape(1024,5056)[:,600:1624].copy()
Image.fromarray(a).save(O/'D01_native_crop_DN.png')
lo,hi=map(float,np.percentile(a,[1,99]));display=np.uint8(np.clip((a.astype(float)-lo)*255/(hi-lo),0,255));Image.fromarray(display).save(O/'D01_native_crop_stretch.png')
# Four-corner bilinear locator ONLY;index corners correspond first/last lines and samples.
# PDS index original graphic latitudes replaced by ODE planetocentric corner coordinates.
def locate(x,y):
 u=x/5055;v=y/52223
 corners=np.array([[243,54.109],[243.87,54.18],[241.71,59.254],[242.73,59.324]])
 return ((1-v)*((1-u)*corners[0]+u*corners[1])+v*((1-u)*corners[2]+u*corners[3])).tolist()
loc=[locate(x,y) for x,y in [(600,36000),(1623,36000),(1623,37023),(600,37023)]]
assert all(242<x<242.5 and 57.5<y<58 for x,y in loc)
(O/'native_crop_provenance.json').write_text(json.dumps(dict(product_id='D01_027566_2370_XN_57N117W',row_start_0based=36000,row_end_0based_inclusive=37023,sample_start_0based=600,sample_end_0based_inclusive=1623,raw_type='uncalibrated8bit SQROOT EDR DN',linear_stretch_percentiles=[1,99],stretch_DN_bounds=[lo,hi],interpolation='none;nearest display',approximate_corner_locator_lonlat=loc,locator_limit='Bilinear from catalogue/index corner ordering;not SPICE camera-model geolocation or orthorectification;no precise Mars measurements or ROI-wide absence claim',visual_read='In inspected patch,tonal mottling,small crater-like features and striping;no reliably traceable closed fracture network. Non-detection does not establish absence;AD1 median diameter about3CTXpixels.'),indent=2)+'\n')
# Earth geometry from source polygons,never polylines.
z=zipfile.ZipFile(R/'outputs/research/MS-03/polygons_Act-IWS_source.zip');b='polygons_Act-IWS';reader=shapefile.Reader(shp=io.BytesIO(z.read(b+'.shp')),shx=io.BytesIO(z.read(b+'.shx')),dbf=io.BytesIO(z.read(b+'.dbf')));geoms=[shape(s.__geo_interface__) for s in reader.shapes()]
summary=json.loads((O/'AD1_geometry_summary.json').read_text());metrics=summary['metrics'];d=metrics['equivalent_circle_diameter_m']
rows=[dict(metric='Mapped polygon count',unit='count',AD1='185 valid source polygons',MS03='unknown;no Mars polygons digitized',comparison='No size/shape distribution test'),dict(metric='Equivalent-circle diameter',unit='m',AD1=f"{d['median']:.3f} median;{d['min']:.3f}–{d['max']:.3f} range",MS03='unknown',comparison='AD1 diameter/CTX6.09m: '+f"{d['median']/6.09:.2f} median;{d['min']/6.09:.2f}–{d['max']/6.09:.2f} pixels;sampling illustration only"),dict(metric='Planar area',unit='m2',AD1=f"{metrics['area_m2']['median']:.3f} median",MS03='unknown',comparison='No reliable Mars boundary measurements'),dict(metric='Circularity4piA/P2',unit='dimensionless',AD1=f"{metrics['circularity_4piA_over_P2']['median']:.4f} median",MS03='unknown',comparison='Resolution-sensitive;not comparable from current Mars images'),dict(metric='Minimum rotated rectangle aspect L/W',unit='dimensionless',AD1=f"{metrics['mrr_aspect_length_width']['median']:.4f} median",MS03='unknown',comparison='Definition differs from paper largest/smallest polygon diameters'),dict(metric='Available sampling',unit='m/pixel',AD1='Existing HRSC-AX2009-derived vectors;source raster GSD not verified this round',MS03='CTX6.08–6.11 nominal;older browse60.9 approx;V17 full-size JPEG block artifacts;HiRISE RDR no catalogue match',comparison='Vector coordinate decimals do not imply raster accuracy'),dict(metric='Cause/ground ice',unit='status',AD1='Known ice-wedge reference per source',MS03='unknown',comparison='Morphology alone cannot establish contraction mechanism,ice wedges or ice depth')]
with (O/'observability_comparison.csv').open('w',newline='') as h:w=csv.DictWriter(h,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,3,figsize=(16,6));colors=['#397b9b','#d59335','#44846b']
for c,p in zip(colors,json.loads((O/'ode_CTX_EDR.json').read_text())['ODEResults']['Products']['Product']):
 g=wkt.loads(p['Footprint_geometry']);x,y=g.exterior.xy;axs[0].fill(x,y,color=c,alpha=.16);axs[0].plot(x,y,color=c,lw=1,label=p['pdsid'].split('_')[0]+' CTX footprint')
axs[0].add_patch(Rectangle((242,57.5),.5,.5,fill=False,lw=2,ec='black',label='MS-03 nominal cell'))
axs[0].add_patch(Rectangle((241.51818024375,57.243063928588),241.83751839088-241.51818024375,57.775298752268-57.243063928588,fill=False,lw=1.3,ls='--',ec='#a34040',label='PSP_006864_2380 bbox: outside'))
axs[0].plot([x[0] for x in loc]+[loc[0][0]],[x[1] for x in loc]+[loc[0][1]],color='black',ls=':',label='Native patch locator (approx.)')
axs[0].set(xlim=(241.45,242.6),ylim=(57.2,58.1),xlabel='Mars east longitude (deg)',ylabel='Planetocentric latitude (deg)',title='A  Catalogue coverage (not valid-pixel coverage)');axs[0].legend(fontsize=8,loc='lower left');axs[0].grid(alpha=.2)
axs[0].set_aspect(1/math.cos(math.radians(57.75)))
axs[1].imshow(display,cmap='gray',interpolation='nearest');axs[1].axis('off');axs[1].set_title('B  CTX native DN patch; no traced polygon')
axs[1].text(.02,.02,'D01_027566_2370 | 2012-06-13\nRows36000–37023; samples600–1623 (0-based)\n1–99% linear stretch; uncalibrated,not orthorectified\n6.09m/pixel nominal; orientation not north-up',transform=axs[1].transAxes,fontsize=8,va='bottom',bbox=dict(facecolor='white',alpha=.85,edgecolor='none'))
minx,miny,maxx,maxy=unary_union(geoms).bounds
for g in geoms:
 x,y=g.exterior.xy;axs[2].plot(np.array(x)-minx,np.array(y)-miny,color='#397b9b',lw=.7)
axs[2].set_aspect('equal');axs[2].set(xlabel='UTM33N easting from source min (m)',ylabel='Northing from source min (m)',title='C  AD1 existing mapped network (185)');axs[2].text(.02,.02,f"Median equivalent diameter: {d['median']:.2f}m\nSource: Ulrich,Härtel,Hauber2020 / PANGAEA921087\nCC BY4.0; existing Mars-comparison precedent",transform=axs[2].transAxes,fontsize=8,bbox=dict(facecolor='white',alpha=.9,edgecolor='none'))
fig.suptitle('MS-03 × Adventdalen AD1: morphology evidence is insufficient',fontsize=15,y=.98)
fig.text(.02,.025,'ODE query snapshot: 3 CTX; 0 HiRISE RDRV11/RDR. CTX union corner footprints cover nominal cell; inspected pixels do not establish AD1-scale networks.\nAD1 downgraded to general method reference. No absence,shared genesis,subsurface ice or resource inference. NASA/JPL/MSSS imagery; see source manifest.',fontsize=9)
fig.subplots_adjust(left=.055,right=.985,bottom=.19,top=.86,wspace=.35)
fig.savefig(O/'MS03_AD1_coverage_interpretation.png',dpi=180);fig.savefig(O/'MS03_AD1_coverage_interpretation.pdf');plt.close(fig)

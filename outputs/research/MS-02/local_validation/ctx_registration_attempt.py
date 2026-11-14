import csv,warnings,itertools,re,numpy as np
warnings.simplefilter('ignore')
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
from scipy.ndimage import map_coordinates
H='.'
fp={}
for r in csv.DictReader(open('product_footprints.csv',encoding='utf-8-sig')):
    if r['catalog']=='CTX_EDR':
        pts=[tuple(map(float,p.split())) for p in re.findall(r'(-?\d+\.?\d*\s-?\d+\.?\d*)',r['footprint_wkt'])][:4]
        fp[r['product_id'][:3].lower()]=pts
def load(k,scale):
    im=Image.open(f'sources/products/{[f for f in __import__("os").listdir("sources/products") if f.startswith(k) and f.endswith("jpeg")][0]}')
    im.draft('L',(im.size[0]//scale,im.size[1]//scale)); return np.asarray(im.convert('L'),dtype=np.float32)
def corners(pts,topN,leftW):
    pts=sorted(pts,key=lambda p:-p[1]); N=sorted(pts[:2]);S=sorted(pts[2:])  # sorted by lon: [W,E]
    Wn,En=N;Ws,Es=S
    top=(Wn,En) if leftW else (En,Wn); bot=(Ws,Es) if leftW else (Es,Ws)
    if not topN: top,bot=bot,top
    return top,bot  # (left,right) lon/lat pairs
def sample(img,pts,topN,leftW,lon,lat):
    (tl,tr),(bl,br)=corners(pts,topN,leftW);h,w=img.shape
    # Build a coarse forward bilinear corner grid; no Newton inverse or camera model.
    gy,gx=np.mgrid[0:h:8,0:w:8]; u=gx/(w-1); v=gy/(h-1)
    LON=(1-v)*((1-u)*tl[0]+u*tr[0])+v*((1-u)*bl[0]+u*br[0]); LAT=(1-v)*((1-u)*tl[1]+u*tr[1])+v*((1-u)*bl[1]+u*br[1])
    # Select the nearest coarse node in lon/lat degrees; no affine refinement.
    out=np.full(lon.shape,np.nan,np.float32)
    from scipy.spatial import cKDTree
    t=cKDTree(np.c_[LON.ravel(),LAT.ravel()]);d,i=t.query(np.c_[lon.ravel(),lat.ravel()])
    ys=(gy.ravel()[i]).astype(float);xs=(gx.ravel()[i]).astype(float)
    ok=d<0.02
    vals=map_coordinates(img,[ys,xs],order=1,mode='nearest')
    out.ravel()[ok]=vals[ok];return out
if __name__=='__main__':
    lon,lat=np.meshgrid(np.linspace(168.0,168.5,100),np.linspace(53.0,52.5,170))
    S=8
    imgs={k:load(k,S) for k in ('v16','j02','g23')}
    res=[]
    for (a,ha),(b,hb) in itertools.product(itertools.product(['v16'],itertools.product([True,False],[True,False])),itertools.product(['j02','g23'],itertools.product([True,False],[True,False]))):
        pass
    import sys
    for b in ('j02','g23'):
        best=[]
        for ha in itertools.product([True,False],[True,False]):
            A=sample(imgs['v16'],fp['v16'],*ha,lon,lat)
            for hb in itertools.product([True,False],[True,False]):
                B=sample(imgs[b],fp[b],*hb,lon,lat);m=~np.isnan(A)&~np.isnan(B)
                if m.sum()<500: continue
                a=A[m]-A[m].mean();c=B[m]-B[m].mean();ncc=(a*c).sum()/np.sqrt((a*a).sum()*(c*c).sum())
                best.append((round(float(ncc),3),ha,hb,int(m.sum())))
        best.sort(reverse=True);print(b,best[:4])

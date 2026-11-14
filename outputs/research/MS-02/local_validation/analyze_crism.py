"""QA one affordable IR survey cube with matching DDR. No mineral/ice band detection."""
from pathlib import Path
import numpy as np,json
P=Path(__file__).resolve().parent;S=P/'sources/products'
a=np.fromfile(S/'msp0001565d_01_if213l_trr3.img',dtype='<f4',count=900*55*64).reshape(900,55,64).transpose(1,0,2)
g=np.fromfile(S/'msp0001565d_01_de213l_ddr1.img',dtype='<f4',count=14*900*64).reshape(14,900,64)
lat,lon=g[3],g[4];roi=(lat>=52.5)&(lat<=53)&(lon>=168)&(lon<=168.5)
x=a[:,roi];valid=np.isfinite(x)&(np.abs(x)<1e20)
# 65535 is a potential missing sentinel; report separately rather than assume all finite values are science.
sentinel=(x==65535);valid &= ~sentinel
out=dict(product='msp0001565d_01_if213l_trr3',geometry='msp0001565d_01_de213l_ddr1',period='2010-01-08',shape_bands_lines_samples=list(a.shape),
 roi_pixel_centres=int(roi.sum()),roi_spectral_samples=int(x.size),numeric_usable_fraction=float(valid.mean()),sentinel_65535_count=int(sentinel.sum()),
 latitude_range=[float(lat[roi].min()),float(lat[roi].max())],longitude_range=[float(lon[roi].min()),float(lon[roi].max())],
 if_quantiles=np.quantile(x[valid],[0,.01,.5,.99,1]).tolist(),
 evidence='calibrated I/F science + matching DDR; numeric/geometric QA only; not corrected for atmosphere/photometry',
 unknown='wavelength calibration and per-band bad pixel masks not acquired; no ice or hydrated-mineral identification; buried ice not constrained')
np.savez_compressed(P/'crism_roi.npz',if_spectra=x,latitude=lat[roi],longitude=lon[roi],numeric_valid=valid)
(P/'crism_quality.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

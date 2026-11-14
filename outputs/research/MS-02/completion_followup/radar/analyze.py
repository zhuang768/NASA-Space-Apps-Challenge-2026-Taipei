"""MS-02 SHARAD diagnostic screening; no subsurface/ice classification.

Run from any directory. Inputs are the three archived ROI power arrays, geometry
and surface-clutter browse images in ../../local_validation/radar_roi.
Fixed thresholds are exploratory image-screening choices, not validated detector
parameters or false-alarm probabilities. Never subtract simulated browse power.
"""
from pathlib import Path
import csv, hashlib, json, math, os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/ms02-radar-matplotlib')
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

P=Path(__file__).resolve().parent
I=P.parents[1]/'local_validation'/'radar_roi'
ORBITS=['00464501','01983502','02004601']
DT_US=0.0375

def write_csv(name, rows):
    if not rows: return
    with (P/name).open('w', newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def distances(lat1,lon1,lat2,lon2):
    a,b,c,d=map(np.deg2rad,[lat1,lon1,lat2,lon2])
    h=np.sin((c-a)/2)**2+np.cos(a)*np.cos(c)*np.sin((d-b)/2)**2
    return 2*3396190*np.arcsin(np.sqrt(np.clip(h,0,1)))

def crossing_count(lat1,lon1,lat2,lon2):
    # An affine Mars-local equirectangular projection preserves intersections.
    # This checks piecewise-linear tracks between delivered sample locations;
    # it is not a claim about unsampled curvature or overlapping radar footprints.
    def project(lat,lon):
        return np.column_stack((np.deg2rad(lon-168.25)*3396190*np.cos(np.deg2rad(52.75)),
                                np.deg2rad(lat-52.75)*3396190))
    a=project(lat1,lon1);b=project(lat2,lon2)
    def orient(p,q,r):
        u=q-p;v=r-p;return u[0]*v[1]-u[1]*v[0]
    count=0
    for p,q in zip(a[:-1],a[1:]):
        for r,s in zip(b[:-1],b[1:]):
            o1,o2,o3,o4=orient(p,q,r),orient(p,q,s),orient(r,s,p),orient(r,s,q)
            if o1*o2<0 and o3*o4<0:count+=1
            # No collinear/touching cases occur for the present coordinates;
            # fail rather than silently classify such a case in future inputs.
            elif min(abs(o1),abs(o2),abs(o3),abs(o4))<1e-9:
                raise ValueError('Degenerate track intersection: requires explicit geometry review')
    return count

def main():
    summary=[];rows=[];horizons=[];inputs=[];geo={};sensitivity=[]
    fig,axs=plt.subplots(3,3,figsize=(13,10),layout='constrained')
    for k,orbit in enumerate(ORBITS):
        prefix='s_'+orbit
        f=I/(prefix+'.npz');g=I/(prefix+'_geom.csv');s=I/(prefix+'_clutter_roi.png')
        for v in [f,g,s]:
            inputs.append(dict(path=str(v.relative_to(P.parents[4])),bytes=v.stat().st_size,sha256=hashlib.sha256(v.read_bytes()).hexdigest()))
        z=np.load(f);power=z['power'].astype(float);nrow,ncol=power.shape
        assert nrow==3600 and np.isfinite(power).all() and (power>0).all()
        geom=list(csv.DictReader(g.open()));assert len(geom)==ncol
        sim=np.asarray(Image.open(s).convert('L'),dtype=float);assert sim.shape==power.shape
        # Argmax is an echo anchor, not an independently known surface pick.
        # Compare with strongest simulated surface/clutter echo to test that use.
        observed_peak=np.argmax(power,axis=0)
        simulated_peak=np.argmax(sim,axis=0)
        peak_shift=observed_peak-simulated_peak
        noise=power[200:1000,:]
        noise_mean=noise.mean(axis=0)
        noise_q999=np.quantile(noise,0.999,axis=0)
        rel=np.arange(-100,501)
        aligned=np.full((len(rel),ncol),np.nan)
        clutter_aligned=np.full_like(aligned,np.nan)
        for j in range(ncol):
            rr=observed_peak[j]+rel
            ok=(rr>=0)&(rr<nrow)
            aligned[ok,j]=power[rr[ok],j]/noise_mean[j]
            # Shift sim by its own strongest echo; timing morphology only.
            sr=simulated_peak[j]+rel
            sok=(sr>=0)&(sr<nrow)
            clutter_aligned[sok,j]=sim[sr[sok],j]
        # Surface-near envelope (0.15-0.90 us) is actual measured echo tail.
        # It contains sidelobes AND possible geology; use conservative envelope,
        # never claim that this has isolated instrument sidelobes.
        tail=aligned[(rel>=4)&(rel<=24),:]
        empirical_tail_q99=np.quantile(tail,0.99,axis=0)
        # Exploratory post-echo screen 1.125-11.25 us, not the 0.45 m interface.
        delayrows=(rel>=30)&(rel<=300)
        for offset in [30,60,120,240]:
            rr=(rel>=offset)&(rel<offset+30)
            # Independent-window average is not assumed: report summaries only.
            horizons.append(dict(orbit=orbit,delay_start_us=offset*DT_US,delay_stop_us=(offset+30)*DT_US,
                median_echo_to_noise_db=float(np.median(10*np.log10(aligned[rr,:]))),
                p95_echo_to_noise_db=float(np.percentile(10*np.log10(aligned[rr,:]),95)),
                median_clutter_dn=float(np.median(clutter_aligned[rr,:])),
                p95_clutter_dn=float(np.percentile(clutter_aligned[rr,:],95))))
        above=(aligned[delayrows,:]>noise_q999[None,:]/noise_mean[None,:])
        conservative=above & (aligned[delayrows,:]>empirical_tail_q99[None,:])
        # Shape screen: require 3 adjacent columns and 3 adjacent delay samples.
        # These are correlated samples, not independent validation.
        raw=conservative
        supported=np.zeros_like(raw)
        for r in range(1,raw.shape[0]-1):
            for c in range(1,ncol-1):
                supported[r,c]=raw[r-1:r+2,c-1:c+2].all()
        for noise_start,noise_stop in [(200,1000),(800,1600)]:
            control=power[noise_start:noise_stop,:]
            for quantile in [.99,.995,.999]:
                th=np.quantile(control,quantile,axis=0)/noise_mean
                hit=aligned[delayrows,:]>th[None,:]
                tailhit=hit & (aligned[delayrows,:]>empirical_tail_q99[None,:])
                for dn in [32,64,128]:
                    # Bright simulation pixels are a browse-location proxy only.
                    # Different DN cuts do not encode physical detection limits.
                    clutter=clutter_aligned[delayrows,:]>=dn
                    sensitivity.append(dict(orbit=orbit,noise_row_start0=noise_start,noise_row_stop_exclusive0=noise_stop,
                        empirical_noise_quantile=quantile,simulated_browse_dn_threshold=dn,
                        above_noise_samples=int(hit.sum()),above_noise_and_tail_samples=int(tailhit.sum()),
                        above_noise_near_bright_simulated_pixels=int((hit&clutter).sum()),
                        above_noise_not_bright_simulated_pixels=int((hit&~clutter).sum()),
                        interpretation='Exploratory sample counts; nonmatch is not a subsurface detection'))
        for j in range(ncol):
            rows.append(dict(orbit=orbit,source_column_1based=int(z['source_columns_1based'][j]),
                utc=geom[j]['utc'],latitude=float(z['latitude'][j]),longitude=float(z['longitude'][j]),
                observed_strongest_row0=int(observed_peak[j]),simulated_strongest_row0=int(simulated_peak[j]),
                relative_strongest_shift_samples=int(peak_shift[j]),
                relative_strongest_shift_us=float(peak_shift[j]*DT_US),
                empirical_pre_echo_mean=float(noise_mean[j]),pre_echo_q999=float(noise_q999[j]),
                strongest_echo_to_noise_db=float(10*np.log10(power[observed_peak[j],j]/noise_mean[j])),
                exploratory_above_noise_sample_count=int(above[:,j].sum()),
                exploratory_above_noise_and_surface_tail_sample_count=int(conservative[:,j].sum()),
                exploratory_3x3_support_count=int(supported[:,j].sum()),
                classification='unclassified echo; not accepted subsurface or ice'))
        summary.append(dict(orbit=orbit,columns=ncol,
            strongest_row_min0=int(observed_peak.min()),strongest_row_max0=int(observed_peak.max()),
            simulated_strongest_row_min0=int(simulated_peak.min()),simulated_strongest_row_max0=int(simulated_peak.max()),
            median_observed_minus_simulated_samples=float(np.median(peak_shift)),
            min_observed_minus_simulated_samples=int(peak_shift.min()),max_observed_minus_simulated_samples=int(peak_shift.max()),
            median_echo_to_noise_db=float(np.median(10*np.log10(power[observed_peak,np.arange(ncol)]/noise_mean))),
            median_pre_echo_q999_to_mean_db=float(np.median(10*np.log10(noise_q999/noise_mean))),
            above_noise_samples=int(above.sum()),above_noise_and_tail_samples=int(conservative.sum()),
            exploratory_3x3_support_count=int(supported.sum()),
            accepted_subsurface_reflector_count=0,accepted_ice_reflector_count=0,
            interpretation='Diagnostic screen only; no validated detector and no ice/non-ice truth'))
        geo[orbit]=(z['latitude'],z['longitude'])
        db=10*np.log10(aligned)
        axs[k,0].imshow(db,origin='upper',aspect='auto',extent=[0,ncol,rel[-1]*DT_US,rel[0]*DT_US],vmin=0,vmax=35,cmap='gray')
        axs[k,0].set_title(orbit+' observed / empirical noise (dB)')
        axs[k,1].imshow(clutter_aligned,origin='upper',aspect='auto',extent=[0,ncol,rel[-1]*DT_US,rel[0]*DT_US],cmap='gray')
        axs[k,1].set_title('Surface simulation (browse DN)')
        axs[k,2].plot(np.median(db,axis=1),rel*DT_US,label='observed median')
        axs[k,2].fill_betweenx(rel*DT_US,np.percentile(db,5,axis=1),np.percentile(db,95,axis=1),alpha=.25,label='5-95% columns')
        axs[k,2].axhline(0,color='k',lw=.5);axs[k,2].set_ylim(11.25,-1.5);axs[k,2].set_title('Relative-delay profile')
        axs[k,2].set_xlabel('dB relative to pre-echo mean');axs[k,2].legend(fontsize=7)
        for ax in axs[k]:ax.set_ylabel('Delay from strongest echo (us)')
        for ax in axs[k,:2]:ax.set_xlabel('ROI column index; not independent samples')
    pairs=[]
    for ai,a in enumerate(ORBITS):
        for b in ORBITS[ai+1:]:
            la,lo=geo[a];lb,lob=geo[b]
            d=distances(la[:,None],lo[:,None],lb[None,:],lob[None,:])
            ia,ib=np.unravel_index(np.argmin(d),d.shape)
            jj=np.argmin(abs(la[:,None]-lb[None,:]),axis=1)
            matched=distances(la,lo,lb[jj],lob[jj])
            intersections=crossing_count(la,lo,lb,lob)
            pairs.append(dict(orbit_a=a,orbit_b=b,min_track_sample_separation_m=float(d[ia,ib]),
                matched_latitude_median_separation_m=float(np.median(matched)),
                closest_a_roi_index=int(ia),closest_b_roi_index=int(ib),
                piecewise_linear_track_intersection_count=intersections,
                crossing_method='Strict segment intersections in Mars-local equirectangular projection',
                interpretation='No track crossing in delivered linear interpolation; footprint overlap and independent truth untested' if not intersections else 'Interpolated crossing requires local reflector association and independent truth'))
    fig.savefig(P/'relative_delay_screen.png',dpi=140)
    write_csv('trace_diagnostics.csv',rows);write_csv('delay_windows.csv',horizons);write_csv('track_separation.csv',pairs)
    write_csv('threshold_sensitivity.csv',sensitivity)
    meta=dict(base_commit='521740108050ba16e406f8becb67a786179ff8bd',roi=dict(lat_min=52.5,lat_max=53,lon_min=168,lon_max=168.5),
        row_indexing='0-based array indices; areoid reference circa row1800 is not surface',
        analysis_class='exploratory diagnostic; no accepted geologic reflector',
        pre_echo_noise_rows0=[200,999],relative_post_echo_screen_samples=[30,300],
        empirical_tail_samples=[4,24],
        sample_spacing_us=DT_US,nominal_bandwidth_hz=1e7,
        nominal_free_space_range_resolution_m=299792458/(2e7),
        assumed_ice_permittivity=3.15,nominal_ice_range_resolution_m=299792458/(2e7*math.sqrt(3.15)),
        model045m_delay_us=2*.4499824941*math.sqrt(3.15)/299792458*1e6,
        model045m_delay_samples=2*.4499824941*math.sqrt(3.15)/299792458*1e6/DT_US,
        thresholds_not_validated=True,
        amplitude_subtraction_performed=False,
        inputs=inputs,orbits=summary,track_pairs=pairs,
        unresolved=['No independently validated surface or subsurface picks','No phase: cannot re-compress or deconvolve actual impulse response','Simulation is surface-only and approximate; no clutter-free inference from nonmatch','No colocated dielectric/ice truth','No proven same-position independent cross-track horizon'])
    (P/'diagnostics.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps(meta,indent=2))

if __name__=='__main__':main()

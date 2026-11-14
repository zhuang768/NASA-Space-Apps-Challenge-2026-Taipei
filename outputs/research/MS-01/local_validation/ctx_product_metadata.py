#!/usr/bin/env python3
"""Build ctx_product_metadata.csv for MS-01 from values read manually in the ODE
web UI (Product Search > Meta Data tab). Browse thumbnails are not data products;
no morphology classification is made. Bounding-box overlap is an upper bound
(strips are slanted)."""
import csv, json, pathlib
here = pathlib.Path(__file__).parent
BOX = dict(lat0=56.5, lat1=57.0, lon0=72.5, lon1=73.0)
rows = [
 # id, obs_time_utc, clat, clon, latmax, latmin, west, east, scale, emis, inc, phase, ls, comment, volume
 ("G23_027348_2388_XN_58N287W","2012-05-27T11:46:00",58.567,72.928,61.165,55.957,71.63,74.05,6.09,2.68,48.44,50.98,116.3,"Ride-along with CRISM","MROX_1657"),
 ("F02_036407_2378_XN_57N287W","2014-05-03T09:15:09",57.541,72.29,60.34,54.732,71.08,73.33,6.07,0.24,51.2,51.02,125.16,"Utopia Planitia","MROX_2096"),
 ("F23_044728_2356_XN_55N286W","2016-02-10T17:16:24.531",55.317,73.279,57.554,53.076,72.54,73.94,6.02,1.56,44.8,43.37,107.26,"Northern plains","MROX_2491"),
 ("V17_086795_2355_XN_55N286W","2025-01-31T10:19:36.067",55.2402,73.4932,57.846,52.6342,72.4,74.45,6.08,0.1,50.75,50.79,37.83,"Utopia Planitia","MROX_5267"),
]
hdr = ["product_id","dataset","volume","obs_time_utc","center_lat","center_lon_e","max_lat","min_lat","west_lon","east_lon",
       "map_scale_m_per_px","emission_deg","incidence_deg","phase_deg","solar_longitude_deg","ode_comment",
       "bbox_overlaps_ms01_box","source","limitations"]
out = []
for r in rows:
    ov = (r[4] >= BOX["lat0"] and r[5] <= BOX["lat1"]) and (r[6] <= BOX["lon1"] and r[7] >= BOX["lon0"])
    out.append([r[0],"MRO-M-CTX-2-EDR-L0-V1.0",r[14],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],
                "yes" if ov else "no",
                "ODE Product Search web UI, Meta Data tab, read 2026-11-15",
                "EDR unprojected; bbox overlap is upper bound for slanted strip; browse thumbnail not a data product; no morphology classified"])
with open(here/"ctx_product_metadata.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(out)
print(len(out), [o[16] for o in out])

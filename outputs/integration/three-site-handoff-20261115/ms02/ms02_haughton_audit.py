#!/usr/bin/env python3
"""Recalculate the MS-02 Haughton scale/colocation checks from published values.
No third-party packages or live downloads needed. Illustrative physics only.
"""
from math import sin, cos, radians, asin, sqrt

C_M_PER_S = 299_792_458
R_EARTH_KM = 6371.0088

def dms(deg, minute, second, direction):
    return (-1 if direction in 'WS' else 1) * (deg+minute/60+second/3600)

def haversine(a, b):
    phi1, phi2 = radians(a[0]), radians(b[0])
    dl = radians(b[1]-a[1])
    z = sin((phi2-phi1)/2)**2 + cos(phi1)*cos(phi2)*sin(dl/2)**2
    return 2*R_EARTH_KM*asin(sqrt(z))

wedge = (dms(75,22,6,'N'), dms(89,31,33,'W'))
drill = (dms(75,25,15.1,'N'), dms(89,45,36.9,'W'))
# Repository E04 candidate anchor; deliberately not treated as the LiDAR polygon centroid.
candidate = (75.37, -89.53)
print('metric,id,value,unit')
for name, pos in [('wedge',wedge),('drill',drill)]:
    for axis, val in zip(('lat','lon'),pos):
        print(f'coordinate,{name}_{axis},{val:.8f},deg')
for name, a, b in [('drill_vs_wedge',drill,wedge),('drill_vs_E04_anchor',drill,candidate),('wedge_vs_E04_anchor',wedge,candidate)]:
    print(f'anchor_distance,{name},{haversine(a,b):.5f},km')
# 3.65–3.90 are the pooled two ice-wedge CMP values in Thomson et al. Sec. 4.1;
# hypothetical illustration of SHARAD resolution, not a measured Mars permittivity.
for eps in (3.65,3.90):
    v = C_M_PER_S / sqrt(eps)
    res = v / (2 * 10e6)
    print(f'SHARAD_nominal_separability,epsilon_{eps},{res:.5f},m')
    for d in (0.4499824941,0.65,0.90):
        print(f'two_way_delay,epsilon_{eps}_depth_{d},{2*d/v*1e9:.5f},ns')
# Conductivity and volumetric heat capacity of Haughton wet patterned ground
# and Phoenix TECP are study-summary averages, not colocated Earth/Future Mars.
for name,k,cap in [('Haughton',.6711,1.6200e6),('Phoenix',.085,1.05e6)]:
    print(f'diffusivity_from_summary_means,{name},{k/cap*1e6:.5f},mm2/s')
    print(f'inertia_from_summary_means,{name},{sqrt(k*cap):.5f},J m-2 K-1 s-0.5')

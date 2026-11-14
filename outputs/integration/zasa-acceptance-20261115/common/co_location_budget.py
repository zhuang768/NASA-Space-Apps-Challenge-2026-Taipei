"""Conditional lateral depth-gradient budgets, not measured Mars slopes."""
import csv, math, json
from pathlib import Path
p=Path(__file__).parent
c=299792458.; B=10e6; eps=3.15
resolution=c/(2*B*math.sqrt(eps))
# Source: main MS-02 completion_followup/radar_notes.md, minimum sample distances.
pairs=[('00464501','01983502',9571.6),('00464501','02004601',562.5),('01983502','02004601',9013.7)]
with (p/'conditional_gradient_budgets.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['track_a','track_b','reported_min_sample_distance_m','allowed_depth_difference_m','max_depth_gradient_m_per_m','equivalent_angle_deg','scope'])
 for a,b,d in pairs:
  for tolerance in [0.45,resolution]:
   gradient=tolerance/d
   w.writerow([a,b,d,tolerance,gradient,math.degrees(math.atan(gradient)),'illustrative uniform-gradient budget at minimum sample separation; not measured slope or footprint test'])
assert resolution>8 and resolution<9
print(json.dumps({'ice_assumed_resolution_m':resolution,'rows':6,'nearest_pair_045m_gradient':0.45/562.5,'nearest_pair_045m_equivalent_angle_deg':math.degrees(math.atan(.45/562.5))},indent=2))

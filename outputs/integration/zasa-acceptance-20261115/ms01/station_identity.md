# MS-01 S/D station identity: bounded follow-up evidence

Status: OPEN. No external messages, credentials, GitHub changes, or new station assignments. Existing workbook/depth-survey analyses were not repeated. This is an evidence note, not a report.

## New useful check

- Downloaded the official [Marinova 2022 publisher PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/432141245F43EF744DD8ABDB56580A5F/S0954102022000025a.pdf/climate-and-energy-balance-of-the-ground-in-university-valley-antarctica.pdf). Visually inspected printed p.145, Fig.1b, including local rendered `Marinova2022_page145.png`.
- The figure explicitly indicates north-up and draws D north of S. This agrees qualitatively with deployment D=A (-77.8597333,160.7169833), S=B (-77.8657667,160.7286667); its Methods prose on p.146 reverses them. The published source therefore contains its own figure/prose inconsistency, rather than being uniform evidence against the deployment notes.
- Do NOT claim a metric georeference: figure has no coordinate grid, no serial labels, no clear surveyed station-point symbols, and no positioning-error estimate. In particular M is drawn north of W although both coordinate versions put M slightly south of W. Label placements/approximation prevent recovering exact logger locations from this figure.

## Primary inventory checked

[Zenodo fixed v1](https://zenodo.org/records/10553882) files re-fetched and verified against all four advertised MD5s. Full SHA256/bytes/source URLs in `source_manifest.json`.

- `UnivValley_Dec2009Deployment_HoboInfo.docx`: the existing serial-linked inventory, not a new independent GPS observation. S8/1122968 (U12) and 2429439 (U23) tied to B; D36/2432936 (U12) and 2429437 (U23) tied to A. Names also describe S as closest to snowpack. Repeated coordinate blocks do not supply an independent measurement.
- `UnivValley_HoboInfo_Dec2010_Update.docx`: batteries/relaunches/failures; no coordinates or new serial-to-waypoint bridge. Does not document a S/D relocation.
- `2010 activities summaries.pdf`: OSL sample-site coordinates support a broad shallow-south/deep-north pattern, but these are different core locations without matching logger serials. Not substitutes for logger GPS. The document itself cautions some descriptions may be inaccurate; no relabeling based on these.
- `University Valley Campbell notes Dec 2010.pdf`: W station serial/coordinate/probe inventory and photographs, not S/D proof.
- Targeted public searches for University Valley logger serial/deployment GPS and exact coordinates found no separate original waypoint export, serial-tagged station plan, or correction. This is a bounded unsuccessful search, not a claim that such records do not exist.
- Direct publisher PNG download returned 403; official PDF download succeeded, so the figure was inspected without that blockage.

## Exact missing primary bridge / stopping rule

Need the original December 2009 deployment GPS waypoint export/fieldbook or dated station map/photo log joining all of: (1) U12 serial 1122968 versus 2432936 (ideally U23 2429439 versus 2429437), (2) logger deployment name and 8/36 cm ice-table probe assignment, (3) measured waypoint/coordinates with datum and uncertainty, and (4) any December 2010 redeployment/relocation history. An author-issued correction explicitly reconciling the 2009 inventory, 2022 Fig.1b and Methods coordinates, and the repeated 2026 coordinates would also resolve the attribution.

Do not silently promote D=A/S=B to verified. Existing depth evidence plus the figure favor it, but neither verifies the physical serial-to-location bridge independently. Continue station-internal analysis by source file/serial; withhold coordinate-dependent terrain/illumination attribution until that bridge or explicit correction is obtained. No repeat download, thermal fit, or nearby-depth match can fill this missing record.

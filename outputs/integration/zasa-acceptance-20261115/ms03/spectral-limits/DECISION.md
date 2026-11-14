# MS-03 scientific detection boundary

Read-only audit, 2026-11-14. No repository edits. No new ice or non-ice classification.

## Decision
Numeric-valid samples establish decodable finite positive I/F and wavelength support, not signal identity, uncertainty, detection probability or a non-detection upper limit. Existing CRISM QA explicitly leaves atmosphere, thermal/photometric correction, cloud/frost masking, instrumental residuals, wavelength-dependent footprint and ice calibration incomplete. Selected two L-detector strips are at Ls 88.05 and 95.41; they are not all seasons or all twelve available products. 966 and 8516 passing pixel centres cannot establish ice absence, area completeness, independent measurements or a depth/content bound.

A correct BD1500_2 implementation would still not uniquely distinguish surface H2O frost from atmospheric ice aerosols. Strong absorption or a positive summary parameter is not a statistical detection unless uncertainty and false-positive controls are evaluated. Conversely a small value cannot exclude subpixel, dust-covered or subsurface ice. The #19 formula/official-product mismatch and #21/#23 missing replay inputs concern processing provenance, not a measured scientific noise floor. Do not use the roughly 0.01935 production difference as either detection significance or an ice upper limit.

## Executed bounded check
`python3 check.py` evaluates actual anchor wavelength mismatch from retained repository anchor_channels.csv. The nearest nominal 1525 nm anchor is median 1514.1665 nm for HSP and 1508.4043 nm for MSP, offsets -10.8335 and -16.5957 nm. Maximum column-specific mismatches are 15.6746 and 18.6360 nm. This is quantitative sampling-adequacy QC only. It does not substitute missing channels or justify applying a contiguous hyperspectral kernel to sparse mapping spectra.

No quantitative frost/cloud/material discrimination was executable defensibly within this bounded pass. IRR1 is a documented candidate discriminator but requires matched visible/NIR channels absent from these selected L-only retained inputs, and its class tendency is not a universal mask or statistical test. A valid next test needs paired co-registered VNIR/IR data and documented mapping-mode wavelengths, cloud/frost controls, instrument/atmospheric correction checks, and injection/recovery or validated endmember/noise tests with detection and false-positive rates. Multi-season repeated observations are needed to distinguish persistent surface material from seasonal alternatives. Existing material quantities cannot be reclassified based on this audit.

## Sources read
- Primary PDS CRISM DPSIS v1.3.7.7, Table 3-3 and summary context: https://pds-geosciences.wustl.edu/mro/mro-m-crism-2-edr-v1/mrocr_0002/document/crism_dpsis.htm
- Primary PDS targeted/processed dataset parameter descriptions (IRR1, water/ice/mineral parameters): https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=MRO-M-CRISM-5-RDR-MPTARGETED-V1.0
- Instrument-team PDS workshop distinguishes BD1500 surface ice and atmospheric aerosols: https://pds-geosciences.wustl.edu/workshops/CRISM_Workshop_Mar12_presentations/CRISM_workshop_2012_MTRDR_SUM_BRS_FPS_SLM.pdf
- Existing repository CRISM README.md, qa.json, anchor_channels.csv: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/tree/main/outputs/research/MS-03/local_validation/crism
- Existing PR records #19, #21, #23, read in full through GitHub. These establish scope and unresolved provenance, not detection validation.

Artifacts: inputs.json retains QA and anchor table; sampling_check.json is reproducible. No standard ice index, significance, calibrated upper limit or material classification generated.

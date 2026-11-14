# BD1500_2: disclosed-code and product-version audit

- Starting main: `fbfa780cf587a0787739200898e80b4d27fea8d1`; fixed MS-03 ROI unchanged.
- Outcome: current multispectral calculation follows the disclosed CAT equation. No numerical correction is justified. The cause of the remaining MRDR product difference is **unknown**.
- Inputs remain unchanged: original MRDR bytes, official parameters, prior recalculation, per-pixel source mask and earlier figure. This package adds diagnostic calculations only.

|Check|Actual result|Limit|
|---|---|---|
|CAT7.4 code vs July2026 document|Same multispectral .5RB1505+.5RB1558 definition, actual nearest wavelengths|Not proof of the1.03.94 production caller/build|
|Python port vs prior calculation|Max absolute difference0 on13,169 strict-source centres|Port of equation; original IDL/runtime not executed|
|Float32 perturbation|Max≈1.35e-7; full product difference max≈0.01935|Cannot explain full difference; not a bound on every producer operation|
|LBL/HDR order|All60 names agree; BD1500_2 zero-based index24|Cannot certify a producer-side physical-band label error absent|
|Independent byte requests|6/6 point values match original retained AL/SU bytes|Three locations/two quantities, not all-file provider checksum|
|ICER1_2 identity on official output bands|Max absolute difference≈0.001822; float perturbation≈1.72e-7|Numerical identity not preserved; cause and intended production stage remain unknown|
|Source grouping|Differences vary across contributing source groups|Location, era, source and processing are confounded; no causal assignment|

## Version/source distinction

- MRDR label names **crism_mapping_execute_flow1.03.94**, product creation2023-07-18. Its exact executable, source, build/hash, caller options and local coefficients were not obtained.
- Official **CAT7.4** code-only archive was acquired and member CRC/SHA verified. The BD function comments record May2012 and March2013 changes; release notes are dated2018-12-28. This is a separate public toolkit, not the version number of the MRDR production flow.
- CAT helper code: with `hyper=false`, nearest single-channel extraction is used; supplied kernel widths do not activate hyperspectral filtering. Continuum weights use the actual nearest sampled wavelengths.
- **PDS July2026 reference** selected pp1–2,5 agrees with that equation. Its later date alone does not explain the residual.
- **JHUAPL/JCAT** pinned commit `ba093b070c6d535c15209c8fc2d7a6b2893eb017` (2024-10-31): relevant targeted path uses1525nm hyperspectral kernel; pom says0.0.1-SNAPSHOT. It is not established as the exact packaged JCAT1.1 executable or MRDR1.03.94 code, and was not substituted for mapping processing.
- Fetched CAT archive:320 readable members scanned; no production-flow name match. Official MRDR document directory lists documentation, not the executable. These are bounded search scopes, not proof that the source is globally unavailable. No team-only author server was accessed and no author was contacted.
- Source URL, exact member, line locator, version and limits: `version_comparison.csv`, `disclosed_source_inventory.json`, `jcat_provenance.json`. Four JCAT blobs were verified against original Git blob SHA1 as well as SHA256.
- CAT raw archive/extracted code and JCAT source copies are local-only. Source links/hashes/locators are retained for inspection. JCAT is MIT-licensed; its license is retained. No blanket new license is assigned to external software.

## Interpreting the diagnostics

- The ICER check applies the disclosed identity `1-(1-BD1435)/(1-BD1500_2)` to the official output triplet. Its mismatch establishes only that these delivered values do not preserve this algebraic identity at the tested precision.
- SIS/catalogue describes strip normalization and separate production stages. Without the exact production configuration/intermediates, this context does not establish that normalization caused this particular difference.
- No fitted gain/offset, clipping, zero substitution, threshold or adjustment to force agreement was applied.
- Ice presence/depth/content, local cloud/frost quality and AD1 morphology status remain unchanged/unknown. Arithmetic checks do not validate ice detection.

## Reproduce and read scope

- System Python `acquire.py` downloads the public CAT code-only ZIP, release notes and reference PDF; `extract_sources.py` inventories relevant functions and locally extracts originals. `fetch_checks.py` repeats six exact point ranges and fetches the official document listing.
- JCAT source URLs are pinned in `jcat_provenance.json`; the public GitHub connector supplied the originals. Restore exact raw files from those URLs if checking source bytes locally.
- Scientific Python (numpy/matplotlib): `compare.py`, `plot.py`; then system Python `build_tables.py` and `validate.py`. `validate.py --retained-only` exercises retained input evidence without ignored source copies.
- Original IDL/CAT and the full production pipeline were not run. Diagnostics are explicit Python ports/independent calculations, not a producer-certified reproduction.
- Relevant CAT functions and helper bodies were read; JCAT BD branch/helper/pom metadata were read, not its full UI. Reference PDF pp1–2,5 and existing SIS§3.5.1/normalization sections were used. Original entire documents are not claimed fully reviewed.
- New figure: `F-BD01_version_and_arithmetic_audit.png`; ranges are spatial percentiles, not confidence intervals.
- To resolve the remaining cause: obtain1.03.94 source/executable and build identity, selected branches/options, intermediate pre/post-normalization AL/SU arrays, corresponding gain/offset files and SU source assignment. No claim these files were acquired.

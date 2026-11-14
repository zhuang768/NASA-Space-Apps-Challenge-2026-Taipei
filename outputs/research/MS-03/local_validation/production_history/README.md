# MRDR production history evidence

- Starting main: `826780f0b270eebe9b6f2f64b8ba1ac5ddcc8177`. Checked on 2026-11-15 (Taipei).
- Scope: MS-03, 57.50 to 58.00°N, 242.00 to 242.50°E, planetocentric/east-positive. This package inspects processing provenance. It adds no ice detection or correction.
- [Source/read-scope table](source_audit.csv), [availability and missing inputs](availability.csv), [version comparison](version_history.csv), [processing stages](processing_stages.csv), [search log](search_log.csv).

| Question | Evidence | Status |
|---|---|---|
| Was a summary-stage adjustment documented before the tile was made? | Archived SIS1.3.7.6, dated 2022-06-22, captured 2022-09-30; Appendix P3 section8. Its normalized section text matches SIS1.3.7.7. | Confirmed documentation, not a recovered execution |
| Does the actual tile identify its producer? | AL and SU XML both identify `crism_mapping_execute_flow`1.03.94 and production on 2023-07-18. | Confirmed label metadata |
| Can the exact residual be reconstructed? | No exact source/build, options, coefficients or paired intermediate arrays obtained. | Unknown |
| Can older MRDRs serve as the unnormalized input? | Earlier versions change inputs, formulas and product sets. | Not a controlled before/after pair |

- The documented sequence includes reflectance optimization, parameter evaluation, then another optimization of surface summary products. Thus evaluating the formula on delivered AL alone need not reproduce delivered SU. This is a workflow-level explanation; the size and origin of this tile's residual remain unknown.
- The historical snapshot predates this product. It does not identify the implementation in build1.03.94. The current SIS alone also cannot prove which settings ran in 2023.
- Prior strict-subset differences are referenced unchanged in `results.json`: 13,169 mapped centres, median calculated-minus-official +0.0007114219669, maximum absolute0.01934733452, dimensionless. These are previous results, not a new measurement or calibrated uncertainty.
- No gain/offset fitting, clipping, interpolation, value replacement or new physical inference. Ice presence, depth and content remain unknown. AD1 remains a general method reference; morphology remains unknown.

## Reproduce and inspect

1. `python3 acquire.py --replay-plan` retries the frozen bounded URL plan, including recorded failures. Original large HTML/PDF inputs stay local; URLs, retrieval status, lengths and SHA256 remain in Git. Failed requests do not establish absence.
2. `python3 inspect_history.py` parses acquired SIS and XML. `history_sections.json` records the normalization method, text offsets and hashes; only a nine-word quotation is retained. The original documents remain unmodified.
3. `python3 build_records.py` writes the reviewed tables. `plot_workflow.py` creates a documentation schematic, not an observed execution trace.
4. `python3 validate.py` checks all available sources and preserved inputs. `python3 validate.py --retained-only` checks the material retained in Git without requiring ignored source downloads.

- Author public material: LPSC2022 abstract2361, pp1-2, describes the optimization framework. The web reader returned both pages; the separate binary request returned403. The HSP author manuscript was only read as a publisher search excerpt. Neither supplies the requested exact production program.
- Public GitHub searches are bounded: exact code query, repository metadata queries for JHUAPL and the author-linked Michael-S-Phillips account, and JCAT release metadata. Search results are not a complete historical software inventory. Related analysis tools and JCAT releases are not substituted for the producer.
- Guessed old3001/3101 archive paths returned404. They do not establish that historical products never existed. No old arrays were obtained or used as pre-normalization data.
- The upstream CAT/JCAT arithmetic and byte checks in [the prior audit](../bd1500_audit/README.md) were not repeated as new research.
- Raw official XML and small metadata responses are retained verbatim for provenance. No new redistribution license is asserted for third-party material. The workflow figure and inspection scripts were created by this project.

## Handoff inputs still needed

- Exact build/source hash, dependency manifest and executable; the actual caller and run settings.
- Same-source strip AL and summary arrays before/after each optimization, pixel masks and traceability IDs.
- Gains/offsets or other actual transformations for each strip/channel/parameter, weights, anchor selection, optimization diagnostics and logs.
- GPU: replay only after those inputs arrive. Keep official SU, formula-only results and future stage-replay results separate; do not tune values to match.
- Human research lead: describe this as documented processing-stage non-equivalence with unresolved numerical attribution. Do not label official data erroneous or claim a new ice detection.

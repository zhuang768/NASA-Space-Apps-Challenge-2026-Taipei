# T1811 run-artifact follow-up

- Starting main: `fee734610c6bacc57880eaaba1a1301f09fdd4d6`. Date: 2026-11-15, Taipei.
- Fixed MS-03 ROI:57.50 to58.00°N,242.00 to242.50°E, planetocentric/east-positive.
- [Source/read-scope audit](source_audit.csv), [artifact decisions](artifact_status.csv), [exact replay inputs needed](replay_inputs_needed.csv), [search attempts](search_log.csv).

| Checked material | Result | Limit |
|---|---|---|
| Official bundle and data inventory | 7,056 data members;4 for T1811:AL/SU/DE/WV. Labels and the existing physical listing agree. | No identified run configuration, optimizer table or paired intermediate product in these checked entries; not a global absence claim. |
| Original index | Four exact792-byte T1811 records retained with field definitions and original record positions. | Reuses the previously acquired original index; no new scientific analysis. |
| Author-deposited paper | Original34-page PDF acquired; repository MD5 verified. Selected pp24-26 and32 read; processing figures visually checked. | The paper is a method description, not the actual execution archive. |
| Before/after example | Fig23 shows Jezero VNIR RGB, outside MS-03, with separate automatic stretches. | Cannot supply T1811 BD1500_2 normalization pairs or coefficients. |
| Actual numerical replay | Not performed: run settings, optimizer outputs and paired intermediate arrays were not obtained. | Numerical cause remains unknown. No values were corrected. |

- The repository record lists one PDF and no related dataset identifier; the PDF contains no embedded files. Its availability statement points to PDS. This describes the checked deposit, not every possible author archive.
- Fig21 identifies model inputs and outputs that a replay would need. The five strips contributing selected local pixels do not establish the full optimization network or anchors. Request the actual dependency set before limiting extraction to those strips.
- Distinguish sensor calibration CDRs, atmospheric/photometric ADR lookup corrections, storage/map offsets and interstrip optimization parameters. None can silently substitute for another. SIS section2.3.4.11 discusses ADR archive plans as of2023; that statement does not establish the current global availability of optimizer coefficients.
- Prior strict residual statistics remain unchanged in `replay_readiness.json`, referenced from `../bd1500_audit/results.json`. Ice presence, depth and content remain unknown. AD1 and morphology status are unchanged.
- GPU: keep official SU and formula-only calculations separate. Replay only after receiving versioned settings, matrices/weights/anchors, model outputs, same-source before/after arrays and projection/template inputs. Do not fit a correction to force agreement.
- Human research lead: the new evidence narrows the available archive contents and rejects a non-local illustrated pair as a replay input. It does not recover the production run or establish a numerical cause.

## Reproduce

1. SystemPython:`python3 acquire.py` retries the bounded `request_plan.json`. Requests append provenance; changed downloads receive a hash-suffixed filename instead of overwriting earlier bytes. Temporary signed redirect queries are omitted from the log.
2. `python3 inspect_inventory.py` inspects bundle/member references and extracts exact records from the existing original index. No physical data transformation occurs.
3. With pypdf installed:`python3 inspect_paper.py`. Only page locators and text hashes are retained; the original PDF stays local. Render pp24-26 using `pdftoppm` for figure checks.
4. `python3 build_records.py` writes reviewed tables. `python3 validate.py` verifies acquired sources and preserved inputs; `--retained-only` excludes ignored downloads and validates retained excerpts.

- The raw paper is CC BY-NC-ND4.0, retained locally without modification and not redistributed in Git. Its DOI is `10.1016/j.icarus.2023.115612`; the original deposit is linked in `source_audit.csv`.
- Full global inventory and large source files stay local. SHA256, provider MD5, URLs, exact subset records and parsing scripts remain traceable. Source metadata is retained verbatim; no new license for third-party material is asserted.

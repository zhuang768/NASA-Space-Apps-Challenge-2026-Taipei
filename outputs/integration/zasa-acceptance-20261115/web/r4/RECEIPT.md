# R4 public release verification

- Live site: https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev/
- Updated live-capture Demo: https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev/demo (same URL, silent 24.000 s 1280×720 H.264, no identity, SHA-256 `cde357a450532bc31b10c433bdb2eb35bbcf32d945ead3911d8df559a34d095c`, 1,844,300 bytes).
- Production Worker version `9d12fadb-1abb-45be-9f26-e7b6e481e7b9`, deployment `4e368e0e-5ce0-492a-b5ee-179193a2b257` at 100%. All seven public responses verified signed-out for exact bytes/MIME; 390px touch interaction, no overflow and playback passed. A separate readback matched the production deployment JSON and MP4 by SHA-256.
- Explorer fixed the SWIM index wording and added exact-product TES and SWIM catalog links; no numeric cells changed. A new genuine recording includes the corrected explanation. Existing releases/acceptance snapshots were not overwritten. R4 manifest distinguished here under `web/r4/`.
- The private research reports are unchanged. This verifies site delivery, not NASA portal submission.

# Explorer evidence and usability refinement

Starting main: `25b0744ac3d2230803505e1679109c2c35b6204d`.

This update changes presentation and navigation. It adds no new observations, scientific analysis, candidate, score or analogue validation.

## Changes

- The overview separates completed regional checks, Earth method references and unverified claims.
- Each of six tabs starts with its interpretation limit and has an expandable **Source & scale** section. Repository links pin the starting commit instead of silently following later data edits.
- Comparison plots use three aligned rows, one per region, with a shared numeric domain. The signed SWIM domain remains −1 to +1.
- A region selector keeps the current research theme while changing the target. Review-cell bounds are visible.
- Earth thermal and latitude plots use progressive disclosure. The air series is labelled January–November 2010; the month selector also works without pointer hover.
- The existing dark palette, serif headings, MOLA globe and three region colours are retained. Mobile uses a smaller map and six visible tabs.
- Map-load errors expose a retry action while leaving the research controls usable.

## Checks actually performed

- JavaScript syntax and Git whitespace checks.
- All 18 region/tab combinations rendered in the browser.
- Desktop 1440 × 960, phone 390 × 844 and 320 × 800, and tablet 768 × 1024 were inspected. No document-level horizontal overflow was found at these sizes. The four-reference matrix's narrowest cells were 48.4 px wide at 320 px.
- Region switching, Earth matrix selection, MY34/MY35 switching, source disclosure, the Sources dialog, keyboard End navigation, month selection and the Mars-context toggle were operated. Month selection and the expanded thermal section persist after the toggle.
- A temporary copy with `mola.jpg` omitted showed the error message, retained region/chart access and exposed the retry control. This tests the failure path; it does not claim an unavailable upstream tile service recovered.
- Five scientific source arrays and five protected research files match the starting commit. The existing challenge-alignment check also passed.
- The mechanical design detector ran once using its degraded regex fallback. No findings were reported; parser-based selector matching and computed contrast were unavailable. The main foreground and secondary text colours were checked separately against the background.
- Browser error-log query returned no errors on the normal preview. The missing-image fixture was checked separately.

See [browser_checks.json](browser_checks.json), [value_preservation.json](value_preservation.json), and [check_evidence.py](check_evidence.py). Screenshots: [desktop overview](desktop_overview.png), [desktop ice evidence](desktop_ice.png), [mobile ice evidence](mobile_ice.png).

## Re-run local checks

```sh
python3 outputs/integration/site_polish_20261115/check_evidence.py
python3 scripts/verify_challenge_alignment.py
python3 scripts/verify_release.py
node --check outputs/integration/zasa-acceptance-20261115/web/app.js
```

Browser checks are recorded observations, not an automated browser-test suite. Google Fonts and NASA Trek detail tiles remain external runtime dependencies. The fallback map is retained locally.

## Limits retained

Local Mars ice presence, depth and amount remain unconfirmed. Earth records are method references, not validated Mars matches. MS-03 fixed-window morphology remains unknown. The precise published definition of University Valley's reported temperature variation was not newly verified; the interface does not rename it daily amplitude. No generated waveform, local mineral interpretation or similarity percentage was added.

## Public deployment

Cloudflare deployed code `e26bc0541b21f371a2ac5c8299e8d1412aeb214d` successfully. Build `da71e1cf-8869-4bce-9aaa-fbfe48445a0c`, Worker version `d186c80e-7075-4b38-93bf-b7f96f52af82`.

The public fingerprint and four assets match the local files byte-for-byte. Redirects were followed: `/index.html` redirects to the canonical root. Public desktop source disclosure and mobile region/Earth-matrix selection were operated, with no horizontal overflow at 1440 px or 390 px. See [the deployment receipt](public_deployment_verification.json), [public desktop capture](public_desktop.png) and [public mobile capture](public_mobile.png).

The later verification-record commit changes documentation and inventory metadata only; the deployed four-file payload is unchanged.

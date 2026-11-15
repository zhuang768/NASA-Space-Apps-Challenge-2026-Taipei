# MS-03 repository-only validation, 2026-11-15

Frozen source main: `07dbe29203504ba0ccde5e379f42ecc16e4b1b4f`. PR #26 inspected: `ac39ed6810156feefd97f60647b95b754210a7da`.

| Check | Result |
|---|---|
| MS-03 regional numeric reproduction | 70 of 70 checks passed |
| Earth closed-vector readback | 185 AD1 source polygons; limited accuracy validation |
| In-box Mars-to-Earth contour comparison | insufficient; no accepted Mars contours |
| Cape Blossom quantitative source package | not found in the searched GitHub records |
| Novelty | insufficient |

This is completion type B: a completed bounded audit, not a passed Earth-to-Mars comparison. Width, area and density remain NA when no Mars contour is accepted.

Read [methods and findings](audit_details.md), [numeric evidence](numeric_evidence.csv), [window decisions](mars_audit/windows.csv), [missing inputs](unmeasured_items.csv), and [reproduction instructions](REPRODUCE.md). The [support figure](mars_audit/MS03_support_and_review_windows.png) separates retained pixels from inspected windows.

The Earth GeoJSON re-encodes published AD1 outlines with source record IDs. It contains no Mars contours and does not certify independent annotation accuracy. No additional field measurements, image sharpening or invented boundaries were used.

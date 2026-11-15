# Replaying the final comparison

Run these commands from the repository root. Use a new local directory outside
the checkout for each replay. The committed tables are reference outputs, not
new observations. No replay verifies the three Earth–Mars pairings.

## 1. Verify inputs

```sh
REPLAY=outputs/research/final-comparison-20261115/replay
python3 "$REPLAY/check_inputs.py" --repo .
# Optional: verify three exact team archives obtained separately:
python3 "$REPLAY/check_inputs.py" --repo . --archives /path/to/team-archives
```

[Input manifest](inputs.json): expected paths, file sizes and SHA-256 digests.
The team ZIP names describe exact delivery packages, not DOI filenames.
Request them from a team member who has access. Do not publish source files
with restricted redistribution terms.

## 2. Choose a workflow

| Workstream | Inputs | Run guide |
|---|---|---|
| MS-01 temperature and Mars crop | Separate `MS01_validation_20261115.zip` and combined ZASA ZIP | Command below |
| MS-02 SHARAD and Adventdalen core log | Already tracked in repository | [MS-02 instructions](ms02/REPLAY.md) |
| MS-02 Askja | Separate team archives or the listed original CC0 USGS data | [MS-02 instructions](ms02/REPLAY.md#askja-separate-inputs) |
| MS-03 AD1 gridding | Original polygon ZIP already tracked in repository | [MS-03 instructions](ms03/README.md) |

### MS-01

Use Python 3.12 and NumPy as listed in [requirements](ms01/requirements.txt).
With both verified ZIPs available:

```sh
python3 "$REPLAY/ms01/replay.py" \
  --ms01 /path/to/MS01_validation_20261115.zip \
  --combined /path/to/ZASA_independent_validation_20261115.zip \
  --out /tmp/zasa-ms01-replay
```

The replay checks the daily harmonics, 428 Mars crop rows, and the annual
phase comparison and sensitivity tables. The output includes working copies of
source data; keep it out of the repository. This workflow does not verify
historical depths, material controls, or ice classification.

### MS-02 and MS-03

Follow the linked guides using the same checkout for the scripts and pinned
repository inputs. The SHARAD workflow should produce 194 widths and the AD1
workflow 11,840 gridding cases. Existing Cape contrast and Mars image review
are described in the [comparison results](../README.md); reproducing the
image workflows requires separate projected image subsets, not just this
checkout.

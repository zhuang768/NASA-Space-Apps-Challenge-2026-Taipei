#!/usr/bin/env bash
# Set GitHub secret CLOUDFLARE_API_TOKEN without pasting the token into chat.
# Usage:
#   1. Create a Cloudflare API token (Edit Cloudflare Workers template) on the zizi account
#   2. Run:  bash scripts/set_cloudflare_token_secret.sh
#   3. Paste the token when prompted (input is hidden), then press Enter
set -euo pipefail
REPO="${REPO:-zhuang768/NASA-Space-Apps-Challenge-2026-Taipei}"

echo "Repo: $REPO"
echo "Paste CLOUDFLARE_API_TOKEN (hidden), then Enter:"
IFS= read -r -s TOKEN
echo
TOKEN="$(printf '%s' "$TOKEN" | tr -d '\r\n' | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')"

if [[ -z "$TOKEN" ]]; then
  echo "Empty token; aborted." >&2
  exit 1
fi
if printf '%s' "$TOKEN" | grep -qE '[[:space:]]|[^\x21-\x7e]'; then
  echo "Token still contains whitespace or non-ASCII characters; copy the raw token only." >&2
  exit 1
fi

printf '%s' "$TOKEN" | gh secret set CLOUDFLARE_API_TOKEN -R "$REPO"
echo "CLOUDFLARE_API_TOKEN updated."
echo "Next: gh workflow run \"Deploy TerraMatch Mission Lab to Cloudflare (team Worker)\" -R $REPO"

"""Verify the publicly served deployment stamp and linked application assets."""

import json
import os
import re
import time
from urllib.parse import urljoin
from urllib.request import Request, urlopen


def fetch(url):
    # Cloudflare often returns 403 to bare urllib clients from cloud IPs.
    request = Request(
        url,
        headers={
            "Cache-Control": "no-cache",
            "User-Agent": (
                "Mozilla/5.0 (compatible; TerraMatchReleaseVerify/1.0; "
                "+https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei)"
            ),
            "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        },
    )
    with urlopen(request, timeout=15) as response:
        return response.read()


def main():
    base = os.environ["SITE_URL"].rstrip("/") + "/"
    expected = os.environ["GITHUB_SHA"]
    last_error = None
    for attempt in range(6):
        try:
            stamp = json.loads(fetch(urljoin(base, f"deployment.json?commit={expected}")))
            if stamp.get("commit") != expected:
                raise ValueError("The public site still serves another commit")
            html = fetch(base + f"?commit={expected}").decode()
            assets = re.findall(r'(?:src|href)="(/assets/[^"\s]+)"', html)
            if not assets:
                raise ValueError("No application assets found in the public HTML")
            for asset in assets:
                if not fetch(urljoin(base, asset)):
                    raise ValueError("Public application asset is empty")
            print(
                f"Verified public release {expected}; {len(assets)} application assets accessible."
            )
            return
        except (OSError, ValueError) as error:
            last_error = error
            if attempt < 5:
                time.sleep(5)
    raise RuntimeError(f"Public release verification failed: {last_error}")


if __name__ == "__main__":
    main()

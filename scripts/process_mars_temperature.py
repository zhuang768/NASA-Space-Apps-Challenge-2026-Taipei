"""Download a bounded MEDA pilot and export auditable local temperature context."""

import argparse
from html.parser import HTMLParser
from pathlib import Path

import requests

from analog import mars, temperature
from analog.provenance import write_json


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        href = dict(attrs).get("href", "")
        if tag == "a" and "CAL_TIRS" in href and href.endswith((".CSV", ".xml")):
            self.links.append(href)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--raw-dir", type=Path, default=mars.RAW_DIR)
    parser.add_argument("--output", type=Path, default=Path("outputs/mars_temperature"))
    args = parser.parse_args()
    if args.download:
        folder = args.raw_dir / "temperature/meda_calibrated"
        folder.mkdir(parents=True, exist_ok=True)
        for sol in (700, 701, 702):
            base = temperature.BASE + f"sol_{sol:04d}/"
            response = requests.get(base, timeout=60)
            response.raise_for_status()
            links = Links()
            links.feed(response.text)
            if len(links.links) != 2:
                raise ValueError("Expected one CSV/label pair; inspect archive versions manually")
            for name in links.links:
                if Path(name).name != name:
                    raise ValueError("Unexpected archive filename")
                mars._fetch(base + name, folder / name)
    context, hourly = temperature.build_context(args.raw_dir)
    if context["status"] == "missing":
        raise FileNotFoundError(context["reason"])
    write_json(args.output / "summary.json", context)
    hourly.to_csv(args.output / "provisional_hourly.csv", index=False)
    print(f"{context['records']} records; {context['quality_supported_records']} quality-supported")
    print(f"Saved {args.output}; provisional observations are excluded from scoring")


if __name__ == "__main__":
    main()

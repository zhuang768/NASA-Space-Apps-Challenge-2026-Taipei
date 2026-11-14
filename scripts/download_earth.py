"""Download public terrain, or discover/download bounded Earthdata monthly products."""

import argparse

from analog import earth


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--product", choices=["public", "lst", "ndvi", "precipitation", "aod"], default="public"
    )
    parser.add_argument("--start", default="2023-01-01")
    parser.add_argument("--end", default="2024-12-31")
    parser.add_argument(
        "--download",
        action="store_true",
        help="Earthdata: actually download; otherwise discovery only",
    )
    args = parser.parse_args()
    if args.product == "public":
        print(earth.download_public())
    else:
        result = earth.download_monthly(args.product, args.start, args.end, args.download)
        print(f"{len(result['granules'])} granules: {result['status']}")


if __name__ == "__main__":
    main()

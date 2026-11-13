"""Download the Mars grids listed in analog.mars.PRODUCTS (about 110 MB in total)."""

from analog import mars


def main() -> None:
    for name in mars.PRODUCTS:
        path = mars.download(name)
        print(f"{name}: {path} ({path.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()

"""Download all Mars grids: MOLA, TES (about 110 MB) and SWIM ice maps (about 140 MB)."""

from analog import mars, swim


def main() -> None:
    for module in (mars, swim):
        for name in module.PRODUCTS:
            path = module.download(name)
            print(f"{name}: {path} ({path.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()

"""Download all Mars grids: MOLA + TES (110 MB), SWIM ice (140 MB), dust (115 MB)."""

from analog import dust, mars, swim


def main() -> None:
    for module in (mars, swim, dust):
        for name in module.PRODUCTS:
            path = module.download(name)
            print(f"{name}: {path} ({path.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()

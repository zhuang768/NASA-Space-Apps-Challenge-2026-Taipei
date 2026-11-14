"""Build data/processed/mars_stack_0p5deg.nc and print a summary per layer."""

from analog import stack as stack_mod


def main() -> None:
    stack = stack_mod.build_mars_stack()
    for name, layer in stack.data_vars.items():
        print(
            f"{name:16s} {float(layer.min()):>10.2f} .. {float(layer.max()):<10.2f}"
            f" median {float(layer.median()):>8.2f}"
            f"  missing {float(layer.isnull().mean()) * 100:5.1f}%"
        )
    path = stack_mod.save(stack)
    print(f"saved {path} ({path.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()

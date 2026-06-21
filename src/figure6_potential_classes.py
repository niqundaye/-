"""Reproduce Figure 6: spatial optimization-potential classes."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from analysis_config import FIGURES, spatial_units_path
from optimize_allocation import ensure_optional_columns
from plot_utils import pseudo_grid, save_or_show
from core.spatial_potential.classifier import classify_units


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    root = Path(__file__).resolve().parents[1]
    input_path = root / args.input if args.input else spatial_units_path()
    output = root / args.output if args.output else FIGURES / "figure6_potential_classes.png"
    df = ensure_optional_columns(pd.read_csv(input_path))
    labels = classify_units(df)
    order = {
        "Cooling-priority units": 0,
        "Ventilation-priority units": 1,
        "Economic-priority units": 2,
        "Balanced-development units": 3,
        "Ecological-restricted units": 4,
    }
    df["class_code"] = labels.map(order)
    grid = pseudo_grid(df, "class_code")
    fig, ax = plt.subplots(figsize=(8, 7))
    cmap = ListedColormap(["#d95f02", "#1b9e77", "#7570b3", "#66a61e", "#1f78b4"])
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=4, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Figure 6. Spatial optimization-potential classification", fontsize=13)
    handles = [plt.Line2D([0], [0], marker="s", linestyle="", color=cmap(i), label=name) for name, i in order.items()]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.20), ncol=2, fontsize=8)
    save_or_show(fig, output)


if __name__ == "__main__":
    main()

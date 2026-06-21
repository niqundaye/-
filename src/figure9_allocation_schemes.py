"""Reproduce Figure 9: representative allocation schemes."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from analysis_config import FIGURES, spatial_units_path
from core.optimization.qla_coa import assign_strategy, ensure_optional_columns
from plot_utils import pseudo_grid, save_or_show


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    root = Path(__file__).resolve().parents[1]
    input_path = root / args.input if args.input else spatial_units_path()
    output = root / args.output if args.output else FIGURES / "figure9_allocation_schemes.png"
    df = ensure_optional_columns(pd.read_csv(input_path))
    scenarios = ["baseline", "cooling_priority", "ventilation_priority", "economic_priority", "balanced_development"]
    fig, axes = plt.subplots(1, 5, figsize=(15, 3.8))
    cmap = ListedColormap(["#dddddd", "#d95f02", "#1b9e77", "#7570b3", "#66a61e"])
    for ax, scenario in zip(axes, scenarios):
        df["strategy"] = assign_strategy(df, scenario)
        ax.imshow(pseudo_grid(df, "strategy"), cmap=cmap, vmin=0, vmax=4, interpolation="nearest")
        ax.set_title(scenario.replace("_", " "), fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("Figure 9. Representative spatial allocation schemes", fontsize=13)
    save_or_show(fig, output)


if __name__ == "__main__":
    main()

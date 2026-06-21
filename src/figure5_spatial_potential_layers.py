"""Reproduce Figure 5: LST, SVF, economic benefit, and integrated potential."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from analysis_config import FIGURES, spatial_units_path
from optimize_allocation import ensure_optional_columns
from plot_utils import plot_grid_map, save_or_show


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    root = Path(__file__).resolve().parents[1]
    input_path = root / args.input if args.input else spatial_units_path()
    output = root / args.output if args.output else FIGURES / "figure5_spatial_potential_layers.png"
    df = ensure_optional_columns(pd.read_csv(input_path))
    df["integrated_potential"] = 0.4 * df["cooling_potential"] + 0.3 * df["ventilation_potential"] + 0.3 * df["economic_benefit"]
    panels = [
        ("lst_c", "(a) Land Surface Temperature", "inferno"),
        ("ventilation_potential", "(b) SVF-based Ventilation Potential", "viridis"),
        ("economic_benefit", "(c) Land-development Economic Benefit", "magma"),
        ("integrated_potential", "(d) Integrated Spatial Optimization Potential", "cividis"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, (col, title, cmap) in zip(axes.ravel(), panels):
        im = plot_grid_map(ax, df, col, title, cmap)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.suptitle("Figure 5. Spatial optimization-potential layers", fontsize=13)
    save_or_show(fig, output)


if __name__ == "__main__":
    main()

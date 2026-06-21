"""Reproduce Figure 1: study area and key spatial characteristics."""

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
    df = ensure_optional_columns(pd.read_csv(input_path))
    output = root / args.output if args.output else FIGURES / "figure1_study_area_characteristics.png"

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))
    for ax, col, title, cmap in [
        (axes[0], "elevation_m", "(a) Terrain / elevation", "terrain"),
        (axes[1], "lst_c", "(b) Land surface temperature", "inferno"),
        (axes[2], "economic_benefit", "(c) Economic benefit", "magma"),
    ]:
        im = plot_grid_map(ax, df, col, title, cmap)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.suptitle("Figure 1. Study area and spatial characteristics", fontsize=13)
    save_or_show(fig, output)


if __name__ == "__main__":
    main()

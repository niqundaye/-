"""Plotting helpers shared by manuscript figure scripts."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd


def save_or_show(fig, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, bbox_inches="tight")
    print(f"Wrote {output}")


def add_panel_label(ax, label: str) -> None:
    ax.set_title(label, loc="left", fontsize=10, fontweight="bold")


def pseudo_grid(df: pd.DataFrame, value_col: str) -> np.ndarray:
    """Convert unit-level values into a square-ish grid for non-geometry smoke tests."""
    values = df[value_col].to_numpy(dtype=float)
    n = len(values)
    cols = int(math.ceil(math.sqrt(n)))
    rows = int(math.ceil(n / cols))
    grid = np.full((rows, cols), np.nan)
    grid.flat[:n] = values
    return grid


def plot_grid_map(ax, df: pd.DataFrame, value_col: str, title: str, cmap: str = "viridis") -> None:
    grid = pseudo_grid(df.sort_values("unit_id") if "unit_id" in df else df, value_col)
    im = ax.imshow(grid, cmap=cmap, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, loc="left", fontsize=10)
    return im

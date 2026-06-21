"""Reproduce Figure 7: mechanism-to-strategy translation matrix."""

from __future__ import annotations

import argparse
from pathlib import Path

from analysis_config import FIGURES
from plot_utils import save_or_show


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    root = Path(__file__).resolve().parents[1]
    output = root / args.output if args.output else FIGURES / "figure7_mechanism_strategy_matrix.png"
    rows = ["Low NDVI", "High bare land", "High land-use intensity", "High SVF", "High night light", "River/wetland sensitivity"]
    cols = ["Cooling", "Ventilation", "Economic", "Balanced", "Ecological restriction"]
    matrix = [
        [1, 0, 0, 1, 1],
        [1, 0, 0, 1, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1],
    ]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.imshow(matrix, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(cols)), cols, rotation=35, ha="right")
    ax.set_yticks(range(len(rows)), rows)
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            ax.text(j, i, "yes" if val else "", ha="center", va="center", fontsize=9)
    ax.set_title("Figure 7. Translation from LST-driving mechanisms to planning strategies", fontsize=13)
    save_or_show(fig, output)


if __name__ == "__main__":
    main()

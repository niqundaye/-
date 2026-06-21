"""Reproduce Figure 2: research framework."""

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
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

    root = Path(__file__).resolve().parents[1]
    output = root / args.output if args.output else FIGURES / "figure2_research_framework.png"
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis("off")
    boxes = [
        (0.03, 0.55, "Stage 1\nRemote-sensing LST\nmechanism identification"),
        (0.36, 0.55, "Stage 2\nSpatial optimization\npotential assessment"),
        (0.69, 0.55, "Stage 3\nMulti-objective\nallocation optimization"),
        (0.03, 0.12, "Inputs\nLandsat, WorldCover,\nDEM, VIIRS, roads,\necology, monitoring"),
        (0.36, 0.12, "Interpretation\nCatBoost, SHAP,\nPDP, ICE, thresholds"),
        (0.69, 0.12, "Outputs\nPareto set, representative\nschemes, trade-offs"),
    ]
    for x, y, text in boxes:
        patch = FancyBboxPatch((x, y), 0.27, 0.26, boxstyle="round,pad=0.02", linewidth=1.2, facecolor="#eef3f7", edgecolor="#38546a")
        ax.add_patch(patch)
        ax.text(x + 0.135, y + 0.13, text, ha="center", va="center", fontsize=10)
    for start, end in [((0.30, 0.68), (0.36, 0.68)), ((0.63, 0.68), (0.69, 0.68)), ((0.165, 0.38), (0.165, 0.55)), ((0.495, 0.38), (0.495, 0.55)), ((0.825, 0.38), (0.825, 0.55))]:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=14, linewidth=1.2, color="#38546a"))
    ax.set_title("Figure 2. Research framework of the heat-resilient spatial allocation model", fontsize=13)
    save_or_show(fig, output)


if __name__ == "__main__":
    main()

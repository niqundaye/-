"""Reproduce Figure 8: Pareto front and objective trade-offs."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from analysis_config import FIGURES
from plot_utils import save_or_show


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="outputs/allocation_scenarios.csv")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    root = Path(__file__).resolve().parents[1]
    path = root / args.input
    if not path.exists():
        from optimize_allocation import main as run_opt
        run_opt()
    df = pd.read_csv(path)
    output = root / args.output if args.output else FIGURES / "figure8_pareto_tradeoff.png"
    fig = plt.figure(figsize=(12, 8))
    ax3d = fig.add_subplot(2, 2, 1, projection="3d")
    ax3d.scatter(df["mean_lst_c"], df["svf_potential"], df["economic_benefit"], s=60)
    ax3d.set_xlabel("Mean LST")
    ax3d.set_ylabel("SVF")
    ax3d.set_zlabel("Economic")
    ax3d.set_title("(a) Objective space")
    pairs = [("mean_lst_c", "svf_potential", "(b) LST vs SVF"), ("mean_lst_c", "economic_benefit", "(c) LST vs economic benefit"), ("svf_potential", "economic_benefit", "(d) SVF vs economic benefit")]
    for i, (x, y, title) in enumerate(pairs, start=2):
        ax = fig.add_subplot(2, 2, i)
        ax.scatter(df[x], df[y], s=55)
        for _, row in df.iterrows():
            ax.annotate(row["scenario"], (row[x], row[y]), fontsize=7)
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(title)
    fig.suptitle("Figure 8. Pareto-style objective trade-off analysis", fontsize=13)
    save_or_show(fig, output)


if __name__ == "__main__":
    main()

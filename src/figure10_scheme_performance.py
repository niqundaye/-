"""Reproduce Figure 10: representative scheme performance comparison."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
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
    output = root / args.output if args.output else FIGURES / "figure10_scheme_performance.png"

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    x = np.arange(len(df))
    axes[0].bar(x - 0.25, df["mean_lst_c"], width=0.25, label="Mean LST")
    axes[0].bar(x, df["svf_potential"], width=0.25, label="SVF")
    axes[0].bar(x + 0.25, df["economic_benefit"], width=0.25, label="Economic")
    axes[0].set_xticks(x, df["scenario"], rotation=30, ha="right")
    axes[0].set_title("(a) Performance comparison", loc="left")
    axes[0].legend()

    metrics = ["mean_lst_c", "svf_potential", "economic_benefit"]
    norm = df[metrics].copy()
    norm["mean_lst_c"] = 1 - (norm["mean_lst_c"] - norm["mean_lst_c"].min()) / (norm["mean_lst_c"].max() - norm["mean_lst_c"].min() + 1e-9)
    for col in ["svf_potential", "economic_benefit"]:
        norm[col] = (norm[col] - norm[col].min()) / (norm[col].max() - norm[col].min() + 1e-9)
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]
    ax = axes[1]
    ax.remove()
    ax = fig.add_subplot(1, 2, 2, polar=True)
    for idx, row in norm.iterrows():
        vals = row.tolist() + row.tolist()[:1]
        ax.plot(angles, vals, label=df.loc[idx, "scenario"], linewidth=1)
    ax.set_xticks(angles[:-1], ["Cooling", "SVF", "Economic"])
    ax.set_title("(b) Radar plot of normalized objectives", loc="left")
    ax.legend(fontsize=7, bbox_to_anchor=(1.28, 1.0))
    fig.suptitle("Figure 10. Performance comparison of representative schemes", fontsize=13)
    save_or_show(fig, output)


if __name__ == "__main__":
    main()

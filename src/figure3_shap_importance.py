"""Reproduce Figure 3: feature importance and SHAP-style effects."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from analysis_config import FEATURES, FIGURES, spatial_units_path
from figure4_pdp_ice import build_model
from plot_utils import save_or_show


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    root = Path(__file__).resolve().parents[1]
    input_path = root / args.input if args.input else spatial_units_path()
    output = root / args.output if args.output else FIGURES / "figure3_feature_importance.png"
    df = pd.read_csv(input_path)
    x = df[FEATURES]
    y = df["lst_c"].astype(float)
    model = build_model(args.seed)
    model.fit(x, y)
    if hasattr(model, "get_feature_importance"):
        importance = np.asarray(model.get_feature_importance(), dtype=float)
    else:
        importance = np.asarray(model.feature_importances_, dtype=float)
    order = np.argsort(importance)

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.2))
    axes[0].barh(np.array(FEATURES)[order], importance[order], color="#4c78a8")
    axes[0].set_title("(a) Global feature importance", loc="left")
    axes[0].set_xlabel("Relative importance")

    top = np.argsort(importance)[-7:]
    for idx in top:
        vals = (x.iloc[:, idx] - x.iloc[:, idx].mean()) / (x.iloc[:, idx].std() + 1e-9)
        axes[1].scatter(vals, y - y.mean(), s=8, alpha=0.35, label=FEATURES[idx])
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_title("(b) Directional effect diagnostic", loc="left")
    axes[1].set_xlabel("Standardized feature value")
    axes[1].set_ylabel("Centered LST")
    axes[1].legend(fontsize=7, ncol=1)
    fig.suptitle("Figure 3. LST-driving factor importance and effect diagnostics", fontsize=13)
    save_or_show(fig, output)


if __name__ == "__main__":
    main()

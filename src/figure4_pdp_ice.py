"""Reproduce Figure 4: PDP and ICE plots for LST-driving factors."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from analysis_config import FEATURES, FIGURES, spatial_units_path


PLOT_FEATURES = [
    ("ndvi", "(a) NDVI"),
    ("bare_land_prop", "(b) Bare-land proportion"),
    ("land_use_intensity", "(c) Land-use intensity"),
    ("svf", "(d) SVF"),
    ("night_light", "(e) Nighttime light"),
    ("elevation_m", "(f) Elevation"),
]


def build_model(seed: int = 2026):
    try:
        from catboost import CatBoostRegressor

        return CatBoostRegressor(
            iterations=700,
            depth=6,
            learning_rate=0.035,
            loss_function="RMSE",
            random_seed=seed,
            verbose=False,
        )
    except Exception:
        from sklearn.ensemble import RandomForestRegressor

        return RandomForestRegressor(
            n_estimators=500,
            min_samples_leaf=4,
            random_state=seed,
            n_jobs=-1,
        )


def compute_pdp_ice(model, x: pd.DataFrame, feature: str, grid_size: int = 45, n_ice: int = 120, seed: int = 2026):
    rng = np.random.default_rng(seed)
    lo, hi = np.quantile(x[feature], [0.02, 0.98])
    grid = np.linspace(lo, hi, grid_size)
    ice_index = rng.choice(len(x), size=min(n_ice, len(x)), replace=False)
    ice_source = x.iloc[ice_index].copy()
    pdp_values = []
    ice_values = []

    for value in grid:
        x_eval = x.copy()
        x_eval[feature] = value
        pdp_values.append(float(np.mean(model.predict(x_eval))))

        ice_eval = ice_source.copy()
        ice_eval[feature] = value
        ice_values.append(np.asarray(model.predict(ice_eval), dtype=float))

    return grid, np.asarray(pdp_values), np.vstack(ice_values).T


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    input_path = root / args.input if args.input else spatial_units_path()
    output_path = root / args.output if args.output else FIGURES / "figure4_pdp_ice.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    import matplotlib.pyplot as plt

    data = pd.read_csv(input_path)
    missing = [col for col in FEATURES + ["lst_c"] if col not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    x = data[FEATURES].copy()
    y = data["lst_c"].astype(float)
    model = build_model(args.seed)
    model.fit(x, y)

    fig, axes = plt.subplots(2, 3, figsize=(13.5, 7.6), dpi=220)
    for ax, (feature, title) in zip(axes.ravel(), PLOT_FEATURES):
        grid, pdp, ice = compute_pdp_ice(model, x, feature, seed=args.seed)
        for row in ice:
            ax.plot(grid, row, color="#9bb7d4", alpha=0.22, linewidth=0.55)
        ax.plot(grid, pdp, color="#12395b", linewidth=2.4)
        ax.set_title(title, loc="left", fontsize=10)
        ax.set_xlabel(feature)
        ax.set_ylabel("Predicted LST (deg C)")
        ax.grid(True, linewidth=0.35, alpha=0.35)

    fig.suptitle("Figure 4. PDP and ICE plots of key LST-driving factors", fontsize=13, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(output_path, bbox_inches="tight")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()

"""PDP/ICE computation for LST drivers."""

from __future__ import annotations

import numpy as np
import pandas as pd


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

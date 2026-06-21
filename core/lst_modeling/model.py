"""Model factory and metrics for LST prediction."""

from __future__ import annotations

import numpy as np


def build_lst_model(seed: int = 2026):
    """Build the primary CatBoost model, with a scikit-learn fallback."""
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


def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)))


def mae(y_true, y_pred) -> float:
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def r2(y_true, y_pred) -> float:
    y_true = np.asarray(y_true)
    ss_res = np.sum((y_true - np.asarray(y_pred)) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1 - ss_res / ss_tot)

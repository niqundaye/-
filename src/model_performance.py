"""Reproduce model-comparison metrics for LST estimation."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from analysis_config import FEATURES, OUTPUTS, spatial_units_path
from figure4_pdp_ice import build_model


def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)))


def mae(y_true, y_pred) -> float:
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def r2(y_true, y_pred) -> float:
    y_true = np.asarray(y_true)
    ss_res = np.sum((y_true - np.asarray(y_pred)) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1 - ss_res / ss_tot)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    input_path = root / args.input if args.input else spatial_units_path()
    data = pd.read_csv(input_path)
    x = data[FEATURES].copy()
    y = data["lst_c"].astype(float)

    try:
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.svm import SVR

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=args.seed)
        models = {
            "Random Forest": RandomForestRegressor(n_estimators=400, random_state=args.seed, n_jobs=-1),
            "Gradient Boosting": GradientBoostingRegressor(random_state=args.seed),
            "Support Vector Regression": SVR(C=20, gamma="scale"),
            "CatBoost_or_fallback": build_model(args.seed),
        }
    except Exception as exc:
        raise RuntimeError("Install scikit-learn to reproduce model comparison metrics.") from exc

    rows = []
    for name, model in models.items():
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        rows.append({"model": name, "r2": r2(y_test, pred), "rmse_c": rmse(y_test, pred), "mae_c": mae(y_test, pred)})

    out = root / args.output if args.output else OUTPUTS / "model_performance.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

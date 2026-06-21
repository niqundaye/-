"""Generate feature-importance table for the LST model."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from analysis_config import FEATURES, TABLES, spatial_units_path
from figure4_pdp_ice import build_model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    input_path = root / args.input if args.input else spatial_units_path()
    df = pd.read_csv(input_path)
    x = df[FEATURES].copy()
    y = df["lst_c"].astype(float)
    model = build_model(args.seed)
    model.fit(x, y)

    if hasattr(model, "get_feature_importance"):
        values = np.asarray(model.get_feature_importance(), dtype=float)
    elif hasattr(model, "feature_importances_"):
        values = np.asarray(model.feature_importances_, dtype=float)
    else:
        values = np.repeat(1 / len(FEATURES), len(FEATURES))

    values = values / values.sum()
    out_df = pd.DataFrame({"variable": FEATURES, "relative_importance": values}).sort_values(
        "relative_importance", ascending=False
    )
    out = root / args.output if args.output else TABLES / "feature_importance.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(out, index=False)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

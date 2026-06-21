"""Transparent QLA-COA-style allocation utilities.

This module provides the executable allocation logic used in the repository.
It is intentionally compact so reviewers can inspect how spatial units are
assigned and how the three manuscript objectives are evaluated.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


STRATEGIES = {
    0: "baseline",
    1: "cooling_priority",
    2: "ventilation_priority",
    3: "economic_priority",
    4: "balanced_development",
}


def ensure_optional_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "economic_benefit" not in df:
        df["economic_benefit"] = (
            0.36 * df["night_light"]
            + 0.24 * df["construction_land_prop"]
            + 0.27 * df["industrial_land_prop"]
            + 0.13 * df["road_accessibility"]
        )
    if "cooling_potential" not in df:
        lst_scaled = (df["lst_c"] - df["lst_c"].min()) / (df["lst_c"].max() - df["lst_c"].min())
        df["cooling_potential"] = 0.46 * lst_scaled + 0.32 * (1 - df["ndvi"]) + 0.22 * df["bare_land_prop"]
    if "ventilation_potential" not in df:
        df["ventilation_potential"] = 0.72 * df["svf"] + 0.28 * (1 - df["land_use_intensity"])
    return df


def assign_strategy(df: pd.DataFrame, scenario: str) -> pd.Series:
    restricted = df["ecological_restricted"].astype(bool)
    cooling_score = df["cooling_potential"].rank(pct=True)
    ventilation_score = df["ventilation_potential"].rank(pct=True)
    economic_score = df["economic_benefit"].rank(pct=True)
    balanced_score = 0.40 * cooling_score + 0.30 * ventilation_score + 0.30 * economic_score
    strategy = pd.Series(0, index=df.index, dtype=int)
    strategy[restricted] = 0

    if scenario == "cooling_priority":
        strategy[(~restricted) & (cooling_score >= 0.66)] = 1
    elif scenario == "ventilation_priority":
        strategy[(~restricted) & (ventilation_score >= 0.66)] = 2
    elif scenario == "economic_priority":
        strategy[(~restricted) & (economic_score >= 0.66)] = 3
    elif scenario == "balanced_development":
        strategy[(~restricted) & (balanced_score >= 0.55)] = 4
        strategy[(~restricted) & (cooling_score >= 0.85)] = 1
        strategy[(~restricted) & (ventilation_score >= 0.90)] = 2
    elif scenario != "baseline":
        raise ValueError(f"Unknown scenario: {scenario}")

    return strategy


def evaluate(df: pd.DataFrame, strategy: pd.Series) -> dict[str, float]:
    area = df["area_km2"].to_numpy()
    lst = df["lst_c"].to_numpy().copy()
    svf = df["ventilation_potential"].to_numpy().copy()
    econ = df["economic_benefit"].to_numpy().copy()
    s = strategy.to_numpy()

    lst[s == 1] -= 1.9 * df.loc[s == 1, "cooling_potential"].to_numpy()
    lst[s == 2] -= 0.8 * df.loc[s == 2, "ventilation_potential"].to_numpy()
    lst[s == 3] += 0.9 * df.loc[s == 3, "land_use_intensity"].to_numpy()
    lst[s == 4] -= 1.2 * (0.55 * df.loc[s == 4, "cooling_potential"] + 0.45 * df.loc[s == 4, "ventilation_potential"]).to_numpy()

    svf[s == 2] += 0.10
    svf[s == 4] += 0.06
    svf[s == 3] -= 0.04
    econ[s == 3] += 0.18
    econ[s == 4] += 0.10
    econ[s == 1] -= 0.04
    econ[s == 2] -= 0.02

    return {
        "mean_lst_c": float(np.average(lst, weights=area)),
        "svf_potential": float(np.average(np.clip(svf, 0, 1), weights=area)),
        "economic_benefit": float(np.average(np.clip(econ, 0, 1), weights=area)),
    }

"""Planning-oriented spatial potential classification."""

from __future__ import annotations

import pandas as pd


def classify_units(df: pd.DataFrame) -> pd.Series:
    restricted = df["ecological_restricted"].astype(bool)
    cooling = df["cooling_potential"].rank(pct=True)
    ventilation = df["ventilation_potential"].rank(pct=True)
    economic = df["economic_benefit"].rank(pct=True)

    labels = pd.Series("Balanced-development units", index=df.index)
    labels[restricted] = "Ecological-restricted units"
    labels[(~restricted) & (cooling >= 0.72)] = "Cooling-priority units"
    labels[(~restricted) & (ventilation >= 0.74) & (cooling < 0.72)] = "Ventilation-priority units"
    labels[(~restricted) & (economic >= 0.76) & (cooling < 0.72)] = "Economic-priority units"
    return labels

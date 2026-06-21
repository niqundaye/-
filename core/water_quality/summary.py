"""Water-quality summary helpers."""

from __future__ import annotations

import pandas as pd


def numeric_value(value):
    if pd.isna(value):
        return None
    text = str(value).strip()
    for marker in ("<=", "<", "ND", "not detected"):
        text = text.replace(marker, "")
    try:
        return float(text)
    except ValueError:
        return None


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["value_numeric"] = df["value_raw"].map(numeric_value)
    return (
        df.dropna(subset=["value_numeric"])
        .groupby(["sampling_month", "river_or_group", "indicator", "unit"], dropna=False)
        .agg(n=("value_numeric", "count"), mean=("value_numeric", "mean"), min=("value_numeric", "min"), max=("value_numeric", "max"))
        .reset_index()
    )

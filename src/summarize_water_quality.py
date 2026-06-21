"""Summarize extracted water-quality monitoring data."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from analysis_config import TABLES, WATER_QUALITY


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    input_path = root / args.input if args.input else WATER_QUALITY
    if not input_path.exists():
        print(f"Skipping water-quality summary; missing {input_path}")
        return

    df = pd.read_csv(input_path, encoding="utf-8-sig")
    df["value_numeric"] = df["value_raw"].map(numeric_value)
    summary = (
        df.dropna(subset=["value_numeric"])
        .groupby(["sampling_month", "river_or_group", "indicator", "unit"], dropna=False)
        .agg(
            n=("value_numeric", "count"),
            mean=("value_numeric", "mean"),
            min=("value_numeric", "min"),
            max=("value_numeric", "max"),
        )
        .reset_index()
    )
    out = root / args.output if args.output else TABLES / "water_quality_summary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

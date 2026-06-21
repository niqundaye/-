"""Classify spatial optimization-potential types."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from analysis_config import OUTPUTS, TABLES, spatial_units_path
from optimize_allocation import ensure_optional_columns


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=None)
    parser.add_argument("--classified-output", default=None)
    parser.add_argument("--summary-output", default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    input_path = root / args.input if args.input else spatial_units_path()
    df = ensure_optional_columns(pd.read_csv(input_path))
    restricted = df["ecological_restricted"].astype(bool)
    cooling = df["cooling_potential"].rank(pct=True)
    ventilation = df["ventilation_potential"].rank(pct=True)
    economic = df["economic_benefit"].rank(pct=True)

    labels = pd.Series("Balanced-development units", index=df.index)
    labels[restricted] = "Ecological-restricted units"
    labels[(~restricted) & (cooling >= 0.72)] = "Cooling-priority units"
    labels[(~restricted) & (ventilation >= 0.74) & (cooling < 0.72)] = "Ventilation-priority units"
    labels[(~restricted) & (economic >= 0.76) & (cooling < 0.72)] = "Economic-priority units"

    df["potential_type"] = labels
    area_total = df["area_km2"].sum()
    summary = (
        df.groupby("potential_type", as_index=False)
        .agg(number_of_units=("unit_id", "count"), area_km2=("area_km2", "sum"))
        .sort_values("potential_type")
    )
    summary["area_proportion_percent"] = 100 * summary["area_km2"] / area_total

    classified_out = root / args.classified_output if args.classified_output else OUTPUTS / "spatial_units_classified.csv"
    summary_out = root / args.summary_output if args.summary_output else TABLES / "spatial_potential_summary.csv"
    classified_out.parent.mkdir(parents=True, exist_ok=True)
    summary_out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(classified_out, index=False)
    summary.to_csv(summary_out, index=False)
    print(f"Wrote {classified_out}")
    print(f"Wrote {summary_out}")


if __name__ == "__main__":
    main()

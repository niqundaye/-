"""Reproduce manuscript tables from data and scripts where applicable."""

from __future__ import annotations

import csv

from analysis_config import OUTPUTS


TABLE_MAP = [
    ("Table 1", "Main datasets and analytical roles", "docs/data_sources.md"),
    ("Table 2", "Candidate allocation strategies", "core/optimization/qla_coa.py"),
    ("Table 3", "Model predictive performance", "outputs/model_performance.csv"),
    ("Table 4", "Feature importance ranking", "outputs/tables/feature_importance.csv"),
    ("Table 5", "Spatial optimization-potential summary", "outputs/tables/spatial_potential_summary.csv"),
    ("Table 6", "Mechanism-to-strategy translation", "src/figure7_mechanism_strategy.py"),
    ("Table 7", "Objective trade-off relationships", "outputs/tables/tradeoff_correlations.csv"),
    ("Table 8", "Representative scheme performance", "outputs/allocation_scenarios.csv"),
    ("Table S1", "Remote sensing datasets and preprocessing", "docs/data_sources.md"),
    ("Table S2", "Economic-benefit calibration inputs", "data/raw/data_dictionary.csv"),
]


def main() -> None:
    out = OUTPUTS / "tables" / "table_reproduction_manifest.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["table", "description", "source_or_script"])
        writer.writerows(TABLE_MAP)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

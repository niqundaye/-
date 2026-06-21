"""Analyze objective trade-offs across allocation scenarios."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from analysis_config import TABLES


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="outputs/allocation_scenarios.csv")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    path = root / args.input
    if not path.exists():
        from optimize_allocation import main as run_optimization

        run_optimization()

    df = pd.read_csv(path)
    pairs = [
        ("mean_lst_c", "svf_potential"),
        ("mean_lst_c", "economic_benefit"),
        ("svf_potential", "economic_benefit"),
    ]
    rows = []
    for a, b in pairs:
        rows.append({"objective_pair": f"{a} vs {b}", "pearson_r": df[a].corr(df[b], method="pearson")})

    out = root / args.output if args.output else TABLES / "tradeoff_correlations.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

"""Main command-line entry point for full manuscript reproduction."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

MODES = {
    "all": ["src/make_all_figures_and_tables.py"],
    "figures": [
        "src/figure1_study_area.py",
        "src/figure2_framework.py",
        "src/figure3_shap_importance.py",
        "src/figure4_pdp_ice.py",
        "src/figure5_spatial_potential_layers.py",
        "src/figure6_potential_classes.py",
        "src/figure7_mechanism_strategy.py",
        "src/figure8_pareto_tradeoff.py",
        "src/figure9_allocation_schemes.py",
        "src/figure10_scheme_performance.py",
    ],
    "tables": ["src/reproduce_tables.py"],
    "lst": ["src/model_performance.py", "src/feature_importance.py", "src/figure3_shap_importance.py", "src/figure4_pdp_ice.py"],
    "potential": ["src/classify_spatial_potential.py", "src/figure5_spatial_potential_layers.py", "src/figure6_potential_classes.py"],
    "optimization": ["src/optimize_allocation.py", "src/tradeoff_analysis.py", "src/figure8_pareto_tradeoff.py", "src/figure9_allocation_schemes.py", "src/figure10_scheme_performance.py"],
    "water-quality": ["src/summarize_water_quality.py"],
}


def run_script(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run manuscript reproduction tasks.")
    parser.add_argument("--mode", choices=sorted(MODES), default="all")
    parser.add_argument("--config", default="configs/default.yaml", help="Documented experiment config path.")
    args = parser.parse_args()

    print(f"Using config: {args.config}")
    for script in MODES[args.mode]:
        run_script(script)


if __name__ == "__main__":
    main()

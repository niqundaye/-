"""Main command-line entry point for full manuscript reproduction."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

MODES = {
    "all": ["src/make_all_figures_and_tables.py"],
    "lst": ["src/model_performance.py", "src/feature_importance.py", "src/figure4_pdp_ice.py"],
    "potential": ["src/classify_spatial_potential.py"],
    "optimization": ["src/optimize_allocation.py", "src/tradeoff_analysis.py"],
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

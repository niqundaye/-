"""Generate the manuscript output manifest.

This wrapper calls the available reproduction scripts and writes a manifest
showing which manuscript outputs were regenerated.
"""

from __future__ import annotations

import csv
import subprocess
import sys

from analysis_config import OUTPUTS, ROOT


TASKS = [
    ("Figure 3/4 model interpretation inputs", "model_performance.py", "outputs/model_performance.csv"),
    ("Table 4 feature importance", "feature_importance.py", "outputs/tables/feature_importance.csv"),
    ("Figure 4 PDP and ICE plots", "figure4_pdp_ice.py", "outputs/figures/figure4_pdp_ice.png"),
    ("Figure 5 spatial optimization potential", "classify_spatial_potential.py", "outputs/tables/spatial_potential_summary.csv"),
    ("Figures 8-10 / Table 8 allocation metrics", "optimize_allocation.py", "outputs/allocation_scenarios.csv"),
    ("Table 7 objective trade-off relationships", "tradeoff_analysis.py", "outputs/tables/tradeoff_correlations.csv"),
    ("Supplementary water-quality monitoring summary", "summarize_water_quality.py", "outputs/tables/water_quality_summary.csv"),
]


def main() -> None:
    manifest = []
    for label, script, output in TASKS:
        subprocess.run([sys.executable, str(ROOT / "src" / script)], cwd=ROOT, check=True)
        manifest.append({"manuscript_item": label, "script": f"src/{script}", "output": output})

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    out = OUTPUTS / "reproduction_manifest.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["manuscript_item", "script", "output"])
        writer.writeheader()
        writer.writerows(manifest)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

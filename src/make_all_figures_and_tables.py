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
    ("Figure 1 study area and spatial characteristics", "figure1_study_area.py", "outputs/figures/figure1_study_area_characteristics.png"),
    ("Figure 2 research framework", "figure2_framework.py", "outputs/figures/figure2_research_framework.png"),
    ("Figure 3 feature importance and SHAP-style diagnostics", "figure3_shap_importance.py", "outputs/figures/figure3_feature_importance.png"),
    ("Figure 3/4 model interpretation inputs", "model_performance.py", "outputs/model_performance.csv"),
    ("Table 4 feature importance", "feature_importance.py", "outputs/tables/feature_importance.csv"),
    ("Figure 4 PDP and ICE plots", "figure4_pdp_ice.py", "outputs/figures/figure4_pdp_ice.png"),
    ("Figure 5 spatial optimization-potential layers", "figure5_spatial_potential_layers.py", "outputs/figures/figure5_spatial_potential_layers.png"),
    ("Figure 6 spatial potential classes", "figure6_potential_classes.py", "outputs/figures/figure6_potential_classes.png"),
    ("Figure 7 mechanism-to-strategy matrix", "figure7_mechanism_strategy.py", "outputs/figures/figure7_mechanism_strategy_matrix.png"),
    ("Spatial optimization-potential table", "classify_spatial_potential.py", "outputs/tables/spatial_potential_summary.csv"),
    ("Figures 8-10 / Table 8 allocation metrics", "optimize_allocation.py", "outputs/allocation_scenarios.csv"),
    ("Figure 8 Pareto-style trade-off analysis", "figure8_pareto_tradeoff.py", "outputs/figures/figure8_pareto_tradeoff.png"),
    ("Figure 9 representative allocation schemes", "figure9_allocation_schemes.py", "outputs/figures/figure9_allocation_schemes.png"),
    ("Figure 10 scheme performance comparison", "figure10_scheme_performance.py", "outputs/figures/figure10_scheme_performance.png"),
    ("Table 7 objective trade-off relationships", "tradeoff_analysis.py", "outputs/tables/tradeoff_correlations.csv"),
    ("Supplementary water-quality monitoring summary", "summarize_water_quality.py", "outputs/tables/water_quality_summary.csv"),
    ("All manuscript tables manifest", "reproduce_tables.py", "outputs/tables/table_reproduction_manifest.csv"),
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

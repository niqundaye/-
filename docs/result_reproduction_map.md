# Manuscript Result Reproduction Map

| Manuscript result | Reproduction script | Required input | Output |
|---|---|---|---|
| Model-performance comparison | `src/model_performance.py` | Spatial-unit table | `outputs/model_performance.csv` |
| SHAP/feature importance ranking | `src/feature_importance.py` | Spatial-unit table | `outputs/tables/feature_importance.csv` |
| Figure 4 PDP/ICE plots | `src/figure4_pdp_ice.py` | Spatial-unit table | `outputs/figures/figure4_pdp_ice.png` |
| Spatial optimization-potential classification | `src/classify_spatial_potential.py` | Spatial-unit table | `outputs/spatial_units_classified.csv`; `outputs/tables/spatial_potential_summary.csv` |
| Multi-objective allocation scenarios | `src/optimize_allocation.py` | Spatial-unit table | `outputs/allocation_scenarios.csv` |
| Objective trade-off relationships | `src/tradeoff_analysis.py` | Allocation scenario output | `outputs/tables/tradeoff_correlations.csv` |
| Water-quality monitoring summary | `src/summarize_water_quality.py` | Water-quality monitoring CSV | `outputs/tables/water_quality_summary.csv` |

## Important Data Note

The included water-quality monitoring table is extracted from the supplied original monitoring appendix and can be treated as real supplementary monitoring data.

The included `data/example/spatial_units_demo.csv` is not the manuscript spatial-unit dataset. It is present only so reviewers can verify the code interface before the releasable spatial-unit dataset is placed at:

```text
data/raw/spatial_units_xi_ujimqin_2023.csv
```

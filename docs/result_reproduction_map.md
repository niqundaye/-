# Manuscript Result Reproduction Map

| Manuscript result | Reproduction script | Required input | Output |
|---|---|---|---|
| Figure 1 study area and spatial characteristics | `src/figure1_study_area.py` | Spatial-unit table | `outputs/figures/figure1_study_area_characteristics.png` |
| Figure 2 research framework | `src/figure2_framework.py` | None | `outputs/figures/figure2_research_framework.png` |
| Figure 3 SHAP/importance diagnostics | `src/figure3_shap_importance.py` | Spatial-unit table | `outputs/figures/figure3_feature_importance.png` |
| Model-performance comparison | `src/model_performance.py` | Spatial-unit table | `outputs/model_performance.csv` |
| SHAP/feature importance ranking | `src/feature_importance.py` | Spatial-unit table | `outputs/tables/feature_importance.csv` |
| Figure 4 PDP/ICE plots | `src/figure4_pdp_ice.py` | Spatial-unit table | `outputs/figures/figure4_pdp_ice.png` |
| Figure 5 spatial optimization-potential layers | `src/figure5_spatial_potential_layers.py` | Spatial-unit table | `outputs/figures/figure5_spatial_potential_layers.png` |
| Figure 6 spatial potential classes | `src/figure6_potential_classes.py` | Spatial-unit table | `outputs/figures/figure6_potential_classes.png` |
| Figure 7 mechanism-to-strategy matrix | `src/figure7_mechanism_strategy.py` | Mechanism definitions | `outputs/figures/figure7_mechanism_strategy_matrix.png` |
| Spatial optimization-potential classification | `src/classify_spatial_potential.py` | Spatial-unit table | `outputs/spatial_units_classified.csv`; `outputs/tables/spatial_potential_summary.csv` |
| Multi-objective allocation scenarios | `src/optimize_allocation.py` | Spatial-unit table | `outputs/allocation_scenarios.csv` |
| Figure 8 Pareto/trade-off analysis | `src/figure8_pareto_tradeoff.py` | Allocation scenarios | `outputs/figures/figure8_pareto_tradeoff.png` |
| Figure 9 representative allocation schemes | `src/figure9_allocation_schemes.py` | Spatial-unit table | `outputs/figures/figure9_allocation_schemes.png` |
| Figure 10 scheme performance comparison | `src/figure10_scheme_performance.py` | Allocation scenarios | `outputs/figures/figure10_scheme_performance.png` |
| Objective trade-off relationships | `src/tradeoff_analysis.py` | Allocation scenario output | `outputs/tables/tradeoff_correlations.csv` |
| Water-quality monitoring summary | `src/summarize_water_quality.py` | Water-quality monitoring CSV | `outputs/tables/water_quality_summary.csv` |
| All manuscript tables | `src/reproduce_tables.py` | Relevant outputs/docs | `outputs/tables/table_reproduction_manifest.csv` |

## Important Data Note

The included water-quality monitoring table is extracted from the supplied original monitoring appendix and can be treated as real supplementary monitoring data.

The included `data/example/spatial_units_demo.csv` is not the manuscript spatial-unit dataset. It is present only so reviewers can verify the code interface before the releasable spatial-unit dataset is placed at:

```text
data/raw/spatial_units_xi_ujimqin_2023.csv
```

# Reproducibility Package: Heat-Resilient Spatial Allocation in Xi Ujimqin Banner

This repository provides the code, data structure, public-data acquisition workflow, and supplementary monitoring data for reproducing the manuscript experiments on remote-sensing-informed heat-resilient spatial allocation in Xi Ujimqin Banner.

The repository was prepared to address the reviewer request:

> Regarding Figure 4, is this based on real data? I strongly suggest the authors provide their source code and raw datasets for verification.

## Main Answer

Figure 4 is generated from the fitted LST prediction model using spatial-unit observations, not from manually drawn or conceptual curves. The curves are partial dependence plots (PDP) and individual conditional expectation (ICE) plots for key LST-driving variables.

## Repository Contents

```text
data/
  raw/
    water_quality_monitoring_long.csv      # Real monitoring appendix data extracted from DOCX
    water_quality_README.md
    data_dictionary.csv                    # Spatial-unit table dictionary
  example/
    spatial_units_demo.csv                 # Demo table for code smoke tests only
data_acquisition/
  gee_export_spatial_layers.js             # Google Earth Engine export script
  README.md                                # Public data acquisition workflow
docs/
  data_sources.md                          # Data-source and preprocessing notes
  reproducibility_standard.md              # Journal-facing data/code standard
  reviewer_response.md                     # Suggested response to reviewer
src/
  extract_water_quality_docx.py            # Converts water-quality DOCX tables to CSV
  figure4_pdp_ice.py                       # Reproduces Figure 4
  feature_importance.py                    # Reproduces feature-importance table
  model_performance.py                     # Reproduces model-comparison metrics
  classify_spatial_potential.py            # Reproduces spatial potential classification
  optimize_allocation.py                   # Reproduces allocation scenario metrics
  tradeoff_analysis.py                     # Reproduces objective trade-off table
  summarize_water_quality.py               # Summarizes monitoring data
  make_all_figures_and_tables.py           # Runs the reproducible manuscript outputs
  run_all.py                               # Main entry point
```

## Data Required for Full Manuscript Reproduction

The full spatial modeling workflow expects:

```text
data/raw/spatial_units_xi_ujimqin_2023.csv
```

This file should contain one row per spatial analysis unit and the variables listed in `data/raw/data_dictionary.csv`, including LST, NDVI, bare-land proportion, land-use intensity, SVF, nighttime light, elevation, road accessibility, land-use proportions, ecological restriction, economic benefit, cooling potential, and ventilation potential.

The repository includes `data/example/spatial_units_demo.csv` only to verify that the code runs. It is not the manuscript dataset and must not be cited as raw evidence.

## Public Online Data Sources

The public-data workflow can reconstruct most spatial variables from:

- Landsat 8/9 Collection 2 Level-2 Surface Temperature and Surface Reflectance
- ESA WorldCover 2021 v200
- NASA SRTMGL1 30 m DEM
- VIIRS DNB annual nighttime-light composites
- OpenStreetMap road data or another documented road layer
- Uploaded study boundary and spatial-unit polygons

See `data_acquisition/gee_export_spatial_layers.js` and `docs/data_sources.md`.

## Real Monitoring Data Included

The file `data/raw/water_quality_monitoring_long.csv` is extracted from the supplied monitoring appendix DOCX. It contains 7560 water-quality records across 33 appendix tables, 149 monitoring stations, 3 sampling months, and 24 indicators. These data support environmental-background and ecological/water-system documentation, but they do not replace the remote-sensing spatial-unit table needed for Figure 4.

## Installation

```bash
pip install -r requirements.txt
```

Google Earth Engine exports require an authenticated Earth Engine account and uploaded boundary/spatial-unit assets.

## Run All Reproducible Outputs

After placing the real spatial-unit table at `data/raw/spatial_units_xi_ujimqin_2023.csv`, run:

```bash
python src/run_all.py
```

Outputs are written to:

```text
outputs/
  figures/
  tables/
  reproduction_manifest.csv
```

## Reproduce Figure 4 Only

```bash
python src/figure4_pdp_ice.py \
  --input data/raw/spatial_units_xi_ujimqin_2023.csv \
  --output outputs/figures/figure4_pdp_ice.png
```

## Recommended Manuscript Statement

> The source code, data dictionary, public remote-sensing acquisition workflow, released spatial-unit dataset, and supplementary monitoring data used for reproducibility are available at the GitHub repository. Figure 4 was generated from the fitted LST prediction model using `src/figure4_pdp_ice.py`.

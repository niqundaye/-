# Remote-Sensing-Informed Heat-Resilient Spatial Allocation for Xi Ujimqin Banner

> Complete reproducibility package for the manuscript on LST-driving mechanisms, spatial optimization-potential assessment, and multi-objective heat-resilient allocation in a semi-arid grassland county region.

---

## Overview

This repository implements the full manuscript workflow:

- **Remote-sensing data construction**
  - Landsat 8/9 LST and NDVI
  - ESA WorldCover land-use proportions
  - SRTM/Copernicus DEM terrain variables
  - VIIRS nighttime-light socioeconomic proxy
  - SVF/openness, road accessibility, ecological restriction, and economic-benefit layers

- **LST mechanism identification**
  - CatBoost-based LST prediction
  - Model-performance comparison
  - Feature-importance ranking
  - PDP/ICE reproduction for Figure 4

- **Planning-oriented spatial potential assessment**
  - Cooling-priority units
  - Ventilation-priority units
  - Economic-priority units
  - Balanced-development units
  - Ecological-restricted units

- **Multi-objective spatial allocation**
  - Baseline, cooling-priority, ventilation-priority, economic-priority, and balanced-development schemes
  - Objective trade-off analysis among LST, SVF-based ventilation potential, and economic benefit

- **Supplementary environmental monitoring**
  - Water-quality monitoring appendix extraction and summary
  - 7560 real monitoring records extracted from the supplied appendix DOCX

---

## Project Structure

```text
heat-resilient-xi-ujimqin/
|-- core/
|   |-- remote_sensing/          # Public remote-sensing dataset registry
|   |-- lst_modeling/            # LST model and PDP/ICE interpretation utilities
|   |-- spatial_potential/       # Planning-oriented potential classification
|   |-- optimization/            # QLA-COA-style allocation utilities
|   `-- water_quality/           # Monitoring-data summary helpers
|-- data/
|   |-- raw/                     # Real/released source tables
|   `-- example/                 # Smoke-test demo table only
|-- data_acquisition/
|   |-- gee_export_spatial_layers.js
|   `-- README.md
|-- configs/
|   |-- default.yaml
|   `-- experiments/
|       `-- full_reproduction.yaml
|-- docs/
|   |-- data_availability_statement.md
|   |-- data_sources.md
|   |-- reproducibility_standard.md
|   |-- result_reproduction_map.md
|   `-- reviewer_response.md
|-- experiments/
|   |-- run_full_reproduction.py
|   |-- run_lst_modeling.py
|   |-- run_spatial_potential.py
|   |-- run_optimization.py
|   `-- run_water_quality.py
|-- src/                         # Script-level reproducibility entry points
|-- outputs/                     # Generated tables and figures
|-- results/                     # Paper-style result folder
|-- run.py                       # Main CLI
`-- requirements.txt
```

---

## Environment Setup

```bash
conda create -n xuji_repro python=3.10 -y
conda activate xuji_repro
pip install -r requirements.txt
```

Google Earth Engine exports require an authenticated Earth Engine account and uploaded study-boundary/spatial-unit assets.

---

## Data Preparation

### 1. Rebuild public remote-sensing predictors

Use:

```text
data_acquisition/gee_export_spatial_layers.js
```

The script exports Landsat LST/NDVI, WorldCover classes, DEM/slope, and VIIRS nighttime-light summaries to spatial units.

### 2. Place the real spatial-unit table

Full manuscript reproduction requires:

```text
data/raw/spatial_units_xi_ujimqin_2023.csv
```

Required columns are listed in:

```text
data/raw/data_dictionary.csv
```

### 3. Water-quality monitoring data

The supplied monitoring appendix DOCX has been converted locally into:

```text
data/raw/water_quality_monitoring_long.csv
```

This file supports ecological/water-environment documentation, but it does not replace the spatial-unit table required for the LST model and Figure 4.

---

## Usage

### Full manuscript reproduction

```bash
python run.py --mode all --config configs/experiments/full_reproduction.yaml
```

Equivalent:

```bash
python experiments/run_full_reproduction.py
```

### LST modeling and Figure 4

```bash
python run.py --mode lst
```

Outputs:

```text
outputs/model_performance.csv
outputs/tables/feature_importance.csv
outputs/figures/figure4_pdp_ice.png
```

### Spatial potential classification

```bash
python run.py --mode potential
```

Outputs:

```text
outputs/spatial_units_classified.csv
outputs/tables/spatial_potential_summary.csv
```

### Allocation and trade-off experiments

```bash
python run.py --mode optimization
```

Outputs:

```text
outputs/allocation_scenarios.csv
outputs/tables/tradeoff_correlations.csv
```

### Water-quality monitoring summary

```bash
python run.py --mode water-quality
```

Output:

```text
outputs/tables/water_quality_summary.csv
```

---

## Manuscript Result Map

| Manuscript component | Script |
|---|---|
| Dataset construction | `data_acquisition/gee_export_spatial_layers.js` |
| Model comparison | `src/model_performance.py` |
| Feature importance | `src/feature_importance.py` |
| Figure 4 PDP/ICE | `src/figure4_pdp_ice.py` |
| Spatial potential classes | `src/classify_spatial_potential.py` |
| Allocation scenarios | `src/optimize_allocation.py` |
| Objective trade-offs | `src/tradeoff_analysis.py` |
| Monitoring-data appendix | `src/extract_water_quality_docx.py`, `src/summarize_water_quality.py` |

---

## Reviewer Note

Figure 4 is based on fitted model responses from spatial-unit observations. It is not a manually drawn conceptual figure. Reproduce it with:

```bash
python src/figure4_pdp_ice.py \
  --input data/raw/spatial_units_xi_ujimqin_2023.csv \
  --output outputs/figures/figure4_pdp_ice.png
```

The included example table is only for smoke testing. The final manuscript archive should include the real spatial-unit table at `data/raw/spatial_units_xi_ujimqin_2023.csv`.

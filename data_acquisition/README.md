# Public Data Acquisition

This folder contains scripts and notes for rebuilding the spatial-unit table from online public datasets.

## Recommended Workflow

1. Prepare `data/raw/boundary/xi_ujimqin_boundary.geojson`.
2. Prepare or generate `data/raw/spatial_units/spatial_units.geojson`.
3. Run the Google Earth Engine script:

   ```text
   data_acquisition/gee_export_spatial_layers.js
   ```

4. Export the table as `data/raw/spatial_units_xi_ujimqin_2023.csv`.
5. Run:

   ```bash
   python src/run_all.py
   ```

## Public Data Coverage

| Variable group | Public source | Repository handling |
|---|---|---|
| LST | Landsat 8/9 Collection 2 Level-2 Surface Temperature | GEE export |
| NDVI | Landsat 8/9 Collection 2 Level-2 Surface Reflectance | GEE export |
| Bare/sparse vegetation, built-up, grassland, water/wetland | ESA WorldCover 2021 v200 | GEE export and zonal proportions |
| Elevation and slope | NASA SRTMGL1 30 m DEM | GEE export |
| Nighttime light | VIIRS DNB annual composites | GEE export |
| Roads/accessibility | OpenStreetMap or local road layer | external preprocessing, then zonal join |
| Economic benefit | VIIRS + construction/industrial land + road accessibility; township statistics if releasable | proxy calibration script / user-supplied table |
| SVF/openness | DEM/DSM-derived openness or topographic openness proxy | local preprocessing; code documents equations |

## Restricted or Local Data

If township GDP, industrial-zone boundaries, detailed planning layers, or high-resolution DSM/building layers cannot be redistributed, place them outside the repository and release the processed spatial-unit table, source metadata, checksum, aggregation/calibration code, and access-restriction explanation.

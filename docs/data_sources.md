# Data Sources and Preprocessing Notes

This file documents the datasets used to construct the spatial-unit table for Xi Ujimqin Banner.

| Data category | Product / collection | Period | Resolution / scale | Main variables | Preprocessing | Analytical role |
|---|---|---:|---:|---|---|---|
| Thermal remote sensing | Landsat 8/9 Collection 2 Level-2 Surface Temperature | June-September 2023 | 30 m | ST_B10 / LST | QA masking for cloud, cloud shadow, snow, fill, invalid pixels, and water-dominated pixels; Celsius conversion; aggregation to spatial units | LST target and thermal objective |
| Multispectral remote sensing | Landsat 8/9 Collection 2 Level-2 Surface Reflectance | Same scenes as LST | 30 m | Red, NIR, NDVI | Surface reflectance scaling; consistent QA masking; NDVI calculation; aggregation to spatial units | Vegetation and exposure variables |
| DEM | NASA SRTMGL1 30 m DEM or Copernicus DEM GLO-30 | Static | 30 m | Elevation, slope | Projection unification, void checking, slope calculation, aggregation | Terrain predictors |
| Morphology / openness | DEM/DSM-derived openness layer | Static | 30 m or best available | SVF | SVF estimation, resampling, aggregation | SVF and ventilation proxy |
| Land-use / land-cover | ESA WorldCover 2021 v200 and local land-use/planning datasets | 2021 and latest available local year | 10 m and local planning scale | Grassland, built-up land, bare/sparse vegetation, forest, water/wetland, industrial land | Reclassification, nearest-neighbor resampling, area-proportion calculation | Land-use structure and feasibility |
| Nighttime light | VIIRS DNB annual composite | 2023 or closest available year | Annual global raster | Average nighttime radiance | Abnormal-value removal, resampling, normalization, aggregation | Socioeconomic proxy |
| Socioeconomic data | Township GDP/statistics and local planning datasets | 2023 or closest available year | Township/planning scale | GDP, industrial land, development zones | Proxy-based spatialization and township back-aggregation validation | Economic-benefit layer |

All raster and vector layers should be projected to a unified coordinate system before zonal statistics. Continuous variables should be resampled with bilinear interpolation; categorical land-use data should be resampled with nearest-neighbor assignment.

"""Public remote-sensing dataset registry used by the manuscript."""

DATASETS = {
    "landsat_l2": {
        "name": "Landsat 8/9 Collection 2 Level-2",
        "variables": ["lst_c", "ndvi"],
        "script": "data_acquisition/gee_export_spatial_layers.js",
    },
    "worldcover": {
        "name": "ESA WorldCover 2021 v200",
        "variables": ["grassland_prop", "construction_land_prop", "bare_land_prop", "water_wetland_prop"],
        "script": "data_acquisition/gee_export_spatial_layers.js",
    },
    "srtm": {
        "name": "NASA SRTMGL1 30 m DEM",
        "variables": ["elevation_m", "slope_deg"],
        "script": "data_acquisition/gee_export_spatial_layers.js",
    },
    "viirs": {
        "name": "VIIRS DNB annual nighttime light",
        "variables": ["night_light"],
        "script": "data_acquisition/gee_export_spatial_layers.js",
    },
}

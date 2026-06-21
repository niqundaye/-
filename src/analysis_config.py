"""Shared analysis configuration."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW_UNITS = DATA / "raw" / "spatial_units_xi_ujimqin_2023.csv"
EXAMPLE_UNITS = DATA / "example" / "spatial_units_demo.csv"
WATER_QUALITY = DATA / "raw" / "water_quality_monitoring_long.csv"
OUTPUTS = ROOT / "outputs"
FIGURES = OUTPUTS / "figures"
TABLES = OUTPUTS / "tables"
SEED = 2026

FEATURES = [
    "ndvi",
    "bare_land_prop",
    "land_use_intensity",
    "svf",
    "night_light",
    "elevation_m",
    "road_accessibility",
    "slope_deg",
    "grassland_prop",
    "construction_land_prop",
    "industrial_land_prop",
    "water_wetland_prop",
]


def spatial_units_path(allow_example: bool = True) -> Path:
    """Return the real spatial-unit table, or the demo table for smoke tests."""
    if RAW_UNITS.exists():
        return RAW_UNITS
    if allow_example and EXAMPLE_UNITS.exists():
        print(f"WARNING: using example data at {EXAMPLE_UNITS}. Replace with {RAW_UNITS} for manuscript reproduction.")
        return EXAMPLE_UNITS
    raise FileNotFoundError(f"Missing required spatial-unit table: {RAW_UNITS}")

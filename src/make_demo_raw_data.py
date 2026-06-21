"""Create a deterministic demo spatial-unit table.

This script is only for testing the reproducibility workflow. Replace the
generated CSV with the released real spatial-unit table before archiving the
manuscript repository.
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "example" / "spatial_units_demo.csv"
N_UNITS = 1531
RNG = random.Random(20260621)


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "unit_id", "township_id", "area_km2", "lst_c", "ndvi", "bare_land_prop",
        "land_use_intensity", "svf", "night_light", "elevation_m", "road_accessibility",
        "slope_deg", "grassland_prop", "construction_land_prop", "industrial_land_prop",
        "water_wetland_prop", "ecological_restricted", "economic_benefit",
        "cooling_potential", "ventilation_potential",
    ]

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for i in range(N_UNITS):
            x = i / (N_UNITS - 1)
            township = f"T{1 + i % 12:02d}"
            ecological_gradient = clamp(0.78 - 0.45 * x + RNG.gauss(0, 0.09))
            development_axis = clamp(0.18 + 0.62 * math.exp(-((x - 0.62) ** 2) / 0.018) + RNG.gauss(0, 0.08))
            industry_axis = clamp(0.10 + 0.70 * math.exp(-((x - 0.72) ** 2) / 0.012) + RNG.gauss(0, 0.07))
            road_access = clamp(0.16 + 0.68 * math.exp(-((x - 0.58) ** 2) / 0.04) + RNG.gauss(0, 0.10))
            ndvi = clamp(ecological_gradient - 0.20 * development_axis + RNG.gauss(0, 0.06))
            bare = clamp(0.52 - 0.55 * ndvi + 0.18 * development_axis + RNG.gauss(0, 0.07))
            land_use = clamp(0.12 + 0.58 * development_axis + 0.20 * industry_axis + RNG.gauss(0, 0.06))
            svf = clamp(0.46 + 0.28 * (1 - land_use) + 0.18 * bare + RNG.gauss(0, 0.05))
            night_light = clamp(0.10 + 0.55 * development_axis + 0.35 * industry_axis + RNG.gauss(0, 0.08))
            elevation = 850 + 1110 * (1 - x) + RNG.gauss(0, 55)
            slope = max(0.2, 2.2 + 6.5 * abs(0.5 - x) + RNG.gauss(0, 1.0))
            construction = clamp(0.04 + 0.50 * development_axis + RNG.gauss(0, 0.04))
            industrial = clamp(0.02 + 0.55 * industry_axis + RNG.gauss(0, 0.04))
            water = clamp(0.02 + 0.12 * math.exp(-((x - 0.33) ** 2) / 0.01) + RNG.gauss(0, 0.02))
            grassland = clamp(1.0 - construction - industrial - bare * 0.28 - water + RNG.gauss(0, 0.03))
            ecological_restricted = int(water > 0.08 or (ndvi > 0.60 and development_axis < 0.35))
            lst = 34.58 - 3.2 * (1 - math.exp(-3.6 * ndvi)) + 3.8 * (1 - math.exp(-4.2 * bare)) + 2.4 / (1 + math.exp(-10 * (land_use - 0.48))) - 1.1 * svf + 1.7 * night_light - 0.0014 * (elevation - 1200) + 0.55 * road_access + RNG.gauss(0, 0.85)
            econ = clamp(0.36 * night_light + 0.24 * construction + 0.27 * industrial + 0.13 * road_access)
            cooling = clamp(0.46 * (lst - 28) / 12 + 0.32 * (1 - ndvi) + 0.22 * bare)
            ventilation = clamp(0.72 * svf + 0.28 * (1 - land_use))
            writer.writerow({
                "unit_id": f"XUJB_{i + 1:04d}", "township_id": township,
                "area_km2": f"{RNG.uniform(9.0, 18.5):.4f}", "lst_c": f"{lst:.4f}",
                "ndvi": f"{ndvi:.5f}", "bare_land_prop": f"{bare:.5f}",
                "land_use_intensity": f"{land_use:.5f}", "svf": f"{svf:.5f}",
                "night_light": f"{night_light:.5f}", "elevation_m": f"{elevation:.3f}",
                "road_accessibility": f"{road_access:.5f}", "slope_deg": f"{slope:.4f}",
                "grassland_prop": f"{grassland:.5f}", "construction_land_prop": f"{construction:.5f}",
                "industrial_land_prop": f"{industrial:.5f}", "water_wetland_prop": f"{water:.5f}",
                "ecological_restricted": ecological_restricted, "economic_benefit": f"{econ:.5f}",
                "cooling_potential": f"{cooling:.5f}", "ventilation_potential": f"{ventilation:.5f}",
            })
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

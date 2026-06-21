"""Run water-quality monitoring summary."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(ROOT / "src" / "summarize_water_quality.py")], cwd=ROOT, check=True)

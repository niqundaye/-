"""Run spatial optimization-potential classification."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(ROOT / "src" / "classify_spatial_potential.py")], cwd=ROOT, check=True)

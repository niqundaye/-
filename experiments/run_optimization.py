"""Run allocation scenario and trade-off experiments."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for script in ("optimize_allocation.py", "tradeoff_analysis.py"):
    subprocess.run([sys.executable, str(ROOT / "src" / script)], cwd=ROOT, check=True)

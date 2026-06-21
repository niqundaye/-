"""Run LST model comparison, feature importance, and Figure 4 reproduction."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

for script in ("model_performance.py", "feature_importance.py", "figure4_pdp_ice.py"):
    subprocess.run([sys.executable, str(ROOT / "src" / script)], cwd=ROOT, check=True)

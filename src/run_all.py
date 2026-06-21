"""Run the core reproducibility workflow."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "src" / script)], check=True, cwd=ROOT)


def main() -> None:
    run("make_all_figures_and_tables.py")


if __name__ == "__main__":
    main()

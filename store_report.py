"""
Store and archive pipeline run outputs.
"""

import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = Path(os.environ.get("AERP_OUTPUT_DIR", PROJECT_ROOT / "AERP_Outputs"))
ARCHIVE_DIR = OUTPUT_DIR / "archive"


def archive_pipeline_run(pptx_path=None):
    """
    Archive the generated PowerPoint report to the archive directory.
    """
    if not pptx_path:
        return

    path = Path(pptx_path)
    if not path.exists():
        print(f"  [Archive] Source report not found: {path}")
        return

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    target = ARCHIVE_DIR / path.name

    try:
        shutil.copy2(path, target)
        print(f"  [OK] Report archived to: {target}")
    except Exception as e:
        print(f"  [WARN] Failed to archive report: {e}")


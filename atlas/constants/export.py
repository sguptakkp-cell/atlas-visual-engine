"""
Atlas Visual Engine — export.py

Global export settings and filename helpers.
"""

import os

# ------------------------------------------------------------------
# Legacy Export Settings
# ------------------------------------------------------------------

TRANSPARENT_BACKGROUND = False
PADDING = 0.10
TIGHT_LAYOUT = True

# ------------------------------------------------------------------
# FRS Export Settings
# ------------------------------------------------------------------

DEFAULT_DPI = 200
DEFAULT_FORMAT = "png"
BBOX_INCHES = "tight"
FACECOLOR = "#F8FAFC"
OUTPUT_DIR = "n3l_diagrams"

# ------------------------------------------------------------------
# Backwards-compat alias
# ------------------------------------------------------------------

BBOX = BBOX_INCHES


def build_filename(question_id: str, variant: str, error_code: str = "") -> str:
    """Return a standardized output filename stem (no extension)."""
    parts = [question_id, variant]
    if error_code:
        parts.append(error_code)
    return "_".join(parts)

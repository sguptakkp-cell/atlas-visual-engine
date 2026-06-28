"""
Atlas Spec Checker v2
=====================
Two-level validation:
  Level 1 — tokens.py numerical values match FROZEN_SPEC
  Level 2 — drawing files use ONLY geometry values, never own calculations

Both levels must pass before any diagram can be generated.
"""

import os
import re

FROZEN_SPEC = {
    "ARROW_HEAD_RATIO":         0.22,
    "ARROW_WIDTH_RATIO":        0.10,
    "ARROW_SHAFT_RATIO":        0.28,
    "ARROW_N_RATIO":            3.2,
    "ARROW_MG_RATIO":           2.8,
    "ARROW_F_RATIO":            2.4,
    "ARROW_T_RATIO":            3.0,
    "BLOCK_W_RATIO":            2.2,
    "BLOCK_H_RATIO":            1.4,
    "BLOCK_RX_RATIO":           0.08,
    "BLOCK_LW_RATIO":           0.18,
    "INCLINE_RENDER_ANGLE_DEG": 20.0,
    "CANVAS_H_RATIO":           10.0,
    "CANVAS_W_RATIO":            8.0,
}

# These patterns must NOT appear in drawing files
# They indicate hardcoded values bypassing the spec
BANNED_IN_DRAWING_FILES = {
    "atlas/elements/arrow.py": [
        r"mutation_scale",          # matplotlib arrow - banned
        r"arrowprops",              # matplotlib annotate - banned  
        r"head_width\s*=\s*[0-9]", # hardcoded head width number
        r"head_length\s*=\s*[0-9]",# hardcoded head length number
        r"lw\s*=\s*[0-9]\.[0-9]",  # hardcoded linewidth number
        r"linewidth\s*=\s*[0-9]",  # hardcoded linewidth number
    ],
    "atlas/elements/block.py": [
        r"linewidth\s*=\s*[0-9]\.[0-9](?!.*style)", # hardcoded lw
        r"boxstyle.*rounding_size\s*=\s*[0-9]\.[0-9](?!.*geo)", # hardcoded rx
    ],
    "atlas/api/scene.py": [
        r"length\s*=\s*[0-9]\.[0-9]\s*\*\s*U",  # hardcoded length * U
        r"lw\s*=\s*[0-9]\.[0-9]",               # hardcoded lw
    ],
}

# These strings MUST appear in drawing files (proof they use spec)
REQUIRED_IN_DRAWING_FILES = {
    "atlas/elements/arrow.py": [
        "geo.shaft_lw",     # must use pre-computed shaft width
        "geo.head_tip",     # must use pre-computed head position
        "geo.head_base_1",  # must use pre-computed head base
    ],
    "atlas/elements/block.py": [
        "geo.rx",           # must use pre-computed corner radius
        "style.fill",       # must use style colors
    ],
    "atlas/api/scene.py": [
        "ARROW_STYLE.get_length",  # must use spec for lengths
    ],
}


class AtlasSpecViolation(Exception):
    pass


def _check_tokens():
    """Level 1: Check token values match frozen spec."""
    import atlas.constants.tokens as T
    violations = []
    for name, expected in FROZEN_SPEC.items():
        actual = getattr(T, name, None)
        if actual is None:
            violations.append(f"  MISSING : {name} — add to tokens.py with value {expected}")
        elif abs(float(actual) - float(expected)) > 1e-6:
            violations.append(
                f"  CHANGED : {name} = {actual} (must be {expected})\n"
                f"           Fix: set {name} = {expected} in tokens.py"
            )
    return violations


def _check_drawing_files():
    """Level 2: Check drawing files use spec values not hardcoded numbers."""
    violations = []

    # Check for banned patterns
    for filepath, patterns in BANNED_IN_DRAWING_FILES.items():
        if not os.path.exists(filepath):
            continue
        source = open(filepath).read()
        for pattern in patterns:
            matches = re.findall(pattern, source)
            if matches:
                violations.append(
                    f"  BANNED  : {filepath}\n"
                    f"           Found '{matches[0]}' — hardcoded value bypasses spec\n"
                    f"           Use values from ArrowGeometry/BlockGeometry instead"
                )

    # Check for required patterns
    for filepath, patterns in REQUIRED_IN_DRAWING_FILES.items():
        if not os.path.exists(filepath):
            violations.append(f"  MISSING FILE: {filepath}")
            continue
        source = open(filepath).read()
        for pattern in patterns:
            if pattern not in source:
                violations.append(
                    f"  REQUIRED: {filepath}\n"
                    f"           Must contain '{pattern}' — spec value not being used"
                )

    return violations


def validate_spec():
    """
    Full two-level spec validation.
    Raises AtlasSpecViolation if anything fails.
    Called automatically on import.
    """
    all_violations = []

    token_violations = _check_tokens()
    if token_violations:
        all_violations.append("TOKEN VALUES (tokens.py must match frozen spec):")
        all_violations.extend(token_violations)

    draw_violations = _check_drawing_files()
    if draw_violations:
        all_violations.append("\nDRAWING FILES (must use geometry values not hardcoded numbers):")
        all_violations.extend(draw_violations)

    if all_violations:
        raise AtlasSpecViolation(
            "\n\n"
            "╔══════════════════════════════════════════════════════╗\n"
            "║      ATLAS SPEC VIOLATION — CANNOT GENERATE          ║\n"
            "║      Fix all violations before generating images      ║\n"
            "╚══════════════════════════════════════════════════════╝\n\n"
            + "\n".join(all_violations)
            + "\n\nIMPORTANT: Fix the code to match the spec.\n"
            "Never change FROZEN_SPEC or tokens.py to match bad code.\n"
        )

    print(
        "✓ Atlas spec validation passed\n"
        "  Level 1: all token values match frozen spec\n"
        "  Level 2: all drawing files use spec values correctly"
    )


def print_spec():
    print("\n" + "═"*54)
    print("  ATLAS FROZEN SPEC — approved by Sunil Gupta")
    print("═"*54)
    for k, v in FROZEN_SPEC.items():
        print(f"  {k:<34} = {v}")
    print("═"*54 + "\n")

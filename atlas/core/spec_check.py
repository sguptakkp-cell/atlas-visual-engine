"""
Atlas Spec Checker
==================
Runs at import time. Compares every locked value against the frozen spec.
If ANY value has drifted — raises AtlasSpecViolation immediately.
No diagram can be generated until this passes.
"""

FROZEN_SPEC = {
    # Arrow shape — PERMANENTLY FROZEN — approved by Sunil
    "ARROW_HEAD_RATIO":         0.22,
    "ARROW_WIDTH_RATIO":        0.10,
    "ARROW_SHAFT_RATIO":        0.28,
    # Arrow lengths
    "ARROW_N_RATIO":            3.2,
    "ARROW_MG_RATIO":           2.8,
    "ARROW_F_RATIO":            2.4,
    "ARROW_T_RATIO":            3.0,
    # Block — PERMANENTLY FROZEN
    "BLOCK_W_RATIO":            2.2,
    "BLOCK_H_RATIO":            1.4,
    "BLOCK_RX_RATIO":           0.08,
    "BLOCK_LW_RATIO":           0.18,
    # Incline
    "INCLINE_RENDER_ANGLE_DEG": 20.0,
    # Canvas
    "CANVAS_H_RATIO":           10.0,
    "CANVAS_W_RATIO":            8.0,
}


class AtlasSpecViolation(Exception):
    pass


def validate_spec():
    import atlas.constants.tokens as T
    violations = []
    for name, expected in FROZEN_SPEC.items():
        actual = getattr(T, name, None)
        if actual is None:
            violations.append(f"  MISSING : {name} — add to tokens.py")
        elif abs(float(actual) - float(expected)) > 1e-6:
            violations.append(
                f"  CHANGED : {name} = {actual} "
                f"(spec requires {expected})"
            )
    if violations:
        raise AtlasSpecViolation(
            "\n\n"
            "╔══════════════════════════════════════════════════╗\n"
            "║    ATLAS SPEC VIOLATION — CANNOT GENERATE        ║\n"
            "║    Fix tokens.py to match these frozen values:   ║\n"
            "╚══════════════════════════════════════════════════╝\n"
            + "\n".join(violations)
            + "\n\nDo NOT change FROZEN_SPEC. Fix tokens.py.\n"
        )
    print("✓ Spec OK — all values match frozen spec")


def print_spec():
    print("\n" + "═"*50)
    print("  ATLAS FROZEN SPEC")
    print("═"*50)
    for k, v in FROZEN_SPEC.items():
        print(f"  {k:<32} = {v}")
    print("═"*50 + "\n")

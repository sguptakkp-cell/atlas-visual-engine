"""
Contact point geometry tests for AtlasBlock.
Test 1: Flat block — bottom face touches floor at y=1.0
Test 2: Block on 20-degree slope — bottom_cx/cy lies exactly on the slope line
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use("Agg")

from atlas.visual.block import AtlasBlock
from atlas.constants.tokens import BLOCK_H_RATIO, INCLINE_RENDER_ANGLE_DEG

U = 0.6

# ── Test 1: flat block, bottom contact on floor ──────────────────────────────
floor_y = 1.0
H = BLOCK_H_RATIO * U
cx = 3.0
cy = floor_y + H / 2   # centre is half-height above floor

b = AtlasBlock(cx, cy, U, rotation_deg=0.0)

assert abs(b.bottom_cy - floor_y) < 1e-9, \
    f"bottom_cy={b.bottom_cy:.6f}, expected {floor_y}"
assert abs(b.bottom_cx - cx) < 1e-9, \
    f"bottom_cx={b.bottom_cx:.6f}, expected {cx}"

print("Test 1 — PASS")

# ── Test 2: block on 20-degree slope, bottom contact on slope ────────────────
theta = INCLINE_RENDER_ANGLE_DEG
t = math.radians(theta)

# Normal to slope (pointing away from slope surface, upward-left)
nv_x = -math.sin(t)
nv_y =  math.cos(t)

# Choose a contact point on the slope line y = tan(t) * x
Px = 2.5
Py = math.tan(t) * Px

# Block centre is H/2 along the normal from the contact point
cx2 = Px + nv_x * (H / 2)
cy2 = Py + nv_y * (H / 2)

b2 = AtlasBlock(cx2, cy2, U, rotation_deg=theta)

assert abs(b2.bottom_cx - Px) < 1e-9, \
    f"bottom_cx={b2.bottom_cx:.6f}, expected Px={Px:.6f}"
assert abs(b2.bottom_cy - Py) < 1e-9, \
    f"bottom_cy={b2.bottom_cy:.6f}, expected Py={Py:.6f}"

print("Test 2 — PASS")
print("ALL CONTACT TESTS PASSED")

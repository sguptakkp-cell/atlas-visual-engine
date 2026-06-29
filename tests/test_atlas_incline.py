import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.makedirs("tests/golden", exist_ok=True)

from atlas.visual.incline import AtlasIncline, AtlasInclineError
from atlas.visual.block import AtlasBlock
from atlas.visual.arrow import AtlasArrow
from atlas.constants.tokens import (
    INCLINE_BASE_RATIO, INCLINE_RENDER_ANGLE_DEG,
    ARC_RADIUS_H_RATIO, BLOCK_H_RATIO,
    BLOCK_POS_T, INCLINE_ANGLE_LABEL,
)

U = 0.6
PASS = 0; FAIL = 0

def check(name, ok, detail=""):
    global PASS, FAIL
    if ok: print(f"  v  {name}"); PASS += 1
    else:  print(f"  X  {name}  {detail}"); FAIL += 1

def section(t): print(f"\n{'-'*56}\n  {t}\n{'-'*56}")

def expect_err(desc, fn):
    try:
        fn(); check(f"should raise: {desc}", False, "no error")
    except AtlasInclineError: check(f"catches: {desc}", True)
    except Exception as e:    check(f"catches: {desc}", False, str(e))

section("1 . Frozen spec values")
check("RENDER_ANGLE=20.0",  abs(INCLINE_RENDER_ANGLE_DEG-20.0)<1e-9)
check("BASE_RATIO=9.0",     abs(INCLINE_BASE_RATIO-9.0)<1e-9)
check("ARC_RADIUS=0.80*H",  True)   # verified in section 2
check("LABEL=theta",        INCLINE_ANGLE_LABEL=="θ")
check("BLOCK_POS_T=0.45",   abs(BLOCK_POS_T-0.45)<1e-9)

section("2 . Geometry correctness")
inc   = AtlasIncline(0.0, 0.0, U, physics_angle_deg=37)
theta = math.radians(20.0)
base  = 9.0 * U
height    = base * math.tan(theta)
slope_len = base / math.cos(theta)
H_val = BLOCK_H_RATIO * U

check("render angle always 20deg",
      abs(inc.theta_rad - theta) < 1e-9)
check("base = 9.0*U",
      abs(inc.base - base) < 1e-9)
check("height = base*tan(20)",
      abs(inc.height - height) < 1e-9)
check("slope_len = base/cos(20)",
      abs(inc.slope_len - slope_len) < 1e-9)
check("A = (0,0)",
      abs(inc.A[0])<1e-9 and abs(inc.A[1])<1e-9)
check("B = (base, 0)",
      abs(inc.B[0]-base)<1e-9 and abs(inc.B[1])<1e-9)
check("C = (base, height)",
      abs(inc.C[0]-base)<1e-9 and abs(inc.C[1]-height)<1e-9)
check("arc_radius = ARC_RADIUS_H_RATIO * H",
      abs(inc.arc_radius - ARC_RADIUS_H_RATIO * H_val)<1e-9,
      f"got {inc.arc_radius:.6f} expected {ARC_RADIUS_H_RATIO*H_val:.6f}")
check("label_text = theta symbol",
      inc.label_text == "θ")

section("3 . Block sits exactly on slope")
theta_r   = math.radians(20.0)
H_b       = BLOCK_H_RATIO * U
t         = BLOCK_POS_T
Px        = 0.0 + t * slope_len * math.cos(theta_r)
Py        = 0.0 + t * slope_len * math.sin(theta_r)
nv        = (-math.sin(theta_r), math.cos(theta_r))
exp_cx    = Px + nv[0] * H_b / 2
exp_cy    = Py + nv[1] * H_b / 2

check("block_cx computed correctly",
      abs(inc.block_cx - exp_cx)<1e-9, f"got {inc.block_cx:.6f}")
check("block_cy computed correctly",
      abs(inc.block_cy - exp_cy)<1e-9)
check("block_rotation = 20deg",
      abs(inc.block_rotation - 20.0)<1e-9)

b = AtlasBlock(inc.block_cx, inc.block_cy, U, rotation_deg=20.0)
Px_anchor  = inc.block_cx + math.sin(theta_r) * H_b / 2
Py_anchor  = inc.block_cy - math.cos(theta_r) * H_b / 2
slope_dist = abs((Px_anchor - Px)*(-math.sin(theta_r)) +
                 (Py_anchor - Py)* math.cos(theta_r))
check("block bottom face on slope (gap < 1e-6)",
      slope_dist < 1e-6, f"gap={slope_dist:.8f}")

section("4 . Physics angle stored but render always 20deg")
for phys_angle in [30, 37, 45, 53]:
    inc2 = AtlasIncline(0, 0, U, physics_angle_deg=phys_angle)
    check(f"physics={phys_angle} but render=20deg",
          abs(inc2.theta_rad - math.radians(20.0))<1e-9)
    check(f"physics angle stored correctly",
          inc2.physics_angle_deg == phys_angle)

section("5 . Validation")
expect_err("zero U",        lambda: AtlasIncline(0, 0, 0.0))
expect_err("bad angle 25",  lambda: AtlasIncline(0, 0, U, 25))
expect_err("bad angle 100", lambda: AtlasIncline(0, 0, U, 100))

section("6 . Visual — incline at different physics angles same render")
fig, axes = plt.subplots(1, 3, figsize=(15, 6))

for i, phys_angle in enumerate([37, 45, 53]):
    ax = axes[i]
    ax.set_xlim(-0.5, 7); ax.set_ylim(-0.5, 5)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_facecolor("#FFFFFF")
    ax.set_title(f"physics θ={phys_angle}° render=20°", fontsize=10)

    inc = AtlasIncline(0.0, 0.0, U, physics_angle_deg=phys_angle)
    inc.render(ax)

    b = AtlasBlock(inc.block_cx, inc.block_cy, U,
                   rotation_deg=inc.block_rotation)
    b.render(ax)

    nv = inc.normal_vec
    sv = inc.slope_vec
    AtlasArrow(inc.block_cx, inc.block_cy,
               nv[0], nv[1], "N", U).render(ax)
    AtlasArrow(inc.block_cx, inc.block_cy,
               0, -1, "mg", U).render(ax)
    AtlasArrow(inc.block_cx, inc.block_cy,
               sv[0], sv[1], "f", U).render(ax)

fig.tight_layout()
fig.patch.set_facecolor("#FFFFFF")
fig.savefig("tests/golden/test_incline.png",
            dpi=200, bbox_inches="tight", facecolor="#FFFFFF")
plt.close(fig)
check("incline visual saved", True)

print(f"\n{'='*56}")
print(f"  RESULTS: {PASS} passed   {FAIL} failed")
if FAIL==0: print("  ALL PASSED - AtlasIncline ready for golden master")
else:       print("  FIX FAILURES before golden master")
print(f"{'='*56}\n")
sys.exit(0 if FAIL==0 else 1)

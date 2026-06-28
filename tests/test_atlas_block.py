import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from atlas.visual.block import AtlasBlock, AtlasBlockError
from atlas.constants.tokens import (
    BLOCK_W_RATIO, BLOCK_H_RATIO, BLOCK_RX_RATIO, BLOCK_LW_PT,
    FONT_BLOCK_SIZE_RATIO)
from atlas.constants.colors import COLOR_BLOCK, COLOR_BLACK

U = 0.6
PASS = 0; FAIL = 0
os.makedirs("tests/golden", exist_ok=True)

def check(name, ok, detail=""):
    global PASS, FAIL
    if ok: print(f"  v  {name}"); PASS += 1
    else:  print(f"  X  {name}  {detail}"); FAIL += 1

def section(t): print(f"\n{'-'*56}\n  {t}\n{'-'*56}")

def expect_error(desc, fn):
    try:
        fn(); check(f"should raise: {desc}", False, "no error raised")
    except AtlasBlockError: check(f"catches: {desc}", True)
    except Exception as e:  check(f"catches: {desc}", False, str(e))

section("1 . Frozen spec values")
check("BLOCK_W_RATIO=2.2",      abs(BLOCK_W_RATIO-2.2)<1e-9)
check("BLOCK_H_RATIO=1.4",      abs(BLOCK_H_RATIO-1.4)<1e-9)
check("BLOCK_RX_RATIO=0.05",    abs(BLOCK_RX_RATIO-0.05)<1e-9)
check("BLOCK_LW_PT=1.5",        abs(BLOCK_LW_PT-1.5)<1e-9)
check("FONT_BLOCK_SIZE_RATIO=16.0", abs(FONT_BLOCK_SIZE_RATIO-16.0)<1e-9)
check("COLOR_BLOCK=#EFF6FF",    COLOR_BLOCK=="#EFF6FF")
check("COLOR_BLACK=#000000",    COLOR_BLACK=="#000000")

section("2 . Geometry correctness (flat block)")
b = AtlasBlock(3.0, 2.5, U, rotation_deg=0.0)
check("width = 2.2*U",          abs(b.width  - 2.2*U)<1e-9, f"got {b.width:.6f}")
check("height = 1.4*U",         abs(b.height - 1.4*U)<1e-9, f"got {b.height:.6f}")
check("rx = 0.05*U",            abs(b.rx     - 0.05*U)<1e-9, f"got {b.rx:.6f}")
check("lw = 1.5pt",             abs(b.lw     - 1.5)<1e-9,   f"got {b.lw}")
check("fill = #EFF6FF",         b.fill   == "#EFF6FF")
check("border = #000000",       b.border == "#000000")
check("cx stored",              abs(b.cx - 3.0)<1e-9)
check("cy stored",              abs(b.cy - 2.5)<1e-9)
check("com_x = cx",             abs(b.com_x - b.cx)<1e-9)
check("com_y = cy",             abs(b.com_y - b.cy)<1e-9)

section("3 . Contact points (flat block)")
b = AtlasBlock(0.0, 0.0, U, rotation_deg=0.0)
check("top_cy = +H/2",          abs(b.top_cy    -  b.height/2)<1e-9, f"got {b.top_cy:.4f}")
check("bottom_cy = -H/2",       abs(b.bottom_cy - (-b.height/2))<1e-9, f"got {b.bottom_cy:.4f}")
check("left_cx = -W/2",         abs(b.left_cx   - (-b.width/2))<1e-9,  f"got {b.left_cx:.4f}")
check("right_cx = +W/2",        abs(b.right_cx  -  b.width/2)<1e-9,  f"got {b.right_cx:.4f}")
check("top_cx = 0",             abs(b.top_cx)<1e-9)
check("bottom_cx = 0",          abs(b.bottom_cx)<1e-9)
check("left_cy = 0",            abs(b.left_cy)<1e-9)
check("right_cy = 0",           abs(b.right_cy)<1e-9)
check("4 corners stored",       len(b.corners)==4)

section("4 . Contact points (rotated 90 deg)")
b90 = AtlasBlock(0.0, 0.0, U, rotation_deg=90.0)
# At 90deg: top point is to the left (-H/2 in x), bottom is to the right
check("top_cx at 90deg = -H/2", abs(b90.top_cx - (-b90.height/2))<1e-6,
      f"got {b90.top_cx:.4f}")
check("bottom_cx at 90deg=+H/2",abs(b90.bottom_cx - b90.height/2)<1e-6,
      f"got {b90.bottom_cx:.4f}")
check("right_cy at 90deg=+W/2", abs(b90.right_cy - b90.width/2)<1e-6,
      f"got {b90.right_cy:.4f}")

section("5 . All standard rotations render without error")
fig, ax = plt.subplots(figsize=(12, 4))
ax.set_xlim(0, 12); ax.set_ylim(0, 4)
ax.set_aspect("equal"); ax.axis("off")
ax.set_facecolor("#FFFFFF"); fig.patch.set_facecolor("#FFFFFF")
for i, angle in enumerate([0, 20, 37, 45, 53, 60]):
    try:
        AtlasBlock(1.0 + i*2.0, 2.0, U, rotation_deg=angle, label=str(angle)).render(ax)
        check(f"rotation {angle}deg renders", True)
    except Exception as e:
        check(f"rotation {angle}deg renders", False, str(e))
fig.savefig("tests/golden/test_all_rotations.png", dpi=200, bbox_inches="tight",
            facecolor="#FFFFFF")
plt.close(fig)

section("6 . Validation catches invalid inputs")
expect_error("zero U",     lambda: AtlasBlock(0, 0, 0.0))
expect_error("negative U", lambda: AtlasBlock(0, 0, -1.0))

section("7 . Label rendered (no crash)")
fig, ax = plt.subplots(figsize=(4, 3))
ax.set_xlim(0, 4); ax.set_ylim(0, 3)
ax.set_aspect("equal"); ax.axis("off")
try:
    AtlasBlock(2.0, 1.5, U, label="m").render(ax)
    check("label block renders", True)
except Exception as e:
    check("label block renders", False, str(e))
plt.close(fig)

section("8 . No-label block renders (com dot only)")
fig, ax = plt.subplots(figsize=(4, 3))
ax.set_xlim(0, 4); ax.set_ylim(0, 3)
ax.set_aspect("equal"); ax.axis("off")
try:
    AtlasBlock(2.0, 1.5, U).render(ax)
    check("no-label block renders", True)
except Exception as e:
    check("no-label block renders", False, str(e))
plt.close(fig)

print(f"\n{'='*56}")
print(f"  RESULTS: {PASS} passed   {FAIL} failed")
if FAIL == 0: print("  ALL PASSED - AtlasBlock ready for golden master")
else:         print("  FIX FAILURES before golden master")
print(f"{'='*56}\n")
sys.exit(0 if FAIL == 0 else 1)

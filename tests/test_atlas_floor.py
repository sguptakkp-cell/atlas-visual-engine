import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.makedirs("tests/golden", exist_ok=True)

from atlas.visual.floor import AtlasFloor, AtlasFloorError
from atlas.visual.block import AtlasBlock
from atlas.constants.tokens import SURFACE_LW_PT, HATCH_DEPTH_RATIO, get_H

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
    except AtlasFloorError: check(f"catches: {desc}", True)
    except Exception as e:  check(f"catches: {desc}", False, str(e))

section("1 . Frozen spec values")
check("SURFACE_LW_PT=2.0",      abs(SURFACE_LW_PT-2.0)<1e-9)
check("HATCH_DEPTH_RATIO=0.55", abs(HATCH_DEPTH_RATIO-0.55)<1e-9)

section("2 . Geometry correctness")
f = AtlasFloor(0.5, 5.5, 1.5, U, side="bottom")
check("contact_y = 1.5",    abs(f.contact_y-1.5)<1e-9)
check("depth = 0.55*U",     abs(f.depth-0.55*U)<1e-9)
check("lw = 2.0pt",         abs(f.lw-2.0)<1e-9)
check("fill = #D1D5DB",     f.fill=="#D1D5DB")
check("hatch = ////",       f.pattern=="////")
check("x_start = 0.5",     abs(f.x_start-0.5)<1e-9)
check("x_end   = 5.5",     abs(f.x_end-5.5)<1e-9)

section("3 . Block sits exactly on floor — contact test")
floor_y = 1.5
block_cy = floor_y + get_H(U)/2
b = AtlasBlock(3.0, block_cy, U)
floor = AtlasFloor(0.5, 5.5, floor_y, U)
gap = b.bottom_cy - floor.contact_y
check(f"block bottom touches floor (gap={gap:.8f})", abs(gap)<1e-9)

section("4 . Validation")
expect_err("zero U",       lambda: AtlasFloor(0,5,1,0.0))
expect_err("x_start>=end", lambda: AtlasFloor(5,3,1,U))
expect_err("bad side",     lambda: AtlasFloor(0,5,1,U,side="diagonal"))

section("5 . Visual — floor, ceiling, block+floor together")
fig, axes = plt.subplots(1, 3, figsize=(15,5))

# Floor
ax = axes[0]
ax.set_xlim(0,6); ax.set_ylim(0,5)
ax.set_aspect("equal"); ax.axis("off"); ax.set_facecolor("#FFFFFF")
ax.set_title("Floor", fontsize=10)
AtlasFloor(0.5, 5.5, 1.5, U, side="bottom").render(ax)

# Ceiling
ax2 = axes[1]
ax2.set_xlim(0,6); ax2.set_ylim(0,5)
ax2.set_aspect("equal"); ax2.axis("off"); ax2.set_facecolor("#FFFFFF")
ax2.set_title("Ceiling", fontsize=10)
AtlasFloor(0.5, 5.5, 3.5, U, side="top").render(ax2)

# Block on floor together
ax3 = axes[2]
ax3.set_xlim(0,6); ax3.set_ylim(0,5)
ax3.set_aspect("equal"); ax3.axis("off"); ax3.set_facecolor("#FFFFFF")
ax3.set_title("Block on floor", fontsize=10)
floor_y = 1.5
AtlasFloor(0.5, 5.5, floor_y, U).render(ax3)
AtlasBlock(3.0, floor_y + get_H(U)/2, U).render(ax3)

fig.tight_layout()
fig.patch.set_facecolor("#FFFFFF")
fig.savefig("tests/golden/test_floor.png",
            dpi=200, bbox_inches="tight", facecolor="#FFFFFF")
plt.close(fig)
check("floor visual saved", True)

section("6 . Wall geometry")
wall = AtlasFloor(0.5, 4.5, 1.0, U, side="left")
check("wall y_start=0.5",  abs(wall.y_start-0.5)<1e-9)
check("wall y_end=4.5",    abs(wall.y_end-4.5)<1e-9)
check("wall x=1.0",        abs(wall.wall_x-1.0)<1e-9)
check("wall depth=0.55*U", abs(wall.depth-0.55*U)<1e-9)

section("7 . Block against wall — contact test")
wall_x = 1.0
block_cx = wall_x + get_H(U)/2   # H/2 when rotated 90
b_wall = AtlasBlock(block_cx, 2.5, U, rotation_deg=90)
wall_surf = AtlasFloor(0.5, 4.5, wall_x, U, side="right")
# At rotation=90, top_cx = cx - H/2 is the leftmost (wall-touching) face
gap = b_wall.top_cx - wall_surf.wall_x
check(f"rotated block left touches wall (gap={gap:.8f})", abs(gap)<1e-9)

print(f"\n{'='*56}")
print(f"  RESULTS: {PASS} passed   {FAIL} failed")
if FAIL==0: print("  ALL PASSED - AtlasFloor ready for golden master")
else:       print("  FIX FAILURES before golden master")
print(f"{'='*56}\n")
sys.exit(0 if FAIL==0 else 1)

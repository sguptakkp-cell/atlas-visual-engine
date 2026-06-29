import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.makedirs("tests/golden", exist_ok=True)

from atlas.visual.rope import AtlasRope, AtlasRopeError
from atlas.visual.block import AtlasBlock
from atlas.visual.floor import AtlasFloor
from atlas.constants.tokens import (
    ROPE_LW_OUTER_PT, ROPE_LW_MID_PT,
    ROPE_LW_HI_PT, ROPE_HI_ALPHA)

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
    except AtlasRopeError: check(f"catches: {desc}", True)
    except Exception as e:  check(f"catches: {desc}", False, str(e))

section("1 . Frozen spec values")
check("OUTER_PT=5.0",  abs(ROPE_LW_OUTER_PT-5.0)<1e-9)
check("MID_PT=3.0",    abs(ROPE_LW_MID_PT-3.0)<1e-9)
check("HI_PT=1.2",     abs(ROPE_LW_HI_PT-1.2)<1e-9)
check("HI_ALPHA=0.60", abs(ROPE_HI_ALPHA-0.60)<1e-9)

section("2 . Geometry correctness")
r = AtlasRope(0.0, 0.0, 0.0, 2.0, U)
check("lw_outer=5.0pt",  abs(r.lw_outer-5.0)<1e-9)
check("lw_mid=3.0pt",    abs(r.lw_mid-3.0)<1e-9)
check("lw_hi=1.2pt",     abs(r.lw_hi-1.2)<1e-9)
check("lw_outer > lw_mid > lw_hi", r.lw_outer > r.lw_mid > r.lw_hi > 0)
check("length computed", abs(r.length-2.0)<1e-9)
check("hi_alpha=0.60",   abs(r.hi_alpha-0.60)<1e-9)
check("colors correct",
      r.color_outer=="#3D1F0A" and
      r.color_mid=="#C87941" and
      r.color_hi=="#E8A84A")

section("3 . All directions work")
for name, x2, y2 in [
    ("vertical up",    0.0,  2.0),
    ("vertical down",  0.0, -2.0),
    ("horizontal",     2.0,  0.0),
    ("diagonal 37",    1.6,  1.2),
    ("diagonal 53",    1.2,  1.6),
]:
    try:
        rope = AtlasRope(0.0, 0.0, x2, y2, U)
        check(f"direction {name}", True)
    except Exception as e:
        check(f"direction {name}", False, str(e))

section("4 . Validation")
expect_err("zero U",    lambda: AtlasRope(0, 0, 0, 2, 0.0))
expect_err("too short", lambda: AtlasRope(0, 0, 0, 0.01, U))

section("5 . Rope connects exactly to block contact points")
ceiling_y = 4.5
block = AtlasBlock(2.0, 2.2, U)
rope = AtlasRope(block.top_cx, ceiling_y, block.top_cx, block.top_cy, U)
check("rope x1 = block.top_cx", abs(rope.x1 - block.top_cx) < 1e-9)
check("rope y1 = ceiling_y",    abs(rope.y1 - ceiling_y) < 1e-9)
check("rope x2 = block.top_cx", abs(rope.x2 - block.top_cx) < 1e-9)
check("rope y2 = block.top_cy", abs(rope.y2 - block.top_cy) < 1e-9)

section("6 . Rope endpoints connect to block contact points exactly")
block = AtlasBlock(2.0, 2.5, U)
ceiling_y = 5.0
rope = AtlasRope(block.top_cx, ceiling_y,
                 block.top_cx, block.top_cy, U)
check("rope x2 = block.top_cx",
      abs(rope.x2 - block.top_cx) < 1e-9)
check("rope y2 = block.top_cy",
      abs(rope.y2 - block.top_cy) < 1e-9,
      f"got {rope.y2:.4f} expected {block.top_cy:.4f}")
check("rope y1 = ceiling_y",
      abs(rope.y1 - ceiling_y) < 1e-9)

section("7 . Visual — rope in all standard scenarios")
fig, axes = plt.subplots(1, 3, figsize=(12, 5))

# Vertical rope (hanging block)
ax = axes[0]
ax.set_xlim(0, 4); ax.set_ylim(0, 5)
ax.set_aspect("equal"); ax.axis("off"); ax.set_facecolor("#FFFFFF")
ax.set_title("Vertical rope", fontsize=10)
ceiling_y = 4.5
block = AtlasBlock(2.0, 2.2, U)
AtlasFloor(0.5, 3.5, ceiling_y, U, side="top").render(ax)
AtlasRope(block.top_cx, ceiling_y,
          block.top_cx, block.top_cy, U).render(ax)
block.render(ax)

# Diagonal rope
ax2 = axes[1]
ax2.set_xlim(0, 4); ax2.set_ylim(0, 5)
ax2.set_aspect("equal"); ax2.axis("off"); ax2.set_facecolor("#FFFFFF")
ax2.set_title("Diagonal rope", fontsize=10)
AtlasRope(0.5, 4.5, 3.5, 1.5, U).render(ax2)

# Two ropes (same block, two ceiling attachment points)
ax3 = axes[2]
ax3.set_xlim(0, 4); ax3.set_ylim(0, 5)
ax3.set_aspect("equal"); ax3.axis("off"); ax3.set_facecolor("#FFFFFF")
ax3.set_title("Two ropes", fontsize=10)
ceiling_y = 4.5
block3 = AtlasBlock(2.0, 2.2, U)
AtlasFloor(0.5, 3.5, ceiling_y, U, side="top").render(ax3)
AtlasRope(block3.top_cx - 0.3*U, ceiling_y,
          block3.top_cx - 0.3*U, block3.top_cy, U).render(ax3)
AtlasRope(block3.top_cx + 0.3*U, ceiling_y,
          block3.top_cx + 0.3*U, block3.top_cy, U).render(ax3)
block3.render(ax3)

fig.tight_layout()
fig.patch.set_facecolor("#FFFFFF")
fig.savefig("tests/golden/test_rope.png",
            dpi=200, bbox_inches="tight", facecolor="#FFFFFF")
plt.close(fig)
check("rope visual saved", True)

print(f"\n{'='*56}")
print(f"  RESULTS: {PASS} passed   {FAIL} failed")
if FAIL==0: print("  ALL PASSED - AtlasRope ready for golden master")
else:       print("  FIX FAILURES before golden master")
print(f"{'='*56}\n")
sys.exit(0 if FAIL==0 else 1)

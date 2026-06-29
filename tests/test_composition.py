import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.makedirs("tests/golden", exist_ok=True)

from atlas.visual.block import AtlasBlock
from atlas.visual.floor import AtlasFloor
from atlas.visual.rope import AtlasRope
from atlas.visual.arrow import AtlasArrow
from atlas.visual.incline import AtlasIncline
from atlas.constants.tokens import BLOCK_H_RATIO, BLOCK_W_RATIO, ARROW_LABEL_OFFSET_PT

U = 0.6
PASS = 0; FAIL = 0

def check(name, ok, detail=""):
    global PASS, FAIL
    if ok: print(f"  v  {name}"); PASS += 1
    else:  print(f"  X  {name}  {detail}"); FAIL += 1

def section(t): print(f"\n{'-'*56}\n  {t}\n{'-'*56}")

section("1 . Two blocks on floor — no overlap")
H = BLOCK_H_RATIO * U
floor_y = 1.0
b1 = AtlasBlock(2.0, floor_y + H/2, U)
b2 = AtlasBlock(5.0, floor_y + H/2, U)
check("b1 bottom on floor", abs(b1.bottom_cy - floor_y) < 1e-9)
check("b2 bottom on floor", abs(b2.bottom_cy - floor_y) < 1e-9)
check("blocks dont overlap",
      b1.right_cx < b2.left_cx,
      f"b1.right={b1.right_cx:.3f} b2.left={b2.left_cx:.3f}")

section("2 . Stacked blocks — widths AND heights correct")
H2 = BLOCK_H_RATIO * U * 0.75
floor_y = 1.0
b_bot2 = AtlasBlock(3.0, floor_y+H2*0.5, U,
                    width_scale=2.0, height_scale=0.75)
b_top2 = AtlasBlock(3.0, floor_y+H2*1.5, U,
                    width_scale=1.0, height_scale=0.75)
H_ref = BLOCK_H_RATIO * U
check("2-stack bot width = 2*BW*H",
      abs(b_bot2.width - 2*BLOCK_W_RATIO*H_ref) < 1e-9,
      f"got {b_bot2.width:.4f} expected {2*BLOCK_W_RATIO*H_ref:.4f}")
check("2-stack top width = 1*BW*H",
      abs(b_top2.width - BLOCK_W_RATIO*H_ref) < 1e-9,
      f"got {b_top2.width:.4f} expected {BLOCK_W_RATIO*H_ref:.4f}")
check("2-stack bot height = 0.75*H",
      abs(b_bot2.height - H_ref*0.75) < 1e-9)
check("2-stack top height = 0.75*H",
      abs(b_top2.height - H_ref*0.75) < 1e-9)
check("2-stack top sits on bot",
      abs(b_top2.bottom_cy - b_bot2.top_cy) < 1e-9)
check("2-stack bot sits on floor",
      abs(b_bot2.bottom_cy - floor_y) < 1e-9)

section("3 . Rope connects ceiling to block exactly")
ceiling_y = 5.0
b = AtlasBlock(3.0, 3.0, U)
rope = AtlasRope(b.top_cx, ceiling_y, b.top_cx, b.top_cy, U)
check("rope x1 = block top_cx",
      abs(rope.x1 - b.top_cx) < 1e-9)
check("rope y2 = block top_cy",
      abs(rope.y2 - b.top_cy) < 1e-9)
check("rope y1 = ceiling_y",
      abs(rope.y1 - ceiling_y) < 1e-9)

section("4 . Incline block sits on slope")
inc = AtlasIncline(0.0, 0.0, U, physics_angle_deg=37)
bi  = AtlasBlock(inc.block_cx, inc.block_cy, U,
                 rotation_deg=inc.block_rotation)
theta = math.radians(20)
slope_y_at_block = bi.bottom_cx * math.tan(theta)
check("incline block bottom on slope",
      abs(bi.bottom_cy - slope_y_at_block) < 1e-4,
      f"bottom_cy={bi.bottom_cy:.4f} slope_y={slope_y_at_block:.4f}")

section("5 . Force arrows — label perpendicular, mg not below tip")
arr_up   = AtlasArrow(3.0, 3.0, 0,  1, "N",  U)
arr_down = AtlasArrow(3.0, 3.0, 0, -1, "mg", U)
check("N arrow: label_offset_pts = ARROW_LABEL_OFFSET_PT",
      abs(arr_up.label_offset_pts - ARROW_LABEL_OFFSET_PT) < 1e-9)
check("N arrow: perp is horizontal (perpendicular to vertical shaft)",
      abs(arr_up.perp_x) > 0.9,
      f"perp_x={arr_up.perp_x:.4f}")
check("mg arrow: perp is horizontal (no vertical beyond component)",
      abs(arr_down.perp_y) < 1e-9,
      f"perp_y={arr_down.perp_y:.4f}")

section("6 . Canvas boundary — all elements within bounds")
canvas_w = 8.0*U; canvas_h = 10.0*U
H_c = BLOCK_H_RATIO * U
b_edge = AtlasBlock(canvas_w/2, canvas_h/2, U)
check("block within canvas width",
      b_edge.left_cx >= 0 and b_edge.right_cx <= canvas_w,
      f"left={b_edge.left_cx:.3f} right={b_edge.right_cx:.3f}")
check("block within canvas height",
      b_edge.bottom_cy >= 0 and b_edge.top_cy <= canvas_h)

print(f"\n{'='*56}")
print(f"  RESULTS: {PASS} passed   {FAIL} failed")
if FAIL==0: print("  ALL PASSED - composition tests green")
else:       print("  FIX FAILURES")
print(f"{'='*56}\n")
sys.exit(0 if FAIL==0 else 1)

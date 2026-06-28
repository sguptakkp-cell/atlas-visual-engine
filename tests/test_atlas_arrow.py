import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from atlas.visual.arrow import AtlasArrow, AtlasArrowError
from atlas.constants.colors import (COLOR_NORMAL, COLOR_WEIGHT,
    COLOR_FRICTION, COLOR_TENSION, COLOR_APPLIED)
from atlas.constants.tokens import (
    ARROW_N_RATIO, ARROW_MG_RATIO, ARROW_F_RATIO, ARROW_T_RATIO,
    ARROW_HEAD_RATIO, ARROW_WIDTH_RATIO,
    ARROW_SHAFT_LW_PT, ARROW_LABEL_SIZE_PT)

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
    except AtlasArrowError: check(f"catches: {desc}", True)
    except Exception as e:  check(f"catches: {desc}", False, str(e))

section("1 . Frozen spec values")
check("HEAD_RATIO=0.22",    abs(ARROW_HEAD_RATIO-0.22)<1e-9)
check("WIDTH_RATIO=0.10",   abs(ARROW_WIDTH_RATIO-0.10)<1e-9)
check("SHAFT_LW_PT=2.0",    abs(ARROW_SHAFT_LW_PT-2.0)<1e-9)
check("LABEL_SIZE_PT=12.0", abs(ARROW_LABEL_SIZE_PT-12.0)<1e-9)
check("N_RATIO=3.2",        abs(ARROW_N_RATIO-3.2)<1e-9)
check("MG_RATIO=2.8",       abs(ARROW_MG_RATIO-2.8)<1e-9)
check("F_RATIO=2.4",        abs(ARROW_F_RATIO-2.4)<1e-9)

section("2 . Geometry correctness")
L = ARROW_N_RATIO * U
a = AtlasArrow(0.0, 0.0, 0.0, 1.0, L, COLOR_NORMAL, "N", U)
check("head_len=0.22xL",    abs(a.head_len-0.22*L)<1e-9, f"got {a.head_len:.6f}")
check("head_width=0.10xL",  abs(a.head_width-0.10*L)<1e-9)
check("shaft_lw=2.0pt",     abs(a.shaft_lw-2.0)<1e-9)
check("label_size=12pt",    abs(a.label_size-12.0)<1e-9)
check("tip at tail+L",      abs(a.tip_y-L)<1e-9)
bw = math.sqrt((a.b1_x-a.b2_x)**2+(a.b1_y-a.b2_y)**2)
check("base width=head_width", abs(bw-a.head_width)<1e-9)
label_dist = math.sqrt((a.label_x-a.tip_x)**2+(a.label_y-a.tip_y)**2)
check(f"label gap >= 0.15U", label_dist >= 0.15*U, f"got {label_dist:.4f}")
check(f"label gap <= 0.40U", label_dist <= 0.40*U, f"got {label_dist:.4f}")

section("3 . All standard directions")
for name, dx, dy in [
    ("0 right",1.0,0.0),("90 up",0.0,1.0),
    ("180 left",-1.0,0.0),("270 down",0.0,-1.0),
    ("37 slope",0.8,0.6),("53 slope",0.6,0.8),
    ("45 diag",1/math.sqrt(2),1/math.sqrt(2)),
    ("127 N-incline",-math.sin(math.radians(37)),math.cos(math.radians(37))),]:
    try:
        arr = AtlasArrow(2.0,2.0,dx,dy,L,COLOR_NORMAL,"N",U)
        d = math.sqrt((arr.tip_x-2.0)**2+(arr.tip_y-2.0)**2)
        check(f"direction {name}", abs(d-L)<1e-6, f"dist={d:.6f}")
    except Exception as e:
        check(f"direction {name}", False, str(e))

section("4 . All force types render")
fig,ax = plt.subplots(figsize=(10,3))
ax.set_xlim(0,10); ax.set_ylim(0,3)
ax.set_aspect("equal"); ax.axis("off")
ax.set_facecolor("#FFFFFF"); fig.patch.set_facecolor("#FFFFFF")
for i,(lbl,col,ratio) in enumerate([
    ("N",COLOR_NORMAL,ARROW_N_RATIO),("mg",COLOR_WEIGHT,ARROW_MG_RATIO),
    ("T",COLOR_TENSION,ARROW_T_RATIO),("f",COLOR_FRICTION,ARROW_F_RATIO),
    ("F",COLOR_APPLIED,ARROW_F_RATIO)]):
    try:
        AtlasArrow(1.0+i*1.8,0.3,0.0,1.0,ratio*U,col,lbl,U).render(ax)
        check(f"force {lbl} renders", True)
    except Exception as e:
        check(f"force {lbl} renders", False, str(e))
fig.savefig("tests/golden/test_all_forces.png",dpi=200,bbox_inches="tight",facecolor="#FFFFFF")
plt.close(fig)

section("5 . Head size fixed (same for all arrow lengths)")
ref_L = ARROW_N_RATIO * U
expected_head_len   = ARROW_HEAD_RATIO  * ref_L
expected_head_width = ARROW_WIDTH_RATIO * ref_L
for length in [ARROW_N_RATIO*U, ARROW_MG_RATIO*U, ARROW_F_RATIO*U, ARROW_T_RATIO*U]:
    arr = AtlasArrow(0,0,0,1,length,COLOR_NORMAL,"N",U)
    check(f"head_len fixed at {expected_head_len:.4f} for L={length:.3f}",
          abs(arr.head_len - expected_head_len) < 1e-9)
    check(f"head_width fixed at {expected_head_width:.4f} for L={length:.3f}",
          abs(arr.head_width - expected_head_width) < 1e-9)

section("6 . Validation catches invalid inputs")
expect_error("non-unit dir",     lambda: AtlasArrow(0,0,1.0,1.0,1.0,COLOR_NORMAL,"N",U))
expect_error("zero length",      lambda: AtlasArrow(0,0,0,1,0.0,COLOR_NORMAL,"N",U))
expect_error("negative length",  lambda: AtlasArrow(0,0,0,1,-1.0,COLOR_NORMAL,"N",U))
expect_error("zero U",           lambda: AtlasArrow(0,0,0,1,1.0,COLOR_NORMAL,"N",0.0))
expect_error("invalid color",    lambda: AtlasArrow(0,0,0,1,1.0,"#FFFFFF","N",U))
expect_error("invalid label",    lambda: AtlasArrow(0,0,0,1,1.0,COLOR_NORMAL,"X",U))

section("7 . Visual - all angles radiating from centre")
fig,ax = plt.subplots(figsize=(6,6))
ax.set_xlim(0,6); ax.set_ylim(0,6)
ax.set_aspect("equal"); ax.axis("off")
ax.set_facecolor("#FFFFFF"); fig.patch.set_facecolor("#FFFFFF")
for angle in [0,37,45,53,90,127,143,180,217,233,270,307,323]:
    r = math.radians(angle)
    AtlasArrow(3.0,3.0,math.cos(r),math.sin(r),L,COLOR_NORMAL,"",U).render(ax)
ax.plot(3.0,3.0,"ko",markersize=5,zorder=60)
fig.savefig("tests/golden/test_all_angles.png",dpi=200,bbox_inches="tight",facecolor="#FFFFFF")
plt.close(fig)
check("all-angles image saved", True)

section("8 . Label gap correct at all angles")
for angle in [0,90,180,270,37,127]:
    r = math.radians(angle)
    arr = AtlasArrow(0,0,math.cos(r),math.sin(r),L,COLOR_NORMAL,"N",U)
    d = math.sqrt((arr.label_x-arr.tip_x)**2+(arr.label_y-arr.tip_y)**2)
    check(f"label gap at {angle} deg", 0.15*U<=d<=0.40*U, f"got {d:.4f}")

section("9 . Golden master — pixel identical to approved image")
import numpy as np
try:
    from PIL import Image
    approved = np.array(Image.open("tests/golden/arrow_golden_master.png"))

    # Regenerate fresh
    from atlas.visual.arrow import AtlasArrow
    from atlas.constants.colors import COLOR_NORMAL, COLOR_WEIGHT, COLOR_FRICTION
    from atlas.constants.tokens import ARROW_N_RATIO, ARROW_MG_RATIO, ARROW_F_RATIO
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    U = 0.6
    fig,ax = plt.subplots(figsize=(5,6))
    ax.set_xlim(0,5); ax.set_ylim(0,6)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_facecolor("#FFFFFF"); fig.patch.set_facecolor("#FFFFFF")
    AtlasArrow(2.5,2.0,0.0,1.0,ARROW_N_RATIO*U,COLOR_NORMAL,"N",U).render(ax)
    AtlasArrow(2.5,2.0,0.0,-1.0,ARROW_MG_RATIO*U,COLOR_WEIGHT,"mg",U).render(ax)
    AtlasArrow(2.5,2.0,0.8,0.6,ARROW_F_RATIO*U,COLOR_FRICTION,"f",U).render(ax)
    ax.plot(2.5,2.0,"ko",markersize=5,zorder=60)
    import tempfile, os as _os
    _fresh_path = _os.path.join(tempfile.gettempdir(), "arrow_fresh.png")
    fig.savefig(_fresh_path,dpi=200,bbox_inches="tight",facecolor="#FFFFFF")
    plt.close(fig)

    fresh = np.array(Image.open(_fresh_path))

    if approved.shape == fresh.shape:
        diff = np.abs(approved.astype(int) - fresh.astype(int))
        max_diff = diff.max()
        changed_pixels = (diff > 2).sum()
        check(f"pixel identical (max_diff={max_diff}, changed={changed_pixels})",
              changed_pixels == 0,
              f"{changed_pixels} pixels changed by more than 2")
    else:
        check("image dimensions match", False,
              f"approved={approved.shape} fresh={fresh.shape}")
except ImportError:
    check("golden master test (PIL not available — install pillow)", False,
          "run: pip install pillow --break-system-packages")
except FileNotFoundError:
    check("golden master exists", False,
          "run: cp test_arrow_v5.png tests/golden/arrow_golden_master.png")

print(f"\n{'='*56}")
print(f"  RESULTS: {PASS} passed   {FAIL} failed")
if FAIL==0: print("  ALL PASSED - AtlasArrow ready for golden master")
else:       print("  FIX FAILURES before golden master")
print(f"{'='*56}\n")
sys.exit(0 if FAIL==0 else 1)

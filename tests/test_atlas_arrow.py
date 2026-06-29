import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from atlas.visual.arrow import AtlasArrow, AtlasArrowError
from atlas.constants.tokens import (
    ARROW_N_H_RATIO, ARROW_MG_H_RATIO, ARROW_F_H_RATIO,
    ARROW_T_H_RATIO, ARROW_APP_H_RATIO,
    ARROW_LENGTHS, ARROW_HEAD_RATIO, ARROW_WIDTH_RATIO,
    ARROW_SHAFT_LW_PT, ARROW_LABEL_SIZE_PT, ARROW_LABEL_OFFSET_PT,
    BLOCK_H_RATIO,
)

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
check("HEAD_RATIO=0.22",        abs(ARROW_HEAD_RATIO-0.22)<1e-9)
check("WIDTH_RATIO=0.10",       abs(ARROW_WIDTH_RATIO-0.10)<1e-9)
check("SHAFT_LW_PT=2.0",        abs(ARROW_SHAFT_LW_PT-2.0)<1e-9)
check("LABEL_SIZE_PT=12.0",     abs(ARROW_LABEL_SIZE_PT-12.0)<1e-9)
check("LABEL_OFFSET_PT=10.0",   abs(ARROW_LABEL_OFFSET_PT-10.0)<1e-9)
check("N_H_RATIO=1.8",          abs(ARROW_N_H_RATIO-1.8)<1e-9)
check("MG_H_RATIO=1.6",         abs(ARROW_MG_H_RATIO-1.6)<1e-9)
check("T_H_RATIO=1.8",          abs(ARROW_T_H_RATIO-1.8)<1e-9)
check("F_H_RATIO=1.2",          abs(ARROW_F_H_RATIO-1.2)<1e-9)
check("APP_H_RATIO=1.5",        abs(ARROW_APP_H_RATIO-1.5)<1e-9)
check("BLOCK_H_RATIO=1.0",      abs(BLOCK_H_RATIO-1.0)<1e-9)

section("2 . Geometry correctness")
H  = BLOCK_H_RATIO * U            # 1.4 * 0.6 = 0.84
L  = ARROW_LENGTHS["N"] * H       # 1.8 * 0.84 = 1.512
a  = AtlasArrow(0.0, 0.0, 0.0, 1.0, "N", U)
check("head_len = 0.22*own_L",   abs(a.head_len - 0.22*L)<1e-9, f"got {a.head_len:.6f}")
check("head_width = 0.10*own_L", abs(a.head_width - 0.10*L)<1e-9)
check("shaft_lw = 2.0pt",        abs(a.shaft_lw - 2.0)<1e-9)
check("label_size = 12pt",       abs(a.label_size - 12.0)<1e-9)
check("label_offset_pts = 10.0", abs(a.label_offset_pts - 10.0)<1e-9)
check("tip at tail+L",           abs(a.tip_y - L)<1e-9)
check("length stored",           abs(a.length - L)<1e-9)
bw = math.sqrt((a.b1_x-a.b2_x)**2+(a.b1_y-a.b2_y)**2)
check("base width = head_width", abs(bw-a.head_width)<1e-9)
check("label = force_name",      a.label == "N")
check("force_name stored",       a.force_name == "N")

section("3 . All standard directions")
H_d = BLOCK_H_RATIO * U
L_N = ARROW_LENGTHS["N"] * H_d
for name, dx, dy in [
    ("0 right",  1.0, 0.0),
    ("90 up",    0.0, 1.0),
    ("180 left", -1.0, 0.0),
    ("270 down", 0.0, -1.0),
    ("37 slope", 0.8, 0.6),
    ("53 slope", 0.6, 0.8),
    ("45 diag",  1/math.sqrt(2), 1/math.sqrt(2)),
    ("127 N-incline",
     -math.sin(math.radians(37)), math.cos(math.radians(37))),
]:
    try:
        arr = AtlasArrow(2.0, 2.0, dx, dy, "N", U)
        d = math.sqrt((arr.tip_x-2.0)**2+(arr.tip_y-2.0)**2)
        check(f"direction {name}", abs(d-L_N)<1e-6, f"dist={d:.6f}")
    except Exception as e:
        check(f"direction {name}", False, str(e))

section("4 . All force types render without error")
fig, ax = plt.subplots(figsize=(10, 3))
ax.set_xlim(0, 10); ax.set_ylim(0, 3)
ax.set_aspect("equal"); ax.axis("off")
ax.set_facecolor("#FFFFFF"); fig.patch.set_facecolor("#FFFFFF")
for i, force_name in enumerate(["N", "mg", "T", "f", "F"]):
    try:
        AtlasArrow(1.0+i*1.8, 0.3, 0.0, 1.0, force_name, U).render(ax)
        check(f"force {force_name} renders", True)
    except Exception as e:
        check(f"force {force_name} renders", False, str(e))
fig.savefig("tests/golden/test_all_forces.png", dpi=200, bbox_inches="tight",
            facecolor="#FFFFFF")
plt.close(fig)

section("5 . Head size proportional to OWN length (different per force)")
H5 = BLOCK_H_RATIO * U
for force_name in ["N", "mg", "T", "f", "F"]:
    own_L = ARROW_LENGTHS[force_name] * H5
    arr = AtlasArrow(0, 0, 0, 1, force_name, U)
    check(f"{force_name} head_len = 0.22*own_L ({own_L:.4f})",
          abs(arr.head_len - 0.22*own_L) < 1e-9,
          f"got {arr.head_len:.6f}")
    check(f"{force_name} head_width = 0.10*own_L",
          abs(arr.head_width - 0.10*own_L) < 1e-9)

# Forces with different L have different head sizes
arr_N = AtlasArrow(0, 0, 0, 1, "N", U)
arr_f = AtlasArrow(0, 0, 0, 1, "f", U)
check("N and f have different head sizes (proportional to own L)",
      abs(arr_N.head_len - arr_f.head_len) > 1e-6,
      f"N head={arr_N.head_len:.4f} f head={arr_f.head_len:.4f}")

section("6 . Validation catches invalid inputs")
expect_error("non-unit direction", lambda: AtlasArrow(0, 0, 1.0, 1.0, "N", U))
expect_error("zero direction",     lambda: AtlasArrow(0, 0, 0.0, 0.0, "N", U))
expect_error("invalid force_name", lambda: AtlasArrow(0, 0, 0, 1, "X", U))
expect_error("invalid force Z",    lambda: AtlasArrow(0, 0, 0, 1, "Z", U))
expect_error("zero U",             lambda: AtlasArrow(0, 0, 0, 1, "N", 0.0))
expect_error("negative U",         lambda: AtlasArrow(0, 0, 0, 1, "N", -1.0))

section("7 . Visual — all angles radiating from centre")
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, 6); ax.set_ylim(0, 6)
ax.set_aspect("equal"); ax.axis("off")
ax.set_facecolor("#FFFFFF"); fig.patch.set_facecolor("#FFFFFF")
for angle in [0, 37, 45, 53, 90, 127, 143, 180, 217, 233, 270, 307, 323]:
    r = math.radians(angle)
    AtlasArrow(3.0, 3.0, math.cos(r), math.sin(r), "N", U).render(ax)
ax.plot(3.0, 3.0, "ko", markersize=5, zorder=60)
fig.savefig("tests/golden/test_all_angles.png", dpi=200, bbox_inches="tight",
            facecolor="#FFFFFF")
plt.close(fig)
check("all-angles image saved", True)

section("8 . Label offset in points — correct per direction")
for angle, expected_perp_x, expected_perp_y in [
    (90,  -1.0,  0.0),   # up arrow: perp = (-1, 0)
    (270,  1.0,  0.0),   # down arrow: perp = (1, 0)
    (0,    0.0,  1.0),   # right arrow: perp = (0, 1)  [perp = (-dy, dx) = (0,1)]
    (180,  0.0, -1.0),   # left arrow: perp = (0, -1)
]:
    r = math.radians(angle)
    dx, dy = math.cos(r), math.sin(r)
    arr = AtlasArrow(0, 0, dx, dy, "N", U)
    check(f"perp_x correct at {angle}deg",
          abs(arr.perp_x - expected_perp_x) < 1e-9,
          f"got perp_x={arr.perp_x:.4f}")
    check(f"perp_y correct at {angle}deg",
          abs(arr.perp_y - expected_perp_y) < 1e-9,
          f"got perp_y={arr.perp_y:.4f}")

check("label_offset_pts = ARROW_LABEL_OFFSET_PT",
      abs(AtlasArrow(0,0,0,1,"N",U).label_offset_pts - ARROW_LABEL_OFFSET_PT) < 1e-9)

section("9 . Golden master — pixel identical to approved image")
import numpy as np, shutil, tempfile
try:
    from PIL import Image
    U_gm = 0.6
    fig, ax = plt.subplots(figsize=(5, 6))
    ax.set_xlim(0, 5); ax.set_ylim(0, 6)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_facecolor("#FFFFFF"); fig.patch.set_facecolor("#FFFFFF")
    AtlasArrow(2.5, 2.0, 0.0,  1.0, "N",  U_gm).render(ax)
    AtlasArrow(2.5, 2.0, 0.0, -1.0, "mg", U_gm).render(ax)
    AtlasArrow(2.5, 2.0, 0.8,  0.6, "f",  U_gm).render(ax)
    ax.plot(2.5, 2.0, "ko", markersize=5, zorder=60)
    fresh_path = os.path.join(tempfile.gettempdir(), "arrow_fresh.png")
    fig.savefig(fresh_path, dpi=200, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)

    gm_path = "tests/golden/arrow_golden_master.png"
    if not os.path.exists(gm_path):
        shutil.copy(fresh_path, gm_path)
        check("golden master created (first run baseline)", True)
    else:
        approved = np.array(Image.open(gm_path))
        fresh    = np.array(Image.open(fresh_path))
        if approved.shape == fresh.shape:
            diff    = np.abs(approved.astype(int) - fresh.astype(int))
            changed = (diff > 2).sum()
            check(f"pixel identical (changed={changed})",
                  changed == 0,
                  f"{changed} pixels changed by more than 2")
        else:
            check("image dimensions match", False,
                  f"approved={approved.shape} fresh={fresh.shape}")
except ImportError:
    check("golden master (PIL not available — install pillow)", False,
          "run: pip install pillow --break-system-packages")

print(f"\n{'='*56}")
print(f"  RESULTS: {PASS} passed   {FAIL} failed")
if FAIL == 0: print("  ALL PASSED - AtlasArrow ready for golden master")
else:         print("  FIX FAILURES before golden master")
print(f"{'='*56}\n")
sys.exit(0 if FAIL == 0 else 1)

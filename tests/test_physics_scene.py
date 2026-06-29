import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from atlas.api.scene import PhysicsScene, PhysicsSceneError

PASS = 0; FAIL = 0
os.makedirs("tests/golden", exist_ok=True)
_TMP = tempfile.gettempdir()

def check(name, ok, detail=""):
    global PASS, FAIL
    if ok: print(f"  v  {name}"); PASS += 1
    else:  print(f"  X  {name}  {detail}"); FAIL += 1

def section(t): print(f"\n{'-'*56}\n  {t}\n{'-'*56}")

def expect_err(desc, fn):
    try:
        fn(); check(f"should raise: {desc}", False, "no error")
    except PhysicsSceneError: check(f"catches: {desc}", True)
    except Exception as e:    check(f"catches: {desc}", False, str(e))

section("1 . All valid scenarios render without error")
scenarios = [
    ("floor_block",     {}),
    ("hanging_block",   {}),
    ("incline_block",   {"theta": 37}),
    ("incline_block",   {"theta": 45}),
    ("incline_block",   {"theta": 53}),
    ("stacked_2",       {}),
    ("stacked_3",       {}),
    ("incline_hanging", {"theta": 37}),
    ("atwood",          {}),
    ("floor_applied",   {"show_applied": True}),
]
for name, kwargs in scenarios:
    try:
        path = os.path.join(_TMP, f"test_{name}.png")
        PhysicsScene(name, U=0.6, **kwargs).render(path)
        check(f"{name} renders", os.path.exists(path))
    except Exception as e:
        check(f"{name} renders", False, str(e))

section("2 . Invalid scenario raises error")
expect_err("unknown scenario",
    lambda: PhysicsScene("flying_block", U=0.6).render(
        os.path.join(_TMP, "x.png")))

section("3 . Force toggles work")
PhysicsScene("floor_block", U=0.6,
             show_N=False, show_mg=False,
             show_friction=False).render(
    os.path.join(_TMP, "test_no_forces.png"))
check("no forces renders",
      os.path.exists(os.path.join(_TMP, "test_no_forces.png")))

PhysicsScene("floor_applied", U=0.6,
             show_applied=True).render(
    os.path.join(_TMP, "test_applied.png"))
check("applied force renders",
      os.path.exists(os.path.join(_TMP, "test_applied.png")))

section("4 . Different U values render correctly")
for U in [0.4, 0.6, 0.8]:
    try:
        PhysicsScene("floor_block", U=U).render(
            os.path.join(_TMP, f"test_U{U}.png"))
        check(f"floor_block at U={U}", True)
    except Exception as e:
        check(f"floor_block at U={U}", False, str(e))

section("5 . Different theta values for incline")
for theta in [30, 37, 45, 53]:
    try:
        PhysicsScene("incline_block", U=0.6,
                     theta=theta).render(
            os.path.join(_TMP, f"test_theta{theta}.png"))
        check(f"incline_block theta={theta}", True)
    except Exception as e:
        check(f"incline_block theta={theta}", False, str(e))

print(f"\n{'='*56}")
print(f"  RESULTS: {PASS} passed   {FAIL} failed")
if FAIL==0: print("  ALL PASSED - PhysicsScene ready to lock")
else:       print("  FIX FAILURES before locking")
print(f"{'='*56}\n")
sys.exit(0 if FAIL==0 else 1)

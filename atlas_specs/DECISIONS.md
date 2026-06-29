# Atlas Visual Engine — Design Decisions Log

## Section 1 – Architecture

_(populated as decisions are made)_

---

## Section 11 – Visual Philosophy

```
2026-06-27  Session 2  : VISUAL PHILOSOPHY FROZEN
  [FROZEN] Diagrams are never drawn to scale
  [FROZEN] Visual render angle = 20° always (looks clean and balanced)
  [FROZEN] Actual physics angle written as label only (θ, 37°, 53° etc)
  [FROZEN] Arrow lengths do not represent force magnitudes visually
  [FROZEN] Students read labels not visual proportions — JEE standard
  [FROZEN] This matches actual JEE diagram convention exactly
```

```
2026-06-29  Session 3  : AtlasRope LOCKED — golden master committed
  [FROZEN] ROPE_LW_OUTER_PT = 5.0   fixed pts
  [FROZEN] ROPE_LW_MID_PT   = 3.0   fixed pts
  [FROZEN] ROPE_LW_HI_PT    = 1.2   fixed pts
  [FROZEN] ROPE_HI_ALPHA    = 0.60
  [FROZEN] colors: #3D1F0A / #C87941 / #E8A84A
  [FROZEN] cap_style = round
  [FROZEN] rope.x2,y2 must equal block.top_cx, block.top_cy exactly
  [FROZEN] T arrow overlap with rope is a zorder issue not a rope bug
  [FROZEN] AtlasRope in atlas/visual/rope.py — DO NOT MODIFY
```

```
2026-06-27  Session 2  : AtlasFloor LOCKED — golden master committed
  [FROZEN] SURFACE_LW_PT = 2.0
  [FROZEN] HATCH_DEPTH_RATIO = 0.55
  [FROZEN] fill = #D1D5DB  alpha=0.55  hatch=#9CA3AF
  [FROZEN] side: bottom=floor top=ceiling left=left-wall right=right-wall
  [FROZEN] Wall block rotated 90deg — H/2 offset from wall not W/2
  [FROZEN] mg through floor is CORRECT FBD convention — not a bug
  [FROZEN] AtlasFloor in atlas/visual/floor.py — DO NOT MODIFY
```

```
2026-06-27  Session 2  : AtlasBlock LOCKED — golden master committed
  [FROZEN] BLOCK_W_RATIO  = 2.2
  [FROZEN] BLOCK_H_RATIO  = 1.4
  [FROZEN] BLOCK_RX_RATIO = 0.05
  [FROZEN] BLOCK_LW_PT    = 1.5
  [FROZEN] BLOCK_FILL     = #EFF6FF
  [FROZEN] BLOCK_BORDER   = #000000
  [FROZEN] Contact geometry: bottom_centre = cy - H/2 in normal direction
  [FROZEN] AtlasBlock in atlas/visual/block.py — DO NOT MODIFY
```

```
2026-06-27  Session 2  : AtlasArrow LOCKED — golden master committed
  [FROZEN] Arrow appearance locked in tests/golden/arrow_golden_master.png
  [FROZEN] HEAD fixed size = ARROW_HEAD_RATIO * ARROW_N_RATIO * U
  [FROZEN] SHAFT_LW = 2.0pt fixed
  [FROZEN] LABEL_SIZE = 12.0pt fixed
  [FROZEN] Label position = tip + dir*0.15*head_len + perp*0.20*U
  [FROZEN] AtlasArrow class in atlas/visual/arrow.py — DO NOT MODIFY
```

---

## Atlas Engineering Rules (AER)

```
[FROZEN] AER-001: Incline always rendered at 20° visual angle
         Physical angle communicated by label only

[FROZEN] AER-002: Physical angle ≠ rendered angle (never to scale)

[FROZEN] AER-003: Force arrow lengths are design tokens, not magnitudes
```

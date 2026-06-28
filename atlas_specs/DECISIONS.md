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

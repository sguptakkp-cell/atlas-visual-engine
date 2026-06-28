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

---

## Atlas Engineering Rules (AER)

```
[FROZEN] AER-001: Incline always rendered at 20° visual angle
         Physical angle communicated by label only

[FROZEN] AER-002: Physical angle ≠ rendered angle (never to scale)

[FROZEN] AER-003: Force arrow lengths are design tokens, not magnitudes
```

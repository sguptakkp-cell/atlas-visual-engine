# Atlas Visual Engine — Element Specification v2.0
# Incorporates third-party audit recommendations (ACP-P04)
# Status: DRAFT for approval
# Date: 2026-06-27

---

## ARCHITECTURAL DECISIONS

### What we adopt from the audit (immediately)
```
1. Separate geometry from rendering
   - geometry/ computes all math, returns dataclasses
   - elements/ only draws — receives geometry, never computes

2. Style objects instead of scattered constants
   - BlockStyle, ArrowStyle, FloorStyle, RopeStyle, CanvasStyle
   - Renderer asks style.width, style.fill — never imports raw constants

3. ForceArrow dataclass
   - draw_arrow(force_arrow) not draw_arrow(x,y,dx,dy,L,color,label)

4. Contact points on BlockGeometry
   - top_centre, bottom_centre, left_centre, right_centre, com
   - No more guessing where arrows start

5. Z-order policy — fully defined below

6. Label offset by perpendicular vector — works for ALL angles
```

### What we defer (Phase 2)
```
- Full scene system (scene.add().render()) — Phase 2
- Animation module — Phase 2
- OpenGL / Cairo / SVG renderer swap — Phase 2
- LaTeX text engine — Phase 2
```

### What we keep from v1.0 (frozen)
```
✅ Single base unit U = canvas_height / 10
✅ Arrow ratios HEAD=0.22, WIDTH=0.10, SHAFT_LW=0.28*U
✅ Force colors (FRS-v1.0)
✅ All mathematical ratios
✅ Enforcement rules
```

---

## PACKAGE STRUCTURE (revised)

```
atlas/
├── constants/
│   ├── colors.py        # force colors, palette — FRS-v1.0 locked
│   ├── typography.py    # fonts, sizes as multiples of U
│   ├── tokens.py        # U and all dimension ratios
│   └── __init__.py
│
├── styles/              # NEW — replaces scattered constants
│   ├── block_style.py   # BlockStyle dataclass
│   ├── arrow_style.py   # ArrowStyle dataclass
│   ├── floor_style.py   # FloorStyle dataclass
│   ├── rope_style.py    # RopeStyle dataclass
│   ├── canvas_style.py  # CanvasStyle dataclass
│   └── __init__.py
│
├── geometry/            # NEW — pure math, zero matplotlib
│   ├── vectors.py       # unit vector, perpendicular, rotate
│   ├── block_geo.py     # BlockGeometry dataclass
│   ├── incline_geo.py   # InclineGeometry dataclass
│   ├── arrow_geo.py     # ArrowGeometry dataclass
│   └── __init__.py
│
├── elements/            # drawing only — receives geometry + style
│   ├── block.py
│   ├── floor.py
│   ├── rope.py
│   ├── arrow.py
│   ├── incline.py
│   └── __init__.py
│
├── fbd/                 # high-level FBD API (existing, refactored)
│   ├── helpers.py       # fig_clean, save — thin wrappers
│   ├── diagrams/        # N3L001, N3L002 etc.
│   └── __init__.py
│
└── core/
    ├── canvas.py        # Canvas class
    ├── renderer.py      # Renderer — only thing that touches matplotlib
    └── __init__.py
```

---

## BASE UNIT

```python
# tokens.py
U = canvas_height / 10

# Example: canvas_height = 6.0 matplotlib units → U = 0.60
# Everything below is × U. Change U → entire diagram rescales.
```

---

## STYLE OBJECTS

### CanvasStyle
```python
@dataclass(frozen=True)
class CanvasStyle:
    width:      float = 8.0   # × U
    height:     float = 10.0  # × U
    width_incl: float = 12.0  # × U  (inclined plane)
    bg_color:   str   = "#FFFFFF"
    dpi_screen: int   = 200
    dpi_tablet: int   = 150
    dpi_print:  int   = 300
```

### BlockStyle
```python
@dataclass(frozen=True)
class BlockStyle:
    width:         float = 2.2   # × U
    height:        float = 1.4   # × U
    aspect_ratio:  float = 1.571 # width/height — locked
    corner_rx:     float = 0.08  # × U
    fill:          str   = "#EFF6FF"
    border_color:  str   = "#000000"
    border_lw:     float = 0.25  # × U → pts
    label_font:    str   = "DejaVu Serif"
    label_style:   str   = "italic"
    label_weight:  str   = "bold"
    label_size:    float = 1.6   # × U → pts
    label_color:   str   = "#1A2744"
    com_radius:    float = 0.08  # × U
    com_color:     str   = "#000000"
```

### ArrowStyle
```python
@dataclass(frozen=True)
class ArrowStyle:
    # Shaft — FIXED, never scales with arrow length
    shaft_lw:      float = 0.28  # × U → pts

    # Head — proportional to arrow length L
    head_ratio:    float = 0.22  # head_len = 0.22 × L
    width_ratio:   float = 0.10  # head_w   = 0.10 × L
    head_style:    str   = "filled_triangle"  # never open chevron

    # Arrow lengths — canvas relative (× U)
    len_N:         float = 2.5   # Normal force
    len_mg:        float = 2.0   # Weight
    len_T:         float = 2.3   # Tension
    len_f:         float = 1.8   # Friction
    len_F:         float = 1.8   # Applied

    # Label
    label_font:    str   = "DejaVu Serif"
    label_style:   str   = "italic"
    label_weight:  str   = "bold"
    label_size:    float = 2.0   # × U → pts
    label_gap:     float = 0.15  # × U (from arrowhead tip)
    # label position: perpendicular offset from arrow direction
    # works for ALL angles — no special cases
    label_offset:  float = 0.20  # × U perpendicular
```

### FloorStyle
```python
@dataclass(frozen=True)
class FloorStyle:
    contact_lw:    float = 0.30  # × U → pts
    contact_color: str   = "#000000"
    hatch_depth:   float = 0.55  # × U
    hatch_fill:    str   = "#D1D5DB"
    hatch_alpha:   float = 0.25
    hatch_color:   str   = "#6B7280"
    hatch_lw:      float = 1.1   # px (fixed — hatch is decorative)
    hatch_pattern: str   = "////"
    hatch_spacing: int   = 8     # px diagonal spacing
```

### RopeStyle
```python
@dataclass(frozen=True)
class RopeStyle:
    # 3 overlaid strokes — TikZ double stroke standard
    outer_color:   str   = "#3D1F0A"
    outer_lw:      float = 0.17  # × U
    mid_color:     str   = "#C87941"
    mid_lw:        float = 0.11  # × U
    hi_color:      str   = "#E8A84A"
    hi_lw:         float = 0.04  # × U
    hi_alpha:      float = 0.60
    cap_style:     str   = "round"
    length:        float = 3.50  # × U  (= 2.5 × BLOCK_H)
    ceiling_width: float = 5.50  # × U  (= 2.5 × BLOCK_W)
```

### InclineStyle
```python
@dataclass(frozen=True)
class InclineStyle:
    base:          float = 9.0   # × U
    fill:          str   = "#CBD5E1"
    fill_alpha:    float = 0.22
    hatch_pattern: str   = "////"
    border_lw:     float = 1.8   # pts (sides)
    slope_lw:      float = 2.5   # pts (contact surface — bolder)
    arc_radius:    float = 0.90  # × U — fixed, not relative to wedge
    arc_lw:        float = 0.20  # × U
    label_size:    float = 2.2   # × U → pts
    label_font:    str   = "DejaVu Serif"
    label_style:   str   = "italic"
    label_weight:  str   = "bold"
    label_color:   str   = "#000000"
    label_gap:     float = 0.30  # × U beyond arc radius
    block_pos_t:   float = 0.45  # 45% along slope from base
```

---

## GEOMETRY DATACLASSES

### BlockGeometry
```python
@dataclass
class BlockGeometry:
    # All positions in matplotlib world coordinates
    centre:         tuple  # (cx, cy)
    top_centre:     tuple  # (cx, cy + H/2)
    bottom_centre:  tuple  # (cx, cy - H/2)
    left_centre:    tuple  # (cx - W/2, cy)
    right_centre:   tuple  # (cx + W/2, cy)
    com:            tuple  # same as centre for uniform block
    corners:        list   # [(x0,y0),(x1,y0),(x1,y1),(x0,y1)] CW
    width:          float
    height:         float
    rotation_deg:   float  # 0 for flat, theta for inclined
```

### InclineGeometry
```python
@dataclass
class InclineGeometry:
    # Wedge corners
    A:              tuple  # bottom-left (angle theta here)
    B:              tuple  # bottom-right (right angle)
    C:              tuple  # top-right (apex)
    base:           float
    height:         float
    slope_len:      float
    theta_deg:      float
    # Unit vectors
    slope_vec:      tuple  # (cos θ, sin θ) — up the slope
    normal_vec:     tuple  # (-sin θ, cos θ) — away from surface
    # Block
    block_anchor:   tuple  # P — point on slope where block sits
    block_centre:   tuple  # C_block — lifted by BLOCK_H/2
    # Arc
    arc_center:     tuple  # = A
    arc_radius:     float
    label_pos:      tuple  # computed from arc bisector
```

### ArrowGeometry
```python
@dataclass
class ArrowGeometry:
    tail:           tuple  # start point
    head_tip:       tuple  # arrow tip
    shaft_end:      tuple  # where shaft ends, head begins
    head_base_1:    tuple  # head triangle point 1
    head_base_2:    tuple  # head triangle point 2
    direction:      tuple  # unit vector
    length:         float
    head_len:       float  # = HEAD_RATIO × length
    head_width:     float  # = WIDTH_RATIO × length
    perp:           tuple  # perpendicular unit vector
    label_pos:      tuple  # computed from tip + perpendicular offset
```

---

## GEOMETRY FUNCTIONS (pure math — no matplotlib)

```python
# vectors.py
def unit_vector(dx, dy) -> tuple
def perpendicular(dx, dy) -> tuple   # 90° CCW rotation
def rotate_vec(dx, dy, theta_deg) -> tuple

# block_geo.py
def compute_block(cx, cy, U, style: BlockStyle,
                  rotation_deg=0) -> BlockGeometry

# incline_geo.py
def compute_incline(theta_deg, x0, y0,
                    U, block_style: BlockStyle,
                    incline_style: InclineStyle) -> InclineGeometry

# arrow_geo.py
def compute_arrow(tail, direction, length, U,
                  style: ArrowStyle) -> ArrowGeometry
```

---

## DRAWING FUNCTIONS (rendering only — no math)

```python
# block.py
def draw_block(ax, geo: BlockGeometry,
               style: BlockStyle, label="") -> None
# Draws rectangle at geo.centre, rotated geo.rotation_deg
# Draws CoM dot at geo.com

# floor.py
def draw_floor(ax, y, x_start, x_end,
               style: FloorStyle) -> None
def draw_ceiling(ax, y, x_start, x_end,
                 style: FloorStyle) -> None
def draw_wall(ax, x, y_start, y_end,
              side="left", style: FloorStyle) -> None

# rope.py
def draw_rope(ax, x1, y1, x2, y2,
              style: RopeStyle) -> None
# 3 overlaid strokes — cylindrical rope look

# arrow.py
def draw_arrow(ax, geo: ArrowGeometry,
               color: str, label="",
               style: ArrowStyle) -> None
# Draws shaft line + filled triangle head
# Draws label at geo.label_pos
# Never computes anything — only renders geo

# incline.py
def draw_incline(ax, geo: InclineGeometry,
                 style: InclineStyle) -> None
# Draws wedge polygon + hatch + borders + angle arc + theta label
```

---

## Z-ORDER POLICY (frozen)

```
zorder 1  : floor / wall / ceiling hatch fill
zorder 2  : floor / wall / ceiling contact line
zorder 3  : rope / string
zorder 4  : inclined plane wedge fill + hatch
zorder 5  : inclined plane borders
zorder 6  : block fill
zorder 7  : block border
zorder 8  : CoM dot
zorder 9  : force arrow shafts
zorder 10 : force arrow heads (triangles)
zorder 11 : force labels
zorder 12 : angle arc
zorder 13 : angle label (theta)
zorder 14 : annotations / notes
```

---

## COORDINATE SYSTEM

```
World coordinates  : matplotlib axes units
                     +x = right, +y = up (standard math)
                     Origin = bottom-left of canvas

Canvas coordinates : pixels at given DPI
                     computed at save time only

Object-local coords: used only inside geometry functions
                     for block: origin at block centre
                     for incline: origin at corner A
                     Converted to world coords before returning
```

---

## RENDERING TOLERANCES

```
Floating point     : all geometry in float64
Minimum line width : 0.5pt (below this is invisible at 200dpi)
DPI scaling        : all pt values × (DPI/72) at export
Anti-aliasing      : matplotlib default (on)
Minimum arrow len  : 0.5*U (below this do not draw head)
Minimum font size  : 6pt (below this do not render label)
```

---

## ENFORCEMENT RULES (unchanged from v1.0 + additions)

```
1. draw_arrow() is the ONLY function that draws force arrows. EVER.
2. draw_block() is the ONLY function that draws blocks. EVER.
3. compute_* functions never touch matplotlib. EVER.
4. draw_* functions never compute geometry. EVER.
5. All dimensions computed from U. No hardcoded numbers. EVER.
6. HEAD=0.22×L, WIDTH=0.10×L, SHAFT_LW=0.28*U — FROZEN.
7. Arc radius = 0.9*U — FROZEN. Not relative to wedge size.
8. Theta label font = 2.2*U — FROZEN.
9. Block on slope: lift = BLOCK_H/2 in normal direction — FROZEN.
10. Z-order as defined above — FROZEN.
```

---

## WHAT REMAINS UNSPECCED (future sessions, same procedure)

```
Phase 2 — study each before speccing:
  - Pulley and wheel geometry
  - Person / human figure
  - Spring element
  - Multiple simultaneous forces (offset rules)
  - Scene system (FBDScene class)

Phase 3:
  - Chemistry diagrams (completely different standard)
  - Mathematics graphs
  - Animation frames
```


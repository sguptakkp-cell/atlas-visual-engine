"""
Atlas Constants - Tokens
========================
H = BLOCK_H_RATIO * U is the master reference.
Every dimension derives from H.
Two types of values:
  H-relative: positions, lengths, radii = ratio * H
  Fixed pts:  linewidths, font sizes = fixed number
STATUS: FROZEN
"""

# Base unit
BLOCK_H_RATIO = 1.0    # H = BLOCK_H_RATIO * U = master reference

# Block (relative to H)
BLOCK_W_RATIO  = 1.6   # W = 1.6 * H  (aspect ratio 1.6:1)
BLOCK_RX_RATIO = 0.03  # corner radius = 0.03 * H
BLOCK_LW_PT    = 1.5   # border linewidth — fixed pts

# CoM dot
COM_R_RATIO = 0.06     # radius = 0.06 * H

# Arrow lengths (relative to H)
ARROW_N_H_RATIO   = 1.8
ARROW_MG_H_RATIO  = 1.6
ARROW_T_H_RATIO   = 1.8
ARROW_F_H_RATIO   = 1.2
ARROW_APP_H_RATIO = 1.5

ARROW_LENGTHS = {
    "N":  ARROW_N_H_RATIO,
    "mg": ARROW_MG_H_RATIO,
    "T":  ARROW_T_H_RATIO,
    "f":  ARROW_F_H_RATIO,
    "F":  ARROW_APP_H_RATIO,
}

# Arrowhead (relative to L — arrow length)
ARROW_HEAD_RATIO  = 0.22   # head_len   = 0.22 * L — FROZEN
ARROW_WIDTH_RATIO = 0.10   # head_width = 0.10 * L — FROZEN

# Arrow visual — fixed pts
ARROW_SHAFT_LW_PT     = 2.0   # shaft linewidth — fixed pts
ARROW_LABEL_SIZE_PT   = 12.0  # label font size — fixed pts
ARROW_LABEL_OFFSET_PT = 10.0  # label gap from tip — fixed pts

# Surface / Floor
SURFACE_LW_PT     = 2.0   # contact line — fixed pts
HATCH_DEPTH_RATIO = 0.55  # hatch depth = 0.55 * U (not H)

# Rope — fixed pts
ROPE_LW_OUTER_PT = 5.0
ROPE_LW_MID_PT   = 3.0
ROPE_LW_HI_PT    = 1.2
ROPE_HI_ALPHA    = 0.60
ROPE_HANG_H_RATIO= 2.5   # hanging rope = 2.5 * H

# Incline
INCLINE_BASE_RATIO       = 9.0    # base = 9.0 * U
INCLINE_RENDER_ANGLE_DEG = 20.0   # always 20 — AER-001
INCLINE_SLOPE_LW_PT      = 2.5    # fixed pts
INCLINE_BORDER_LW_PT     = 1.5    # fixed pts
INCLINE_FILL_ALPHA       = 0.22
INCLINE_LABEL_ANGLE_DEG  = 20.0
INCLINE_LABEL_DIST_RATIO = 1.5    # * arc_radius
INCLINE_ANGLE_LABEL      = "θ"
ARC_RADIUS_H_RATIO       = 0.80   # arc radius = 0.80 * H
ARC_LW_PT                = 2.0    # fixed pts
ARC_LABEL_SIZE_PT        = 16.0   # fixed pts
BLOCK_POS_T              = 0.45   # 45% along slope

# Stacked blocks
STACK_2_H = 0.75   # height_scale for n=2
STACK_3_H = 0.60   # height_scale for n=3
STACK_2_W = 2.0    # width_scale for bottom of n=2
STACK_3_W = 3.0    # width_scale for bottom of n=3

# Canvas (relative to H per scenario)
CANVAS_SCENARIO = {
    "floor_only":       {"W": 8.0,  "H": 6.0},
    "hanging_only":     {"W": 4.0,  "H": 8.0},
    "incline_only":     {"W": 12.0, "H": 6.0},
    "floor_hanging":    {"W": 10.0, "H": 7.0},
    "atwood":           {"W": 5.0,  "H": 10.0},
    "incline_hanging":  {"W": 14.0, "H": 7.0},
}

# Export
DPI_SCREEN  = 150
DPI_PRINT   = 300
DPI_PREVIEW = 72
IMAGE_W_PX  = 800
IMAGE_H_PX  = 600

# Z-order (frozen)
Z_GROUND_HATCH   =  1
Z_GROUND_LINE    =  2
Z_ROPE           =  3
Z_INCLINE_FILL   =  4
Z_INCLINE_BORDER =  5
Z_BLOCK_FILL     =  6
Z_BLOCK_BORDER   =  7
Z_COM_DOT        =  8
Z_ARROW_SHAFT    =  9
Z_ARROW_HEAD     = 10
Z_FORCE_LABEL    = 11
Z_ANGLE_ARC      = 12
Z_ANGLE_LABEL    = 13
Z_ANNOTATION     = 14

# Font
FONT_FAMILY = "DejaVu Serif"
FONT_STYLE  = "italic"
FONT_WEIGHT = "bold"

def get_H(U):
    """Return block height H from base unit U."""
    return BLOCK_H_RATIO * U

def compute_canvas(scenario, U):
    """Return (width, height) in matplotlib units for a scenario."""
    H = get_H(U)
    dims = CANVAS_SCENARIO.get(scenario, {"W": 8.0, "H": 6.0})
    return dims["W"] * H, dims["H"] * H

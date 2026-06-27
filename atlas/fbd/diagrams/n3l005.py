"""
N3L005 — Block on 37-degree inclined surface: FBD variants.

Generates 5 PNG files into n3l_diagrams/:
  N3L005_situation.png          — block on incline, no forces
  N3L005_option0_correct.png    — W straight down (green), N perpendicular to surface (blue, 127°)
  N3L005_option1_wrong_E04.png  — N drawn straight up instead of perpendicular (E04)
  N3L005_option2_wrong_E02.png  — only W shown, N missing (E02)
  N3L005_option3_wrong_E03.png  — only N shown, W missing (E03)
"""

import sys
import os
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches

from atlas.fbd.helpers import fig_clean, draw_force, save
from atlas.constants.colors import (
    COLOR_WEIGHT, COLOR_NORMAL, COLOR_OBJECT, COLOR_GROUND,
    COLOR_SLATE, COLOR_NAVY,
)
from atlas.constants.dimensions import (
    BLOCK_WIDTH, BLOCK_HEIGHT, OBJECT_BORDER_WIDTH, GROUND_BORDER_WIDTH,
)
from atlas.constants.typography import (
    FONT_FAMILY, FONT_SIZE_OBJECT, FONT_WEIGHT_OBJECT,
)

# ------------------------------------------------------------------
# Incline geometry  (all in data coordinates)
# ------------------------------------------------------------------

ANGLE_DEG = 37
_ang  = math.radians(ANGLE_DEG)
_COS  = math.cos(_ang)   # ≈ 0.7986
_SIN  = math.sin(_ang)   # ≈ 0.6018

# Incline: right-triangle wedge with hypotenuse rising left→right at 37°
#   A = lower-left corner of hypotenuse (start of incline surface)
#   B = upper-right end of hypotenuse
#   C = directly below B at floor level (right-angle corner)
INCLINE_AX, INCLINE_AY = 0.8, 0.5
INCLINE_LEN = 2.5

INCLINE_BX = INCLINE_AX + INCLINE_LEN * _COS   # ≈ 2.797
INCLINE_BY = INCLINE_AY + INCLINE_LEN * _SIN   # ≈ 2.005
INCLINE_CX = INCLINE_BX                         # right-angle corner x
INCLINE_CY = INCLINE_AY                         # right-angle corner y (floor level)

# Block contact point on incline surface (d=1.5 from A)
_CONTACT_D = 1.5
_CONTACT_X = INCLINE_AX + _CONTACT_D * _COS    # ≈ 1.998
_CONTACT_Y = INCLINE_AY + _CONTACT_D * _SIN    # ≈ 1.403

# Block centre: BH/2 along outward normal from contact
# Outward normal to incline = (-sin37, cos37)
_OUT_X = -_SIN    # ≈ -0.6018
_OUT_Y =  _COS    # ≈  0.7986
BW, BH = BLOCK_WIDTH, BLOCK_HEIGHT
BCX = _CONTACT_X + (BH / 2) * _OUT_X   # ≈ 1.757
BCY = _CONTACT_Y + (BH / 2) * _OUT_Y   # ≈ 1.722

# Normal force direction: perpendicular to incline, pointing outward = 37+90 = 127°
N_ANGLE = ANGLE_DEG + 90   # 127°

ARROW_LEN = 0.9


# ------------------------------------------------------------------
# Local helpers
# ------------------------------------------------------------------

def _draw_incline_wedge(ax):
    """Draw the right-triangle wedge representing the inclined surface."""
    wedge = mpatches.Polygon(
        [(INCLINE_AX, INCLINE_AY),
         (INCLINE_BX, INCLINE_BY),
         (INCLINE_CX, INCLINE_CY)],
        closed=True,
        facecolor=COLOR_GROUND,
        edgecolor=COLOR_SLATE,
        linewidth=GROUND_BORDER_WIDTH,
        hatch="////",
        zorder=1,
    )
    ax.add_patch(wedge)


def _draw_incline_block(ax, label=""):
    """Draw a block rotated to sit flush on the incline."""
    along = (_COS, _SIN)
    outward = (_OUT_X, _OUT_Y)

    corners = []
    for sa, sp in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
        x = BCX + sa * (BW / 2) * along[0] + sp * (BH / 2) * outward[0]
        y = BCY + sa * (BW / 2) * along[1] + sp * (BH / 2) * outward[1]
        corners.append((x, y))

    block = mpatches.Polygon(
        corners,
        closed=True,
        facecolor=COLOR_OBJECT,
        edgecolor=COLOR_NAVY,
        linewidth=OBJECT_BORDER_WIDTH,
        zorder=3,
    )
    ax.add_patch(block)
    if label:
        ax.text(BCX, BCY, label,
                ha="center", va="center",
                fontsize=FONT_SIZE_OBJECT, fontweight=FONT_WEIGHT_OBJECT,
                fontfamily=FONT_FAMILY, color=COLOR_NAVY, zorder=4)


def _setup_ax(ax):
    ax.set_xlim(0.0, 4.0)
    ax.set_ylim(0.0, 4.0)


def _draw_scene(ax):
    _draw_incline_wedge(ax)
    _draw_incline_block(ax, label="Block")


# ------------------------------------------------------------------
# Diagram generators
# ------------------------------------------------------------------

def make_situation():
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    return save(fig, "N3L005_situation.png")


def make_option0_correct():
    """W straight down, N perpendicular to incline surface (127°)."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, BCX, BCY, angle_deg=270,     color=COLOR_WEIGHT, label="W", length=ARROW_LEN)
    draw_force(ax, BCX, BCY, angle_deg=N_ANGLE, color=COLOR_NORMAL, label="N", length=ARROW_LEN)
    return save(fig, "N3L005_option0_correct.png")


def make_option1_wrong_E04():
    """E04 — N drawn straight up (90°) instead of perpendicular to surface (127°)."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, BCX, BCY, angle_deg=270, color=COLOR_WEIGHT, label="W", length=ARROW_LEN)
    draw_force(ax, BCX, BCY, angle_deg=90,  color=COLOR_NORMAL, label="N", length=ARROW_LEN)
    return save(fig, "N3L005_option1_wrong_E04.png")


def make_option2_wrong_E02():
    """E02 — only W shown; normal force missing."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, BCX, BCY, angle_deg=270, color=COLOR_WEIGHT, label="W", length=ARROW_LEN)
    return save(fig, "N3L005_option2_wrong_E02.png")


def make_option3_wrong_E03():
    """E03 — only N shown; weight missing."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, BCX, BCY, angle_deg=N_ANGLE, color=COLOR_NORMAL, label="N", length=ARROW_LEN)
    return save(fig, "N3L005_option3_wrong_E03.png")


if __name__ == "__main__":
    outputs = [
        make_situation(),
        make_option0_correct(),
        make_option1_wrong_E04(),
        make_option2_wrong_E02(),
        make_option3_wrong_E03(),
    ]
    for path in outputs:
        print(f"Saved: {path}")

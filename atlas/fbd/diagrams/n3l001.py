"""
N3L001 — Block on a floor: Free Body Diagram variants.

Generates 5 PNG files into n3l_diagrams/:
  N3L001_situation.png          — block on floor, no forces
  N3L001_option0_correct.png    — mg down (green, from COM), N up (blue, from bottom edge)
  N3L001_option1_wrong_E03.png  — only N shown (missing weight)
  N3L001_option2_wrong_E02.png  — only mg shown (missing normal)
  N3L001_option3_wrong_E04.png  — mg up, N down (wrong directions)
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import matplotlib
matplotlib.use("Agg")

from atlas.fbd.helpers import fig_clean, draw_block, draw_floor, draw_force, save
from atlas.constants.colors import COLOR_WEIGHT, COLOR_NORMAL
from atlas.constants.dimensions import BLOCK_WIDTH, BLOCK_HEIGHT, ARROW_LENGTH

# ------------------------------------------------------------------
# Scene geometry (uses current constants so dimensions stay in sync)
# ------------------------------------------------------------------

CX, CY   = 2.0, 1.9            # block centre
BW, BH   = BLOCK_WIDTH, BLOCK_HEIGHT    # 1.4 × 0.9
FLOOR_Y  = CY - BH / 2         # 1.9 − 0.45 = 1.45  (block bottom = floor surface)
FLOOR_X  = 0.5
FLOOR_W  = 3.0
ARROW_LEN = ARROW_LENGTH        # 1.1


def _setup_ax(ax):
    ax.set_xlim(0.0, 4.0)
    ax.set_ylim(0.0, 4.0)


def _draw_scene(ax):
    draw_floor(ax, FLOOR_X, FLOOR_Y, width=FLOOR_W)
    draw_block(ax, CX, CY, width=BW, height=BH)


def make_situation():
    fig, ax = fig_clean(6, 5)
    _setup_ax(ax)
    _draw_scene(ax)
    return save(fig, "N3L001_situation.png")


def make_option0_correct():
    fig, ax = fig_clean(6, 5)
    _setup_ax(ax)
    _draw_scene(ax)
    # N: contact force — tail at bottom edge (origin_point="edge")
    draw_force(ax, CX, CY, angle_deg=90,  color=COLOR_NORMAL, label="N",
               length=ARROW_LEN, origin_point="edge")
    # mg: body force — tail at centre of mass (origin_point="centre")
    draw_force(ax, CX, CY, angle_deg=270, color=COLOR_WEIGHT, label="mg",
               length=ARROW_LEN, origin_point="centre")
    return save(fig, "N3L001_option0_correct.png")


def make_option1_wrong_E03():
    """E03 — missing weight (only N shown)."""
    fig, ax = fig_clean(6, 5)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, CX, CY, angle_deg=90, color=COLOR_NORMAL, label="N",
               length=ARROW_LEN, origin_point="edge")
    return save(fig, "N3L001_option1_wrong_E03.png")


def make_option2_wrong_E02():
    """E02 — missing normal (only mg shown)."""
    fig, ax = fig_clean(6, 5)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, CX, CY, angle_deg=270, color=COLOR_WEIGHT, label="mg",
               length=ARROW_LEN, origin_point="centre")
    return save(fig, "N3L001_option2_wrong_E02.png")


def make_option3_wrong_E04():
    """E04 — wrong directions: mg up, N down."""
    fig, ax = fig_clean(6, 5)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, CX, CY, angle_deg=90,  color=COLOR_WEIGHT, label="mg",
               length=ARROW_LEN, origin_point="centre")
    draw_force(ax, CX, CY, angle_deg=270, color=COLOR_NORMAL, label="N",
               length=ARROW_LEN, origin_point="edge")
    return save(fig, "N3L001_option3_wrong_E04.png")


if __name__ == "__main__":
    outputs = [
        make_situation(),
        make_option0_correct(),
        make_option1_wrong_E03(),
        make_option2_wrong_E02(),
        make_option3_wrong_E04(),
    ]
    for path in outputs:
        print(f"Saved: {path}")

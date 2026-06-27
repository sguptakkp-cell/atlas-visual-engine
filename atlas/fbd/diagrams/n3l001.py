"""
N3L001 — Block on a floor: Free Body Diagram variants.

Generates 5 PNG files into n3l_diagrams/:
  N3L001_situation.png        — block on floor, no forces
  N3L001_option0_correct.png  — W down (green), N up (blue)
  N3L001_option1_wrong_E03.png — only N shown (missing weight)
  N3L001_option2_wrong_E02.png — only W shown (missing normal)
  N3L001_option3_wrong_E04.png — W up, N down (wrong directions)
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import matplotlib
matplotlib.use("Agg")

from atlas.fbd.helpers import fig_clean, draw_block, draw_ground, draw_force, save
from atlas.constants.colors import COLOR_WEIGHT, COLOR_NORMAL

# ------------------------------------------------------------------
# Scene geometry (all values in data coordinates)
# ------------------------------------------------------------------

CX, CY = 2.0, 1.9          # block center
BW, BH = 1.2, 0.8          # block width, height
FLOOR_X = 0.5              # floor left edge
FLOOR_Y = CY - BH / 2     # floor top = block bottom
FLOOR_W = 3.0
ARROW_LEN = 0.9


def _setup_ax(ax):
    ax.set_xlim(0.0, 4.0)
    ax.set_ylim(0.0, 4.0)


def _draw_scene(ax):
    draw_ground(ax, FLOOR_X, FLOOR_Y, width=FLOOR_W, direction="floor")
    draw_block(ax, CX, CY, width=BW, height=BH, label="Block")


def make_situation():
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    return save(fig, "N3L001_situation.png")


def make_option0_correct():
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, CX, CY, angle_deg=90,  color=COLOR_NORMAL, label="N", length=ARROW_LEN)
    draw_force(ax, CX, CY, angle_deg=270, color=COLOR_WEIGHT, label="W", length=ARROW_LEN)
    return save(fig, "N3L001_option0_correct.png")


def make_option1_wrong_E03():
    """E03 — missing weight (only normal force shown)."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, CX, CY, angle_deg=90, color=COLOR_NORMAL, label="N", length=ARROW_LEN)
    return save(fig, "N3L001_option1_wrong_E03.png")


def make_option2_wrong_E02():
    """E02 — missing normal (only weight shown)."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, CX, CY, angle_deg=270, color=COLOR_WEIGHT, label="W", length=ARROW_LEN)
    return save(fig, "N3L001_option2_wrong_E02.png")


def make_option3_wrong_E04():
    """E04 — wrong directions: W up, N down."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, CX, CY, angle_deg=90,  color=COLOR_WEIGHT, label="W", length=ARROW_LEN)
    draw_force(ax, CX, CY, angle_deg=270, color=COLOR_NORMAL, label="N", length=ARROW_LEN)
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

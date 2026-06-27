"""
N3L004 — Hanging block (tension + weight): FBD variants.

Generates 5 PNG files into n3l_diagrams/:
  N3L004_situation.png          — block hanging from ceiling by string, no forces
  N3L004_option0_correct.png    — T up (red), W down (green) on block
  N3L004_option1_wrong_E07.png  — only W shown, T missing (E07)
  N3L004_option2_wrong_E03.png  — only T shown, W missing (E03)
  N3L004_option3_wrong_E04.png  — T down, W up (wrong directions) (E04)
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches

from atlas.fbd.helpers import (
    fig_clean, draw_block, draw_string, draw_force, save,
)
from atlas.constants.colors import (
    COLOR_WEIGHT, COLOR_TENSION, COLOR_GROUND, COLOR_SLATE,
)
from atlas.constants.dimensions import GROUND_BORDER_WIDTH, BLOCK_HEIGHT

# ------------------------------------------------------------------
# Scene geometry
# ------------------------------------------------------------------

BW, BH = 1.2, 0.8

# Ceiling surface (bottom face of ceiling slab)
CEIL_Y    = 3.2
CEIL_X    = 0.5
CEIL_W    = 3.0
CEIL_SLAB = 0.2          # height of the ceiling slab drawn above CEIL_Y

# Block hanging below ceiling
BCX, BCY = 2.0, 2.0      # block centre; block spans y=[1.6, 2.4]
BLOCK_TOP_Y = BCY + BH / 2   # = 2.4

ARROW_LEN = 0.9
_DX = 0.2


def _draw_ceiling(ax):
    slab = mpatches.Rectangle(
        (CEIL_X, CEIL_Y), CEIL_W, CEIL_SLAB,
        facecolor=COLOR_GROUND,
        edgecolor=COLOR_SLATE,
        linewidth=GROUND_BORDER_WIDTH,
        hatch="////",
        zorder=1,
    )
    ax.add_patch(slab)


def _setup_ax(ax):
    ax.set_xlim(0.0, 4.0)
    ax.set_ylim(0.0, 4.0)


def _draw_scene(ax):
    _draw_ceiling(ax)
    draw_string(ax, BCX, CEIL_Y, BCX, BLOCK_TOP_Y)
    draw_block(ax, BCX, BCY, width=BW, height=BH, label="Block")


def make_situation():
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    return save(fig, "N3L004_situation.png")


def make_option0_correct():
    """T↑ (red) and W↓ (green) on hanging block."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, BCX, BCY, angle_deg=90,  color=COLOR_TENSION, label="T", length=ARROW_LEN)
    draw_force(ax, BCX, BCY, angle_deg=270, color=COLOR_WEIGHT,  label="W", length=ARROW_LEN)
    return save(fig, "N3L004_option0_correct.png")


def make_option1_wrong_E07():
    """E07 — only W shown; tension missing."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, BCX, BCY, angle_deg=270, color=COLOR_WEIGHT, label="W", length=ARROW_LEN)
    return save(fig, "N3L004_option1_wrong_E07.png")


def make_option2_wrong_E03():
    """E03 — only T shown; weight missing."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, BCX, BCY, angle_deg=90, color=COLOR_TENSION, label="T", length=ARROW_LEN)
    return save(fig, "N3L004_option2_wrong_E03.png")


def make_option3_wrong_E04():
    """E04 — T downward, W upward (wrong directions); offset to separate."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, BCX - _DX, BCY, angle_deg=270, color=COLOR_TENSION, label="T", length=ARROW_LEN)
    draw_force(ax, BCX + _DX, BCY, angle_deg=90,  color=COLOR_WEIGHT,  label="W", length=ARROW_LEN)
    return save(fig, "N3L004_option3_wrong_E04.png")


if __name__ == "__main__":
    outputs = [
        make_situation(),
        make_option0_correct(),
        make_option1_wrong_E07(),
        make_option2_wrong_E03(),
        make_option3_wrong_E04(),
    ]
    for path in outputs:
        print(f"Saved: {path}")

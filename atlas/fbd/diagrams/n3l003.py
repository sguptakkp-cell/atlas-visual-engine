"""
N3L003 — Earth–Person gravity action-reaction pair: FBD variants.

Generates 5 PNG files into n3l_diagrams/:
  N3L003_situation.png          — person (ball) on earth (floor), no forces
  N3L003_option0_correct.png    — W_p down on person; W_e up on earth (correct pair)
  N3L003_option1_wrong_E05.png  — both arrows on person only (E05)
  N3L003_option2_wrong_E03.png  — only W_p shown, reaction missing (E03)
  N3L003_option3_wrong_E04.png  — W_p upward on person, W_e downward on earth (E04)
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import matplotlib
matplotlib.use("Agg")

from atlas.fbd.helpers import (
    fig_clean, draw_ball, draw_ground, draw_force, save,
)
from atlas.constants.colors import COLOR_WEIGHT

# ------------------------------------------------------------------
# Scene geometry
# ------------------------------------------------------------------

BALL_R = 0.35

FLOOR_Y = 1.45
FLOOR_X = 0.5
FLOOR_W = 3.0

# Person (ball): bottom touches floor
PCX, PCY = 2.0, FLOOR_Y + BALL_R   # = (2.0, 1.80)

# Earth reaction force anchor — offset right to avoid overlap with person
EARTH_FX, EARTH_FY = 2.8, FLOOR_Y

ARROW_LEN = 0.9
ARROW_LEN_SHORT = 0.7


def _setup_ax(ax):
    ax.set_xlim(0.0, 4.0)
    ax.set_ylim(0.0, 4.0)


def _draw_scene(ax):
    draw_ground(ax, FLOOR_X, FLOOR_Y, width=FLOOR_W, direction="floor")
    draw_ball(ax, PCX, PCY, radius=BALL_R)


def make_situation():
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    return save(fig, "N3L003_situation.png")


def make_option0_correct():
    """W_p↓ on person; W_e↑ on earth — correct action-reaction pair."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, PCX,     PCY,     angle_deg=270, color=COLOR_WEIGHT, label="W_p", length=ARROW_LEN)
    draw_force(ax, EARTH_FX, EARTH_FY, angle_deg=90, color=COLOR_WEIGHT, label="W_e", length=ARROW_LEN)
    return save(fig, "N3L003_option0_correct.png")


def make_option1_wrong_E05():
    """E05 — both W_p and W_e placed on person (incorrect pair placement)."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, PCX - 0.2, PCY, angle_deg=270, color=COLOR_WEIGHT, label="W_p", length=ARROW_LEN)
    draw_force(ax, PCX + 0.2, PCY, angle_deg=90,  color=COLOR_WEIGHT, label="W_e", length=ARROW_LEN)
    return save(fig, "N3L003_option1_wrong_E05.png")


def make_option2_wrong_E03():
    """E03 — only W_p shown; reaction on earth missing."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, PCX, PCY, angle_deg=270, color=COLOR_WEIGHT, label="W_p", length=ARROW_LEN)
    return save(fig, "N3L003_option2_wrong_E03.png")


def make_option3_wrong_E04():
    """E04 — W_p upward on person; W_e downward on earth (wrong directions)."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, PCX,     PCY,     angle_deg=90,  color=COLOR_WEIGHT, label="W_p", length=ARROW_LEN)
    draw_force(ax, EARTH_FX, EARTH_FY, angle_deg=270, color=COLOR_WEIGHT, label="W_e", length=ARROW_LEN_SHORT)
    return save(fig, "N3L003_option3_wrong_E04.png")


if __name__ == "__main__":
    outputs = [
        make_situation(),
        make_option0_correct(),
        make_option1_wrong_E05(),
        make_option2_wrong_E03(),
        make_option3_wrong_E04(),
    ]
    for path in outputs:
        print(f"Saved: {path}")

"""
N3L002 — Stacked blocks (Block A on Block B, Block B on floor): FBD variants.

Generates 5 PNG files into n3l_diagrams/:
  N3L002_situation.png          — two stacked blocks on floor, no forces
  N3L002_option0_correct.png    — FBD of B: W_B down, N_f up, N_A down
  N3L002_option1_wrong_E01.png  — N_A drawn upward instead of downward (E01)
  N3L002_option2_wrong_E08.png  — forces drawn on Block A instead of B (E08)
  N3L002_option3_wrong_E10.png  — N_A upward equal to N_f, violating N3L (E10)
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import matplotlib
matplotlib.use("Agg")

from atlas.fbd.helpers import fig_clean, draw_block, draw_ground, draw_force, save
from atlas.constants.colors import COLOR_WEIGHT, COLOR_NORMAL

# ------------------------------------------------------------------
# Scene geometry
# ------------------------------------------------------------------

BW, BH = 1.2, 0.8

# Floor
FLOOR_Y = 1.0
FLOOR_X = 0.5
FLOOR_W = 3.0

# Block B (bottom)
BCX, BCY = 2.0, 1.4          # cy = FLOOR_Y + BH/2

# Block A (top)
ACX, ACY = 2.0, 2.2          # cy = BCY + BH

ARROW_LEN = 0.9

# x-offsets to separate co-directional arrows
_DX = 0.2


def _setup_ax(ax):
    ax.set_xlim(0.0, 4.0)
    ax.set_ylim(0.0, 4.0)


def _draw_scene(ax):
    draw_ground(ax, FLOOR_X, FLOOR_Y, width=FLOOR_W, direction="floor")
    draw_block(ax, BCX, BCY, width=BW, height=BH, label="B")
    draw_block(ax, ACX, ACY, width=BW, height=BH, label="A")


def make_situation():
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    return save(fig, "N3L002_situation.png")


def make_option0_correct():
    """FBD of Block B: W_B↓ + N_f↑ + N_A↓ (A pushes down on B)."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, BCX,        BCY, angle_deg=90,  color=COLOR_NORMAL, label="N_f", length=ARROW_LEN)
    draw_force(ax, BCX - _DX, BCY, angle_deg=270, color=COLOR_WEIGHT, label="W_B", length=ARROW_LEN)
    draw_force(ax, BCX + _DX, BCY, angle_deg=270, color=COLOR_NORMAL, label="N_A", length=ARROW_LEN)
    return save(fig, "N3L002_option0_correct.png")


def make_option1_wrong_E01():
    """E01 — N_A drawn upward instead of downward (same-object interaction error)."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, BCX - _DX, BCY, angle_deg=90,  color=COLOR_NORMAL, label="N_f", length=ARROW_LEN)
    draw_force(ax, BCX + _DX, BCY, angle_deg=90,  color=COLOR_NORMAL, label="N_A", length=ARROW_LEN)
    draw_force(ax, BCX,        BCY, angle_deg=270, color=COLOR_WEIGHT, label="W_B", length=ARROW_LEN)
    return save(fig, "N3L002_option1_wrong_E01.png")


def make_option2_wrong_E08():
    """E08 — forces shown on Block A (wrong object) instead of Block B."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, ACX,        ACY, angle_deg=90,  color=COLOR_NORMAL, label="N_B", length=ARROW_LEN)
    draw_force(ax, ACX,        ACY, angle_deg=270, color=COLOR_WEIGHT, label="W_A", length=ARROW_LEN)
    return save(fig, "N3L002_option2_wrong_E08.png")


def make_option3_wrong_E10():
    """E10 — N_A drawn upward and equal to N_f, violating Newton's 3rd Law."""
    fig, ax = fig_clean(4, 4)
    _setup_ax(ax)
    _draw_scene(ax)
    draw_force(ax, BCX,        BCY, angle_deg=270, color=COLOR_WEIGHT, label="W_B", length=ARROW_LEN)
    draw_force(ax, BCX - _DX, BCY, angle_deg=90,  color=COLOR_NORMAL, label="N_f", length=ARROW_LEN)
    draw_force(ax, BCX + _DX, BCY, angle_deg=90,  color=COLOR_NORMAL, label="N_A", length=ARROW_LEN)
    return save(fig, "N3L002_option3_wrong_E10.png")


if __name__ == "__main__":
    outputs = [
        make_situation(),
        make_option0_correct(),
        make_option1_wrong_E01(),
        make_option2_wrong_E08(),
        make_option3_wrong_E10(),
    ]
    for path in outputs:
        print(f"Saved: {path}")

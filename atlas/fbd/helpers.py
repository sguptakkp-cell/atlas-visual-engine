"""
Atlas Visual Engine — fbd/helpers.py  (v3 — textbook-standard conventions)

Arrow / origin conventions
--------------------------
  Normal force  (N)  — tail at BOTTOM edge of object  (cy – height/2),  UP
  Weight        (mg) — tail at CENTRE OF MASS          (cx, cy),         DOWN
  Tension       (T)  — tail at TOP edge of object      (cy + height/2),  UP

Use draw_force(…, origin_point="edge")   for surface/contact forces (N, T)
    draw_force(…, origin_point="centre") for body forces (gravity / mg)

The shift for "edge" mode is OPPOSITE to the arrow direction so the tail
lands on the surface from which the force acts:
  UP   force → tail shifted DOWN  by edge_offset  (e.g. floor contact)
  DOWN force → tail shifted UP    by edge_offset  (e.g. weight from inside)

Centre-of-mass dot
------------------
Every draw_force() call plots a filled •  at (cx, cy) to mark the COM.
"""

import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from atlas.constants.colors import COLOR_BG, COLOR_OBJECT_CIRCLE, COLOR_ROPE, COLOR_HIGHLIGHT
from atlas.constants.dimensions import (
    ARROW_LINE_WIDTH, ARROW_HEAD_WIDTH, ARROW_HEAD_LENGTH, ARROW_LENGTH,
    BLOCK_WIDTH, BLOCK_HEIGHT, BALL_RADIUS,
)
from atlas.constants.export import DEFAULT_DPI, BBOX_INCHES, FACECOLOR, OUTPUT_DIR

# ------------------------------------------------------------------
# Internal palette (avoids long re-import chains in sub-modules)
# ------------------------------------------------------------------
_NAVY  = "#1A2744"
_SLATE = "#64748B"
_GND   = "#CBD5E1"

# ------------------------------------------------------------------
# Typography for force labels — textbook italic-math style
# ------------------------------------------------------------------
_LABEL_FONT   = "STIXGeneral"    # falls back gracefully if not present
_LABEL_SIZE   = 16
_LABEL_STYLE  = "italic"
_LABEL_WEIGHT = "bold"
_LABEL_OFFSET = 0.28             # perpendicular offset from arrow tip (data units)


# ==================================================================
# Figure
# ==================================================================

def fig_clean(width=6, height=5):
    """Return (fig, ax) — 6×5 in, FRS background, equal aspect, axes off."""
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


# ==================================================================
# Object primitives
# ==================================================================

def draw_block(ax, cx, cy, width=BLOCK_WIDTH, height=BLOCK_HEIGHT,
               label="", color="#FAFAFA", highlighted=False):
    """Draw a rectangular block centred at (cx, cy).
    Text labels are intentionally suppressed — use force labels for annotation.
    """
    face = COLOR_HIGHLIGHT if highlighted else color
    rect = mpatches.Rectangle(
        (cx - width / 2, cy - height / 2), width, height,
        facecolor=face,
        edgecolor=_NAVY,
        linewidth=2.5,
        zorder=3,
    )
    ax.add_patch(rect)


def draw_ball(ax, cx, cy, radius=BALL_RADIUS, label="", color=COLOR_OBJECT_CIRCLE):
    """Draw a circle centred at (cx, cy)."""
    circle = mpatches.Circle(
        (cx, cy), radius,
        facecolor=color,
        edgecolor=_NAVY,
        linewidth=2.0,
        zorder=3,
    )
    ax.add_patch(circle)


# ==================================================================
# Ground / wall surfaces
# ==================================================================

def draw_ground(ax, x, y, width=3.0, direction="floor"):
    """Draw a hatched slab only (no bold contact line).
    direction: 'floor', 'left', or 'right'.
    """
    t = 0.22    # slab thickness in data units
    kw = dict(facecolor=_GND, alpha=0.5, edgecolor=_SLATE, linewidth=0.8,
              hatch="////", zorder=1)
    if direction == "floor":
        ax.add_patch(mpatches.Rectangle((x, y - t), width, t, **kw))
    elif direction == "left":
        ax.add_patch(mpatches.Rectangle((x - t, y), t, width, **kw))
    elif direction == "right":
        ax.add_patch(mpatches.Rectangle((x, y), t, width, **kw))
    else:
        raise ValueError(f"Unknown direction {direction!r}. Use 'floor', 'left', or 'right'.")


def draw_floor(ax, x, y, width=3.0):
    """Draw a floor at y: bold contact line at y + hatched slab below y."""
    # 1. Hatched slab (below the surface)
    draw_ground(ax, x, y, width=width, direction="floor")
    # 2. Bold contact line on the surface
    ax.plot([x, x + width], [y, y],
            color=_NAVY, lw=3.0, zorder=4, solid_capstyle="round")


def draw_wall(ax, x, y, height=3.0, side="left"):
    """Draw a vertical wall at x spanning height."""
    draw_ground(ax, x, y, width=height, direction=side)


# ==================================================================
# Force arrows + labels
# ==================================================================

def draw_arrow(ax, x, y, angle_deg, length=ARROW_LENGTH, color="#000000"):
    """Draw a single force arrow from tail (x, y) in direction angle_deg.
    Uses ax.annotate() exclusively for the open-chevron arrowhead.
    """
    rad   = math.radians(angle_deg)
    tip_x = x + length * math.cos(rad)
    tip_y = y + length * math.sin(rad)
    ax.annotate(
        "",
        xy=(tip_x, tip_y),
        xytext=(x, y),
        arrowprops=dict(
            arrowstyle=f"->, head_width={ARROW_HEAD_WIDTH}, head_length={ARROW_HEAD_LENGTH}",
            color=color,
            lw=3.5,
            mutation_scale=30,
        ),
        zorder=5,
    )


def draw_force_label(ax, x, y, angle_deg, length, text, color,
                     offset=_LABEL_OFFSET):
    """Place an italic-math force label at the arrow tip + perpendicular offset."""
    rad      = math.radians(angle_deg)
    tip_x    = x + length * math.cos(rad)
    tip_y    = y + length * math.sin(rad)
    perp_rad = math.radians(angle_deg + 90)
    lx = tip_x + offset * math.cos(perp_rad)
    ly = tip_y + offset * math.sin(perp_rad)
    ax.text(
        lx, ly, text,
        ha="center", va="center",
        fontsize=_LABEL_SIZE,
        fontstyle=_LABEL_STYLE,
        fontweight=_LABEL_WEIGHT,
        fontfamily=_LABEL_FONT,
        color=color,
        zorder=6,
    )


def draw_force(ax, cx, cy, angle_deg, color, label="", length=ARROW_LENGTH,
               origin_point="centre", edge_offset=None):
    """Draw a labelled force vector and a centre-of-mass dot.

    Parameters
    ----------
    cx, cy       : CENTRE of the object (always the reference position)
    angle_deg    : direction the force arrow points
    origin_point : "centre"  — tail at (cx, cy)               [body force, e.g. mg]
                   "edge"    — tail at the object edge opposite
                               to the force direction           [contact force, e.g. N, T]
    edge_offset  : half-thickness of object for edge placement
                   (default: BLOCK_HEIGHT / 2)
    """
    if edge_offset is None:
        edge_offset = BLOCK_HEIGHT / 2

    if origin_point == "edge":
        rad = math.radians(angle_deg)
        # Shift OPPOSITE to arrow direction → tail sits on the contact surface
        sx = cx - edge_offset * math.cos(rad)
        sy = cy - edge_offset * math.sin(rad)
    else:
        sx, sy = cx, cy

    draw_arrow(ax, sx, sy, angle_deg, length=length, color=color)

    # Centre-of-mass dot (always at object centre, not at arrow tail)
    ax.plot(cx, cy, "o", color=_NAVY, markersize=5, zorder=6)

    if label:
        draw_force_label(ax, sx, sy, angle_deg, length, label, color)


# ==================================================================
# Utility
# ==================================================================

def draw_string(ax, x1, y1, x2, y2, color=COLOR_ROPE, linewidth=2.0):
    """Draw a straight rope/string between two points."""
    ax.plot([x1, x2], [y1, y2],
            color=color, linewidth=linewidth,
            solid_capstyle="round", zorder=2)


def save(fig, filename, output_dir=OUTPUT_DIR):
    """Save figure to output_dir/filename at DEFAULT_DPI; closes fig."""
    os.makedirs(output_dir, exist_ok=True)
    if not filename.endswith((".png", ".pdf", ".svg")):
        filename = filename + ".png"
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=DEFAULT_DPI, bbox_inches=BBOX_INCHES, facecolor=FACECOLOR)
    plt.close(fig)
    return filepath

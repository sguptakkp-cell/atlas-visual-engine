"""
Atlas Visual Engine — fbd/helpers.py

Low-level drawing primitives for Free Body Diagrams.
All rendering goes through matplotlib; backend must be set before import.
"""

import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from atlas.constants.colors import (
    COLOR_BG, COLOR_OBJECT, COLOR_OBJECT_CIRCLE, COLOR_GROUND,
    COLOR_ROPE, COLOR_HIGHLIGHT, COLOR_NAVY, COLOR_SLATE,
)
from atlas.constants.dimensions import (
    ARROW_LINE_WIDTH, ARROW_HEAD_WIDTH, ARROW_HEAD_LENGTH, ARROW_LENGTH,
    BLOCK_WIDTH, BLOCK_HEIGHT, BALL_RADIUS,
    OBJECT_BORDER_WIDTH, GROUND_BORDER_WIDTH, LABEL_OFFSET,
)
from atlas.constants.typography import (
    FONT_FAMILY, FONT_SIZE_OBJECT, FONT_SIZE_FORCE,
    FONT_WEIGHT_OBJECT, FONT_WEIGHT_FORCE,
)
from atlas.constants.export import DEFAULT_DPI, BBOX_INCHES, FACECOLOR, OUTPUT_DIR


def fig_clean(width=4, height=4):
    """Create a clean figure with FRS background, equal aspect, axes off."""
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def draw_block(ax, cx, cy, width=BLOCK_WIDTH, height=BLOCK_HEIGHT,
               label="", color=COLOR_OBJECT, highlighted=False):
    """Draw a rectangular block centered at (cx, cy)."""
    face = COLOR_HIGHLIGHT if highlighted else color
    rect = mpatches.Rectangle(
        (cx - width / 2, cy - height / 2), width, height,
        facecolor=face,
        edgecolor=COLOR_NAVY,
        linewidth=OBJECT_BORDER_WIDTH,
        zorder=3,
    )
    ax.add_patch(rect)
    if label:
        ax.text(
            cx, cy, label,
            ha="center", va="center",
            fontsize=FONT_SIZE_OBJECT,
            fontweight=FONT_WEIGHT_OBJECT,
            fontfamily=FONT_FAMILY,
            color=COLOR_NAVY,
            zorder=4,
        )


def draw_ball(ax, cx, cy, radius=BALL_RADIUS, label="", color=COLOR_OBJECT_CIRCLE):
    """Draw a circle centered at (cx, cy)."""
    circle = mpatches.Circle(
        (cx, cy), radius,
        facecolor=color,
        edgecolor=COLOR_NAVY,
        linewidth=OBJECT_BORDER_WIDTH,
        zorder=3,
    )
    ax.add_patch(circle)
    if label:
        ax.text(
            cx, cy, label,
            ha="center", va="center",
            fontsize=FONT_SIZE_OBJECT,
            fontweight=FONT_WEIGHT_OBJECT,
            fontfamily=FONT_FAMILY,
            color=COLOR_NAVY,
            zorder=4,
        )


def draw_ground(ax, x, y, width=3.0, direction="floor"):
    """Draw a hatched ground surface. direction: 'floor', 'left', or 'right'."""
    thickness = 0.18
    if direction == "floor":
        rect = mpatches.Rectangle(
            (x, y - thickness), width, thickness,
            facecolor=COLOR_GROUND,
            edgecolor=COLOR_SLATE,
            linewidth=GROUND_BORDER_WIDTH,
            hatch="////",
            zorder=1,
        )
    elif direction == "left":
        rect = mpatches.Rectangle(
            (x - thickness, y), thickness, width,
            facecolor=COLOR_GROUND,
            edgecolor=COLOR_SLATE,
            linewidth=GROUND_BORDER_WIDTH,
            hatch="////",
            zorder=1,
        )
    elif direction == "right":
        rect = mpatches.Rectangle(
            (x, y), thickness, width,
            facecolor=COLOR_GROUND,
            edgecolor=COLOR_SLATE,
            linewidth=GROUND_BORDER_WIDTH,
            hatch="////",
            zorder=1,
        )
    else:
        raise ValueError(f"Unknown direction: {direction!r}. Use 'floor', 'left', or 'right'.")
    ax.add_patch(rect)


def draw_floor(ax, x, y, width=3.0):
    """Draw a floor surface at (x, y) spanning the given width."""
    draw_ground(ax, x, y, width=width, direction="floor")


def draw_wall(ax, x, y, height=3.0, side="left"):
    """Draw a vertical wall at (x, y) with the given height."""
    draw_ground(ax, x, y, width=height, direction=side)


def draw_arrow(ax, x, y, angle_deg, length=ARROW_LENGTH, color="#000000"):
    """Draw a force arrow from (x, y) in the given direction using ax.annotate."""
    rad = math.radians(angle_deg)
    tip_x = x + length * math.cos(rad)
    tip_y = y + length * math.sin(rad)
    ax.annotate(
        "",
        xy=(tip_x, tip_y),
        xytext=(x, y),
        arrowprops=dict(
            arrowstyle=f"->, head_width={ARROW_HEAD_WIDTH}, head_length={ARROW_HEAD_LENGTH}",
            color=color,
            lw=ARROW_LINE_WIDTH,
        ),
        zorder=5,
    )


def draw_force_label(ax, x, y, angle_deg, length, text, color, offset=LABEL_OFFSET):
    """Place a force label at the arrow tip, offset perpendicularly."""
    rad = math.radians(angle_deg)
    tip_x = x + length * math.cos(rad)
    tip_y = y + length * math.sin(rad)
    perp_rad = math.radians(angle_deg + 90)
    label_x = tip_x + offset * math.cos(perp_rad)
    label_y = tip_y + offset * math.sin(perp_rad)
    ax.text(
        label_x, label_y, text,
        ha="center", va="center",
        fontsize=FONT_SIZE_FORCE,
        fontweight=FONT_WEIGHT_FORCE,
        fontfamily=FONT_FAMILY,
        color=color,
        zorder=6,
    )


def draw_string(ax, x1, y1, x2, y2, color=COLOR_ROPE, linewidth=2.0):
    """Draw a straight rope/string between two points."""
    ax.plot(
        [x1, x2], [y1, y2],
        color=color,
        linewidth=linewidth,
        solid_capstyle="round",
        zorder=2,
    )


def save(fig, filename, output_dir=OUTPUT_DIR):
    """Save figure to output_dir/filename, create directory if needed."""
    os.makedirs(output_dir, exist_ok=True)
    if not filename.endswith((".png", ".pdf", ".svg")):
        filename = filename + ".png"
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=DEFAULT_DPI, bbox_inches=BBOX_INCHES, facecolor=FACECOLOR)
    plt.close(fig)
    return filepath


def draw_force(ax, x, y, angle_deg, color, label="", length=ARROW_LENGTH):
    """Convenience: draw arrow + label for a single force vector."""
    draw_arrow(ax, x, y, angle_deg, length=length, color=color)
    if label:
        draw_force_label(ax, x, y, angle_deg, length, label, color)

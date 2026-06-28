"""Atlas Elements - floor, ceiling, and wall surface renderers."""
import matplotlib.patches as mpatches
from atlas.styles.floor_style import FloorStyle, FLOOR_STYLE
from atlas.constants.tokens import Z_GROUND_HATCH, Z_GROUND_LINE


def draw_floor(ax, y: float, x_start: float, x_end: float,
               style: FloorStyle = FLOOR_STYLE, U: float = 0.6):
    depth = style.hatch_depth_ratio * U
    slab = mpatches.Rectangle(
        (x_start, y - depth), x_end - x_start, depth,
        facecolor=style.hatch_fill, alpha=style.hatch_alpha,
        edgecolor=style.hatch_color, linewidth=style.hatch_lw_px,
        hatch=style.hatch_pattern, zorder=Z_GROUND_HATCH,
    )
    ax.add_patch(slab)
    ax.plot(
        [x_start, x_end], [y, y],
        color=style.contact_color,
        linewidth=style.contact_lw_ratio * 10,
        solid_capstyle="round",
        zorder=Z_GROUND_LINE,
    )


def draw_ceiling(ax, y: float, x_start: float, x_end: float,
                 style: FloorStyle = FLOOR_STYLE, U: float = 0.6):
    depth = style.hatch_depth_ratio * U
    slab = mpatches.Rectangle(
        (x_start, y), x_end - x_start, depth,
        facecolor=style.hatch_fill, alpha=style.hatch_alpha,
        edgecolor=style.hatch_color, linewidth=style.hatch_lw_px,
        hatch=style.hatch_pattern, zorder=Z_GROUND_HATCH,
    )
    ax.add_patch(slab)
    ax.plot(
        [x_start, x_end], [y, y],
        color=style.contact_color,
        linewidth=style.contact_lw_ratio * 10,
        solid_capstyle="round",
        zorder=Z_GROUND_LINE,
    )


def draw_wall(ax, x: float, y_start: float, y_end: float,
              side: str = "left", style: FloorStyle = FLOOR_STYLE, U: float = 0.6):
    depth = style.hatch_depth_ratio * U
    if side == "left":
        rect_xy = (x - depth, y_start)
    else:
        rect_xy = (x, y_start)
    slab = mpatches.Rectangle(
        rect_xy, depth, y_end - y_start,
        facecolor=style.hatch_fill, alpha=style.hatch_alpha,
        edgecolor=style.hatch_color, linewidth=style.hatch_lw_px,
        hatch=style.hatch_pattern, zorder=Z_GROUND_HATCH,
    )
    ax.add_patch(slab)
    ax.plot(
        [x, x], [y_start, y_end],
        color=style.contact_color,
        linewidth=style.contact_lw_ratio * 10,
        solid_capstyle="round",
        zorder=Z_GROUND_LINE,
    )

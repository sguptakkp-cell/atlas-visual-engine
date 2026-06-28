"""Atlas Elements - block renderer."""
import matplotlib.patches as mpatches
from atlas.geometry.block_geo import BlockGeometry
from atlas.styles.block_style import BlockStyle, BLOCK_STYLE
from atlas.constants.tokens import Z_BLOCK_FILL, Z_COM_DOT


def draw_block(ax, geo: BlockGeometry, style: BlockStyle = BLOCK_STYLE,
               label="", show_com=True):
    U = geo.width / style.width_ratio
    corners_xy = [c.as_tuple() for c in geo.corners]
    poly = mpatches.Polygon(
        corners_xy, closed=True,
        facecolor=style.fill,
        edgecolor=style.border,
        linewidth=style.lw_ratio * 10,
        zorder=Z_BLOCK_FILL,
    )
    ax.add_patch(poly)

    if show_com:
        dot = mpatches.Circle(
            geo.com.as_tuple(),
            radius=style.com_r_ratio * geo.width,
            facecolor=style.com_color,
            edgecolor="none",
            zorder=Z_COM_DOT,
        )
        ax.add_patch(dot)

    if label:
        ax.text(
            geo.centre.x, geo.centre.y, label,
            ha="center", va="center",
            fontsize=style.label_size_ratio * 8,
            fontstyle=style.font_style,
            fontweight=style.font_weight,
            fontfamily=style.font_family,
            color=style.label_color,
            zorder=Z_COM_DOT + 1,
        )

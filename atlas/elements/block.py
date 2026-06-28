"""Atlas Elements - block renderer. All geometry from BlockGeometry. STATUS: FROZEN"""
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
from atlas.geometry.block_geo import BlockGeometry
from atlas.styles.block_style import BlockStyle, BLOCK_STYLE
from atlas.constants.tokens import Z_BLOCK_FILL, Z_BLOCK_BORDER, Z_COM_DOT


def draw_block(ax, geo: BlockGeometry, style: BlockStyle = BLOCK_STYLE,
               label: str = "", show_com: bool = True):
    trans = (
        mtransforms.Affine2D()
        .rotate_deg_around(geo.centre.x, geo.centre.y, geo.rotation_deg)
        + ax.transData
    )

    patch = mpatches.FancyBboxPatch(
        (geo.centre.x - geo.width / 2, geo.centre.y - geo.height / 2),
        geo.width, geo.height,
        boxstyle=f"round,pad=0,rounding_size={geo.rx}",
        facecolor=style.fill,
        edgecolor=style.border,
        linewidth=style.lw_ratio * geo.width,
        transform=trans,
        zorder=Z_BLOCK_FILL,
    )
    ax.add_patch(patch)

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
            fontsize=style.label_size_ratio * geo.width,
            fontstyle=style.font_style,
            fontweight=style.font_weight,
            fontfamily=style.font_family,
            color=style.label_color,
            zorder=Z_COM_DOT + 1,
        )

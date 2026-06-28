"""Atlas Elements - arrow renderer. Shaft + 4-point chevron head."""
import matplotlib.patches as mpatches
from atlas.geometry.arrow_geo import ArrowGeometry
from atlas.styles.arrow_style import ArrowStyle, ARROW_STYLE
from atlas.constants.tokens import Z_ARROW_SHAFT, Z_ARROW_HEAD, Z_FORCE_LABEL


def draw_arrow(ax, geo: ArrowGeometry, color: str, label: str = "",
               style: ArrowStyle = ARROW_STYLE):
    # Notch point: recessed 25% of head_len behind the wing base
    # Creates a concave tail for a sharper, 4-point chevron arrowhead
    notch = geo.shaft_end - geo.direction * (0.25 * geo.head_len)

    # Shaft terminates at notch for a clean connection
    ax.plot(
        [geo.tail.x, notch.x],
        [geo.tail.y, notch.y],
        color=color,
        linewidth=1.8,
        solid_capstyle="butt",
        zorder=Z_ARROW_SHAFT,
    )

    # 4-point arrowhead: tip → right wing → notch → left wing
    head_patch = mpatches.Polygon(
        [
            geo.head_tip.as_tuple(),
            geo.head_base_1.as_tuple(),
            notch.as_tuple(),
            geo.head_base_2.as_tuple(),
        ],
        closed=True,
        facecolor=color, edgecolor=color, linewidth=0,
        zorder=Z_ARROW_HEAD,
    )
    ax.add_patch(head_patch)

    if label:
        ax.text(
            geo.label_pos.x, geo.label_pos.y, label,
            ha="center", va="center",
            fontsize=style.label_size_ratio * 8,
            fontstyle=style.font_style,
            fontweight=style.font_weight,
            fontfamily=style.font_family,
            color=color,
            zorder=Z_FORCE_LABEL,
        )

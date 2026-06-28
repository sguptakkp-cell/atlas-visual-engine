"""Atlas Elements - arrow renderer. All geometry from ArrowGeometry. STATUS: FROZEN"""
from atlas.geometry.arrow_geo import ArrowGeometry
from atlas.styles.arrow_style import ArrowStyle, ARROW_STYLE
from atlas.constants.tokens import Z_ARROW_SHAFT, Z_ARROW_HEAD, Z_FORCE_LABEL


def draw_arrow(ax, geo: ArrowGeometry, color: str, label: str = "",
               style: ArrowStyle = ARROW_STYLE):
    ax.plot(
        [geo.tail.x, geo.shaft_end.x],
        [geo.tail.y, geo.shaft_end.y],
        color=color,
        linewidth=geo.shaft_lw,
        solid_capstyle="round",
        zorder=Z_ARROW_SHAFT,
    )

    ax.fill(
        [geo.head_tip.x, geo.head_base_1.x, geo.head_base_2.x],
        [geo.head_tip.y, geo.head_base_1.y, geo.head_base_2.y],
        color=color,
        zorder=Z_ARROW_HEAD,
    )

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

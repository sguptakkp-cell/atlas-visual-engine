"""Atlas Elements - rope renderer. TikZ-style triple stroke."""
from atlas.styles.rope_style import RopeStyle, ROPE_STYLE
from atlas.constants.tokens import Z_ROPE


def draw_rope(ax, x1: float, y1: float, x2: float, y2: float,
              style: RopeStyle = ROPE_STYLE, U: float = 0.6):
    common = dict(solid_capstyle=style.cap_style, zorder=Z_ROPE)
    ax.plot([x1, x2], [y1, y2],
            color=style.outer_color,
            linewidth=style.outer_lw_ratio * 10,
            **common)
    ax.plot([x1, x2], [y1, y2],
            color=style.mid_color,
            linewidth=style.mid_lw_ratio * 10,
            **common)
    ax.plot([x1, x2], [y1, y2],
            color=style.hi_color,
            linewidth=style.hi_lw_ratio * 10,
            alpha=style.hi_alpha,
            **common)

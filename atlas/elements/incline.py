"""Atlas Elements - incline (wedge) renderer."""
import matplotlib as mpl
import matplotlib.patches as mpatches
from atlas.geometry.incline_geo import InclineGeometry
from atlas.styles.incline_style import InclineStyle, INCLINE_STYLE
from atlas.constants.tokens import Z_INCLINE_FILL, Z_INCLINE_BORDER, Z_ANGLE_ARC, Z_ANGLE_LABEL


def draw_incline(ax, geo: InclineGeometry, style: InclineStyle = INCLINE_STYLE):
    wedge_pts = [geo.A.as_tuple(), geo.B.as_tuple(), geo.C.as_tuple()]

    # Solid fill — almost transparent, just a surface hint
    fill = mpatches.Polygon(
        wedge_pts, closed=True,
        facecolor=style.fill, alpha=0.12,
        edgecolor="none",
        zorder=Z_INCLINE_FILL,
    )
    ax.add_patch(fill)

    # Hatch layer — separate alpha so lines are independently controlled
    old_lw = mpl.rcParams["hatch.linewidth"]
    mpl.rcParams["hatch.linewidth"] = 0.6
    hatch_poly = mpatches.Polygon(
        wedge_pts, closed=True,
        facecolor="none", alpha=0.25,
        edgecolor=style.fill, linewidth=0,
        hatch="/",
        zorder=Z_INCLINE_FILL,
    )
    ax.add_patch(hatch_poly)
    mpl.rcParams["hatch.linewidth"] = old_lw

    # Wedge outline — thin, visually secondary
    border = mpatches.Polygon(
        wedge_pts, closed=True,
        facecolor="none", edgecolor=style.fill,
        linewidth=0.8,
        zorder=Z_INCLINE_BORDER,
    )
    ax.add_patch(border)

    # Bold slope line (hypotenuse A→C)
    ax.plot(
        [geo.A.x, geo.C.x], [geo.A.y, geo.C.y],
        color=style.fill,
        linewidth=1.8,
        solid_capstyle="round",
        zorder=Z_INCLINE_BORDER,
    )

    # Angle arc
    arc = mpatches.Arc(
        geo.arc_center.as_tuple(),
        width=2 * geo.arc_radius,
        height=2 * geo.arc_radius,
        angle=0, theta1=0, theta2=geo.theta_deg,
        color=style.label_color,
        linewidth=style.arc_lw_ratio * 10,
        zorder=Z_ANGLE_ARC,
    )
    ax.add_patch(arc)

    ax.text(
        geo.arc_label_pos.x, geo.arc_label_pos.y,
        f"θ={geo.label_theta_deg:.0f}°",
        ha="center", va="center",
        fontsize=style.label_size_ratio * 8,
        fontstyle=style.label_style,
        fontweight=style.label_weight,
        fontfamily=style.label_font,
        color=style.label_color,
        zorder=Z_ANGLE_LABEL,
    )

import math
import matplotlib.patches as patches
from matplotlib.patches import Arc

from atlas.constants.tokens import (
    INCLINE_BASE_RATIO, INCLINE_RENDER_ANGLE_DEG,
    ARC_RADIUS_H_RATIO, BLOCK_H_RATIO,
    BLOCK_POS_T, Z_INCLINE_FILL, Z_INCLINE_BORDER,
    Z_ANGLE_ARC, Z_ANGLE_LABEL, INCLINE_SLOPE_LW_PT,
    INCLINE_BORDER_LW_PT, INCLINE_FILL_ALPHA,
    ARC_LABEL_SIZE_PT, ARC_LW_PT,
    INCLINE_ANGLE_LABEL,
    HATCH_DEPTH_RATIO,
)

ALLOWED_ANGLES_DEG = frozenset({30, 37, 45, 53})


class AtlasInclineError(Exception):
    pass


class AtlasIncline:
    """
    An inclined plane wedge.
    FROZEN: always rendered at 20 degrees visual angle (AER-001).
    Physics angle stored separately — used only for label.
    """

    RENDER_ANGLE_DEG = 20.0  # FROZEN — always 20 degrees visual

    def __init__(self, x0, y0, U, physics_angle_deg=37):

        if U <= 0:
            raise AtlasInclineError(f"U must be > 0, got {U}")
        if physics_angle_deg not in ALLOWED_ANGLES_DEG:
            raise AtlasInclineError(
                f"physics_angle {physics_angle_deg} not in allowed set"
            )

        self.x0 = x0
        self.y0 = y0
        self.U  = U
        self.physics_angle_deg = physics_angle_deg

        # RENDER angle — always 20 degrees (AER-001)
        theta = math.radians(self.RENDER_ANGLE_DEG)

        # Wedge geometry
        base      = INCLINE_BASE_RATIO * U
        height    = base * math.tan(theta)
        slope_len = base / math.cos(theta)

        # Three corners
        self.A = (x0,        y0)            # bottom-left — angle here
        self.B = (x0 + base, y0)            # bottom-right — right angle
        self.C = (x0 + base, y0 + height)   # top-right — apex

        self.base      = base
        self.height    = height
        self.slope_len = slope_len
        self.theta_rad = theta

        # Direction vectors
        self.slope_vec  = ( math.cos(theta),  math.sin(theta))
        self.normal_vec = (-math.sin(theta),  math.cos(theta))

        # Block placement on slope
        t  = BLOCK_POS_T
        H  = BLOCK_H_RATIO * U
        Px = x0 + t * slope_len * math.cos(theta)
        Py = y0 + t * slope_len * math.sin(theta)
        self.block_cx       = Px + self.normal_vec[0] * H / 2
        self.block_cy       = Py + self.normal_vec[1] * H / 2
        self.block_rotation = self.RENDER_ANGLE_DEG

        # Angle arc — radius relative to H (master reference)
        self.arc_radius  = ARC_RADIUS_H_RATIO * H
        self.arc_center  = self.A

        # Cartesian label position — x and y set independently
        self.label_x    = x0 + self.arc_radius + 0.15 * U   # just right of arc
        self.label_y    = y0 + 0.02 * U                      # just above floor line
        self.label_text = INCLINE_ANGLE_LABEL
        self.label_size = ARC_LABEL_SIZE_PT

        # Style
        self.fill_alpha = INCLINE_FILL_ALPHA
        self.slope_lw   = INCLINE_SLOPE_LW_PT
        self.border_lw  = INCLINE_BORDER_LW_PT
        self.arc_lw     = ARC_LW_PT
        self.z_fill     = Z_INCLINE_FILL
        self.z_border   = Z_INCLINE_BORDER
        self.z_arc      = Z_ANGLE_ARC
        self.z_label    = Z_ANGLE_LABEL

    def render(self, ax):
        Ax, Ay = self.A
        Bx, By = self.B
        Cx, Cy = self.C

        triangle_x = [Ax, Bx, Cx, Ax]
        triangle_y = [Ay, By, Cy, Ay]

        # Solid light fill
        ax.fill(triangle_x, triangle_y,
                color="#E8EDF2", alpha=0.30,
                zorder=self.z_fill)
        # Hatch overlay — light, sparse, matches AtlasFloor
        ax.fill(triangle_x, triangle_y,
                fill=False, hatch="////",
                edgecolor="#B0B8C4", linewidth=0.6,
                alpha=0.5,
                zorder=self.z_fill)

        # Base (bottom)
        ax.plot([Ax, Bx], [Ay, By],
                color="#000000", lw=self.border_lw,
                solid_capstyle="round", zorder=self.z_border)
        # Right side (vertical)
        ax.plot([Bx, Cx], [By, Cy],
                color="#000000", lw=self.border_lw,
                solid_capstyle="round", zorder=self.z_border)
        # Slope — bold contact surface
        ax.plot([Ax, Cx], [Ay, Cy],
                color="#000000", lw=self.slope_lw,
                solid_capstyle="round", zorder=self.z_border)

        # Right-angle marker at B
        sq = 0.15 * self.U
        ax.plot([Bx - sq, Bx - sq, Bx],
                [By,      By + sq,  By + sq],
                color="#000000", lw=1.0, zorder=self.z_border)

        # Angle arc at A
        arc = Arc(self.A,
                  2 * self.arc_radius, 2 * self.arc_radius,
                  angle=0,
                  theta1=0, theta2=self.RENDER_ANGLE_DEG,
                  color="#000000", lw=self.arc_lw,
                  zorder=self.z_arc)
        ax.add_patch(arc)

        # Theta label — only θ symbol, never a number
        ax.text(self.label_x, self.label_y, self.label_text,
                fontfamily="DejaVu Serif",
                fontstyle="italic", fontweight="bold",
                fontsize=self.label_size,
                color="#000000",
                ha="left", va="bottom",
                zorder=self.z_label)

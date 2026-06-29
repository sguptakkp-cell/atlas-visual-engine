import math

from atlas.constants.tokens import (
    ROPE_LW_OUTER_PT, ROPE_LW_MID_PT, ROPE_LW_HI_PT,
    ROPE_HI_ALPHA, Z_ROPE,
)
from atlas.constants.colors import COLOR_ROPE_OUTER, COLOR_ROPE_MID, COLOR_ROPE_HI


class AtlasRopeError(Exception):
    pass


class AtlasRope:
    """
    A rope between two points.
    TikZ double-stroke style — 3 overlaid lines.

    FROZEN appearance:
        3 strokes: outer (dark brown) + mid (amber) + highlight (light amber)
        lw values are fixed pts — never × U
        cap_style = round
    """

    def __init__(self, x1, y1, x2, y2, U):

        if U <= 0:
            raise AtlasRopeError(f"U must be > 0, got {U}")
        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if length < 0.1 * U:
            raise AtlasRopeError(
                f"rope too short: {length:.4f} < 0.1*U={0.1*U:.4f}"
            )

        self.x1 = x1;  self.y1 = y1
        self.x2 = x2;  self.y2 = y2
        self.U  = U
        self.length = length

        self.lw_outer    = ROPE_LW_OUTER_PT   # 7.0pt fixed
        self.lw_mid      = ROPE_LW_MID_PT     # 4.0pt fixed
        self.lw_hi       = ROPE_LW_HI_PT      # 1.5pt fixed
        self.hi_alpha    = ROPE_HI_ALPHA
        self.color_outer = COLOR_ROPE_OUTER
        self.color_mid   = COLOR_ROPE_MID
        self.color_hi    = COLOR_ROPE_HI
        self.z           = Z_ROPE

    def render(self, ax):
        xs = [self.x1, self.x2]
        ys = [self.y1, self.y2]

        ax.plot(xs, ys, color=self.color_outer,
                lw=self.lw_outer, solid_capstyle="round",
                solid_joinstyle="round", zorder=self.z)

        ax.plot(xs, ys, color=self.color_mid,
                lw=self.lw_mid, solid_capstyle="round",
                solid_joinstyle="round", zorder=self.z + 1)

        ax.plot(xs, ys, color=self.color_hi,
                lw=self.lw_hi, alpha=self.hi_alpha,
                solid_capstyle="round", solid_joinstyle="round",
                zorder=self.z + 2)

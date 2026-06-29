import math

from atlas.constants.tokens import (
    ARROW_LENGTHS, ARROW_HEAD_RATIO, ARROW_WIDTH_RATIO,
    ARROW_SHAFT_LW_PT, ARROW_LABEL_SIZE_PT, ARROW_LABEL_OFFSET_PT,
    BLOCK_H_RATIO, Z_ARROW_SHAFT, Z_ARROW_HEAD, Z_FORCE_LABEL,
    FONT_FAMILY, FONT_STYLE, FONT_WEIGHT,
)
from atlas.constants.colors import VALID_FORCE_COLORS, get_force_color


class AtlasArrowError(Exception):
    pass


class AtlasArrow:
    """
    Self-contained force arrow.
    Caller provides: position, direction, force_name, U.
    Class computes: length, color, label, head size — everything.
    """
    VALID_FORCES = tuple(ARROW_LENGTHS.keys())

    def __init__(self, tail_x, tail_y, dir_x, dir_y, force_name, U):

        # VALIDATION
        if U <= 0:
            raise AtlasArrowError(f"U must be > 0, got {U}")
        mag = math.sqrt(dir_x**2 + dir_y**2)
        if abs(mag - 1.0) > 1e-6:
            raise AtlasArrowError(
                f"direction must be unit vector, got magnitude={mag:.6f}")
        if force_name not in self.VALID_FORCES:
            raise AtlasArrowError(
                f"force_name '{force_name}' not valid. "
                f"Valid: {self.VALID_FORCES}")

        # SELF-CONTAINED — all computed from force_name and U
        H = BLOCK_H_RATIO * U
        length = ARROW_LENGTHS[force_name] * H

        self.tail_x     = tail_x
        self.tail_y     = tail_y
        self.force_name = force_name
        self.U          = U
        self.color      = get_force_color(force_name)
        self.label      = force_name
        self.length     = length

        # Head — proportional to own L
        self.head_len   = ARROW_HEAD_RATIO  * length
        self.head_width = ARROW_WIDTH_RATIO * length
        self.shaft_lw   = ARROW_SHAFT_LW_PT
        self.label_size = ARROW_LABEL_SIZE_PT
        self.label_offset_pts = ARROW_LABEL_OFFSET_PT

        # Direction and perpendicular
        self.dir_x  = dir_x
        self.dir_y  = dir_y
        self.perp_x = -dir_y
        self.perp_y =  dir_x

        # Tip
        self.tip_x = tail_x + dir_x * length
        self.tip_y = tail_y + dir_y * length

        # Shaft end (where head triangle base sits)
        shaft_len = length - self.head_len
        self.shaft_end_x = tail_x + dir_x * shaft_len
        self.shaft_end_y = tail_y + dir_y * shaft_len

        # Head triangle corners
        hw = self.head_width / 2.0
        self.b1_x = self.shaft_end_x + self.perp_x * hw
        self.b1_y = self.shaft_end_y + self.perp_y * hw
        self.b2_x = self.shaft_end_x - self.perp_x * hw
        self.b2_y = self.shaft_end_y - self.perp_y * hw

    def render(self, ax):
        # Shaft
        ax.plot([self.tail_x, self.shaft_end_x],
                [self.tail_y, self.shaft_end_y],
                color=self.color, lw=self.shaft_lw,
                solid_capstyle="round", zorder=Z_ARROW_SHAFT)

        # Head
        ax.fill([self.tip_x, self.b1_x, self.b2_x],
                [self.tip_y, self.b1_y, self.b2_y],
                color=self.color, zorder=Z_ARROW_HEAD)

        # Label — offset in pts from tip, perpendicular to arrow direction
        if self.label:
            offset_x_pts = self.perp_x * self.label_offset_pts
            offset_y_pts = self.perp_y * self.label_offset_pts
            if abs(self.perp_x) > abs(self.perp_y):   # label goes left or right
                ha = "right" if self.perp_x < 0 else "left"
                va = "center"
            else:                                       # label goes up or down
                ha = "center"
                va = "bottom" if self.perp_y > 0 else "top"
            ax.annotate(
                self.label,
                xy=(self.tip_x, self.tip_y),
                xytext=(offset_x_pts, offset_y_pts),
                textcoords="offset points",
                fontfamily=FONT_FAMILY,
                fontstyle=FONT_STYLE,
                fontweight=FONT_WEIGHT,
                fontsize=self.label_size,
                color=self.color,
                ha=ha, va=va,
                zorder=Z_FORCE_LABEL,
                annotation_clip=False,
            )

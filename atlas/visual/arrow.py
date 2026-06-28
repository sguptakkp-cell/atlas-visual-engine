import math

from atlas.constants.tokens import ARROW_HEAD_RATIO, ARROW_WIDTH_RATIO, ARROW_SHAFT_RATIO
from atlas.constants.colors import VALID_FORCE_COLORS

LABEL_SIZE_RATIO   = 2.0
LABEL_OFFSET_RATIO = 0.20


class AtlasError(Exception):
    pass


class AtlasArrowError(AtlasError):
    pass


class AtlasArrow:
    def __init__(self, tail_x, tail_y, dir_x, dir_y,
                 length, color, label, U):

        # VALIDATION
        mag = math.sqrt(dir_x**2 + dir_y**2)
        if abs(mag - 1.0) > 1e-6:
            raise AtlasArrowError(f"direction must be unit vector, got magnitude={mag:.6f}")
        if length <= 0:
            raise AtlasArrowError(f"length must be > 0, got {length}")
        if U <= 0:
            raise AtlasArrowError(f"U must be > 0, got {U}")
        if color not in VALID_FORCE_COLORS.values():
            raise AtlasArrowError(f"color {color} not in approved palette")
        if label not in ("N", "mg", "T", "f", "F", ""):
            raise AtlasArrowError(f"label '{label}' not in approved labels")

        # FROZEN APPEARANCE
        self.head_len     = ARROW_HEAD_RATIO  * length
        self.head_width   = ARROW_WIDTH_RATIO * length
        self.shaft_lw     = ARROW_SHAFT_RATIO * U
        self.label_size   = LABEL_SIZE_RATIO  * U
        self.label_offset = LABEL_OFFSET_RATIO * U

        # GEOMETRY
        self.tail_x = tail_x
        self.tail_y = tail_y
        self.color  = color
        self.label  = label

        # perpendicular (CCW rotation of direction)
        self.perp_x = -dir_y
        self.perp_y =  dir_x

        # head tip
        self.tip_x = tail_x + dir_x * length
        self.tip_y = tail_y + dir_y * length

        # shaft end
        shaft_len = length - self.head_len
        self.shaft_end_x = tail_x + dir_x * shaft_len
        self.shaft_end_y = tail_y + dir_y * shaft_len

        # head triangle corners
        hw = self.head_width / 2.0
        self.b1_x = self.shaft_end_x + self.perp_x * hw
        self.b1_y = self.shaft_end_y + self.perp_y * hw
        self.b2_x = self.shaft_end_x - self.perp_x * hw
        self.b2_y = self.shaft_end_y - self.perp_y * hw

        # label position
        self.label_x = self.tip_x + self.perp_x * self.label_offset
        self.label_y = self.tip_y + self.perp_y * self.label_offset

    def render(self, ax):
        # shaft
        ax.plot([self.tail_x, self.shaft_end_x],
                [self.tail_y, self.shaft_end_y],
                color=self.color, lw=self.shaft_lw,
                solid_capstyle="round", zorder=40)
        # head
        ax.fill([self.tip_x, self.b1_x, self.b2_x],
                [self.tip_y, self.b1_y, self.b2_y],
                color=self.color, zorder=41)
        # label
        if self.label:
            ax.text(self.label_x, self.label_y, self.label,
                    fontfamily="DejaVu Serif", fontstyle="italic",
                    fontweight="bold", color=self.color,
                    fontsize=self.label_size,
                    ha="center", va="center", zorder=50)

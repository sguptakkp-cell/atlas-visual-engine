import math
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D

from atlas.constants.tokens import (
    BLOCK_W_RATIO, BLOCK_H_RATIO, BLOCK_RX_RATIO, BLOCK_LW_PT,
    COM_R_RATIO,
    Z_BLOCK_FILL, Z_BLOCK_BORDER, Z_COM_DOT,
    FONT_FAMILY, FONT_STYLE, FONT_WEIGHT,
)
from atlas.constants.colors import COLOR_BLOCK, COLOR_BLACK


class AtlasBlockError(Exception):
    pass


class AtlasBlock:
    def __init__(self, cx, cy, U, rotation_deg=0.0, label="",
                 width_scale=1.0, height_scale=1.0):

        # VALIDATION
        if U <= 0:
            raise AtlasBlockError(f"U must be > 0, got {U}")
        if width_scale <= 0:
            raise AtlasBlockError(f"width_scale must be > 0, got {width_scale}")
        if height_scale <= 0:
            raise AtlasBlockError(f"height_scale must be > 0, got {height_scale}")

        # Master reference: H = BLOCK_H_RATIO * U
        Hm = BLOCK_H_RATIO * U

        # FROZEN APPEARANCE — all relative to H
        self.width  = BLOCK_W_RATIO  * Hm * width_scale
        self.height = Hm * height_scale
        self.rx     = BLOCK_RX_RATIO * Hm
        self.lw     = BLOCK_LW_PT           # fixed pts — NOT * U
        self.com_r  = COM_R_RATIO   * Hm
        self.fill   = COLOR_BLOCK           # #EFF6FF
        self.border = COLOR_BLACK           # #000000
        self.label  = label
        self.cx     = cx
        self.cy     = cy
        self.U      = U
        self.rotation_deg = rotation_deg

        # CONTACT POINTS — all computed once in __init__
        r = math.radians(rotation_deg)
        cos_r = math.cos(r)
        sin_r = math.sin(r)
        W = self.width
        H = self.height

        def rotate(dx, dy):
            return (cx + dx * cos_r - dy * sin_r,
                    cy + dx * sin_r + dy * cos_r)

        self.top_cx,    self.top_cy    = rotate(0,      H / 2)
        self.bottom_cx, self.bottom_cy = rotate(0,     -H / 2)
        self.left_cx,   self.left_cy   = rotate(-W / 2,  0)
        self.right_cx,  self.right_cy  = rotate( W / 2,  0)
        self.com_x,     self.com_y     = cx, cy   # CoM = centre

        # CORNERS for drawing (clockwise from bottom-left)
        self.corners = [
            rotate(-W / 2, -H / 2),
            rotate( W / 2, -H / 2),
            rotate( W / 2,  H / 2),
            rotate(-W / 2,  H / 2),
        ]

    def render(self, ax):
        # Draw block as rotated FancyBboxPatch
        fancy = patches.FancyBboxPatch(
            (-self.width / 2, -self.height / 2),
            self.width, self.height,
            boxstyle=f"round,pad=0,rounding_size={self.rx}",
            linewidth=self.lw,
            edgecolor=self.border,
            facecolor=self.fill,
            zorder=Z_BLOCK_FILL,
        )
        transform = (Affine2D()
                     .rotate_deg(self.rotation_deg)
                     .translate(self.cx, self.cy)
                     + ax.transData)
        fancy.set_transform(transform)
        ax.add_patch(fancy)

        # CoM dot — size from spec
        dot = patches.Circle(
            (self.com_x, self.com_y), self.com_r,
            color=COLOR_BLACK, zorder=Z_COM_DOT)
        ax.add_patch(dot)

        # Optional label
        if self.label:
            ax.text(self.cx, self.cy, self.label,
                    fontfamily=FONT_FAMILY,
                    fontstyle=FONT_STYLE,
                    fontweight=FONT_WEIGHT,
                    fontsize=12.0,
                    color="#1A2744",
                    ha="center", va="center",
                    zorder=Z_BLOCK_BORDER)

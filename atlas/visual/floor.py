import matplotlib.patches as patches

from atlas.constants.tokens import (
    SURFACE_LW_PT, HATCH_DEPTH_RATIO,
    Z_GROUND_HATCH, Z_GROUND_LINE,
)


class AtlasFloorError(Exception):
    pass


class AtlasFloor:
    """
    A surface: floor, ceiling, or wall.
    Built from a contact line + hatch rectangle.

    FROZEN appearance:
        contact_lw  = SURFACE_LW_PT (fixed pts)
        hatch_depth = HATCH_DEPTH_RATIO * U
        fill        = #D1D5DB
        hatch_color = #9CA3AF
        pattern     = "////"

    Floor/ceiling: AtlasFloor(x_start, x_end, y, U, side="bottom"/"top")
    Wall:          AtlasFloor(y_start, y_end, wall_x, U, side="left"/"right")
                   (x_start=y_start, x_end=y_end, y=wall_x — same param order)
    """

    def __init__(self, x_start, x_end, y, U, side="bottom"):

        if U <= 0:
            raise AtlasFloorError(f"U must be > 0, got {U}")
        if x_start >= x_end:
            raise AtlasFloorError(f"x_start must be < x_end, got {x_start} >= {x_end}")
        if side not in ("bottom", "top", "left", "right"):
            raise AtlasFloorError(f"side must be bottom/top/left/right, got '{side}'")

        self.x_start     = x_start
        self.x_end       = x_end
        self.y           = y
        self.side        = side
        self.U           = U
        self.lw          = SURFACE_LW_PT
        self.depth       = HATCH_DEPTH_RATIO * U
        self.fill        = "#D1D5DB"
        self.hatch_color = "#9CA3AF"
        self.pattern     = "////"
        self.z_hatch     = Z_GROUND_HATCH
        self.z_line      = Z_GROUND_LINE

        # Horizontal contact line (floor/ceiling)
        self.contact_x1 = x_start
        self.contact_x2 = x_end
        self.contact_y  = y

        # Wall: reuse parameters as vertical extents + x position
        if side in ("left", "right"):
            if not hasattr(self, 'y_start'):
                self.y_start = x_start  # reuse parameter as y_start
                self.y_end   = x_end    # reuse parameter as y_end
                self.wall_x  = y        # reuse y parameter as wall_x

    def render(self, ax):

        if self.side in ("bottom", "top"):
            # FLOOR or CEILING — horizontal
            if self.side == "bottom":
                hatch_y = self.y - self.depth
            else:
                hatch_y = self.y

            rect = patches.Rectangle(
                (self.x_start, hatch_y),
                self.x_end - self.x_start, self.depth,
                hatch=self.pattern, facecolor=self.fill,
                edgecolor=self.hatch_color, alpha=0.55,
                linewidth=1.2, zorder=self.z_hatch)
            ax.add_patch(rect)
            ax.plot(
                [self.contact_x1, self.contact_x2],
                [self.contact_y,  self.contact_y],
                color="#000000", lw=self.lw,
                solid_capstyle="round", zorder=self.z_line)

        else:
            # WALL — vertical
            wall_x  = self.wall_x
            y_start = self.y_start
            y_end   = self.y_end

            if self.side == "left":
                hatch_x = wall_x - self.depth  # hatch extends LEFT of contact line
            else:
                hatch_x = wall_x               # hatch extends RIGHT of contact line

            rect = patches.Rectangle(
                (hatch_x, y_start),
                self.depth, y_end - y_start,
                hatch=self.pattern, facecolor=self.fill,
                edgecolor=self.hatch_color, alpha=0.55,
                linewidth=1.2, zorder=self.z_hatch)
            ax.add_patch(rect)
            ax.plot(
                [wall_x, wall_x], [y_start, y_end],
                color="#000000", lw=self.lw,
                solid_capstyle="round", zorder=self.z_line)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math
import os

from atlas.visual.block   import AtlasBlock
from atlas.visual.floor   import AtlasFloor
from atlas.visual.rope    import AtlasRope
from atlas.visual.arrow   import AtlasArrow
from atlas.visual.incline import AtlasIncline
from atlas.constants.tokens import compute_canvas, get_H, STACK_2_H, STACK_3_H

class PhysicsSceneError(Exception): pass

class PhysicsScene:
    """
    Top-level API. One call produces one complete diagram.

    Usage:
        PhysicsScene("floor_block",    U=0.6).render("out.png")
        PhysicsScene("hanging_block",  U=0.6).render("out.png")
        PhysicsScene("incline_block",  U=0.6, theta=37).render("out.png")
        PhysicsScene("stacked_2",      U=0.6).render("out.png")
        PhysicsScene("stacked_3",      U=0.6).render("out.png")
        PhysicsScene("incline_hanging",U=0.6, theta=37).render("out.png")
        PhysicsScene("atwood",         U=0.6).render("out.png")
        PhysicsScene("floor_applied",  U=0.6).render("out.png")

    Rules:
        - Caller provides ONLY scenario name + physics params
        - All positions, sizes, forces computed internally
        - All classes used — no raw matplotlib
        - Canvas auto-sized from scenario
    """

    VALID_SCENARIOS = (
        "floor_block",
        "hanging_block",
        "incline_block",
        "stacked_2",
        "stacked_3",
        "incline_hanging",
        "atwood",
        "floor_applied",
    )

    def __init__(self, scenario, U=0.6, theta=37,
                 show_friction=True, show_N=True, show_mg=True,
                 show_T=True, show_applied=False):

        if scenario not in self.VALID_SCENARIOS:
            raise PhysicsSceneError(
                f"Unknown scenario '{scenario}'. "
                f"Valid: {self.VALID_SCENARIOS}")

        self.scenario      = scenario
        self.U             = U
        self.theta         = theta
        self.show_friction = show_friction
        self.show_N        = show_N
        self.show_mg       = show_mg
        self.show_T        = show_T
        self.show_applied  = show_applied
        self.H             = get_H(U)

    def render(self, filepath="output.png", dpi=150):
        """Render scenario to PNG. Returns filepath."""
        fig, ax = self._make_canvas()
        self._draw(ax)
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        fig.savefig(filepath, dpi=dpi,
                    bbox_inches="tight", facecolor="#FFFFFF")
        plt.close(fig)
        return filepath

    def _make_canvas(self):
        canvas_map = {
            "floor_block":    "floor_only",
            "hanging_block":  "hanging_only",
            "incline_block":  "incline_only",
            "stacked_2":      "floor_only",
            "stacked_3":      "floor_only",
            "incline_hanging":"incline_hanging",
            "atwood":         "atwood",
            "floor_applied":  "floor_only",
        }
        key = canvas_map[self.scenario]
        W, H_c = compute_canvas(key, self.U)
        fig, ax = plt.subplots(figsize=(W*1.5, H_c*1.5))
        ax.set_xlim(0, W)
        ax.set_ylim(0, H_c)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_facecolor("#FFFFFF")
        fig.patch.set_facecolor("#FFFFFF")
        self._W  = W
        self._Hc = H_c
        return fig, ax

    def _draw(self, ax):
        getattr(self, f"_draw_{self.scenario}")(ax)

    # ── SCENARIO DRAWERS ─────────────────────────────────────

    def _draw_floor_block(self, ax):
        H = self.H; W = self._W; H_c = self._Hc
        floor_y = H_c * 0.35
        AtlasFloor(0.3*H, W-0.3*H, floor_y, self.U).render(ax)
        b = AtlasBlock(W/2, floor_y + H/2, self.U)
        b.render(ax)
        if self.show_N:
            AtlasArrow(b.bottom_cx, b.bottom_cy,  0,  1, "N",  self.U).render(ax)
        if self.show_mg:
            AtlasArrow(b.com_x,     b.com_y,      0, -1, "mg", self.U).render(ax)
        if self.show_friction:
            AtlasArrow(b.bottom_cx, b.bottom_cy,  1,  0, "f",  self.U).render(ax)

    def _draw_hanging_block(self, ax):
        H = self.H; W = self._W; H_c = self._Hc
        ceil_y = H_c * 0.85
        AtlasFloor(0.3*H, W-0.3*H, ceil_y, self.U, side="top").render(ax)
        b = AtlasBlock(W/2, ceil_y - H*2.5 - H/2, self.U)
        b.render(ax)
        AtlasRope(b.top_cx, ceil_y, b.top_cx, b.top_cy, self.U).render(ax)
        if self.show_T:
            AtlasArrow(b.top_cx, b.top_cy+0.05*H, 0, 1, "T", self.U).render(ax)
        if self.show_mg:
            AtlasArrow(b.com_x, b.com_y, 0, -1, "mg", self.U).render(ax)

    def _draw_incline_block(self, ax):
        H = self.H; W = self._W; H_c = self._Hc
        floor_y = H
        AtlasFloor(0, W, floor_y, self.U).render(ax)
        inc = AtlasIncline(H, floor_y, self.U, physics_angle_deg=self.theta)
        inc.render(ax)
        b = AtlasBlock(inc.block_cx, inc.block_cy, self.U,
                       rotation_deg=inc.block_rotation)
        b.render(ax)
        if self.show_N:
            AtlasArrow(b.com_x, b.com_y,
                       inc.normal_vec[0], inc.normal_vec[1], "N", self.U).render(ax)
        if self.show_mg:
            AtlasArrow(b.com_x, b.com_y, 0, -1, "mg", self.U).render(ax)
        if self.show_friction:
            AtlasArrow(b.com_x, b.com_y,
                       inc.slope_vec[0], inc.slope_vec[1], "f", self.U).render(ax)

    def _draw_stacked_2(self, ax):
        H = self.H; W = self._W; H_c = self._Hc
        H2 = H * STACK_2_H
        floor_y = H_c * 0.30
        AtlasFloor(0.3*H, W-0.3*H, floor_y, self.U).render(ax)
        b_bot = AtlasBlock(W/2, floor_y+H2*0.5, self.U,
                           width_scale=2.0, height_scale=STACK_2_H)
        b_top = AtlasBlock(W/2, floor_y+H2*1.5, self.U,
                           width_scale=1.0, height_scale=STACK_2_H)
        b_bot.render(ax); b_top.render(ax)
        if self.show_N:
            AtlasArrow(b_top.com_x, b_top.com_y, 0,  1, "N",  self.U).render(ax)
        if self.show_mg:
            AtlasArrow(b_bot.com_x, b_bot.com_y, 0, -1, "mg", self.U).render(ax)

    def _draw_stacked_3(self, ax):
        H = self.H; W = self._W; H_c = self._Hc
        H3 = H * STACK_3_H
        floor_y = H_c * 0.20
        AtlasFloor(0.3*H, W-0.3*H, floor_y, self.U).render(ax)
        b_bot = AtlasBlock(W/2, floor_y+H3*0.5, self.U,
                           width_scale=3.0, height_scale=STACK_3_H)
        b_mid = AtlasBlock(W/2, floor_y+H3*1.5, self.U,
                           width_scale=2.0, height_scale=STACK_3_H)
        b_top = AtlasBlock(W/2, floor_y+H3*2.5, self.U,
                           width_scale=1.0, height_scale=STACK_3_H)
        b_bot.render(ax); b_mid.render(ax); b_top.render(ax)
        if self.show_N:
            AtlasArrow(b_top.com_x, b_top.com_y, 0,  1, "N",  self.U).render(ax)
        if self.show_mg:
            AtlasArrow(b_bot.com_x, b_bot.com_y, 0, -1, "mg", self.U).render(ax)

    def _draw_incline_hanging(self, ax):
        H = self.H; W = self._W; H_c = self._Hc
        floor_y = H
        inc = AtlasIncline(H, floor_y, self.U, physics_angle_deg=self.theta)
        AtlasFloor(0, W, floor_y, self.U).render(ax)
        AtlasFloor(inc.B[0]+H, inc.B[0]+4*H, H_c-H, self.U, side="top").render(ax)
        inc.render(ax)
        bi = AtlasBlock(inc.block_cx, inc.block_cy, self.U,
                        rotation_deg=inc.block_rotation)
        bi.render(ax)
        bh = AtlasBlock(inc.B[0]+2*H, H_c-H-H*2.5-H/2, self.U)
        bh.render(ax)
        AtlasRope(bh.top_cx, H_c-H, bh.top_cx, bh.top_cy, self.U).render(ax)
        if self.show_N:
            AtlasArrow(bi.com_x, bi.com_y,
                       inc.normal_vec[0], inc.normal_vec[1], "N", self.U).render(ax)
        if self.show_mg:
            AtlasArrow(bi.com_x, bi.com_y, 0, -1, "mg", self.U).render(ax)
            AtlasArrow(bh.com_x, bh.com_y, 0, -1, "mg", self.U).render(ax)
        if self.show_T:
            AtlasArrow(bh.top_cx, bh.top_cy+0.05*H, 0, 1, "T", self.U).render(ax)

    def _draw_atwood(self, ax):
        H = self.H; W = self._W; H_c = self._Hc
        ceil_y = H_c * 0.92
        AtlasFloor(0.2*H, W-0.2*H, ceil_y, self.U, side="top").render(ax)

        # Left block higher, right block lower — Atwood standard
        cx = W / 2
        b1 = AtlasBlock(cx*0.5, ceil_y - H*2.0 - H/2, self.U)
        b2 = AtlasBlock(cx*1.5, ceil_y - H*3.5 - H/2, self.U)
        b1.render(ax); b2.render(ax)
        AtlasRope(b1.top_cx, ceil_y, b1.top_cx, b1.top_cy, self.U).render(ax)
        AtlasRope(b2.top_cx, ceil_y, b2.top_cx, b2.top_cy, self.U).render(ax)
        if self.show_T:
            # T labels on opposite sides
            AtlasArrow(b1.top_cx, b1.top_cy+0.05*H,
                       0, 1, "T", self.U).render(ax)
            AtlasArrow(b2.top_cx, b2.top_cy+0.05*H,
                       0, 1, "T", self.U).render(ax)
        if self.show_mg:
            AtlasArrow(b1.com_x, b1.com_y, 0, -1, "mg", self.U).render(ax)
            AtlasArrow(b2.com_x, b2.com_y, 0, -1, "mg", self.U).render(ax)

    def _draw_floor_applied(self, ax):
        H = self.H; W = self._W; H_c = self._Hc
        floor_y = H_c * 0.35
        AtlasFloor(0.3*H, W-0.3*H, floor_y, self.U).render(ax)
        b = AtlasBlock(W/2, floor_y+H/2, self.U)
        b.render(ax)
        if self.show_N:
            AtlasArrow(b.bottom_cx, b.bottom_cy, 0, 1, "N", self.U).render(ax)
        if self.show_mg:
            AtlasArrow(b.com_x, b.com_y, 0, -1, "mg", self.U).render(ax)
        if self.show_friction:
            AtlasArrow(b.bottom_cx, b.bottom_cy, -1, 0, "f", self.U).render(ax)
        if self.show_applied:
            AtlasArrow(b.right_cx, b.right_cy, 1, 0, "F", self.U).render(ax)

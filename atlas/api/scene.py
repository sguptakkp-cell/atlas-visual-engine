"""Atlas API - PhysicsScene: one-call incline FBD renderer."""
import matplotlib.patches as mpatches

from atlas.geometry.incline_geo import compute_incline
from atlas.geometry.block_geo import compute_block
from atlas.geometry.arrow_geo import compute_arrow
from atlas.physics.incline import InclineInput, compute_frame
from atlas.styles.block_style import BLOCK_STYLE
from atlas.styles.arrow_style import ARROW_STYLE
from atlas.elements.block import draw_block
from atlas.elements.arrow import draw_arrow
from atlas.elements.incline import draw_incline
from atlas.renderer.canvas import fig_clean, save
from atlas.constants.tokens import Z_COM_DOT


class PhysicsScene:
    def __init__(self, theta_deg: float = 37, mu: float = 0.3,
                 active_forces: tuple = ("N", "mg", "f"), U: float = 0.6):
        self.theta_deg = theta_deg
        self.mu = mu
        self.active_forces = tuple(active_forces)
        self.U = U

    def render(self, filename: str = "output.png") -> str:
        U = self.U
        BLOCK_W = BLOCK_STYLE.width_ratio * U

        # Incline geometry — canvas size derived from block/wedge proportions
        incline_geo = compute_incline(self.theta_deg, U)
        fig, ax = fig_clean(
            U=U,
            canvas_w=incline_geo.canvas_w,
            canvas_h=incline_geo.canvas_h,
        )

        draw_incline(ax, incline_geo)

        # Block rotated flush to slope
        block_geo = compute_block(
            incline_geo.block_centre.x,
            incline_geo.block_centre.y,
            U,
            rotation_deg=self.theta_deg,
        )
        draw_block(ax, block_geo, show_com=False)

        # COM dot — tiny black circle, drawn explicitly
        com_dot = mpatches.Circle(
            block_geo.com.as_tuple(),
            radius=0.03 * BLOCK_W,
            facecolor="black", edgecolor="none",
            zorder=Z_COM_DOT,
        )
        ax.add_patch(com_dot)

        # Physics at t=0
        inp = InclineInput(
            theta_deg=self.theta_deg, mu=self.mu,
            active_forces=self.active_forces,
        )
        frame = compute_frame(inp, t=0, block_centre=incline_geo.block_centre)
        sv = frame.slope_vec

        for force in frame.forces:
            if force.name == "N":
                # Contact force — tail at slope contact surface
                tail = block_geo.bottom_centre
            elif force.name == "f":
                # Near COM but offset down-slope to separate from mg label
                tail = block_geo.com - sv * (0.08 * BLOCK_W)
            else:
                # Body force (mg) — tail at COM
                tail = block_geo.com

            length = ARROW_STYLE.get_length(force.name, U)
            arrow_geo = compute_arrow(tail, force.direction, length, U)
            draw_arrow(ax, arrow_geo, force.color, label=force.label)

        return save(fig, filename)

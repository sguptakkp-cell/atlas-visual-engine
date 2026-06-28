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
from atlas.constants.tokens import Z_COM_DOT, INCLINE_RENDER_ANGLE_DEG


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

        # Incline geometry — visual angle 20° (AER-001); physics angle in label
        incline_geo = compute_incline(self.theta_deg, U)
        fig, ax = fig_clean(
            U=U,
            canvas_w=incline_geo.canvas_w,
            canvas_h=incline_geo.canvas_h,
        )

        draw_incline(ax, incline_geo)

        # Block rotated at visual render angle (20°), not physics angle
        block_geo = compute_block(
            incline_geo.block_centre.x,
            incline_geo.block_centre.y,
            U,
            rotation_deg=INCLINE_RENDER_ANGLE_DEG,
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

        # Physics at actual angle (self.theta_deg); geometry follows visual angle
        inp = InclineInput(
            theta_deg=self.theta_deg, mu=self.mu,
            active_forces=self.active_forces,
        )
        frame = compute_frame(inp, t=0, block_centre=incline_geo.block_centre)

        # Visual vectors from 20° geometry (AER-001)
        sv_visual = incline_geo.slope_vec
        nv_visual = incline_geo.normal_vec

        for force in frame.forces:
            if force.name == "N":
                # Contact force: tail at block base, direction along visual normal
                tail = block_geo.bottom_centre
                direction = nv_visual
            elif force.name == "f":
                # Near COM, offset down visual slope; direction up visual slope
                tail = block_geo.com - sv_visual * (0.08 * BLOCK_W)
                direction = sv_visual
            else:
                # Body force (mg): tail at COM, direction straight down
                tail = block_geo.com
                direction = force.direction

            length = ARROW_STYLE.get_length(force.name, U)
            arrow_geo = compute_arrow(tail, direction, length, U)
            draw_arrow(ax, arrow_geo, force.color, label=force.label)

        return save(fig, filename)

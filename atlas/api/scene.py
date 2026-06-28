"""Atlas API - PhysicsScene: one-call incline FBD renderer."""
from atlas.geometry.incline_geo import compute_incline
from atlas.geometry.block_geo import compute_block
from atlas.geometry.arrow_geo import compute_arrow
from atlas.physics.incline import InclineInput, compute_frame
from atlas.styles.arrow_style import ARROW_STYLE
from atlas.elements.block import draw_block
from atlas.elements.arrow import draw_arrow
from atlas.elements.incline import draw_incline

from atlas.renderer.canvas import fig_clean, save


class PhysicsScene:
    def __init__(self, theta_deg: float = 37, mu: float = 0.3,
                 active_forces: tuple = ("N", "mg", "f"), U: float = 0.6):
        self.theta_deg = theta_deg
        self.mu = mu
        self.active_forces = tuple(active_forces)
        self.U = U

    def render(self, filename: str = "output.png") -> str:
        U = self.U
        fig, ax = fig_clean(U=U, scenario="incline")

        # Incline positioned for balanced margins
        x0, y0 = 1.5 * U, 2.0 * U
        incline_geo = compute_incline(self.theta_deg, x0, y0, U)

        draw_incline(ax, incline_geo)

        # Block rotated to sit flush on slope
        block_geo = compute_block(
            incline_geo.block_centre.x,
            incline_geo.block_centre.y,
            U,
            rotation_deg=self.theta_deg,
        )
        draw_block(ax, block_geo, show_com=True)

        # Physics
        inp = InclineInput(
            theta_deg=self.theta_deg, mu=self.mu,
            active_forces=self.active_forces,
        )
        frame = compute_frame(inp, t=0, block_centre=incline_geo.block_centre)

        sv = frame.slope_vec

        for force in frame.forces:
            if force.name == "N":
                tail = block_geo.bottom_centre
            elif force.name == "f":
                # Offset slightly down-slope from N to separate arrow origins
                tail = block_geo.bottom_centre + sv * (-0.1 * U)
            else:
                tail = block_geo.com

            length = ARROW_STYLE.get_length(force.name, U)
            arrow_geo = compute_arrow(tail, force.direction, length, U)
            draw_arrow(ax, arrow_geo, force.color, label=force.label)

        return save(fig, filename)

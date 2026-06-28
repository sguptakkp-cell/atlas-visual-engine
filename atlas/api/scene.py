"""Atlas API - PhysicsScene: one-call incline FBD renderer."""
from atlas.geometry.incline_geo import compute_incline
from atlas.geometry.block_geo import compute_block
from atlas.geometry.arrow_geo import compute_arrow
from atlas.physics.incline import InclineInput, compute_frame
from atlas.styles.block_style import BLOCK_STYLE
from atlas.styles.arrow_style import ARROW_STYLE
from atlas.elements.block import draw_block
from atlas.elements.arrow import draw_arrow
from atlas.elements.incline import draw_incline
from atlas.elements.floor import draw_floor
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
        canvas_w = 12.0 * U
        canvas_h = 10.0 * U

        # Incline anchored in bottom-left margin
        margin = 0.5 * U
        x0, y0 = margin, margin
        incline_geo = compute_incline(self.theta_deg, x0, y0, U)

        draw_incline(ax, incline_geo)
        draw_floor(ax, y0, x0, x0 + incline_geo.base, U=U)

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

        nv = frame.normal_vec
        H = BLOCK_STYLE.height_ratio * U

        for force in frame.forces:
            # Contact forces originate at slope surface; body forces at COM
            if force.name in ("N", "f"):
                tail = incline_geo.block_centre - nv * (H / 2)
            else:
                tail = incline_geo.block_centre

            length = ARROW_STYLE.get_length(force.name, U)
            arrow_geo = compute_arrow(tail, force.direction, length, U)
            draw_arrow(ax, arrow_geo, force.color, label=force.label)

        return save(fig, filename)

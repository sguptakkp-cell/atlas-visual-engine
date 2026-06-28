"""Atlas Geometry - InclineGeometry. Block-relative composition. STATUS: ACTIVE"""
import math
from dataclasses import dataclass
from atlas.geometry.vectors import Vector2, slope_vectors
from atlas.styles.incline_style import InclineStyle, INCLINE_STYLE
from atlas.styles.block_style import BlockStyle, BLOCK_STYLE
from atlas.constants.tokens import (
    ALLOWED_ANGLES_DEG, BLOCK_REL_SLOPE_MULTIPLIER, ARC_RADIUS_BLOCK,
    INCLINE_RENDER_ANGLE_DEG,
)

@dataclass(frozen=True)
class InclineGeometry:
    A:Vector2; B:Vector2; C:Vector2
    base:float; height:float; slope_len:float; theta_deg:float; theta_rad:float
    slope_vec:Vector2; normal_vec:Vector2
    block_anchor:Vector2; block_centre:Vector2
    arc_center:Vector2; arc_radius:float; arc_label_pos:Vector2
    canvas_w:float; canvas_h:float
    label_theta_deg:float


def compute_incline(physics_theta_deg, U, i_style=INCLINE_STYLE, b_style=BLOCK_STYLE):
    assert U > 0
    assert 0 < physics_theta_deg < 90, f"theta must be 0-90, got {physics_theta_deg}"
    assert physics_theta_deg in ALLOWED_ANGLES_DEG, \
        f"{physics_theta_deg} not in {ALLOWED_ANGLES_DEG}"

    # AER-001: all geometry at visual render angle (20°), physics angle goes to label
    t = math.radians(INCLINE_RENDER_ANGLE_DEG)

    # Block dimensions are the visual reference
    BW = b_style.width_ratio * U
    BH = b_style.height_ratio * U

    # Slope and wedge dimensions derived from block
    slope_len = BW * BLOCK_REL_SLOPE_MULTIPLIER
    base = slope_len * math.cos(t)
    height = slope_len * math.sin(t)

    # Canvas: wedge + margin, always landscape (h ≤ 75% of w)
    canvas_w = base + 3.5 * U
    if height > canvas_w * 0.72:
        scale = (canvas_w * 0.65) / height
        base *= scale
        height *= scale
        slope_len *= scale  # keep block position consistent
    canvas_h = min(height + 3.0 * U, canvas_w * 0.75)

    # Wedge origin: 1.5U from bottom-left of canvas
    x0 = 1.5 * U
    y0 = 1.5 * U
    A = Vector2(x0, y0)
    B = Vector2(x0 + base, y0)
    C = Vector2(x0 + base, y0 + height)

    sv, nv = slope_vectors(INCLINE_RENDER_ANGLE_DEG)

    # Block: t=0.45 along slope, lifted half block-height along normal
    P = A + sv * (i_style.block_pos_t * slope_len)
    bc = P + nv * (BH / 2)

    # Angle arc — block-relative radius, bisector at visual angle
    arc_r = ARC_RADIUS_BLOCK * BW
    bis = Vector2(
        math.cos(math.radians(INCLINE_RENDER_ANGLE_DEG / 2)),
        math.sin(math.radians(INCLINE_RENDER_ANGLE_DEG / 2)),
    )
    lp = A + bis * (arc_r + i_style.label_gap_ratio * U)

    return InclineGeometry(
        A=A, B=B, C=C,
        base=base, height=height, slope_len=slope_len,
        theta_deg=INCLINE_RENDER_ANGLE_DEG, theta_rad=t,
        slope_vec=sv, normal_vec=nv,
        block_anchor=P, block_centre=bc,
        arc_center=A, arc_radius=arc_r,
        arc_label_pos=lp,
        canvas_w=canvas_w, canvas_h=canvas_h,
        label_theta_deg=float(physics_theta_deg),
    )

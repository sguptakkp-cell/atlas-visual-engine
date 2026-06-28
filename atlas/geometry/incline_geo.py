"""Atlas Geometry - InclineGeometry. Pure math. STATUS: FROZEN"""
import math
from dataclasses import dataclass
from atlas.geometry.vectors import Vector2, slope_vectors
from atlas.styles.incline_style import InclineStyle, INCLINE_STYLE
from atlas.styles.block_style import BlockStyle, BLOCK_STYLE
from atlas.constants.tokens import ALLOWED_ANGLES_DEG, CANVAS_W_INCL_RATIO, CANVAS_H_RATIO

@dataclass(frozen=True)
class InclineGeometry:
    A:Vector2; B:Vector2; C:Vector2
    base:float; height:float; slope_len:float; theta_deg:float; theta_rad:float
    slope_vec:Vector2; normal_vec:Vector2
    block_anchor:Vector2; block_centre:Vector2
    arc_center:Vector2; arc_radius:float; arc_label_pos:Vector2
    canvas_w:float; canvas_h:float

def compute_incline(theta_deg,x0,y0,U,i_style=INCLINE_STYLE,b_style=BLOCK_STYLE):
    assert U>0
    assert 0<theta_deg<90,f"theta must be 0-90, got {theta_deg}"
    assert theta_deg in ALLOWED_ANGLES_DEG,f"{theta_deg} not in {ALLOWED_ANGLES_DEG}"
    t=math.radians(theta_deg)
    base=i_style.base_ratio*U; height=base*math.tan(t); slope_len=base/math.cos(t)
    A=Vector2(x0,y0); B=Vector2(x0+base,y0); C=Vector2(x0+base,y0+height)
    sv,nv=slope_vectors(theta_deg)
    P=A+sv*(i_style.block_pos_t*slope_len)
    bc=P+nv*(b_style.height_ratio*U/2.0)
    arc_r=i_style.arc_radius_ratio*U
    bis=Vector2(math.cos(math.radians(theta_deg/2)),math.sin(math.radians(theta_deg/2)))
    lp=A+bis*(arc_r+i_style.label_gap_ratio*U)
    return InclineGeometry(
        A=A,B=B,C=C,base=base,height=height,slope_len=slope_len,
        theta_deg=theta_deg,theta_rad=t,slope_vec=sv,normal_vec=nv,
        block_anchor=P,block_centre=bc,arc_center=A,arc_radius=arc_r,
        arc_label_pos=lp,canvas_w=CANVAS_W_INCL_RATIO*U,canvas_h=CANVAS_H_RATIO*U,
    )

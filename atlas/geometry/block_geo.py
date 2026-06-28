"""Atlas Geometry - BlockGeometry. Pure math. STATUS: FROZEN"""
import math
from dataclasses import dataclass
from atlas.geometry.vectors import Vector2
from atlas.styles.block_style import BlockStyle, BLOCK_STYLE

@dataclass(frozen=True)
class BlockGeometry:
    centre:Vector2; rotation_deg:float; width:float; height:float; rx:float
    top_centre:Vector2; bottom_centre:Vector2; left_centre:Vector2; right_centre:Vector2
    com:Vector2; corners:tuple

def compute_block(cx,cy,U,style=BLOCK_STYLE,rotation_deg=0.0):
    assert U>0
    W=style.width_ratio*U; H=style.height_ratio*U; rx=style.rx_ratio*U
    r=math.radians(rotation_deg); cos_r=math.cos(r); sin_r=math.sin(r)
    def rot(dx,dy): return Vector2(cx+dx*cos_r-dy*sin_r, cy+dx*sin_r+dy*cos_r)
    return BlockGeometry(
        centre=Vector2(cx,cy), rotation_deg=rotation_deg, width=W, height=H, rx=rx,
        top_centre=rot(0,H/2), bottom_centre=rot(0,-H/2),
        left_centre=rot(-W/2,0), right_centre=rot(W/2,0),
        com=Vector2(cx,cy),
        corners=(rot(-W/2,-H/2),rot(W/2,-H/2),rot(W/2,H/2),rot(-W/2,H/2)),
    )

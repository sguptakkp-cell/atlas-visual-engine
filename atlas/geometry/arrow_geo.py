"""Atlas Geometry - ArrowGeometry. HEAD=0.22xL WIDTH=0.10xL SHAFT=0.28xU. STATUS: FROZEN"""
from dataclasses import dataclass
from atlas.geometry.vectors import Vector2
from atlas.styles.arrow_style import ArrowStyle, ARROW_STYLE

@dataclass(frozen=True)
class ArrowGeometry:
    tail:Vector2; head_tip:Vector2; shaft_end:Vector2
    head_base_1:Vector2; head_base_2:Vector2; label_pos:Vector2
    direction:Vector2; perp:Vector2; length:float
    head_len:float; head_width:float; shaft_lw:float

def compute_arrow(tail,direction,length,U,style=ARROW_STYLE):
    assert U>0; assert length>0
    assert abs(direction.magnitude()-1.0)<1e-6,"direction must be unit vector"
    perp=direction.perpendicular_ccw()
    head_len=style.head_ratio*length
    head_width=style.width_ratio*length
    shaft_lw=style.shaft_ratio*U
    head_tip=tail+direction*length
    shaft_end=tail+direction*(length-head_len)
    hw=head_width/2.0
    return ArrowGeometry(
        tail=tail, head_tip=head_tip, shaft_end=shaft_end,
        head_base_1=shaft_end+perp*hw, head_base_2=shaft_end+perp*-hw,
        label_pos=head_tip+perp*style.label_offset_ratio*U,
        direction=direction, perp=perp, length=length,
        head_len=head_len, head_width=head_width, shaft_lw=shaft_lw,
    )

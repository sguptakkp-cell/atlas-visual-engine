"""Atlas Styles - FloorStyle. STATUS: FROZEN"""
from dataclasses import dataclass
from atlas.constants.colors import COLOR_BLACK,COLOR_GROUND,COLOR_HATCH
from atlas.constants.tokens import SURFACE_LW_RATIO,HATCH_DEPTH_RATIO,HATCH_LW_PX,HATCH_SPACING_PX

@dataclass(frozen=True)
class FloorStyle:
    contact_lw_ratio:float=SURFACE_LW_RATIO; contact_color:str=COLOR_BLACK
    hatch_depth_ratio:float=HATCH_DEPTH_RATIO; hatch_fill:str=COLOR_GROUND
    hatch_alpha:float=0.25; hatch_color:str=COLOR_HATCH
    hatch_lw_px:float=HATCH_LW_PX; hatch_spacing_px:int=HATCH_SPACING_PX
    hatch_pattern:str="////"
    def __post_init__(self):
        assert 0<self.hatch_alpha<=1

FLOOR_STYLE=FloorStyle()

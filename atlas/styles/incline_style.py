"""Atlas Styles - InclineStyle. STATUS: FROZEN"""
from dataclasses import dataclass
from atlas.constants.colors import COLOR_GROUND,COLOR_BLACK
from atlas.constants.tokens import INCLINE_BASE_RATIO,INCLINE_SLOPE_LW,INCLINE_BORDER_LW,INCLINE_FILL_ALPHA,ARC_RADIUS_RATIO,ARC_LW_RATIO,ARC_LABEL_SIZE_RATIO,ARC_LABEL_GAP_RATIO,BLOCK_POS_T,FONT_FAMILY,FONT_STYLE,FONT_WEIGHT

@dataclass(frozen=True)
class InclineStyle:
    base_ratio:float=INCLINE_BASE_RATIO; fill:str=COLOR_GROUND; fill_alpha:float=INCLINE_FILL_ALPHA
    hatch_pattern:str="////"; slope_lw:float=INCLINE_SLOPE_LW; border_lw:float=INCLINE_BORDER_LW
    arc_radius_ratio:float=ARC_RADIUS_RATIO; arc_lw_ratio:float=ARC_LW_RATIO
    label_size_ratio:float=ARC_LABEL_SIZE_RATIO; label_gap_ratio:float=ARC_LABEL_GAP_RATIO
    label_font:str=FONT_FAMILY; label_style:str=FONT_STYLE; label_weight:str=FONT_WEIGHT
    label_color:str=COLOR_BLACK; block_pos_t:float=BLOCK_POS_T
    def __post_init__(self):
        assert self.base_ratio>0; assert 0<self.fill_alpha<=1; assert 0<self.block_pos_t<1

INCLINE_STYLE=InclineStyle()

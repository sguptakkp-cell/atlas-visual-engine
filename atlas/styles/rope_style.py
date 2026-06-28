"""Atlas Styles - RopeStyle. TikZ double-stroke. STATUS: FROZEN"""
from dataclasses import dataclass
from atlas.constants.colors import COLOR_ROPE_OUTER,COLOR_ROPE_MID,COLOR_ROPE_HI
from atlas.constants.tokens import ROPE_LW_OUTER_RATIO,ROPE_LW_MID_RATIO,ROPE_LW_HI_RATIO,ROPE_HI_ALPHA,ROPE_LEN_RATIO,CEILING_W_RATIO

@dataclass(frozen=True)
class RopeStyle:
    outer_color:str=COLOR_ROPE_OUTER; mid_color:str=COLOR_ROPE_MID; hi_color:str=COLOR_ROPE_HI
    outer_lw_ratio:float=ROPE_LW_OUTER_RATIO; mid_lw_ratio:float=ROPE_LW_MID_RATIO
    hi_lw_ratio:float=ROPE_LW_HI_RATIO; hi_alpha:float=ROPE_HI_ALPHA
    cap_style:str="round"; len_ratio:float=ROPE_LEN_RATIO; ceiling_w_ratio:float=CEILING_W_RATIO
    def __post_init__(self):
        assert self.outer_lw_ratio>self.mid_lw_ratio>self.hi_lw_ratio>0
        assert self.cap_style=="round"

ROPE_STYLE=RopeStyle()

"""Atlas Styles - ArrowStyle. LOCKED RATIOS: HEAD=0.22 WIDTH=0.10 SHAFT=0.28xU. STATUS: FROZEN"""
from dataclasses import dataclass
from atlas.constants.tokens import ARROW_HEAD_RATIO,ARROW_WIDTH_RATIO,ARROW_SHAFT_RATIO,ARROW_N_RATIO,ARROW_MG_RATIO,ARROW_T_RATIO,ARROW_F_RATIO,LABEL_SIZE_RATIO,LABEL_GAP_RATIO,LABEL_OFFSET_RATIO,ARROW_SCALE_FIXED,ARROW_F_REFERENCE,FONT_FAMILY,FONT_STYLE,FONT_WEIGHT

@dataclass(frozen=True)
class ArrowStyle:
    head_ratio:float=ARROW_HEAD_RATIO; width_ratio:float=ARROW_WIDTH_RATIO; shaft_ratio:float=ARROW_SHAFT_RATIO
    head_style:str="filled_triangle"
    len_N:float=ARROW_N_RATIO; len_mg:float=ARROW_MG_RATIO; len_T:float=ARROW_T_RATIO
    len_f:float=ARROW_F_RATIO; len_F:float=ARROW_F_RATIO
    scaling_policy:str=ARROW_SCALE_FIXED; f_reference:float=ARROW_F_REFERENCE
    label_size_ratio:float=LABEL_SIZE_RATIO; label_gap_ratio:float=LABEL_GAP_RATIO
    label_offset_ratio:float=LABEL_OFFSET_RATIO
    font_family:str=FONT_FAMILY; font_style:str=FONT_STYLE; font_weight:str=FONT_WEIGHT
    def __post_init__(self):
        assert 0<self.head_ratio<1; assert 0<self.width_ratio<1
        assert self.head_ratio>self.width_ratio,"head must be longer than wide"
        assert self.head_style=="filled_triangle","only filled_triangle allowed"
        assert self.scaling_policy in ("fixed","physical")
    def get_length(self,force_name,U,magnitude=None):
        base={"N":self.len_N,"mg":self.len_mg,"T":self.len_T,"f":self.len_f,"F":self.len_F}.get(force_name)
        if base is None: raise ValueError(f"Unknown force '{force_name}'")
        if self.scaling_policy=="fixed": return base*U
        if magnitude is None: raise ValueError("magnitude required for physical scaling")
        return max(0.5*U, min((magnitude/self.f_reference)*self.len_N*U, 4.0*U))

ARROW_STYLE=ArrowStyle()

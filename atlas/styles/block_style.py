"""Atlas Styles - BlockStyle. STATUS: FROZEN"""
from dataclasses import dataclass
from atlas.constants.colors import COLOR_BLOCK, COLOR_BLACK, COLOR_NAVY
from atlas.constants.tokens import BLOCK_W_RATIO,BLOCK_H_RATIO,BLOCK_RX_RATIO,BLOCK_LW_RATIO,COM_R_RATIO,FONT_FAMILY,FONT_STYLE,FONT_WEIGHT,FONT_BLOCK_SIZE_RATIO

@dataclass(frozen=True)
class BlockStyle:
    width_ratio:float=BLOCK_W_RATIO; height_ratio:float=BLOCK_H_RATIO
    rx_ratio:float=BLOCK_RX_RATIO; lw_ratio:float=BLOCK_LW_RATIO; com_r_ratio:float=COM_R_RATIO
    fill:str=COLOR_BLOCK; border:str=COLOR_BLACK; label_color:str=COLOR_NAVY; com_color:str=COLOR_BLACK
    font_family:str=FONT_FAMILY; font_style:str=FONT_STYLE; font_weight:str=FONT_WEIGHT
    label_size_ratio:float=FONT_BLOCK_SIZE_RATIO
    def __post_init__(self):
        assert self.width_ratio>0; assert self.height_ratio>0
        assert self.rx_ratio>=0; assert self.lw_ratio>0

BLOCK_STYLE=BlockStyle()

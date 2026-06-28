"""Atlas Styles - CanvasStyle. STATUS: FROZEN"""
from dataclasses import dataclass
from atlas.constants.colors import COLOR_BG
from atlas.constants.tokens import CANVAS_H_RATIO,CANVAS_W_RATIO,CANVAS_W_INCL_RATIO,CANVAS_MARGIN_RATIO,DPI_SCREEN,DPI_TABLET,DPI_PRINT

@dataclass(frozen=True)
class CanvasStyle:
    h_ratio:float=CANVAS_H_RATIO; w_ratio:float=CANVAS_W_RATIO
    w_incl_ratio:float=CANVAS_W_INCL_RATIO; margin_ratio:float=CANVAS_MARGIN_RATIO
    bg_color:str=COLOR_BG; dpi_screen:int=DPI_SCREEN; dpi_tablet:int=DPI_TABLET
    dpi_print:int=DPI_PRINT; backend:str="Agg"
    def __post_init__(self):
        assert self.h_ratio>0 and self.w_ratio>0
        assert self.backend=="Agg","only Agg backend permitted in Phase 1"

CANVAS_STYLE=CanvasStyle()

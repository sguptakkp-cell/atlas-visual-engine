"""
Atlas Constants - Tokens. Single source of truth for ALL dimensions.
U = canvas_height / 10. Every dimension = ratio * U. STATUS: FROZEN
"""
CANVAS_H_RATIO=10.0; CANVAS_W_RATIO=8.0; CANVAS_W_INCL_RATIO=12.0; CANVAS_MARGIN_RATIO=0.6
DPI_SCREEN=200; DPI_TABLET=150; DPI_PRINT=300
BLOCK_W_RATIO=2.2; BLOCK_H_RATIO=1.4; BLOCK_RX_RATIO=0.05; BLOCK_LW_RATIO=0.18  # FROZEN
COM_R_RATIO=0.015
ARROW_HEAD_RATIO=0.22; ARROW_WIDTH_RATIO=0.10  # ratios — dimensionless, × L (data units)
ARROW_N_RATIO=3.2; ARROW_MG_RATIO=2.8; ARROW_T_RATIO=3.0; ARROW_F_RATIO=2.4  # × U → data units
ARROW_SHAFT_LW_PT=2.0; ARROW_LABEL_SIZE_PT=12.0  # fixed pt — never × U
BLOCK_LW_PT=1.5; SURFACE_LW_PT=2.0; ARC_LW_PT=1.2  # fixed pt — never × U
ARROW_SCALE_FIXED="fixed"; ARROW_SCALE_PHYSICAL="physical"
ARROW_F_REFERENCE=9.8
LABEL_SIZE_RATIO=1.7; LABEL_GAP_RATIO=0.15
SPACING_S_RATIO=0.083            # s = block_W/12 — universal spacing unit
LABEL_OFFSET_RATIO=3.0*SPACING_S_RATIO  # 3s from arrowhead tip (≈ 0.249)
SURFACE_LW_RATIO=0.30; HATCH_DEPTH_RATIO=0.55; HATCH_LW_PX=1.1; HATCH_SPACING_PX=14
ROPE_LW_OUTER_PT=5.0; ROPE_LW_MID_PT=3.0; ROPE_LW_HI_PT=1.2  # fixed pts — never × U
ROPE_HI_ALPHA=0.60; ROPE_LEN_RATIO=3.50; CEILING_W_RATIO=5.50
INCLINE_BASE_RATIO=12.0; INCLINE_SLOPE_LW=2.5; INCLINE_BORDER_LW=1.8; INCLINE_FILL_ALPHA=0.22
ARC_RADIUS_RATIO=0.30; ARC_LW_RATIO=0.14; ARC_LABEL_SIZE_RATIO=2.2; ARC_LABEL_GAP_RATIO=0.30
BLOCK_POS_T=0.55
BLOCK_REL_SLOPE_MULTIPLIER=5.5   # slope length = 5.5 × block_width (block is 18% of slope)
HATCH_SPACING_BLOCK=0.09          # incline hatch spacing reference = 0.09 × block_width
ARC_RADIUS_BLOCK=0.60             # angle arc radius = 0.60 × block_width
LABEL_OFFSET_BLOCK=0.30           # label offset = 0.30 × block_width
INCLINE_RENDER_ANGLE_DEG=20.0        # AER-001: visual angle always 20°, physics in label
INCLINE_ANGLE_LABEL="θ"              # FROZEN: angle label is θ symbol only, no numbers
ALLOWED_ANGLES_DEG={0,30,37,45,53,60,90}
TRIG={37:{"sin":0.6,"cos":0.8,"tan":0.75},53:{"sin":0.8,"cos":0.6,"tan":1.333}}
Z_GROUND_HATCH=1; Z_GROUND_LINE=2; Z_ROPE=3; Z_INCLINE_FILL=4; Z_INCLINE_BORDER=5
Z_BLOCK_FILL=6; Z_BLOCK_BORDER=7; Z_COM_DOT=8; Z_ARROW_SHAFT=9; Z_ARROW_HEAD=10
Z_FORCE_LABEL=11; Z_ANGLE_ARC=12; Z_ANGLE_LABEL=13; Z_ANNOTATION=14
FONT_FAMILY="DejaVu Serif"; FONT_STYLE="italic"; FONT_WEIGHT="bold"
FONT_BLOCK_SIZE_RATIO=16.0   # fixed pts for block label (× U → pt)

def compute_tokens(U):
    return {
        "U":U,"canvas_h":CANVAS_H_RATIO*U,"canvas_w":CANVAS_W_RATIO*U,
        "block_w":BLOCK_W_RATIO*U,"block_h":BLOCK_H_RATIO*U,"block_rx":BLOCK_RX_RATIO*U,
        "arrow_head":ARROW_HEAD_RATIO,"arrow_width":ARROW_WIDTH_RATIO,
        "arrow_shaft_lw":ARROW_SHAFT_RATIO*U,
        "arrow_n_len":ARROW_N_RATIO*U,"arrow_mg_len":ARROW_MG_RATIO*U,
        "label_size":LABEL_SIZE_RATIO*U,"arc_radius":ARC_RADIUS_RATIO*U,
    }

def print_spec_report(canvas_height=6.0):
    U=canvas_height/10; t=compute_tokens(U)
    bar="─"*52
    print(f"\n{bar}\n  Atlas Visual Engine — Spec Report")
    print(f"  canvas_height={canvas_height}  U={U:.4f}\n{bar}")
    print(f"  Canvas  {t['canvas_w']:.3f} x {t['canvas_h']:.3f}")
    print(f"  Block   {t['block_w']:.3f} x {t['block_h']:.3f}  rx={t['block_rx']:.3f}")
    print(f"  Arrow   HEAD={ARROW_HEAD_RATIO}xL  WIDTH={ARROW_WIDTH_RATIO}xL  SHAFT={t['arrow_shaft_lw']:.3f}pt (fixed)")
    print(f"  N={t['arrow_n_len']:.3f}  mg={t['arrow_mg_len']:.3f}")
    print(f"  Label   {t['label_size']:.3f}pt")
    print(f"  Arc_r   {t['arc_radius']:.3f}\n{bar}\n")

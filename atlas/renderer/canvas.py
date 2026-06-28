"""Atlas Renderer - canvas factory and save helper."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from atlas.styles.canvas_style import CanvasStyle, CANVAS_STYLE


def fig_clean(U: float = 0.6, scenario: str = "default",
              canvas_w: float = None, canvas_h: float = None,
              style: CanvasStyle = CANVAS_STYLE):
    """Return (fig, ax) for the given canvas dimensions.

    Pass canvas_w/canvas_h to override ratio-based sizing (e.g. for block-relative inclines).
    scenario="default"  → 8U × 10U
    scenario="incline"  → 12U × 10U  (only used when canvas_w/canvas_h are None)
    """
    if canvas_w is None:
        w_ratio = style.w_incl_ratio if scenario == "incline" else style.w_ratio
        canvas_w = w_ratio * U
    if canvas_h is None:
        canvas_h = style.h_ratio * U
    fig, ax = plt.subplots(figsize=(canvas_w, canvas_h))
    fig.patch.set_facecolor(style.bg_color)
    ax.set_facecolor(style.bg_color)
    ax.set_xlim(0, canvas_w)
    ax.set_ylim(0, canvas_h)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, filename: str, dpi: int = None, style: CanvasStyle = CANVAS_STYLE) -> str:
    """Save fig to filename at given DPI; close fig; return filepath."""
    if dpi is None:
        dpi = style.dpi_screen
    if not filename.endswith((".png", ".pdf", ".svg")):
        filename += ".png"
    dirpart = os.path.dirname(filename)
    if dirpart:
        os.makedirs(dirpart, exist_ok=True)
    fig.savefig(filename, dpi=dpi, bbox_inches="tight", facecolor=style.bg_color)
    plt.close(fig)
    return filename

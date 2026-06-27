"""
Atlas Visual Engine
===================

canvas.py

Core Canvas class for Atlas.
"""

from matplotlib import pyplot as plt

from atlas.core.renderer import Renderer

from atlas.constants import (
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    BACKGROUND_COLOR,
    SHOW_GRID,
    SHOW_AXES,
    DEFAULT_DPI,
    DEFAULT_FORMAT,
)


class Canvas:
    """
    Atlas drawing canvas.
    """

    def __init__(self):
        self.figure, self.axes = plt.subplots(
            figsize=(CANVAS_WIDTH, CANVAS_HEIGHT)
        )

        self.axes.set_facecolor(BACKGROUND_COLOR)

        self.axes.grid(SHOW_GRID)

        if not SHOW_AXES:
            self.axes.set_axis_off()

        self.renderer = Renderer()

    def set_title(self, title: str):
        """Set the canvas title."""
        self.axes.set_title(title)

    def save(self, filename: str):
        """Save the figure."""

        if "." not in filename:
            filename += "." + DEFAULT_FORMAT

        self.figure.savefig(
            filename,
            dpi=DEFAULT_DPI,
        )

    def render(self, scene):
        """
        Render a Scene.
        """
        self.renderer.render(self, scene)

    def show(self):
        """Display the canvas."""
        plt.show()

    def close(self):
        """Close the canvas."""
        plt.close(self.figure)
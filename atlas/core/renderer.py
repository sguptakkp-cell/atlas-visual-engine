"""
Atlas Visual Engine
===================

renderer.py

Responsible for rendering Atlas primitives.
"""

from atlas.primitives.line import Line


class Renderer:
    """
    Atlas rendering engine.
    """

    def render(self, canvas, scene):
        """
        Render every object inside the scene.
        """

        for obj in scene.objects:

            if isinstance(obj, Line):

                canvas.axes.plot(
                    [obj.x1, obj.x2],
                    [obj.y1, obj.y2],
                    color=obj.color,
                    linewidth=obj.linewidth,
                )
from atlas.core.canvas import Canvas
from atlas.core.scene import Scene
from atlas.core.renderer import Renderer

from atlas.primitives.line import Line


canvas = Canvas()

scene = Scene()

scene.add(Line(1, 1, 8, 6))

renderer = Renderer()

renderer.render(canvas, scene)

canvas.set_title("Atlas First Renderer")

canvas.save("renderer_test")

canvas.show()

canvas.close()
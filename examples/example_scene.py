from atlas.core.scene import Scene
from atlas.primitives.line import Line

scene = Scene()

scene.add(Line(0, 0, 5, 3))
scene.add(Line(5, 3, 8, 1))

print("Objects in scene:", len(scene))
"""
Atlas Visual Engine
===================

scene.py

Stores drawable objects.
"""


class Scene:
    """
    Collection of drawable objects.
    """

    def __init__(self):
        self.objects = []

    def add(self, obj):
        """
        Add a drawable object.
        """
        self.objects.append(obj)

    def clear(self):
        """
        Remove all objects.
        """
        self.objects.clear()

    def __len__(self):
        return len(self.objects)
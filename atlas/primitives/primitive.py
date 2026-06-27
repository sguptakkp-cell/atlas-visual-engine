"""
Atlas Visual Engine
===================

primitive.py

Base class for every drawable object.
"""

from dataclasses import dataclass


@dataclass
class Primitive:
    """
    Base class for all Atlas primitives.
    """

    visible: bool = True

    layer: int = 0
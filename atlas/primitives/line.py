"""
Atlas Visual Engine
===================

line.py

Line primitive.
"""

from dataclasses import dataclass

from atlas.primitives.primitive import Primitive


@dataclass
class Line(Primitive):
    """
    Represents a straight line.
    """

    x1: float = 0
    y1: float = 0

    x2: float = 0
    y2: float = 0

    color: str = "black"

    linewidth: float = 2.0
"""Atlas Physics - Force object. STATUS: FROZEN"""
from dataclasses import dataclass
from atlas.geometry.vectors import Vector2
from atlas.constants.colors import get_force_color

@dataclass(frozen=True)
class Force:
    name:str; magnitude:float; direction:Vector2; tail:Vector2
    label:str=""; color:str=""
    def __post_init__(self):
        assert self.magnitude>=0
        assert abs(self.direction.magnitude()-1.0)<1e-6,"direction must be unit vector"
        if not self.color: object.__setattr__(self,"color",get_force_color(self.name))
        if not self.label: object.__setattr__(self,"label",self.name)

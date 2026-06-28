"""Atlas Geometry - Vectors. Pure math. Zero matplotlib. STATUS: FROZEN"""
import math
from dataclasses import dataclass

@dataclass(frozen=True)
class Vector2:
    x:float; y:float
    def __add__(self,o): return Vector2(self.x+o.x, self.y+o.y)
    def __sub__(self,o): return Vector2(self.x-o.x, self.y-o.y)
    def __mul__(self,s): return Vector2(self.x*s, self.y*s)
    def __rmul__(self,s): return self.__mul__(s)
    def magnitude(self): return math.sqrt(self.x**2+self.y**2)
    def unit(self):
        m=self.magnitude()
        if m<1e-10: raise ValueError("Cannot normalize zero vector")
        return Vector2(self.x/m, self.y/m)
    def perpendicular_ccw(self): return Vector2(-self.y, self.x)
    def perpendicular_cw(self):  return Vector2( self.y,-self.x)
    def dot(self,o): return self.x*o.x+self.y*o.y
    def rotate_deg(self,deg):
        r=math.radians(deg)
        return Vector2(self.x*math.cos(r)-self.y*math.sin(r), self.x*math.sin(r)+self.y*math.cos(r))
    def as_tuple(self): return (self.x,self.y)
    def __repr__(self): return f"V2({self.x:.4f},{self.y:.4f})"

UNIT_UP=Vector2(0,1); UNIT_DOWN=Vector2(0,-1)
UNIT_RIGHT=Vector2(1,0); UNIT_LEFT=Vector2(-1,0)

def from_angle_deg(deg):
    r=math.radians(deg); return Vector2(math.cos(r),math.sin(r))

def slope_vectors(theta_deg):
    t=math.radians(theta_deg)
    return Vector2(math.cos(t),math.sin(t)), Vector2(-math.sin(t),math.cos(t))

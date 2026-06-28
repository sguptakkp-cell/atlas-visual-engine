"""Atlas Physics - InclineModel. Pure physics. Zero rendering. STATUS: FROZEN"""
import math
from dataclasses import dataclass
from atlas.geometry.vectors import Vector2, slope_vectors, UNIT_DOWN
from atlas.physics.force import Force
from atlas.constants.tokens import ALLOWED_ANGLES_DEG

@dataclass(frozen=True)
class InclineInput:
    theta_deg:float; mu:float; mass:float=1.0; g:float=9.8
    u0:float=0.0; active_forces:tuple=("N","mg","f")

@dataclass(frozen=True)
class InclineFrame:
    time:float; position:Vector2; velocity:Vector2; acceleration:Vector2
    forces:tuple; is_sliding:bool; theta_deg:float; theta_rad:float
    slope_vec:Vector2; normal_vec:Vector2

def compute_frame(inp,t,block_centre):
    assert t>=0; assert 0<=inp.mu<1; assert inp.mass>0
    assert inp.theta_deg in ALLOWED_ANGLES_DEG
    theta=math.radians(inp.theta_deg)
    sv,nv=slope_vectors(inp.theta_deg)
    N_mag=inp.mass*inp.g*math.cos(theta)
    mg_mag=inp.mass*inp.g
    f_mag=inp.mu*N_mag
    a=(mg_mag*math.sin(theta)-f_mag)/inp.mass
    v=inp.u0+a*t; s=max(0.0,inp.u0*t+0.5*a*t**2)
    forces=[]
    if "N"  in inp.active_forces: forces.append(Force("N", N_mag, nv,       block_centre))
    if "mg" in inp.active_forces: forces.append(Force("mg",mg_mag,UNIT_DOWN, block_centre))
    if "f"  in inp.active_forces and f_mag>0:
        fd=sv  # friction opposes motion: block slides down, so f points up slope
        forces.append(Force("f",f_mag,fd,block_centre))
    return InclineFrame(
        time=t,position=sv*s,velocity=sv*v,acceleration=sv*a,
        forces=tuple(forces),is_sliding=abs(v)>1e-4 or abs(a)>1e-4,
        theta_deg=inp.theta_deg,theta_rad=theta,slope_vec=sv,normal_vec=nv,
    )

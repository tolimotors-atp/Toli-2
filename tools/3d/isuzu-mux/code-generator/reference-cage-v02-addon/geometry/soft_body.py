"""Reference-informed primary surfacing; detail gate remains separate."""
import math
from .rounded import generate_rounded,at_x,samples
SURFACE_CLASSES={
 'A_SOFT':{'regions':['bonnet crown','door skins','roof crown','quarter volume'],'strategy':'broad monotone cubic ribbons'},
 'B_CONTROLLED':{'regions':['fender return','shoulder','bumper corner'],'strategy':'nearby support rails and localized axle influence'},
 'C_DEFINED':{'regions':['glass/lamp/grille boundaries','panel separations'],'strategy':'retain construction boundaries; not detailed before clay approval'},
}

def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def profile(x,p,rail):
 L=p['length'];half=p['width']/2
 hood=at_x(rail['CURVE_BONNET_CENTER'],x);roof=at_x(rail['CURVE_ROOF_CENTER'],x);master=at_x(rail['CURVE_SIDE_MASTER'],x);belt=at_x(rail['CURVE_BELT'],x);shoulder=at_x(rail['CURVE_SHOULDER'],x);lower=at_x(rail['CURVE_LOWER_BODY'],x);sill=at_x(rail['CURVE_SILL'],x)
 cowl=-.19*L;roof_start=-.08*L;roof_end=.37*L;rear_base=.475*L
 # Shared center profile: the old hard switches at cowl/roof are removed.
 if x<cowl:
  t=smooth((x/L+.25)/.06);top=hood.z+(p['height']*.70-hood.z)*t
 elif x<roof_start:
  t=(x-cowl)/(roof_start-cowl);top=p['height']*(.70+(.96-.70)*(t*.70+smooth(t)*.30))
 elif x<roof_end:top=roof.z
 else:
  t=smooth((x-roof_end)/(rear_base-roof_end));top=rail['CURVE_ROOF_CENTER'][-1].z*(1-t)+p['height']*.70*t
  if x>rear_base:top-=.10*smooth((x-rear_base)/(.025*L))
 u=abs(x)/(L/2);end=smooth((u-.82)/.18);taper=1-.09*end
 w=min(half,shoulder.y)*.985
 for axle,name in [(-p['wheelbase']/2,'CURVE_FRONT_FENDER_CROWN'),(p['wheelbase']/2,'CURVE_REAR_FENDER_CROWN')]:
  influence=math.exp(-((x-axle)/.48)**4);crown=at_x(rail[name],x);w+=(min(half,crown.y)-w)*influence
 w=min(half,w)*taper
 side_top=min(shoulder.z,top-.12);belt_z=min(belt.z,top-.075)
 cabin=smooth((top-belt.z)/.28);roof_edge=at_x(rail['CURVE_ROOF_LEFT_EDGE'],x).y;edge_y=w*.85*(1-cabin)+min(w*.86,roof_edge)*cabin
 base=p['ground_clearance'];lower_z=max(base+.12,min(lower.z,side_top-.18))
 # Class A convex skins; Class B close support rails retain a shallow shoulder.
 return [(0,base),(w*.77,base),(w*.90,max(base+.035,sill.z)),(w*.95,lower_z),(w*.984,min(.76,side_top-.07)),(w*.996,side_top-.035),(w,side_top),(w*.992,side_top+.020),(min(w*.98,belt.y),belt_z),(edge_y,top-.04),(edge_y*.55,top-.006),(0,top)]

def generate_soft(scene,p):
 return generate_rounded(scene,p,profile_function=profile)

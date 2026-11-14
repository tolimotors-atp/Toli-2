"""Bezier engine. The actual curve datablocks are the first-stage output."""
import bpy,math
from ..mux_curve_data import CURVES,CLOSED,MIRROR
COLLECTION='TOLI_MUX_CONSTRUCTION'
def clear():
 col=bpy.data.collections.get(COLLECTION)
 if col:
  for o in list(col.objects):
   d=o.data;bpy.data.objects.remove(o,do_unlink=True)
   if d.users==0:bpy.data.curves.remove(d)
  bpy.data.collections.remove(col)
def curve(col,name,coords,closed=False,quality=False):
 data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.resolution_u=24 if quality else 12;data.bevel_depth=.003;data.bevel_resolution=1
 s=data.splines.new('BEZIER');s.bezier_points.add(len(coords)-1);s.use_cyclic_u=closed
 for bp,co in zip(s.bezier_points,coords):bp.co=co;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
 if name in ['CURVE_ROOF_CENTER','CURVE_SIDE_MASTER']:
  pts=s.bezier_points
  for i,bp in enumerate(pts):
   prev=pts[max(0,i-1)].co.copy();co=bp.co.copy();nxt=pts[min(len(pts)-1,i+1)].co.copy();left=max(1e-6,co.x-prev.x);right=max(1e-6,nxt.x-co.x);slope=[]
   for k in [1,2]:
    a=(co[k]-prev[k])/left;b=(nxt[k]-co[k])/right
    slope.append(2*a*b/(a+b) if a*b>0 else 0)
   bp.handle_left_type='FREE';bp.handle_right_type='FREE'
   bp.handle_left=(co.x-left/3,co.y-slope[0]*left/3,co.z-slope[1]*left/3);bp.handle_right=(co.x+right/3,co.y+slope[0]*right/3,co.z+slope[1]*right/3)
 o=bpy.data.objects.new(name,data);col.objects.link(o);o.color=(.1,.6,.9,1)
 m=bpy.data.materials.get('MUX construction cyan') or bpy.data.materials.new('MUX construction cyan');m.diffuse_color=(.025,.5,.8,1);data.materials.append(m)
 return o

def generate_curves(scene,p):
 clear();col=bpy.data.collections.new(COLLECTION);scene.collection.children.link(col);quality=p['quality']=='QUALITY'
 def add(name,points,closed=False,mirror=False):
  coords=[]
  for x,y,z in points:
   xx=x*p['length'];yy=y*p['width']/2;zz=z*p['height']
   if 'BONNET_CENTER' in name:zz+=p['bonnet_height']-1.13
   if 'ROOF_CENTER' in name:zz+=p['roof_crown']-.055
   if 'SHOULDER' in name or 'BELT' in name:zz+=p['belt_height']-1.19
   if 'FENDER_CROWN' in name:zz+=p['fender_bulge']-.025
   if 'A_PILLAR' in name or 'WINDSCREEN_TOP' in name:xx+=(p['windscreen_run']-.50)*max(0,(z-.69)/.27)
   if x>.20:yy*=1-(p['rear_taper']-.08)*(x-.20)/.30
   coords.append((xx,yy,zz))
  curve(col,name,coords,closed,quality)
  if mirror:curve(col,name.replace('_LEFT','_RIGHT') if '_LEFT' in name else name+'_MIRROR',[(x,-y,z) for x,y,z in coords],closed,quality)
 for name,points in CURVES.items():add(name,points,name in CLOSED,name in MIRROR)
 for axle,x in [('FRONT',-p['wheelbase']/2),('REAR',p['wheelbase']/2)]:
  r=p['tire_diameter']/2;pts=[]
  for i in range(9):
   t=math.pi-i*math.pi/8;rx=r+(.075 if math.cos(t)<0 else .06);pts.append(((x+rx*math.cos(t))/p['length'],1,(r+(r+.07)*math.sin(t))/p['height']))
  add('CURVE_'+axle+'_ARCH',pts,mirror=True)
  add('CURVE_'+axle+'_FENDER_CROWN',[(xx,yy,zz+.045) for xx,yy,zz in pts],mirror=True)
 # A transverse network, explicitly curves rather than box-mesh sections.
 for i,x in enumerate([-.48,-.30,-.18,0,.20,.30,.45]):
  add(f'CURVE_SECTION_{i:02d}',[(x,-.92,.24),(x,-1,.48),(x,-.96,.65),(x,0,.69),(x,.96,.65),(x,1,.48),(x,.92,.24)])
 return col

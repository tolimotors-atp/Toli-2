import bpy,json,math
from pathlib import Path
from mathutils import Vector
from ..traced_data import TRACES,SOURCES,ANCHORS
COL='TOLI_MUX_REFERENCE_CAGE'
COLORS={'silhouette':(.95,.30,.08,1),'greenhouse':(.1,.65,1,1),'front':(1,.8,.1,1),'rear':(.8,.2,1,1),'character':(.1,1,.35,1),'section':(.65,.65,.65,1)}
def category(name,source):
 if source in ['front','rear']:return source
 if any(t in name for t in ['WINDOW','GLASS','PILLAR','ROOF','WINDSCREEN']):return 'greenhouse'
 return 'silhouette' if name=='SIDE_MASTER' else 'character'
def side_x(u,p):
 knots=[(144,-p['length']/2),(284,-p['wheelbase']/2),(776,p['wheelbase']/2),(928,p['length']/2)]
 for (u0,x0),(u1,x1) in zip(knots,knots[1:]):
  if u<=u1:return x0+(u-u0)/(u1-u0)*(x1-x0)
 return knots[-1][1]
def project(source,pixel,depth,p):
 u,v=pixel
 if source=='side':return Vector((side_x(u,p),-depth*p['width']/2,(455-v)/331*p['height']))
 center=ANCHORS[source+'_center'];half=ANCHORS[source+'_half_body']
 # Inferred vertical registration at roof/cowl/ground, not a solved camera.
 knots=[(132,1.86),(249,1.30),(350,.88),(480,0)] if source=='front' else [(140,1.86),(257,1.30),(413,.28),(476,0)]
 z=0
 for (v0,z0),(v1,z1) in zip(knots,knots[1:]):
  if v<=v1:z=z0+(v-v0)/(v1-v0)*(z1-z0);break
 return Vector((depth*p['length'],-abs(u-center)/half*p['width']/2,z*p['height']/1.86))
def make(col,name,coords,kind,closed=False):
 data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.resolution_u=16;data.bevel_depth=.0025;data.bevel_resolution=1;s=data.splines.new('BEZIER');s.bezier_points.add(len(coords)-1);s.use_cyclic_u=closed
 # Explicit FREE handles: chord-aligned at corners, centred tangent on smooth runs.
 for i,(bp,co) in enumerate(zip(s.bezier_points,coords)):
  prev=coords[(i-1)%len(coords)] if closed else coords[max(0,i-1)];nxt=coords[(i+1)%len(coords)] if closed else coords[min(len(coords)-1,i+1)];tangent=(nxt-prev)/6;bp.co=co;bp.handle_left_type='FREE';bp.handle_right_type='FREE';bp.handle_left=co-tangent;bp.handle_right=co+tangent
 o=bpy.data.objects.new(name,data);col.objects.link(o);m=bpy.data.materials.get('Cage '+kind) or bpy.data.materials.new('Cage '+kind);m.diffuse_color=COLORS[kind];m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=COLORS[kind];bs.inputs['Emission Color'].default_value=COLORS[kind];bs.inputs['Emission Strength'].default_value=.35;data.materials.append(m);o['trace_class']=kind;return o

def generate_cage(scene,p):
 old=bpy.data.collections.get(COL)
 if old:
  for o in list(old.objects):
   d=o.data;bpy.data.objects.remove(o,do_unlink=True)
   if d.users==0:bpy.data.curves.remove(d)
  bpy.data.collections.remove(old)
 col=bpy.data.collections.new(COL);scene.collection.children.link(col)
 for name,(source,pixels,depth,closed) in TRACES.items():
  points=[project(source,uv,depth,p) for uv in pixels];kind=category(name,source)
  if name=='SIDE_MASTER':points=[Vector((v.x,(-.74 if v.z>1.5 else -.94)*p['width']/2,v.z)) for v in points]
  make(col,'TRACE_'+name,points,kind,closed);make(col,'TRACE_'+name+'_R',[Vector((v.x,-v.y,v.z)) for v in points],kind,closed)
  for o in [col.objects['TRACE_'+name],col.objects['TRACE_'+name+'_R']]:o['source']=SOURCES[source];o['pixel_points']=json.dumps(pixels);o['depth']='Inferred; not calibrated'
 # A few transverse links share exact sampled cage landmarks; do not invent body panels.
 for n in ['BONNET_FRONT','WINDSCREEN_TOP','WINDSCREEN_BOTTOM','FRONT_ROOF']:
  left=col.objects['TRACE_'+n].data.splines[0].bezier_points[0].co.copy();make(col,'LINK_'+n,[left,Vector((left.x,0,left.z+.025)),Vector((left.x,-left.y,left.z))],'section')
 return col

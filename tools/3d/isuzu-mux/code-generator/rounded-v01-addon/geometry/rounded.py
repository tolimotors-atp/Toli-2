"""Body patches sampled from actual generated Blender Bezier rails."""
import bpy,math,bmesh
from mathutils import Vector
from mathutils.geometry import interpolate_bezier
from .curves import generate_curves,COLLECTION
from . import mesh,material
from ..surfaces import symmetric_bake
ROUNDED='TOLI_MUX_CURVE_ROUNDED'
RADII={'body_edge_radius':.006,'arch_lip_radius':.012,'bumper_edge_radius':.045,'shoulder_radius':.025,'sill_radius':.035}

def samples(name,res=12):
 o=bpy.data.collections[COLLECTION].objects[name];s=o.data.splines[0];p=s.bezier_points;out=[]
 for a,b in zip(p,p[1:]):out.extend(interpolate_bezier(a.co,a.handle_right,b.handle_left,b.co,res)[:-1])
 out.append(p[-1].co.copy());return out

def at_x(points,x):
 # All longitudinal rails are monotone in X; endpoint extension is bounded to the fascia.
 if x<=points[0].x:return points[0].copy()
 for a,b in zip(points,points[1:]):
  if x<=b.x:return a.lerp(b,(x-a.x)/max(1e-9,b.x-a.x))
 return points[-1].copy()

def catmull(points,steps):
 # Monotone cubic component tangents prevent width/height overshoot at crowns.
 def slope(a,b):return 2*a*b/(a+b) if a*b>0 else 0
 out=[]
 for i in range(len(points)):
  a,b,c,d=[Vector(points[j%len(points)]) for j in [i-1,i,i+1,i+2]]
  m0=Vector([slope(b[k]-a[k],c[k]-b[k]) for k in range(2)]);m1=Vector([slope(c[k]-b[k],d[k]-c[k]) for k in range(2)])
  for n in range(steps):
   t=n/steps;out.append((2*t**3-3*t*t+1)*b+(t**3-2*t*t+t)*m0+(-2*t**3+3*t*t)*c+(t**3-t*t)*m1)
 return out

def generate_rounded(scene,p):
 generate_curves(scene,p);old=bpy.data.collections.get(ROUNDED)
 if old:
  for o in list(old.objects):
   d=o.data;bpy.data.objects.remove(o,do_unlink=True)
   if d.users==0:bpy.data.meshes.remove(d)
  bpy.data.collections.remove(old)
 col=bpy.data.collections.new(ROUNDED);scene.collection.children.link(col)
 paint=material('Rounded neutral clay',(.42,.44,.46));rubber=material('Rounded tire',(.018,.02,.024));metal=material('Rounded rim',(.40,.43,.46),.6)
 names=['CURVE_SIDE_MASTER','CURVE_BONNET_CENTER','CURVE_ROOF_CENTER','CURVE_SHOULDER','CURVE_BELT','CURVE_LOWER_BODY','CURVE_SILL'];rail={n:samples(n,24 if p['quality']=='QUALITY' else 12) for n in names}
 count=97 if p['quality']=='QUALITY' else 57;steps=5 if p['quality']=='QUALITY' else 3;sections=[]
 for i in range(count):
  x=(-.5+i/(count-1))*p['length'];master=at_x(rail['CURVE_SIDE_MASTER'],x);shoulder=at_x(rail['CURVE_SHOULDER'],x);belt=at_x(rail['CURVE_BELT'],x);lower=at_x(rail['CURVE_LOWER_BODY'],x);sill=at_x(rail['CURVE_SILL'],x)
  # End radius varies longitudinal width; no global bevel supplies the main curvature.
  u=abs(x)/(p['length']/2);end=max(0,(u-.82)/.18);taper=1-.11*end*end*(3-2*end)
  w=min(p['width']/2,shoulder.y)*taper;top=master.z
  if x<-.18*p['length']:top=at_x(rail['CURVE_BONNET_CENTER'],x).z
  elif -.08*p['length']<x<.37*p['length']:top=at_x(rail['CURVE_ROOF_CENTER'],x).z
  cabin=max(0,min(1,(top-belt.z)/.30));edge_y=w*(1-.25*cabin);side_top=min(shoulder.z,top-.055);base=p['ground_clearance']
  # Distinct surface ribbons share these exact rail samples and their tangents.
  half=[(0,base),(w*.78,base),(w*.91,max(base+.035,sill.z+RADII['sill_radius']*.1)),(w*.965,lower.z),(w,.77),(w,side_top-RADII['shoulder_radius']*1.8),(w*.99,side_top),(edge_y,top-.065),(edge_y*.55,top-RADII['body_edge_radius']*2),(0,top)]
  yz=half+[(-y,z) for y,z in reversed(half[1:-1])];sections.append([(x,v.x,v.y) for v in catmull(yz,steps)])
 # Rounded fascia caps: shared outer ring, progressively inset rings, not n-gon planes.
 for index,sign in [(0,-1),(-1,1)]:
  ring=sections[index];sections[index]=[(x-sign*(RADII['bumper_edge_radius']*3.111111111)*(abs(y)/(p['width']/2))**2,y,z) for x,y,z in ring]
 body=mesh('MUX_CURVE_SURFACE_PATCHES',sections,paint,col)
 data=body.data;verts=[tuple(v.co) for v in data.vertices];faces=[tuple(poly.vertices) for poly in list(data.polygons)[:-2]];n=len(sections[0])
 for index,sign in [(0,-1),(len(sections)-1,1)]:
  boundary=list(range(index*n,(index+1)*n));ring=[Vector(verts[k]) for k in boundary];zmid=(min(v.z for v in ring)+max(v.z for v in ring))/2;center=Vector((sign*p['length']/2,0,zmid))
  for factor in [.75,.50,.25]:
   indices=[]
   for v in ring:
    co=center+(v-center)*factor;co.x=center.x+(v.x-center.x)*factor*factor;indices.append(len(verts));verts.append(tuple(co))
   for j in range(n):faces.append((boundary[j],boundary[(j+1)%n],indices[(j+1)%n],indices[j]))
   boundary=indices
  c=len(verts);verts.append(tuple(center))
  for j in range(n):faces.append((boundary[j],boundary[(j+1)%n],c))
 fresh=bpy.data.meshes.new('Shared rounded patches');fresh.from_pydata(verts,[],faces);fresh.materials.append(paint);body.data=fresh;bpy.data.meshes.remove(data)
 bm=bmesh.new();bm.from_mesh(fresh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(fresh);bm.free()
 for poly in fresh.polygons:poly.use_smooth=True
 # The cutter follows the Bezier arch itself, then closes below the ground plane.
 for name in ['CURVE_FRONT_ARCH','CURVE_REAR_ARCH']:
  arc=samples(name,8 if p['quality']=='QUALITY' else 5);profile=[(arc[0].x,-.1)]+[(v.x,v.z) for v in arc]+[(arc[-1].x,-.1)]
  cutter=mesh('Bezier arch cutter',[[(x,y,z) for x,z in profile] for y in [-p['width'],p['width']]],None,col)
  mod=body.modifiers.new('Bezier wheel opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=mod.name);data=cutter.data;bpy.data.objects.remove(cutter,do_unlink=True);bpy.data.meshes.remove(data)
 lip=body.modifiers.new('Local hard-cut arch lip radius','BEVEL');lip.width=RADII['arch_lip_radius'];lip.segments=3;lip.limit_method='ANGLE';lip.angle_limit=.7
 symmetric_bake(body)
 # Evaluate the mirror, then establish outward winding on the closed assembled body.
 deps=bpy.context.evaluated_depsgraph_get();closed=bpy.data.meshes.new_from_object(body.evaluated_get(deps),depsgraph=deps);old=body.data;body.modifiers.clear();body.data=closed
 if old.users==0:bpy.data.meshes.remove(old)
 bm=bmesh.new();bm.from_mesh(closed);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
 bm.to_mesh(closed);bm.free()
 for axle,x in [('F',-p['wheelbase']/2),('R',p['wheelbase']/2)]:
  for side,y in [('L',-p['track']/2),('R',p['track']/2)]:
   for label,radius,depth,mat in [('TIRE',p['tire_diameter']/2,.24,rubber),('RIM',p['tire_diameter']*.31,.245,metal)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=64 if p['quality']=='QUALITY' else 40,radius=radius,depth=depth,location=(x,y,p['tire_diameter']/2),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name=f'ROUND_{axle}{side}_{label}'
    for c in list(o.users_collection):c.objects.unlink(o)
    col.objects.link(o);o.data.materials.append(mat)
 bpy.data.collections[COLLECTION].hide_render=True
 return col

import bpy,math
from ..reference_data import BODY_STATIONS,GREENHOUSE_STATIONS
COLLECTION='TOLI_MUX_GENERATED'
def material(name,color,metal=0):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.4;return m
def mesh(name,sections,mat,col):
 verts=[v for section in sections for v in section];n=len(sections[0]);faces=[]
 for i in range(len(sections)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
 faces+=[tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))]
 data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update();o=bpy.data.objects.new(name,data);col.objects.link(o);data.materials.append(mat)
 # Closed sections are wound outward through a consistent topology operation.
 import bmesh
 bm=bmesh.new();bm.from_mesh(data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(data);bm.free()
 for p in data.polygons:p.use_smooth=True
 return o
def generate(scene,p):
 old=bpy.data.collections.get(COLLECTION)
 if old:
  for o in list(old.objects):
   data=o.data;bpy.data.objects.remove(o,do_unlink=True)
   if data and data.users==0 and isinstance(data,bpy.types.Mesh):bpy.data.meshes.remove(data)
  bpy.data.collections.remove(old)
 col=bpy.data.collections.new(COLLECTION);scene.collection.children.link(col)
 paint=material('MUX coded silver',(.48,.51,.55),.65);dark=material('MUX coded greenhouse block',(.035,.045,.055));rubber=material('MUX coded rubber',(.015,.018,.022));metal=material('MUX coded wheel',(.50,.53,.56),.8)
 sections=[]
 for x,w,h in BODY_STATIONS:
  half=p['width']*.5*w+p['fender_bulge']*max(0,1-abs(abs(x*p['length'])-p['wheelbase']/2)/.5);half=min(half,p['width']/2);top=(p['bonnet_height'] if x<-.24 else h*p['height']);bottom=p['ground_clearance'];belt=p['belt_height']
  sections.append([(x*p['length'],-half*.94,bottom),(x*p['length'],half*.94,bottom),(x*p['length'],half,belt*.86),(x*p['length'],half*.96,top),(x*p['length'],-half*.96,top),(x*p['length'],-half,belt*.86)])
 body=mesh('MUX_BODY',sections,paint,col)
 # Real Boolean wheel openings, not floating arch trim. Bake before removing cutters.
 for x in [-p['wheelbase']/2,p['wheelbase']/2]:
  bpy.ops.mesh.primitive_cylinder_add(vertices=48 if p['quality']=='QUALITY' else 32,radius=p['tire_diameter']/2+p['arch_clearance'],depth=p['width']*1.5,location=(x,0,p['tire_diameter']/2),rotation=(math.pi/2,0,0));cut=bpy.context.object
  mod=body.modifiers.new('Axle-derived wheel opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
 bevel=body.modifiers.new('Restrained body edges','BEVEL');bevel.width=.025;bevel.segments=3 if p['quality']=='QUALITY' else 2
 roof=[]
 for x,w,h in GREENHOUSE_STATIONS:
  if x<-.1:x=-.5+p['bonnet_length']/p['length']+(x+.24)*p['windscreen_run']/(.11*p['length'])
  if x>.26:w*=1-p['rear_taper']*(x-.26)/.20
  z=p['belt_height']+.02;top=z+(p['height']-p['roof_crown']-z)*h;half=p['greenhouse_width']*.5*w
  roof.append([(x*p['length'],-half,z),(x*p['length'],half,z),(x*p['length'],half*.94,top),(x*p['length'],0,top+p['roof_crown']),(x*p['length'],-half*.94,top)])
 mesh('MUX_GREENHOUSE_BLOCK',roof,dark,col)
 for axle,x in [('F',-p['wheelbase']/2),('R',p['wheelbase']/2)]:
  for side,y in [('L',-p['track']/2),('R',p['track']/2)]:
   for label,r,depth,mat in [('TIRE',p['tire_diameter']/2,.24,rubber),('RIM',p['tire_diameter']*.31,.245,metal)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=64 if p['quality']=='QUALITY' else 32,radius=r,depth=depth,location=(x,y,p['tire_diameter']/2),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name=f'MUX_{axle}{side}_{label}'
    for c in list(o.users_collection):c.objects.unlink(o)
    col.objects.link(o);o.data.materials.append(mat)
 return col

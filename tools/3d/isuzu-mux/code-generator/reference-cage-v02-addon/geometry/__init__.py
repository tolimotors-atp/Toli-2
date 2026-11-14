import bpy,math
from ..surfaces import body_sections,cabin_sections,cut_arch,symmetric_bake,windows
COLLECTION='TOLI_MUX_GENERATED'
def material(name,color,metal=0):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.4;return m
def mesh(name,sections,mat,col):
 verts=[v for section in sections for v in section];n=len(sections[0]);faces=[]
 for i in range(len(sections)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
 faces+=[tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))]
 data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update();o=bpy.data.objects.new(name,data);col.objects.link(o);
 if mat:data.materials.append(mat)
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
 count=85 if p['quality']=='QUALITY' else 49
 body=mesh('MUX_BODY',body_sections(p,count),paint,col);cut_arch(body,p,mesh,col)
 bevel=body.modifiers.new('Body edge radius','BEVEL');bevel.width=.012;bevel.segments=3 if p['quality']=='QUALITY' else 2
 symmetric_bake(body)
 cabin=mesh('MUX_GREENHOUSE_SHELL',cabin_sections(p,count),paint,col);symmetric_bake(cabin)
 windows(p,mesh,col,dark)
 for axle,x in [('F',-p['wheelbase']/2),('R',p['wheelbase']/2)]:
  for side,y in [('L',-p['track']/2),('R',p['track']/2)]:
   for label,r,depth,mat in [('TIRE',p['tire_diameter']/2,.24,rubber),('RIM',p['tire_diameter']*.31,.245,metal)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=64 if p['quality']=='QUALITY' else 32,radius=r,depth=depth,location=(x,y,p['tire_diameter']/2),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name=f'MUX_{axle}{side}_{label}'
    for c in list(o.users_collection):c.objects.unlink(o)
    col.objects.link(o);o.data.materials.append(mat)
 return col

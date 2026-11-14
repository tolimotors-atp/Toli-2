import bpy,bmesh,json,math
from mathutils import Vector
from .reference_cage import COL
from .section_network import zone_a,zone_b,zone_c
from ..parameters import BASE
SURFACES='TOLI_CROSSVIEW_SURFACES';CONTROL='TOLI_SURFACE_CONTROL_SECTIONS'

def boundary_type(a,b):
 names={a,b}
 if 'rear_glass' in names:return 'DEFINED'
 if any('return' in s and 'roof_return'!=s for s in names):return 'CONTROLLED'
 if any('edge' in s or 'roll' in s for s in names):return 'CONTROLLED'
 if 'cowl_root' in names:return 'DEFINED'
 return 'SOFT'

def clear(name,scene):
 old=bpy.data.collections.get(name)
 if old:
  for o in list(old.objects):
   d=o.data;bpy.data.objects.remove(o,do_unlink=True)
   if d.users==0:
    if isinstance(d,bpy.types.Mesh):bpy.data.meshes.remove(d)
    elif isinstance(d,bpy.types.Curve):bpy.data.curves.remove(d)
  bpy.data.collections.remove(old)
 col=bpy.data.collections.new(name);scene.collection.children.link(col);return col

def clay(name,value,roughness=.55):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.diffuse_color=(value,value,value,1);m.use_nodes=True;bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=m.diffuse_color;bs.inputs['Roughness'].default_value=roughness;bs.inputs['Metallic'].default_value=0
 return m

def build(scene,p,version=1):
 for n in ['length','width','height','wheelbase','track','tire_diameter']:
  if abs(p[n]-BASE[n])>1e-5:raise ValueError('Prototype preserves V04 family dimensions; restore the V04 dimension values first.')
 if COL not in bpy.data.collections:raise ValueError('Generate or load the preserved V04 constraints before this prototype.')
 surfaces=clear(SURFACES,scene);controls=clear(CONTROL,scene);constraints=bpy.data.collections[COL];manifest={}
 for zone,fn in [('A',zone_a),('B',zone_b),('C',zone_c)]:
  net=fn(constraints,p,refine=version==2);mesh=bpy.data.meshes.new('ZONE_'+zone+'_CONTROL');mesh.from_pydata(net.vertices,[],net.faces);mesh.update();o=bpy.data.objects.new('SURFACE_ZONE_'+zone,mesh);surfaces.objects.link(o)
  labels=sorted(set(net.labels));ids=mesh.attributes.new('patch_id','INT','FACE')
  for v,label in zip(ids.data,net.labels):v.value=labels.index(label)
  mesh.materials.append(clay('Prototype neutral clay',.30));mesh.materials.append(clay('Prototype aperture clay',.19))
  for face,label in zip(mesh.polygons,net.labels):face.material_index=int(label=='rear_glass');face.use_smooth=True
  bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
  # Orient each connected open construction component by its roof/outboard direction.
  unseen=set(bm.faces)
  while unseen:
   seed=unseen.pop();component={seed};stack=[seed]
   while stack:
    f=stack.pop()
    for edge in f.edges:
     for other in edge.link_faces:
      if other in unseen:unseen.remove(other);component.add(other);stack.append(other)
   score=0
   for f in component:
    c=f.calc_center_median();direction=Vector((1 if c.x>2.05 else 0,(-1 if c.y<0 else 1),.20)) if zone=='C' else Vector((0,0,1))
    score+=f.calc_area()*f.normal.dot(direction)
   if score<0:bmesh.ops.reverse_faces(bm,faces=list(component))
  bm.to_mesh(mesh);bm.free();mesh.update()
  edge_faces={e.index:[] for e in mesh.edges};lookup={tuple(sorted(e.vertices)):e.index for e in mesh.edges}
  for f in mesh.polygons:
   for pair in f.edge_keys:edge_faces[lookup[tuple(sorted(pair))]].append(f.index)
  crease=mesh.attributes.new('crease_edge','FLOAT','EDGE');boundaries=[]
  for e in mesh.edges:
   linked=edge_faces[e.index]
   if len(linked)==2:
    la,lb=[labels[mesh.attributes['patch_id'].data[i].value] for i in linked]
    if la!=lb:
     kind=boundary_type(la,lb)
     if version==2:
      if {la,lb}=={'cowl_root','A_root'}:kind='SOFT'
     crease.data[e.index].value={'SOFT':0.,'CONTROLLED':.22,'DEFINED':.65}[kind]
     if version==2:
      if kind=='CONTROLLED':crease.data[e.index].value=.22 if zone=='B' else .12
      if kind=='DEFINED':crease.data[e.index].value=.65 if zone=='B' else .40
     boundaries.append({'edge':e.index,'patches':[la,lb],'type':kind,'shared_vertex_ids':list(e.vertices),'position_gap_m':0.})
  o['patch_labels']=json.dumps(labels);o['boundary_manifest']=json.dumps(boundaries);o['zone']=zone;o['construction']='Shared low-density control vertices; local feature bands; open construction cuts';o['surface_approved']=False
  # The control mesh is checked before evaluation; subdivision is not the source of the form.
  assert all(f.area>1e-10 for f in mesh.polygons),(zone,[(f.index,net.labels[f.index],list(f.vertices)) for f in mesh.polygons if f.area<=1e-10])
  assert all(len(v)<=2 for v in edge_faces.values()),'Non-manifold interior control edge'
  sub=o.modifiers.new('Control-net evaluation only','SUBSURF');sub.subdivision_type='CATMULL_CLARK';sub.levels=2;sub.render_levels=2;sub.show_only_control_edges=True
  data=bpy.data.curves.new('SECTIONS_'+zone,'CURVE');data.dimensions='3D';data.bevel_depth=.0018;data.bevel_resolution=0
  for row in net.sections:
   sp=data.splines.new('POLY');sp.points.add(len(row)-1)
   for bp,v in zip(sp.points,row):bp.co=(*v,1)
  wires=bpy.data.objects.new('CONTROL_SECTIONS_'+zone,data);controls.objects.link(wires);wires['zone']=zone;data.materials.append(clay('Control section contrast',.08));wires.hide_render=True;wires.hide_viewport=True
  manifest[zone]={'patches':labels,'shared_boundaries':boundaries,'base_vertices':len(mesh.vertices),'base_faces':len(mesh.polygons)}
 scene['surface_prototype_version']=version
 scene['surface_prototype_manifest']=json.dumps(manifest);return surfaces

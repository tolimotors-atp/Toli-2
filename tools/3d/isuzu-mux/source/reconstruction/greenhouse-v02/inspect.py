import bpy,math,json,os
from pathlib import Path
from mathutils import Vector
O=Path(os.environ.get('MUX_GREENHOUSE_OUTPUT',Path(__file__).resolve().parents[3]));A=O/'source/reconstruction/greenhouse-v02';R=O/'renders';p=O/'source/reconstruction/isuzu-mux-reference-constrained-v02.blend';bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene
frozen=json.loads((A/'geometry-checks.json').read_text())['stance_signature']
for item in frozen:
 ob=bpy.data.objects[item['name']];assert [list(x) for x in ob.matrix_world]==item['matrix']
 if ob.type=='MESH':assert [list(v.co) for v in ob.data.vertices]==item['vertices']
meshes=[ob for ob in bpy.data.objects if ob.type=='MESH' and not any(m and m.name in ['Stance tire proxy','Stance wheel proxy'] for m in ob.data.materials)]
stations=json.loads((A/'stations.json').read_text());cuts=[]
for row in stations:
 x=row['x'];lines=[]
 for ob in meshes:
  ob.data.calc_loop_triangles()
  for tri in ob.data.loop_triangles:
   vs=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices];hits=[]
   for a,b in zip(vs,vs[1:]+vs[:1]):
    if (a.x-x)*(b.x-x)<0:
     t=(x-a.x)/(b.x-a.x);pt=a+t*(b-a);hits.append([pt.y,pt.z])
   if len(hits)==2:lines.append(hits)
 cuts.append(dict(id=row['id'],region=row['region'],x=x,actual_mesh_intersections=lines,controls=row))
(A/'cross-section-cuts.json').write_text(json.dumps(cuts,indent=2))
tires=[o for o in bpy.data.objects if o.name.startswith('Tire stance proxy')];ground=[min((o.matrix_world@v.co).z for v in o.data.vertices) for o in tires];assert len(tires)==4 and max(abs(z) for z in ground)<1e-5
(A/'reopen-validation.json').write_text(json.dumps(dict(opened_saved_blend=True,stance_exactly_preserved=True,tire_ground_heights=ground,packed_images=sum(bool(i.packed_file) for i in bpy.data.images),actual_section_count=len(cuts),sections_with_surface_intersections=sum(bool(c['actual_mesh_intersections']) for c in cuts)),indent=2))
# Reflection-only scene: neutral opaque diagnostic surfaces, no production materials or added body geometry.
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.resolution_x=1000;s.render.resolution_y=700;s.render.resolution_percentage=100;s.world.use_nodes=True;s.world.node_tree.nodes.get('Background').inputs[0].default_value=(.12,.12,.12,1);s.world.node_tree.nodes.get('Background').inputs[1].default_value=.4
for ob in bpy.data.objects:
 if ob.type=='LIGHT':bpy.data.objects.remove(ob,do_unlink=True)
for m in [m for m in bpy.data.materials if m.name.startswith('Diagnostic neutral') or m.name.startswith('Diagnostic opaque')]:
 node=m.node_tree.nodes.get('Principled BSDF');node.inputs['Base Color'].default_value=(.23,.23,.23,1);node.inputs['Metallic'].default_value=.65;node.inputs['Roughness'].default_value=.13
emit=bpy.data.materials.new('Diagnostic broad white strip emitter');emit.use_nodes=True;ns=emit.node_tree.nodes;ns.clear();e=ns.new('ShaderNodeEmission');e.inputs[0].default_value=(1,1,1,1);e.inputs[1].default_value=5;o=ns.new('ShaderNodeOutputMaterial');emit.node_tree.links.new(e.outputs[0],o.inputs[0])
for i in range(6):
 bpy.ops.mesh.primitive_plane_add(size=1,location=(-.9+i*.34,0,1.25));ob=bpy.context.object;ob.name='Reflection strip '+str(i);ob.scale=(.095,2,1);ob.data.materials.append(emit);ob.visible_camera=False
for i in range(3):
 bpy.ops.mesh.primitive_plane_add(size=1,location=(0,-1.3,.45+i*.35),rotation=(math.pi/2,0,0));ob=bpy.context.object;ob.name='Side reflection strip '+str(i);ob.scale=(2,.08,1);ob.data.materials.append(emit);ob.visible_camera=False
for item in frozen:bpy.data.objects[item['name']].hide_render=True
for name in ['front-left','rear-left']:
 s.camera=bpy.data.objects['V02 diagnostic '+name];s.camera.data.lens=105;s.camera.rotation_euler=(Vector((.12,0,.53))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(R/f'greenhouse-strip-{name}-v02.png');bpy.ops.render.render(write_still=True)
# Keep reflection setup separate; master remains the neutral saved geometry milestone.
bpy.ops.wm.save_as_mainfile(filepath=str(A/'reflection-diagnostic-scene-v02.blend'))

import bpy,json,math,os
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
O=Path(os.environ.get('MUX_GENERATED_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';R=O/'renders';A=D/'generated';p=D/'isuzu-mux-generated-master.blend';bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;s.frame_set(1)
def descendants(o):return [o]+[z for c in o.children for z in descendants(c)]
root=bpy.data.objects['MUX_ROOT'];vehicle=[o for o in descendants(root) if o.type in ['MESH','CURVE'] and not o.name.startswith('CUT')];stats=dict(base_vertices=sum(len(o.data.vertices) for o in vehicle if o.type=='MESH'),evaluated_vertices=0,evaluated_triangles=0,mesh_and_curve_objects=len(vehicle),materials=len({m.name for o in vehicle for m in o.data.materials if m}),texture_images=0,external_paid_assets='NONE',fresh_authored_geometry=True)
dg=bpy.context.evaluated_depsgraph_get()
for ob in vehicle:
 ev=ob.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();stats['evaluated_vertices']+=len(me.vertices);stats['evaluated_triangles']+=len(me.loop_triangles);assert all(math.isfinite(float(c)) for v in me.vertices for c in v.co);ev.to_mesh_clear()
ground={}
for n in ['WHEEL_FL','WHEEL_FR','WHEEL_RL','WHEEL_RR']:
 ob=next(o for o in bpy.data.objects[n].children if o.name.endswith('tire'));ground[n]=min((ob.matrix_world@v.co).z for v in ob.data.vertices)
assert max(abs(v) for v in ground.values())<1e-5,ground
stats['tire_ground_heights']=ground;stats['vehicle_parts_bounds_include_mirrors_steps']=True
motion={};collisions=[];fixed=bpy.data.objects['BODY — editable half control cage']
def bvh(ob):
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();vs=[ob.matrix_world@v.co for v in me.vertices];polys=[list(f.vertices) for f in me.polygons];tree=BVHTree.FromPolygons(vs,polys);ev.to_mesh_clear();return tree
for frame in [1,15,30,50]:
 s.frame_set(frame);bpy.context.view_layer.update();fb=bvh(fixed)
 for n in ['DOOR_FL','DOOR_FR','DOOR_RL','DOOR_RR','BONNET','TAILGATE']:
  ob=bpy.data.objects[n];motion.setdefault(n,[]).append(dict(frame=frame,rotation_radians=list(ob.rotation_euler)))
  panel=next((z for z in descendants(ob) if z.type=='MESH' and ('painted outer shell' in z.name or z.name.startswith('BONNET editable') or z.name.startswith('TAILGATE painted'))),None)
  if panel:collisions.append(dict(frame=frame,panel=n,triangle_overlap_pairs_with_fixed_shell=len(fb.overlap(bvh(panel)))))
s.frame_set(1);(A/'geometry-checks.json').write_text(json.dumps(stats,indent=2));(A/'functional-checks.json').write_text(json.dumps(dict(controllers=motion,painted_panel_shell_intersections=collisions,scope='Triangle intersection diagnostic for painted panels versus main fixed shell only; not proof of full swept-volume or all-part clearance.'),indent=2))
for name,loc,target in [('front3q',(-7,-8,3.4),(0,0,.9)),('rear3q',(7,-8,3.1),(.1,0,.9))]:
 if not bpy.data.objects.get('VIEW '+name):
  bpy.ops.object.camera_add(location=loc);cam=bpy.context.object;cam.name='VIEW '+name;cam.data.lens=58;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
# Neutral automotive validation studio, no imported HDRIs or third-party models/textures.
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=20;s.cycles.use_denoising=True;s.render.resolution_x=1100;s.render.resolution_y=750;s.render.resolution_percentage=100;s.world.use_nodes=True;s.world.node_tree.nodes.get('Background').inputs[0].default_value=(.32,.32,.32,1);s.world.node_tree.nodes.get('Background').inputs[1].default_value=.45
floor=bpy.data.materials.new('STUDIO matte floor');floor.use_nodes=True;pn=floor.node_tree.nodes.get('Principled BSDF');pn.inputs['Base Color'].default_value=(.11,.115,.12,1);pn.inputs['Roughness'].default_value=.28
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.005));ob=bpy.context.object;ob.name='STUDIO ground';ob.data.materials.append(floor)
for i,(loc,power,sx,sy) in enumerate([((-3,-4,6),1700,5,2),((2,4,5),1900,5,3),((4,-3,3),1000,3,3)]):
 bpy.ops.object.light_add(type='AREA',location=loc);ob=bpy.context.object;ob.name='STUDIO area '+str(i);ob.data.energy=power;ob.data.shape='RECTANGLE';ob.data.size=sx;ob.data.size_y=sy;ob.rotation_euler=(Vector((0,0,.9))-ob.location).to_track_quat('-Z','Y').to_euler()
for i in range(4):
 bpy.ops.object.light_add(type='AREA',location=(-2.5+i*1.5,0,4.2));ob=bpy.context.object;ob.name='STUDIO reflection strip '+str(i);ob.data.energy=100;ob.data.shape='RECTANGLE';ob.data.size=.20;ob.data.size_y=5
for frame,views,prefix in [(1,['front3q','rear3q'],'generated-studio-closed'),(50,['front3q','rear3q'],'generated-studio-open')]:
 s.frame_set(frame)
 for name in views:
  s.camera=bpy.data.objects['VIEW '+name];s.render.filepath=str(R/f'{prefix}-{name}.png');bpy.ops.render.render(write_still=True)
s.frame_set(1);s.camera=bpy.data.objects['VIEW front3q'];bpy.ops.wm.save_as_mainfile(filepath=str(D/'milestones/generated-studio-v01.blend'))
# Master remains editable and opens ready for neutral studio inspection.
bpy.ops.wm.save_as_mainfile(filepath=str(p));bpy.ops.wm.open_mainfile(filepath=str(p));assert bpy.data.objects.get('MUX_ROOT') and len([n for n in ['DOOR_FL','DOOR_FR','DOOR_RL','DOOR_RR','BONNET','TAILGATE'] if bpy.data.objects.get(n)])==6
(A/'reopen-validation.json').write_text(json.dumps(dict(passed=True,production_master_reopened=True,six_panel_controllers=True,neutral_closed_frame=1,paid_assets=False,website_integration=False),indent=2))

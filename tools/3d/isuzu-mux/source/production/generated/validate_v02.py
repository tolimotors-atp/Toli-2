import bpy,json,math,os
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
O=Path(os.environ.get('MUX_V02_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';R=O/'renders/refinement-v02';P=D/'isuzu-mux-generated-master.blend';bpy.ops.wm.open_mainfile(filepath=str(P));s=bpy.context.scene;s.frame_set(1)
def descendants(ob):return [ob]+[z for c in ob.children for z in descendants(c)]
def parts(ob):return [z for z in descendants(ob) if z.type in ['MESH','CURVE'] and not z.hide_render and not z.name.startswith('CUT')]
root=bpy.data.objects['MUX_ROOT'];vehicle=parts(root);controllers=['DOOR_FL','DOOR_FR','DOOR_RL','DOOR_RR','BONNET','TAILGATE'];base=json.loads((A/'fixed-cameras-v02.json').read_text())
for n,d in base.items():
 c=bpy.data.objects['CAM_COMPARE_'+n];assert max(abs(a-b) for a,b in zip(c.location,d['location']))<1e-6;assert max(abs(a-b) for a,b in zip(c.rotation_euler,d['rotation']))<1e-6
stats={'base_vertices':sum(len(o.data.vertices) for o in vehicle if o.type=='MESH'),'evaluated_vertices':0,'evaluated_triangles':0,'mesh_and_curve_objects':len(vehicle),'materials':len({m.name for o in vehicle for m in o.data.materials if m}),'texture_images':0}
for ob in vehicle:
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();stats['evaluated_vertices']+=len(me.vertices);stats['evaluated_triangles']+=len(me.loop_triangles);assert all(math.isfinite(c) for v in me.vertices for c in v.co);ev.to_mesh_clear()
ground={}
for n in ['WHEEL_FL','WHEEL_FR','WHEEL_RL','WHEEL_RR']:
 tire=next(o for o in bpy.data.objects[n].children if o.name.endswith('tire'));ground[n]=min((tire.matrix_world@v.co).z for v in tire.data.vertices)
assert max(abs(v) for v in ground.values())<1e-5
(A/'geometry-v02.json').write_text(json.dumps(dict(stats,ground_heights=ground,fixed_cameras_unchanged=True),indent=2))
def bvh(ob):
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();vs=[ob.matrix_world@v.co for v in me.vertices];polys=[list(f.vertices) for f in me.polygons];tree=BVHTree.FromPolygons(vs,polys);ev.to_mesh_clear();return tree
# Broad moving-assembly checks against every other render-visible vehicle part, including trim/interior.
# shortcut: discrete surface intersections do not prove continuous swept-volume or solid containment clearance.
static={ob.name:bvh(ob) for ob in vehicle};rows=[];limits={n:(2,math.radians(55)*(1 if n.endswith('L') else -1)) for n in controllers[:4]};limits.update(BONNET=(1,math.radians(58)),TAILGATE=(1,-math.radians(82)))
for name in controllers:
 ob=bpy.data.objects[name];assembly=parts(ob);own={z.name for z in assembly};axis,angle=limits[name]
 for fraction in [0,.25,.5,.75,1]:
  s.frame_set(1);ob.rotation_euler[axis]=fraction*angle;bpy.context.view_layer.update();assert abs(ob.rotation_euler[axis]-fraction*angle)<1e-6;contacts=[]
  for moving in assembly:
   movingtree=bvh(moving)
   for other in vehicle:
    if other.name in own:continue
    count=len(movingtree.overlap(static[other.name]))
    if count:contacts.append({'moving':moving.name,'fixed':other.name,'face_overlap_pairs':count})
  rows.append({'panel':name,'fraction':fraction,'angle_degrees':math.degrees(fraction*angle),'contacts':contacts})
 s.frame_set(1)
(A/'motion-v02.json').write_text(json.dumps({'samples':rows,'scope':'Each complete moving assembly versus all other render-visible vehicle mesh/curve parts held closed; surfaces at five exact angular fractions. Shared-edge contacts are included and require visual interpretation. Not continuous swept-volume proof.'},indent=2))
# Contact-sheet poses complement the individual-assembly numerical checks.
actions={n:(bpy.data.objects[n].animation_data.action,bpy.data.objects[n].animation_data.action_slot) for n in controllers}
for n in controllers:bpy.data.objects[n].animation_data.action=None
s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.display.shading.show_shadows=True;s.render.resolution_x=900;s.render.resolution_y=600
for frac in [0,.25,.5,.75,1]:
 s.frame_set(1)
 for name,(axis,angle) in limits.items():bpy.data.objects[name].rotation_euler[axis]=frac*angle
 for view in ['FRONT_34','REAR_34']:
  s.camera=bpy.data.objects['CAM_COMPARE_'+view];s.render.filepath=str(R/('motion-'+str(int(frac*100))+'-'+view.lower()+'.png'));bpy.ops.render.render(write_still=True)
for n,(action,slot) in actions.items():
 bpy.data.objects[n].animation_data.action=action;bpy.data.objects[n].animation_data.action_slot=slot
s.frame_set(1);s.render.engine='CYCLES';s.render.resolution_x=960;s.render.resolution_y=640;s.camera=bpy.data.objects['CAM_COMPARE_FRONT_34'];bpy.ops.wm.save_as_mainfile(filepath=str(P));bpy.ops.wm.open_mainfile(filepath=str(P));assert all(bpy.data.objects.get(n) for n in controllers)
(A/'reopen-v02.json').write_text(json.dumps({'passed':True,'source_reopened':True,'six_panel_controls':True,'fixed_camera_count':5,'website_integration':False,'glb_export':False},indent=2));print('V02 CHECKS COMPLETE',flush=True)

# All outputs are saved; bypass a headless audio-shutdown hang in this Blender runtime.
os._exit(0)

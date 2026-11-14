import bpy,json,math,os,hashlib
from pathlib import Path
O=Path(os.environ.get('MUX_V03_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';P=D/'isuzu-mux-generated-v03.blend';bpy.ops.wm.open_mainfile(filepath=str(P));s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update()
prefixes=('WHEEL_','INTERIOR','CENTER CONSOLE','Seat ','ENGINE','Engine ','Battery','Air filter','Major intake','Reservoir','Radiator','Firewall','RHD ','Steering ','Climate ','Instrument ','Center radio','Infotainment','Gear ','Cargo ')
def retained():return [o for o in bpy.data.objects if o.type in ['MESH','CURVE'] and o.name.startswith(prefixes)]
def signatures():
 out={}
 for ob in retained():
  co=[[round(c,6) for c in v.co] for v in ob.data.vertices] if ob.type=='MESH' else [[round(c,6) for c in p.co] for sp in ob.data.splines for p in sp.points]
  vals=[co,[[round(c,6) for c in row] for row in ob.matrix_world],[m.name for m in ob.data.materials]];out[ob.name]=hashlib.sha256(json.dumps(vals).encode()).hexdigest()
 return out
keep=retained();assert len(keep)==113,len(keep);after=signatures();new=[o for o in bpy.data.collections['V03_EXTERIOR'].objects if o.type in ['MESH','CURVE']];assert bpy.data.objects['V03_NEW_EXTERIOR_SHELL'].data!=bpy.data.objects['BODY — editable half control cage'].data
assert bpy.data.collections['V02_REFERENCE_BODY'].hide_render and bpy.data.collections['V02_REFERENCE_BODY'].hide_viewport
# Stored legacy reference geometry is excluded from every V03 geometry count.
def stats(objects):
 d={'base_vertices':sum(len(o.data.vertices) for o in objects if o.type=='MESH'),'evaluated_vertices':0,'evaluated_triangles':0,'objects':len(objects),'materials':len({m.name for o in objects for m in o.data.materials if m})}
 for ob in objects:
  ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();d['evaluated_vertices']+=len(me.vertices);d['evaluated_triangles']+=len(me.loop_triangles);assert all(math.isfinite(c) for v in me.vertices for c in v.co);ev.to_mesh_clear()
 return d
geom={'new_exterior':stats(new),'new_exterior_plus_wheels':stats(new+[o for o in keep if o.name.startswith('WHEEL_')]),'new_exterior_plus_all_retained':stats(new+keep),'image_textures':0,'legacy_reference_excluded':True}
ground={}
for n in ['WHEEL_FL','WHEEL_FR','WHEEL_RL','WHEEL_RR']:
 t=next(o for o in bpy.data.objects[n].children if o.name.endswith('tire'));ground[n]=min((t.matrix_world@v.co).z for v in t.data.vertices)
assert max(abs(v) for v in ground.values())<1e-5
camera={n:(list(bpy.data.objects['CAM_COMPARE_'+n].location),list(bpy.data.objects['CAM_COMPARE_'+n].rotation_euler),bpy.data.objects['CAM_COMPARE_'+n].data.type,bpy.data.objects['CAM_COMPARE_'+n].data.lens,bpy.data.objects['CAM_COMPARE_'+n].data.ortho_scale) for n in ['FRONT','FRONT_34','SIDE','REAR_34','REAR']}
bpy.ops.wm.open_mainfile(filepath=str(D/'milestones/isuzu-mux-generated-v02.blend'));bpy.context.scene.frame_set(1);bpy.context.view_layer.update();before=signatures();assert before==after,'Retained wheel/interior/engine parts changed'
for n,v in camera.items():
 c=bpy.data.objects['CAM_COMPARE_'+n];check=(list(c.location),list(c.rotation_euler),c.data.type,c.data.lens,c.data.ortho_scale);assert check==v,('Camera changed',n)
bpy.ops.wm.open_mainfile(filepath=str(P));(A/'v03-validation.json').write_text(json.dumps({'geometry':geom,'retained_count':len(keep),'retained_geometry_transform_material_signatures_unchanged':True,'wheel_ground_heights':ground,'fixed_cameras_unchanged':True,'new_exterior_uses_old_control_cage':False,'v02_reference_hidden':True,'source_reopened':True,'panels':'NOT YET REBUILT','clearance':'NOT REACHED','paid_assets':'NONE','glb':'NOT EXPORTED'},indent=2));print('V03 GEOMETRY / RETAINED PARTS / CAMERAS / GROUNDING CHECKS PASS',flush=True);os._exit(0)

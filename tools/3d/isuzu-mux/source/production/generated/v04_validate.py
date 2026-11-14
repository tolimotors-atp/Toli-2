import bpy,json,os,math,hashlib
from pathlib import Path
from mathutils import Vector
O=Path(os.environ.get('MUX_V04_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';P=D/'isuzu-mux-generated-v04.blend';bpy.ops.wm.open_mainfile(filepath=str(P));bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
prefixes=('WHEEL_','INTERIOR','CENTER CONSOLE','Seat ','ENGINE','Engine ','Battery','Air filter','Major intake','Reservoir','Radiator','Firewall','RHD ','Steering ','Climate ','Instrument ','Center radio','Infotainment','Gear ','Cargo ')
def kept():return [o for o in bpy.data.objects if o.type in ['MESH','CURVE'] and o.name.startswith(prefixes)]
def signatures(objects):
 out={}
 for ob in objects:
  co=[[round(c,6) for c in v.co] for v in ob.data.vertices] if ob.type=='MESH' else [[round(c,6) for c in p.co] for sp in ob.data.splines for p in sp.points];vals=[co,[[round(c,6) for c in row] for row in ob.matrix_world],[m.name for m in ob.data.materials]];out[ob.name]=hashlib.sha256(json.dumps(vals).encode()).hexdigest()
 return out
keep=kept();assert len(keep)==113;after=signatures(keep);glassnames=['V03_COHERENT_WINDSCREEN','V03_COHERENT_FRONT_-1','V03_COHERENT_FRONT_1'];frontglass=signatures([bpy.data.objects[n] for n in glassnames])
objects=[o for c in ['V03_EXTERIOR','V04_FRONT_COMPOSITION','V04_REAR_COMPOSITION'] for o in bpy.data.collections[c].objects if o.type in ['MESH','CURVE']]
def stats(objects):
 d={'base_vertices':sum(len(o.data.vertices) for o in objects if o.type=='MESH'),'evaluated_vertices':0,'evaluated_triangles':0,'objects':len(objects),'materials':len({m.name for o in objects for m in o.data.materials if m})};lo=[float('inf')]*3;hi=[-float('inf')]*3
 for ob in objects:
  ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();d['evaluated_vertices']+=len(me.vertices);d['evaluated_triangles']+=len(me.loop_triangles)
  for v in me.vertices:
   co=ob.matrix_world@v.co;assert all(math.isfinite(c) for c in co)
   for k in range(3):lo[k]=min(lo[k],co[k]);hi[k]=max(hi[k],co[k])
  ev.to_mesh_clear()
 d['bounds_min']=lo;d['bounds_max']=hi;d['dimensions']=[b-a for a,b in zip(lo,hi)];return d
geometry={'exterior':stats(objects),'exterior_plus_retained':stats(objects+keep),'body_foundation':stats([bpy.data.objects['V03_NEW_EXTERIOR_SHELL']]),'image_textures_added':0}
# Thickness tolerances do not change the frozen nominal hard-point markers.
lo=geometry['exterior']['bounds_min'];hi=geometry['exterior']['bounds_max'];assert lo[0]>=-2.3325 and hi[0]<=2.5025,(lo,hi);assert max(abs(lo[1]),abs(hi[1]))<=.9401,(lo,hi)
ground={}
for n in ['WHEEL_FL','WHEEL_FR','WHEEL_RL','WHEEL_RR']:
 tire=next(o for o in bpy.data.objects[n].children if o.name.endswith('tire'));ground[n]=min((tire.matrix_world@v.co).z for v in tire.data.vertices)
assert max(abs(v) for v in ground.values())<1e-5
names=['FRONT','FRONT_34','SIDE','REAR_34','REAR'];cams={n:(list(bpy.data.objects['CAM_COMPARE_'+n].location),list(bpy.data.objects['CAM_COMPARE_'+n].rotation_euler),bpy.data.objects['CAM_COMPARE_'+n].data.type,bpy.data.objects['CAM_COMPARE_'+n].data.lens,bpy.data.objects['CAM_COMPARE_'+n].data.ortho_scale) for n in names}
def roof_samples():
 ob=bpy.data.objects['V03_NEW_EXTERIOR_SHELL'].evaluated_get(bpy.context.evaluated_depsgraph_get());out={}
 for x in [-.34,.28,1.14,1.98]:
  hit,co,no,idx=ob.ray_cast(Vector((x,0,3)),Vector((0,0,-1)));assert hit;out[str(x)]=co.z
 return out
roof=roof_samples();bpy.ops.wm.open_mainfile(filepath=str(D/'milestones/isuzu-mux-generated-v03.blend'));bpy.context.scene.frame_set(1);bpy.context.view_layer.update();assert after==signatures(kept()),'Retained components changed';assert frontglass==signatures([bpy.data.objects[n] for n in glassnames]),'Frozen windscreen/front windows changed';before_roof=roof_samples();roof_delta={n:roof[n]-z for n,z in before_roof.items()};assert max(abs(v) for v in roof_delta.values())<1e-5,roof_delta
for n,old in cams.items():
 c=bpy.data.objects['CAM_COMPARE_'+n];assert old==(list(c.location),list(c.rotation_euler),c.data.type,c.data.lens,c.data.ortho_scale)
bpy.ops.wm.open_mainfile(filepath=str(P));(A/'v04-validation.json').write_text(json.dumps({'geometry':geometry,'retained_expected':113,'retained_actual':len(keep),'retained_geometry_transforms_material_slots_unchanged':True,'front_glazing_unchanged':True,'main_roof_centerline_height_delta_m':roof_delta,'fixed_cameras_unchanged':True,'tire_ground_heights':ground,'source_reopened':True,'functional_panels':'NOT REBUILT','clearance':'NOT PERFORMED','glb':'NOT EXPORTED'},indent=2));print('V04 RETAINED PARTS / MACRO / GEOMETRY CHECKS PASS',flush=True);os._exit(0)

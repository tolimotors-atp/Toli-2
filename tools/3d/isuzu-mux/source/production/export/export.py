import bpy,json,os
from pathlib import Path
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');O=Path(os.environ.get('MUX_WEB_EXPORT_OUTPUT',Path(__file__).resolve().parent));bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-generated-v04.blend'));s=bpy.context.scene;s.frame_set(1)
prefixes=('WHEEL_','INTERIOR','CENTER CONSOLE','Seat ','ENGINE','Engine ','Battery','Air filter','Major intake','Reservoir','Radiator','Firewall','RHD ','Steering ','Climate ','Instrument ','Center radio','Infotainment','Gear ','Cargo ')
retained=[o for o in bpy.data.objects if o.type in ['MESH','CURVE'] and o.name.startswith(prefixes)];assert len(retained)==113
exterior=[o for c in ['V03_EXTERIOR','V04_FRONT_COMPOSITION','V04_REAR_COMPOSITION'] for o in bpy.data.collections[c].objects if o.type in ['MESH','CURVE']]
keep=set(exterior+retained)
# Keep genuine wheel parent empties so their inspected names remain stable in glTF.
for o in list(keep):
 p=o.parent
 while p:keep.add(p);p=p.parent
# Bake modifier results while Boolean/reference dependencies still exist.
deps=bpy.context.evaluated_depsgraph_get()
baked={o:bpy.data.meshes.new_from_object(o.evaluated_get(deps),depsgraph=deps) for o in keep if o.type=='MESH'}
for o,mesh in baked.items():
 o.modifiers.clear();o.data=mesh
for o in list(bpy.data.objects):
 if o not in keep and o.type not in ['CAMERA','LIGHT']:bpy.data.objects.remove(o,do_unlink=True)
for o in bpy.data.objects:o.select_set(o in keep)
for o in keep:o.hide_set(False);o.hide_viewport=False;o.hide_render=False
s['WEB_STATUS']='V04 PREVIEW / TEMPORARY PRODUCTION ASSET; static panels; not factory CAD'
bpy.ops.wm.save_as_mainfile(filepath=str(O/'isuzu-mux-web-v04.blend'))
bpy.ops.export_scene.gltf(filepath=str(P/'public/models/vehicles/isuzu-mux/isuzu-mux-web.glb'),export_format='GLB',use_selection=True,export_apply=True,export_cameras=False,export_lights=False,export_extras=False)
info={'retained_components':len(retained),'exterior_objects':len(exterior),'wheels':{n:[c.name for c in bpy.data.objects[n].children] for n in ['WHEEL_FL','WHEEL_FR','WHEEL_RL','WHEEL_RR']},'cameras':{n:{'location':list(bpy.data.objects[n].location),'rotation':list(bpy.data.objects[n].rotation_euler)} for n in ['CAM_COMPARE_FRONT','CAM_COMPARE_SIDE']},'materials':[m.name for m in bpy.data.materials]};(O/'source-audit.json').write_text(json.dumps(info,indent=2));print('EXPORTED',flush=True)

import os
os._exit(0)

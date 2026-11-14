import bpy,sys,os,json
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'tools/blender-addons'))
import toli_mux_generator as addon
from toli_mux_generator.surface_diagnostics import setup,camera_for,zebra
from toli_mux_generator.geometry.surface_patch import SURFACES,CONTROL,clay
from toli_mux_generator.surface_ui import update
source=os.environ.get('MUX_SURFACE_SOURCE','v03');assert source in ['v02','v03']
addon.register();bpy.ops.wm.open_mainfile(filepath=str(P/f'tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-{source}.blend'));s=bpy.context.scene;setup(s)
zone=os.environ.get('MUX_SURFACE_ZONE','A');assert zone in ['A','B','C'];stage=os.environ.get('MUX_SURFACE_STAGE','full');s.toli_mux.surface_zone=zone
r=P/'tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03'/('zone-'+zone.lower());r.mkdir(parents=True,exist_ok=True)
views={'A':['FRONT','FRONT34','SIDE'],'B':['SIDE','REAR34','REAR'],'C':['SIDE','REAR34','REAR']}[zone];primary='FRONT34' if zone=='A' else 'REAR34'
jobs=[('base-control',primary,'base',False)]+[('base-'+v.lower(),v,'base',False) for v in views]+[('base-close',primary,'base',True)]+[('clay-'+v.lower(),v,'clay',False) for v in views]+[('clay-close',primary,'clay',True),('cage',primary,'cage',False),('reflection',primary,'reflection',True),('zebra',primary,'zebra',True),('constraints-overlay',primary,'overlay',False),('control-sections',primary,'control',False)]
if stage=='preview':jobs=[j for j in jobs if j[0] in ['base-control','clay-'+primary.lower()]]
selection=os.environ.get('MUX_SURFACE_JOBS')
if selection:jobs=[j for j in jobs if j[0] in selection.split(',')]
assert jobs,'No diagnostic jobs selected'
for name,view,mode,close in jobs:
 s.toli_mux.surface_constraints=mode in ['cage','overlay'];s.toli_mux.surface_control_sections=mode=='control';update(s.toli_mux,bpy.context)
 for o in bpy.data.collections[SURFACES].objects:
  o.hide_render=mode=='cage' or o['zone']!=zone;o.modifiers[0].show_render=mode not in ['base','control']
  for poly in o.data.polygons:poly.use_smooth=mode!='base'
  slots=[poly.material_index for poly in o.data.polygons]
  o.data.materials.clear();o.data.materials.append(zebra() if mode=='zebra' else clay('Prototype reflection clay',.25,.14) if mode=='reflection' else clay('Prototype neutral clay',.30,.55));o.data.materials.append(o.data.materials[0] if mode in ['reflection','zebra'] else clay('Prototype aperture clay',.19,.55))
  for poly,slot in zip(o.data.polygons,slots):poly.material_index=slot
 for o in bpy.data.objects:
  if o.type=='LIGHT' and o.name.startswith('PROTO_'):o.hide_render=(o.name.startswith('PROTO_STRIP'))!=(mode=='reflection')
 if mode=='cage':
  # Keep the relevant V04 comparison network rather than only the authoritative overlay subset.
  from toli_mux_generator.geometry.flow_cage import JOIN_CURVES
  joins={'A':['J01','J02'],'B':['J03','J04','J08'],'C':['J05','J06','J07']}[zone];allowed=set(sum([JOIN_CURVES[j] for j in joins],[]))
  for o in bpy.data.collections['TOLI_MUX_REFERENCE_CAGE'].objects:o.hide_render=o.name.removesuffix('_R') not in allowed
 spec=json.loads((r.parent/'fixed-v01-cameras.json').read_text())[f'{zone}/{view}/{int(close)}'];cam=bpy.data.objects['PROTO_Camera'];cam.location=spec['location'];cam.rotation_euler=spec['rotation'];cam.data.ortho_scale=spec['scale'];s.camera=cam
 if os.environ.get('MUX_SURFACE_FEATURE')=='lower':
  assert zone=='C' and close
  cam.location+=__import__('mathutils').Vector((.04,.05,-.39));cam.data.ortho_scale=1.10
  name=('v02-' if source=='v02' else '')+'lower-'+mode
 s.render.filepath=str(r/(name+'.png'));bpy.ops.render.render(write_still=True)
print('ZONE',zone,stage,'RENDERS COMPLETE',flush=True);os._exit(0)

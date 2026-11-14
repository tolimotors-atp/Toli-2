import bpy,sys,json,os,hashlib
from pathlib import Path
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');sys.path.insert(0,str(P/'tools/blender-addons'));import toli_mux_generator as a
from toli_mux_generator.parameters import values
from toli_mux_generator.validation import validate
a.register();bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-code-generated-v02.blend'))
def sig():
 rows=[]
 for o in sorted(bpy.data.collections['TOLI_MUX_GENERATED'].objects,key=lambda o:o.name):
  e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();rows.append((o.name,[[round(c,6) for c in o.matrix_world@v.co] for v in m.vertices]));e.to_mesh_clear()
 return hashlib.sha256(json.dumps(rows).encode()).hexdigest()
old=sig();bpy.ops.toli_mux.regenerate();one=sig();bpy.ops.toli_mux.regenerate();two=sig();v=validate(bpy.context.scene,values(bpy.context.scene));assert one==two and v['symmetry'];v.update(reproducibility='PASS',saved_scene_matches_current_code=old==one);r=P/'tools/3d/isuzu-mux/code-generator/renders/v02';(r/'final-check.json').write_text(json.dumps(v,indent=2));print(json.dumps(v),flush=True);os._exit(0)

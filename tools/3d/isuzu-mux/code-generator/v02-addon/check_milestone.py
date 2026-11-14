import sys,bpy,json,os
from pathlib import Path
p=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');sys.path.insert(0,str(p/'tools/blender-addons'));import toli_mux_generator as a
from toli_mux_generator.validation import validate
from toli_mux_generator.parameters import values
bpy.ops.wm.read_factory_settings(use_empty=True);a.register();bpy.ops.wm.open_mainfile(filepath=str(p/'tools/3d/isuzu-mux/source/production/isuzu-mux-code-generated-v02.blend'));s=bpy.context.scene;v=validate(s,values(s));s.toli_mux.quality='QUALITY';bpy.ops.toli_mux.regenerate();q=validate(s,values(s));assert q['triangles']>v['triangles'];s.toli_mux.length=5;bpy.ops.toli_mux.reset();assert abs(s.toli_mux.length-4.825)<1e-5 and s.toli_mux.quality=='PREVIEW';bpy.ops.toli_mux.regenerate();v=validate(s,values(s));v.update(delete_and_regenerate_identical=True,quality_triangles=q['triangles'],reset_test='PASS',reopen_test='PASS');(p/'tools/3d/isuzu-mux/code-generator/renders/v02/validation.json').write_text(json.dumps(v,indent=2));print(json.dumps(v),flush=True);os._exit(0)

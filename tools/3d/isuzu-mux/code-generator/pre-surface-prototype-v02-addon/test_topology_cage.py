import bpy,sys,json,os
from pathlib import Path
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');sys.path.insert(0,str(P/'tools/blender-addons'));from toli_mux_generator.geometry.soft_body import generate_soft
from toli_mux_generator.geometry.rounded import ROUNDED
from toli_mux_generator.parameters import BASE
from toli_mux_generator import validation
bpy.ops.wm.read_factory_settings(use_empty=True);validation.COLLECTION=ROUNDED;out={}
for mode in ['PREVIEW','QUALITY']:
 p=dict(BASE,quality=mode);generate_soft(bpy.context.scene,p);v=validation.validate(bpy.context.scene,p);v['arch_weighted_edges']=bpy.data.objects['MUX_CURVE_SURFACE_PATCHES'].get('arch_edges_beveled');out[mode]=v;assert v['arch_weighted_edges']>0;assert v['degenerate_faces']==0 and v['nonmanifold_edges']==0 and v['symmetry'],v
r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v01';r.mkdir(parents=True,exist_ok=True);(r/'topology-fix.json').write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True);os._exit(0)

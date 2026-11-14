import sys,bpy,json,os,hashlib
from pathlib import Path
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');sys.path.insert(0,str(P/'tools/blender-addons'));import toli_mux_generator as a
from toli_mux_generator.geometry.reference_cage import COL
a.register();bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v01.blend'))
def sig():return hashlib.sha256(json.dumps([(o.name,[[list(v.co),list(v.handle_left),list(v.handle_right)] for v in o.data.splines[0].bezier_points]) for o in sorted(bpy.data.collections[COL].objects,key=lambda x:x.name)]).encode()).hexdigest()
bpy.ops.toli_mux.reference_cage();a1=sig();bpy.ops.toli_mux.reference_cage();assert sig()==a1;assert bpy.context.scene.toli_mux.curve_cage_only;assert len(bpy.data.collections['TOLI_CAGE_SUPPORT'].objects)==5
s=bpy.context.scene;s.toli_mux.curve_cage_only=False;assert bpy.data.collections[COL].hide_viewport;s.toli_mux.curve_cage_only=True;assert not bpy.data.collections[COL].hide_viewport
result={'registered_cage_operator':'PASS','delete_and_regenerate_curves_handles':'PASS','cage_only_toggle':'PASS','four_wheels_ground':'PASS','surfaces':'NOT REACHED: curve gate unapproved'};r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v01';(r/'addon-tests.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);os._exit(0)

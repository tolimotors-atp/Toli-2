import sys,bpy,json,hashlib,os
from pathlib import Path
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');sys.path.insert(0,str(P/'tools/blender-addons'));import toli_mux_generator as a
from toli_mux_generator.geometry.curves import COLLECTION,generate_curves
from toli_mux_generator.parameters import values
a.register();bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-curve-generated-v01.blend'));s=bpy.context.scene
# Registered UI execution, visibility, references and quality sampling.
bpy.ops.toli_mux.curve_network();s.toli_mux.show_construction_curves=False;assert bpy.data.collections[COLLECTION].hide_viewport;s.toli_mux.show_construction_curves=True
s.toli_mux.reference_front=True;assert bpy.data.objects.get('REF_IMAGE_front');assert not bpy.data.objects['REF_IMAGE_front'].data.packed_file;s.toli_mux.reference_front=False
p=values(s)
def fingerprint():
 return hashlib.sha256(json.dumps([(o.name,[[list(b.co),list(b.handle_left),list(b.handle_right)] for b in o.data.splines[0].bezier_points]) for o in sorted(bpy.data.collections[COLLECTION].objects,key=lambda x:x.name)]).encode()).hexdigest()
a1=fingerprint();bpy.ops.toli_mux.curve_network();a2=fingerprint();assert a1==a2
s.toli_mux.quality='QUALITY';bpy.ops.toli_mux.curve_network();assert fingerprint()==a1;assert all(o.data.resolution_u==24 for o in bpy.data.collections[COLLECTION].objects)
s.toli_mux.quality='PREVIEW';s.toli_mux.bonnet_height+=.02;bpy.ops.toli_mux.curve_network();assert fingerprint()!=a1
result={'UI_operator':'PASS','show_curves_toggle':'PASS','reference_toggle_unpacked_original':'PASS','delete_and_regenerate_including_handles':'PASS','quality_preserves_design':'PASS','parameter_changes_curve':'PASS','surfaces':'NOT GENERATED: curve gate not accepted','surface_reproducibility':'NOT REACHED'};r=P/'tools/3d/isuzu-mux/code-generator/renders/curve-validation';(r/'addon-tests.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);os._exit(0)

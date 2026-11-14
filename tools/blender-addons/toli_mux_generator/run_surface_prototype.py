import bpy,sys,json,os
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'tools/blender-addons'))
import toli_mux_generator as addon
from toli_mux_generator.geometry.surface_patch import build,SURFACES
from toli_mux_generator.geometry.continuity import validate,fingerprint
from toli_mux_generator.parameters import values
addon.register();bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v04.blend'));s=bpy.context.scene;p=values(s)
assert bpy.ops.toli_mux.surface_prototype()=={'FINISHED'};a=fingerprint();build(s,p);assert fingerprint()==a
from toli_mux_generator.surface_ui import update
update(s.toli_mux,bpy.context);stats=validate(s,p);stats['reproducibility']='PASS';stats['prototype']='Three independent surface construction zones, not a full body'
r=P/'tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01';r.mkdir(parents=True,exist_ok=True);(r/'geometry-validation.json').write_text(json.dumps(stats,indent=2));(r/'patch-manifest.json').write_text(s['surface_prototype_manifest'])
for name,v in stats['zones'].items():
 print(name,json.dumps({k:v[k] for k in ['base','evaluated','base_control_symmetry_m','boundary_cracks','constraints']}),flush=True)
 assert v['base']['degenerate_faces']==v['evaluated']['degenerate_faces']==0
 assert v['base']['interior_nonmanifold_edges']==v['evaluated']['interior_nonmanifold_edges']==0
 assert v['boundary_cracks']==0,(name,v['base']['boundary_t_junctions'])
 assert v['base']['nonadjacent_triangle_overlap_pairs']==v['evaluated']['nonadjacent_triangle_overlap_pairs']==0
 assert v['base_control_symmetry_m']==0
 assert all(v['constraints'].values())
print(json.dumps(stats['total']),flush=True)
from toli_mux_generator.surface_diagnostics import setup,camera_for
setup(s);camera_for(s,'ALL','FRONT34')
bpy.ops.wm.save_as_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v01.blend'));print('PROTOTYPE SAVED',flush=True);os._exit(0)

import bpy,json,os,math
from pathlib import Path
O=Path(os.environ.get('MUX_SURFACE_OUTPUT',Path(__file__).resolve().parents[3]));A=O/'source/reconstruction/surface-v01';p=O/'source/reconstruction/isuzu-mux-greenhouse-surface-v01.blend';bpy.ops.wm.open_mainfile(filepath=str(p));bpy.data.orphans_purge(do_recursive=True);s=bpy.context.scene;g=json.loads((A/'gate-decision.json').read_text());s['STATUS']='G1 FAIL — MANUAL REFERENCE-CONSTRAINED RECONSTRUCTION HAS REACHED ITS RELIABLE LIMIT';s['GATES']=json.dumps({k:g[k] for k in ['G1','G2','G3','G4','G5','G6']});s['STOP']='No roof, pillars, side glass, rear glass or further manual correction loops';s['reference_priority']='PRIMARY O06; SECONDARY O07; VALIDATION O11; O10 contextual only';s['LIMIT_SCOPE']=g['scope'];bpy.ops.wm.save_as_mainfile(filepath=str(p));bpy.ops.wm.open_mainfile(filepath=str(p))
surfaces=[o for o in bpy.data.objects if o.type=='SURFACE'];assert len(surfaces)==1
o=surfaces[0];assert len(o.data.splines[0].points)==16 and not o.modifiers
assert all(math.isfinite(float(c)) for pt in o.data.splines[0].points for c in pt.co)
frozen=json.loads((A/'geometry-checks.json').read_text())['stance_signature']
for item in frozen:
 ob=bpy.data.objects[item['name']];assert [list(r) for r in ob.matrix_world]==item['matrix']
 if ob.type=='MESH':assert [list(v.co) for v in ob.data.vertices]==item['vertices']
assert len([o for o in bpy.data.objects if o.type=='MESH'])==8
assert len(bpy.data.meshes)==8,'Unexpected inherited mesh datablocks'
(A/'final-save-verification.json').write_text(json.dumps(dict(passed=True,reopened=True,only_one_new_surface=True,controls=16,stance_exactly_preserved=True,no_other_body=True,G1='FAIL',later_gates='NOT REACHED'),indent=2))

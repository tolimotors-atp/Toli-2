import bpy,json,os
from pathlib import Path
O=Path(os.environ.get('MUX_GREENHOUSE_OUTPUT',Path(__file__).resolve().parents[3]));A=O/'source/reconstruction/greenhouse-v02';p=O/'source/reconstruction/isuzu-mux-reference-constrained-v02.blend';bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;g=json.loads((A/'visual-gates.json').read_text());assert g['overall']=='FAIL'
s['STATUS']='GREENHOUSE GATE FAIL — header/glass curvature, C/D junctions and cross-car depth need correction. STOP: no other body.';s['acceptance_categories']=json.dumps(g['categories']);s['website_integration']='NOT ACTIVATED';s['stance']='V01 unchanged, exact mesh/transform comparison passed'
for o in list(bpy.data.objects):
 if o.type=='CURVE' and ' ACTUAL ' in o.name:bpy.data.objects.remove(o,do_unlink=True);continue
 if o.name.startswith('G') and o.type=='CURVE':o.name='Guide '+o.name;o.hide_render=True
for row in json.loads((A/'cross-section-cuts.json').read_text()):
 cu=bpy.data.curves.new(row['id']+' actual section','CURVE');cu.dimensions='3D'
 for a,b in row['actual_mesh_intersections']:
  sp=cu.splines.new('POLY');sp.points.add(1);sp.points[0].co=(row['x'],*a,1);sp.points[1].co=(row['x'],*b,1)
 ob=bpy.data.objects.new(row['id']+' ACTUAL '+row['region'],cu);bpy.context.collection.objects.link(ob);ob.hide_render=True;ob['method']='Actual triangle/plane intersection; not an idealized envelope'
s.camera=bpy.data.objects['V02 diagnostic neutral'];bpy.ops.wm.save_as_mainfile(filepath=str(p))
# Read the just-saved milestone independently before delivery.
bpy.ops.wm.open_mainfile(filepath=str(p));assert bpy.context.scene['STATUS'].startswith('GREENHOUSE GATE FAIL')
frozen=json.loads((A/'geometry-checks.json').read_text())['stance_signature']
for r in frozen:
 o=bpy.data.objects[r['name']];assert [list(x) for x in o.matrix_world]==r['matrix']
 if o.type=='MESH':assert [list(v.co) for v in o.data.vertices]==r['vertices']
assert sum(bool(i.packed_file) for i in bpy.data.images)>=14
(A/'final-save-verification.json').write_text(json.dumps(dict(saved_and_reopened=True,stance_unchanged=True,packed_references=14,overall='FAIL',no_other_body=True),indent=2))

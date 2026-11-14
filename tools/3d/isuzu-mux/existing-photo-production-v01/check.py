import bpy,bmesh,json,sys,os,math
from pathlib import Path
from mathutils import Vector,kdtree
P=Path(__file__).resolve().parents[4];B=P/'tools/3d/isuzu-mux';R=B/'code-generator/renders/existing-photo-production-v01';bpy.ops.wm.open_mainfile(filepath=str(B/'source/production/isuzu-mux-existing-photo-production-v01.blend'));s=bpy.context.scene
obs=[o for col in bpy.data.collections if col.name.startswith('M1_') for o in col.objects if o.type=='MESH'];dg=bpy.context.evaluated_depsgraph_get();rows=[];allco=[]
def stats(me):
 bm=bmesh.new();bm.from_mesh(me);out={'vertices':len(me.vertices),'triangles':sum(len(f.verts)-2 for f in bm.faces),'n_gons':sum(len(f.verts)>4 for f in bm.faces),'degenerate_faces':sum(f.calc_area()<1e-10 for f in bm.faces),'zero_length_edges':sum(e.calc_length()<1e-7 for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'boundary_edges':sum(e.is_boundary for e in bm.edges)};bm.free();return out
for o in obs:
 ev=o.evaluated_get(dg);me=ev.to_mesh();co=[o.matrix_world@v.co for v in me.vertices];allco+=co;rows.append({'object':o.name,'base':stats(o.data),'evaluated':stats(me)});ev.to_mesh_clear()
tree=kdtree.KDTree(len(allco))
for i,v in enumerate(allco):tree.insert(v,i)
tree.balance();sym=max(tree.find(Vector((v.x,-v.y,v.z)))[2] for v in allco)
lo=[min(v[k] for v in allco) for k in range(3)];hi=[max(v[k] for v in allco) for k in range(3)];totals={state:{key:sum(v[state][key] for v in rows) for key in rows[0][state]} for state in ['base','evaluated']}
centres=json.loads(s['wheel_centres']);nom=json.loads(s['nominal_framework']);assert len(centres)==4
for name,co in centres.items():
 o=bpy.data.objects[name];actual=[(min(v.co[k] for v in o.data.vertices)+max(v.co[k] for v in o.data.vertices))/2 for k in range(3)]
 assert (Vector(actual)-Vector(co)).length<1e-6
 assert abs(max(v.co.z for v in o.data.vertices)-min(v.co.z for v in o.data.vertices)-nom['tire_diameter'])<1e-6
 assert abs(abs(co[0])-nom['wheelbase']/2)<1e-9 and abs(abs(co[1])-nom['track']/2)<1e-9 and abs(co[2]-nom['tire_diameter']/2)<1e-9
print('Ground min / symmetry',lo[2],sym,flush=True)
assert abs(lo[2])<1e-6 and sym<1e-4
result={'totals':totals,'objects':rows,'evaluated_dimensions':[hi[k]-lo[k] for k in range(3)],'bounds':{'min':lo,'max':hi},'nominal_framework':nom,'wheelbase':nom['wheelbase'],'wheel_centres':centres,'wheel_object_transforms':{o.name:{'location':list(o.location),'rotation':list(o.rotation_euler),'scale':list(o.scale),'note':'Wheel coordinates are baked in the mesh; centre is recorded separately.'} for o in obs if o.name.startswith('ANCHOR_')},'symmetry_discrepancy':sym,'grounding':'PASS','fixed_wheel_anchors':'PASS','actual_wheel_mesh_centres_and_diameters':'PASS','note':'Base counts are half-body control meshes before symmetry/subdivision. Counts exclude studio and image reference empties. Per-object manifoldness does not establish a joined watertight vehicle.'}
(R/'geometry-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['totals','evaluated_dimensions','symmetry_discrepancy','grounding','fixed_wheel_anchors']}),flush=True);os._exit(0)

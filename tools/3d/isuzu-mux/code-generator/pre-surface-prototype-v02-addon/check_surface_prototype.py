import bpy,sys,json,os,hashlib,math
from pathlib import Path
from mathutils import Vector,kdtree
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'tools/blender-addons'))
import toli_mux_generator as addon
from toli_mux_generator.parameters import values
from toli_mux_generator.geometry.surface_patch import build,SURFACES,CONTROL
from toli_mux_generator.geometry.continuity import validate,fingerprint
from toli_mux_generator.geometry.flow_cage import sample_x,points
from toli_mux_generator.geometry.section_network import loop_samples
addon.register();bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v01.blend'));s=bpy.context.scene;p=values(s);r=P/'tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01'
def constraint_sig():
 return hashlib.sha256(json.dumps([(o.name,[[list(b.co),list(b.handle_left),list(b.handle_right)] for b in o.data.splines[0].bezier_points]) for o in sorted(bpy.data.collections['TOLI_MUX_REFERENCE_CAGE'].objects,key=lambda o:o.name)]).encode()).hexdigest()
wheel={o.name:[list(o.location),list(o.rotation_euler),list(o.scale)] for o in bpy.data.objects if o.name.startswith('CAGE_WHEEL')};ref=constraint_sig();build(s,p);sig=fingerprint();build(s,p);assert fingerprint()==sig and constraint_sig()==ref
try:build(s,p|{'length':p['length']+.1});raise AssertionError('Unapproved dimension accepted')
except ValueError:pass
assert fingerprint()==sig
for zone in ['A','B','C','ALL']:
 s.toli_mux.surface_zone=zone
 assert all(o.hide_render==(zone!='ALL' and o['zone']!=zone) for o in bpy.data.collections[SURFACES].objects)
 s.toli_mux.surface_control_sections=True;assert any(not o.hide_render for o in bpy.data.collections[CONTROL].objects)
 s.toli_mux.surface_control_sections=False;assert all(o.hide_render for o in bpy.data.collections[CONTROL].objects)
s.toli_mux.curve_cage_only=True;assert bpy.data.collections[SURFACES].hide_viewport and bpy.data.collections[SURFACES].hide_render
s.toli_mux.curve_cage_only=False;assert not bpy.data.collections[SURFACES].hide_viewport
assert wheel=={o.name:[list(o.location),list(o.rotation_euler),list(o.scale)] for o in bpy.data.objects if o.name.startswith('CAGE_WHEEL')}
stats=validate(s,p)
for v in stats['zones'].values():
 assert v['base']['degenerate_faces']==v['evaluated']['degenerate_faces']==0
 assert v['base']['interior_nonmanifold_edges']==v['evaluated']['interior_nonmanifold_edges']==v['boundary_cracks']==0
 assert v['base']['nonadjacent_triangle_overlap_pairs']==v['evaluated']['nonadjacent_triangle_overlap_pairs']==0
 assert v['base_control_symmetry_m']==0 and all(v['constraints'].values())
 assert all(q['type'] in ['SOFT','CONTROLLED','DEFINED'] and q['position_gap_m']==0 for q in v['shared_boundary_normal_diagnostics'])
assert len(bpy.data.collections[SURFACES].objects)==3
# Quantify controlled departures rather than claiming every internal V04 guide was followed.
a=bpy.data.objects['SURFACE_ZONE_A'];center=[v.co for v in a.data.vertices if abs(v.co.y)<1e-8 and v.co.x<-.9];cz=[abs(v.z-sample_x(bpy.data.objects['TRACE_BONNET_CENTER'],v.x).z) for v in center]
c=bpy.data.objects['SURFACE_ZONE_C'];lamp=loop_samples(bpy.data.objects['TRACE_TAIL_LAMP']);diff=[]
for v in lamp:
 candidates=[w.co for w in c.data.vertices if abs(w.co.y-v.y)<1e-6 and abs(w.co.z-v.z)<1e-6]
 assert candidates,'Lamp Y/Z anchor missing'
 diff.append(min(abs(w.x-v.x) for w in candidates))
# Evaluated aperture proximity is diagnostic; Catmull-Clark is not an exact interpolation of the reference curve.
b=bpy.data.objects['SURFACE_ZONE_B'];ev=b.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();edge_count={e.index:0 for e in me.edges};lookup={tuple(sorted(e.vertices)):e.index for e in me.edges}
for f in me.polygons:
 for pair in f.edge_keys:edge_count[lookup[tuple(sorted(pair))]]+=1
ids=set(i for e in me.edges if edge_count[e.index]==1 for i in e.vertices);tree=kdtree.KDTree(len(ids))
for j,i in enumerate(ids):tree.insert(me.vertices[i].co,j)
tree.balance();qdist=max(tree.find(v)[2] for v in loop_samples(bpy.data.objects['TRACE_QUARTER_GLASS']));ev.to_mesh_clear()
depart={'bonnet_center_max_z_departure_nominal_m':max(cz),'lamp_yz_control_anchors':'PRESERVED','lamp_x_max_departure_nominal_m':max(diff),'quarter_window_evaluated_boundary_proximity_max_m':qdist,'interpretation':'Nominal model coordinates only; nearest evaluated open-edge sample is a diagnostic, not physical reconstruction accuracy.'}
labels=json.loads(b['patch_labels']);glass_id=labels.index('rear_glass');faceattr=b.data.attributes['patch_id'];glassids=set(i for poly in b.data.polygons if faceattr.data[poly.index].value==glass_id for i in poly.vertices);gd=points(bpy.data.objects['TRACE_REAR_GLASS']);rear_depart=[]
from toli_mux_generator.geometry.flow_cage import cubic
for t in [0,.18,.43,.70,1.]:
 u=t*2;v=cubic(gd[2],gd[3],u)[0] if u<=1 else cubic(gd[3],gd[4],u-1)[0];cand=[b.data.vertices[i].co for i in glassids if abs(b.data.vertices[i].co.y-v.y)<1e-6 and abs(b.data.vertices[i].co.z-v.z)<1e-6];assert cand;rear_depart.append(min(abs(co.x-v.x) for co in cand))
depart['rear_glass_yz_section_samples']='PRESERVED';depart['rear_glass_x_section_max_departure_m']=max(rear_depart)
old=json.loads((r/'pre-rear-fix-zone-signatures.json').read_text());now={o['zone']:hashlib.sha256(json.dumps(([list(v.co) for v in o.data.vertices],[list(f.vertices) for f in o.data.polygons])).encode()).hexdigest() for o in bpy.data.collections[SURFACES].objects};assert old['A']==now['A'] and old['C']==now['C'];(r/'zone-render-cache-validation.json').write_text(json.dumps({'unchanged_zones':['A','C'],'pre_rear_fix':old,'final':now,'reason':'Only Zone B control geometry changed; A/C rendering materials, camera fitting and lighting unchanged'},indent=2));(r/'geometry-validation.json').write_text(json.dumps(stats|{'reproducibility':'PASS'},indent=2))
(r/'constraint-departures.json').write_text(json.dumps(depart,indent=2))
result={'registered_generator':'PASS','delete_and_regenerate':'PASS','V04_constraints_unchanged_in_memory':'PASS','fixed_wheel_anchors':'PASS','dimension_lock_rejection_preserves_candidate':'PASS','zone_isolation_and_control_section_toggles':'PASS','curve_cage_only_mode':'PASS','only_three_surface_zones':'PASS','base_control_symmetry_m':0.,'topology_checks':'PASS','nonadjacent_triangle_overlap_checks':'PASS','A_C_geometry_unchanged_after_B_fix':'PASS','full_body':'NOT GENERATED','GLB':'NOT EXPORTED'};(r/'addon-tests.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);print(json.dumps(depart),flush=True);os._exit(0)

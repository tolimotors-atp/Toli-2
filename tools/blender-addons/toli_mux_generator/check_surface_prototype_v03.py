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
addon.register();bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v03.blend'));s=bpy.context.scene;p=values(s);r=P/'tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03'
def complete_sig():
 return fingerprint(),[(o.name,[v.value for v in o.data.attributes['crease_edge'].data],[(m.type,m.levels,m.render_levels) for m in o.modifiers]) for o in bpy.data.collections[SURFACES].objects]
def constraint_sig():
 return hashlib.sha256(json.dumps([(o.name,[[list(b.co),list(b.handle_left),list(b.handle_right)] for b in o.data.splines[0].bezier_points]) for o in sorted(bpy.data.collections['TOLI_MUX_REFERENCE_CAGE'].objects,key=lambda o:o.name)]).encode()).hexdigest()
wheel={o.name:[list(o.location),list(o.rotation_euler),list(o.scale)] for o in bpy.data.objects if o.name.startswith('CAGE_WHEEL')};ref=constraint_sig();build(s,p,version=3);sig=complete_sig();build(s,p,version=3);assert complete_sig()==sig and constraint_sig()==ref
try:build(s,p|{'length':p['length']+.1},version=3);raise AssertionError('Unapproved dimension accepted')
except ValueError:pass
assert complete_sig()==sig
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
assert all(len(f.vertices)==4 for o in bpy.data.collections[SURFACES].objects for f in o.data.polygons)
assert all(o.modifiers[0].levels==o.modifiers[0].render_levels==2 for o in bpy.data.collections[SURFACES].objects)
# Quantify controlled departures rather than claiming every internal V04 guide was followed.
a=bpy.data.objects['SURFACE_ZONE_A'];center=[v.co for v in a.data.vertices if abs(v.co.y)<1e-8 and v.co.x<-.9];cz=[abs(v.z-sample_x(bpy.data.objects['TRACE_BONNET_CENTER'],v.x).z) for v in center]
c=bpy.data.objects['SURFACE_ZONE_C'];clabels=json.loads(c['patch_labels']);boundary_ids=set()
for edge in c.data.edges:
 names={clabels[c.data.attributes['patch_id'].data[f.index].value] for f in c.data.polygons if tuple(sorted(edge.vertices)) in [tuple(sorted(pair)) for pair in f.edge_keys]}
 if names=={'lamp_return','lamp_edge'}:boundary_ids.update(edge.vertices)
lamp=loop_samples(bpy.data.objects['TRACE_TAIL_LAMP']);diff=[]
for v in lamp:
 candidates=[c.data.vertices[i].co for i in boundary_ids if abs(c.data.vertices[i].co.y-v.y)<1e-6 and abs(c.data.vertices[i].co.z-v.z)<1e-6]
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

(r/'constraint-departures.json').write_text(json.dumps(depart,indent=2))
result={'registered_generator':'PASS','delete_and_regenerate':'PASS','fixed_V04_constraints':'PASS','fixed_wheel_transforms':'PASS','dimension_rejection_preserves_candidate':'PASS','zone_and_control_visibility':'PASS','cage_only_mode':'PASS','three_zones_only':'PASS','strict_base_symmetry':'PASS','topology_and_overlap_checks':'PASS'}
(r/'addon-tests.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);os._exit(0)

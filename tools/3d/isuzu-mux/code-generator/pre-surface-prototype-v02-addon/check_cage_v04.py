import bpy,sys,json,os,hashlib,math
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'tools/blender-addons'))
import toli_mux_generator as a
from toli_mux_generator.geometry.reference_cage import COL
from toli_mux_generator.geometry.depth_cage import LEVELS,STATIONS
from toli_mux_generator.geometry.flow_cage import generate_cage as v03
from toli_mux_generator.geometry.flow_cage import curvature_audit,JOIN_CURVES,JOIN_STATION,points
from toli_mux_generator.parameters import values,BASE
from toli_mux_generator.geometry.soft_body import generate_soft
from toli_mux_generator.geometry.rounded import ROUNDED
from toli_mux_generator import validation
r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04';a.register();bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v04.blend'));s=bpy.context.scene;p=values(s)
def coordinates(n):return [[list(b.co),list(b.handle_left),list(b.handle_right)] for b in points(bpy.data.objects[n])]
def sig():return hashlib.sha256(json.dumps([(o.name,coordinates(o.name),[list(m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value) for m in o.data.materials]) for o in sorted(bpy.data.collections[COL].objects,key=lambda o:o.name)]).encode()).hexdigest()
def j03():return {n:coordinates(n)[i] for n,i in [('TRACE_A_PILLAR',-1),('TRACE_ROOF_EDGE',0)]}
v03(s,p);protected={n:coordinates(n) for n in ['TRACE_SIDE_MASTER','TRACE_FRONT_WINDOW','TRACE_REAR_WINDOW','TRACE_BONNET_CENTER','TRACE_ROOF_CENTER']};j=j03();baseline=curvature_audit(bpy.data.collections[COL]);(r/'curvature-v03.json').write_text(json.dumps(baseline,indent=2))
bpy.ops.toli_mux.reference_cage();one=sig();assert j03()==j
for n,c in protected.items():assert coordinates(n)==c,n
bpy.ops.toli_mux.reference_cage();assert one==sig();assert j03()==j
co=[b.co.copy() for o in bpy.data.collections[COL].objects for b in points(o)];error=max(min((Vector((v.x,-v.y,v.z))-w).length for w in co) for v in co);assert error==0
assert len([o for o in bpy.data.collections[COL].objects if o.name.startswith('SECTION_BONNET_')])==5
assert all(len(points(bpy.data.objects['SECTION_BONNET_'+str(i)]))==9 for i in range(5))
assert max(b.co.z for b in points(bpy.data.objects['SECTION_D_BODY']))<=1.575*p['height']/1.86+1e-7
assert points(bpy.data.objects['TRACE_REAR_BUMPER'])[-1].co.x<=2.30*p['length']/4.825+1e-7
assert all(o.type=='CURVE' for o in bpy.data.collections[COL].objects)
for o in bpy.data.collections['TOLI_CAGE_SUPPORT'].objects:
 if o.name.startswith('CAGE_WHEEL'):assert abs(abs(o.location.x)-p['wheelbase']/2)<1e-6 and abs(o.location.z-p['tire_diameter']/2)<1e-6
initial={o.name:(o.hide_viewport,o.hide_render) for o in bpy.data.collections[COL].objects}
for join in JOIN_CURVES:
 s.toli_mux.join_debug=join
 assert not bpy.data.objects['SLICE_'+JOIN_STATION[join]].hide_viewport
 assert all(o.hide_viewport for o in bpy.data.collections[COL].objects if o.name.removesuffix('_R') not in JOIN_CURVES[join] and o.name!='SLICE_'+JOIN_STATION[join]),join
 s.toli_mux.show_curvature_combs=True
 assert any(not o.hide_viewport for o in bpy.data.collections['TOLI_CAGE_COMBS'].objects),join
bpy.ops.toli_mux.reference_cage();assert not bpy.data.objects['TRACE_REAR_GLASS'].hide_viewport
s.toli_mux.curve_cage_only=False;assert bpy.data.collections['TOLI_CAGE_COMBS'].hide_viewport
s.toli_mux.curve_cage_only=True;assert not bpy.data.collections['TOLI_CAGE_COMBS'].hide_viewport
s.toli_mux.join_debug='OFF';s.toli_mux.show_curvature_combs=False
assert initial=={o.name:(o.hide_viewport,o.hide_render) for o in bpy.data.collections[COL].objects}
flow=json.loads(s['v04_flow_constraints']);assert all(row.get('gap_m',0)==0 for row in flow.values())
for n in ['J03','J04','J05','J07']:assert flow[n]['tangent_angle_deg']<.05,flow[n]
curves=json.loads(s['v04_curvature_audit']);flags=[];values_k=[]
for join,rows in curves.items():
 for row in rows:
  for q in row['internal_junctions']:
   assert all(math.isfinite(v) for v in q['curvature_before']+q['curvature_after']);values_k+=q['curvature_before']+q['curvature_after']
   if q['relative_curvature_jump']>.65:flags.append({'join':join,'curve':row['curve'],'control':q['control_index'],'relative_jump':q['relative_curvature_jump']})
(r/'curvature-warnings.json').write_text(json.dumps({'interpretation':'Heuristic >65% relative jump; character cuts and intersections require visual classification, not automatic failure','warnings':flags,'maximum_sampled_curvature':max(values_k)},indent=2))
# Adjacent-section normal proxies; these are cross-products of guide tangents, not body normals.
normals=[];rail=points(bpy.data.objects['TRACE_BONNET_EDGE'])
for i in range(5):
 ps=points(bpy.data.objects['SECTION_BONNET_'+str(i)]);bp=ps[2];near=min(rail,key=lambda b:abs(b.co.x-bp.co.x));long=near.handle_right-near.handle_left;cross=bp.handle_right-bp.handle_left;n=long.cross(cross).normalized();assert n.length>.99
 normals.append(n)
(r/'flow-normal-proxies.json').write_text(json.dumps({'scope':'Bonnet edge longitudinal/transverse tangent cross-products; inferred cage, no surface normals','normal_vectors':[list(n) for n in normals],'adjacent_angles_deg':[math.degrees(a.angle(b)) for a,b in zip(normals,normals[1:])]},indent=2))
from toli_mux_generator.convergence_data import EVIDENCE
assert set(EVIDENCE)==set(['J01','J02','J04','J05','J06','J07','J08'])
assert s['v04_no_added_controls']
for n in ['TRACE_REAR_GLASS','TRACE_REAR_GLASS_R']:
 assert not bpy.data.objects[n].data.splines[0].use_cyclic_u
 assert len(points(bpy.data.objects[n]))==6
 assert points(bpy.data.objects[n])[0].co.y==0 and points(bpy.data.objects[n])[-1].co.y==0
out={'no_added_structural_curves_or_controls':'PASS','reference_evidence_all_seven_regions':'PASS','reproducibility':'PASS','j03_exact_endpoint_handle_preservation':'PASS','side_window_and_primary_silhouette_preservation':'PASS','fixed_wheels':'PASS','five_bonnet_sections':'PASS','join_debug_all_eight_and_restore':'PASS','curvature_combs_toggle':'PASS','finite_curvature_sampling':'PASS','symmetry_m':error,'surfaces':'NOT STARTED'};(r/'addon-tests.json').write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
bpy.ops.wm.read_factory_settings(use_empty=True);validation.COLLECTION=ROUNDED;top={}
for mode in ['PREVIEW','QUALITY']:
 pp=dict(BASE,quality=mode);generate_soft(bpy.context.scene,pp);v=validation.validate(bpy.context.scene,pp);assert v['degenerate_faces']==0 and v['nonmanifold_edges']==0 and v['symmetry'];v['scope']='Legacy soft-body regression only; V04 remains a curve cage';top[mode]=v
(r/'topology-regression.json').write_text(json.dumps(top,indent=2));print(json.dumps(top),flush=True);os._exit(0)

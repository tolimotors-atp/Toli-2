"""Preserve V01; regenerate and check only the three V02 experimental zones."""
import bpy,sys,json,os,hashlib
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'tools/blender-addons'))
import toli_mux_generator as addon
from toli_mux_generator.geometry.surface_patch import build,SURFACES
from toli_mux_generator.geometry.continuity import validate,fingerprint
from toli_mux_generator.parameters import values
from toli_mux_generator.surface_diagnostics import setup,camera_for
from toli_mux_generator.surface_ui import update
from toli_mux_generator.geometry.flow_cage import points,cubic
R=P/'tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v02';R.mkdir(parents=True,exist_ok=True)

def guide_signature():
 col=bpy.data.collections['TOLI_MUX_REFERENCE_CAGE']
 return hashlib.sha256(repr([(o.name,[(tuple(v.co),tuple(v.handle_left),tuple(v.handle_right)) for sp in o.data.splines for v in sp.bezier_points]) for o in col.objects if o.type=='CURVE']).encode()).hexdigest()

def boundary_metrics():
 out={};col=bpy.data.collections['TOLI_MUX_REFERENCE_CAGE'];o=bpy.data.objects['SURFACE_ZONE_B'];labels=json.loads(o['patch_labels'])
 def curve(name,closed):
  ps=points(col.objects['TRACE_'+name]);pairs=list(zip(ps,ps[1:]))+([(ps[-1],ps[0])] if closed else [])
  return [cubic(a,b,t/32)[0] for a,b in pairs for t in range(32)]
 q=curve('QUARTER_GLASS',True)
 g=points(col.objects['TRACE_REAR_GLASS']);rear=[cubic(a,b,t/32)[0] for a,b in zip(g[:4],g[1:5]) for t in range(33)]
 rear += [Vector((v.x,-v.y,v.z)) for v in rear[:]]
 def metric(mesh,name,refs,yz):
  linked={tuple(sorted(e.vertices)):[] for e in mesh.edges};ids=mesh.attributes['patch_id']
  for f in mesh.polygons:
   for key in f.edge_keys:linked[tuple(sorted(key))].append(labels[ids.data[f.index].value])
  edges=[]
  for key,ls in linked.items():
   if len(ls)!=2:continue
   ok=set(ls)=={'window_return','quarter_frame'} if name=='quarter_glass' else ('rear_glass' in ls and len(set(ls))==2)
   if ok:
    a,b=[mesh.vertices[i].co.copy() for i in key]
    if name=='quarter_glass' and a.y>0:continue
    if yz:a.x=b.x=0
    edges.append((a,b))
  assert edges,(name,'Boundary extraction failed')
  ds=[]
  for p0 in refs:
   p=p0.copy()
   if yz:p.x=0
   ds.append(min((p-(a+(b-a)*max(0,min(1,(p-a).dot(b-a)/max((b-a).length_squared,1e-20))))).length for a,b in edges))
  return {'mean':sum(ds)/len(ds),'maximum':max(ds),'samples':len(ds),'boundary_edges':len(edges),'space':'YZ silhouette; X depth inferred' if yz else '3D model coordinates','direction':'dense fixed reference curve to actual patch-interface edge segments'}
 for state in ['base','evaluated']:
  if state=='evaluated':ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
  else:mesh=o.data
  out[state]={'quarter_glass':metric(mesh,'quarter_glass',q,False),'rear_glass':metric(mesh,'rear_glass',rear,True)}
  if state=='evaluated':ev.to_mesh_clear()
 return out

addon.register();bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v01.blend'));s=bpy.context.scene;p=values(s);original=fingerprint();guides=guide_signature();wheels={o.name:list(o.location) for o in bpy.data.objects if o.name.startswith('CAGE_WHEEL')}
baseline=validate(s,p);old_metrics=boundary_metrics();setup(s);cameras={}
for z in 'ABC':
 for view in (['FRONT','FRONT34','SIDE'] if z=='A' else ['SIDE','REAR34','REAR']):
  for close in [False,True]:
   c=camera_for(s,z,view,close);cameras[f'{z}/{view}/{int(close)}']={'location':list(c.location),'rotation':list(c.rotation_euler),'scale':c.data.ortho_scale}
(R/'fixed-v01-cameras.json').write_text(json.dumps(cameras,indent=2))
build(s,p);assert fingerprint()==original,'Default V01 generator changed';build(s,p,version=2);update(s.toli_mux,bpy.context);a=fingerprint();stats=validate(s,p);new_metrics=boundary_metrics()
# Deletes all candidate geometry through the same public regenerate operator used by the panel.
assert bpy.ops.toli_mux.surface_prototype()=={'FINISHED'};assert fingerprint()==a
assert guide_signature()==guides;assert {o.name:list(o.location) for o in bpy.data.objects if o.name.startswith('CAGE_WHEEL')}==wheels
try:build(s,{**p,'length':p['length']+.1},version=2);raise AssertionError('Invalid dimensions accepted')
except ValueError:assert fingerprint()==a
for z,v in stats['zones'].items():
 print(z,json.dumps({k:v[k] for k in ['base','evaluated','base_control_symmetry_m','boundary_cracks','constraints']}),flush=True)
for z,v in stats['zones'].items():
 for state in ['base','evaluated']:
  for field in ['degenerate_faces','interior_nonmanifold_edges','nonadjacent_triangle_overlap_pairs']:assert v[state][field]==0,(z,state,field,v[state][field])
 assert v['boundary_cracks']==v['base_control_symmetry_m']==0
 assert all(v['constraints'].values())
stats['reproducibility']='PASS';stats['default_v01_regression']='PASS';stats['fixed_guides_and_wheels']='PASS';stats['invalid_dimensions_rejected']='PASS';stats['fingerprint']=a
(R/'geometry-validation.json').write_text(json.dumps(stats,indent=2));(R/'v01-geometry.json').write_text(json.dumps(baseline,indent=2));(R/'boundary-deviations.json').write_text(json.dumps({'V01':old_metrics,'V02':new_metrics,'units':'Uncalibrated model-space nominal metres; diagnostic, not physical measurement.'},indent=2));(R/'patch-manifest.json').write_text(s['surface_prototype_manifest'])
s.toli_mux.surface_zone='ALL';s.toli_mux.surface_constraints=False;update(s.toli_mux,bpy.context);camera_for(s,'ALL','FRONT34');bpy.ops.wm.save_as_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v02.blend'));print('V02 SAVED',json.dumps(stats['total']),flush=True);os._exit(0)

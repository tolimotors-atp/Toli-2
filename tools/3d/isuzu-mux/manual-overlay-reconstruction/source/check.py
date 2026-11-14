import bpy,bmesh,json,sys,os,math
from pathlib import Path
from mathutils import Vector,kdtree
from bpy_extras.object_utils import world_to_camera_view
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';W=B/'manual-overlay-reconstruction';bpy.ops.wm.open_mainfile(filepath=str(B/'source/production/isuzu-mux-manual-overlay-v01.blend'));s=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get()
def stats(me):
 bm=bmesh.new();bm.from_mesh(me);d={'vertices':len(bm.verts),'triangles':sum(len(f.verts)-2 for f in bm.faces),'quads':sum(len(f.verts)==4 for f in bm.faces),'n_gons':sum(len(f.verts)>4 for f in bm.faces),'degenerate_faces':sum(f.calc_area()<1e-10 for f in bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'boundary_edges':sum(e.is_boundary for e in bm.edges),'interior_nonmanifold_edges':sum(not e.is_manifold and not e.is_boundary for e in bm.edges)};bm.free();return d
allco=[];rows=[]
obs=list(bpy.data.collections['MUX_PRIMARY_SURFACES'].objects)+list(bpy.data.collections['MUX_WHEELS'].objects)
for o in obs:
 ev=o.evaluated_get(dg);me=ev.to_mesh();allco.extend(o.matrix_world@v.co for v in me.vertices);rows.append({'object':o.name,'base':stats(o.data),'evaluated':stats(me)});ev.to_mesh_clear()
tree=kdtree.KDTree(len(allco))
for i,v in enumerate(allco):tree.insert(v,i)
tree.balance();sym=max(tree.find(Vector((v.x,-v.y,v.z)))[2] for v in allco)
lo=[min(v[k] for v in allco) for k in range(3)];hi=[max(v[k] for v in allco) for k in range(3)];totals={state:{key:sum(r[state][key] for r in rows) for key in rows[0][state]} for state in ['base','evaluated']};nom=json.loads(s['nominal_framework']);anchors=json.loads(s['wheel_centres']);wheelchecks=[]
for name,expected in anchors.items():
 o=bpy.data.objects[name];co=[o.matrix_world@v.co for v in o.data.vertices];actual=[(max(v[k] for v in co)+min(v[k] for v in co))/2 for k in range(3)];diam=max(v.z for v in co)-min(v.z for v in co);assert (Vector(actual)-Vector(expected)).length<1e-6;assert abs(diam-nom['tire_diameter'])<1e-6;assert abs(min(v.z for v in co))<1e-6;wheelchecks.append({'object':name,'actual_center':actual,'diameter':diam,'ground_min':min(v.z for v in co)})
assert sym<1e-5 and totals['evaluated']['degenerate_faces']==0
fits=json.loads((W/'cameras/reference-fits.json').read_text());projections=[]
for f in fits:
 if f['type']=='ORTHO':continue
 cam=bpy.data.objects['REFERENCE_FIT_'+f['id']];s.camera=cam;bpy.context.view_layer.update();delta=[]
 for a in f['anchors']:
  uv=world_to_camera_view(s,cam,Vector(a['world']));xy=[uv.x*800,(1-uv.y)*520];delta.append(math.dist(xy,a['projected']))
 assert max(delta)<.01,(f['id'],delta)
 projections.append({'id':f['id'],'blender_vs_saved_fit_max_error_px':max(delta)})
(W/'diagnostics/scene-cameras.json').write_text(json.dumps({f['id']:{'position':list(bpy.data.objects['REFERENCE_FIT_'+f['id']].location),'rotation_euler':list(bpy.data.objects['REFERENCE_FIT_'+f['id']].rotation_euler)} for f in fits},indent=2))
# Exercise the embedded convenience operators in background; viewport presentation still requires UI.
exec(compile(bpy.data.texts['overlay_tools.py'].as_string(),'overlay_tools.py','exec'))
for mode in ['REFERENCE','MODEL','HALF','SILHOUETTE','WIRE']:
 result=bpy.ops.mux.reference_overlay(mode=mode);assert result=={'FINISHED'}
 if mode=='REFERENCE':assert all(o.hide_get() for o in bpy.data.collections['MUX_PRIMARY_SURFACES'].objects)
 if mode=='MODEL':assert not any(o.hide_get() for o in bpy.data.collections['MUX_PRIMARY_SURFACES'].objects)
result={'totals':totals,'objects':rows,'bounds':{'min':lo,'max':hi},'evaluated_dimensions':[hi[k]-lo[k] for k in range(3)],'nominal_framework':nom,'actual_wheel_mesh_checks':wheelchecks,'wheelbase':abs(anchors['Wheel_REAR_NEG_Y'][0]-anchors['Wheel_FRONT_NEG_Y'][0]),'symmetry_discrepancy':sym,'camera_projection_checks':projections,'overlay_operator_self_check':'PASS; background execution, interactive viewport not user-tested','note':'Open patch boundaries are intentional at this diagnostic stage. Separate patches are NOT a watertight or G1-joined production shell; boundary gaps and overlap remain visual failures. Technical validity does not imply recognition.'}
(W/'diagnostics/geometry-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['totals','evaluated_dimensions','symmetry_discrepancy']}),flush=True);os._exit(0)

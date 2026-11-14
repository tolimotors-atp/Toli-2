import bpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parents[3];p=O/'source/reconstruction/isuzu-mux-reference-constrained-v01.blend';bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;c=bpy.data.objects['Diagnostic side']
def px(v):
 a=world_to_camera_view(s,c,v);return [a.x*1000,(1-a.y)*650]
a=px(Vector((-.5,0,0)));b=px(Vector((.5,0,0)));scale=506/(b[0]-a[0])
def aligned(v):
 x,y=px(v);return [280+(x-a[0])*scale,455+(y-a[1])*scale]
edges=[]
for ob in bpy.data.objects:
 if ob.type=='MESH' and not any(k in ob.name for k in ['Tire','Cylinder']):
  if ob.name.startswith('Authored'):
   for e in ob.data.edges:
    vs=[ob.matrix_world@ob.data.vertices[i].co for i in e.vertices]
    if all(v.y<-.2 for v in vs):edges.append([aligned(v) for v in vs])
  elif ob.name.endswith('-1'):
   for e in ob.data.edges:edges.append([aligned(ob.matrix_world@ob.data.vertices[i].co) for i in e.vertices])
 elif ob.type=='CURVE' and ob.name.endswith('-1'):
  for spline in ob.data.splines:
   vs=[aligned(ob.matrix_world@Vector(v.co[:3])) for v in spline.points];edges.extend([[a,b] for a,b in zip(vs,vs[1:])])
meshes=[ob for ob in bpy.data.objects if ob.type=='MESH'];assert all(math.isfinite(float(x)) for ob in meshes for v in ob.data.vertices for x in v.co)
tires=[ob for ob in meshes if ob.name.startswith('Tire stance proxy')];assert len(tires)==4
grounds=[min((ob.matrix_world@v.co).z for v in ob.data.vertices) for ob in tires];assert max(abs(z) for z in grounds)<1e-5
assert sum(bool(i.packed_file) for i in bpy.data.images)>=7
s['STATUS']='GREENHOUSE GATE FAIL — needs curved glass, integrated roof/pillars and depth refinement; STOP before bonnet/body'
bpy.ops.wm.save_as_mainfile(filepath=str(p))
(O/'source/reconstruction/reference-constrained-v01/reopen-validation.json').write_text(json.dumps({'opened_saved_blend':True,'finite_vertices':True,'four_tire_ground_heights':grounds,'packed_reference_count':sum(bool(i.packed_file) for i in bpy.data.images),'mesh_count':len(meshes),'vertices':sum(len(o.data.vertices) for o in meshes),'triangles':sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in meshes),'gate':'FAIL','overlay_is_manual_2D_alignment_not_calibration':True,'projected_edges':edges},indent=2))

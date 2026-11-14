"""Second macro-only correction; no identity/detail pass is implied."""
import bpy,json,math
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=bpy.context.scene;o=bpy.data.objects['BODY_PASS3A_PROPORTION_STUDY']
# Narrow the swollen upper quarter and reduce the excessively square rear roof end.
for v in o.data.vertices:
 x,y,z=v.co
 upper=max(0,min(1,(z-1.20)/.55))
 if x< -1.65:
  influence=min(1,(-x-1.65)/.55)*upper
  v.co.z-=.045*influence;v.co.x+=.045*influence
 if .30<x<1.05:
  # Move the cowl-side transition toward the front without flattening the roof crown.
  v.co.x+=.035*math.sin((x-.30)/.75*math.pi)*max(0,1-abs(z-1.42)/.4)
 v.co.y-=.018*upper*max(0,min(1,(abs(x)-1.2)/.6))*min(1,abs(y)/.5)
assert all(v.co.y>=-1e-7 for v in o.data.vertices), 'Mirror half crossed centerline'
o.data.update();s['status']='PASS 3A REVISED — PROPORTION GATE STILL REQUIRED'
for f in ['source/milestones/isuzu-mux-body-pass3a-refined.blend','source/milestones/isuzu-mux-body-pass3.blend']:
 bpy.ops.wm.save_as_mainfile(filepath=str(R/f))
mat=bpy.data.materials.get('PASS3A FLAT GREY') or bpy.data.materials.new('PASS3A FLAT GREY');mat.use_nodes=True;shader=mat.node_tree.nodes['Principled BSDF'];shader.inputs['Base Color'].default_value=(.38,.40,.42,1);shader.inputs['Roughness'].default_value=.65;s.view_layers[0].material_override=mat;s.render.engine='CYCLES';s.cycles.samples=6
cam=s.camera;cam.data.type='PERSP';cam.data.lens=65
views={'front':(9.5,0,1.55),'left':(0,10.4,1.65),'right':(0,-10.4,1.65),'rear':(-9.5,0,1.55),'front-three-quarter':(7.8,6.2,3.1),'rear-three-quarter':(-7.8,6.2,3.1)}
for n,p in views.items():
 cam.location=p;cam.rotation_euler=(Vector((0,0,.95))-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(R/'renders'/('body-v04-'+n+'.png'));bpy.ops.render.render(write_still=True)
d=s.evaluated_depsgraph_get() if hasattr(s,'evaluated_depsgraph_get') else bpy.context.evaluated_depsgraph_get()
stats={'vertices':0,'triangles':0,'stage':'Pass 3A revised only; not identity or finish validation','production_textures':0}
for ob in s.objects:
 if ob.type=='MESH' and ob.name!='REVIEW_FLOOR':
  ev=ob.evaluated_get(d);m=ev.to_mesh();m.calc_loop_triangles();assert all(math.isfinite(c) for v in m.vertices for c in v.co);stats['vertices']+=len(m.vertices);stats['triangles']+=len(m.loop_triangles);ev.to_mesh_clear()
(R/'source/pass3-statistics.json').write_text(json.dumps(stats,indent=2))

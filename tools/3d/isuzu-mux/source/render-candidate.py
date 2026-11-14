import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
scene=bpy.context.scene
stats={'stage':'body cage, not approved','vertices':0,'triangles':0,'materials':len(bpy.data.materials),'texture_images':len(bpy.data.images),'texture_dimensions':{i.name:list(i.size) for i in bpy.data.images},'textures_note':'Packed reference images only; no production textures','meshes':0}
deps=bpy.context.evaluated_depsgraph_get()
for o in scene.objects:
 if o.type=='MESH' and o.name!='REVIEW_FLOOR':
  ev=o.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();stats['vertices']+=len(me.vertices);stats['triangles']+=len(me.loop_triangles);stats['meshes']+=1
  assert all(math.isfinite(c) for v in me.vertices for c in v.co),o.name
  ev.to_mesh_clear()
wheels=[o for o in scene.objects if o.name.startswith('WHEEL_')];assert len(wheels)==4
assert all(abs(o.location.z-.39)<1e-6 for o in wheels)
(ROOT/'source/body-v02-statistics.json').write_text(json.dumps(stats,indent=2))
scene.cycles.samples=8
for name,pos,scale in [('rear',(-8,0,1),5),('front-three-quarter',(7,6,3.6),6.15),('rear-three-quarter',(-7,6,3.6),6.15)]:
 scene.camera.location=pos;scene.camera.data.ortho_scale=scale;scene.camera.rotation_euler=(Vector((0,0,.92))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(ROOT/'renders'/('body-v02-'+name+'.png'));bpy.ops.render.render(write_still=True)

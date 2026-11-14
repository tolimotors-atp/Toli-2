import bpy,json,math
from pathlib import Path
from mathutils import Vector
O=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/renders/web-export-v04');O.mkdir(parents=True,exist_ok=True);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path('/home/thunder/shared/tolimotors-main1/toli-static-website/public/models/vehicles/isuzu-mux/isuzu-mux-web.glb')));objects=list(bpy.context.scene.objects);meshes=[o for o in objects if o.type=='MESH'];lo=[float('inf')]*3;hi=[-float('inf')]*3;verts=tris=0
for o in meshes:
 me=o.data;me.calc_loop_triangles();verts+=len(me.vertices);tris+=len(me.loop_triangles)
 for v in me.vertices:
  c=o.matrix_world@v.co
  for k in range(3):lo[k]=min(lo[k],c[k]);hi[k]=max(hi[k],c[k])
 assert all(math.isfinite(v) for n in me.vertices for v in n.normal)
assert len(meshes)==156 and abs(lo[2])<1e-5
assert all(bpy.data.objects.get('WHEEL_'+tag) for tag in ['FL','FR','RL','RR'])
assert all(bpy.data.objects.get(n) for n in ['V03_COHERENT_WINDSCREEN','V04_REAR_GLASS'])
result={'reimport':'PASS','vertices':verts,'triangles':tris,'materials':len({m.name for o in meshes for m in o.data.materials if m}),'objects':len(objects),'mesh_objects':len(meshes),'bounds_min':lo,'bounds_max':hi,'bytes':(Path('/home/thunder/shared/tolimotors-main1/toli-static-website/public/models/vehicles/isuzu-mux/isuzu-mux-web.glb')).stat().st_size,'normals_finite':True,'wheels':4,'glass_geometry':True,'textures':0};(O/'reimport.json').write_text(json.dumps(result,indent=2))
# Reuse the exact source camera/light setup for five clean-import comparison views.
s=bpy.context.scene
with bpy.data.libraries.load(str(Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/export/isuzu-mux-web-v04.blend')),link=False) as (available,loaded):loaded.objects=[n for n in available.objects if n.startswith('CAM_COMPARE_') or n.startswith('LIGHT') or 'softbox' in n.lower()]
for o in loaded.objects:
 if o and o.type in ['CAMERA','LIGHT']:s.collection.objects.link(o)
s.world=bpy.data.worlds.new('Neutral web audit');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.25,.25,.25,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.7
# Explicit neutral studio lights, outside exported asset.
for name,pos,power,size in [('key',(-3,-4,6),1500,5),('fill',(2,4,5),1200,4),('rim',(4,0,6),1500,4)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
s.render.engine='CYCLES';s.cycles.samples=12;s.render.resolution_x=720;s.render.resolution_y=480;s.render.resolution_percentage=100
for view in ['FRONT','FRONT_34','SIDE','REAR_34','REAR']:
 s.camera=bpy.data.objects['CAM_COMPARE_'+view];s.render.filepath=str(O/(view.lower()+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps(result),flush=True)

import os
os._exit(0)

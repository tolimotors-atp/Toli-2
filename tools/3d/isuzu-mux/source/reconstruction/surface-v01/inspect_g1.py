import bpy,json,math,os
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(os.environ.get('MUX_SURFACE_OUTPUT',Path(__file__).resolve().parents[3]));A=P/'source/reconstruction/surface-v01';R=P/'renders';bpy.ops.wm.open_mainfile(filepath=str(P/'source/reconstruction/isuzu-mux-greenhouse-surface-v01.blend'));s=bpy.context.scene;o=bpy.data.objects['G1 Windscreen — NEW 4x4 bicubic NURBS'];s['reference_priority']='PRIMARY O06; SECONDARY O07; VALIDATION O11; O10 contextual opposite-view cross-check only'
# Export real evaluated boundary projections for manual stance-anchored overlays, not camera calibration.
dg=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(dg);me=ev.to_mesh();edges={}
for face in me.polygons:
 for a,b in zip(face.vertices,list(face.vertices[1:])+[face.vertices[0]]):key=tuple(sorted((a,b)));edges[key]=edges.get(key,0)+1
out={}
for name in ['front','side','front-left','front-right']:
 cam=bpy.data.objects['G1 diagnostic '+name]
 def project(v):
  q=world_to_camera_view(s,cam,Vector(v));return[q.x*1100,(1-q.y)*750]
 out[name]=dict(boundary=[[project(o.matrix_world@me.vertices[a].co),project(o.matrix_world@me.vertices[b].co)] for (a,b),n in edges.items() if n==1],control_points=[project(o.matrix_world@Vector(p.co[:3])) for p in o.data.splines[0].points],front_wheel_left=project((-.5,-.286,0)),front_wheel_right=project((-.5,.286,0)),front_axle=project((-.5,0,0)),rear_axle=project((.5,0,0)))
ev.to_mesh_clear();(A/'projection-diagnostics.json').write_text(json.dumps(out,indent=2))
# Curvature-only G1 inspection. This is not G6: no roof/header/other surfaces exist.
for ob in bpy.data.objects:
 if ob!=o and ob.type in ['MESH','CURVE']:ob.hide_render=True
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True;s.world.use_nodes=True;s.world.node_tree.nodes.get('Background').inputs[0].default_value=(.12,.12,.12,1);s.world.node_tree.nodes.get('Background').inputs[1].default_value=.5
node=o.data.materials[0].node_tree.nodes.get('Principled BSDF');node.inputs['Metallic'].default_value=.7;node.inputs['Roughness'].default_value=.12
m=bpy.data.materials.new('G1 diagnostic white emitter');m.use_nodes=True;m.node_tree.nodes.clear();e=m.node_tree.nodes.new('ShaderNodeEmission');e.inputs[1].default_value=4;outnode=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],outnode.inputs[0])
for i in range(5):
 bpy.ops.mesh.primitive_plane_add(size=1,location=(-.7+i*.23,0,1.1));ob=bpy.context.object;ob.scale=(.09,1.3,1);ob.data.materials.append(m);ob.visible_camera=False
cam=bpy.data.objects['G1 diagnostic front-left'];cam.data.lens=110;cam.rotation_euler=(Vector((-.27,0,.51))-cam.location).to_track_quat('-Z','Y').to_euler();s.camera=cam;s.render.filepath=str(R/'g1-windscreen-curvature-surface-v01.png');bpy.ops.render.render(write_still=True)

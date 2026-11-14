import bpy,math,json,os
from pathlib import Path
from mathutils import Vector
ROOT=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux');OUT=Path(os.environ.get('MUX_SURFACE_OUTPUT',Path(__file__).resolve().parents[3]));A=OUT/'source/reconstruction/surface-v01';R=OUT/'renders';A.mkdir(parents=True,exist_ok=True);R.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'source/reconstruction/isuzu-mux-reference-constrained-v02.blend'));s=bpy.context.scene
def sig(o):return dict(name=o.name,matrix=[list(r) for r in o.matrix_world],vertices=[list(v.co) for v in o.data.vertices] if o.type=='MESH' else [])
keep=[o for o in bpy.data.objects if (o.type=='MESH' and any(m and m.name in ['Stance tire proxy','Stance wheel proxy'] for m in o.data.materials)) or o.name in ['Front axle','Rear axle','Centerline']];frozen=[sig(o) for o in keep]
for o in list(bpy.data.objects):
 if o not in keep:bpy.data.objects.remove(o,do_unlink=True)
bpy.data.orphans_purge(do_recursive=True)
# A new clamped bicubic NURBS surface. No V02 control points or polygon coordinates are read.
bpy.ops.surface.primitive_nurbs_surface_surface_add(location=(0,0,0));o=bpy.context.object;o.name='G1 Windscreen — NEW 4x4 bicubic NURBS';cu=o.data;cu.name='Editable 16-point windscreen surface';sp=cu.splines[0];assert sp.point_count_u==4 and sp.point_count_v==4
sp.order_u=4;sp.order_v=4;sp.use_endpoint_u=True;sp.use_endpoint_v=True;sp.use_cyclic_u=False;sp.use_cyclic_v=False;cu.resolution_u=12;cu.resolution_v=12;cu.render_resolution_u=12;cu.render_resolution_v=12
controls=[]
for j in range(4):
 v=j/3;w=(1-v)*.269+v*.230
 for i in range(4):
  t=-1+2*i/3;edge_x=(1-v)*(-.345)+v*(-.145);wrap=(1-v)*.060+v*.032
  x=edge_x-(4*wrap/3 if i in (1,2) else 0)-(.010 if j in (1,2) else 0)
  z=(1-v)*.438+v*.593+(.012 if i in (1,2) else 0)+(.002 if j in (1,2) else 0)
  p=(x,t*w,z,1);sp.points[j*4+i].co=p;controls.append(dict(row=j,column=i,co=p))
mat=bpy.data.materials.new('G1 neutral opaque diagnostic surface');mat.diffuse_color=(.22,.25,.27,1);mat.use_nodes=True;pn=mat.node_tree.nodes.get('Principled BSDF');pn.inputs['Base Color'].default_value=(.20,.22,.24,1);pn.inputs['Roughness'].default_value=.18;pn.inputs['Metallic'].default_value=.4;o.data.materials.append(mat)
s['METHOD']='LOW-CONTROL AUTOMOTIVE SURFACE PATCHES';s['STATUS']='G1 method-validation candidate only; no roof or pillar construction';s['reference_priority']='PRIMARY O06 windscreen; SECONDARY O07 side; VALIDATION O11 front 3Q; opposite O10 is contextual only, not another fitting target';o['control_definition']='Four rows: base, lower bow, upper bow, header; each has left/right edge and two transverse-bow handles';o['not_inherited']='No V02 greenhouse topology, mesh, shrinkwrap, deformation or copied control rows';o['units']='Wheelbase=1; reference-constrained estimates, not metres'
assert [sig(x) for x in keep]==frozen
s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.display.shading.show_shadows=True;s.display.shading.background_type='WORLD';s.world.color=(.8,.8,.8);s.render.resolution_x=1100;s.render.resolution_y=750;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
views={'front':((-3.2,0,.94),(-.1,0,.40),'PERSP',55),'side':((0,-4,.34),(0,0,.34),'ORTHO',1.9),'front-left':((-2.5,-3,1.02),(0,0,.36),'PERSP',62),'front-right':((-2.5,3,1.02),(0,0,.36),'PERSP',62)}
for name,(loc,tar,typ,scale) in views.items():
 bpy.ops.object.camera_add(location=loc);cam=bpy.context.object;cam.name='G1 diagnostic '+name;cam.rotation_euler=(Vector(tar)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type=typ
 if typ=='ORTHO':cam.data.ortho_scale=scale
 else:cam.data.lens=scale
 s.camera=cam;s.render.filepath=str(R/f'g1-windscreen-{name}-surface-v01.png');bpy.ops.render.render(write_still=True)
 # A close view of exactly the same patch, without changing its shape or stance.
 for ob in keep:ob.hide_render=True
 oldrot=cam.rotation_euler.copy();oldlens=cam.data.lens;oldscale=cam.data.ortho_scale;cam.rotation_euler=(Vector((-.275,0,.51))-cam.location).to_track_quat('-Z','Y').to_euler()
 if typ=='ORTHO':cam.data.ortho_scale=.7
 else:cam.data.lens=100
 s.render.filepath=str(R/f'g1-windscreen-close-{name}-surface-v01.png');bpy.ops.render.render(write_still=True);cam.rotation_euler=oldrot;cam.data.lens=oldlens;cam.data.ortho_scale=oldscale
 for ob in keep:ob.hide_render=False
s.camera=bpy.data.objects['G1 diagnostic front-left'];dg=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();stats=dict(control_points=16,control_grid='4x4',surface_type=o.type,nurbs_order_u=sp.order_u,nurbs_order_v=sp.order_v,evaluated_vertices=len(me.vertices),evaluated_triangles=len(me.loop_triangles),no_greenhouse_mesh_inherited=True,only_new_surface='windscreen',stance_unchanged=True,stance_signature=frozen,controls=controls);ev.to_mesh_clear();(A/'geometry-checks.json').write_text(json.dumps(stats,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source/reconstruction/isuzu-mux-greenhouse-surface-v01.blend'))
# Saved source must remain an editable surface, not the evaluated render mesh.
bpy.ops.wm.open_mainfile(filepath=str(OUT/'source/reconstruction/isuzu-mux-greenhouse-surface-v01.blend'));new=bpy.data.objects['G1 Windscreen — NEW 4x4 bicubic NURBS'];assert new.type=='SURFACE' and len(new.data.splines[0].points)==16
for item in frozen:
 ob=bpy.data.objects[item['name']];assert sig(ob)==item
(A/'reopen-validation.json').write_text(json.dumps(dict(passed=True,editable_surface=True,control_points=16,stance_preserved=True),indent=2))

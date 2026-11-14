import sys,bpy,json,hashlib,os
from pathlib import Path
from mathutils import Vector
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');sys.path.insert(0,str(P/'tools/blender-addons'))
from toli_mux_generator.geometry.curves import generate_curves,COLLECTION
from toli_mux_generator.parameters import BASE
from toli_mux_generator.operators import cameras
bpy.ops.wm.read_factory_settings(use_empty=True);p=dict(BASE,quality='PREVIEW')
def sig():
 return hashlib.sha256(json.dumps([(o.name,[list(bp.co) for bp in o.data.splines[0].bezier_points]) for o in sorted(bpy.data.collections[COLLECTION].objects,key=lambda x:x.name)]).encode()).hexdigest()
generate_curves(bpy.context.scene,p);a=sig();generate_curves(bpy.context.scene,p);assert a==sig();col=bpy.data.collections[COLLECTION]
assert len(col.objects)<100 and all('.00' not in o.name for o in col.objects),'Duplicate construction curves'
coords=[tuple(bp.co) for o in col.objects for bp in o.data.splines[0].bezier_points];error=max(min(sum((a-b)**2 for a,b in zip((x,-y,z),v)) for v in coords)**.5 for x,y,z in coords)
assert error<.0001
s=bpy.context.scene;cameras(s);s.world=bpy.data.worlds.new('Curve review');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.035,.035,.035,1)
for pos in [(-4,-5,6),(4,4,5)]:
 d=bpy.data.lights.new('Review area','AREA');d.energy=1800;d.size=5;o=bpy.data.objects.new('Review area',d);s.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
r=P/'tools/3d/isuzu-mux/code-generator/renders/curve-validation';r.mkdir(parents=True,exist_ok=True);stats={'curves':len(col.objects),'control_points':len(coords),'symmetry_error_m':error,'curve_regeneration':'PASS','surfaces':'NOT GENERATED — curve gate first','preview_mesh_vertices':0,'preview_mesh_triangles':0};(r/'validation.json').write_text(json.dumps(stats,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-curve-generated-v01.blend'));s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=720;s.render.resolution_y=480;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA'
for view in ['FRONT','FRONT34','SIDE','REAR34','REAR']:
 s.camera=bpy.data.objects['CAM_'+view];s.render.filepath=str(r/(view.lower()+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps(stats),flush=True);os._exit(0)

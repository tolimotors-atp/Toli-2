import bpy,sys,json,os,hashlib
from pathlib import Path
from mathutils import Vector
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');sys.path.insert(0,str(P/'tools/blender-addons'));from toli_mux_generator.geometry.reference_cage import generate_cage,COL
from toli_mux_generator.parameters import BASE
from toli_mux_generator.operators import cameras
from toli_mux_generator.curve_ui import references
import toli_mux_generator as addon
bpy.ops.wm.read_factory_settings(use_empty=True);addon.register();s=bpy.context.scene;p=dict(BASE,quality='PREVIEW')
def sig():return hashlib.sha256(json.dumps([(o.name,[[list(b.co),list(b.handle_left),list(b.handle_right)] for b in o.data.splines[0].bezier_points]) for o in sorted(bpy.data.collections[COL].objects,key=lambda x:x.name)]).encode()).hexdigest()
generate_cage(s,p);before=sig();generate_cage(s,p);assert before==sig();coords=[b.co.copy() for o in bpy.data.collections[COL].objects for b in o.data.splines[0].bezier_points];error=max(min((Vector((v.x,-v.y,v.z))-w).length for w in coords) for v in coords);assert error<1e-7
support=bpy.data.collections.new('TOLI_CAGE_SUPPORT');s.collection.children.link(support)
for x in [-p['wheelbase']/2,p['wheelbase']/2]:
 for y in [-p['track']/2,p['track']/2]:
  bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=p['tire_diameter']/2,depth=.23,location=(x,y,p['tire_diameter']/2),rotation=(1.57079632679,0,0));o=bpy.context.object;o.name='CAGE_WHEEL'
  for c in list(o.users_collection):c.objects.unlink(o)
  support.objects.link(o)
from toli_mux_generator.geometry.reference_cage import make
make(bpy.data.collections[COL],'GUIDE_CENTERLINE',[Vector((-2.6,0,0)),Vector((2.6,0,0))],'section')
for x in [-p['wheelbase']/2,p['wheelbase']/2]:make(bpy.data.collections[COL],'GUIDE_AXLE',[Vector((x,-1.1,.382)),Vector((x,1.1,.382))],'section')
bpy.ops.mesh.primitive_plane_add(size=12);ground=bpy.context.object;ground.name='CAGE_GROUND';ground.hide_render=True
for key in ['front','side','rear','threequarter']:setattr(s.toli_mux,'reference_'+key,True)
cameras(s);s.world=bpy.data.worlds.new('Cage background');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.04,.04,.04,1);d=bpy.data.lights.new('Cage studio','AREA');d.energy=1500;d.size=5;o=bpy.data.objects.new('Cage studio',d);s.collection.objects.link(o);o.location=(-4,-4,6);o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v01';r.mkdir(parents=True,exist_ok=True);(r/'cage-validation.json').write_text(json.dumps({'traced_curves':len(bpy.data.collections[COL].objects)-3,'control_points':len(coords),'symmetry_error_m':error,'regeneration':'PASS','surfaces':'NOT GENERATED: curve gate first'},indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v01.blend'));s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=720;s.render.resolution_y=480;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA'
for view in ['FRONT','FRONT34','SIDE','REAR34','REAR']:
 s.camera=bpy.data.objects['CAM_'+view];s.render.filepath=str(r/(view.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('CAGE SAVED AND RENDERED',flush=True);os._exit(0)

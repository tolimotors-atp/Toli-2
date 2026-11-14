import bpy,sys,json,os,hashlib
from pathlib import Path
from mathutils import Vector
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');sys.path.insert(0,str(P/'tools/blender-addons'));from toli_mux_generator.geometry.rounded import generate_rounded,ROUNDED
from toli_mux_generator.parameters import BASE
from toli_mux_generator.operators import cameras
from toli_mux_generator import validation
bpy.ops.wm.read_factory_settings(use_empty=True);p=dict(BASE,quality='PREVIEW');validation.COLLECTION=ROUNDED

def signature():
 rows=[]
 for o in sorted(bpy.data.collections[ROUNDED].objects,key=lambda x:x.name):
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();rows.append((o.name,[list(v.co) for v in m.vertices]));ev.to_mesh_clear()
 return hashlib.sha256(json.dumps(rows).encode()).hexdigest()
generate_rounded(bpy.context.scene,p);a=signature();generate_rounded(bpy.context.scene,p);assert a==signature();preview=validation.validate(bpy.context.scene,p);p['quality']='QUALITY';generate_rounded(bpy.context.scene,p);quality=validation.validate(bpy.context.scene,p);p['quality']='PREVIEW';generate_rounded(bpy.context.scene,p)
s=bpy.context.scene;cameras(s);s.world=bpy.data.worlds.new('Clay review');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.22,.22,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.65
for name,pos in [('key',(-4,-5,6)),('fill',(4,4,6))]:
 d=bpy.data.lights.new(name,'AREA');d.energy=1400;d.size=5;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
r=P/'tools/3d/isuzu-mux/code-generator/renders/curve-rounded-v01';r.mkdir(parents=True,exist_ok=True);result={'preview':preview,'quality':quality,'regeneration':'PASS'};(r/'validation.json').write_text(json.dumps(result,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-curve-rounded-v01.blend'))
s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=720;s.render.resolution_y=480;s.render.resolution_percentage=100
for view in ['FRONT','FRONT34','SIDE','REAR34','REAR']:
 s.camera=bpy.data.objects['CAM_'+view];s.render.filepath=str(r/('clay-'+view.lower()+'.png'));bpy.ops.render.render(write_still=True)
s.world.node_tree.nodes['Background'].inputs[1].default_value=.08
for o in s.objects:
 if o.type=='LIGHT':o.data.shape='RECTANGLE';o.data.size=7;o.data.size_y=.22;o.data.energy=2300
for view in ['FRONT34','SIDE','REAR34']:
 s.camera=bpy.data.objects['CAM_'+view];s.render.filepath=str(r/('strips-'+view.lower()+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps(result),flush=True);os._exit(0)

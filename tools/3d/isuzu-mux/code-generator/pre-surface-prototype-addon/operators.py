import bpy,json
from pathlib import Path
from mathutils import Vector
from .parameters import BASE,values
from .geometry import generate
from .validation import validate
ROOT=Path(__file__).resolve().parents[3]
OUTPUT=ROOT/'tools/3d/isuzu-mux/code-generator/renders/v02'
VIEWS={'FRONT':(-9,0,1.2),'FRONT34':(-7,-7,3),'SIDE':(0,-9,1.2),'REAR34':(7,-7,3),'REAR':(9,0,1.2)}
def cameras(scene):
 col=bpy.data.collections.get('TOLI_MUX_REFERENCES')
 if not col:col=bpy.data.collections.new('TOLI_MUX_REFERENCES');scene.collection.children.link(col)
 for name,pos in VIEWS.items():
  key='CAM_'+name;o=bpy.data.objects.get(key)
  if not o:o=bpy.data.objects.new(key,bpy.data.cameras.new(key));col.objects.link(o)
  o.location=pos;o.rotation_euler=(Vector((0,0,.93))-o.location).to_track_quat('-Z','Y').to_euler();o.data.type='ORTHO';o.data.ortho_scale=6.1
class Generate(bpy.types.Operator):
 bl_idname='toli_mux.generate';bl_label='Generate MU-X';bl_options={'REGISTER','UNDO'}
 def execute(self,context):generate(context.scene,values(context.scene));cameras(context.scene);return {'FINISHED'}
class Regenerate(bpy.types.Operator):
 bl_idname='toli_mux.regenerate';bl_label='Regenerate MU-X';bl_options={'REGISTER','UNDO'}
 def execute(self,context):generate(context.scene,values(context.scene));cameras(context.scene);return {'FINISHED'}
class Reset(bpy.types.Operator):
 bl_idname='toli_mux.reset';bl_label='Reset to Reference Baseline';bl_options={'REGISTER','UNDO'}
 def execute(self,context):
  for k,v in BASE.items():setattr(context.scene.toli_mux,k,v)
  context.scene.toli_mux.quality='PREVIEW'
  return {'FINISHED'}
class Validate(bpy.types.Operator):
 bl_idname='toli_mux.validate';bl_label='Validate Geometry'
 def execute(self,context):
  OUTPUT.mkdir(parents=True,exist_ok=True);result=validate(context.scene,values(context.scene));(OUTPUT/'validation.json').write_text(json.dumps(result,indent=2));self.report({'INFO'},'Validation saved; visual gate still required');return {'FINISHED'}
class Render(bpy.types.Operator):
 bl_idname='toli_mux.render';bl_label='Render Validation Views'
 def execute(self,context):
  OUTPUT.mkdir(parents=True,exist_ok=True);s=context.scene;cameras(s);s.render.engine='CYCLES';s.cycles.samples=12;s.render.resolution_x=720;s.render.resolution_y=480;s.render.resolution_percentage=100
  for name in VIEWS:s.camera=bpy.data.objects['CAM_'+name];s.render.filepath=str(OUTPUT/(name.lower()+'.png'));bpy.ops.render.render(write_still=True)
  return {'FINISHED'}
class Export(bpy.types.Operator):
 bl_idname='toli_mux.export';bl_label='Export (quality gate pending)'
 def execute(self,context):self.report({'WARNING'},'Milestone 1 has no exterior approval; export is blocked');return {'CANCELLED'}
CLASSES=(Generate,Regenerate,Reset,Validate,Render,Export)

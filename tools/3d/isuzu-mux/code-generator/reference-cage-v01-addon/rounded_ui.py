import bpy
from .geometry.soft_body import generate_soft as generate_rounded
from .parameters import values
class GenerateRounded(bpy.types.Operator):
 bl_idname='toli_mux.rounded';bl_label='Generate MU-X — Soft Body — Clay Gate';bl_options={'REGISTER','UNDO'}
 def execute(self,context):
  generate_rounded(context.scene,values(context.scene));old=bpy.data.collections.get('TOLI_MUX_GENERATED')
  if old:old.hide_viewport=True;old.hide_render=True
  self.report({'INFO'},'Rounded candidate only — no visual approval or export');return {'FINISHED'}
class RenderRounded(bpy.types.Operator):
 bl_idname='toli_mux.render_rounded';bl_label='Render Rounded Validation Views'
 def execute(self,context):
  from . import operators
  previous=operators.OUTPUT;operators.OUTPUT=operators.ROOT/'tools/3d/isuzu-mux/code-generator/renders/deep-detail-v01'
  try:return bpy.ops.toli_mux.render()
  finally:operators.OUTPUT=previous

import bpy
from pathlib import Path
from .geometry.curves import generate_curves,COLLECTION
from .parameters import values

def visibility(self,context):
 col=bpy.data.collections.get(COLLECTION)
 if col:col.hide_viewport=not self.show_construction_curves

def references(self,context):
 folder=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');col=bpy.data.collections.get('TOLI_MUX_REFERENCES')
 if not col:col=bpy.data.collections.new('TOLI_MUX_REFERENCES');context.scene.collection.children.link(col)
 for key,time,pos in [('front','18-17-10',(-4,0,1)),('side','18-17-14',(0,3,1)),('rear','18-17-18',(4,0,1)),('threequarter','18-17-27',(0,5,1))]:
  name='REF_IMAGE_'+key;o=bpy.data.objects.get(name);show=getattr(self,'reference_'+key)
  if show and not o:
   path=folder/f'Screenshot From 2026-11-06 {time}.png'
   if not path.exists():continue
   o=bpy.data.objects.new(name,None);col.objects.link(o);o.empty_display_type='IMAGE';o.data=bpy.data.images.load(str(path),check_existing=True);o.empty_display_size=5;o.location=pos;o.rotation_euler=(1.570796,0,0);o.hide_render=True
  if o:o.hide_set(not show)
class GenerateCurves(bpy.types.Operator):
 bl_idname='toli_mux.curve_network';bl_label='Generate / Regenerate Construction Curves';bl_options={'REGISTER','UNDO'}
 def execute(self,context):
  generate_curves(context.scene,values(context.scene));legacy=bpy.data.collections.get('TOLI_MUX_GENERATED')
  if legacy:legacy.hide_viewport=True;legacy.hide_render=True
  visibility(context.scene.toli_mux,context);self.report({'INFO'},'Curve gate only: surfaces and export remain blocked');return {'FINISHED'}

class RenderCurves(bpy.types.Operator):
 bl_idname='toli_mux.render_curves';bl_label='Render Curve Validation Views'
 def execute(self,context):
  from . import operators
  previous=operators.OUTPUT;operators.OUTPUT=operators.ROOT/'tools/3d/isuzu-mux/code-generator/renders/curve-validation'
  try:return bpy.ops.toli_mux.render()
  finally:operators.OUTPUT=previous

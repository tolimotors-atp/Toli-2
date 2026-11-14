"""Run this text once in Blender, then Camera View > N > MU-X Overlay."""
import bpy
class MUX_OT_overlay(bpy.types.Operator):
 bl_idname='mux.reference_overlay';bl_label='Reference overlay';mode:bpy.props.StringProperty()
 def execute(self,context):
  mode=self.mode;s=context.scene
  for name in ['MUX_PRIMARY_SURFACES','MUX_WHEELS']:
   for o in bpy.data.collections[name].objects:o.hide_set(mode=='REFERENCE')
  for bg in s.camera.data.background_images:
   bg.alpha=0 if mode=='MODEL' else 1 if mode=='REFERENCE' else .5;bg.display_depth='FRONT' if mode=='HALF' else 'BACK'
  for area in (context.screen.areas if context.screen else []):
   if area.type=='VIEW_3D':
    sh=area.spaces.active.shading;sh.type='WIREFRAME' if mode=='WIRE' else 'SOLID';sh.light='FLAT' if mode=='SILHOUETTE' else 'STUDIO';sh.color_type='SINGLE' if mode=='SILHOUETTE' else 'MATERIAL';sh.single_color=(.9,.23,.1);area.spaces.active.region_3d.view_perspective='CAMERA'
  return {'FINISHED'}
class MUX_PT_overlay(bpy.types.Panel):
 bl_label='MU-X reference overlay';bl_idname='MUX_PT_overlay';bl_space_type='VIEW_3D';bl_region_type='UI';bl_category='MU-X Overlay'
 def draw(self,context):
  layout=self.layout;layout.label(text='REFERENCE-FIT — NOT CALIBRATED');layout.prop(context.scene,'camera')
  for mode,label in [('REFERENCE','Reference only'),('MODEL','Model only'),('HALF','50% reference/model'),('SILHOUETTE','Silhouette overlay'),('WIRE','Wire overlay')]:layout.operator('mux.reference_overlay',text=label).mode=mode
for cls in [MUX_OT_overlay,MUX_PT_overlay]:
 old=getattr(bpy.types,cls.__name__,None)
 if old:bpy.utils.unregister_class(old)
 bpy.utils.register_class(cls)

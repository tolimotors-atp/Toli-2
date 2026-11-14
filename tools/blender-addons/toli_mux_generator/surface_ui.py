import bpy
from .geometry.surface_patch import build,SURFACES,CONTROL
from .geometry.reference_cage import COL
from .parameters import values
AUTH={
 'A':['TRACE_SIDE_MASTER','TRACE_BONNET_FRONT','TRACE_FRONT_ARCH','TRACE_BONNET_EDGE','TRACE_A_PILLAR','TRACE_WINDSCREEN_BOTTOM'],
 'B':['TRACE_SIDE_MASTER','TRACE_ROOF_EDGE','TRACE_ROOF_CENTER','TRACE_QUARTER_GLASS','TRACE_REAR_GLASS','TRACE_D_PILLAR'],
 'C':['TRACE_SIDE_MASTER','TRACE_REAR_ARCH','TRACE_TAIL_LAMP','TRACE_SHOULDER','TRACE_REAR_BUMPER']}

def update(self,context):
 if SURFACES not in bpy.data.collections:return
 cage_only=self.curve_cage_only;chosen=self.surface_zone
 for n in [SURFACES,CONTROL]:bpy.data.collections[n].hide_viewport=cage_only;bpy.data.collections[n].hide_render=cage_only
 for o in bpy.data.collections[SURFACES].objects:o.hide_viewport=o.hide_render=chosen!='ALL' and o['zone']!=chosen
 for o in bpy.data.collections[CONTROL].objects:o.hide_viewport=o.hide_render=not self.surface_control_sections or (chosen!='ALL' and o['zone']!=chosen)
 col=bpy.data.collections[COL];col.hide_viewport=False;col.hide_render=False
 allowed=set(sum(AUTH.values(),[])) if chosen=='ALL' else set(AUTH[chosen])
 for o in col.objects:
  if cage_only:visible=not o.get('station_slice')
  else:visible=self.surface_constraints and (o.name.removesuffix('_R') in allowed or o.name.startswith('GUIDE_'))
  o.hide_viewport=o.hide_render=not visible
 if 'TOLI_CAGE_SUPPORT' in bpy.data.collections:
  for o in bpy.data.collections['TOLI_CAGE_SUPPORT'].objects:
   if o.name.startswith('CAGE_WHEEL'):
    visible=cage_only or chosen=='ALL' or (o.location.x<0)==(chosen=='A');o.hide_viewport=o.hide_render=not visible

class GeneratePrototype(bpy.types.Operator):
 bl_idname='toli_mux.surface_prototype';bl_label='Regenerate Current Surface Prototype';bl_options={'REGISTER','UNDO'}
 def execute(self,context):
  try:build(context.scene,values(context.scene),version=context.scene.get('surface_prototype_version',1))
  except (ValueError,AssertionError) as e:self.report({'ERROR'},str(e));return {'CANCELLED'}
  context.scene.toli_mux.curve_cage_only=False;update(context.scene.toli_mux,context);return {'FINISHED'}

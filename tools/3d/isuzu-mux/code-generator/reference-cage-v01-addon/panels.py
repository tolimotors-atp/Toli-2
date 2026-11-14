import bpy
class Panel(bpy.types.Panel):
 bl_label='TOLI MU-X';bl_idname='TOLI_PT_MUX';bl_space_type='VIEW_3D';bl_region_type='UI';bl_category='TOLI MU-X'
 def draw(self,context):
  l=self.layout;p=context.scene.toli_mux;l.label(text='Reference-traced cage — surfaces gated');l.operator('toli_mux.reference_cage');l.prop(p,'curve_cage_only');l.operator('toli_mux.render_cage');l.operator('toli_mux.curve_network');l.prop(p,'show_construction_curves');l.prop(p,'quality')
  for title,keys in [('Dimensions',['length','width','height','wheelbase','tire_diameter']),('Curve controls',['bonnet_height','roof_crown','belt_height','fender_bulge','windscreen_run','rear_taper']),('References',['reference_front','reference_side','reference_rear','reference_threequarter'])]:
   box=l.box();box.label(text=title)
   for key in keys:box.prop(p,key)
  l.operator('toli_mux.reset');l.operator('toli_mux.render_curves');l.operator('toli_mux.export')

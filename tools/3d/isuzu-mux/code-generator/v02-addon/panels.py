import bpy
class Panel(bpy.types.Panel):
 bl_label='TOLI MU-X';bl_idname='TOLI_PT_MUX';bl_space_type='VIEW_3D';bl_region_type='UI';bl_category='TOLI MU-X'
 def draw(self,context):
  l=self.layout;p=context.scene.toli_mux;l.label(text='V02 — visual gate unapproved');l.prop(p,'quality')
  for title,keys in [('Dimensions',['length','width','height','wheelbase','track','ground_clearance']),('Greenhouse',['greenhouse_width']),('Wheels',['tire_diameter'])]:
   box=l.box();box.label(text=title)
   for key in keys:box.prop(p,key)
  l.label(text='Body/arch profiles: mux_shape_data.py');l.operator('toli_mux.generate');l.operator('toli_mux.regenerate');l.operator('toli_mux.reset');l.operator('toli_mux.validate');l.operator('toli_mux.render');l.operator('toli_mux.export')

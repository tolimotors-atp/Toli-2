import bpy,json
from .geometry.reference_cage import COL,make
from .geometry.converged_cage import generate_cage
from .parameters import values
from mathutils import Vector

def support(scene,p):
 name='TOLI_CAGE_SUPPORT';old=bpy.data.collections.get(name)
 if old:
  for o in list(old.objects):
   data=o.data;bpy.data.objects.remove(o,do_unlink=True)
   if data.users==0:bpy.data.meshes.remove(data)
  bpy.data.collections.remove(old)
 col=bpy.data.collections.new(name);scene.collection.children.link(col)
 for x in [-p['wheelbase']/2,p['wheelbase']/2]:
  for y in [-p['track']/2,p['track']/2]:
   bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=p['tire_diameter']/2,depth=.23,location=(x,y,p['tire_diameter']/2),rotation=(1.57079632679,0,0));o=bpy.context.object;o.name='CAGE_WHEEL'
   for c in list(o.users_collection):c.objects.unlink(o)
   col.objects.link(o)
 make(bpy.data.collections[COL],'GUIDE_CENTERLINE',[Vector((-2.6,0,0)),Vector((2.6,0,0))],'section')
 for i,x in enumerate([-p['wheelbase']/2,p['wheelbase']/2]):make(bpy.data.collections[COL],'GUIDE_AXLE_'+str(i),[Vector((x,-1.1,.382)),Vector((x,1.1,.382))],'section')
 bpy.ops.mesh.primitive_plane_add(size=12);o=bpy.context.object;o.name='CAGE_GROUND';o.hide_render=True
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o)

def cage_only(self,context):
 names=['TOLI_MUX_GENERATED','TOLI_MUX_CURVE_ROUNDED','TOLI_MUX_CONSTRUCTION']
 if self.curve_cage_only:
  if 'cage_hidden_states' not in context.scene:context.scene['cage_hidden_states']=json.dumps({n:[bpy.data.collections[n].hide_viewport,bpy.data.collections[n].hide_render] for n in names if n in bpy.data.collections})
  for n in names:
   if n in bpy.data.collections:bpy.data.collections[n].hide_viewport=True;bpy.data.collections[n].hide_render=True
  for key in ['front','side','rear','threequarter']:setattr(self,'reference_'+key,True)
 else:
  for name,state in json.loads(context.scene.get('cage_hidden_states','{}')).items():
   if name in bpy.data.collections:bpy.data.collections[name].hide_viewport,bpy.data.collections[name].hide_render=state
  if 'cage_hidden_states' in context.scene:del context.scene['cage_hidden_states']
 for n in [COL,'TOLI_CAGE_SUPPORT','TOLI_CAGE_COMBS']:
  if n in bpy.data.collections:bpy.data.collections[n].hide_viewport=not self.curve_cage_only
class GenerateCage(bpy.types.Operator):
 bl_idname='toli_mux.reference_cage';bl_label='Generate Reference-Traced Cage V04';bl_options={'REGISTER','UNDO'}
 def execute(self,context):
  p=values(context.scene);generate_cage(context.scene,p);support(context.scene,p);context.scene.toli_mux.curve_cage_only=True;cage_only(context.scene.toli_mux,context);section_visibility(context.scene.toli_mux,context);from .join_debug import join_visibility;join_visibility(context.scene.toli_mux,context);return {'FINISHED'}
class RenderCage(bpy.types.Operator):
 bl_idname='toli_mux.render_cage';bl_label='Render Cage Validation'
 def execute(self,context):
  from . import operators
  prev=operators.OUTPUT;operators.OUTPUT=operators.ROOT/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04'
  try:return bpy.ops.toli_mux.render()
  finally:operators.OUTPUT=prev


def section_visibility(self,context):
 col=bpy.data.collections.get(COL)
 if col:
  for o in col.objects:
   if o.get('station_slice'):
    visible=self.show_depth_slices and (self.depth_station=='ALL' or o.name=='SLICE_'+self.depth_station)
    o.hide_viewport=not visible;o.hide_render=not visible

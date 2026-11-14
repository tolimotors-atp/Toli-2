import bpy
from bpy.props import FloatProperty,EnumProperty,BoolProperty
# Family-scale guidance supplied in brief, not newly verified official dimensions.
BASE={'length':4.825,'width':1.860,'height':1.860,'wheelbase':2.845,'track':1.570,'tire_diameter':.764,'ground_clearance':.23,'bonnet_length':1.20,'bonnet_height':1.13,'roof_crown':.055,'greenhouse_width':1.49,'belt_height':1.19,'rear_taper':.08,'fender_bulge':.025,'arch_clearance':.07,'windscreen_run':.50}
class MUXParameters(bpy.types.PropertyGroup):
 quality:EnumProperty(name='Mode',items=[('PREVIEW','Preview','Low-density iteration'),('QUALITY','Quality','Higher wheel sampling and bevel segments')],default='PREVIEW')
for key,value in BASE.items():
 MUXParameters.__annotations__[key]=FloatProperty(name=key.replace('_',' ').title(),default=value,min=value*.65,max=value*1.35,precision=3)
def values(scene):return {k:getattr(scene.toli_mux,k) for k in BASE}|{'quality':scene.toli_mux.quality}

# Lazy callbacks avoid importing Blender UI operators while defining parameters.
def construction_visibility(self,context):
 from .curve_ui import visibility
 visibility(self,context)
def reference_visibility(self,context):
 from .curve_ui import references
 references(self,context)
MUXParameters.__annotations__['show_construction_curves']=BoolProperty(name='Show Construction Curves',default=True,update=construction_visibility)
for key in ['front','side','rear','threequarter']:
 MUXParameters.__annotations__['reference_'+key]=BoolProperty(name=key.title()+' reference',default=False,update=reference_visibility)

def cage_visibility(self,context):
 from .cage_ui import cage_only
 cage_only(self,context)
MUXParameters.__annotations__['curve_cage_only']=BoolProperty(name='Curve Cage Only',default=False,update=cage_visibility)


def depth_visibility(self,context):
 from .cage_ui import section_visibility
 section_visibility(self,context)
MUXParameters.__annotations__['show_depth_slices']=BoolProperty(name='Show Width Stations',default=False,update=depth_visibility)
MUXParameters.__annotations__['depth_station']=EnumProperty(name='Width Station',items=[(n,n.replace('_',' ').title(),'Inferred transverse depth section') for n in ['ALL','front_bumper','front_wheel','cowl','B_pillar','C_pillar','rear_wheel','tail_lamp','rear_bumper']],default='ALL',update=depth_visibility)


def join_visibility(self,context):
 from .join_debug import join_visibility as update
 update(self,context)
MUXParameters.__annotations__['join_debug']=EnumProperty(name='Join Debug',items=[('OFF','Off','Full cage')]+[(n,n,'Isolate join, neighbours, station and relevant wheels') for n in ['J01','J02','J03','J04','J05','J06','J07','J08']],default='OFF',update=join_visibility)
MUXParameters.__annotations__['show_curvature_combs']=BoolProperty(name='Curvature Combs',default=False,update=join_visibility)

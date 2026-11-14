bl_info={'name':'TOLI MU-X Generator','author':'TOLI project','version':(0,1,0),'blender':(4,2,0),'location':'View3D > Sidebar > TOLI MU-X','category':'Add Mesh'}
import bpy
from .parameters import MUXParameters
from .operators import CLASSES
from .panels import Panel
from .curve_ui import GenerateCurves,RenderCurves
classes=(MUXParameters,*CLASSES,GenerateCurves,RenderCurves,Panel)
def register():
 for cls in classes:bpy.utils.register_class(cls)
 bpy.types.Scene.toli_mux=bpy.props.PointerProperty(type=MUXParameters)
def unregister():
 del bpy.types.Scene.toli_mux
 for cls in reversed(classes):bpy.utils.unregister_class(cls)

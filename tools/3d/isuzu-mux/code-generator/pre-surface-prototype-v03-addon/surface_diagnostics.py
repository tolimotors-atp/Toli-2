import bpy,math
from mathutils import Vector
from .geometry.surface_patch import SURFACES,CONTROL,clay

def setup(scene):
 for o in list(bpy.data.objects):
  if o.type=='LIGHT' or o.name.startswith('PROTO_'):bpy.data.objects.remove(o,do_unlink=True)
 world=bpy.data.worlds.new('Prototype neutral studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.08,.08,.08,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35;scene.world=world
 def light(n,loc,power,size,other=None):
  d=bpy.data.lights.new(n,'AREA');d.energy=power;d.shape='RECTANGLE';d.size=size;d.size_y=other or size;o=bpy.data.objects.new(n,d);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler();return o
 light('PROTO_Key',(-3,-4,6),900,3);light('PROTO_Fill',(4,3,5),400,4);light('PROTO_Rim',(3,-1,5),600,3)
 for i,y in enumerate([-2,-1,0,1,2]):light('PROTO_STRIP_TOP_'+str(i),(0,y,4),350,.10,6)
 for i,x in enumerate([-2,0,2]):light('PROTO_STRIP_SIDE_'+str(i),(x,-4,2),250,.10,4)
 bpy.ops.mesh.primitive_plane_add(size=14,location=(0,0,-.018));floor=bpy.context.object;floor.name='PROTO_Floor';floor.data.materials.append(clay('Prototype studio floor',.16,.80))
 for o in bpy.data.objects:
  if o.name.startswith('CAGE_WHEEL'):o.data.materials.clear();o.data.materials.append(clay('Prototype wheel anchors',.11,.7))
 camdata=bpy.data.cameras.new('PROTO_Camera');cam=bpy.data.objects.new('PROTO_Camera',camdata);scene.collection.objects.link(cam);camdata.type='ORTHO';scene.camera=cam
 scene.render.engine='CYCLES';scene.cycles.samples=12;scene.render.resolution_x=1000;scene.render.resolution_y=700;scene.render.resolution_percentage=100;scene.render.film_transparent=False;scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX';scene.render.image_settings.color_mode='RGB'
 return cam

def camera_for(scene,zone,view,close=False):
 cam=bpy.data.objects['PROTO_Camera'];base=bpy.data.objects['CAM_'+view];cam.rotation_euler=base.rotation_euler
 obs=[o for o in bpy.data.collections[SURFACES].objects if zone=='ALL' or o['zone']==zone];co=[o.matrix_world@Vector(v) for o in obs for v in o.bound_box]
 if zone in ['A','C'] and not close:
  co += [o.matrix_world@Vector(v) for o in bpy.data.objects if o.name.startswith('CAGE_WHEEL') and ((o.location.x<0)==(zone=='A')) for v in o.bound_box]
 lo=Vector(tuple(min(v[i] for v in co) for i in range(3)));hi=Vector(tuple(max(v[i] for v in co) for i in range(3)));center=(lo+hi)/2
 if close:center=Vector({'A':(-1.38,-.56,1.03),'B':(1.98,-.67,1.54),'C':(2.12,-.75,.91)}[zone])
 cam.location=center+(base.location-Vector((0,0,.93)));rot=cam.rotation_euler.to_matrix();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));aspect=scene.render.resolution_x/scene.render.resolution_y
 if close:cam.data.ortho_scale={'A':2.05,'B':1.35,'C':1.65}[zone]
 else:cam.data.ortho_scale=max(max(v.dot(right) for v in co)-min(v.dot(right) for v in co),(max(v.dot(up) for v in co)-min(v.dot(up) for v in co))*aspect)*1.16
 scene.camera=cam;bpy.context.view_layer.update();return cam

def zebra():
 m=bpy.data.materials.get('Prototype synthetic reflection zebra') or bpy.data.materials.new('Prototype synthetic reflection zebra');m.use_nodes=True;n=m.node_tree.nodes;n.clear();links=m.node_tree.links
 tex=n.new('ShaderNodeTexCoord');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(1,.15,.28);mult=n.new('ShaderNodeMath');mult.operation='MULTIPLY';mult.inputs[1].default_value=32;sin=n.new('ShaderNodeMath');sin.operation='SINE';cut=n.new('ShaderNodeMath');cut.operation='GREATER_THAN';cut.inputs[1].default_value=0;mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.015,.015,.015,1);mix.inputs[2].default_value=(.85,.85,.85,1);em=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial')
 for a,b in [(tex.outputs['Reflection'],dot.inputs[0]),(dot.outputs['Value'],mult.inputs[0]),(mult.outputs[0],sin.inputs[0]),(sin.outputs[0],cut.inputs[0]),(cut.outputs[0],mix.inputs[0]),(mix.outputs[0],em.inputs['Color']),(em.outputs[0],out.inputs['Surface'])]:links.new(a,b)
 return m

import bpy,math,json
from pathlib import Path
from mathutils import Vector
O=Path(__file__).resolve().parents[3];D=O/'source/reconstruction';R=O/'renders';bpy.ops.wm.read_factory_settings(use_empty=True)
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);return m
grey=mat('Neutral diagnostic body',(.48,.48,.48));glass=mat('Opaque diagnostic glass',(.08,.11,.12));rubber=mat('Stance tire proxy',(.075,.075,.075));rim=mat('Stance wheel proxy',(.3,.3,.3))
def mesh(n,v,f,m):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);o.data.materials.append(m);return o
def line(n,pts,r=.004,m=grey):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=2;p=c.splines.new('POLY');p.points.add(len(pts)-1)
 for a,b in zip(p.points,pts):a.co=(*b,1)
 o=bpy.data.objects.new(n,c);bpy.context.collection.objects.link(o);o.data.materials.append(m);return o
# shortcut: normalized wheelbase and estimated cross-car depth, replace with measured scale and validated perspective when available.
stations=[(-.39,.300,.455),(-.29,.290,.532),(-.17,.280,.590),(-.05,.277,.614),(.15,.278,.618),(.35,.280,.615),(.52,.278,.606),(.60,.270,.575),(.70,.298,.445)]
verts=[]
for x,w,z in stations:
 for t in (-1,-.75,-.4,0,.4,.75,1):verts.append((x,w*t,z+.014*(1-t*t)))
roof=mesh('Authored roof and front/rear transition',verts,[(i*7+j,i*7+j+1,(i+1)*7+j+1,(i+1)*7+j) for i in range(len(stations)-1) for j in range(6)],grey)
# Distinct main roof is retained; sloping end sections are diagnostic glass rather than a painted solid wedge.
roof.data.materials.append(glass)
for p in roof.data.polygons:
 if p.center.x<-.18 or p.center.x>.60:pass
for i,p in enumerate(roof.data.polygons):
 if i//6 in (0,1,7):p.material_index=1
def sx(u):return (u-280)/506-.5
def sz(v):return (455-v)/506
windows={
 'Front door glass':[(397,221),(432,185),(470,171),(506,166),(553,164),(559,229),(475,236),(412,238)],
 'Rear door glass':[(584,164),(686,163),(730,166),(729,191),(719,213),(701,221),(591,232)],
 'Quarter glass':[(781,168),(816,169),(827,181),(850,211),(847,219),(802,220),(791,208)]}
for side in (-1,1):
 for name,uv in windows.items():
  vs=[(sx(u),side*(.300-(sz(v)-.43)*.11),sz(v)) for u,v in uv]
  mesh(name+f' {side}',vs,[tuple(range(len(vs)))],glass);line(name+' seal '+str(side),vs+[vs[0]],.005)
 # Foreground A/B/C/D pillars and top/lower window rails. No door meshes or production cuts yet.
 for name,uv in {'A pillar':[(355,235),(418,176),(468,154)],'B pillar':[(567,158),(572,235)],'C pillar':[(754,160),(771,226)],'D pillar':[(832,161),(871,227)],'Upper side rail':[(418,176),(468,154),(560,151),(660,151),(750,153),(832,161)],'Lower side rail':[(355,242),(480,244),(595,240),(720,228),(871,227)]}.items():
  line(name+str(side),[(sx(u),side*(.300-(sz(v)-.43)*.11),sz(v)) for u,v in uv],.009 if name.endswith('pillar') else .006)
 # Neutral frame patches between adjacent glass units.
 for name,uv in {'B frame':[(553,158),(584,158),(591,238),(559,239)],'C frame':[(730,159),(781,161),(791,225),(717,232)],'D frame':[(816,161),(835,159),(880,232),(849,225)]}.items():
  vs=[(sx(u),side*(.300-(sz(v)-.43)*.11),sz(v)) for u,v in uv];mesh(name+str(side),vs,[(0,1,2,3)],grey)
for x in (-.5,.5):
 for y in (-.286,.286):
  bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.137,depth=.09,location=(x,y,.137),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name=f'Tire stance proxy {x} {y}';o.data.materials.append(rubber)
  bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.092,depth=.092,location=(x,y,.137),rotation=(math.pi/2,0,0));bpy.context.object.data.materials.append(rim)
line('Front axle',[(-.5,-.33,.137),(-.5,.33,.137)],.003)
line('Rear axle',[(.5,-.33,.137),(.5,.33,.137)],.003)
line('Centerline',[(-.85,0,.005),(.82,0,.005)],.002)
scene=bpy.context.scene;scene['STATUS']='REGIONS 1/2 ONLY — NOT VALIDATED; no body continuation before greenhouse gate';scene['origin']='Fresh authored surface study; no previous body or V02 geometry imported';scene['units']='wheelbase=1; physical metres unknown';scene['references']='O07 profile; O09 opposite profile; O02/O04 pillars; O10/O11 front3Q; O12/O13 rear3Q; S13 S15 S21 secondary'
for key in ['O07','O09','O11','O12','S13','S15','S21']:
 p=O/f'references/complete-library/{key}.png';im=bpy.data.images.load(str(p));im.pack();im.use_fake_user=True
world=bpy.data.worlds.new('Neutral world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.65,.65,1);world.node_tree.nodes['Background'].inputs[1].default_value=.8;scene.world=world
for loc,power,size in [((-2,-3,4),500,5),((1,3,3),350,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);bpy.context.object.data.energy=power;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=size
scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True;scene.display.shading.background_type='WORLD';scene.world.color=(.8,.8,.8)
scene.render.resolution_x=1000;scene.render.resolution_y=650;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
views={'side':((0,-4,.32),(0,0,.32),'ORTHO',1.9),'front':((-4,0,.32),(0,0,.32),'ORTHO',1.25),'rear':((4,0,.32),(0,0,.32),'ORTHO',1.25),'front3q':((-2.5,-3,1.15),(0,0,.33),'PERSP',52),'rear3q':((2.5,-3,1.15),(0,0,.33),'PERSP',52)}
for name,(loc,target,typ,scale) in views.items():
 bpy.ops.object.camera_add(location=loc);cam=bpy.context.object;cam.name='Diagnostic '+name;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type=typ
 if typ=='ORTHO':cam.data.ortho_scale=scale
 else:cam.data.lens=scale
 scene.camera=cam;scene.render.filepath=str(R/f'greenhouse-{name}-v01.png');bpy.ops.render.render(write_still=True)
scene.camera=bpy.data.objects['Diagnostic side']
assert len([o for o in bpy.data.objects if o.name.startswith('Tire stance proxy')])==4
bpy.context.view_layer.update()
assert abs(min((o.matrix_world@v.co).z for o in bpy.data.objects if o.name.startswith('Tire stance proxy') for v in o.data.vertices))<1e-5
bpy.ops.wm.save_as_mainfile(filepath=str(D/'isuzu-mux-reference-constrained-v01.blend'))
(D/'reference-constrained-v01/model-checks.json').write_text(json.dumps({'fresh_scene':True,'previous_body_imported':False,'V02_geometry_imported':False,'wheelbase_normalized':1,'tire_radius_estimated':.137,'track_estimated':.572,'physical_scale_verified':False,'four_tires_grounded':True,'body_beyond_greenhouse':False,'GLB':False,'gate':'PENDING VISUAL INSPECTION'},indent=2))

"""Reference-specific exterior cage study, not an approved production vehicle.
Run: blender -b --python tools/3d/isuzu-mux/source/build-body-candidate.py
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'
scene['status']='BODY CANDIDATE — SILHOUETTE REVIEW REQUIRED; NOT FOR WEBSITE'
scene['coordinates']='metres; +X front, +Y vehicle left, +Z up; tire contact Z=0'
scene['scale_basis']='Estimated 4.84m length / 2.85m wheelbase / 1.86m body width / 1.84m roof. Not surveyed.'
def material(name,color,metal=0,rough=.4):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 return m
paint=material('Cage neutral silver',(.48,.51,.54),.65,.3)
glass=material('Window area study — opaque for silhouette',(.07,.09,.10),.3,.25)
rubber=material('Tire study',(.026,.029,.031),0,.75)
rim=material('Wheel placeholder — design not detailed',(.25,.27,.29),.75,.3)
def mesh(name,verts,faces,mat,sub=0):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);scene.collection.objects.link(ob);ob.data.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 if sub:
  mod=ob.modifiers.new('Control-cage smoothing','SUBSURF');mod.levels=sub;mod.render_levels=sub
 return ob
# Hand-authored body cross-sections, canonical open-side reference controls the stance.
# x, half-width, shoulder height, top/cowl height.
stations=[(-2.42,.73,1.04,1.15),(-2.36,.86,1.11,1.21),(-2.22,.92,1.17,1.25),(-1.95,.93,1.18,1.25),(-1.65,.935,1.19,1.25),(-1.425,.935,1.19,1.25),(-1.2,.932,1.19,1.25),(-.95,.927,1.19,1.25),(-.6,.923,1.19,1.25),(-.2,.923,1.19,1.25),(.2,.925,1.19,1.25),(.6,.928,1.19,1.25),(.95,.93,1.18,1.25),(1.2,.934,1.16,1.25),(1.425,.935,1.15,1.24),(1.65,.93,1.13,1.22),(1.9,.92,1.10,1.19),(2.16,.90,1.08,1.16),(2.32,.85,1.04,1.12),(2.42,.76,.99,1.07)]
# Densify stations around tire apertures to preserve a smooth circular arch boundary.
xs=sorted(set([r[0] for r in stations]+[c+.465*math.cos(i*math.pi/16) for c in [-1.425,1.425] for i in range(17)]))
def interp(x,j):
 for a,b in zip(stations,stations[1:]):
  if a[0]<=x<=b[0]:return a[j]+(b[j]-a[j])*(x-a[0])/(b[0]-a[0])
 return stations[0 if x<0 else -1][j]
def arch(x):
 z=.40
 for c in [-1.425,1.425]:
  d=abs(x-c)
  if d<.465:z=max(z,.39+math.sqrt(.465**2-d*d))
 return z
# Each side is a quad patch with a true open wheel aperture, not a wheel pasted on a solid slab.
for sign,side in [(1,'L'),(-1,'R')]:
 vs=[]
 for x in xs:
  w,h,t=[interp(x,j) for j in [1,2,3]];z=arch(x)
  vs.extend([(x,sign*(w-.045),z),(x,sign*w,z+.035),(x,sign*(w+.008),max(z+.075,.83)),(x,sign*w,h-.08),(x,sign*(w-.025),h),(x,sign*(w-.13),t)])
 fs=[(i*6+j,(i+1)*6+j,(i+1)*6+j+1,i*6+j+1) for i in range(len(xs)-1) for j in range(5)]
 if sign<0:fs=[f[::-1] for f in fs]
 ob=mesh('BODY_SIDE_'+side,vs,fs,paint,1)
 # A narrow arch lip follows the same aperture, leaving the wheel opening empty.
 for c in [-1.425,1.425]:
  vs=[]
  for i in range(33):
   a=i*math.pi/32;x=c+.465*math.cos(a);z=.39+.465*math.sin(a);w=interp(x,1)
   vs.extend([(x,sign*(w+.009),z),(c+.487*math.cos(a),sign*(w+.012),.39+.487*math.sin(a))])
  mesh('ARCH_'+side+str(c),vs,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(32)],paint)
# Bonnet, with longitudinal crown and front narrowing, individually editable cage.
vs=[]
for x in [1.02,1.09,1.25,1.55,1.85,2.15,2.30,2.35]:
 w=interp(x,1)-.13;t=interp(x,3)
 for f in [-1,-.86,-.55,0,.55,.86,1]:vs.append((x,w*f,t+.045*(1-f*f)))
mesh('BONNET_CAGE',vs,[(i*7+j,i*7+j+1,(i+1)*7+j+1,(i+1)*7+j) for i in range(7) for j in range(6)],paint,1)
# Upper cabin cage: rear D pillar, long near-level roof, sloped windscreen, upright SUV hatch.
# x, lower belt half-width, roof half-width, roof z
cab=[(-2.25,.79,.66,1.47),(-2.19,.81,.72,1.69),(-2.08,.81,.75,1.79),(-1.90,.81,.76,1.83),(-1.60,.81,.77,1.84),(-1.15,.81,.77,1.845),(-.65,.81,.77,1.845),(-.20,.81,.76,1.84),(.25,.81,.745,1.82),(.48,.81,.73,1.77),(.62,.81,.71,1.68),(1.08,.80,.74,1.29)]
for sign,side in [(1,'L'),(-1,'R')]:
 vs=[]
 for x,b,r,z in cab:vs.extend([(x,sign*b,1.25),(x,sign*(r+.025),z-.055),(x,sign*r,z)])
 mesh('CABIN_SURROUND_'+side,vs,[(i*3+j,(i+1)*3+j,(i+1)*3+j+1,i*3+j+1) for i in range(len(cab)-1) for j in range(2)],paint,1)
vs=[]
for x,b,r,z in cab:
 for f in [-1,-.92,-.5,0,.5,.92,1]:vs.append((x,r*f,z+.025*(1-f*f)))
roof=mesh('ROOF_WINDSCREEN_CAGE',vs,[(i*7+j,(i+1)*7+j,(i+1)*7+j+1,i*7+j+1) for i in range(len(cab)-1) for j in range(6)],paint,1)
roof.data.materials.append(glass)
for poly in roof.data.polygons:
 if sum(roof.data.vertices[v].co.x for v in poly.vertices)/len(poly.vertices)>.48:poly.material_index=1
# Window openings represented as inset opaque area studies; no final glass claimed.
for sign,side in [(1,'L'),(-1,'R')]:
 for label,points in [('FRONT',[(.96,1.285),(.43,1.735),(-.24,1.775),(-.24,1.285)]),('REAR',[(-.32,1.285),(-.32,1.775),(-1.23,1.775),(-1.23,1.285)]),('QUARTER',[(-1.32,1.285),(-1.32,1.775),(-1.97,1.74),(-2.10,1.32)])]:
  verts=[]
  for x,z in points:
   lo=.81;hi=.765;roofz=1.84
   if x>.25:hi=.74;roofz=1.82
   y=lo+(hi+.025-lo)*(z-1.25)/(roofz-.055-1.25)+.012
   verts.append((x,sign*y,z))
  mesh('WINDOW_AREA_'+side+'_'+label,verts,[(0,1,2,3)],glass)
# Distinct windscreen surface, avoiding an all-silver cabin interpretation.
mesh('WINDSCREEN_AREA',[(.50,-.71,1.77),(.50,.71,1.77),(1.085,.78,1.32),(1.085,-.78,1.32)],[(0,1,2,3)],glass)
mesh('REAR_GLASS_AREA',[(-2.22,-.73,1.48),(-2.22,.73,1.48),(-2.12,.70,1.75),(-2.12,-.70,1.75)],[(0,1,2,3)],glass)
# Front and rear provisional closure surfaces. Fascia is deliberately not detailed at this gate.
for x,name in [(2.39,'FRONT_FASCIA_UNDETAILED'),(-2.39,'TAILGATE_UNDETAILED')]:
 w=.79;mesh(name,[(x,-w,.42),(x,w,.42),(x,w,1.10),(x,-w,1.10)],[(0,1,2,3)],paint)
# Four separate tire-envelope studies. Origins at axle centers; +X forward, wheels rotate around Y.
for x,axle in [(1.425,'F'),(-1.425,'R')]:
 for y,side in [(.825,'L'),(-.825,'R')]:
  vs=[];fs=[];profile=[(-.133,.292),(-.139,.33),(-.125,.371),(-.097,.39),(.097,.39),(.125,.371),(.139,.33),(.133,.292)]
  for off,r in profile:
   for i in range(64):
    a=i*2*math.pi/64;vs.append((r*math.sin(a),off,r*math.cos(a)))
  for j in range(len(profile)-1):
   for i in range(64):fs.append((j*64+i,j*64+(i+1)%64,(j+1)*64+(i+1)%64,(j+1)*64+i))
  wheel=mesh('WHEEL_'+axle+side,vs,fs,rubber);wheel.location=(x,y,.39);wheel['contact_z']=0.0;wheel['stage']='Envelope only; canonical split spokes pending silhouette approval'
  bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.276,depth=.20,location=(x,y,.39),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name='RIM_ENVELOPE_'+axle+side;o.data.materials.append(rim)
# Canonical reference empties, packed so the .blend remains editable without external absolute paths.
refs=bpy.data.collections.new('REFERENCE_PLANES — canonical only');scene.collection.children.link(refs)
for filename,name,loc,rot,size in [('18-09-21','FRONT',(2.8,0,1),(math.pi/2,0,math.pi/2),2.9),('18-09-40','LEFT',(0,1.25,1),(math.pi/2,0,0),5.5),('18-09-48','REAR',(-2.8,0,1),(math.pi/2,0,-math.pi/2),3.6),('18-10-06','RIGHT',(0,-1.25,1),(math.pi/2,0,math.pi),5.5)]:
 p=Path('/home/thunder/Pictures/Screenshots')/('Screenshot From 2026-11-06 '+filename+'.png');assert p.exists(),p
 im=bpy.data.images.load(str(p));im.pack();o=bpy.data.objects.new('REF_'+name,None);refs.objects.link(o);o.empty_display_type='IMAGE';o.data=im;o.empty_display_size=size;o.color[3]=.45;o.location=loc;o.rotation_euler=rot;o.hide_render=True;o['note']='Perspective photograph — scale/alignment approximate; not an orthographic blueprint'
refs.hide_render=True;refs.hide_viewport=True
# Neutral studio for judging surfaces, never hides proportions with bloom or badges.
floor=material('Review floor',(.15,.16,.18),0,.65)
bpy.ops.mesh.primitive_plane_add(size=200);bpy.context.object.name='REVIEW_FLOOR';bpy.context.object.data.materials.append(floor)
scene.world.color=(.22,.22,.22)
def aim(obj,p):obj.rotation_euler=(Vector(p)-obj.location).to_track_quat('-Z','Y').to_euler()
for name,loc,energy,size in [('Key',(4,4,7),1500,6),('Fill',(-3,-4,5),1200,5),('Roof',(-1,2,7),900,5)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=energy;o.data.shape='DISK';o.data.size=size;aim(o,(0,0,.9))
bpy.ops.object.camera_add(location=(7,6,3.7));camera=bpy.context.object;scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=6.25;aim(camera,(0,0,.9))
scene.render.engine='CYCLES';scene.cycles.samples=24
scene.render.resolution_x=1000;scene.render.resolution_y=650;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG'
# Save early cage before rendering so a render interruption never loses modeling work.
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'source/isuzu-mux-master.blend'))
views={'front':((8,0,1.0),5.0),'left':((0,8,1.0),5.8),'right':((0,-8,1.0),5.8),'rear':((-8,0,1.0),5.0),'front-three-quarter':((7,6,3.6),6.15),'rear-three-quarter':((-7,6,3.6),6.15)}
for name,(pos,scale) in views.items():
 camera.location=pos;camera.data.ortho_scale=scale;aim(camera,(0,0,.92));scene.render.filepath=str(ROOT/'renders'/('body-v02-'+name+'.png'));bpy.ops.render.render(write_still=True)
stats={'stage':'body cage, not approved','vertices':0,'triangles':0,'materials':len(bpy.data.materials),'texture_images':4,'textures_note':'Packed reference images only; no production textures','meshes':0}
deps=bpy.context.evaluated_depsgraph_get()
for o in scene.objects:
 if o.type=='MESH' and o.name!='REVIEW_FLOOR':
  me=o.evaluated_get(deps).to_mesh();me.calc_loop_triangles();stats['vertices']+=len(me.vertices);stats['triangles']+=len(me.loop_triangles);stats['meshes']+=1;o.evaluated_get(deps).to_mesh_clear()
assert all(abs(o.location.z-.39)<1e-6 for o in scene.objects if o.name.startswith('WHEEL_'))
(ROOT/'source/body-v02-statistics.json').write_text(json.dumps(stats,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'source/isuzu-mux-master.blend'))

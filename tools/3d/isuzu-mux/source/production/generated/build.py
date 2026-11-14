import bpy,bmesh,math,json,os
from pathlib import Path
from mathutils import Vector
O=Path(os.environ.get('MUX_GENERATED_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';R=O/'renders';A=D/'generated';ROOT=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux');STAGE=os.environ.get('MUX_STAGE','blockout');bpy.ops.wm.read_factory_settings(use_empty=True)
for p in [D/'milestones',R,A]:p.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.world=bpy.data.worlds.new('Neutral diagnostic world')
def mat(name,c,metal=0,rough=.4,trans=0,emit=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*c,1);n.inputs['Metallic'].default_value=metal;n.inputs['Roughness'].default_value=rough;n.inputs['Transmission Weight'].default_value=trans
 if emit:n.inputs['Emission Color'].default_value=(*c,1);n.inputs['Emission Strength'].default_value=emit
 return m
paint=mat('Silver metallic paint',(.47,.50,.53),.72,.25);black=mat('Graphite polymer',(.018,.022,.027),.05,.34);rubber=mat('Tire rubber',(.012,.014,.017),0,.8);chrome=mat('Brushed bright metal',(.64,.69,.73),.92,.17);glass=mat('Smoked automotive glass',(.055,.09,.12),.1,.12,.35);red=mat('Rear red lens',(.4,.008,.015),.18,.2,.1);light=mat('Neutral lamp element',(.75,.86,.95),.2,.18,0,.3);seatmat=mat('Charcoal seat upholstery',(.035,.041,.048),0,.8);inside=mat('Interior graphite',(.055,.06,.065),0,.58);screen=mat('Infotainment screen',(.02,.045,.065),.1,.2)
def mesh(name,vs,fs,m=paint,sub=0,mirror=False):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob.data.materials.append(m)
 for f in me.polygons:f.use_smooth=True
 if mirror:
  mod=ob.modifiers.new('Symmetry Y','MIRROR');mod.use_axis[0]=False;mod.use_axis[1]=True;mod.use_clip=True
 if sub:
  mod=ob.modifiers.new('Broad subdivision surfaces','SUBSURF');mod.levels=sub;mod.render_levels=sub
 return ob
def cube(name,loc,size,m=paint,bevel=.02):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);ob=bpy.context.object;ob.name=name;ob.scale=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ob.data.materials.append(m)
 if bevel:mod=ob.modifiers.new('Controlled edge radius','BEVEL');mod.width=bevel;mod.segments=3
 for f in ob.data.polygons:f.use_smooth=True
 if bevel:ob.modifiers.new('Stable hard-surface normals','WEIGHTED_NORMAL')
 return ob
def tube(name,pts,r=.01,m=chrome):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=12;cu.bevel_depth=r;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,q in zip(sp.points,pts):p.co=(*q,1)
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);cu.materials.append(m);return ob
def cyl(name,loc,r,depth,m=black,axis='Y',segments=40):
 rot=(math.pi/2,0,0) if axis=='Y' else (0,math.pi/2,0) if axis=='X' else (0,0,0);bpy.ops.mesh.primitive_cylinder_add(vertices=segments,radius=r,depth=depth,location=loc,rotation=rot);ob=bpy.context.object;ob.name=name;ob.data.materials.append(m)
 for f in ob.data.polygons:f.use_smooth=True
 return ob
def parent(ob,p):
 bpy.context.view_layer.update();world=ob.matrix_world.copy();ob.parent=p;ob.matrix_world=world
def empty(n,loc=(0,0,0)):
 ob=bpy.data.objects.new(n,None);bpy.context.collection.objects.link(ob);ob.location=loc;return ob
root=empty('MUX_ROOT');axles=[-1.4225,1.4225];radius=.382;track=1.570
for i,x in enumerate(axles):
 for side in [-1,1]:empty(('FRONT' if i==0 else 'REAR')+(' LEFT' if side>0 else ' RIGHT')+' WHEEL CENTER',(x,side*track/2,radius))
s['dimension_source']='https://www.isuzu.in/images/Brochure/pdf_area/ISUZU%20mu-X%20brochure.pdf';s['documented_dimensions']='4825mm L / 1860mm W / 1860mm H / 2845mm wheelbase / 905mm front / 1075mm rear overhang / 1570mm track. India same-body-family brochure; exact trim/year not asserted.';s['approximation']='Tire radius .382m and all body/glass curvature are reference-inspired modeling decisions, not recovered CAD.'
bpy.ops.wm.save_as_mainfile(filepath=str(D/'milestones/generated-hardpoints-v01.blend'))
sections=[(-2.3275,1.075,.86),(-2.30,1.09,.88),(-2.19,1.13,.92),(-1.95,1.16,.93),(-1.4225,1.20,.93),(-1.02,1.255,.91),(-.82,1.24,.90),(-.35,1.23,.91),(.25,1.25,.92),(.8,1.27,.93),(1.4225,1.29,.93),(1.93,1.30,.92),(2.34,1.30,.90),(2.475,1.29,.87),(2.4975,1.28,.85)]
vs=[]
for x,z,w in sections:
 for y,zz in [(0,.42),(.65,.42),(w-.045,.45),(w,.66),(w,.93),(w-.012,z-.13),(w-.06,z-.035),(.64,z),(0,z+.025)]:vs.append((x,y,zz))
N=9;fs=[(i*N+j,(i+1)*N+j,(i+1)*N+j+1,i*N+j+1) for i in range(len(sections)-1) for j in range(N-1)];fs+=[tuple(range(N-1,-1,-1)),tuple((len(sections)-1)*N+j for j in range(N))];body=mesh('BODY — editable half control cage',vs,fs,paint,1,True)
cutters=[]
def boolcut(ob,cutter,operation='DIFFERENCE',apply=False):
 mod=ob.modifiers.new('Opening / '+cutter.name,'BOOLEAN');mod.object=cutter;mod.operation=operation;mod.solver='EXACT';cutter.hide_render=True;cutter.hide_set(True);cutters.append(cutter)
 if apply:bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=mod.name)
for x in axles:boolcut(body,cyl('CUT wheel arch '+str(x),(x,0,radius),.445,2.7,black,'Y',64))
# The cabin is hollow rather than a closed box underneath the windows.
boolcut(body,cube('CUT cabin hollow',(.68,0,1.2),(3.05,1.53,1.52),black,0))
def patch(name,fun,nu=8,nv=6,m=paint,sub=1,mirror=False):
 vs=[fun(i/nu,j/nv) for i in range(nu+1) for j in range(nv+1)];fs=[(i*(nv+1)+j,(i+1)*(nv+1)+j,(i+1)*(nv+1)+j+1,i*(nv+1)+j+1) for i in range(nu) for j in range(nv)];return mesh(name,vs,fs,m,sub,mirror)
roofrows=[(-.48,1.71,.66),(-.40,1.76,.70),(-.16,1.79,.73),(.35,1.80,.735),(1.05,1.80,.735),(1.7,1.79,.73),(1.99,1.76,.70),(2.08,1.69,.66)]
rvs=[(x,w*t,z-.045*t*t) for x,z,w in roofrows for t in [0,.35,.7,.93,1]];rfs=[(i*5+j,(i+1)*5+j,(i+1)*5+j+1,i*5+j+1) for i in range(len(roofrows)-1) for j in range(4)];roof=mesh('ROOF — longitudinal crown cage',rvs,rfs,paint,2,True)
def wind(u,v):
 t=2*u-1;return(-1.13*(1-v)-.48*v+.12*t*t*(1-v)+.035*t*t*v-.025*math.sin(math.pi*v)*(1-t*t),t*(.755*(1-v)+.655*v),1.255*(1-v)+1.70*v+.025*(1-t*t))
windob=patch('WINDSCREEN',wind,10,6,glass,1);windob.modifiers.new('Glass thickness','SOLIDIFY').thickness=.006
def rearwind(u,v):
 t=2*u-1;return(2.34*(1-v)+2.075*v-.045*t*t,t*(.765*(1-v)+.65*v),1.30*(1-v)+1.695*v+.022*(1-t*t))
rearob=patch('REAR GLASS',rearwind,10,6,glass,1);rearob.modifiers.new('Glass thickness','SOLIDIFY').thickness=.006
def sideY(z):return .865-(z-1.24)*.235
def roundpoly(points,amount=.10):
 out=[]
 for i,b in enumerate(points):
  a=Vector(points[i-1]);b=Vector(b);c=Vector(points[(i+1)%len(points)]);p=b+(a-b)*amount;q=b+(c-b)*amount
  for j in range(5):t=j/4;v=(1-t)**2*p+2*(1-t)*t*b+t*t*q;out.append(tuple(v))
 return out
windows={ 'FRONT':[(-.78,1.265),(-.34,1.655),(.17,1.69),(.22,1.27)],'REAR':[(.37,1.28),(.33,1.69),(1.28,1.68),(1.26,1.47),(1.14,1.33)],'QUARTER':[(1.64,1.33),(1.51,1.67),(1.93,1.65),(2.14,1.32)]}
glassparts={};frameparts={}
for side in [-1,1]:
 for name,pts in windows.items():
  poly=roundpoly(pts,.10);n=len(poly);cx=sum(x for x,z in poly)/n;cz=sum(z for x,z in poly)/n
  vs=[(cx,side*sideY(cz),cz)]+[(x,side*sideY(z),z) for x,z in poly];ob=mesh(name+' SIDE GLASS '+str(side),vs,[(0,i+1,(i+1)%n+1) for i in range(n)],glass);ob.modifiers.new('Glass thickness','SOLIDIFY').thickness=.006;glassparts[(name,side)]=ob
  for f in ob.data.polygons:f.use_smooth=False
  outer=[(cx+(x-cx)*1.10,cz+(z-cz)*1.13) for x,z in poly];vs=[(x,side*(sideY(z)+.002),z) for x,z in poly]+[(x,side*sideY(z),z) for x,z in outer];frameparts[(name,side)]=mesh(name+' WINDOW FRAME '+str(side),vs,[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],paint)
 # Broad structural pillars and roof-side rail, without heavy trim hiding the window outlines.
 mesh('A PILLAR '+str(side),[(-1.01,side*.755,1.255),(-.445,side*.655,1.70),(-.30,side*sideY(1.71),1.71),(-.80,side*sideY(1.24),1.24)],[(0,1,2,3)],paint)
 cube('B PILLAR '+str(side),(.285,side*.82,1.11),(.085,.075,1.13),black,.012)
 mesh('C PILLAR '+str(side),[(1.29,side*sideY(1.70),1.70),(1.51,side*sideY(1.70),1.70),(1.66,side*sideY(1.27),1.27),(1.16,side*sideY(1.27),1.27)],[(0,1,2,3)],paint)
 mesh('D PILLAR '+str(side),[(1.94,side*sideY(1.70),1.70),(2.04,side*.65,1.695),(2.295,side*.765,1.30),(2.14,side*sideY(1.30),1.30)],[(0,1,2,3)],paint)
 bridge=[(-.33,.74,1.715),(-.10,.75,1.745),(.5,.75,1.755),(1.4,.74,1.745),(1.98,.70,1.715)]
 bv=[(x,side*y,z) for x,y,z in bridge]+[(x,side*sideY(1.685),1.685) for x,y,z in bridge];mesh('Roof edge bridge '+str(side),bv,[(i,i+1,i+1+len(bridge),i+len(bridge)) for i in range(len(bridge)-1)],paint)
 tube('Roof-side structure '+str(side),[(-.42,side*.735,1.715),(-.10,side*.765,1.735),(.5,side*.77,1.745),(1.4,side*.76,1.735),(1.99,side*.70,1.71)],.028,paint)
wheelroots=[]
for axle,x in enumerate(axles):
 for side in [-1,1]:
  n='WHEEL_'+('F' if axle==0 else 'R')+('L' if side>0 else 'R');wr=empty(n,(x,side*.785,radius));wheelroots.append(wr)
  prof=[(.265,-.125),(.34,-.1275),(.373,-.105),(.382,-.055),(.382,.055),(.373,.105),(.34,.1275),(.265,.125)];v=[(x+rad*math.cos(2*math.pi*i/64),side*.785+yy,radius+rad*math.sin(2*math.pi*i/64)) for i in range(64) for rad,yy in prof];f=[(i*8+j,((i+1)%64)*8+j,((i+1)%64)*8+(j+1)%8,i*8+(j+1)%8) for i in range(64) for j in range(8)];parent(mesh(n+' tire',v,f,rubber),wr)
  parent(cyl(n+' rim barrel',(x,side*.785,radius),.258,.20,black),wr)
  if STAGE=='full':
   y=side*(.785+.132)
   for k in range(6):
    for spread in [-.080,.080]:
     a=2*math.pi*k/6+spread;pts=[]
     for rad,off in [(.07,-.012),(.246,-.009),(.246,.009),(.07,.012)]:pts.append((x+rad*math.cos(a)+off*math.sin(a),y,radius+rad*math.sin(a)-off*math.cos(a)))
     ob=mesh(n+' split spoke',pts,[(0,1,2,3)],chrome);ob.modifiers.new('Spoke depth','SOLIDIFY').thickness=.018;parent(ob,wr)
   parent(cyl(n+' hub',(x,y,radius),.071,.025,chrome),wr)
   bpy.ops.mesh.primitive_torus_add(major_radius=.249,minor_radius=.011,major_segments=64,minor_segments=8,location=(x,y,radius),rotation=(math.pi/2,0,0));ob=bpy.context.object;ob.name=n+' rim lip';ob.data.materials.append(chrome);parent(ob,wr)
def setup_views(prefix):
 s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.display.shading.show_shadows=True;s.display.shading.background_type='WORLD';s.world.color=(.7,.7,.7);s.render.resolution_x=1100;s.render.resolution_y=750;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
 views={'front':((-9,0,2.9),(0,0,.95),'PERSP',58),'side':((0,-9,.95),(0,0,.95),'ORTHO',6.1),'right':((0,9,.95),(0,0,.95),'ORTHO',6.1),'rear':((9,0,2.6),(.1,0,.95),'PERSP',58),'front3q':((-7,-8,3.4),(0,0,.9),'PERSP',58),'rear3q':((7,-8,3.1),(.1,0,.9),'PERSP',58)}
 for name,(loc,tar,typ,scale) in views.items():
  cam=bpy.data.objects.get('VIEW '+name)
  if not cam:bpy.ops.object.camera_add(location=loc);cam=bpy.context.object;cam.name='VIEW '+name
  cam.location=loc;cam.rotation_euler=(Vector(tar)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type=typ
  if typ=='ORTHO':cam.data.ortho_scale=scale
  else:cam.data.lens=scale
  s.camera=cam;s.render.filepath=str(R/f'{prefix}-{name}.png');bpy.ops.render.render(write_still=True)
if STAGE=='blockout':
 s['STATUS']='Fresh reference-based subdivision blockout, practical visual target; no borrowed geometry';setup_views('generated-blockout');bpy.ops.wm.save_as_mainfile(filepath=str(D/'milestones/generated-blockout-v01.blend'))
if STAGE=='full':
 # Extract functional panels from this newly authored body, then leave actual openings in the fixed shell.
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();base=bpy.data.meshes.new_from_object(body.evaluated_get(dg));doorroots={}
 for side in [-1,1]:
  for letter,(lo,hi) in [('F',(-.80,.24)),('R',(.265,1.28))]:
   name='DOOR_'+letter+('L' if side>0 else 'R');pivot=empty(name,(lo-.015,side*.955,.62));doorroots[(letter,side)]=pivot
   ob=bpy.data.objects.new(name+' painted outer shell',base.copy());bpy.context.collection.objects.link(ob);ob.data.materials.clear();ob.data.materials.append(paint)
   cutter=cube('CUT '+name+' panel extraction',((lo+hi)/2,side*.91,.865),(hi-lo-.014,.39,.77),black,0);boolcut(ob,cutter,'INTERSECT',True)
   bevel=ob.modifiers.new('Panel edge radius','BEVEL');bevel.width=.005;bevel.segments=2;ob.modifiers.new('Panel broad-face normals','WEIGHTED_NORMAL');parent(ob,pivot)
   boolcut(body,cube('CUT '+name+' aperture',((lo+hi)/2,side*.91,.865),(hi-lo+.006,.42,.79),black,0))
   for part in [glassparts[('FRONT' if letter=='F' else 'REAR',side)],frameparts[('FRONT' if letter=='F' else 'REAR',side)]]:parent(part,pivot)
   parent(cube(name+' inner door card',((lo+hi)/2,side*.775,.89),(hi-lo-.09,.055,.55),inside,.035),pivot)
   parent(cube(name+' armrest',((lo+hi)/2+.04,side*.73,.86),(.42,.075,.065),black,.025),pivot)
   parent(cube(name+' outer handle',(hi-.17,side*.94,1.11),(.16,.028,.035),chrome,.015),pivot)
   parent(cube(name+' inner pull',(hi-.20,side*.73,.99),(.12,.022,.035),chrome,.012),pivot)
  # Fixed aperture sills, upper seals and interior jambs.
  cube('Cabin sill '+str(side),(.22,side*.77,.465),(2.1,.12,.09),black,.018)
  for x in [-.80,.25,1.28]:cube('Door jamb '+str(side)+' '+str(x),(x,side*.78,.86),(.045,.11,.78),paint,.012)
  cube('SIDE STEP '+str(side),(.37,side*.98,.40),(2.55,.17,.09),black,.035);cube('Step metallic edge '+str(side),(.37,side*1.055,.41),(2.5,.025,.04),chrome,.012)
  tube('ROOF RAIL '+str(side),[(-.35,side*.62,1.81),(-.23,side*.63,1.85),(.3,side*.64,1.86),(1.5,side*.63,1.85),(1.90,side*.61,1.80)],.018,chrome)
  for x in [-.25,.65,1.82]:cube('Rail foot',(x,side*.63,1.79),(.10,.07,.07),black,.02)
  # Reference-inspired wheel-arch lips are broad strips, not dense tread detail.
  for x in axles:
   vs=[]
   for j in range(33):
    a=math.radians(7+166*j/32)
    for rad,yy in [(.443,.925),(.481,.941)]:vs.append((x+rad*math.cos(a),side*yy,radius+rad*math.sin(a)))
   mesh('Wheel-arch edge '+str(side)+' '+str(x),vs,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(32)],paint)
  mirrorroot=empty('MIRROR_'+('L' if side>0 else 'R'),(-.73,side*.88,1.23));parent(mirrorroot,doorroots[('F',side)])
  parent(cube('Mirror support '+str(side),(-.72,side*.94,1.22),(.09,.16,.06),black,.025),mirrorroot)
  parent(cube('Mirror body '+str(side),(-.74,side*1.075,1.25),(.23,.18,.14),paint,.055),mirrorroot)
  parent(cube('Mirror glass '+str(side),(-.618,side*1.075,1.25),(.009,.15,.102),glass,.025),mirrorroot)
 # Hood cut and engine aperture. The panel is a new mirrored subdivision surface.
 boolcut(body,cube('CUT engine aperture',(-1.56,0,1.22),(1.36,1.58,.58),black,0))
 bonnet=empty('BONNET',(-.98,0,1.275))
 def hood(u,v):
  x=-2.20+1.22*u;w=.69+.075*u;return(x+.10*v*v*(1-u),w*v,1.075+.17*u+.04*(1-v*v)*math.sin(math.pi*(.12+.76*u)))
 h=patch('BONNET editable half cage',hood,7,5,paint,2,True);h.modifiers.new('Bonnet inner thickness','SOLIDIFY').thickness=.018;parent(h,bonnet)
 parent(patch('Bonnet underside insulation',lambda u,v:(-2.08+1.02*u,(-.55+1.1*v),1.07+.15*u),6,4,black,1),bonnet)
 # Hollow tailgate opening plus a separate metal lower panel and rear glass assembly.
 boolcut(body,cube('CUT tailgate aperture',(2.40,0,.90),(.35,1.48,1.05),black,0))
 hatch=empty('TAILGATE',(2.07,0,1.70))
 tail=patch('TAILGATE painted panel',lambda u,v:(2.405-.06*(2*u-1)**2+.025*math.sin(math.pi*v),(2*u-1)*(.71+.035*v),.48+.82*v),8,6,paint,1);tail.modifiers.new('Tailgate thickness','SOLIDIFY').thickness=.035;parent(tail,hatch);parent(rearob,hatch)
 parent(cube('Tailgate interior trim',(2.38,0,.9),(.045,1.30,.65),inside,.07),hatch)
 # Fascia housings follow the reference's angular, outward-rising envelopes.
 def faceplate(name,points,m,xfunc,solid=.008):
  ob=mesh(name,[(xfunc(y,z),y,z) for y,z in points],[tuple(range(len(points)))],m);ob.modifiers.new('Housing depth','SOLIDIFY').thickness=solid;return ob
 boolcut(body,cube('CUT upper fascia seating',(-2.325,0,.985),(.35,1.86,.33),black,0))
 grille=[(-.50,.76),(-.63,1.00),(-.54,1.075),(.54,1.075),(.63,1.00),(.50,.76)];faceplate('GRILLE dark recess',grille,black,lambda y,z:-2.345+.06*abs(y))
 for z,w in [(1.025,.58),(.89,.535)]:
  for side in [-1,1]:
   pts=[(0,z+.027),(side*w,z+.037),(side*(w-.08),z-.036),(0,z-.024)];faceplate('GRILLE chrome double bar',pts,chrome,lambda y,z:-2.367+.07*abs(y),.016)
 for z in [.53,.59,.65,.71]:cube('LOWER INTAKE slat',(-2.35,0,z),(.035,1.10,.014),black,.005)
 cube('LOWER INTAKE shadow',(-2.338,0,.62),(.04,1.16,.24),black,.055)
 for side in [-1,1]:
  pts=[(side*.54,1.035),(side*.885,1.135),(side*.92,.925),(side*.78,.88),(side*.58,.925)];xf=lambda y,z:-2.36+.43*(abs(y)-.54)
  housing=faceplate('HEADLIGHT housing '+str(side),pts,black,xf,.035);tube('Headlight bright perimeter '+str(side),[(xf(y,z)-.01,y,z) for y,z in pts+[pts[0]]],.009,chrome)
  cyl('LIGHTS_FRONT projector '+str(side),(-2.295,side*.775,1.015),.055,.025,chrome,'X');cyl('LIGHTS_FRONT lens '+str(side),(-2.314,side*.775,1.015),.043,.006,light,'X')
  tube('LIGHTS_FRONT upper guide '+str(side),[(xf(side*y,z)-.018,side*y,z) for y,z in [(.57,1.035),(.74,1.085),(.87,1.115)]],.005,light)
  lens=faceplate('HEADLIGHT outer lens '+str(side),pts,glass,lambda y,z:xf(y,z)-.018,.004)
  fogpts=[(side*.63,.49),(side*.91,.50),(side*.88,.77),(side*.70,.79)];faceplate('Fog housing '+str(side),fogpts,black,lambda y,z:-2.365+.02*abs(y),.04);cyl('Fog chrome ring '+str(side),(-2.37,side*.775,.646),.067,.026,chrome,'X');cyl('Fog lens '+str(side),(-2.39,side*.775,.646),.050,.010,light,'X')
  tube('Fog angled trim '+str(side),[(-2.38,side*.65,.51),(-2.38,side*.90,.52),(-2.37,side*.87,.76)],.011,chrome)
 # Bumper and rear broad split lamps, including side wrap and hatch-mounted inner halves.
 cube('Front lower skid edge',(-2.30,0,.455),(.12,1.4,.10),paint,.04);cube('Rear lower bumper',(2.445,0,.53),(.14,1.72,.20),black,.055);cube('Rear bumper metallic edge',(2.465,0,.66),(.10,1.72,.055),paint,.02)
 for side in [-1,1]:
  outpts=[(side*.73,1.23),(side*.91,1.255),(side*.91,1.10),(side*.72,1.09)];faceplate('LIGHTS_REAR outer lens '+str(side),outpts,red,lambda y,z:2.46-.10*abs(y),.015)
  innerpts=[(side*.46,1.22),(side*.72,1.23),(side*.72,1.095),(side*.57,1.11)];parent(faceplate('LIGHTS_REAR hatch lens '+str(side),innerpts,red,lambda y,z:2.44-.07*abs(y),.015),hatch)
  tube('Rear lamp clear upper strip '+str(side),[(2.40,side*.49,1.205),(2.39,side*.72,1.215),(2.35,side*.90,1.25)],.016,light)
  # Outer red lamp wraps forward around the rear quarter.
  mesh('Rear lamp side wrap '+str(side),[(2.18,side*.915,1.23),(2.40,side*.88,1.25),(2.40,side*.88,1.10),(2.23,side*.91,1.13)],[(0,1,2,3)],red)
  cube('Rear reflector '+str(side),(2.505,side*.73,.50),(.015,.16,.045),red,.015)
 parent(cube('Tailgate chrome garnish',(2.457,0,1.235),(.035,1.28,.045),chrome,.012),hatch);parent(cube('Rear plate recess',(2.46,0,.985),(.025,.40,.15),black,.02),hatch)
 parent(cube('Tailgate latch',(2.466,0,.78),(.02,.15,.03),black,.012),hatch)
 # Interior is deliberately economical but continuous through every opening.
 cube('INTERIOR cabin floor',(.62,0,.515),(3.14,1.50,.07),inside,.035);cube('Cargo rear floor',(1.99,0,.60),(.60,1.45,.10),inside,.03)
 dash=cube('INTERIOR dashboard',(-.71,0,1.075),(.35,1.44,.30),inside,.09)
 cube('Center radio pod',(-.48,0,1.07),(.08,.30,.33),black,.045);cube('Infotainment display',(-.432,0,1.13),(.012,.22,.13),screen,.012)
 cyl('Climate control ring',(-.423,0,.97),.067,.012,chrome,'X');cyl('Climate control center',(-.435,0,.97),.052,.014,black,'X')
 cube('CENTER CONSOLE',(-.06,0,.72),(.70,.24,.25),inside,.065);cube('Gear selector base',(-.22,0,.85),(.18,.18,.035),chrome,.02);cube('Gear lever',(-.20,0,.92),(.055,.055,.13),black,.02)
 bpy.ops.mesh.primitive_torus_add(major_radius=.147,minor_radius=.018,major_segments=48,minor_segments=8,location=(-.39,-.44,1.12),rotation=(0,math.pi/2,0));ob=bpy.context.object;ob.name='RHD STEERING WHEEL';ob.data.materials.append(black);cyl('Steering hub',(-.39,-.44,1.12),.06,.065,black,'X')
 for a in [0,2.1,4.2]:tube('Steering spoke',[(-.39,-.44,1.12),(-.39,-.44+.13*math.cos(a),1.12+.13*math.sin(a))],.018,inside)
 cube('Instrument binnacle',(-.57,-.44,1.20),(.16,.32,.15),black,.05)
 for row,x in enumerate([.10,1.04,1.85]):
  for side in [-1,1]:
   y=side*(.41 if row<2 else .36);cube('Seat cushion '+str(row)+str(side),(x,y,.69),(.48,.48,.17),seatmat,.075);back=cube('Seat back '+str(row)+str(side),(x+.25,y,.97),(.14,.48,.53),seatmat,.065);back.rotation_euler[1]=.15;cube('Seat headrest '+str(row)+str(side),(x+.28,y,1.31),(.12,.23,.16),seatmat,.04)
 # Engine bay visible masses only, referenced to authoritative 18-05-58 image.
 cube('ENGINE_BAY floor',(-1.57,0,.69),(1.30,1.40,.08),black,.025);cube('Firewall',(-.91,0,.96),(.06,1.36,.48),inside,.025)
 for side in [-1,1]:cube('Engine bay side structure',(-1.55,side*.66,.93),(1.25,.08,.22),paint,.02)
 cube('ENGINE cover',(-1.50,0,1.055),(.58,.57,.17),black,.08);cube('Engine upper inset',(-1.48,0,1.15),(.35,.30,.035),inside,.035)
 cube('Battery',(-1.28,-.49,1.02),(.31,.25,.20),black,.015);cube('Battery positive terminal',(-1.22,-.49,1.135),(.07,.05,.02),red,.007);cube('Air filter box',(-1.73,.48,1.02),(.36,.28,.23),black,.035)
 tube('Major intake hose',[(-1.72,.46,1.10),(-1.63,.31,1.12),(-1.50,.20,1.09)],.045,black)
 for x,y,r in [(-1.25,.52,.075),(-1.92,-.51,.065)]:
  cyl('Reservoir',(x,y,1.01),r,.14,mat('Reservoir polymer '+str(x),(.65,.65,.58),0,.4),'Z',24);cyl('Reservoir cap',(x,y,1.09),r*.6,.02,black,'Z',24)
 cube('Radiator upper rail',(-2.09,0,.98),(.07,1.22,.08),black,.012)
 # Editable keyframes; neutral closed frame 1 and normal open range at frame 50.
 motion=[]
 for (letter,side),ob in doorroots.items():motion.append((ob,2,side*math.radians(55)))
 motion += [(bonnet,1,math.radians(58)),(hatch,1,-math.radians(82))]
 for ob,axis,angle in motion:
  ob.rotation_euler=(0,0,0);ob.keyframe_insert(data_path='rotation_euler',frame=1);ob.rotation_euler[axis]=angle;ob.keyframe_insert(data_path='rotation_euler',frame=50)
 s.frame_set(1)
 bevel=body.modifiers.new('Body opening edge softening','BEVEL');bevel.width=.006;bevel.segments=2;body.modifiers.new('Body broad-face normals','WEIGHTED_NORMAL')
 # An optional named light rig is not part of exported geometry.
 for ob in list(bpy.context.scene.objects):
  if ob.parent is None and ob!=root and ob.type not in ['CAMERA','LIGHT'] and not ob.name.startswith('CUT'):parent(ob,root)
 s['STATUS']='Fresh generated practical MU-X candidate — visual review pending; no CAD accuracy claim';s['paid_assets']='NONE';s['references']='All 18 authoritative images; body/trim authority canonical silver; engine/interior supplements used only in their regions';s['functional_frames']='1 closed / 50 doors, bonnet and tailgate open'
 bpy.ops.wm.save_as_mainfile(filepath=str(D/'milestones/generated-components-v01.blend'));setup_views('generated-closed')
 s.frame_set(50)
 for name in ['front3q','rear3q']:
  s.camera=bpy.data.objects['VIEW '+name];s.render.filepath=str(R/f'generated-open-{name}.png');bpy.ops.render.render(write_still=True)
 s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(D/'isuzu-mux-generated-master.blend'))

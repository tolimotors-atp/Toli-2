import bpy,bmesh,math,json,os,ast
from pathlib import Path
from mathutils import Vector
O=Path(os.environ.get('MUX_V02_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';R=O/'renders/refinement-v02';A=D/'generated'
bpy.ops.wm.open_mainfile(filepath=str(D/'milestones/isuzu-mux-v01-comparison-rig.blend'));s=bpy.context.scene;s.frame_set(1)
root=bpy.data.objects['MUX_ROOT'];body=bpy.data.objects['BODY — editable half control cage'];bonnet=bpy.data.objects['BONNET'];hatch=bpy.data.objects['TAILGATE'];paint=bpy.data.materials['Silver metallic paint'];black=bpy.data.materials['Graphite polymer'];chrome=bpy.data.materials['Brushed bright metal'];glass=bpy.data.materials['Smoked automotive glass'];red=bpy.data.materials['Rear red lens'];light=bpy.data.materials['Neutral lamp element']
source=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/generated/build.py').read_text();tree=ast.parse(source);defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['mesh','cube','tube','cyl','parent','patch','sideY']];exec(compile(ast.Module(body=defs,type_ignores=[]),'v01_helpers','exec'))
def attach(ob,p=root):parent(ob,p);return ob
def remove_prefixes(prefixes):
 for ob in list(bpy.data.objects):
  if any(ob.name.startswith(p) for p in prefixes):bpy.data.objects.remove(ob,do_unlink=True)
def faceplate(name,pts,m,xf,p=root,depth=.009):
 ob=attach(mesh(name,[(xf(y,z),y,z) for y,z in pts],[tuple(range(len(pts)))],m),p);mod=ob.modifiers.new('Envelope depth','SOLIDIFY');mod.thickness=depth;bev=ob.modifiers.new('Envelope edge radius','BEVEL');bev.width=.004;bev.segments=2
 for f in ob.data.polygons:f.use_smooth=False
 return ob
def cut(ob,loc,size,name):
 cutter=cube('CUT V02 '+name,loc,size,black,0);cutter.hide_render=True;cutter.hide_set(True);mod=ob.modifiers.new('V02 seating '+name,'BOOLEAN');mod.object=cutter;mod.solver='EXACT';return cutter
# Keep the original half cage and extracted door meshes, and move their existing vertices together.
def sculpt_world(co):
 x,y,z=co;sgn=1 if y>=0 else -1;ay=abs(y)
 if ay>.69 and .47<z<1.31:
  arch=max(math.exp(-((x-a)/.46)**2) for a in [-1.4225,1.4225]);shoulder=math.exp(-((z-1.07)/.20)**2);lower=math.exp(-((z-.64)/.12)**2)
  y+=sgn*(.034*arch*shoulder-.012*lower*(1-.65*arch))
 if x<-1.82:x+=.14*(ay/.94)**3*math.exp(-((x+2.31)/.43)**2)
 return Vector((x,y,z))
for ob in [body]+[o for o in bpy.data.objects if 'painted outer shell' in o.name]:
 inv=ob.matrix_world.inverted()
 for v in ob.data.vertices:v.co=inv@sculpt_world(ob.matrix_world@v.co)
# Shape the existing bonnet's control points, not a replacement bonnet.
hood=next(o for o in bonnet.children if o.name.startswith('BONNET editable'))
for v in hood.data.vertices:
 co=hood.matrix_world@v.co;x,y,z=co;u=max(0,min(1,(x+2.2)/1.22));co.z+=.018*math.sin(math.pi*u)*(1-(y/.80)**2);v.co=hood.matrix_world.inverted()@co
# Remove only obsolete fascia/lighting modules; preserve body, apertures and pivots.
remove_prefixes(['GRILLE ','HEADLIGHT ','Headlight bright','LIGHTS_FRONT ','Fog housing','Fog chrome','Fog lens','Fog angled','LOWER INTAKE','Front lower skid'])
# Broad curved bumper skin sits on the existing nose. Apertures are real cutouts.
def bumper(u,v):
 t=2*u-1;z=.445+(.395+.14*abs(t)**6)*v;y=.945*t;xx=-2.36+.24*abs(t)**3+.025*math.sin(math.pi*v);return xx,y,z
bumperob=attach(patch('V02 front bumper continuous skin',bumper,24,12,paint,0));sol=bumperob.modifiers.new('Bumper thickness','SOLIDIFY');sol.thickness=.045
cut(bumperob,(-2.35,0,.67),(.6,1.17,.22),'lower intake');cut(body,(-2.33,0,.68),(.40,1.20,.25),'intake recess')
cut(body,(-2.32,0,.98),(.42,1.23,.30),'upper grille recess')
for side in [-1,1]:cut(bumperob,(-2.25,side*.785,.66),(.70,.27,.26),'fog recess '+str(side))
attach(cube('V02 lower intake recess',(-2.33,0,.67),(.06,1.16,.21),black,.045))
for z in [.60,.65,.70,.75]:attach(cube('V02 lower intake slat',(-2.375,0,z),(.018,1.10,.009),black,.003))
# Grille and bars use reference-led angular outlines rather than rectangular floating bars.
xf=lambda y,z:-2.375+.10*(abs(y)/.61)**2
outline=[(-.46,.825),(-.615,1.035),(-.54,1.115),(.54,1.115),(.615,1.035),(.46,.825)]
faceplate('V02 grille recessed envelope',outline,black,lambda y,z:xf(y,z)+.025,depth=.025)
for pts in [[(-.545,1.105),(.545,1.105),(.60,1.045),(.50,1.047),(-.50,1.047),(-.60,1.045)],[(-.575,1.008),(-.49,.95),(.49,.95),(.575,1.008),(.43,.986),(-.43,.986)],[(-.49,.91),(-.435,.845),(.435,.845),(.49,.91),(.37,.883),(-.37,.883)]]:
 faceplate('V02 grille chrome contour',pts,chrome,xf,depth=.012)
remove_prefixes(['V02 grille chrome contour'])
for zi,width in [(1.077,.555),(.963,.515),(.867,.445)]:
 def bar(u,v,zi=zi,width=width):
  y=(2*u-1)*width;z=zi+.030-.060*v+.013*(abs(y)/width)**4;return xf(y,z)-.012+.028*v-.006*math.sin(math.pi*v),y,z
 attach(patch('V02 grille crowned chrome bar',bar,16,4,chrome,0))
# Headlight outer envelope sweeps around the fender; the outer end is farther back and higher.
for side in [-1,1]:
 cut(body,(-2.20,side*.74,1.08),(.84,.48,.32),'headlamp seating '+str(side))
 coords=[(.49,1.085),(.875,1.20),(.935,1.16),(.91,1.00),(.70,.975),(.565,1.025)];pts=[(side*y,z) for y,z in coords]
 hx=lambda y,z:-2.37+.53*((abs(y)-.49)/.445)**1.5
 faceplate('V02 headlamp dark housing '+str(side),pts,black,lambda y,z:hx(y,z)+.010,depth=.03)
 tubeob=attach(tube('V02 headlamp chrome perimeter '+str(side),[(hx(y,z)-.004,y,z) for y,z in pts+[pts[0]]],.006,chrome))
 # Subtle lenses, below the outer shell; envelope is the focus of this pass.
 attach(cyl('V02 headlamp projector '+str(side),(hx(side*.73,1.06)-.007,side*.73,1.06),.047,.010,chrome,'X',32))
 attach(cyl('V02 headlamp projector glass '+str(side),(hx(side*.73,1.06)-.017,side*.73,1.06),.035,.003,light,'X',32))
 faceplate('V02 headlamp outer lens '+str(side),pts,glass,lambda y,z:hx(y,z)-.009,depth=.003)
 attach(tube('V02 headlamp upper guide '+str(side),[(hx(side*y,z)-.016,side*y,z) for y,z in coords[:3]],.004,light))
 fog=[(side*.65,.565),(side*.91,.55),(side*.90,.76),(side*.72,.79)];fx=lambda y,z:-2.38+.20*(abs(y)/.945)**3
 faceplate('V02 fog pocket '+str(side),fog,black,fx,depth=.025)
 attach(cyl('V02 fog ring '+str(side),(fx(side*.785,.66)-.01,side*.785,.66),.058,.020,chrome,'X',32));attach(cyl('V02 fog lens '+str(side),(fx(side*.785,.66)-.025,side*.785,.66),.044,.007,light,'X',32))
 attach(tube('V02 fog lower chrome '+str(side),[(fx(side*y,z)-.01,side*y,z) for y,z in [(.66,.575),(.88,.565),(.89,.75)]],.007,chrome))
# Existing arch lips follow the newly sculpted volumes; avoid a detached bright arc.
for ob in [o for o in bpy.data.objects if o.name.startswith('Wheel-arch edge')]:
 inv=ob.matrix_world.inverted()
 for v in ob.data.vertices:
  co=ob.matrix_world@v.co;co.y+=math.copysign(.012*math.exp(-((co.z-1.0)/.25)**2),co.y);v.co=inv@co
# Window frames retain their existing outlines; thin dark seals and sill closure join them to the body.
for ob in [o for o in bpy.data.objects if 'WINDOW FRAME' in o.name]:
 ob.data.materials.clear();ob.data.materials.append(black)
for side in [-1,1]:
 for name,lo,hi,zlo,zhi,control in [('front',-.79,.23,1.235,1.25,'DOOR_F'),('rear',.36,1.28,1.25,1.30,'DOOR_R'),('quarter',1.60,2.18,1.30,1.30,None)]:
  p=bpy.data.objects[control+('L' if side>0 else 'R')] if control else root
  pts=[(lo,side*.87,zlo),(hi,side*.87,zhi),(hi,side*.842,zhi+.035),(lo,side*.855,zlo+.05)]
  ob=attach(mesh('V02 '+name+' window lower closure '+str(side),pts,[(0,1,2,3)],paint),p);ob.modifiers.new('Sill closure thickness','SOLIDIFY').thickness=.014
  attach(tube('V02 '+name+' belt seal '+str(side),[(lo,side*.86,zlo+.05),(hi,side*.85,zhi+.035)],.008,black),p)
 for prefix in ['A PILLAR','C PILLAR','D PILLAR']:
  ob=bpy.data.objects[prefix+' '+str(side)]
  if prefix=='C PILLAR':
   for v in ob.data.vertices:
    if v.co.x<1.25:v.co.x+=.09
    elif v.co.x>1.60:v.co.x-=.07
  
  for f in ob.data.polygons:f.use_smooth=False
  ob.modifiers.new('Pillar return thickness','SOLIDIFY').thickness=.018
 # Fill only the existing header mismatch; keep roof and windscreen cages intact.
 attach(mesh('V02 roof edge return '+str(side),[(-.35,side*.72,1.735),(-.35,side*.765,1.69),(1.94,side*.765,1.69),(1.94,side*.70,1.735)],[(0,1,2,3)],paint))
# Rear modules are refined with broader tapered lenses; inner portions move with the hatch.
remove_prefixes(['LIGHTS_REAR ','Rear lamp clear upper','Rear lamp side wrap','Tailgate chrome garnish','Rear plate recess'])
for side in [-1,1]:
 outer=[(side*.725,1.265),(side*.925,1.31),(side*.925,1.095),(side*.73,1.075)]
 inner=[(side*.725,1.265),(side*.415,1.205),(side*.505,1.075),(side*.725,1.075)]
 rx=lambda y,z:2.465-.055*(abs(y)/.93)**2
 faceplate('V02 rear fixed lamp '+str(side),outer,red,rx,depth=.018)
 faceplate('V02 rear hatch lamp '+str(side),inner,red,lambda y,z:rx(y,z)+.003,hatch,.018)
 attach(mesh('V02 rear quarter lamp wrap '+str(side),[(2.07,side*.93,1.31),(2.42,side*.90,1.31),(2.42,side*.90,1.095),(2.20,side*.93,1.12)],[(0,1,2,3)],red))
 attach(tube('V02 fixed clear lamp strip '+str(side),[(rx(side*.74,1.25)+.01,side*.74,1.25),(rx(side*.90,1.285)+.01,side*.90,1.285)],.013,light))
 attach(tube('V02 hatch clear lamp strip '+str(side),[(rx(side*.435,1.19)+.01,side*.435,1.19),(rx(side*.71,1.245)+.01,side*.71,1.245)],.012,light),hatch)
attach(cube('V02 hatch chrome garnish',(2.453,0,1.245),(.025,.82,.034),chrome,.008),hatch)
attach(cube('V02 rear plate recess',(2.466,0,1.065),(.022,.43,.165),black,.02),hatch)
# Broader motion diagnostics exposed existing hinge/cowl and sill contacts not covered by V01's shell-only test.
for name,loc in [('BONNET',(-1.15,0,1.275)),('TAILGATE',(2.01,0,1.735))]:
 control=bpy.data.objects[name];bpy.context.view_layer.update();worlds={o:o.matrix_world.copy() for o in control.children};control.location=loc;bpy.context.view_layer.update()
 for child,world in worlds.items():child.matrix_world=world
for ob in bonnet.children:
 if ob.type=='MESH' and ('editable half cage' in ob.name or 'underside insulation' in ob.name):
  inv=ob.matrix_world.inverted()
  for v in ob.data.vertices:
   co=ob.matrix_world@v.co
   if co.x>-1.18:co.x=-1.18+(co.x+1.18)*.015
   v.co=inv@co
for side in [-1,1]:
 ob=bpy.data.objects['Cabin sill '+str(side)];ob.location.y=side*.67;ob.scale.y=.58
for ob in [o for o in bpy.data.objects if 'WINDOW FRAME' in o.name]:
 # Keep the existing perimeter and halve only its oversized frame expansion.
 n=len(ob.data.vertices)//2
 for i in range(n):ob.data.vertices[n+i].co=ob.data.vertices[i].co.lerp(ob.data.vertices[n+i].co,.45)
# V01's broad black bumper tube is reduced to a lower insert, exposing painted rear mass.
ob=bpy.data.objects['Rear lower bumper'];ob.scale.z=.65;ob.location.z=.49
for mod in list(body.modifiers):
 if mod.type in ['BEVEL','WEIGHTED_NORMAL']:
  i=body.modifiers.find(mod.name);body.modifiers.move(i,len(body.modifiers)-1)
s['STATUS']='V02 exterior recognition refinement — visual review required';s['v02_method']='In-place V01 cage/door/bonnet edits; local fascia/lamp modules refined; pivots/interior/engine/wheels retained';s.frame_set(1)
# Invariants: dimensions and camera definitions must not drift; model pivots/animation stay intact.
manifest=json.loads((A/'fixed-cameras-v02.json').read_text())
for n,info in manifest.items():
 cam=bpy.data.objects['CAM_COMPARE_'+n];assert max(abs(a-b) for a,b in zip(cam.location,info['location']))<1e-6;assert max(abs(a-b) for a,b in zip(cam.rotation_euler,info['rotation']))<1e-6
bpy.ops.wm.save_as_mainfile(filepath=str(D/'milestones/isuzu-mux-exterior-v02.blend'));bpy.ops.wm.save_as_mainfile(filepath=str(D/'isuzu-mux-generated-master.blend'))
for name in manifest:
 s.camera=bpy.data.objects['CAM_COMPARE_'+name];s.render.filepath=str(R/('v02-'+name.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('V02 EXTERIOR SAVED AND RENDERED',flush=True)

# All outputs are saved; bypass a headless audio-shutdown hang in this Blender runtime.
os._exit(0)

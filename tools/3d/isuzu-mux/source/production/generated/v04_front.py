import bpy,bmesh,math,json,os,ast
from pathlib import Path
from mathutils import Vector
O=Path(os.environ.get('MUX_V04_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';R=O/'renders/v04';bpy.ops.wm.open_mainfile(filepath=str(D/'isuzu-mux-generated-v04.blend'));s=bpy.context.scene;s.frame_set(1);assert not bpy.data.collections.get('V04_FRONT_COMPOSITION'), 'Run v04_prepare.py before repeating front construction';body=bpy.data.objects['V03_NEW_EXTERIOR_SHELL'];paint=bpy.data.materials['Silver metallic paint'];black=bpy.data.materials['Graphite polymer'];chrome=bpy.data.materials['Brushed bright metal']
# Reuse only existing small construction helpers, never a previous body constructor.
old=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/generated/build.py');tree=ast.parse(old.read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['mesh','cube','tube']],type_ignores=[]),'existing_mesh_helpers','exec'))
def coll(n):c=bpy.data.collections.new(n);s.collection.children.link(c);return c
front=coll('V04_FRONT_COMPOSITION');cuts=coll('V04_CONSTRUCTION_CUTTERS');archive=coll('V03_IDENTITY_REFERENCE');archive.hide_render=True;archive.hide_viewport=True
for ob in list(bpy.data.collections['V03_EXTERIOR'].objects):
 if ob.name.startswith(('V03_GRILLE','V03_HEADLAMP','V03_CORNER','V03_LOWER_OPENING')):
  for c in list(ob.users_collection):c.objects.unlink(ob)
  archive.objects.link(ob)
def put(ob,c=front):
 for old in list(ob.users_collection):old.objects.unlink(ob)
 c.objects.link(ob);return ob
def boolean(ob,c):
 put(c,cuts);c.hide_render=True;c.hide_set(True);m=ob.modifiers.new('V04 region seating / '+c.name,'BOOLEAN');m.object=c;m.solver='EXACT';m.operation='DIFFERENCE'
def prism(name,poly,xa=-2.60,xb=-1.86):
 vs=[(x,y,z) for x in [xa,xb] for y,z in poly];n=len(poly);fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];return mesh(name,vs,fs,black)
def face(name,poly,fun,m,thick=.012):
 ob=put(mesh(name,[(fun(y,z),y,z) for y,z in poly],[tuple(range(len(poly)))],m));sol=ob.modifiers.new('Physical envelope thickness','SOLIDIFY');sol.thickness=thick;sol.offset=0;bev=ob.modifiers.new('Envelope return radius','BEVEL');bev.width=.003;bev.segments=2
 for f in ob.data.polygons:f.use_smooth=False
 ob.modifiers.new('Envelope face normals','WEIGHTED_NORMAL');return ob
# Local changes only: front fender crown and leading shoulder, not the roof or cabin stations.
for i in [1,2]:
 for j in [5,6,7,8,9,10]:
  v=body.data.vertices[i*12+j]
  if abs(v.co.y)>.64:v.co.z+=(.045 if i==1 else .012)*(min(abs(v.co.y)/.90,1))
for j,z in {5:1.115,6:1.24,7:1.27,8:1.245,9:1.21,10:1.19}.items():body.data.vertices[12+j].co.z=z
for j,z in {6:1.255,7:1.28,8:1.29}.items():body.data.vertices[24+j].co.z=z
bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get())
# Sample the uncut original regional boundary so the new nose has actual returns into V03.
hood_back=[]
for i in range(25):
 y=-.78+1.56*i/24;hit,co,no,idx=ev.ray_cast(Vector((-2.105,y,3)),Vector((0,0,-1)));assert hit;hood_back.append(tuple(co))
side_back={}
for side in [-1,1]:
 side_back[side]=[]
 for j in range(17):
  z=.42+.805*j/16;hit,co,no,idx=ev.ray_cast(Vector((-2.105,side*2,z)),Vector((0,-side,0)))
  side_back[side].append(tuple(co) if hit else (-2.105,side*.83,min(z,1.23)))
boolean(body,cube('V04_CUT_OLD_NOSE',(-2.43,0,.85),(.55,2.2,.98),black,0))
def fx(y,z):return -2.3275+.040*max(0,min(1,(z-.42)/.75))+.20*(abs(y)/.89)**3
ny=32;nz=16;vs=[]
for i in range(ny+1):
 y=-.89+1.78*i/ny;ztop=1.11+.115*(abs(y)/.89)**2
 for j in range(nz+1):z=.42+(ztop-.42)*j/nz;vs.append((fx(y,z),y,z))
fs=[(i*(nz+1)+j,i*(nz+1)+j+1,(i+1)*(nz+1)+j+1,(i+1)*(nz+1)+j) for i in range(ny) for j in range(nz)]
skin=put(mesh('V04_FASCIA_SHARED_CURVED_SKIN',vs,fs,paint));sol=skin.modifiers.new('Fascia real skin thickness','SOLIDIFY');sol.thickness=.028;sol.offset=-1
# A broad upper bridge and both side returns seat the composition into the retained macro shell.
vs=[]
for i,back in enumerate(hood_back):
 y=back[1];zf=1.11+.115*(abs(y)/.89)**2;fore=Vector((fx(y,zf),y,zf));back=Vector(back)
 for j in range(5):u=j/4;co=fore.lerp(back,u);co.z+=.006*math.sin(math.pi*u);vs.append(tuple(co))
put(mesh('V04_BONNET_LEADING_TRANSITION',vs,[(i*5+j,(i+1)*5+j,(i+1)*5+j+1,i*5+j+1) for i in range(24) for j in range(4)],paint))
for side in [-1,1]:
 vs=[]
 for j,back in enumerate(side_back[side]):
  z=.42+.805*j/16;fore=(fx(side*.89,z),side*.89,z);vs.extend([fore,back])
 put(mesh('V04_FENDER_FRONT_RETURN_'+str(side),vs,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(16)],paint))
grille=[(-.45,.80),(-.60,.99),(-.555,1.105),(.555,1.105),(.60,.99),(.45,.80)]
lower=[(-.475,.70),(.475,.70),(.44,.52),(-.44,.52)]
holes=[('grille',grille),('lower',lower)]
for side in [-1,1]:
 lamp=[(side*.54,1.06),(side*.82,1.22),(side*.845,1.18),(side*.835,.99),(side*.68,.955),(side*.56,1.00)]
 corner=[(side*.59,.52),(side*.835,.54),(side*.81,.76),(side*.65,.75)];holes.extend([('lamp_'+str(side),lamp),('corner_'+str(side),corner)])
for n,poly in holes:
 boolean(skin,prism('V04_CUT_SKIN_'+n,poly));boolean(body,prism('V04_CUT_BODY_'+n,poly))
 # The recess walls and backing carry real depth, instead of painted projected patches.
 center=sum((Vector(p) for p in poly),Vector((0,0)))/len(poly);inner=[tuple(center+(Vector(p)-center)*.94) for p in poly];vv=[(fx(y,z),y,z) for y,z in poly]+[(fx(y,z)+.045,y,z) for y,z in inner];nn=len(poly)
 put(mesh('V04_RECESS_RETURN_'+n,vv,[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],black))
 face('V04_RECESSED_ENVELOPE_'+n,inner,lambda y,z:fx(y,z)+.043,black,.008)
# Upper surround and lower bar form the dominant double-bar composition; no grille mesh or badge.
outer=[(-.55,1.10),(.55,1.10),(.59,1.025),(.46,.95),(-.46,.95),(-.59,1.025)];inner=[(-.40,1.066),(.40,1.066),(.43,1.029),(.385,.992),(-.385,.992),(-.43,1.029)];vv=[(fx(y,z)-.006,y,z) for y,z in outer+inner];nn=len(outer)
bar=put(mesh('V04_GRILLE_UPPER_CHROME_SURROUND',vv,[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],chrome));bar.modifiers.new('Chrome bar thickness','SOLIDIFY').thickness=.014
face('V04_GRILLE_LOWER_CHROME_BAR',[(-.515,.955),(-.44,.875),(.44,.875),(.515,.955),(.42,.935),(-.42,.935)],lambda y,z:fx(y,z)-.006,chrome,.012)
for side in [-1,1]:
 pts=[(side*.54,1.06),(side*.82,1.22),(side*.845,1.18),(side*.835,.99),(side*.68,.955),(side*.56,1.00)];put(tube('V04_LAMP_ENVELOPE_EDGE_'+str(side),[(fx(y,z)+.002,y,z) for y,z in pts+[pts[0]]],.005,chrome))
# No new regional PASS milestone is saved until the rendered front is judged better.
s['V04_STAGE']='Front composition candidate; actual seated recesses, no optical internals or panel cuts';bpy.ops.wm.save_as_mainfile(filepath=str(D/'isuzu-mux-generated-v04.blend'))
for name in ['FRONT','FRONT_34','SIDE']:
 s.camera=bpy.data.objects['CAM_COMPARE_'+name];s.render.filepath=str(R/('v04-front-candidate-'+name.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('V04 FRONT CANDIDATE SAVED AND RENDERED; NOT YET PASSED',flush=True);os._exit(0)

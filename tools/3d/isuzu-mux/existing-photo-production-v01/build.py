"""Milestone 1: authored primary sections and independent bonnet/glazing, not an old body generator."""
import bpy,bmesh,math,ast,json,sys,hashlib,os
from pathlib import Path
from mathutils import Vector,kdtree
P=Path(__file__).resolve().parents[4];B=P/'tools/3d/isuzu-mux';R=B/'code-generator/renders/existing-photo-production-v01';R.mkdir(parents=True,exist_ok=True)
T=ast.parse((P/'tools/blender-addons/toli_mux_generator/parameters.py').read_text());D=next(ast.literal_eval(n.value) for n in T.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='BASE' for t in n.targets))
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
cols={}
for name in ['M1_PRIMARY_BODY','M1_GREENHOUSE','M1_WHEEL_FRAMEWORK','M1_REFERENCES']:
 c=bpy.data.collections.new(name);s.collection.children.link(c);cols[name]=c

def mat(name,value):
 m=bpy.data.materials.new(name);m.diffuse_color=(value,value,value,1);m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=m.diffuse_color;m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.55;return m
clay=mat('M1 neutral clay',.30);glass=mat('M1 glazing diagnostic charcoal',.075);rubber=mat('M1 wheel anchor clay',.08);wheelmat=mat('M1 plain wheel volume',.19)

def mesh(name,vs,fs,col,material,sub=0,mirror=False,skin=False):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);cols[col].objects.link(o);me.materials.append(material)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for f in me.polygons:f.use_smooth=True
 if mirror:
  m=o.modifiers.new('One authored side, shared centreline','MIRROR');m.use_axis[0]=False;m.use_axis[1]=True;m.use_clip=True;m.merge_threshold=.00001
 if sub:
  m=o.modifiers.new('Primary surface evaluation','SUBSURF');m.levels=m.render_levels=sub
 if skin:
  m=o.modifiers.new('Primary panel return thickness','SOLIDIFY');m.thickness=.006;m.offset=-1
 o['milestone']='PRIMARY EXTERIOR ONLY';o['production_approved']=False
 return o

def grid(name,rows,col,material,sub=2,mirror=True,skin=False,caps=False):
 vs=[tuple(v) for row in rows for v in row];n=len(rows[0]);fs=[]
 for i in range(len(rows)-1):
  for j in range(n-1):a=i*n+j;fs.append((a,a+n,a+n+1,a+1))
 if caps:
  assert n%2==0
  for row,reverse in [(0,True),(len(rows)-1,False)]:
   ids=[row*n+j for j in range(n)];center=sum((Vector(vs[i]) for i in ids),Vector())/n;ci=len(vs);vs.append(tuple(center))
   for j in range(0,n,2):
    face=(ci,ids[j],ids[(j+1)%n],ids[(j+2)%n]);fs.append(tuple(reversed(face)) if reverse else face)
 return mesh(name,vs,fs,col,material,sub,mirror,skin)

def at(table,x):
 if x<=table[0][0]:return table[0][1:]
 for a,b in zip(table,table[1:]):
  if a[0]<=x<=b[0]:
   t=(x-a[0])/(b[0]-a[0]);return [av+(bv-av)*t for av,bv in zip(a[1:],b[1:])]
 return table[-1][1:]

# Explicit, regional authored section intentions: X, deck Z, shoulder Z, half-width.
BODY=[(-2.4125,.98,.90,.79),(-2.40,1.00,.92,.81),(-2.30,1.06,.98,.88),(-2.16,1.115,1.04,.91),(-1.95,1.17,1.095,.925),(-1.4225,1.235,1.16,.93),(-1.02,1.265,1.205,.915),(-.84,1.285,1.24,.90),(-.52,1.275,1.25,.895),(.25,1.27,1.25,.90),(1.05,1.265,1.245,.92),(1.4225,1.25,1.23,.93),(1.83,1.235,1.23,.93),(2.06,1.22,1.20,.91),(2.29,1.15,1.11,.88),(2.40,1.04,1.00,.82),(2.4125,1.02,.98,.80)]
# Arch offsets are authored relative to hard axle anchors; no silhouette-derived wheelbase fit.
ARCH=[(-.51,.40),(-.47,.49),(-.38,.69),(-.22,.82),(0,.86),(.22,.82),(.38,.69),(.47,.49),(.51,.40)]
xs=sorted(set([row[0] for row in BODY]+[ax+dx for ax in [-D['wheelbase']/2,D['wheelbase']/2] for dx,z in ARCH]));filtered=[]
for x in xs:
 if not filtered or x-filtered[-1]>.045 or abs(x)>2.39:filtered.append(x)
rows=[]
for x in filtered:
 deck,shoulder,w=at(BODY,x);lip=.40
 for ax in [-D['wheelbase']/2,D['wheelbase']/2]:
  if abs(x-ax)<=.51:lip=max(lip,at(ARCH,x-ax)[0])
 underside=.30
 rows.append([(x,0,deck-.026),(x,.30,deck-.028),(x,w*.64,deck-.033),(x,w*.81,deck-.049),(x,w*.91,shoulder+.045),(x,w,shoulder),(x,w,max(lip+.075,shoulder-.14)),(x,w-.004,lip+.027),(x,w-.032,lip),(x,.63,lip-.018),(x,.63,underside),(x,0,underside)])
body=grid('AUTHORED_main_body_front_fenders_rear_quarters',rows,'M1_PRIMARY_BODY',clay,caps=True)
# The bonnet is an independently authored compound panel, not the upper face of a global body equation.
HOOD=[(-2.23,1.105,.655),(-2.20,1.115,.67),(-2.02,1.17,.71),(-1.74,1.225,.735),(-1.43,1.265,.75),(-1.15,1.285,.755),(-.92,1.298,.746),(-.865,1.305,.735)]
rows=[]
for x,z,w in HOOD:rows.append([(x,0,z),(x,w*.35,z-.004),(x,w*.70,z-.012),(x,w*.91,z-.024),(x,w,z-.047)])
hood=grid('AUTHORED_compound_bonnet',rows,'M1_PRIMARY_BODY',clay,skin=True)
# Continuous greenhouse volume supplies cowl/root and D-pillar structure; no isolated tab strips.
CABIN=[(-.89,1.285,.72,1.24),(-.85,1.325,.72,1.245),(-.67,1.52,.68,1.25),(-.38,1.78,.645,1.25),(-.29,1.835,.64,1.25),(.10,1.86,.645,1.25),(.70,1.86,.65,1.25),(1.27,1.845,.655,1.245),(1.68,1.815,.66,1.24),(1.89,1.735,.665,1.23),(2.07,1.54,.70,1.22),(2.25,1.27,.76,1.20),(2.27,1.245,.76,1.195)]
rows=[]
for x,top,tw,belt in CABIN:
 belt-=.085
 rows.append([(x,0,top),(x,tw*.52,top-.008),(x,tw,top-.032),(x,.76,max(belt+.018,top-.13)),(x,.80,belt),(x,0,belt)])
cabin=grid('AUTHORED_greenhouse_roof_A_and_D_structure',rows,'M1_GREENHOUSE',clay,caps=True)

def cabin_y(x,z):
 top,tw,belt=at(CABIN,x);upper=top-.032
 if z>=upper:return tw
 shoulder=max(belt+.018,top-.13)
 if z>=shoulder:return tw+(.76-tw)*(upper-z)/max(upper-shoulder,.001)
 return .76+(.80-.76)*(shoulder-z)/max(shoulder-belt,.001)

def sideglass(name,corners):
 rows=[]
 for i in range(5):
  t=i/4;a=Vector(corners[0]).lerp(Vector(corners[1]),t);b=Vector(corners[3]).lerp(Vector(corners[2]),t);row=[]
  for j in range(5):
   x,z=a.lerp(b,j/4);row.append((x,cabin_y(x,z)+.008,z))
  rows.append(row)
 o=grid(name,rows,'M1_GREENHOUSE',glass,skin=True)
 # Finite crease preserves the visual envelope without unbounded subdivision shrink.
 a=o.data.attributes.new('crease_edge','FLOAT','EDGE');counts={tuple(sorted(e.vertices)):0 for e in o.data.edges}
 for f in o.data.polygons:
  for e in f.edge_keys:counts[tuple(sorted(e))]+=1
 for e in o.data.edges:
  if counts[tuple(sorted(e.vertices))]==1:a.data[e.index].value=.65
 return o
sideglass('AUTHORED_front_side_window',[(-.735,1.32),(-.265,1.765),(.31,1.77),(.335,1.295)])
sideglass('AUTHORED_rear_side_window',[(.405,1.295),(.385,1.77),(1.18,1.745),(1.225,1.285)])
sideglass('AUTHORED_quarter_glass',[(1.305,1.285),(1.28,1.725),(1.82,1.675),(2.045,1.30)])
rows=[]
for t in [0,.15,.5,.85,1]:
 x=-.87+.49*t;z=1.315+.466*t;w=.715-.085*t;rows.append([(x-.024*(1-u*u),w*u,z+.012*(1-u*u)) for u in [0,.25,.5,.75,1]])
grid('AUTHORED_windscreen',rows,'M1_GREENHOUSE',glass,skin=True)
rows=[]
for t in [0,.15,.5,.85,1]:
 x=2.24-.29*t;z=1.30+.38*t;w=.705-.07*t;rows.append([(x+.014*(1-u*u),w*u,z+.008*(1-u*u)) for u in [0,.25,.5,.75,1]])
grid('AUTHORED_rear_glass',rows,'M1_GREENHOUSE',glass,skin=True)
# Grounded repeated wheel volumes; no identity detailing.
centres={}
for axle,x in [('FRONT',-D['wheelbase']/2),('REAR',D['wheelbase']/2)]:
 for side,y in [('NEGATIVE_Y',-D['track']/2),('POSITIVE_Y',D['track']/2)]:
  vs=[];fs=[];profile=[(.245,-.12),(.34,-.12),(.382,-.09),(.382,.09),(.34,.12),(.245,.12)];N=64
  for i in range(N):
   th=2*math.pi*i/N
   for radius,dy in profile:vs.append((x+radius*math.cos(th),y+dy,D['tire_diameter']/2+radius*math.sin(th)))
  for i in range(N):
   for j in range(6):fs.append((i*6+j,((i+1)%N)*6+j,((i+1)%N)*6+(j+1)%6,i*6+(j+1)%6))
  o=mesh('ANCHOR_'+axle+'_'+side+'_TIRE',vs,fs,'M1_WHEEL_FRAMEWORK',rubber);centres[o.name]=[x,y,D['tire_diameter']/2]
  vs=[];fs=[]
  for dy in [-.121,.121]:
   vs.extend([(x+.246*math.cos(2*math.pi*i/N),y+dy,D['tire_diameter']/2+.246*math.sin(2*math.pi*i/N)) for i in range(N)])
  for i in range(N):j=(i+1)%N;fs.append((i,j,j+N,i+N))
  for offset,dy in [(0,-.121),(N,.121)]:
   ci=len(vs);vs.append((x,y+dy,D['tire_diameter']/2))
   for i in range(N):fs.append((ci,offset+i,offset+(i+1)%N))
  mesh('PLAIN_'+axle+'_'+side+'_WHEEL',vs,fs,'M1_WHEEL_FRAMEWORK',wheelmat)
s['nominal_framework']=json.dumps(D);s['wheel_centres']=json.dumps(centres);s['branch']='Existing-photo visual candidate V01 / milestone 1';s['approved']=False
# Seat regional skins on their own authored host; this is interface construction, not photo-derived depth.
for o in cols['M1_GREENHOUSE'].objects:
 if o==cabin:continue
 wrap=o.modifiers.new('Seat glazing on authored greenhouse','SHRINKWRAP');wrap.target=cabin;wrap.wrap_method='NEAREST_SURFACEPOINT';wrap.offset=.003
 index=list(o.modifiers).index(wrap);o.modifiers.move(index,index-1)
vg=hood.vertex_groups.new(name='Bonnet perimeter interface')
vg.add([v.index for v in hood.data.vertices if v.index<5 or v.index>=35 or v.index%5==4],1.,'REPLACE')
wrap=hood.modifiers.new('Seat bonnet perimeter only','SHRINKWRAP');wrap.target=body;wrap.vertex_group=vg.name;wrap.offset=.001
hood.modifiers.move(len(hood.modifiers)-1,1)
# Local originals are linked as non-rendered image references; not projected onto the body.
for view,time in [('front','18-17-10'),('front34','18-17-27'),('side','18-17-14'),('rear34','18-17-31'),('rear','18-17-18')]:
 im=bpy.data.images.load(str(P.parent/'Isuzu MU-X'/f'Screenshot From 2026-11-06 {time}.png'));o=bpy.data.objects.new('REFERENCE_'+view,None);cols['M1_REFERENCES'].objects.link(o);o.empty_display_type='IMAGE';o.data=im;o.hide_render=True;o.hide_viewport=True
# Save the actual primary-surface milestone before studio tooling.
source=B/'source/production/isuzu-mux-existing-photo-production-v01.blend';milestone=B/'source/production/milestones/isuzu-mux-existing-photo-primary-surfaces-v01.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(milestone))
sys.path.insert(0,str(P/'tools/blender-addons'))
from toli_mux_generator.surface_diagnostics import setup
setup(s)
VIEWS={'FRONT':(-9,0,1.2),'FRONT34':(-7,-7,3),'SIDE':(0,-9,1.2),'REAR34':(7,-7,3),'REAR':(9,0,1.2)}
for name,pos in VIEWS.items():
 d=bpy.data.cameras.new('M1_CAM_'+name);o=bpy.data.objects.new('M1_CAM_'+name,d);s.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,.93))-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=6.1
s.camera=bpy.data.objects['M1_CAM_FRONT34'];bpy.ops.wm.save_as_mainfile(filepath=str(source))
print('PRIMARY SURFACE MASTER SAVED',source,flush=True);os._exit(0)

"""Fresh reference-guided patch cage. Does NOT load or read any previous body mesh.
Run with: blender -b -t 2 --python tools/3d/isuzu-mux/source/authored/build-authored-v01.py
"""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];OUT=R/'renders/authored-v01';OUT.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene;sc.unit_settings.system='METRIC'
sc['method']='NEW AUTHORED BODY / NOT PASS-3 DEFORMATION';sc['coordinates']='metres, +X front, +Y left, +Z up; floor 0'
sc['scale']='Estimated 2.85m wheelbase, .39m tire radius, 1.66m track; photographic constraints not engineering dimensions'
def mat(name,c,metal=0,rough=.4):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
paint=mat('Neutral evaluation silver',(.35,.38,.41),.7,.24);glass=mat('Study glass',(.028,.043,.050),.05,.23);glass.node_tree.nodes['Principled BSDF'].inputs['Transmission Weight'].default_value=.06;glass.node_tree.nodes['Principled BSDF'].inputs['IOR'].default_value=1.05
dark=mat('Study graphite',(.023,.026,.03),0,.6);rubber=mat('Tire envelope',(.015,.017,.019),0,.8)
refs=bpy.data.collections.new('REFERENCE_RIG');sc.collection.children.link(refs)
refsets={'REF_FRONT':['18-09-21'],'REF_LEFT':['18-09-40'],'REF_RIGHT':['18-10-06'],'REF_REAR':['18-09-48'],'REF_FRONT_3Q':['18-17-27','18-17-25'],'REF_REAR_3Q':['18-17-31','18-17-35'],'REF_OPEN_PANELS':['18-09-21','18-09-40','18-09-48','18-10-06']}
for label,times in refsets.items():
 c=bpy.data.collections.new(label);refs.children.link(c)
 for i,t in enumerate(times):
  p=Path('/home/thunder/Pictures/Screenshots')/f'Screenshot From 2026-11-06 {t}.png';im=bpy.data.images.load(str(p),check_existing=True);im.pack();o=bpy.data.objects.new(label+'_'+str(i),None);c.objects.link(o);o.empty_display_type='IMAGE';o.data=im;o.empty_display_size=5.0;o.location=((2.7,0,1) if label=='REF_FRONT' else (-2.7,0,1) if label=='REF_REAR' else (0,-1.3,1) if label=='REF_RIGHT' else (0,1.3+i*.1,1));o.rotation_euler=(math.pi/2,0,math.pi/2 if label=='REF_FRONT' else -math.pi/2 if label=='REF_REAR' else math.pi if label=='REF_RIGHT' else 0);o.color[3]=.4;o.hide_render=True;o['role']='Canonical' if t.startswith('18-09') or t=='18-10-06' else 'Secondary compatible view only'
refs.hide_render=True;refs.hide_viewport=True
curvecol=bpy.data.collections.new('LANDMARK_CURVES / STATIONS');sc.collection.children.link(curvecol)
def curve(name,pts):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for p,co in zip(s.points,pts):p.co=(*co,1)
 ob=bpy.data.objects.new(name,c);curvecol.objects.link(ob);ob.hide_render=True;return ob
# Fresh independently specified section controls, not extracted from the prior cage.
sections=[('S13 rear bumper',-2.38,.85),('S12 hatch/lamp',-2.20,.91),('S11 rear quarter',-1.90,.95),('S10 rear axle',-1.425,.96),('S09 rear door',-1.0,.928),('S08 B pillar',-.46,.921),('S07 front door',-.05,.921),('S06 A/cabin',.35,.929),('S05 cowl',1.07,.939),('S04 bonnet rear',1.15,.946),('S03 front axle',1.425,.966),('S02 grille/lamp',2.10,.922),('S01 front bumper',2.25,.867)]
def interp(x,data):
 for (a,v),(b,w) in zip(data,data[1:]):
  if a<=x<=b:return v+(w-v)*(x-a)/(b-a)
 return data[0 if x<data[0][0] else -1][1]
def width(x):return interp(x,[(x,w) for _,x,w in sections])
def belt(x):return 1.18-.012*x
roofnodes=[(-2.04,.75,1.75),(-1.36,.755,1.79),(-.46,.75,1.80),(.35,.73,1.76)]
def roofz(x):return interp(x,[(x,z) for x,y,z in roofnodes])
def roofy(x):return interp(x,[(x,y) for x,y,z in roofnodes])
def sidey(x,z):
 t=max(0,min(1,(z-belt(x))/(roofz(x)-belt(x))))
 return .855+(roofy(x)-.855)*t+.008*math.sin(t*math.pi)
def side(x,z):return (x,sidey(x,z),z)
# Reference-specific guide contours; rear/front arches deliberately differ.
frontarch=[(.93,.35),(.98,.59),(1.13,.79),(1.39,.87),(1.61,.84),(1.80,.66),(1.91,.35)]
reararch=[(-1.91,.35),(-1.85,.61),(-1.69,.80),(-1.43,.865),(-1.18,.81),(-1.02,.61),(-.95,.35)]
for name,pts in {'SIDE_ROOF':[(x,y,z) for x,y,z in roofnodes],'SIDE_BONNET':[(1.07,0,1.225),(1.425,0,1.23),(1.90,0,1.19),(2.25,0,1.13)],'SIDE_BELT':[side(x,belt(x)) for _,x,w in sections],'SIDE_SHOULDER':[(x,width(x),belt(x)-.07) for _,x,w in sections],'SIDE_ROCKER':[(-2.38,.84,.35),(0,.87,.35),(2.25,.84,.35)],'WINDSCREEN_SIDE':[side(1.07,belt(1.07)),side(.35,1.76)],'FRONT_ARCH':[(x,.96,z) for x,z in frontarch],'REAR_ARCH':[(x,.96,z) for x,z in reararch],'FRONT_BUMPER':[(2.28,0,.35),(2.30,.55,.55),(2.25,.87,.75)],'REAR_BUMPER':[(-2.40,0,.35),(-2.42,.55,.55),(-2.38,.85,.80)],'GRILLE_BOUNDARY':[(2.25,0,1.04),(2.23,.58,1.04),(2.27,.52,.72),(2.28,0,.72)],'HEADLIGHT_BOUNDARY':[(2.23,.59,1.06),(2.12,.89,1.16),(2.16,.90,.96),(2.25,.60,.96)],'FRONT_ROOF_WIDTH':[(.35,0,1.795),(.35,.73,1.76)],'REAR_GLASS': [(-2.34,0,1.25),(-2.12,.67,1.65),(-2.07,0,1.74)],'REAR_LAMP': [(-2.25,.85,1.23),(-2.26,.88,.98),(-2.35,.60,1.05)],'REAR_TAILGATE':[(-2.38,0,.72),(-2.36,.74,1.20),(-2.04,.75,1.75)],'REAR_SHOULDER':[(-2.20,.91,1.12),(-1.90,.95,1.13)]}.items():curve(name,pts)
V=[];F=[];M=[];groups=[]
EDGE=[0,.08,.25,.5,.75,.92,1]
def addpatch(name,vs,fs,material=0):
 offset=len(V);V.extend(vs);F.extend(tuple(offset+i for i in f) for f in fs);M.extend([material]*len(fs));groups.append((name,len(vs),len(fs)))
def grid(name,rows,material=0):
 n=len(rows[0]);addpatch(name,[p for row in rows for p in row],[(i*n+j,(i+1)*n+j,(i+1)*n+j+1,i*n+j+1) for i in range(len(rows)-1) for j in range(n-1)],material)
# A — Main side volume; guide x locations make lower sill/frame boundaries explicit.
cells=[[(1.07,belt(1.07)),(.35,1.76),(-.46,1.80),(-.46,belt(-.46))],[(-.46,belt(-.46)),(-.46,1.80),(-1.36,1.79),(-1.36,belt(-1.36))],[(-1.36,belt(-1.36)),(-1.36,1.79),(-2.04,1.75),(-2.38,belt(-2.38))]]
xs=set(x for _,x,w in sections)
for points in [frontarch,reararch]:xs.update(x for x,z in points)
for q in cells:
 for t in EDGE:xs.add(q[0][0]+(q[3][0]-q[0][0])*t)
xs.update([1.07,1.425,1.7,1.95,2.10,2.25]);xs=sorted(xs)
side_rows=[]
for x in xs:
 w=width(x);b=belt(x)
 # Build broad volume first; wheel opening modifies only the lower three rows later.
 side_rows.append([(x,w-.075,.35),(x,w-.018,.385),(x,w+.005,.68),(x,w-.008,b-.075),(x,.855,b)])
for label,x,w in sections:
 b=belt(x);curve(label,[(x,0,.35),(x,w-.075,.35),(x,w,.68),(x,w-.008,b-.075),(x,.855,b),(x,roofy(x),roofz(x))])
# B — Cabin constructed around new explicit polygonal window perimeters, never old topology.
innerquads=[[(.925,1.235),(.315,1.705),(-.397,1.738),(-.397,1.245)],[(-.523,1.245),(-.523,1.738),(-1.286,1.724),(-1.286,1.26)],[(-1.444,1.27),(-1.444,1.724),(-1.965,1.672),(-2.10,1.29)]]
windowfaces=[]
for cell,(outer,inner) in enumerate(zip(cells,innerquads)):
 curve('SIDE_GLASS_'+str(cell),[side(x,z) for x,z in inner+[inner[0]]])
 ol=[];il=[]
 for k in range(4):
  a=Vector(outer[k]);b=Vector(outer[(k+1)%4])
  for t in EDGE[:-1]:ol.append(side(*(a.lerp(b,t))))
  a=Vector(inner[k]);prev=Vector(inner[(k-1)%4]);nxt=Vector(inner[(k+1)%4]);p=a.lerp(prev,.08);q=a.lerp(nxt,.08)
  # Two rounded-corner samples plus edge samples, sixteen constraints per loop.
  for v in [p,p*.444+a*.444+q*.112,p*.112+a*.444+q*.444,q,q.lerp(nxt.lerp(a,.08),1/3),q.lerp(nxt.lerp(a,.08),2/3)]:il.append(side(*v))
 vs=ol+il;fs=[(k,(k+1)%24,(k+1)%24+24,k+24) for k in range(24)]
 addpatch('CABIN_FRAME_'+str(cell),vs,fs)
 start=len(F);center=tuple(sum(p[k] for p in il)/24 for k in range(3));addpatch('GLASS_REGION_'+str(cell),il+[center],[(k,(k+1)%24,24) for k in range(24)],1);windowfaces.append(start)
# Roof patch follows the cabin's actual outer top edges, with a mild transverse crown.
ux=[0,.4,.75,.93,1]
rx=[]
for a,b in zip(roofnodes,roofnodes[1:]):
 for t in EDGE[:-1]:rx.append(tuple(Vector(a).lerp(Vector(b),t)))
rx.append(roofnodes[-1]);grid('ROOF', [[(x,y*u,z+.035*(1-u*u)) for u in ux] for x,y,z in rx])
# C — Bonnet/cowl; same base edge as fresh windscreen, controlled shallow crown.
hx=[x for x in xs if x>=1.07]
def hood(x,u):return (x,.855*u,belt(x)+(.045 if x<1.5 else .035)*(1-u*u))
grid('BONNET_COWL',[[hood(x,u) for u in ux] for x in hx])
# Windscreen and hatch are structured half-grids: no overlapping sheet or center pillar.
def glazing(name,base,top,rear=False):
 rows=[];vv=EDGE
 for t in vv:
  row=[]
  for u in ux:
   p=Vector(base(u)).lerp(Vector(top(u)),t);p.x+=(-1 if rear else 1)*.018*math.sin(math.pi*t)*(1-u*u);edge=Vector(base(1)).lerp(Vector(top(1)),t);p.y=sidey(edge.x,edge.z)*u;row.append(tuple(p))
  rows.append(row)
 start=len(F);grid(name,rows)
 for i in range(6):
  for j in range(4):
   if i in [1,2,3,4] and j<3:M[start+i*4+j]=1
 curve(name+'_OUTLINE',[rows[0][0],rows[0][-1],rows[-1][-1],rows[-1][0],rows[0][0]])
glazing('WINDSCREEN',lambda u:hood(1.07,u),lambda u:(.35,.73*u,1.76+.035*(1-u*u)))
glazing('REAR_GLASS_HATCH',lambda u:(-2.38,.855*u,belt(-2.38)+.035*(1-u*u)),lambda u:(-2.04,.75*u,1.75+.035*(1-u*u)),True)
# D/E — front and rear volume are independently controlled by the named section widths.
# H — Shape distinct openings only after the side volume has been established.
for i,x in enumerate(xs):
 low=.35
 for arch in [frontarch,reararch]:
  if arch[0][0]<=x<=arch[-1][0]:low=max(low,interp(x,arch))
 w=width(x);b=belt(x)
 side_rows[i]=[(x,w-.075,low),(x,w-.018,low+.025),(x,w+.005,low+(b-.075-low)*.46),(x,w-.008,b-.075),(x,.855,b)]
grid('SIDE_FENDER_QUARTER',side_rows)
# F/G — quad transfinite closure, no visible radial cap pole. Multiple depth planes.
def cap(name,edge,top,front):
 sgn=1 if front else -1;xc=edge[0][0];rows=[];vs=[0,.16,.48,.80,1]
 B0=Vector((xc+sgn*.02,0,edge[0][2]));B1=Vector(edge[0]);T0=Vector(top(0));T1=Vector(top(1))
 for i,t in enumerate(vs):
  E=Vector(edge[i]);C=Vector((xc+sgn*[.02,.06,.015,-.04,0][i],0,B0.z+(T0.z-B0.z)*t));row=[]
  for u in ux:
   bottom=B0.lerp(B1,u);upper=Vector(top(u));bilinear=B0*(1-u)*(1-t)+B1*u*(1-t)+T0*(1-u)*t+T1*u*t
   p=bottom*(1-t)+upper*t+C*(1-u)+E*u-bilinear;row.append(tuple(p))
  rows.append(row)
 grid(name,rows)
cap('FRONT_MAJOR_VOLUME',side_rows[-1],lambda u:hood(2.25,u),True)
cap('REAR_BUMPER_MAJOR_VOLUME',side_rows[0],lambda u:(-2.38,.855*u,belt(-2.38)+.035*(1-u*u)),False)
# Assemble freshly authored patches; weld coincident boundary vertices, preserve half-body.
me=bpy.data.meshes.new('AUTHORED_HALF_CAGE_V01');me.from_pydata(V,[],F);me.materials.clear()
for m in [paint,glass,dark]:me.materials.append(m)
for p,m in zip(me.polygons,M):p.material_index=m;p.use_smooth=True
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
body=bpy.data.objects.new('AUTHORED_BODY_V01',me);sc.collection.objects.link(body)
# Make side normals outward before applying symmetry.
p=next(p for p in me.polygons if p.center.y>.9 and abs(p.center.x)<.5)
if p.normal.y<0:
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
assert all(v.co.y>=-1e-6 for v in me.vertices)
mirror=body.modifiers.new('Centerline symmetry Y','MIRROR');mirror.use_axis[0]=False;mirror.use_axis[1]=True;mirror.use_clip=True
sub=body.modifiers.new('Single diagnostic subdivision','SUBSURF');sub.levels=1;sub.render_levels=1
body['method']='Fresh authored patch network; no prior body copied, shrinkwrapped or loaded';body['patch_inventory']=json.dumps(groups)
# Fresh tire measurement envelopes only; no previous mesh reused.
for x,a in [(1.425,'F'),(-1.425,'R')]:
 for y,s in [(.83,'L'),(-.83,'R')]:
  vs=[];fs=[]
  for off,rad in [(-.13,.29),(-.13,.35),(-.10,.39),(.10,.39),(.13,.35),(.13,.29)]:
   for k in range(32):v=k*math.tau/32;vs.append((x+rad*math.sin(v),y+off,.39+rad*math.cos(v)))
  for j in range(5):
   for k in range(32):fs.append((j*32+k,j*32+(k+1)%32,(j+1)*32+(k+1)%32,(j+1)*32+k))
  mm=bpy.data.meshes.new('TIRE_'+a+s);mm.from_pydata(vs,[],fs);o=bpy.data.objects.new(mm.name,mm);sc.collection.objects.link(o);mm.materials.append(rubber)
  for p in mm.polygons:p.use_smooth=True
  bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.27,depth=.24,location=(x,y,.39),rotation=(math.pi/2,0,0));bpy.context.object.name='RIM_STUDY_'+a+s;bpy.context.object.data.materials.append(dark)
# Studio with long rectangular reflection sources. No texture, badge or HDRI likeness shortcuts.
floor=mat('Evaluation floor',(.11,.12,.14),0,.65);bpy.ops.mesh.primitive_plane_add(size=200);bpy.context.object.name='STUDIO_FLOOR';bpy.context.object.data.materials.append(floor)
sc.world=bpy.data.worlds.new('Neutral world');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.2,.2,.2,1)
for name,pos,power,sizex,sizey in [('STRIP_KEY',(3,4,5),1600,6,.7),('STRIP_SIDE',(-2,-4,3.5),1100,5,.5),('ROOF_SOFT',(0,1,7),1400,6,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='RECTANGLE';o.data.size=sizex;o.data.size_y=sizey;o.rotation_euler=(Vector((0,0,.95))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='REFERENCE_COMPARISON_CAMERA';cam.data.lens=70;sc.camera=cam
views={'front':(10,0,1.65),'left':(1.0,10.5,1.8),'right':(1.0,-10.5,1.8),'rear':(-10,0,1.65),'front-three-quarter':(8,6,2.8),'rear-three-quarter':(-8,6,2.8)}
for name,pos in views.items():
 c=bpy.data.cameras.new('CAL_'+name);ob=bpy.data.objects.new('CAL_'+name,c);sc.collection.objects.link(ob);ob.location=pos;ob.rotation_euler=(Vector((0,0,.95))-ob.location).to_track_quat('-Z','Y').to_euler();c.lens=70;ob['calibration']='Estimated, not solved. Approximate matching from wheel centers/diameter. No calibrated lens metadata.'
(R/'source/authored/camera-estimates.json').write_text(json.dumps({'views':views,'lens_mm':70,'target':[0,0,.95],'status':'Estimated only; no exact calibration PASS claimed'},indent=2))
sc.render.engine='CYCLES';sc.cycles.samples=6;sc.render.resolution_x=1000;sc.render.resolution_y=650;sc.render.resolution_percentage=100
cam.location=views['front-three-quarter'];cam.rotation_euler=(Vector((0,0,.95))-cam.location).to_track_quat('-Z','Y').to_euler()
curvecol.hide_render=True;curvecol.hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/authored/isuzu-mux-authored-v01.blend'))
# Statistics distinguish body cage from evaluated scene geometry.
d=bpy.context.evaluated_depsgraph_get();stats={'body_base_vertices':len(me.vertices),'body_base_faces':len(me.polygons),'evaluated_vertices':0,'evaluated_triangles':0,'production_textures':0,'method':sc['method'],'checkpoints':'Pending visual review'}
for o in sc.objects:
 if o.type=='MESH' and o.name!='STUDIO_FLOOR':
  ev=o.evaluated_get(d);m=ev.to_mesh();m.calc_loop_triangles();assert all(math.isfinite(c) for v in m.vertices for c in v.co);stats['evaluated_vertices']+=len(m.vertices);stats['evaluated_triangles']+=len(m.loop_triangles);ev.to_mesh_clear()
bm=bmesh.new();bm.from_mesh(me);unseen=set(bm.faces);components=0
while unseen:
 components+=1;stack=[unseen.pop()]
 while stack:
  for e in stack.pop().edges:
   for f in e.link_faces:
    if f in unseen:unseen.remove(f);stack.append(f)
stats['body_edge_connected_face_components']=components;stats['body_boundary_edges']=sum(e.is_boundary for e in bm.edges);bm.free()
(R/'source/authored/statistics-v01.json').write_text(json.dumps(stats,indent=2))
# Basic-volume grey override is a checkpoint render, not approval of subsequent stages.
grey=mat('CHECKPOINT_A_GREY',(.34,.36,.38),.1,.45);sc.view_layers[0].material_override=grey
# Checkpoint renders are generated by inspect-authored-v01.py.

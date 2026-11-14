import bpy,bmesh,math,json,os
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux')
OUT=Path(os.environ.get('MUX_GREENHOUSE_OUTPUT',Path(__file__).resolve().parents[3]));D=OUT/'source/reconstruction';R=OUT/'renders';A=D/'greenhouse-v02';A.mkdir(parents=True,exist_ok=True);R.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'source/reconstruction/isuzu-mux-reference-constrained-v01.blend'));s=bpy.context.scene
def signature(ob):return {'name':ob.name,'matrix':[list(r) for r in ob.matrix_world],'vertices':[list(v.co) for v in ob.data.vertices] if ob.type=='MESH' else []}
keep=[o for o in bpy.data.objects if (o.type=='MESH' and any(m and m.name in ['Stance tire proxy','Stance wheel proxy'] for m in o.data.materials)) or o.name in ['Front axle','Rear axle','Centerline']]
frozen=[signature(o) for o in keep]
for ob in list(bpy.data.objects):
 if ob not in keep:bpy.data.objects.remove(ob,do_unlink=True)
def material(name,c,rough=.3,metal=.0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
clay=material('Diagnostic neutral cabin',(.48,.49,.50),.35);glass=material('Diagnostic opaque glass — curvature only',(.055,.075,.085),.18);gridmat=material('Cross section lines',(.8,.19,.025));body=[]
def mesh(name,v,f,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 body.append(ob);return ob
def patch(name,fn,nu=12,nv=8,mat=clay):
 vs=[fn(i/nu,j/nv) for i in range(nu+1) for j in range(nv+1)];fs=[(i*(nv+1)+j,(i+1)*(nv+1)+j,(i+1)*(nv+1)+j+1,i*(nv+1)+j+1) for i in range(nu) for j in range(nv)];return mesh(name,vs,fs,mat)
def curve(name,pts,r=.0008,mat=gridmat,hide=True):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=1;sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,q in zip(sp.points,pts):p.co=(*q,1)
 ob=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat);ob.hide_render=hide;return ob
def mix(a,b,t):return tuple((1-t)*x+t*y for x,y in zip(a,b))
def bez(a,b,c,d,t):return tuple((1-t)**3*x+3*(1-t)**2*t*y+3*(1-t)*t*t*z+t**3*w for x,y,z,w in zip(a,b,c,d))
def bz(ps):return lambda t:bez(*ps,t)
# Eleven explicit cross-car controls, wheelbase-normalized; no manufacturer's metre scale inferred.
# x, roof-side half-width, upper-edge z, lower-side half-width, lower-edge z, transverse crown
stations=[[-.405,.287,.438,.306,.421,.006],[-.29,.270,.522,.305,.426,.017],[-.155,.250,.592,.306,.431,.021],[-.075,.250,.609,.307,.435,.015],[.015,.251,.612,.308,.439,.014],[.092,.252,.613,.309,.442,.014],[.255,.253,.612,.309,.451,.014],[.438,.251,.607,.307,.462,.014],[.535,.247,.600,.304,.468,.014],[.630,.244,.580,.300,.465,.016],[.720,.280,.447,.296,.445,.006]]
names=['windscreen base/cowl','lower A-pillar','upper A-pillar','front roof','front-door cabin','B-pillar','rear-door cabin','C-pillar','quarter glass','D-pillar','rear glass']
def interp(x,k):
 x=max(stations[0][0],min(stations[-1][0],x));idx=min(next((i for i in range(len(stations)-1) if x<=stations[i+1][0]),len(stations)-2),len(stations)-2);a=stations[idx];b=stations[idx+1];t=(x-a[0])/(b[0]-a[0]);delta=b[0]-a[0]
 def slope(i):
  l=max(0,i-1);r=min(len(stations)-1,i+1);return (stations[r][k]-stations[l][k])/(stations[r][0]-stations[l][0])
 return (2*t**3-3*t*t+1)*a[k]+(t**3-2*t*t+t)*delta*slope(idx)+(-2*t**3+3*t*t)*b[k]+(t**3-t*t)*delta*slope(idx+1)
def sidept(x,z,side):
 bottom=interp(x,4);top=interp(x,2);t=max(0,min(1,(z-bottom)/max(.02,top-bottom)));y=(1-t)*interp(x,3)+t*interp(x,1)+.0025*math.sin(math.pi*t);return(x,side*y,z)
def roofpt(x,t):return(x,interp(x,1)*t,interp(x,2)+interp(x,5)*(1-t*t))
roof=patch('Longitudinal and transverse roof crown',lambda u,v:roofpt(-.075+u*.705,2*v-1),24,12)
for n,row in enumerate(stations,1):
 x=row[0];pts=[sidept(x,row[4]+(row[2]-row[4])*j/6,-1) for j in range(7)];pts += [roofpt(x,-1+2*j/16) for j in range(1,17)];pts += [sidept(x,row[2]-(row[2]-row[4])*j/6,1) for j in range(1,7)];curve(f'G{n:02} {names[n-1]}',pts)
(A/'stations.json').write_text(json.dumps([dict(id=f'G{i+1:02}',region=names[i],x=r[0],roof_halfwidth=r[1],upper_z=r[2],lower_halfwidth=r[3],lower_z=r[4],crown=r[5],confidence='manual reference-constrained estimate; not calibrated') for i,r in enumerate(stations)],indent=2))
s['STATUS']='DEPTH/STATION MILESTONE — not validated';bpy.ops.wm.save_as_mainfile(filepath=str(A/'milestones/depth-stations-v02.blend'))
# Curved windscreen: bowed base/header, subtle double curvature; grey corner strips are structural, not trim.
def windshield(u,v):
 t=2*u-1;w=.269*(1-v)+.238*v;z=.421*(1-v)+.587*v+.009*(1-t*t)+.002*math.sin(math.pi*v)*(1-t*t);x=-.405*(1-v)-.180*v+(.045*(1-v)+.025*v)*t*t-.009*(1-t*t)*math.sin(math.pi*v);return(x,t*w,z)
def rounded_surface(name,fn):
 # Rounded UV perimeter, concentric quad rings, one small center fan; no thick trim masks the corners.
 r=.055;uv=[]
 for cx,cy,start in [(1-r,r,-90),(1-r,1-r,0),(r,1-r,90),(r,r,180)]:
  for j in range(7):
   a=math.radians(start+90*j/6);uv.append((cx+r*math.cos(a),cy+r*math.sin(a)))
 # Add broad straight-edge samples between corner arcs, maintaining the same perimeter order.
 per=[]
 for i,a in enumerate(uv):
  b=uv[(i+1)%len(uv)];per.append(a)
  if math.dist(a,b)>.2:per.extend([mix(a,b,t) for t in (.25,.5,.75)])
 n=len(per);vs=[fn(.5,.5)]+[fn(*mix((.5,.5),q,t)) for t in (.25,.5,.75,1) for q in per];fs=[(0,1+i,1+(i+1)%n) for i in range(n)]
 for j in range(3):
  for i in range(n):fs.append((1+j*n+i,1+j*n+(i+1)%n,1+(j+1)*n+(i+1)%n,1+(j+1)*n+i))
 ob=mesh(name,vs,fs,glass)
 # Fill only the clipped tiny corner areas to retain the shared A/header/D boundary.
 outer=[]
 for q in per:
  t=1/max(abs(2*q[0]-1),abs(2*q[1]-1));outer.append((.5+(q[0]-.5)*t,.5+(q[1]-.5)*t))
 mesh(name+' corner support',[fn(*q) for q in per]+[fn(*q) for q in outer],[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n) if math.dist(per[i],outer[i])>1e-6 or math.dist(per[(i+1)%n],outer[(i+1)%n])>1e-6],clay)
 return ob
wind=rounded_surface('Windscreen curved surface',windshield)
for side in (-1,1):
 patch('A-pillar surface '+str(side),lambda u,v,side=side:mix(windshield(0 if side<0 else 1,v),sidept(-.360+v*.205,.421+v*.166,side),u),3,12)
def header(u,v):
 p=windshield(u,1);q=roofpt(-.075,2*u-1);a=windshield(u,.999);b=roofpt(-.074,2*u-1);m=[(p[i]-a[i])/.001*.20 for i in range(3)];n=[(b[i]-q[i])/.001*.085 for i in range(3)]
 return tuple((2*v**3-3*v*v+1)*p[i]+(v**3-2*v*v+v)*m[i]+(-2*v**3+3*v*v)*q[i]+(v**3-v*v)*n[i] for i in range(3))
patch('Windscreen header transition',header,16,8)
for side in (-1,1):
 patch('Header side supporting junction '+str(side),lambda u,v,side=side:mix(header(0 if side<0 else 1,u),sidept(header(0 if side<0 else 1,u)[0],interp(header(0 if side<0 else 1,u)[0],2),side),v),12,2)
patch('Cowl glass support only',lambda u,v:mix(windshield(u,0),(-.414,(2*u-1)*.292,.416),v),16,2)
# Each side cell has four broad outer curves and its own rounded glass boundary. They share the same 3D side field.
def coons(B,T,L,R,u,v):
 b=B(u);t=T(u);l=L(v);r=R(v);p00=B(0);p10=B(1);p01=T(0);p11=T(1)
 return tuple((1-v)*b[k]+v*t[k]+(1-u)*l[k]+u*r[k]-((1-u)*(1-v)*p00[k]+u*(1-v)*p10[k]+(1-u)*v*p01[k]+u*v*p11[k]) for k in range(2))
# Control points in x/z; no pixel-by-pixel outline fitting. Front/rear glass corners curve through Bezier boundaries.
cells=[
 ('Front side glass',
  [(-.255,.427),(-.18,.425),(-.04,.432),(.054,.440)],
  [(-.143,.560),(-.10,.575),(-.015,.584),(.048,.586)],
  [(-.255,.427),(-.271,.446),(-.196,.529),(-.143,.560)],
  [(.054,.440),(.054,.48),(.050,.55),(.048,.586)],
  (-.360,.090,-.155,.090)),
 ('Rear side glass',
  [(.125,.448),(.21,.452),(.35,.460),(.374,.478)],
  [(.115,.586),(.20,.590),(.35,.587),(.399,.582)],
  [(.125,.448),(.121,.49),(.118,.55),(.115,.586)],
  [(.374,.478),(.405,.49),(.415,.557),(.399,.582)],
  (.090,.455,.090,.455)),
 ('Upright quarter glass',
  [(.521,.479),(.555,.473),(.619,.473),(.650,.472)],
  [(.492,.574),(.52,.583),(.574,.579),(.602,.572)],
  [(.521,.479),(.502,.493),(.489,.55),(.492,.574)],
  [(.650,.472),(.642,.503),(.618,.55),(.602,.572)],
  (.455,.707,.455,.630))]
for side in (-1,1):
 for name,b,t,l,r,outer in cells:
  B,T,L,RR=map(bz,[b,t,l,r]);bl,br,tl,tr=outer
  OB=lambda u,bl=bl,br=br:(bl+(br-bl)*u,interp(bl+(br-bl)*u,4))
  OT=lambda u,tl=tl,tr=tr:(tl+(tr-tl)*u,interp(tl+(tr-tl)*u,2))
  OL=lambda v,bl=bl,tl=tl:mix((bl,interp(bl,4)),(tl,interp(tl,2)),v)
  OR=lambda v,br=br,tr=tr:mix((br,interp(br,4)),(tr,interp(tr,2)),v)
  def point(uv,side=side):return sidept(*uv,side)
  def g(u,v,B=B,T=T,L=L,RR=RR,side=side):
   x,z=coons(B,T,L,RR,u,v);p=sidept(x,z,side);return(p[0],p[1]-side*.0015*math.sin(math.pi*u)*math.sin(math.pi*v),p[2])
  patch(name+' '+str(side),g,12,8,glass)
  for label,inner,outeredge in [('lower',B,OB),('upper',T,OT),('leading',L,OL),('trailing',RR,OR)]:
   patch(name+' structural '+label+' '+str(side),lambda u,v,inner=inner,outeredge=outeredge,side=side:sidept(*mix(inner(u),outeredge(u),v),side),12,3,clay)
# Rear glass independently curved across cabin, not a terminal flat roof segment.
def rearglass(u,v):
 t=2*u-1;w=.272*(1-v)+.227*v;z=.445*(1-v)+.573*v+.008*(1-t*t);x=.722*(1-v)+.631*v-(.015*(1-v)+.001*v)*t*t+.010*(1-t*t)*math.sin(math.pi*v);return(x,t*w,z)
rounded_surface('Rear glass curved surface',rearglass)
patch('Rear header junction',lambda u,v:mix(rearglass(u,1),roofpt(.630,2*u-1),v),16,3)
for side in (-1,1):
 patch('D-pillar to rear glass '+str(side),lambda u,v,side=side:mix(rearglass(0 if side<0 else 1,v),sidept(.707-v*.077,.445+v*.135,side),u),4,12)
# Recalculate normals consistently. These are naked surface studies, not a watertight production shell.
for ob in body:
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(ob.data);bm.free()
assert [signature(o) for o in keep]==frozen,'Stance changed'
for key in ['O02','O04','O06','O07','O08','O09','O10','O11','O12','O13','S13','S19','S21']:
 path=ROOT/f'references/complete-library/{key}.png';im=bpy.data.images.load(str(path),check_existing=True);im.pack();im.use_fake_user=True
s['STATUS']='GREENHOUSE PRECISION V02 — PENDING VISUAL GATES; no other body';s['reference_family']='Unchanged canonical silver family; manual Route B';s['depth_method']='G01-G11 varying width/tumblehome/crown, curved windscreen and rear glass; no calibrated depth claim'
bpy.ops.wm.save_as_mainfile(filepath=str(A/'milestones/curved-glass-pillars-v02.blend'))
# Neutral diagnostic cameras. Reference camera matching is deliberately not claimed.
s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.display.shading.show_shadows=True;s.world.color=(.8,.8,.8);s.display.shading.background_type='WORLD';s.render.resolution_x=1100;s.render.resolution_y=750;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
views={'side':((0,-4,.335),(0,0,.335),'ORTHO',1.9),'front':((-4,0,.335),(0,0,.335),'ORTHO',1.25),'rear':((4,0,.335),(0,0,.335),'ORTHO',1.25),'front-left':((-2.4,-3,1.07),(0,0,.35),'PERSP',62),'front-right':((-2.4,3,1.07),(0,0,.35),'PERSP',62),'rear-left':((2.4,-3,1.07),(0,0,.35),'PERSP',62),'rear-right':((2.4,3,1.07),(0,0,.35),'PERSP',62),'neutral':((-1.5,-2.4,1.0),(0,0,.38),'PERSP',58)}
projection={}
for name,(loc,tar,typ,scale) in views.items():
 bpy.ops.object.camera_add(location=loc);cam=bpy.context.object;cam.name='V02 diagnostic '+name;cam.rotation_euler=(Vector(tar)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type=typ
 if typ=='ORTHO':cam.data.ortho_scale=scale
 else:cam.data.lens=scale
 s.camera=cam;s.render.filepath=str(R/f'greenhouse-{name}-v02.png');bpy.ops.render.render(write_still=True)
 if name=='side':
  def px(v):
   a=world_to_camera_view(s,cam,Vector(v));return[a.x*1100,(1-a.y)*750]
  a=px((-.5,0,0));b=px((.5,0,0));k=506/(b[0]-a[0]);edges=[]
  for ob in body:
   if ('glass -1' in ob.name or ob.name=='Longitudinal and transverse roof crown'):
    counts={}
    for f in ob.data.polygons:
     for i,j in zip(f.vertices,list(f.vertices[1:])+[f.vertices[0]]):key=tuple(sorted((i,j)));counts[key]=counts.get(key,0)+1
    for (i,j),count in counts.items():
     if count!=1:continue
     vv=[ob.data.vertices[z].co for z in (i,j)]
     if ob.name.startswith('Longitudinal') and not all(v.y<-.1 for v in vv):continue
     pts=[px(v) for v in vv];edges.append([[280+(v[0]-a[0])*k,455+(v[1]-a[1])*k] for v in pts])
  projection={'edges':edges,'alignment':'manual x/z wheelbase and floor only; orthographic, NOT calibrated'}
(A/'profile-projection.json').write_text(json.dumps(projection))
s.camera=bpy.data.objects['V02 diagnostic neutral'];bpy.ops.wm.save_as_mainfile(filepath=str(D/'isuzu-mux-reference-constrained-v02.blend'))
dg=bpy.context.evaluated_depsgraph_get();stats={'base_cage_vertices':sum(len(o.data.vertices) for o in body),'evaluated_vertices':0,'evaluated_triangles':0,'greenhouse_mesh_objects':len(body),'stance_frozen':True,'station_count':11,'no_production_body':True,'profile_alignment':'manual not calibrated'}
for ob in body:
 me=ob.evaluated_get(dg).to_mesh();me.calc_loop_triangles();stats['evaluated_vertices']+=len(me.vertices);stats['evaluated_triangles']+=len(me.loop_triangles);ob.evaluated_get(dg).to_mesh_clear()
assert all(math.isfinite(float(c)) for o in body for v in o.data.vertices for c in v.co)
stats['stance_signature']=frozen;(A/'geometry-checks.json').write_text(json.dumps(stats,indent=2))

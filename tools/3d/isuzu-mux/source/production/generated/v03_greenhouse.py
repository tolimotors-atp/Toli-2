import bpy,bmesh,json,math,os
from pathlib import Path
from mathutils import Vector
O=Path(os.environ.get('MUX_V03_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';R=O/'renders/v03';gate=json.loads((A/'v03-gates.json').read_text());assert gate['five_view_silhouette']=='PASS'
bpy.ops.wm.open_mainfile(filepath=str(D/'milestones/isuzu-mux-v03-blockout.blend'));s=bpy.context.scene;body=bpy.data.objects['V03_NEW_EXTERIOR_SHELL'];ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());col=bpy.data.collections['V03_EXTERIOR'];black=bpy.data.materials['Graphite polymer']
def roundpoly(pts):
 out=[]
 for i,p in enumerate(pts):
  b=Vector(p);a=b+(Vector(pts[i-1])-b)*.09;c=b+(Vector(pts[(i+1)%len(pts)])-b)*.09
  for j in range(3):t=j/2;out.append(tuple((1-t)**2*a+2*(1-t)*t*b+t*t*c))
 return out
def patch(name,points,axis,side,material=None,offset=.008):
 pts=roundpoly(points);center=sum((Vector(p) for p in pts),Vector((0,0)))/len(pts);verts=[];faces=[]
 def project(q):
  u,v=q
  if axis=='Y':origin=Vector((u,side*2.0,v));direction=Vector((0,-side,0))
  else:origin=Vector((side*4.0,u,v));direction=Vector((-side,0,0))
  hit,co,normal,index=ev.ray_cast(origin,direction)
  assert hit,(name,list(q));return co-direction*offset
 # Six subdivisions per fan triangle keep the opaque study surface seated on the shared shell.
 for k,p in enumerate(pts):
  a=center;b=Vector(p);c=Vector(pts[(k+1)%len(pts)]);ids={};n=6
  for i in range(n+1):
   for j in range(n+1-i):ids[(i,j)]=len(verts);verts.append(project(a+(b-a)*i/n+(c-a)*j/n))
  for i in range(n):
   for j in range(n-i):
    faces.append((ids[(i,j)],ids[(i+1,j)],ids[(i,j+1)]))
    if j<n-i-1:faces.append((ids[(i+1,j)],ids[(i+1,j+1)],ids[(i,j+1)]))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=.00001);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.normal_update()
 expected=Vector((0,side,0)) if axis=='Y' else Vector((side,0,0))
 for f in bm.faces:
  if f.normal.dot(expected)<0:f.normal_flip()
 bm.to_mesh(me);bm.free();ob=bpy.data.objects.new(name,me);col.objects.link(ob);me.materials.append(material or black)
 for f in me.polygons:f.use_smooth=True
 return ob
windows={'FRONT':[(-.88,1.285),(-.27,1.68),(.22,1.70),(.22,1.30)],'REAR':[(.35,1.30),(.35,1.70),(1.23,1.70),(1.20,1.43),(1.08,1.34)],'QUARTER':[(1.47,1.345),(1.40,1.69),(1.87,1.65),(2.16,1.35)],'B_PILLAR':[(.225,1.30),(.225,1.70),(.345,1.70),(.345,1.30)]}
for side in [-1,1]:
 for name,points in windows.items():patch('V03_COHERENT_'+name+'_'+str(side),points,'Y',side)
patch('V03_COHERENT_WINDSCREEN',[(-.69,1.345),(.69,1.345),(.59,1.70),(-.59,1.70)],'X',-1)
patch('V03_COHERENT_REAR_GLASS',[(-.69,1.38),(.69,1.38),(.59,1.68),(-.59,1.68)],'X',1)
s['V03_STAGE']='Coherent greenhouse study projected from the new common shell; no panel cuts';s['V03_GLAZING_LIMIT']='Opaque graphite study surfaces, not finished transparent glass. Every point derives from the same evaluated shell; no independent frame offsets or floating glass.'
bpy.ops.wm.save_as_mainfile(filepath=str(D/'milestones/isuzu-mux-v03-greenhouse.blend'));bpy.ops.wm.save_as_mainfile(filepath=str(D/'isuzu-mux-generated-v03.blend'))
for name in ['FRONT','FRONT_34','SIDE','REAR_34','REAR']:
 s.camera=bpy.data.objects['CAM_COMPARE_'+name];s.render.filepath=str(R/('v03-greenhouse-'+name.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('V03 GREENHOUSE SAVED; NO IDENTITY DETAILS OR PANEL CUTS',flush=True);os._exit(0)

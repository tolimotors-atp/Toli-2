import math,bpy,bmesh
from .mux_shape_data import BODY,CABIN,ARCH,WINDOWS

def sample(table,x):
 """Cubic Hermite with centred slopes; station endpoints stay fixed."""
 i=next((i for i in range(len(table)-1) if x<=table[i+1][0]),len(table)-2);a,b=table[i:i+2];t=max(0,min(1,(x-a[0])/(b[0]-a[0])));out=[]
 for k in range(1,len(a)):
  prev=table[max(0,i-1)];nxt=table[min(len(table)-1,i+2)];m0=(b[k]-prev[k])/(b[0]-prev[0]);m1=(nxt[k]-a[k])/(nxt[0]-a[0]);d=b[0]-a[0];out.append((2*t**3-3*t*t+1)*a[k]+(t**3-2*t*t+t)*d*m0+(-2*t**3+3*t*t)*b[k]+(t**3-t*t)*d*m1)
 return out

def symmetric_bake(o):
 """Keep one evaluated half and mirror it: no tolerance relaxation."""
 deps=bpy.context.evaluated_depsgraph_get();data=bpy.data.meshes.new_from_object(o.evaluated_get(deps),depsgraph=deps);o.modifiers.clear();old=o.data;o.data=data
 if old.users==0:bpy.data.meshes.remove(old)
 bm=bmesh.new();bm.from_mesh(data);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,0),plane_no=(0,1,0),clear_outer=True)
 for v in bm.verts:
  if abs(v.co.y)<1e-6:v.co.y=0
 bmesh.ops.dissolve_degenerate(bm,dist=1e-7,edges=list(bm.edges));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(data);bm.free();m=o.modifiers.new('Exact centreline mirror','MIRROR');m.use_axis[0]=False;m.use_axis[1]=True;m.use_clip=True;m.use_mirror_merge=True;m.merge_threshold=1e-6

def body_sections(p,count):
 out=[]
 for i in range(count):
  x=-.5+i/(count-1);w,top,shoulder,bulge=sample(BODY,x);w*=p['width']/1.86;top*=p['height']/1.86;shoulder*=p['height']/1.86
  crown=.035 if x<-.14 else .012;bottom=p['ground_clearance']
  # Full cross-section: sill, concave lower return, convex door, shoulder, bonnet crown.
  half=[(0,bottom),(w*.83,bottom),(w*.90,.36),(w*.94,.48),(w*.97+bulge*.25,.69),(w,.88),(w,shoulder),(w*.96,top-.055),(w*.80,top-.008),(w*.45,top+crown*.7),(0,top+crown)]
  yz=half+ [(-y,z) for y,z in reversed(half[1:-1])];out.append([(x*p['length'],y,z) for y,z in yz])
 return out

def cabin_sections(p,count):
 out=[]
 for i in range(count):
  x=CABIN[0][0]+(CABIN[-1][0]-CABIN[0][0])*i/(count-1);lo,up,z,top=sample(CABIN,x);lo*=p['greenhouse_width']/1.49;up*=p['greenhouse_width']/1.49;top*=p['height']/1.86
  half=[(0,z),(lo,z),(lo*.99,z+.05),(up,top-.06),(up*.60,top-.012),(0,top)];yz=half+[(-y,z) for y,z in reversed(half[1:-1])];out.append([(x*p['length'],y,z) for y,z in yz])
 return out

def cut_arch(body,p,mesh,col):
 # Extruded asymmetric longitudinal arch profile; paired across Y by one shared cutter.
 for x in [-p['wheelbase']/2,p['wheelbase']/2]:
  r=p['tire_diameter']/2;profile=[(-r-ARCH['front_clearance'],-.15)]
  for i in range(33):
   a=math.pi-i*math.pi/32;rx=r+(ARCH['front_clearance'] if math.cos(a)<0 else ARCH['rear_clearance']);profile.append((rx*math.cos(a),r+(r+ARCH['top_clearance'])*math.sin(a)))
  profile.append((r+ARCH['rear_clearance'],-.15));sections=[[(x+dx,y,z) for dx,z in profile] for y in [-p['width'],p['width']]];cut=mesh('ARCH_CUT',sections,None,col);mod=body.modifiers.new('Original arch profile','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=mod.name);data=cut.data;bpy.data.objects.remove(cut,do_unlink=True);bpy.data.meshes.remove(data)

def windows(p,mesh,col,mat):
 for sign in [-1,1]:
  for i,outline in enumerate(WINDOWS):
   section=[]
   for x,z in outline:
    lo,up,base,top=sample(CABIN,x/p['length']);blend=min(1,max(0,(z-base)/max(.05,top-base)));y=(lo+(up-lo)*blend)*p['greenhouse_width']/1.49+.005;section.append((x,sign*y,z))
   # Thin closed paired volumes, not open decals.
   mesh(f'MUX_SIDE_WINDOW_{sign}_{i}',[section,[(x,y+sign*.003,z) for x,y,z in section]],mat,col)

"""Anatomical control nets for three independent construction tests.
shortcut: new transverse depth sections are inferred; these are not calibrated vehicle surfaces.
"""
import math
from mathutils import Vector
from .flow_cage import points,cubic,sample_x
from .depth_cage import width

class Net:
 def __init__(self):self.vertices=[];self.faces=[];self.labels=[];self.lookup={};self.sections=[]
 def vertex(self,co):
  co=tuple(Vector(co));key=co
  if key not in self.lookup:self.lookup[key]=len(self.vertices);self.vertices.append(co)
  return self.lookup[key]
 def grid(self,rows,label):
  ids=[[self.vertex(v) for v in row] for row in rows]
  for i in range(len(ids)-1):
   for j in range(len(ids[i])-1):self.faces.append((ids[i][j],ids[i+1][j],ids[i+1][j+1],ids[i][j+1]));self.labels.append(label(i,j) if callable(label) else label)
  self.sections.extend(rows);return ids
 def ring(self,loops,labels):
  ids=[[self.vertex(v) for v in row] for row in loops];n=len(ids[0])
  for i in range(len(ids)-1):
   for j in range(n):self.faces.append((ids[i][j],ids[i][(j+1)%n],ids[i+1][(j+1)%n],ids[i+1][j]));self.labels.append(labels[i])
  self.sections.extend([row+[row[0]] for row in loops]);return ids

def loop_samples(o):
 ps=points(o)
 return [cubic(a,b,t)[0] for a,b in zip(ps,list(ps[1:])+[ps[0]]) for t in [0,.5]]

def zone_a(col,p):
 net=Net();obj=lambda n:col.objects['TRACE_'+n];sx=p['length']/4.825;sy=p['width']/1.86;sz=p['height']/1.86
 xs=[-2.18,-2.03,-1.87,-1.56,-p['wheelbase']/2,-1.25,-.94,-.82];rows=[]
 for rawx in xs:
  x=rawx*sx if rawx!=-p['wheelbase']/2 else rawx
  edge=sample_x(obj('BONNET_EDGE'),x);center=sample_x(obj('BONNET_CENTER'),x);cap=sample_x(obj('SIDE_MASTER'),x).z
  zc=min(center.z,cap+.010*sz)
  if rawx>-.94:zc=min(sample_x(obj('A_PILLAR'),x).z+.018*sz,cap+.010*sz)
  ze=min(edge.z,zc-.025*sz);ew=abs(edge.y);outer=min(width(x,'maximum',p),.930*sy)
  lip=sample_x(obj('FRONT_ARCH'),x).z
  if x<points(obj('FRONT_ARCH'))[0].co.x:lip=.64*sz
  if rawx>-.94:lip=.58*sz
  crown=max(lip+.095*sz,ze-.115*sz);side=max(lip+.045*sz,min(crown-.035*sz,ze-.21*sz))
  half=[Vector((x,0,zc)),Vector((x,-ew*.45,zc-.004*sz)),Vector((x,-ew*.82,ze+.014*sz)),Vector((x,-ew,ze)),Vector((x,-(ew+outer)*.5,crown)),Vector((x,-outer,side)),Vector((x,-outer,lip+.015*sz)),Vector((x,-(outer-.014*sy),lip))]
  row=list(reversed(half))+[Vector((v.x,-v.y,v.z)) for v in half[1:]];rows.append(row)
 bands=['lip_return','arch_roll','fender_outer','fender_upper','bonnet_roll','bonnet_outer','bonnet_center']+list(reversed(['lip_return','arch_roll','fender_outer','fender_upper','bonnet_roll','bonnet_outer','bonnet_center']))
 net.grid(rows,lambda i,j:'cowl_root' if i==len(rows)-2 else bands[j])
 # The root is a shared-edge surface strip, not an independent curve or a full A-pillar.
 for sign in [1,-1]:
  start=[rows[-1][4],rows[-1][5]]
  root_rows=[[Vector((v.x,sign*v.y,v.z)) for v in start]]
  for x0 in [-.76,-.70,-.64]:
   x=x0*sx;a=sample_x(obj('A_PILLAR'),x);cap=sample_x(obj('SIDE_MASTER'),x).z
   z=min(a.z,cap+.006*sz)
   root_rows.append([Vector((x,sign*(a.y-.035*sy),z-.018*sz)),Vector((x,sign*(a.y+.035*sy),z))])
  net.grid(root_rows,'A_root')
 return net

def zone_b(col,p):
 net=Net();sx=p['length']/4.825;sy=p['width']/1.86;sz=p['height']/1.86;obj=lambda n:col.objects['TRACE_'+n]
 q=loop_samples(obj('QUARTER_GLASS'));cx=sum(v.x for v in q)/len(q);cz=sum(v.z for v in q)/len(q)
 outer=[]
 for i,v in enumerate(q):
  x=cx+(v.x-cx)*1.16;z=cz+(v.z-cz)*1.20
  z=max(z,(1.315 if x>2.0*sx else 1.245)*sz);z=min(z,sample_x(obj('SIDE_MASTER'),x).z+.004*sz)
  y=-min(.885*sy,max(.64*sy,(.885-.22*max(0,min(1,(z/sz-1.24)/.52)))*sy))
  co=Vector((x,y,z))
  if i in [0,1,2]:co=sample_x(obj('ROOF_EDGE'),v.x)
  outer.append(co)
 # Rear-glass boundary rows retain V04 outer positions and receive an inferred lateral crown.
 g=points(obj('REAR_GLASS'));ts=[0,.18,.43,.70,1.]
 left=[]
 for t in ts:
  u=t*2;left.append(cubic(g[2],g[3],u)[0] if u<=1 else cubic(g[3],g[4],u-1)[0])
 # Rear Y/Z aperture evidence is retained; its inherited X must clear the side-window frame.
 def rear_cap_x(z):
  lo,hi=1.85*sx,2.40*sx
  for _ in range(24):
   mid=(lo+hi)/2
   if sample_x(obj('SIDE_MASTER'),mid).z>z:lo=mid
   else:hi=mid
  return (lo+hi)/2
 for i,v in enumerate(left):
  # Reserve a narrow D-return without pushing the glass past the side silhouette.
  outer[i+2].x=min(outer[i+2].x,rear_cap_x(v.z)-.065*sx)
  v.x=min(max(v.x,outer[i+2].x+.045*sx),rear_cap_x(v.z)-.015*sx)
 top=[g[2].co.copy(),g[1].co.copy(),g[0].co.copy()];top+= [Vector((v.x,-v.y,v.z)) for v in reversed(top[:-1])]
 bottom=[g[4].co.copy(),g[4].co.lerp(g[5].co,.5),g[5].co.copy()];bottom += [Vector((v.x,-v.y,v.z)) for v in reversed(bottom[:-1])]
 glass=[]
 for i,t in enumerate(ts):
  row=[]
  for j,u in enumerate([-1,-.5,0,.5,1]):
   co=top[j].lerp(bottom[j],t);co.x+=.018*sx*(1-u*u)*math.sin(math.pi*t)
   if j==0:co=left[i].copy()
   elif j==4:co=Vector((left[i].x,-left[i].y,left[i].z))
   row.append(co)
  glass.append(row)
 # One coupled transverse crown keeps the glass behind the D frame without moving Y/Z evidence.
 for i,row in enumerate(glass):
  center_x=max(left[i].x,min(max(row[2].x,left[i].x+.012*sx),rear_cap_x(row[2].z)-.005*sx))
  for j,u in enumerate([-1,-.5,0,.5,1]):row[j].x=left[i].x+(center_x-left[i].x)*(1-u*u)
 net.grid(glass,'rear_glass')
 # The side-window ring embeds the reference aperture, with a small returned physical lip.
 for sign in [1,-1]:
  reflect=lambda v:Vector((v.x,sign*v.y,v.z))
  lip=[Vector((v.x,v.y+.008*sy,v.z)) for v in q]
  net.ring([[reflect(v) for v in lip],[reflect(v) for v in q],[reflect(v) for v in outer]],['window_return','quarter_frame'])
  bridge=[]
  for i,idx in enumerate(range(2,7)):
   a=reflect(outer[idx]);b=reflect(left[i]);mid=a.lerp(b,.5);mid.y-=sign*.010*sy
   bridge.append([a,mid,b])
  net.grid(bridge,'D_surface')
 # Roof sections share the actual outer-ring nodes along its upper boundary.
 xs=[1.15*sx]+[outer[i].x for i in [0,1,2]];roof=[]
 for i,x in enumerate(xs):
  edge=sample_x(obj('ROOF_EDGE'),x) if i==0 else outer[i-1];center=sample_x(obj('ROOF_CENTER'),x)
  row=[]
  for u in [-1,-.5,0,.5,1]:
   co=Vector((x,abs(edge.y)*u,center.z-(center.z-edge.z)*abs(u)**2))
   if abs(u)==1:co=Vector((edge.x,abs(edge.y)*u,edge.z))
   row.append(co)
  roof.append(row)
 net.grid(roof,'rear_roof')
 mid=[a.lerp(b,.5) for a,b in zip(roof[-1],glass[0])]
 # Match both D-bridge first-row middle vertices exactly, so there is no T junction.
 mid[0].y-=.010*sy;mid[-1].y+=.010*sy
 net.grid([roof[-1],mid,glass[0]],'roof_return')
 return net

def corner_x(y,z,p):
 sy=p['width']/1.86;sx=p['length']/4.825;sz=p['height']/1.86
 t=max(0,min(1,(z/sz-.5)/.5));t=t*t*(3-2*t);wrap=.10+.20*t
 return (2.36-wrap*(abs(y)/(.93*sy))**3-.03*max(0,(.45-z/sz)/.15))*sx

def zone_c(col,p):
 net=Net();sx=p['length']/4.825;sy=p['width']/1.86;sz=p['height']/1.86;obj=lambda n:col.objects['TRACE_'+n]
 original=loop_samples(obj('TAIL_LAMP'));cy=sum(v.y for v in original)/len(original);cz=sum(v.z for v in original)/len(original)
 # Only Y/Z lamp outline has high authority; X is reconstructed in the coupled corner section.
 boundary=[Vector((corner_x(v.y,v.z,p),v.y,v.z)) for v in original]
 outer=[]
 for v in boundary:
  y=max(-.93*sy,cy+(v.y-cy)*1.12);z=min(1.315*sz,cz+(v.z-cz)*1.14);outer.append(Vector((corner_x(y,z,p),y,z)))
 for sign in [1,-1]:
  ref=lambda v:Vector((v.x,sign*v.y,v.z))
  returned=[Vector((v.x-.008*sx,v.y,v.z)) for v in boundary]
  support=[v.lerp(o,.35) for v,o in zip(boundary,outer)]
  net.ring([[ref(v) for v in row] for row in [returned,boundary,support,outer]],['lamp_return','lamp_edge','lamp_frame'])
  tops=[]
  for x0 in [.80,.96,1.18,p['wheelbase']/2,1.70,1.94]:
   x=x0*sx if x0!=p['wheelbase']/2 else x0;z=min(1.20*sz,sample_x(obj('SHOULDER'),x).z+.13*sz);tops.append(Vector((x,-.80*sy,z)))
  tops += [outer[i].copy() for i in [9,8,7,6]]
  rows=[]
  for i,top in enumerate(tops):
   if i<6:
    lip=sample_x(obj('REAR_ARCH'),top.x).z;dx=(top.x-p['wheelbase']/2)/sx;influence=math.exp(-(dx/(.48 if dx<0 else .68))**2)
    zs=[top.z,max(lip+.10*sz,top.z-.10*sz),max(lip+.045*sz,top.z-.22*sz),lip+.018*sz,lip+.005*sz,lip-.004*sz]
    ys=[top.y,-(.895+.015*influence)*sy,-.93*sy,-.93*sy,-.925*sy,-.915*sy]
    row=[Vector((top.x,y,z)) for y,z in zip(ys,zs)]
   else:
    zs=[top.z,top.z-.13*sz,.68*sz,.46*sz,.325*sz,.30*sz];row=[]
    for j,z in enumerate(zs):
     y=top.y*(1 if j<3 else .97 if j==3 else .94);co=Vector((corner_x(y,z,p),y,z));row.append(top.copy() if j==0 else co)
   rows.append([ref(v) for v in row])
  roles=['quarter_upper','quarter_crown','quarter_outer','arch_roll','lip_return']
  net.grid(rows,lambda i,j:('bumper_'+roles[j] if i>=6 else roles[j]))
  # A painted quarter bridge joins the lamp frame; the remaining cut leads toward the unbuilt upper body.
  bridge=[]
  for k,idx in enumerate([9,10,11,0]):
   free=tops[5].copy() if k==0 else Vector((1.94*sx,-(.80+.02*k)*sy,(1.18+.045*k)*sz))
   bridge.append([ref(free),ref(outer[idx])])
  net.grid(bridge,'quarter_lamp_bridge')
 return net

"""V02 inferred depth constraints. Native side X/Z stays locked except named joins.
shortcut: uncontrolled photos constrain envelopes, not metric depth; replace profiles after calibrated capture.
"""
import bpy, math
from mathutils import Vector
from .reference_cage import generate_cage as generate_v01, COL, make
from ..traced_data import TRACES

LEVELS=('sill','lower','maximum','shoulder','belt','greenhouse','roof')
# X / half-widths in family-scale metres. Independent profiles, not a single taper.
STATIONS=[
 ('front_bumper',-2.4125,(.76,.80,.84,.82,.76,.59,.54)),
 ('front_wheel',-1.4225,(.86,.91,.93,.91,.82,.68,.64)),
 ('cowl',-.94,(.85,.89,.90,.88,.82,.73,.68)),
 ('B_pillar',.35,(.85,.89,.91,.90,.83,.77,.70)),
 ('C_pillar',1.27,(.86,.90,.93,.92,.84,.75,.69)),
 ('rear_wheel',1.4225,(.87,.91,.93,.92,.84,.73,.68)),
 ('tail_lamp',2.12,(.82,.87,.90,.88,.81,.68,.63)),
 ('rear_bumper',2.4125,(.78,.83,.86,.83,.76,.61,.56))]

def width(x,level,p):
 i=LEVELS.index(level);x=x*4.825/p['length']
 for (_,a,wa),(_,b,wb) in zip(STATIONS,STATIONS[1:]):
  if x<=b:
   t=max(0,min(1,(x-a)/(b-a)));t=t*t*(3-2*t)
   return (wa[i]*(1-t)+wb[i]*t)*p['width']/1.86
 return STATIONS[-1][2][i]*p['width']/1.86

def reset_handles(o):
 ps=o.data.splines[0].bezier_points;closed=o.data.splines[0].use_cyclic_u
 for i,b in enumerate(ps):
  a=ps[(i-1)%len(ps)] if closed else ps[max(0,i-1)]
  c=ps[(i+1)%len(ps)] if closed else ps[min(len(ps)-1,i+1)]
  t=(c.co-a.co)/6;b.handle_left=b.co-t;b.handle_right=b.co+t

def points(o):return o.data.splines[0].bezier_points

def at_x(o,x):
 ps=points(o)
 for a,b in zip(ps,ps[1:]):
  if min(a.co.x,b.co.x)<=x<=max(a.co.x,b.co.x):return a.co.lerp(b.co,(x-a.co.x)/(b.co.x-a.co.x))
 return min(ps,key=lambda b:abs(b.co.x-x)).co.copy()

def generate_cage(scene,p):
 col=generate_v01(scene,p)
 for o in list(col.objects):
  if o.name.startswith('LINK_'):
   d=o.data;bpy.data.objects.remove(o,do_unlink=True);bpy.data.curves.remove(d)
 side_before={n:[(b.co.x,b.co.z) for b in points(col.objects['TRACE_'+n])] for n,(src,*_) in TRACES.items() if src=='side'}
 for n,(source,uv,depth,closed) in TRACES.items():
  o=col.objects['TRACE_'+n]
  for b in points(o):
   v=b.co
   if source=='side':
    if depth==0:v.y=0
    else:
     level='maximum'
     if 'ROOF' in n:level='roof'
     elif any(t in n for t in ['WINDOW','GLASS','PILLAR']):level='greenhouse'
     elif n in ['BELT','BONNET_EDGE']:level='belt'
     elif n=='SILL':level='sill'
     elif n=='SHOULDER':level='shoulder'
     elif n=='SIDE_MASTER':level='roof' if v.z>1.5 else 'maximum'
     v.y=-width(v.x,level,p)
   else:
    # Face centre projects forward; lamp/bumper edges return onto the sides.
    t=min(1,abs(v.y)/(p['width']/2));wrap=t*t
    if source=='front':
     face={'BONNET_FRONT':-2.26,'HEADLIGHT':-2.30,'GRILLE_UPPER':-2.36,'GRILLE_SURROUND':-2.38,'GRILLE_LOWER':-2.39,'FRONT_LOWER_OPENING':-2.40,'FRONT_BUMPER':-2.4125}
     if n=='FRONT_ROOF':v.x=.69*p['length']/4.825
     if n in face:v.x=(face[n]+(.32 if n in ['HEADLIGHT','FRONT_BUMPER'] else .18)*wrap)*p['length']/4.825
    else:
     face={'REAR_GLASS':2.20,'TAIL_LAMP':2.30,'TAILGATE':2.34,'REAR_BUMPER':2.4125,'REAR_LOWER_TRIM':2.39}
     v.x=(face[n]-(.28 if n in ['TAIL_LAMP','REAR_BUMPER'] else .14)*wrap)*p['length']/4.825
     if n=='REAR_GLASS':v.x=(2.20-(v.z-1.30)*.45-.10*wrap)*p['length']/4.825
  reset_handles(o)
 def obj(n):return col.objects['TRACE_'+n]
 def add(n,co,kind='section',closed=False):
  o=make(col,n,[Vector(c) for c in co],kind,closed);o['depth']='Inferred; not calibrated';return o
 def transverse(n,x,edge,center,kind='section'):
  y=abs(edge.y);co=[(x,-y,edge.z),(x,-y*.67,center.z-(center.z-edge.z)*.24),(x,0,center.z),(x,y*.67,center.z-(center.z-edge.z)*.24),(x,y,edge.z)]
  o=add(n,co,kind);o['depth_slice']=True;return o
 # Shared cowl/roof/D coordinates. All mirrored only after correction.
 joins=[];bridge_joins=[]
 def join(code,a,ai,b,bi,soft):
  pa,pb=points(obj(a))[ai],points(obj(b))[bi];pb.co=pa.co.copy()
  reset_handles(obj(a));reset_handles(obj(b))
  if soft:
   ta=pa.co-pa.handle_left;tb=pb.handle_right-pb.co
   t=(ta.normalized()+tb.normalized()).normalized();pa.handle_left=pa.co-t*ta.length;pa.handle_right=pa.co+t*ta.length;pb.handle_left=pb.co-t*tb.length;pb.handle_right=pb.co+t*tb.length
  joins.append((code,a,ai,b,bi,soft))
 join('J02','BONNET_EDGE',-1,'A_PILLAR',0,False)
 join('J03','ROOF_EDGE',0,'A_PILLAR',-1,True)
 join('J04','ROOF_EDGE',-1,'D_PILLAR',0,True)
 join('WINDSCREEN_ROOF','ROOF_CENTER',0,'WINDSCREEN_CENTER',-1,True)
 # Cowl/windscreen boundaries share the same three-dimensional section.
 for name,edge,center in [('WINDSCREEN_BOTTOM','BONNET_EDGE','BONNET_CENTER'),('WINDSCREEN_TOP','ROOF_EDGE','ROOF_CENTER')]:
  ep=points(obj(edge))[-1 if name.endswith('BOTTOM') else 0].co;cp=points(obj(center))[-1 if name.endswith('BOTTOM') else 0].co
  ps=points(obj(name))
  for i,b in enumerate(ps):b.co=ep.lerp(cp,i/(len(ps)-1))
  reset_handles(obj(name))
 # Crown sections anchored to retained side rail heights.
 x0=max(points(obj('BONNET_CENTER'))[0].co.x,points(obj('BONNET_EDGE'))[0].co.x);x1=points(obj('BONNET_EDGE'))[-1].co.x
 for i,t in enumerate([0,.25,.5,.75,1]):
  x=x0+(x1-x0)*t;e=at_x(obj('BONNET_EDGE'),x);c=at_x(obj('BONNET_CENTER'),x);transverse('SECTION_BONNET_'+str(i),x,e,c)
 for n,x in [('FRONT_ROOF',points(obj('ROOF_EDGE'))[0].co.x),('B_ROOF',.35),('C_ROOF',1.27),('D_ROOF',points(obj('ROOF_EDGE'))[-1].co.x)]:
  transverse('SECTION_'+n,x,at_x(obj('ROOF_EDGE'),x),at_x(obj('ROOF_CENTER'),x))
 transverse('SECTION_WINDSCREEN_MID',-.65,at_x(obj('A_PILLAR'),-.65),at_x(obj('WINDSCREEN_CENTER'),-.65))
 # Fixed axles remain the hard reference; outer lip/fender widths are independently constrained.
 for end,x in [('FRONT',-p['wheelbase']/2),('REAR',p['wheelbase']/2)]:
  for i,t in enumerate([-.75,0,.75]):
   xx=x+t*.43;z=.382+math.sqrt(max(0,.47**2-(xx-x)**2))
   add(end+'_FENDER_WRAP_'+str(i),[(xx,-.90,z),(xx,-width(xx,'maximum',p),z+.045),(xx,-width(xx,'shoulder',p),z+.18),(xx,-width(xx,'belt',p),z+.25)],'character')
  e=at_x(obj(end+'_FENDER_CROWN'),x);c=e.copy();c.y=0;c.z+=.09;transverse('SECTION_'+end+'_FENDER',x,e,c)
 # Bridge existing rails with explicit endpoint tangents. Character cuts retain their break.
 def bridge(code,name,a,ai,b,bi,soft):
  pa,pb=points(obj(a))[ai],points(obj(b))[bi];o=add(name,[pa.co,pa.co.lerp(pb.co,.5),pb.co],'character');ps=points(o)
  if soft:
   ta=(pa.handle_right-pa.co).normalized();tb=(pb.co-pb.handle_left).normalized();d=(pa.co-pb.co).length/3
   ps[0].handle_right=ps[0].co+ta*d;ps[0].handle_left=ps[0].co-ta*d;ps[-1].handle_left=ps[-1].co-tb*d;ps[-1].handle_right=ps[-1].co+tb*d
  o['join_id']=code;o['join_type']='soft' if soft else 'character cut';bridge_joins.append((code,o,a,ai,b,bi,soft));return o
 bridge('J01','FENDER_TO_BONNET','FRONT_FENDER_CROWN',2,'BONNET_EDGE',1,True)
 bridge('J05','SHOULDER_TO_QUARTER','SHOULDER',-1,'REAR_QUARTER_RETURN',1,True)
 bridge('J06','QUARTER_TO_LAMP','REAR_QUARTER_RETURN',1,'TAIL_LAMP',0,False)
 bridge('J07','QUARTER_TO_BUMPER','REAR_QUARTER_RETURN',-1,'REAR_BUMPER',1,True)
 bridge('J08','D_TO_REAR_GLASS','D_PILLAR',-1,'REAR_GLASS',-2,False)
 for end,rail,face in [('FRONT','FRONT_DOOR_RETURN','FRONT_BUMPER'),('REAR','REAR_QUARTER_RETURN','REAR_BUMPER')]:
  a=points(obj(face))[1].co;b=points(obj(rail))[-1].co
  add(end+'_BUMPER_RETURN',[a,(a.x*.65+b.x*.35,-width(a.x,'lower',p),a.z),(b.x,-width(b.x,'sill',p),b.z)],'character')
 for station,x,_ in STATIONS:
  x*=p['length']/4.825
  co=[(x,-width(x,l,p),z*p['height']/1.86) for l,z in zip(LEVELS,[.40,.65,.95,1.05,1.24,1.52,1.75])]
  co += [(x,0,1.80*p['height']/1.86)]+[(a,-b,c) for a,b,c in reversed(co)]
  o=add('SLICE_'+station,co);o['depth_slice']=True;o['station_slice']=True;o.hide_render=True;o.hide_viewport=True
 # Restore both endpoint tangents after all shared-rail edits (roof has two joins).
 for code,a,ai,b,bi,soft in joins:
  if not soft:continue
  pa,pb=points(obj(a))[ai],points(obj(b))[bi]
  ta=pa.co-pa.handle_left;tb=pb.handle_right-pb.co;t=(ta.normalized()+tb.normalized()).normalized()
  pa.handle_left=pa.co-t*ta.length;pa.handle_right=pa.co+t*ta.length;pb.handle_left=pb.co-t*tb.length;pb.handle_right=pb.co+t*tb.length
 add('REAR_ROOF_GLASS_RETURN',[points(obj('ROOF_EDGE'))[-1].co,points(obj('REAR_GLASS'))[0].co],'greenhouse')
 add('REAR_CENTER_DEPTH',[points(obj('ROOF_CENTER'))[-1].co,points(obj('REAR_GLASS'))[2].co,points(obj('REAR_GLASS'))[3].co,points(obj('TAILGATE'))[-1].co],'rear')
 # Mirror all corrected traces and newly authored half curves, retaining diagnostic geometry.
 for o in list(col.objects):
  if o.name.endswith('_R'):continue
  ps=points(o)
  if o.get('depth_slice'):continue
  if not any(abs(b.co.y)>1e-8 for b in ps) and col.objects.get(o.name+'_R') is None:continue
  mirror=col.objects.get(o.name+'_R')
  if mirror is None:mirror=add(o.name+'_R',[b.co for b in ps],o['trace_class'],o.data.splines[0].use_cyclic_u)
  for b,c in zip(ps,points(mirror)):
   for attr in ['co','handle_left','handle_right']:
    v=getattr(b,attr);setattr(c,attr,(v.x,-v.y,v.z))
  mat=bpy.data.materials.get('V02 far '+o.name) or o.data.materials[0].copy();mat.name='V02 far '+o.name;mat.diffuse_color=tuple(v*.24 for v in mat.diffuse_color[:3])+(1,);bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=mat.diffuse_color;bs.inputs['Emission Color'].default_value=mat.diffuse_color;mirror.data.materials.clear();mirror.data.materials.append(mat)
 audit=[]
 for code,a,ai,b,bi,soft in joins:
  pa,pb=points(obj(a))[ai],points(obj(b))[bi];audit.append({'id':code,'position_error_m':(pa.co-pb.co).length,'type':'soft' if soft else 'character cut','tangent_angle_deg':math.degrees((pa.co-pa.handle_left).angle(pb.handle_right-pb.co,0)) if soft else None})
 for code,o,a,ai,b,bi,soft in bridge_joins:
  ps=points(o);pa,pb=points(obj(a))[ai],points(obj(b))[bi]
  angles=[math.degrees((pa.handle_right-pa.co).angle(ps[0].handle_right-ps[0].co,0)),math.degrees((pb.co-pb.handle_left).angle(ps[-1].co-ps[-1].handle_left,0))] if soft else []
  audit.append({'id':code,'position_error_m':max((pa.co-ps[0].co).length,(pb.co-ps[-1].co).length),'depth_error_m':max(abs(pa.co.y-ps[0].co.y),abs(pb.co.y-ps[-1].co.y)),'type':'soft' if soft else 'character cut','tangent_angle_deg':max(angles) if angles else None})
 scene['v02_join_measurements']=__import__('json').dumps(audit)
 scene['v02_side_max_xz_change_m']=max(math.hypot(b.co.x-x,b.co.z-z) for n,coords in side_before.items() for b,(x,z) in zip(points(obj(n)),coords))
 return col

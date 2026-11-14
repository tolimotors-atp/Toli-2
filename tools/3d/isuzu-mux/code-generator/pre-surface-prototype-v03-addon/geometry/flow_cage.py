"""Local V03 flow corrections over the preserved V02 construction.
shortcut: curvature diagnostics are envelope guidance, not a calibrated surface proof.
"""
import bpy,math,json
from mathutils import Vector
from .depth_cage import generate_cage as generate_v02,points,reset_handles,width,STATIONS,LEVELS
from .reference_cage import COL,make
JOIN_CURVES={
 'J01':['TRACE_BONNET_EDGE','TRACE_FRONT_FENDER_CROWN','FENDER_TO_BONNET','FRONT_FENDER_SHOULDER']+['SECTION_BONNET_'+str(i) for i in range(5)],
 'J02':['TRACE_BONNET_EDGE','TRACE_A_PILLAR','TRACE_WINDSCREEN_BOTTOM','COWL_ROOT_BLEND','SECTION_BONNET_4'],
 'J03':['TRACE_A_PILLAR','TRACE_ROOF_EDGE','TRACE_WINDSCREEN_TOP'],
 'J04':['TRACE_ROOF_EDGE','TRACE_D_PILLAR','TRACE_QUARTER_GLASS','REAR_ROOF_GLASS_RETURN','SECTION_D_BODY'],
 'J05':['TRACE_SHOULDER','TRACE_REAR_FENDER_CROWN','TRACE_REAR_QUARTER_RETURN','SHOULDER_TO_QUARTER','SECTION_REAR_FENDER'],
 'J06':['TRACE_REAR_QUARTER_RETURN','TRACE_TAIL_LAMP','QUARTER_TO_LAMP','SECTION_LAMP_BAND'],
 'J07':['TRACE_REAR_QUARTER_RETURN','TRACE_REAR_BUMPER','TRACE_REAR_LOWER_TRIM','QUARTER_TO_BUMPER','REAR_BUMPER_RETURN','SECTION_UPPER_BUMPER','SECTION_LOWER_BUMPER'],
 'J08':['TRACE_D_PILLAR','TRACE_REAR_GLASS','TRACE_TAILGATE','D_TO_REAR_GLASS','REAR_CENTER_DEPTH','SECTION_D_BODY','SECTION_REAR_GLASS','SECTION_TAILGATE']}
JOIN_STATION={'J01':'front_wheel','J02':'cowl','J03':'cowl','J04':'C_pillar','J05':'rear_wheel','J06':'tail_lamp','J07':'rear_bumper','J08':'tail_lamp'}

def cubic(a,b,t):
 p0,p1,p2,p3=a.co,a.handle_right,b.handle_left,b.co;u=1-t
 co=u**3*p0+3*u*u*t*p1+3*u*t*t*p2+t**3*p3
 d=3*(u*u*(p1-p0)+2*u*t*(p2-p1)+t*t*(p3-p2))
 dd=6*(u*(p2-2*p1+p0)+t*(p3-2*p2+p1))
 k=d.cross(dd).length/max(d.length**3,1e-12)
 return co,d,k

def sample_x(o,x):
 ps=points(o)
 for a,b in zip(ps,ps[1:]):
  if a.co.x<=x<=b.co.x:
   lo,hi=0.,1.
   for _ in range(30):
    t=(lo+hi)/2
    if cubic(a,b,t)[0].x<x:lo=t
    else:hi=t
   return cubic(a,b,(lo+hi)/2)[0]
 return min(ps,key=lambda b:abs(b.co.x-x)).co.copy()

def shape_handles(o):
 """Chord-length handles prevent a tiny bridge from inheriting a long rail tangent."""
 ps=points(o);cyclic=o.data.splines[0].use_cyclic_u
 for i,b in enumerate(ps):
  a=ps[(i-1)%len(ps)] if cyclic else ps[max(0,i-1)];c=ps[(i+1)%len(ps)] if cyclic else ps[min(len(ps)-1,i+1)]
  ab=b.co-a.co;bc=c.co-b.co
  t=(ab.normalized()+bc.normalized()).normalized() if ab.length and bc.length else (ab+bc).normalized()
  b.handle_left=b.co-t*ab.length/3;b.handle_right=b.co+t*bc.length/3

def curvature_audit(col):
 out={}
 for join,names in JOIN_CURVES.items():
  records=[]
  for name in names:
   o=col.objects.get(name)
   if not o:continue
   ps=points(o);junctions=[]
   for i in range(1,len(ps)-1):
    left=[cubic(ps[i-1],ps[i],t)[2] for t in [.8,.9,.98,1]]
    right=[cubic(ps[i],ps[i+1],t)[2] for t in [0,.02,.1,.2]]
    dl=cubic(ps[i-1],ps[i],1)[1];dr=cubic(ps[i],ps[i+1],0)[1]
    junctions.append({'control_index':i,'gap_m':0.,'tangent_angle_deg':math.degrees(dl.angle(dr,0)),'curvature_before':left,'curvature_after':right,'relative_curvature_jump':abs(left[-1]-right[0])/max(left[-1],right[0],1e-6)})
   records.append({'curve':name,'internal_junctions':junctions})
  out[join]=records
 return out

def generate_cage(scene,p):
 col=generate_v02(scene,p)
 def obj(n):return col.objects[n if n in col.objects else 'TRACE_'+n]
 protected={n:[[b.co.copy(),b.handle_left.copy(),b.handle_right.copy()] for b in points(obj(n))] for n in ['SIDE_MASTER','FRONT_WINDOW','REAR_WINDOW','QUARTER_GLASS']}
 # J03 includes both endpoints/handles; restore it after the local rear-roof edits.
 j03={n:[getattr(points(obj(n))[i],a).copy() for a in ['co','handle_left','handle_right']] for n,i in [('A_PILLAR',-1),('ROOF_EDGE',0)]}
 def replace(n,co,kind=None,section=False):
  old=col.objects.get(n)
  if old:
   kind=kind or old.get('trace_class','character');d=old.data;bpy.data.objects.remove(old,do_unlink=True)
   if d.users==0:bpy.data.curves.remove(d)
  o=make(col,n,[Vector(c) for c in co],kind or 'character');o['depth']='Inferred; not calibrated'
  if section:o['depth_slice']=True
  shape_handles(o);return o
 def half_section(n,left,kind='section'):
  co=[Vector(c) for c in left];co += [Vector((v.x,-v.y,v.z)) for v in reversed(co[:-1])]
  return replace(n,co,kind,True)
 # Five existing bonnet sections need two extra points per side to represent edge roll AND fender.
 for i in range(5):
  old=points(obj('SECTION_BONNET_'+str(i)));x=old[2].co.x;e=sample_x(obj('BONNET_EDGE'),x);c=sample_x(obj('BONNET_CENTER'),x)
  outer=width(x,'maximum',p);roll=(abs(e.y)+outer)*.5
  half_section('SECTION_BONNET_'+str(i),[(x,-outer,e.z-.12),(x,-roll,e.z-.035),e,(x,e.y*.55,c.z-(c.z-e.z)*.12),(x,0,c.z)])
 x=-p['wheelbase']/2;e=sample_x(obj('BONNET_EDGE'),x);f=sample_x(obj('FRONT_FENDER_CROWN'),x)
 replace('FENDER_TO_BONNET',[f,Vector((x,(e.y+f.y)/2,e.z-.045)),e])
 sh=points(obj('SHOULDER'));fc=points(obj('FRONT_FENDER_CROWN'))
 replace('FRONT_FENDER_SHOULDER',[fc[2].co,sh[1].co,sh[2].co,sh[3].co])
 # Rounded lower screen/cowl with fixed outer and centre anchors.
 screen=points(obj('WINDSCREEN_BOTTOM'));screen[1].co.x-=.018*p['length']/4.825;screen[1].co.z+=.009*p['height']/1.86;shape_handles(obj('WINDSCREEN_BOTTOM'))
 root=points(obj('A_PILLAR'))[0].co.copy();a=sample_x(obj('BONNET_EDGE'),root.x-.10);b=points(obj('A_PILLAR'))[1].co.lerp(root,.65)
 replace('COWL_ROOT_BLEND',[a,root,b],'greenhouse')
 # Preserve A/roof endpoints, reshape only their neighbouring handle lengths.
 shape_handles(obj('A_PILLAR'));shape_handles(obj('ROOF_EDGE'))
 d=points(obj('D_PILLAR'));d[1].co.y=-.72*p['width']/1.86;d[2].co.y=-.81*p['width']/1.86;shape_handles(obj('D_PILLAR'))
 roof=points(obj('ROOF_EDGE'));t=(d[1].co-roof[-2].co).normalized()
 roof[-1].handle_left=roof[-1].co-t*(roof[-1].co-roof[-2].co).length/3;roof[-1].handle_right=roof[-1].co+t*(d[1].co-d[0].co).length/3
 d[0].handle_left=d[0].co-t*(roof[-1].co-roof[-2].co).length/3;d[0].handle_right=d[0].co+t*(d[1].co-d[0].co).length/3
 # Nonlinear rear shoulder/crown progression; front-door rail and wheel anchors stay fixed.
 sh[3].co.z+=.018*p['height']/1.86;sh[4].co.z+=.025*p['height']/1.86
 lamp=points(obj('TAIL_LAMP'));lamp[4].co.x=2.10*p['length']/4.825
 lamp[0].co.x=2.075*p['length']/4.825;lamp[5].co.x=2.06*p['length']/4.825
 shape_handles(obj('TAIL_LAMP'))
 q=points(obj('REAR_QUARTER_RETURN'));q[1].co=lamp[4].co.copy();sh[-1].co=q[1].co.copy();shape_handles(obj('SHOULDER'))
 rear=points(obj('REAR_FENDER_CROWN'))
 for bp in rear:
  dx=(bp.co.x-p['wheelbase']/2)/(p['length']/4.825);influence=math.exp(-(dx/(.50 if dx<0 else .70))**2)
  bp.co.y=-min(width(bp.co.x,'maximum',p),abs(bp.co.y)+.009*influence*p['width']/1.86)
  bp.co.z+=.018*influence*p['height']/1.86
 shape_handles(obj('REAR_FENDER_CROWN'))
 replace('SHOULDER_TO_QUARTER',[sh[4].co,sh[5].co,sh[-1].co])
 replace('QUARTER_TO_LAMP',[q[0].co,lamp[0].co,lamp[4].co])
 bump=points(obj('REAR_BUMPER'));sx=p['length']/4.825;sy=p['width']/1.86;sz=p['height']/1.86
 for bp,co in zip(bump,[(2.29,-.87,.653),(2.26,-.87,.443),(2.23,-.763,.293),(2.30,0,.28)]):bp.co=(co[0]*sx,co[1]*sy,co[2]*sz)
 for bp,x in zip(points(obj('REAR_LOWER_TRIM')),[2.25,2.29,2.31]):bp.co.x=x*sx
 shape_handles(obj('REAR_LOWER_TRIM'))
 q[2].co=(2.30*sx,-.89*sy,.764*sz);q[3].co=bump[1].co.copy();shape_handles(obj('REAR_QUARTER_RETURN'));shape_handles(obj('REAR_BUMPER'))
 replace('QUARTER_TO_BUMPER',[q[2].co,bump[0].co,bump[1].co])
 replace('REAR_BUMPER_RETURN',[q[3].co,bump[2].co,points(obj('REAR_LOWER_TRIM'))[0].co])
 glass=points(obj('REAR_GLASS'));glass[4].co.x=2.17*sx;glass[4].co.y=-.745*sy;glass[3].co.x=2.23*sx;shape_handles(obj('REAR_GLASS'))
 replace('D_TO_REAR_GLASS',[d[-1].co,(2.22*sx,-.795*sy,1.28*sz),glass[4].co],'greenhouse')
 replace('REAR_ROOF_GLASS_RETURN',[roof[-1].co,glass[0].co],'greenhouse')
 replace('REAR_CENTER_DEPTH',[points(obj('ROOF_CENTER'))[-1].co,glass[2].co,glass[3].co,points(obj('TAILGATE'))[-1].co],'rear')
 half_section('SECTION_D_BODY',[(2.10*sx,-.89*sy,1.05*sz),(2.10*sx,-.81*sy,1.25*sz),(2.10*sx,-.72*sy,1.49*sz),(2.10*sx,-.64*sy,1.55*sz),(2.10*sx,0,1.575*sz)])
 half_section('SECTION_REAR_GLASS',[glass[4].co,(2.215*sx,-.42*sy,1.32*sz),glass[3].co])
 half_section('SECTION_LAMP_BAND',[lamp[4].co,(2.24*sx,-.68*sy,1.10*sz),(2.32*sx,0,1.16*sz)])
 half_section('SECTION_TAILGATE',[(2.30*sx,-.84*sy,.86*sz),(2.34*sx,-.46*sy,.96*sz),(2.36*sx,0,.98*sz)])
 half_section('SECTION_UPPER_BUMPER',[bump[0].co,(2.36*sx,-.50*sy,.66*sz),(2.39*sx,0,.66*sz)])
 half_section('SECTION_LOWER_BUMPER',[bump[2].co,(2.40*sx,-.40*sy,.285*sz),bump[3].co])
 # Front corner links use actual envelope anchors, not detached longitudinal tangents.
 replace('FRONT_CORNER_FLOW',[points(obj('BONNET_EDGE'))[0].co,points(obj('HEADLIGHT'))[0].co,points(obj('FRONT_BUMPER'))[0].co],'front')
 for n,idx in [('A_PILLAR',-1),('ROOF_EDGE',0)]:
  for attr,v in zip(['co','handle_left','handle_right'],j03[n]):setattr(points(obj(n))[idx],attr,v)
 # Shared longitudinal continuations use a common local flow, unlike transverse section crossings.
 for an,ai,bn,bi in [('SHOULDER',-1,'REAR_QUARTER_RETURN',1),('REAR_QUARTER_RETURN',-1,'REAR_BUMPER',1)]:
  pa,pb=points(obj(an))[ai],points(obj(bn))[bi];ap=points(obj(an))[ai-1];bc=points(obj(bn))[bi+1]
  t=((pa.co-ap.co).normalized()+(bc.co-pb.co).normalized()).normalized()
  al=(pa.co-ap.co).length/3;bl=(bc.co-pb.co).length/3
  pa.handle_left=pa.co-t*al;pa.handle_right=pa.co+t*al;pb.handle_left=pb.co-t*bl;pb.handle_right=pb.co+t*bl
 # Every edit is authored on one side. Replace mirrors after all local changes.
 for o in list(col.objects):
  if o.name.endswith('_R') or o.get('depth_slice'):continue
  ps=points(o);mirror=col.objects.get(o.name+'_R')
  if mirror is None and not any(abs(b.co.y)>1e-8 for b in ps):continue
  if mirror is None or len(points(mirror))!=len(ps):
   mirror=replace(o.name+'_R',[Vector((b.co.x,-b.co.y,b.co.z)) for b in ps],o.get('trace_class'))
  for a,b in zip(ps,points(mirror)):
   for attr in ['co','handle_left','handle_right']:
    v=getattr(a,attr);setattr(b,attr,(v.x,-v.y,v.z))
  mirror.data.splines[0].use_cyclic_u=o.data.splines[0].use_cyclic_u
  # Reset from the near-side colour so repeated regeneration cannot progressively dim mirrors.
  mat=bpy.data.materials.get('V03 far '+o.name) or o.data.materials[0].copy();mat.name='V03 far '+o.name
  color=o.data.materials[0].diffuse_color;shade=tuple(c*.18 for c in color[:3])+(1,);mat.diffuse_color=shade;bs=mat.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=shade;bs.inputs['Emission Color'].default_value=shade;bs.inputs['Emission Strength'].default_value=.1
  mirror.data.materials.clear();mirror.data.materials.append(mat)
 for n,base in protected.items():
  assert all(all((getattr(b,attr)-v).length==0 for attr,v in zip(['co','handle_left','handle_right'],row)) for b,row in zip(points(obj(n)),base)),n
 flow={code:join_samples(obj(a),ai,obj(b),bi) for code,a,ai,b,bi in [('J03','A_PILLAR',-1,'ROOF_EDGE',0),('J04','ROOF_EDGE',-1,'D_PILLAR',0),('J05','SHOULDER',-1,'REAR_QUARTER_RETURN',1),('J07','REAR_QUARTER_RETURN',-1,'REAR_BUMPER',1)]}
 flow['J01']={'section_to_bonnet_gap_m':(points(obj('FENDER_TO_BONNET'))[-1].co-sample_x(obj('BONNET_EDGE'),-p['wheelbase']/2)).length,'section_to_fender_gap_m':(points(obj('FENDER_TO_BONNET'))[0].co-sample_x(obj('FRONT_FENDER_CROWN'),-p['wheelbase']/2)).length,'type':'transverse roll; longitudinal tangent is not a G1 requirement'}
 flow['J02']={'gap_m':(points(obj('A_PILLAR'))[0].co-points(obj('BONNET_EDGE'))[-1].co).length,'type':'cowl character break with blend guide'}
 flow['J06']={'gap_m':(q[1].co-lamp[4].co).length,'type':'lamp envelope character cut'}
 flow['J08']={'gap_m':(points(obj('D_TO_REAR_GLASS'))[-1].co-glass[4].co).length,'type':'glass/pillar character cut'}
 scene['v03_flow_constraints']=json.dumps(flow)
 build_combs(scene,col)
 scene['v03_curvature_audit']=json.dumps(curvature_audit(col));scene['v03_j03_preserved']=True
 return col

def join_samples(a,ai,b,bi):
 pa,pb=points(a),points(b);ai%=len(pa);bi%=len(pb)
 left=[cubic(pa[ai-1],pa[ai],t)[2] for t in [.8,.9,.98,1]]
 right=[cubic(pb[bi],pb[bi+1],t)[2] for t in [0,.02,.1,.2]]
 dl=cubic(pa[ai-1],pa[ai],1)[1];dr=cubic(pb[bi],pb[bi+1],0)[1]
 return {'gap_m':(pa[ai].co-pb[bi].co).length,'tangent_angle_deg':math.degrees(dl.angle(dr,0)),'curvature_before':left,'curvature_after':right,'relative_curvature_jump':abs(left[-1]-right[0])/max(left[-1],right[0],1e-6)}

def build_combs(scene,col):
 name='TOLI_CAGE_COMBS';old=bpy.data.collections.get(name)
 if old:
  for o in list(old.objects):
   d=o.data;bpy.data.objects.remove(o,do_unlink=True)
   if d.users==0:bpy.data.curves.remove(d)
  bpy.data.collections.remove(old)
 combs=bpy.data.collections.new(name);scene.collection.children.link(combs)
 for n in ['TRACE_BONNET_EDGE','TRACE_FRONT_FENDER_CROWN','TRACE_SHOULDER','TRACE_ROOF_EDGE','TRACE_D_PILLAR','TRACE_REAR_QUARTER_RETURN']:
  data=bpy.data.curves.new('COMB_'+n,'CURVE');data.dimensions='3D';data.bevel_depth=.001
  ps=points(col.objects[n])
  for a,b in zip(ps,ps[1:]):
   for t in [.1,.3,.5,.7,.9]:
    co,d,k=cubic(a,b,t);before=cubic(a,b,max(0,t-.01))[1].normalized();after=cubic(a,b,min(1,t+.01))[1].normalized();normal=(after-before).normalized();tip=co+normal*min(.12,k*.025)
    for sign in [-1,1]:
     sp=data.splines.new('POLY');sp.points.add(1)
     sp.points[0].co=(co.x,sign*co.y,co.z,1);sp.points[1].co=(tip.x,sign*tip.y,tip.z,1)
  o=bpy.data.objects.new('COMB_'+n,data);combs.objects.link(o);o['comb_source']=n;o.hide_viewport=True;o.hide_render=True
 return combs

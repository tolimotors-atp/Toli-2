"""V04 bounded, reference-linked edits of existing V03 controls only.
shortcut: image-space width fitting cannot solve longitudinal depth; stop at the cage gate.
"""
import bpy,math,json
from mathutils import Vector
from .flow_cage import generate_cage as v03,points,shape_handles,sample_x,join_samples,curvature_audit,build_combs,cubic
from .depth_cage import STATIONS,LEVELS,width
from .reference_cage import COL
from ..convergence_data import FRONT,REAR

def fractions(col,p,view):
 rows=FRONT if view=='front' else REAR
 def span(n):return 2*max(abs(b.co.y) for b in points(col.objects[n]))/p['width']
 out={}
 for label,n,*_ in rows:
  if n in ['BODY','QUARTER']:v=1.
  elif n=='TIRES':v=p['track']/p['width']
  elif n=='ROOF':v=2*abs(points(col.objects['TRACE_ROOF_EDGE'])[-1].co.y)/p['width']
  elif n=='SHOULDER':v=2*abs(points(col.objects['TRACE_SHOULDER'])[-1].co.y)/p['width']
  elif n=='GLASS_BAND':v=(1-span('TRACE_REAR_GLASS'))/2
  elif n=='LOWER_BUMPER':v=2*abs(points(col.objects['TRACE_REAR_BUMPER'])[2].co.y)/p['width']
  elif n in ['LAMP_OUTER','LAMP_INNER']:
   ps=points(col.objects['TRACE_HEADLIGHT' if view=='front' else 'TRACE_TAIL_LAMP']);ys=[abs(b.co.y) for b in ps];v=2*(max(ys) if n=='LAMP_OUTER' else min(ys))/p['width']
  else:v=span(n)
  out[label]=v
 return out

def generate_cage(scene,p):
 col=v03(scene,p);w=p['width'];sx=p['length']/4.825;sy=w/1.86;sz=p['height']/1.86
 original_count={o.name:len(points(o)) for o in col.objects};baseline={v:fractions(col,p,v) for v in ['front','rear']}
 locked={n:[[(getattr(b,a)).copy() for a in ['co','handle_left','handle_right']] for b in points(col.objects[n])] for n in ['TRACE_SIDE_MASTER','TRACE_FRONT_WINDOW','TRACE_REAR_WINDOW','TRACE_BONNET_CENTER','TRACE_ROOF_CENTER']}
 j03={n:[getattr(points(col.objects[n])[i],a).copy() for a in ['co','handle_left','handle_right']] for n,i in [('TRACE_A_PILLAR',-1),('TRACE_ROOF_EDGE',0)]}
 def obj(n):return col.objects[n if n in col.objects else 'TRACE_'+n]
 def ps(n):return points(obj(n))
 def fit(n,fraction):
  scale=fraction*w/2/max(abs(b.co.y) for b in ps(n))
  for b in ps(n):
   for a in ['co','handle_left','handle_right']:v=getattr(b,a).copy();v.y*=scale;setattr(b,a,v)
 def lamp_fit(n,outer,inner):
  ys=[abs(b.co.y) for b in ps(n)];lo,hi=min(ys),max(ys)
  for b in ps(n):b.co.y=-(inner+(abs(b.co.y)-lo)/(hi-lo)*(outer-inner))*w/2
  shape_handles(obj(n))
 def z_front(v):
  knots=[(132,1.86),(249,1.30),(350,.88),(480,0)]
  for (a,za),(b,zb) in zip(knots,knots[1:]):
   if v<=b:return (za+(v-a)/(b-a)*(zb-za))*sz
  return 0.
 # Frontal widths are paired source-image proportions; depth remains inferred.
 for n,f in [('BONNET_FRONT',.853),('WINDSCREEN_BOTTOM',.780),('GRILLE_UPPER',.406),('GRILLE_SURROUND',.588),('GRILLE_LOWER',.397),('FRONT_LOWER_OPENING',.530),('FRONT_BUMPER',.970)]:fit(n,f)
 lamp_fit('HEADLIGHT',.860,.430)
 for n,rows in [('GRILLE_UPPER',[316,319,319]),('GRILLE_SURROUND',[307,334,357,359]),('GRILLE_LOWER',[361,367,367]),('FRONT_LOWER_OPENING',[371,397,398]),('FRONT_BUMPER',[334,389,426,434,434])]:
  for b,v in zip(ps(n),rows):b.co.z=z_front(v)
  shape_handles(obj(n))
 # Recompute front corner depth with the updated lateral placement, retaining established face layers.
 for n,base,wrap in [('GRILLE_UPPER',-2.36,.18),('GRILLE_SURROUND',-2.38,.18),('GRILLE_LOWER',-2.39,.18),('FRONT_LOWER_OPENING',-2.40,.18),('FRONT_BUMPER',-2.4125,.32)]:
  for b in ps(n):b.co.x=(base+wrap*(abs(b.co.y)/(w/2))**2)*sx
  shape_handles(obj(n))
 # Paint/cowl and inner glass are distinct widths; J03 stays fixed.
 ps('BONNET_EDGE')[-2].co.y=-.801*sy;ps('BONNET_EDGE')[-1].co.y=-.790*sy;shape_handles(obj('BONNET_EDGE'));ps('A_PILLAR')[0].co=ps('BONNET_EDGE')[-1].co.copy()
 ps('A_PILLAR')[1].co.y=(ps('A_PILLAR')[0].co.y+ps('A_PILLAR')[-1].co.y)*.5;shape_handles(obj('A_PILLAR'))
 for i in range(5):
  sec=ps('SECTION_BONNET_'+str(i));x=sec[4].co.x;e=sample_x(obj('BONNET_EDGE'),x);c=sample_x(obj('BONNET_CENTER'),x);outer=width(x,'maximum',p);roll=(abs(e.y)+outer)/2
  left=[Vector((x,-outer,e.z-.095*sz)),Vector((x,-roll,e.z-.026*sz)),e,Vector((x,e.y*.55,c.z-(c.z-e.z)*.12)),c]
  co=left+[Vector((v.x,-v.y,v.z)) for v in reversed(left[:-1])]
  for b,v in zip(sec,co):b.co=v
  shape_handles(obj('SECTION_BONNET_'+str(i)))
 x=-p['wheelbase']/2;e=sample_x(obj('BONNET_EDGE'),x);f=sample_x(obj('FRONT_FENDER_CROWN'),x)
 for b,v in zip(ps('FENDER_TO_BONNET'),[f,Vector((x,(e.y+f.y)/2,e.z-.035*sz)),e]):b.co=v
 shape_handles(obj('FENDER_TO_BONNET'))
 root=ps('A_PILLAR')[0].co
 for b,v in zip(ps('COWL_ROOT_BLEND'),[sample_x(obj('BONNET_EDGE'),root.x-.10*sx),root,ps('A_PILLAR')[1].co.lerp(root,.65)]):b.co=v
 shape_handles(obj('COWL_ROOT_BLEND'))
 for b,v in zip(ps('FRONT_CORNER_FLOW'),[ps('BONNET_EDGE')[0].co,ps('HEADLIGHT')[0].co,ps('FRONT_BUMPER')[0].co]):b.co=v
 shape_handles(obj('FRONT_CORNER_FLOW'))
 # A defined quarter-glass cut uses shorter handles; control landmarks remain fixed.
 for i in [0,2,3,4]:
  b=ps('QUARTER_GLASS')[i];b.handle_left=b.co+(b.handle_left-b.co)*.72;b.handle_right=b.co+(b.handle_right-b.co)*.72
 d=ps('D_PILLAR');d[1].co.y=-.735*sy;d[-1].co.y=-.820*sy;shape_handles(obj('D_PILLAR'))
 for bp in ps('REAR_FENDER_CROWN'):
  dx=(bp.co.x-p['wheelbase']/2)/sx;bp.co.z-=.006*math.exp(-(dx/(.48 if dx<0 else .68))**2)*sz
 shape_handles(obj('REAR_FENDER_CROWN'))
 lamp_fit('TAIL_LAMP',.980,.480);ps('TAIL_LAMP')[0].co.x=2.065*sx;ps('TAIL_LAMP')[4].co.x=2.09*sx;shape_handles(obj('TAIL_LAMP'))
 q=ps('REAR_QUARTER_RETURN');sh=ps('SHOULDER');q[1].co=ps('TAIL_LAMP')[4].co.copy();sh[-1].co=q[1].co.copy();shape_handles(obj('SHOULDER'))
 for b,v in zip(ps('SHOULDER_TO_QUARTER'),[sh[4].co,sh[5].co,sh[-1].co]):b.co=v
 shape_handles(obj('SHOULDER_TO_QUARTER'))
 for b,v in zip(ps('QUARTER_TO_LAMP'),[q[0].co,ps('TAIL_LAMP')[0].co,ps('TAIL_LAMP')[4].co]):b.co=v
 shape_handles(obj('QUARTER_TO_LAMP'))
 bump=ps('REAR_BUMPER');bump[0].co.y=bump[1].co.y=-.955*w/2;bump[2].co.y=-.855*w/2;q[-1].co=bump[1].co.copy();shape_handles(obj('REAR_QUARTER_RETURN'));shape_handles(obj('REAR_BUMPER'))
 glass=ps('REAR_GLASS');glass[4].co.y=-.850*w/2;glass[5].co.y=-.765*w/2;shape_handles(obj('REAR_GLASS'))
 for b,v in zip(ps('D_TO_REAR_GLASS'),[d[-1].co,Vector((2.22*sx,-.805*sy,1.28*sz)),glass[4].co]):b.co=v
 shape_handles(obj('D_TO_REAR_GLASS'))
 for b,v in zip(ps('REAR_ROOF_GLASS_RETURN'),[ps('ROOF_EDGE')[-1].co,glass[0].co]):b.co=v
 shape_handles(obj('REAR_ROOF_GLASS_RETURN'))
 for b,v in zip(ps('QUARTER_TO_BUMPER'),[q[2].co,bump[0].co,bump[1].co]):b.co=v
 shape_handles(obj('QUARTER_TO_BUMPER'))
 for b,v in zip(ps('REAR_BUMPER_RETURN'),[q[-1].co,bump[2].co,ps('REAR_LOWER_TRIM')[0].co]):b.co=v
 shape_handles(obj('REAR_BUMPER_RETURN'))
 for n,left in [('SECTION_REAR_GLASS',[glass[4].co,Vector((2.215*sx,-.44*sy,1.32*sz)),glass[3].co]),('SECTION_LAMP_BAND',[ps('TAIL_LAMP')[4].co,Vector((2.24*sx,-.68*sy,1.10*sz)),Vector((2.32*sx,0,1.16*sz))]),('SECTION_UPPER_BUMPER',[bump[0].co,Vector((2.36*sx,-.50*sy,.66*sz)),Vector((2.39*sx,0,.66*sz))]),('SECTION_LOWER_BUMPER',[bump[2].co,Vector((2.40*sx,-.40*sy,.285*sz)),bump[3].co])]:
  co=[v.copy() for v in left]+[Vector((v.x,-v.y,v.z)) for v in reversed(left[:-1])]
  for b,v in zip(ps(n),co):b.co=v
  shape_handles(obj(n))
 ps('SECTION_D_BODY')[1].co.y=-.82*sy;ps('SECTION_D_BODY')[-2].co.y=.82*sy;ps('SECTION_D_BODY')[2].co.y=-.735*sy;ps('SECTION_D_BODY')[-3].co.y=.735*sy;shape_handles(obj('SECTION_D_BODY'))
 # Balance only soft continuation handles within ±15%; preserve all feature cuts and J03.
 balances={}
 for code,an,ai,bn,bi in [('J04','ROOF_EDGE',-1,'D_PILLAR',0),('J05','SHOULDER',-1,'REAR_QUARTER_RETURN',1),('J07','REAR_QUARTER_RETURN',-1,'REAR_BUMPER',1)]:
  pa,pb=ps(an)[ai],ps(bn)[bi];before=join_samples(obj(an),ai,obj(bn),bi)
  t=((pa.co-ps(an)[ai-1].co).normalized()+(ps(bn)[bi+1].co-pb.co).normalized()).normalized();la=(pa.co-ps(an)[ai-1].co).length/3;lb=(ps(bn)[bi+1].co-pb.co).length/3
  best=None
  for fa in [.85,1.,1.15]:
   for fb in [.85,1.,1.15]:
    pa.handle_left=pa.co-t*la*fa;pb.handle_right=pb.co+t*lb*fb;m=join_samples(obj(an),ai,obj(bn),bi);score=m['relative_curvature_jump']+.02*(abs(math.log(fa))+abs(math.log(fb)))
    if best is None or score<best[0]:best=(score,fa,fb,m)
  pa.handle_left=pa.co-t*la*best[1];pa.handle_right=pa.co+t*la*best[1];pb.handle_left=pb.co-t*lb*best[2];pb.handle_right=pb.co+t*lb*best[2]
  balances[code]={'before':before,'after':join_samples(obj(an),ai,obj(bn),bi),'handle_multipliers':best[1:3]}
 for n,i in [('TRACE_A_PILLAR',-1),('TRACE_ROOF_EDGE',0)]:
  for a,v in zip(['co','handle_left','handle_right'],j03[n]):setattr(points(col.objects[n])[i],a,v)
 # A glass perimeter must not close each half through the centre of the aperture.
 old=[b.co.copy() for b in ps('REAR_GLASS')]
 for b,i in zip(ps('REAR_GLASS'),[2,1,0,5,4,3]):b.co=old[i]
 obj('REAR_GLASS').data.splines[0].use_cyclic_u=False;shape_handles(obj('REAR_GLASS'))
 for i,sign,neighbor in [(0,-1,1),(-1,1,-2)]:
  b=ps('REAR_GLASS')[i];length=(b.co-ps('REAR_GLASS')[neighbor].co).length/3;t=Vector((0,sign*length,0));b.handle_left=b.co-t;b.handle_right=b.co+t
 for n in ['WINDSCREEN_BOTTOM','WINDSCREEN_TOP']:
  b=ps(n)[-1];t=Vector((0,abs(ps(n)[-2].co.y)/3,0));b.handle_left=b.co-t;b.handle_right=b.co+t
 # Short, defined lamp-corner handles preserve cuts instead of melted oval outlines.
 for n,indices in [('HEADLIGHT',[0,2,3]),('TAIL_LAMP',[0,2,3,4])]:
  for i in indices:
   b=ps(n)[i];b.handle_left=b.co+(b.handle_left-b.co)*.60;b.handle_right=b.co+(b.handle_right-b.co)*.60
 scene['v04_rear_glass_half_perimeter']='Open half: top centre / upper mid / upper outer / side / lower outer / lower centre; centre return removed'
 # Exact reflection of one authored side, including defined-corner handles.
 for o in list(col.objects):
  if o.name.endswith('_R') or o.get('depth_slice'):continue
  mirror=col.objects.get(o.name+'_R')
  if mirror:
   mirror.data.splines[0].use_cyclic_u=o.data.splines[0].use_cyclic_u
   for b,c in zip(points(o),points(mirror)):
    for a in ['co','handle_left','handle_right']:v=getattr(b,a);setattr(c,a,(v.x,-v.y,v.z))
 assert {o.name:len(points(o)) for o in col.objects}==original_count
 for n,base in locked.items():assert all(all((getattr(b,a)-v).length==0 for a,v in zip(['co','handle_left','handle_right'],row)) for b,row in zip(points(col.objects[n]),base)),n
 flows={code:join_samples(obj(a),ai,obj(b),bi) for code,a,ai,b,bi in [('J03','A_PILLAR',-1,'ROOF_EDGE',0),('J04','ROOF_EDGE',-1,'D_PILLAR',0),('J05','SHOULDER',-1,'REAR_QUARTER_RETURN',1),('J07','REAR_QUARTER_RETURN',-1,'REAR_BUMPER',1)]}
 flows['J01']={'section_to_bonnet_gap_m':(ps('FENDER_TO_BONNET')[-1].co-sample_x(obj('BONNET_EDGE'),-p['wheelbase']/2)).length,'section_to_fender_gap_m':(ps('FENDER_TO_BONNET')[0].co-sample_x(obj('FRONT_FENDER_CROWN'),-p['wheelbase']/2)).length,'type':'transverse roll'}
 flows['J02']={'gap_m':(ps('A_PILLAR')[0].co-ps('BONNET_EDGE')[-1].co).length,'type':'cowl character cut'}
 flows['J06']={'gap_m':(q[1].co-ps('TAIL_LAMP')[4].co).length,'type':'lamp character cut'}
 flows['J08']={'gap_m':(ps('D_TO_REAR_GLASS')[-1].co-glass[4].co).length,'type':'glass character cut'}
 scene['v04_flow_constraints']=json.dumps(flows)
 scene['v04_proportions']=json.dumps({'v03':baseline,'v04':{v:fractions(col,p,v) for v in ['front','rear']}});scene['v04_handle_balance']=json.dumps(balances);scene['v04_curvature_audit']=json.dumps(curvature_audit(col));scene['v04_no_added_controls']=True
 build_combs(scene,col)
 # Additional diagnostic combs reuse the existing sampler; no structural curves are added.
 combs=bpy.data.collections['TOLI_CAGE_COMBS']
 for name in ['COWL_ROOT_BLEND','REAR_BUMPER_RETURN']:
  data=bpy.data.curves.new('COMB_'+name,'CURVE');data.dimensions='3D';data.bevel_depth=.001
  for a,b in zip(ps(name),ps(name)[1:]):
   for t in [.1,.3,.5,.7,.9]:
    co,der,k=cubic(a,b,t);normal=(cubic(a,b,t+.01)[1].normalized()-cubic(a,b,t-.01)[1].normalized()).normalized();tip=co+normal*min(.12,k*.025)
    for sign in [-1,1]:
     sp=data.splines.new('POLY');sp.points.add(1);sp.points[0].co=(co.x,sign*co.y,co.z,1);sp.points[1].co=(tip.x,sign*tip.y,tip.z,1)
  ob=bpy.data.objects.new('COMB_'+name,data);combs.objects.link(ob);ob['comb_source']=name;ob.hide_viewport=True;ob.hide_render=True
 return col

import bpy,bmesh,math,json,os,ast
from pathlib import Path
from mathutils import Vector
O=Path(os.environ.get('MUX_V04_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';R=O/'renders/v04';g=json.loads((A/'v04-gates.json').read_text());assert g['front']=='YES' and g['side'] in ['YES','NO']
bpy.ops.wm.open_mainfile(filepath=str(D/'isuzu-mux-generated-v04.blend'));s=bpy.context.scene;s.frame_set(1);assert not bpy.data.collections.get('V04_REAR_COMPOSITION'), 'Restore the side-stage working source before repeating rear construction';body=bpy.data.objects['V03_NEW_EXTERIOR_SHELL'];paint=bpy.data.materials['Silver metallic paint'];black=bpy.data.materials['Graphite polymer'];chrome=bpy.data.materials['Brushed bright metal'];red=bpy.data.materials['Rear red lens']
front=bpy.data.collections.new('V04_REAR_COMPOSITION');s.collection.children.link(front);col=front;cuts=bpy.data.collections['V04_CONSTRUCTION_CUTTERS'];archive=bpy.data.collections['V03_IDENTITY_REFERENCE']
old=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/generated/build.py');tree=ast.parse(old.read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['mesh','cube','tube']],type_ignores=[]),'existing_mesh_helpers','exec'))
tree=ast.parse((A/'v04_front.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['put','boolean','prism','face']],type_ignores=[]),'V04_region_helpers','exec'))
# Taper the whole upper rear cabin, with its centerline roof trajectory untouched.
for v in body.data.vertices:
 x,y,z=v.co
 if 1.0<x<2.40 and z>1.28 and abs(y)>.35:
  taper=.035*math.exp(-((x-1.98)/.62)**2)*min(1,(z-1.28)/.30);v.co.y=y*(1-taper)
bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());sections={}
for name,x in [('B',.28),('C',1.14),('D',1.98),('REAR_GLASS',2.18)]:
 sections[name]={'x':x,'halfwidth_at_height':{}}
 for z in [1.32,1.50,1.68]:
  hit,co,no,idx=ev.ray_cast(Vector((x,2,z)),Vector((0,-1,0)))
  if hit:sections[name]['halfwidth_at_height'][str(z)]=float(co.y)
# Re-derive rear side glass, quarter glass and rear window from this changed common volume.
for ob in list(bpy.data.objects):
 if ob.name.startswith(('V03_COHERENT_REAR_','V03_COHERENT_QUARTER_')) or ob.name=='V03_COHERENT_REAR_GLASS':
  for c in list(ob.users_collection):c.objects.unlink(ob)
  archive.objects.link(ob)
tree=ast.parse(Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/generated/v03_greenhouse.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['roundpoly','patch']],type_ignores=[]),'V03_common_surface_helpers','exec'))
for side in [-1,1]:
 patch('V04_REAR_SIDE_GLASS_'+str(side),[(.35,1.30),(.35,1.70),(1.23,1.70),(1.20,1.43),(1.08,1.34)],'Y',side)
 patch('V04_QUARTER_GLASS_'+str(side),[(1.47,1.345),(1.40,1.69),(1.87,1.65),(2.16,1.35)],'Y',side,offset=.014)
patch('V04_REAR_GLASS',[(-.775,1.32),(.775,1.32),(.65,1.725),(-.65,1.725)],'X',1,offset=.018)
upper=[];sideback={}
for i in range(25):
 y=-.80+1.6*i/24;hit,co,no,idx=ev.ray_cast(Vector((4,y,1.355)),Vector((-1,0,0)));upper.append(tuple(co) if hit else (2.30,y,1.355))
for side in [-1,1]:
 sideback[side]=[]
 for j in range(17):
  z=.43+.91*j/16;hit,co,no,idx=ev.ray_cast(Vector((2.305,side*2,z)),Vector((0,-side,0)));sideback[side].append(tuple(co) if hit else (2.305,side*.83,z))
for ob in list(bpy.data.collections['V03_EXTERIOR'].objects):
 if ob.name.startswith(('V03_REAR_','V03_REAR_LAMP')):
  for c in list(ob.users_collection):c.objects.unlink(ob)
  archive.objects.link(ob)
boolean(body,cube('V04_CUT_OLD_REAR_CAP',(2.54,0,.85),(.47,2.2,1.0),black,0))
def rx(y,z):
 u=max(0,min(1,(z-.62)/.23));u=u*u*(3-2*u);press=.050*math.exp(-((y/.43)**4)-(((z-1.03)/.16)**4));return 2.4975-.075*(abs(y)/.86)**4-.075*u-press+.012*u*math.exp(-((y/.68)**4)-(((z-.88)/.35)**4))
ny=32;nz=18;vs=[]
for i in range(ny+1):
 y=-.86+1.72*i/ny;top=1.32+.02*(abs(y)/.86)**2
 for j in range(nz+1):z=.43+(top-.43)*j/nz;vs.append((rx(y,z),y,z))
skin=put(mesh('V04_REAR_SHARED_TAILGATE_BUMPER_SKIN',vs,[(i*(nz+1)+j,(i+1)*(nz+1)+j,(i+1)*(nz+1)+j+1,i*(nz+1)+j+1) for i in range(ny) for j in range(nz)],paint));sol=skin.modifiers.new('Rear region skin thickness','SOLIDIFY');sol.thickness=.028;sol.offset=-1
vs=[]
for back in upper:
 y=back[1];z=1.32+.02*(abs(y)/.86)**2;fore=Vector((rx(y,z),y,z));back=Vector(back)
 for j in range(5):vs.append(tuple(fore.lerp(back,j/4)))
put(mesh('V04_REAR_GLASS_LOWER_BODY_RETURN',vs,[(i*5+j,(i+1)*5+j,(i+1)*5+j+1,i*5+j+1) for i in range(24) for j in range(4)],paint))
for side in [-1,1]:
 vs=[]
 for j,back in enumerate(sideback[side]):
  z=.43+.91*j/16;vs.extend([(rx(side*.86,z),side*.86,z),back])
 put(mesh('V04_REAR_QUARTER_RETURN_'+str(side),vs,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(16)],paint))
for side in [-1,1]:
 outer=[(side*.715,1.26),(side*.855,1.29),(side*.855,1.055),(side*.715,1.04)]
 inner=[(side*.70,1.26),(side*.44,1.195),(side*.535,1.045),(side*.70,1.04)]
 for label,poly in [('OUTER',outer),('INNER',inner)]:
  boolean(skin,prism('V04_CUT_REAR_LAMP_'+label+str(side),poly,2.22,2.70));boolean(body,prism('V04_CUT_REAR_BODY_LAMP_'+label+str(side),poly,2.22,2.70));face('V04_REAR_LAMP_ENVELOPE_'+label+str(side),poly,lambda y,z:rx(y,z)-.012,red,.018)
 # A real wrap surface returns around the quarter, without optical/internal detail.
 vv=[];nx=12;nz=4
 for i in range(nx+1):
  u=i/nx;rear_x=rx(side*.855,1.18)-.012;x=2.08*(1-u)+rear_x*u
  for j in range(nz+1):
   z=(1.10*(1-u)+1.055*u)*(1-j/nz)+(1.295*(1-u)+1.29*u)*(j/nz);sample_x=min(x,2.30)
   hit,co,no,idx=body.evaluated_get(bpy.context.evaluated_depsgraph_get()).ray_cast(Vector((sample_x,side*2,z)),Vector((0,-side,0)));assert hit
   mix=max(0,min(1,(x-2.30)/max(.001,rear_x-2.30)));y=co.y*(1-mix)+side*.855*mix;vv.append((x,y+side*.006,z))
 put(mesh('V04_REAR_LAMP_QUARTER_WRAP_'+str(side),vv,[(i*(nz+1)+j,(i+1)*(nz+1)+j,(i+1)*(nz+1)+j+1,i*(nz+1)+j+1) for i in range(nx) for j in range(nz)],red))
face('V04_REAR_GARNISH_MAIN_FORM',[(-.48,1.286),(.48,1.286),(.50,1.26),(-.50,1.26)],lambda y,z:rx(y,z)+.006,chrome,.008)
insert=[(-.765,.62),(.765,.62),(.70,.465),(-.70,.465)];boolean(skin,prism('V04_CUT_BUMPER_INSERT',insert,2.22,2.70));face('V04_REAR_BUMPER_RECESSED_INSERT',insert,lambda y,z:rx(y,z)-.018,black,.012)
sections['TAILGATE']={'skin_halfwidth':.86,'broad_center_pressing_depth':.050};(A/'v04-rear-sections.json').write_text(json.dumps(sections,indent=2));s['V04_STAGE']='Complete rear-volume candidate: cabin taper, common glazing, recessed lamp/body/bumper composition; no separated hatch';bpy.ops.wm.save_as_mainfile(filepath=str(D/'isuzu-mux-generated-v04.blend'))
for name in ['FRONT','FRONT_34','SIDE','REAR_34','REAR']:
 s.camera=bpy.data.objects['CAM_COMPARE_'+name];s.render.filepath=str(R/('v04-final-'+name.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('V04 ALL REGIONS SAVED FOR REVIEW; NO FINAL SURFACE POLISH',flush=True);os._exit(0)

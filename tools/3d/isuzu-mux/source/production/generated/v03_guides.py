import bpy,json,math,os,hashlib
from pathlib import Path
from mathutils import Vector
O=Path(os.environ.get('MUX_V03_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';R=O/'renders/v03';R.mkdir(parents=True,exist_ok=True)
source=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/milestones/isuzu-mux-generated-v02.blend');bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;s.frame_set(1)
assert all(bpy.data.objects[n].animation_data.action for n in ['DOOR_FL','DOOR_FR','DOOR_RL','DOOR_RR','BONNET','TAILGATE']);(A/'v02-preserved-open.json').write_text(json.dumps({'path':str(source),'opened':True,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()},indent=2))
def descendants(o):return [o]+[z for c in o.children for z in descendants(c)]
root=bpy.data.objects['MUX_ROOT'];legacy=descendants(root);prefixes=('WHEEL_','INTERIOR','CENTER CONSOLE','Seat ','ENGINE','Engine ','Battery','Air filter','Major intake','Reservoir','Radiator','Firewall','RHD ','Steering ','Climate ','Instrument ','Center radio','Infotainment','Gear ','Cargo ')
keep=[o for o in legacy if o.type in ['MESH','CURVE'] and o.name.startswith(prefixes)];assert len(keep)==113,len(keep)
def collection(n):c=bpy.data.collections.new(n);s.collection.children.link(c);return c
ref=collection('V02_REFERENCE_BODY');ret=collection('V02_RETAINED_COMPONENTS');wheels=collection('V03_WHEELS_REUSED');guides=collection('V03_LANDMARK_GUIDES');shell=collection('V03_EXTERIOR');ret.hide_render=True;ref.hide_render=True;ref.hide_viewport=True
ancestors={root}
for ob in keep:
 p=ob.parent
 while p:ancestors.add(p);p=p.parent
for ob in legacy:
 col=wheels if ob.name.startswith('WHEEL_') else ret if ob in keep or ob in ancestors else ref
 for c in list(ob.users_collection):c.objects.unlink(ob)
 col.objects.link(ob)
 if col==ref:ob.hide_set(True)
# Wheel and original interior/engine geometry are not moved or rescaled.
paint=bpy.data.materials['Silver metallic paint'];black=bpy.data.materials['Graphite polymer']
def curve(n,points,col=guides,r=.008,closed=False):
 cu=bpy.data.curves.new(n,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=1;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for p,q in zip(sp.points,points):p.co=(*q,1)
 sp.use_cyclic_u=closed;ob=bpy.data.objects.new(n,cu);col.objects.link(ob);cu.materials.append(black);return ob
def landmark(n,co):
 ob=bpy.data.objects.new(n,None);guides.objects.link(ob);ob.location=co;ob.empty_display_type='SPHERE';ob.empty_display_size=.025;ob.show_in_front=True;return ob
outline=[(-2.3275,.54),(-2.3275,.80),(-2.26,1.06),(-1.99,1.15),(-1.4225,1.27),(-1.04,1.31),(-.34,1.755),(.28,1.80),(1.14,1.80),(1.98,1.745),(2.28,1.39),(2.4975,1.21),(2.4975,.54)]
curve('GUIDE_SIDE_UPPER',[(x,-1.01,z) for x,z in outline]);curve('GUIDE_SIDE_SILL',[(-2.3275,-1.01,.54),(-1.87,-1.01,.43),(-.97,-1.01,.43),(.97,-1.01,.43),(1.87,-1.01,.43),(2.4975,-1.01,.54)])
for x in [-1.4225,1.4225]:curve('GUIDE_ARCH_'+str(x),[(x+.445*math.cos(a),-1.01,.382+.445*math.sin(a)) for a in [math.pi*j/32 for j in range(33)]])
points={'FRONT_TIP':(-2.3275,0,.80),'REAR_TIP':(2.4975,0,.80),'FRONT_AXLE':(-1.4225,0,.382),'REAR_AXLE':(1.4225,0,.382),'BONNET_TOP':(-1.4225,0,1.27),'COWL':(-1.04,0,1.31),'ROOF_FRONT':(-.34,0,1.755),'ROOF_PEAK':(.28,0,1.80),'ROOF_REAR':(1.98,0,1.745),'WINDSCREEN_TOP':(-.34,0,1.73),'WINDSCREEN_BOTTOM':(-1.04,0,1.31),'A_PILLAR':(-.70,-.78,1.50),'B_PILLAR':(.28,-.80,1.50),'C_PILLAR':(1.32,-.79,1.53),'D_PILLAR':(2.12,-.75,1.54),'BELT_FRONT':(-.9,-.85,1.25),'BELT_REAR':(2.16,-.85,1.35),'QUARTER_GLASS':(1.76,-.78,1.52),'REAR_GLASS':(2.20,0,1.54),'FRONT_ARCH':(-1.4225,-.93,.827),'REAR_ARCH':(1.4225,-.93,.827),'GROUND':(0,0,0)}
for n,co in points.items():landmark('LM_'+n,co)
# Eleven deliberate primary stations; dimensions are family anchors, transverse/height shapes are visual estimates.
stations=[[-2.3275,.82,1.07,1.10,.60],[-2.18,.89,1.11,1.16,.65],[-1.4225,.93,1.22,1.285,.65],[-1.04,.90,1.26,1.32,.66],[-.34,.875,1.27,1.755,.70],[.28,.875,1.285,1.80,.735],[1.14,.89,1.32,1.80,.735],[1.4225,.93,1.34,1.79,.73],[1.98,.915,1.35,1.745,.70],[2.28,.895,1.32,1.40,.66],[2.4975,.845,1.21,1.24,.60]]
for i,(x,w,belt,top,rw) in enumerate(stations):curve('WIDTH_X'+str(i+1).zfill(2),[(x,-w,.8),(x,w,.8)],r=.004)
hard={'coordinate_system':'X forward negative / Y left positive / Z up','wheelbase_m':2.845,'length_m':4.825,'nominal_width_m':1.86,'nominal_height_m':1.86,'roof_crown_estimate_m':1.80,'track_m':1.570,'retained_tire_radius_m':.382,'tire_diameter_m':.764,'front_overhang_m':.905,'rear_overhang_m':1.075,'dimension_source':'https://www.isuzu.in/images/Brochure/pdf_area/ISUZU%20mu-X%20brochure.pdf','compatibility':'India MU-X same older body family, photographed exact year/trim unverified. Roof crown/cowl/belt/cross-sections and curvature are visual modeling estimates. Tire radius retained from V02; nominal tire specification checked separately.'}
ratios={'wheelbase_length':2.845/4.825,'height_wheelbase':1.86/2.845,'bonnet_length_length':1.2875/4.825,'roof_length_length':2.32/4.825,'front_overhang_wheelbase':.905/2.845,'rear_overhang_wheelbase':1.075/2.845,'tire_diameter_height':.764/1.86,'windscreen_rise_height':(.445)/1.86}
(A/'v03-guides.json').write_text(json.dumps({'hard_points':hard,'normalized_ratios':ratios,'landmarks':points,'side_upper_outline':outline,'stations':stations,'retained_components':len(keep)},indent=2));s['V03_STAGE']='2D guide only — side silhouette review required before 3D shell';s.camera=bpy.data.objects['CAM_COMPARE_SIDE'];s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='FLAT';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=False;s.display.shading.show_cavity=False;s.render.resolution_x=1200;s.render.resolution_y=800;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
bpy.ops.wm.save_as_mainfile(filepath=str(D/'milestones/isuzu-mux-v03-guides.blend'));bpy.ops.wm.save_as_mainfile(filepath=str(D/'isuzu-mux-generated-v03.blend'));s.render.filepath=str(R/'v03-guide-side.png');bpy.ops.render.render(write_still=True);print('V03 GUIDES SAVED; NO SHELL BUILT',flush=True);os._exit(0)

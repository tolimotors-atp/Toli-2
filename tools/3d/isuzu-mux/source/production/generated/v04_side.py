import bpy,bmesh,json,os,math
from pathlib import Path
from mathutils import Vector
O=Path(os.environ.get('MUX_V04_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';R=O/'renders/v04';assert json.loads((A/'v04-gates.json').read_text())['front']=='YES'
bpy.ops.wm.open_mainfile(filepath=str(D/'milestones/isuzu-mux-v04-front.blend'));s=bpy.context.scene;body=bpy.data.objects['V03_NEW_EXTERIOR_SHELL'];c=bpy.data.collections['V04_IDENTITY_GUIDES'];black=bpy.data.materials['Graphite polymer']
# Move existing cross-section points; roof, glazing rows and all wheel hard points remain untouched.
for si,z in [(3,1.12),(4,1.105),(5,1.11),(6,1.13),(7,1.14),(8,1.15)]:body.data.vertices[si*12+5].co.z=z
for si in [4,5]:
 body.data.vertices[si*12+5].co.y-=.016;body.data.vertices[si*12+4].co.y-=.010;body.data.vertices[si*12+6].co.y-=.006
for si in [3,6]:body.data.vertices[si*12+4].co.y-=.005
# Apply only the already-visible V03 mirror/subdivision, then add local edge density for real arch volume.
bpy.context.view_layer.objects.active=body;body.hide_set(False)
for mod in list(body.modifiers):
 if mod.type in ['MIRROR','SUBSURF']:bpy.ops.object.modifier_apply(modifier=mod.name)
bm=bmesh.new();bm.from_mesh(body.data)
edges=[e for e in bm.edges if all(abs(v.co.y)>.60 and .40<v.co.z<1.32 and min(abs(v.co.x-a) for a in [-1.4225,1.4225])<.80 for v in e.verts)]
bmesh.ops.subdivide_edges(bm,edges=edges,cuts=1,use_grid_fill=True);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(body.data);bm.free()
for v in body.data.vertices:
 x,y,z=v.co;ay=abs(y)
 if ay<.65 or not .40<z<1.30:continue
 r=min(math.hypot(x-a,z-.382) for a in [-1.4225,1.4225]);flare=.045*math.exp(-((r-.49)/.125)**2)-.008*math.exp(-((r-.70)/.10)**2)
 door_weight=math.exp(-((x-.20)/.90)**4);dish=.015*door_weight*math.exp(-((z-.88)/.12)**2)
 new_y=min(.9300492,ay+flare-dish);v.co.y=math.copysign(new_y,y)
bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());sections={}
def curve(name,pts):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=.004;cu.bevel_resolution=1;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,v in zip(sp.points,pts):p.co=(*v,1)
 ob=bpy.data.objects.new(name,cu);c.objects.link(ob);cu.materials.append(black)
for name,x in [('AHEAD',-1.90),('WHEEL_CENTER',-1.4225),('BEHIND',-1.04),('DOOR_TRANSITION',-.78)]:
 pts=[]
 for i in range(29):
  z=.42+.90*i/28;hit,co,no,index=ev.ray_cast(Vector((x,2,z)),Vector((0,-1,0)))
  if hit and co.y>.4:pts.append(tuple(co))
 assert len(pts)>3;(sections.setdefault(name,{})).update(x=x,points=pts);curve('V04_FENDER_SECTION_'+name,pts)
curve('V04_SHOULDER_GUIDE',[tuple(body.data.vertices[si*12+5].co) for si in range(1,9)])
(A/'v04-fender-sections.json').write_text(json.dumps(sections,indent=2));s['V04_STAGE']='Front passed relative comparison; side shoulder/fender candidate, no door cuts';bpy.ops.wm.save_as_mainfile(filepath=str(D/'isuzu-mux-generated-v04.blend'))
for name in ['FRONT_34','SIDE','REAR_34']:
 s.camera=bpy.data.objects['CAM_COMPARE_'+name];s.render.filepath=str(R/('v04-side-candidate-'+name.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('V04 SIDE CANDIDATE SAVED; NO REGIONAL PASS CLAIMED',flush=True);os._exit(0)

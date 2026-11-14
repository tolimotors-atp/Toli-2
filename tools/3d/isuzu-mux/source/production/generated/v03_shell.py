import bpy,bmesh,math,json,os
from pathlib import Path
O=Path(os.environ.get('MUX_V03_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';R=O/'renders/v03';bpy.ops.wm.open_mainfile(filepath=str(D/'milestones/isuzu-mux-v03-guides.blend'));s=bpy.context.scene;guides=json.loads((A/'v03-guides.json').read_text());assert guides['side_silhouette_gate']['status'].startswith('PASS')
bpy.data.collections['V03_LANDMARK_GUIDES'].hide_render=True;col=bpy.data.collections['V03_EXTERIOR'];paint=bpy.data.materials['Silver metallic paint'];stations=guides['stations'];vs=[]
for x,w,belt,top,rw in stations:
 for y,z in [(0,.34),(.64,.34),(w-.055,.43),(w-.025,.54),(w-.045,.72),(w,min(1.02,belt-.11)),(w-.025,belt-.045),(w-.06,belt),(rw+.035,belt+.65*(top-belt)),(rw,top-.005),(rw*.60,top+.012),(0,top+.022)]:vs.append((x,y,z))
N=12;fs=[(i*N+j,(i+1)*N+j,(i+1)*N+j+1,i*N+j+1) for i in range(len(stations)-1) for j in range(N-1)];# Fill end caps with quad strips instead of an n-gon subdivision fan.
for si in [0,len(stations)-1]:
 base=si*N;center={1:base}
 for j in range(2,N-1):center[j]=len(vs);vs.append((stations[si][0],0,vs[base+j][2]))
 for j in range(1,N-2):fs.append((base+j,base+j+1,center[j+1],center[j]))
 fs.append((base+N-2,base+N-1,center[N-2]))
# Compensate the small subdivision width loss while the fixed tire track stays unchanged.
vs=[(x,y*1.0225,z) for x,y,z in vs]
me=bpy.data.meshes.new('V03_NEW_HALF_SHELL_CAGE');me.from_pydata(vs,[],fs);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free();ob=bpy.data.objects.new('V03_NEW_EXTERIOR_SHELL',me);col.objects.link(ob);me.materials.append(paint)
for f in me.polygons:f.use_smooth=True
crease=me.attributes.new('crease_edge','FLOAT','EDGE')
for edge in me.edges:
 a,b=edge.vertices
 if a>=len(stations)*N or b>=len(stations)*N:continue
 sa,ja=divmod(a,N);sb,jb=divmod(b,N)
 if sa==sb and sa in [3,4,8,9] and min(ja,jb)>=7:crease.data[edge.index].value=.40
 elif ja==jb==7 and min(sa,sb)>=3 and max(sa,sb)<=9:crease.data[edge.index].value=.45
m=ob.modifiers.new('V03 symmetry centerline','MIRROR');m.use_axis[0]=False;m.use_axis[1]=True;m.use_clip=True;m=ob.modifiers.new('V03 broad cage subdivision','SUBSURF');m.levels=1;m.render_levels=1
cuts=bpy.data.collections.new('V03_CONSTRUCTION_CUTTERS');s.collection.children.link(cuts)
for x in [-1.4225,1.4225]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.445,depth=3,location=(x,0,.382),rotation=(math.pi/2,0,0));c=bpy.context.object;c.name='V03_ARCH_CUT_'+str(x)
 for cc in list(c.users_collection):cc.objects.unlink(c)
 cuts.objects.link(c);c.hide_render=True;c.hide_set(True);m=ob.modifiers.new('V03 wheel opening','BOOLEAN');m.object=c;m.operation='DIFFERENCE';m.solver='EXACT'
# No door, bonnet, hatch, trim or identity cutouts at the macro-volume gate.
s['V03_STAGE']='New eleven-section half shell — five-view silhouette review required';s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.use_denoising=True;s.render.resolution_x=960;s.render.resolution_y=640;s.render.resolution_percentage=100;s.camera=bpy.data.objects['CAM_COMPARE_FRONT_34'];s.frame_set(1)
def stats(ob):
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();mesh.calc_loop_triangles();d={'base_vertices':len(ob.data.vertices),'base_faces':len(ob.data.polygons),'evaluated_vertices':len(mesh.vertices),'evaluated_triangles':len(mesh.loop_triangles),'bounds_min':[min(v.co[k] for v in mesh.vertices) for k in range(3)],'bounds_max':[max(v.co[k] for v in mesh.vertices) for k in range(3)]};assert all(math.isfinite(c) for v in mesh.vertices for c in v.co);ev.to_mesh_clear();return d
(A/'v03-blockout-geometry.json').write_text(json.dumps(stats(ob),indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(D/'milestones/isuzu-mux-v03-blockout.blend'));bpy.ops.wm.save_as_mainfile(filepath=str(D/'isuzu-mux-generated-v03.blend'))
for name in ['FRONT','FRONT_34','SIDE','REAR_34','REAR']:
 s.camera=bpy.data.objects['CAM_COMPARE_'+name];s.render.filepath=str(R/('v03-blockout-'+name.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('V03 NEW SHELL SAVED; NO IDENTITY DETAILS OR PANEL CUTS',flush=True);os._exit(0)

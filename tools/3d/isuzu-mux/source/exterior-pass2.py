"""Pass 2 control-cage reconstruction. Loads and retains the reference/tire study.
blender -b tools/3d/isuzu-mux/source/milestones/isuzu-mux-body-pass1.blend -t 2 --python tools/3d/isuzu-mux/source/exterior-pass2.py
"""
import bpy, bmesh, math, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sc=bpy.context.scene
# Record the open surface topology before replacing it.
def topology(objects):
 result={}
 for o in objects:
  if o.type!='MESH':continue
  bm=bmesh.new();bm.from_mesh(o.data);unseen=set(bm.verts);components=0
  while unseen:
   components+=1;stack=[unseen.pop()]
   while stack:
    for e in stack.pop().link_edges:
     for v in e.verts:
      if v in unseen:unseen.remove(v);stack.append(v)
  result[o.name]={'components':components,'boundary_edges':sum(e.is_boundary for e in bm.edges),'vertices':len(bm.verts)};bm.free()
 return result
old=[o for o in sc.objects if o.type=='MESH' and not o.name.startswith(('WHEEL_','RIM_','REVIEW_'))]
(ROOT/'source/pass1-topology-inspection.json').write_text(json.dumps(topology(old),indent=2))
# Reflection-friendly studio camera retained; orthographic remains useful for topology review.
cam=sc.camera;cam.location=(7,6,3.0);cam.data.type='ORTHO';cam.data.ortho_scale=6.15
cam.rotation_euler=(Vector((0,0,.92))-cam.location).to_track_quat('-Z','Y').to_euler()
sc.render.resolution_x=1000;sc.render.resolution_y=650;sc.render.engine='BLENDER_WORKBENCH'
shade=sc.display.shading;shade.light='STUDIO';shade.color_type='MATERIAL';shade.show_shadows=True;shade.show_cavity=True
if not (ROOT/'renders/pass2-inspection/pass1-studio.png').exists():
 for mode in ['solid','matcap','wireframe']:
  shade.light='MATCAP' if mode=='matcap' else 'STUDIO'
  if mode=='matcap':
   lights=[l.name for l in bpy.context.preferences.studio_lights if l.type=='MATCAP'];shade.studio_light=next((n for n in lights if 'metal' in n.lower()),lights[0])
  mods=[]
  if mode=='wireframe':
   for o in old:
    m=o.modifiers.new('Inspection wire','WIREFRAME');m.thickness=.004;mods.append((o,m))
  sc.render.filepath=str(ROOT/'renders/pass2-inspection'/('pass1-'+mode+'.png'));bpy.ops.render.render(write_still=True)
  for o,m in mods:o.modifiers.remove(m)
 sc.render.engine='CYCLES';sc.cycles.samples=8;sc.render.filepath=str(ROOT/'renders/pass2-inspection/pass1-studio.png');bpy.ops.render.render(write_still=True)
for o in old:bpy.data.objects.remove(o,do_unlink=True)
paint=bpy.data.materials['Cage neutral silver'];glass=bpy.data.materials['Window area study — opaque for silhouette']
paint.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.24
# Keep study glass dark enough to judge openings without an interior; not final production glass.
glass.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value=.0
glass.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.3
# Named longitudinal design sections: x, width, belt z, upper z, upper half-width.
sections=[
 (-2.43,.81,1.145,1.46,.70), # rear bumper / hatch base
 (-2.36,.90,1.205,1.69,.75), # rear closure / D pillar
 (-2.20,.945,1.24,1.795,.765), # rear quarter
 (-1.98,.95,1.25,1.835,.77), # rear roof shoulder
 (-1.425,.95,1.25,1.85,.777), # rear axle
 (-1.10,.925,1.255,1.855,.78), # rear door
 (-.65,.919,1.255,1.855,.78), # B pillar
 (-.22,.922,1.25,1.848,.775), # front door
 (.25,.925,1.24,1.82,.758), # upper A pillar
 (.44,.928,1.23,1.76,.75), # roof/windscreen transition
 (.76,.93,1.215,1.53,.77), # windscreen
 (1.08,.939,1.20,1.295,.80), # cowl / bonnet rear
 (1.425,.955,1.18,1.265,.81), # front axle / fender crown
 (1.78,.942,1.145,1.24,.80), # hood / headlight shoulder
 (2.13,.919,1.105,1.205,.78), # grille/headlight region
 (2.31,.87,1.07,1.16,.735), # bumper corner
 (2.43,.805,1.015,1.105,.68), # front fascia
]
# Cubic Hermite between deliberate sections, no random noise or micro-surface displacement.
def at(x,j):
 for i,(a,b) in enumerate(zip(sections,sections[1:])):
  if a[0]<=x<=b[0]:
   p=sections[max(i-1,0)];n=sections[min(i+2,len(sections)-1)]
   m0=(b[j]-p[j])/(b[0]-p[0]);m1=(n[j]-a[j])/(n[0]-a[0]);t=(x-a[0])/(b[0]-a[0]);h=b[0]-a[0]
   return (2*t**3-3*t*t+1)*a[j]+(t**3-2*t*t+t)*h*m0+(-2*t**3+3*t*t)*b[j]+(t**3-t*t)*h*m1
 return sections[0 if x<0 else -1][j]
# Arch endpoints use a supported circular arc; keep wider tire envelopes unchanged.
archrad=.47
xs=[s[0] for s in sections]
for a,b in zip(sections,sections[1:]):
 for k in range(1,4):xs.append(a[0]+(b[0]-a[0])*k/4)
for c in [-1.425,1.425]:
 for i in range(25):xs.append(c+archrad*math.cos(math.pi*i/24))
# Explicit window/pillar boundaries, not independently floating glass patches.
xs+= [-2.12,-1.95,-1.35,-1.29,-.48,-.42,.28,.38,1.02,1.12]
xs=sorted(set(round(x,5) for x in xs));xs=[x for i,x in enumerate(xs) if i==0 or x-xs[i-1]>.008]
verts=[];faces=[];mats=[]
for x in xs:
 w,b,top,tw=[at(x,j) for j in [1,2,3,4]]
 hump=max(math.exp(-((x-c)/.43)**2) for c in [-1.425,1.425])
 low=.36
 for c in [-1.425,1.425]:
  d=abs(x-c)
  if d<=archrad:low=max(low,.39+math.sqrt(max(0,archrad**2-d*d)))
 # Curved door skin: rocker recess, lower outward belly, subtle character crease,
 # muscular fender and gently rolled shoulder. All same connected vertex lattice.
 shoulder=b-.08
 rows=[(w-.10,low),(w-.065,low+.022),(w-.025+.012*hump,low+.06),
       (w+.012*hump,low+(shoulder-low)*.43),
       (w-.014,shoulder-.055),(w-.027,b-.005),(w-.085,b+.022),
       (tw+.045,b+(top-b)*.48),(tw+.01,b+(top-b)*.91),
       (tw-.01,top-.008),(tw*.91,top+.008),(tw*.62,top+.027),(tw*.29,top+.038),(0,top+.041)]
 # Prevent folded side rows above tight arch crowns.
 for k in range(1,len(rows)):
  if rows[k][1]<=rows[k-1][1]:rows[k]=(rows[k][0],rows[k-1][1]+.004)
 verts.extend((x,y,z) for y,z in rows)
N=14
for i in range(len(xs)-1):
 mid=(xs[i]+xs[i+1])/2
 for j in range(N-1):
  faces.append((i*N+j,(i+1)*N+j,(i+1)*N+j+1,i*N+j+1))
  # Side windows include paint B/C pillars and substantial rear D pillar.
  window=(-1.94<mid<-1.35 or -1.29<mid<-.48 or -.42<mid<.30)
  windshield=(.44<mid<1.02 or mid<-2.20) and j>=10
  mats.append(1 if ((window and j in [6,7]) or windshield) else 0)
# Front and rear closure surfaces share the body's boundary vertices.
# Successive inset contour rings create a convex fascia volume instead of detached masks.
for front in [False,True]:
 idx=len(xs)-1 if front else 0;x=xs[idx];bottom=len(verts);verts.append((x,0,verts[idx*N][2]));edge=[bottom]+[idx*N+j for j in range(N)];zcenter=.76 if front else .99
 previous=edge
 for step,scale in enumerate([.92,.67,.36]):
  new=[]
  for j,k in enumerate(edge):
   _,y,z=verts[k];yy=y*scale;zz=zcenter+(z-zcenter)*scale
   xx=x+(1 if front else -1)*(.055+(.022 if front else .01)*math.sin(math.pi*scale))
   # Shape a broad grille/bumper recess, avoiding disconnected boolean cutouts.
   if front and .54<zz<1.02 and yy<.68:xx-=.045*(1-yy/.68)
   new.append(len(verts));verts.append((xx,yy,zz))
  for j in range(len(edge)-1):
   face=(previous[j],new[j],new[j+1],previous[j+1]);faces.append(face if front else face[::-1]);
   midz=(verts[face[0]][2]+verts[face[2]][2])/2;midy=(verts[face[0]][1]+verts[face[2]][1])/2
   # Material areas only: the identifying fascia remains a volume blockout.
   mats.append(1 if ((not front and midz>1.36 and midy<.67) or (front and .66<midz<1.03 and midy<.62)) else 0)
  previous=new
 center=len(verts);verts.append((x+(.075 if front else -.075),0,zcenter))
 for j in range(len(edge)-1):faces.append((previous[j],center,previous[j+1]) if front else (previous[j+1],center,previous[j]));mats.append(0)
me=bpy.data.meshes.new('MU_X_CONNECTED_CONTROL_CAGE');me.from_pydata(verts,[],faces);me.update()
body=bpy.data.objects.new('BODY_PASS2_CONTINUOUS',me);sc.collection.objects.link(body);me.materials.append(paint);me.materials.append(glass)
for p,m in zip(me.polygons,mats):p.material_index=m;p.use_smooth=True
# Reorient the connected component once, then mirror across the vehicle centerline.
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
# Surface outside orientation is verified using a central side-face normal.
side=next(p for p in me.polygons if abs(p.center.x)<.3 and p.center.y>.86 and .6<p.center.z<1.1)
if side.normal.y<0:
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
mirror=body.modifiers.new('Vehicle centerline symmetry','MIRROR');mirror.use_axis[0]=False;mirror.use_axis[1]=True;mirror.use_clip=True;mirror.merge_threshold=.001
sub=body.modifiers.new('One deliberate surface subdivision','SUBSURF');sub.levels=1;sub.render_levels=1
body['stage']='Connected exterior volume study, closed panels; no functional rig';body['canonical']='Silver open-panel set';body['sections']=json.dumps(sections)
sc['status']='EXTERIOR PASS 2 — NOT FOR WEBSITE; visual gate pending'
# Broader rectangular reflection sources expose contour discontinuities.
for o in sc.objects:
 if o.type=='LIGHT':
  o.data.shape='RECTANGLE';o.data.size=5.5;o.data.size_y=1.1
sc.render.engine='CYCLES';sc.cycles.samples=8
sc.render.resolution_x=1000;sc.render.resolution_y=650;sc.render.resolution_percentage=100
# Save before any render, with both milestone and master protected on disk.
bpy.context.view_layer.objects.active=body;body.select_set(True)
for path in ['source/milestones/isuzu-mux-body-pass2.blend','source/isuzu-mux-master.blend']:bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/path))
# Numeric checks support, but never replace, visual judgement.
deps=bpy.context.evaluated_depsgraph_get();stats={'vertices':0,'triangles':0,'vehicle_meshes':0,'body_control':topology([body]),'symmetry':'Mirror Y, welded centerline','production_textures':0,'functional_panels':False}
for o in sc.objects:
 if o.type=='MESH' and o.name!='REVIEW_FLOOR':
  ev=o.evaluated_get(deps);m=ev.to_mesh();m.calc_loop_triangles();assert all(math.isfinite(c) for v in m.vertices for c in v.co);stats['vertices']+=len(m.vertices);stats['triangles']+=len(m.loop_triangles);stats['vehicle_meshes']+=1;ev.to_mesh_clear()
assert stats['body_control'][body.name]['components']==1
assert len([o for o in sc.objects if o.name.startswith('WHEEL_')])==4
(ROOT/'source/pass2-statistics.json').write_text(json.dumps(stats,indent=2))
# Same six comparisons, lower perspective angle and longer lens approximates the photographs.
cam.data.type='PERSP';cam.data.lens=65
views={'front':(9.5,0,1.55),'left':(0,10.4,1.65),'right':(0,-10.4,1.65),'rear':(-9.5,0,1.55),'front-three-quarter':(7.8,6.2,3.1),'rear-three-quarter':(-7.8,6.2,3.1)}
for name,pos in views.items():
 cam.location=pos;cam.rotation_euler=(Vector((0,0,.95))-cam.location).to_track_quat('-Z','Y').to_euler();sc.render.filepath=str(ROOT/'renders'/('body-v03-'+name+'.png'));bpy.ops.render.render(write_still=True)
# Diagnostic solid/matcap/wireframe of the new body, separate from production output.
sc.render.engine='BLENDER_WORKBENCH';cam.location=(7.8,6.2,3.1);cam.rotation_euler=(Vector((0,0,.95))-cam.location).to_track_quat('-Z','Y').to_euler()
for mode in ['solid','matcap','wireframe']:
 shade.light='MATCAP' if mode=='matcap' else 'STUDIO'
 if mode=='matcap':
  lights=[l.name for l in bpy.context.preferences.studio_lights if l.type=='MATCAP'];shade.studio_light=next((n for n in lights if 'metal' in n.lower()),lights[0])
 m=None
 if mode=='wireframe':m=body.modifiers.new('Inspection wire','WIREFRAME');m.thickness=.003
 sc.render.filepath=str(ROOT/'renders/pass2-inspection'/('pass2-'+mode+'.png'));bpy.ops.render.render(write_still=True)
 if m:body.modifiers.remove(m)

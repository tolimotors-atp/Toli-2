import bpy,bmesh,json,math,ast,sys,os,shutil
from pathlib import Path
from mathutils import Vector
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';W=B/'manual-overlay-reconstruction';sys.path.insert(0,str(P/'tools/blender-addons'))
from toli_mux_generator.surface_diagnostics import setup
D=next(ast.literal_eval(n.value) for n in ast.parse((P/'tools/blender-addons/toli_mux_generator/parameters.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='BASE' for t in n.targets))
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;cols={}
for name in ['MUX_REFERENCE_CAMERAS','MUX_REFERENCE_IMAGES','MUX_WHEELS','MUX_PRIMARY_SURFACES','MUX_DEBUG','MUX_LIGHTING','MUX_VALIDATION']:
 c=bpy.data.collections.new(name);s.collection.children.link(c);cols[name]=c

def mat(n,v,r=.55):
 m=bpy.data.materials.new(n);m.diffuse_color=(v,v,v,1);m.use_nodes=True;bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=m.diffuse_color;bs.inputs['Roughness'].default_value=r;return m
clay=mat('Neutral primary automotive clay',.30);glass=mat('Diagnostic glazing region',.065);rubber=mat('Framework tires',.07);rim=mat('Plain wheel volume',.19)
for p in json.loads((W/'source/authored-control-net.json').read_text())['patches']:
 me=bpy.data.meshes.new(p['name']);me.from_pydata(p['vertices'],[],p['faces']);me.materials.append(clay);me.materials.append(glass);me.update();o=bpy.data.objects.new(p['name'],me);cols['MUX_PRIMARY_SURFACES'].objects.link(o)
 for f,mi in zip(me.polygons,p['material_indices']):f.material_index=mi;f.use_smooth=True
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 mi=o.modifiers.new('Exact Y centreline symmetry','MIRROR');mi.use_axis[0]=False;mi.use_axis[1]=True;mi.use_clip=True;mi.merge_threshold=1e-6
 su=o.modifiers.new('Low-density authored surface evaluation','SUBSURF');su.levels=su.render_levels=2
 # Finite boundary crease retains envelope; interior crown comes from authored vertices.
 counts={tuple(sorted(e.vertices)):0 for e in me.edges}
 for f in me.polygons:
  for e in f.edge_keys:counts[tuple(sorted(e))]+=1
 cr=me.attributes.new('crease_edge','FLOAT','EDGE')
 for e in me.edges:
  if counts[tuple(sorted(e.vertices))]==1 and any(abs(me.vertices[v].co.y)>1e-6 for v in e.vertices):cr.data[e.index].value=.6
 o['surface_method']='Manually authored explicit low-density control net';o['approved']=False
centres={}
for axle,x in [('FRONT',-D['wheelbase']/2),('REAR',D['wheelbase']/2)]:
 for side,y in [('NEG_Y',-D['track']/2),('POS_Y',D['track']/2)]:
  center=(x,y,D['tire_diameter']/2);name=f'Wheel_{axle}_{side}';centres[name]=list(center)
  bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=8,location=center,rotation=(math.pi/2,0,0),major_radius=.29,minor_radius=.092)
  o=bpy.context.object;o.name=name
  for c in list(o.users_collection):c.objects.unlink(o)
  cols['MUX_WHEELS'].objects.link(o);o.data.materials.append(rubber)
  for f in o.data.polygons:f.use_smooth=True
  bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.235,depth=.13,location=center,rotation=(math.pi/2,0,0));o=bpy.context.object;o.name=name+'_plain_rim'
  for c in list(o.users_collection):c.objects.unlink(o)
  cols['MUX_WHEELS'].objects.link(o);o.data.materials.append(rim)
# Wheel milestone is saved before primary surface release, so anchors remain independently inspectable.
s['nominal_framework']=json.dumps(D);s['wheel_centres']=json.dumps(centres);s['visual_approval']='PENDING';s['branch']='MANUAL OVERLAY V01 — PRIMARY BODY ONLY'
fits=json.loads((W/'cameras/reference-fits.json').read_text());sel={r['id']:r for r in json.loads((W/'references/selection.json').read_text())}
for f in fits:
 d=bpy.data.cameras.new('REFERENCE_FIT_'+f['id']);o=bpy.data.objects.new(d.name,d);cols['MUX_REFERENCE_CAMERAS'].objects.link(o);o.location=f['position'];target=Vector(f['target']);o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
 if f['type']=='ORTHO':d.type='ORTHO';d.ortho_scale=f['ortho_scale'];o.rotation_euler=(0,0,0)
 else:
  d.type='PERSP';d.lens=f['lens_mm_assumed_36mm_sensor'];d.sensor_width=36;d.sensor_fit='HORIZONTAL';cx,cy=f['principal_point'];d.shift_x=(400-cx)/800;d.shift_y=(cy-260)/800
 o['camera_status']='REFERENCE-FIT — NOT CALIBRATED';o['confidence']=f['confidence'];o['fit_rms_pixels']=f.get('fit_rms_pixels') or -1
 d.show_background_images=True;bg=d.background_images.new();bg.image=bpy.data.images.load(str(W/'normalized'/f"{int(f['id'][-3:]):03}.png"),check_existing=True);bg.alpha=.5;bg.display_depth='FRONT';bg.frame_method='FIT'
setup(s)
for o in list(bpy.data.objects):
 if o.type=='LIGHT':
  for c in list(o.users_collection):c.objects.unlink(o)
  cols['MUX_LIGHTING'].objects.link(o)
 if o.name.startswith('PROTO_') and o.type in ['MESH','CAMERA']:
  for c in list(o.users_collection):c.objects.unlink(o)
  cols['MUX_VALIDATION'].objects.link(o)
s.camera=bpy.data.objects['REFERENCE_FIT_MUX-016'];s.render.resolution_x=800;s.render.resolution_y=520;s.render.image_settings.color_mode='RGBA';s.render.film_transparent=True;s.cycles.samples=8;s.render.threads_mode='FIXED';s.render.threads=4
for o in bpy.data.objects:
 if o.name.startswith('PROTO_STRIP'):o.hide_render=True
s['overlay_instructions']='Run text overlay_tools.py once; Camera View > N > MU-X Overlay. Switch scene camera there. All cameras are visual reference fits.'
text=bpy.data.texts.new('overlay_tools.py');text.write((W/'source/overlay_tools.py').read_text());readme=bpy.data.texts.new('READ_ME_FIRST');readme.write('PRIMARY BODY ONLY / NOT APPROVED.\n'+s['overlay_instructions']+'\nNominal dimensions are constraints, not measured vehicle geometry. No export or website integration.')
for im in bpy.data.images:
 if im.source=='FILE':im.pack()
# Multiple non-overwriting saved checkpoints within this branch.
master=B/'source/production/isuzu-mux-manual-overlay-v01.blend';assert not master.exists()
bpy.ops.wm.save_as_mainfile(filepath=str(master));shutil.copy2(master,W/'milestones/isuzu-mux-manual-overlay-primary-body-v01.blend')
print('SAVED',master,flush=True);os._exit(0)

import bpy,sys,json,hashlib,os
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'tools/blender-addons'))
import toli_mux_generator as addon
from toli_mux_generator.geometry.depth_cage import generate_cage,STATIONS,LEVELS
from toli_mux_generator.geometry.reference_cage import COL
from toli_mux_generator.cage_ui import support
from toli_mux_generator.parameters import BASE
from toli_mux_generator.operators import cameras
r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v02';r.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);addon.register();s=bpy.context.scene;p=dict(BASE,quality='PREVIEW')
def sig():
 return hashlib.sha256(json.dumps([(o.name,[[list(b.co),list(b.handle_left),list(b.handle_right)] for b in o.data.splines[0].bezier_points]) for o in sorted(bpy.data.collections[COL].objects,key=lambda o:o.name)]).encode()).hexdigest()
generate_cage(s,p);a=sig();generate_cage(s,p);assert a==sig()
co=[b.co.copy() for o in bpy.data.collections[COL].objects for b in o.data.splines[0].bezier_points]
err=max(min((Vector((v.x,-v.y,v.z))-w).length for w in co) for v in co);assert err==0,err
support(s,p);assert len(bpy.data.collections['TOLI_CAGE_SUPPORT'].objects)==5
for o in bpy.data.collections['TOLI_CAGE_SUPPORT'].objects:
 if o.name.startswith('CAGE_WHEEL'):assert abs(abs(o.location.x)-p['wheelbase']/2)<1e-6 and abs(o.location.z-p['tire_diameter']/2)<1e-6
wheelmat=bpy.data.materials.new('Diagnostic graphite wheels');wheelmat.diffuse_color=(.09,.105,.12,1);wheelmat.use_nodes=True;wheelmat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=wheelmat.diffuse_color
for o in bpy.data.collections['TOLI_CAGE_SUPPORT'].objects:
 if o.type=='MESH' and o.name.startswith('CAGE_WHEEL'):o.data.materials.append(wheelmat)
for key in ['front','side','rear','threequarter']:setattr(s.toli_mux,'reference_'+key,True)
s.toli_mux.curve_cage_only=True;cameras(s)
s.world=bpy.data.worlds.new('Cage background');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.04,.04,.04,1)
d=bpy.data.lights.new('Cage studio','AREA');d.energy=1500;d.size=5;o=bpy.data.objects.new('Cage studio',d);s.collection.objects.link(o);o.location=(-4,-4,6);o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
s.render.engine='CYCLES';s.cycles.samples=12;s.render.resolution_x=960;s.render.resolution_y=640;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA'
col=bpy.data.collections[COL]
validation={'control_point_symmetry_m':err,'regeneration':'PASS','fixed_wheels':'PASS','curves':len(col.objects),'control_points':len(co),'side_xz_max_edit_m':s['v02_side_max_xz_change_m'],'joins':json.loads(s['v02_join_measurements']),'width_stations':[{ 'name':n,'x':x,**dict(zip(LEVELS,w))} for n,x,w in STATIONS],'body_surfaces':'NOT STARTED','glb':'NOT EXPORTED'}
(r/'cage-validation.json').write_text(json.dumps(validation,indent=2))
(r/'coordinates.json').write_text(json.dumps({o.name:{'class':o.get('trace_class'),'points':[list(b.co) for b in o.data.splines[0].bezier_points]} for o in col.objects},indent=2))
# Save with all structural geometry intact; slices optional in the sidebar.
bpy.ops.wm.save_as_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v02.blend'))
for view in ['FRONT','FRONT34','SIDE','REAR34','REAR']:
 for o in col.objects:
  kind=o.get('trace_class');o.hide_render=bool(o.get('station_slice')) or (view=='FRONT' and kind not in ['front','section']) or (view=='REAR' and kind not in ['rear','section']) or (view=='SIDE' and kind in ['front','rear'])
 s.camera=bpy.data.objects['CAM_'+view];s.render.filepath=str(r/(view.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('V02 SAVED; CAGE ONLY',flush=True);os._exit(0)

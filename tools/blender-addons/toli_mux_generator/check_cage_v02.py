import bpy,sys,json,os,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'tools/blender-addons'))
import toli_mux_generator as a
from toli_mux_generator.geometry.reference_cage import COL,project
from toli_mux_generator.traced_data import TRACES
from toli_mux_generator.geometry.depth_cage import LEVELS,STATIONS
from toli_mux_generator import validation
from toli_mux_generator.geometry.soft_body import generate_soft
from toli_mux_generator.geometry.rounded import ROUNDED
from toli_mux_generator.parameters import BASE,values
r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v02';a.register();bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v02.blend'))
def sig():return hashlib.sha256(json.dumps([(o.name,[[list(v.co),list(v.handle_left),list(v.handle_right)] for v in o.data.splines[0].bezier_points]) for o in sorted(bpy.data.collections[COL].objects,key=lambda o:o.name)]).encode()).hexdigest()
bpy.ops.toli_mux.reference_cage();before=sig();bpy.ops.toli_mux.reference_cage();assert before==sig()
s=bpy.context.scene;s.toli_mux.curve_cage_only=False;assert bpy.data.collections[COL].hide_viewport;s.toli_mux.curve_cage_only=True;assert not bpy.data.collections[COL].hide_viewport
s.toli_mux.show_depth_slices=True;s.toli_mux.depth_station='cowl';assert not bpy.data.objects['SLICE_cowl'].hide_viewport;assert bpy.data.objects['SLICE_rear_wheel'].hide_viewport
s.toli_mux.show_depth_slices=False;assert all(o.hide_viewport for o in bpy.data.collections[COL].objects if o.get('station_slice'))
assert len({tuple(round(w[i]/w[2],5) for _,x,w in STATIONS) for i in range(7)})==7
assert len([o for o in bpy.data.collections[COL].objects if o.name.startswith('SECTION_BONNET_')])==5
for o in bpy.data.collections[COL].objects:
 if o.name.startswith('SECTION_BONNET_'):
  ps=o.data.splines[0].bezier_points;assert ps[2].co.z>ps[0].co.z and ps[2].co.y==0
for name in ['SIDE_MASTER','FRONT_WINDOW','REAR_WINDOW','QUARTER_GLASS','BONNET_CENTER']:
 src,uv,dep,closed=TRACES[name];ps=bpy.data.objects['TRACE_'+name].data.splines[0].bezier_points
 assert all(abs(b.co.x-project(src,pixel,dep,values(s)).x)<1e-7 and abs(b.co.z-project(src,pixel,dep,values(s)).z)<1e-7 for b,pixel in zip(ps,uv)),name
joins=json.loads(s['v02_join_measurements']);assert len(joins)==9
for j in joins:
 assert j['position_error_m']==0,j
 if j['type']=='soft':assert j['tangent_angle_deg']<.05,j
out={'locked_side_silhouette_and_window_xz':'PASS','join_endpoints_and_soft_tangents':'PASS','registered_ui_regeneration':'PASS','cage_visibility':'PASS','selected_width_station_toggle':'PASS','independent_width_profiles':'PASS','five_crowned_bonnet_sections':'PASS'}
(r/'addon-tests.json').write_text(json.dumps(out,indent=2));bpy.ops.wm.read_factory_settings(use_empty=True);validation.COLLECTION=ROUNDED;top={}
for mode in ['PREVIEW','QUALITY']:
 p=dict(BASE,quality=mode);generate_soft(bpy.context.scene,p);v=validation.validate(bpy.context.scene,p);v['scope']='Legacy soft-body regression only; V02 is curves, not a surfaced body';assert v['degenerate_faces']==0 and v['nonmanifold_edges']==0 and v['symmetry'];top[mode]=v
(r/'topology-regression.json').write_text(json.dumps(top,indent=2));print(json.dumps(out),flush=True);print(json.dumps(top),flush=True);os._exit(0)

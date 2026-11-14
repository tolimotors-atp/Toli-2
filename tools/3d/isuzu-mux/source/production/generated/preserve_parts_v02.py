import bpy,json,hashlib,os
from pathlib import Path
O=Path(os.environ.get('MUX_V02_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';p=D/'isuzu-mux-generated-master.blend'
prefixes=('WHEEL_','INTERIOR','CENTER CONSOLE','Seat ','ENGINE','Engine ','Battery','Air filter','Major intake','Reservoir','Radiator','Firewall','RHD ','Steering ','Climate ','Instrument ','Center radio','Infotainment','Gear ','Cargo ')
def snapshot():
 out={}
 for ob in bpy.data.objects:
  if ob.type in ['MESH','CURVE'] and ob.name.startswith(prefixes):
   if ob.type=='MESH':co=[[round(c,6) for c in v.co] for v in ob.data.vertices]
   else:co=[[round(c,6) for c in pt.co] for sp in ob.data.splines for pt in sp.points]
   vals=[co,[[round(c,6) for c in row] for row in ob.matrix_world],[m.name for m in ob.data.materials]];out[ob.name]=hashlib.sha256(json.dumps(vals).encode()).hexdigest()
 return out
bpy.ops.wm.open_mainfile(filepath=str(p));bpy.context.scene.frame_set(1);bpy.context.view_layer.update();after=snapshot();topology={n:len(bpy.data.objects[n].data.vertices) for n in ['BODY — editable half control cage','WINDSCREEN','ROOF — longitudinal crown cage']}
bpy.ops.wm.open_mainfile(filepath=str(D/'milestones/isuzu-mux-generated-v01.blend'));bpy.context.scene.frame_set(1);bpy.context.view_layer.update();before=snapshot();diff=[n for n,h in before.items() if after.get(n)!=h];assert not diff,diff
assert topology=={n:len(bpy.data.objects[n].data.vertices) for n in topology}
bpy.ops.wm.open_mainfile(filepath=str(p));(A/'retained-parts-v02.json').write_text(json.dumps({'passed':True,'checked_parts':len(before),'changed_parts':diff,'unchanged_control_cage_vertex_counts':topology,'scope':'Base geometry, world transforms and material slots for existing wheel/interior/engine parts; topology-count continuity of existing body/windscreen/roof cages.'},indent=2));print('RETAINED PARTS CHECK PASSED',flush=True)

assert all(bpy.data.objects[n].animation_data and bpy.data.objects[n].animation_data.action for n in ['DOOR_FL','DOOR_FR','DOOR_RL','DOOR_RR','BONNET','TAILGATE'])
q=A/'retained-parts-v02.json';v=json.loads(q.read_text());v['six_animation_actions_restored']=True;q.write_text(json.dumps(v,indent=2))
# All outputs are saved; bypass a headless audio-shutdown hang in this Blender runtime.
os._exit(0)

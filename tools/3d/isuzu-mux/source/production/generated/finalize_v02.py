import bpy,json,os
from pathlib import Path
O=Path(os.environ.get('MUX_V02_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';p=D/'isuzu-mux-generated-master.blend';bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;s.frame_set(1)
s['STATUS']='V02 exterior: MAJOR REWORK REQUIRED — not production approved';s['MOTION_STATUS']='NEEDS WORK — closed/early-angle assembly contacts remain';s['v02_method']='Retained V01 model; in-place cages and local fascia/lamp refinements; four door pivots retained; bonnet/tailgate hinges corrected; interior/engine/wheels unchanged'
readme=bpy.data.texts.get('V02_REVIEW_STATUS') or bpy.data.texts.new('V02_REVIEW_STATUS');readme.clear();readme.write('Exterior decision: MAJOR REWORK REQUIRED.\nReview GENERATED_MODEL_REPORT.md and renders/generated-final-comparison-v02.jpg.\nMotion remains NEEDS WORK. Frames 1 closed and 50 open.\nGLB not exported. Website unchanged.\n')
controls=['DOOR_FL','DOOR_FR','DOOR_RL','DOOR_RR','BONNET','TAILGATE'];assert all(bpy.data.objects[n].animation_data and bpy.data.objects[n].animation_data.action for n in controls)
bpy.ops.wm.save_as_mainfile(filepath=str(D/'milestones/isuzu-mux-exterior-v02.blend'));bpy.ops.wm.save_as_mainfile(filepath=str(p));bpy.ops.wm.open_mainfile(filepath=str(p));assert s!=bpy.context.scene or bpy.context.scene['STATUS'].startswith('V02')
(A/'final-save-v02.json').write_text(json.dumps({'passed':True,'master_reopened':True,'six_animated_controls':all(bpy.data.objects[n].animation_data and bpy.data.objects[n].animation_data.action is not None for n in controls),'status':bpy.context.scene['STATUS'],'closed_frame':bpy.context.scene.frame_current},indent=2));print('FINAL SOURCE SAVED AND REOPENED',flush=True)
# All outputs are saved; bypass a headless audio-shutdown hang in this Blender runtime.
os._exit(0)

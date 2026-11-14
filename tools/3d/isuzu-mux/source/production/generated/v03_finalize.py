import bpy,json,os
from pathlib import Path
O=Path(os.environ.get('MUX_V03_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';p=D/'isuzu-mux-generated-v03.blend';checks=[]
for rel in ['milestones/isuzu-mux-v03-guides.blend','milestones/isuzu-mux-v03-blockout.blend','milestones/isuzu-mux-v03-greenhouse.blend','milestones/isuzu-mux-v03-identity.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(D/rel));assert bpy.data.collections.get('V02_REFERENCE_BODY');checks.append({'path':rel,'reopened':True})
bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;s.frame_set(1);s['STATUS']='V03: C — NOT BETTER THAN V02; STOP BEFORE DETAILING';s['V03_STAGE']='Identity gate NOT PASSED; no surface finishing, panel cuts, clearance or GLB';s['V02_EXTERIOR_REUSED_AS_CONTROL_CAGE']=False;s['V03_PAID_ASSETS']='NONE';s['V03_RETAINED_PARTS']=113
for ob in bpy.data.collections['V02_REFERENCE_BODY'].objects:ob.hide_set(False)
for name,co in [('LM_OVERALL_HEIGHT',(.28,0,1.86)),('LM_NOMINAL_WIDTH_LEFT',(.28,.93,1.0)),('LM_NOMINAL_WIDTH_RIGHT',(.28,-.93,1.0))]:
 if not bpy.data.objects.get(name):
  ob=bpy.data.objects.new(name,None);bpy.data.collections['V03_LANDMARK_GUIDES'].objects.link(ob);ob.location=co;ob.empty_display_type='SPHERE';ob.empty_display_size=.025
readme=bpy.data.texts.get('V03_REVIEW_STATUS') or bpy.data.texts.new('V03_REVIEW_STATUS');readme.clear();readme.write('V03 decision C: identity improvement threshold NOT PASSED.\nStop before detailing. No new panel cuts or functional clearance.\nV02_REFERENCE_BODY is hidden reference only.\n113 wheel/interior/engine parts retained unchanged; internal parts hidden for exterior review.\nReview GENERATED_MODEL_REPORT.md and renders/v03/v02-v03-comparison.jpg.\nNo GLB / integration / deployment.\n');s.camera=bpy.data.objects['CAM_COMPARE_FRONT_34'];bpy.ops.wm.save_as_mainfile(filepath=str(p));bpy.ops.wm.open_mainfile(filepath=str(p));assert bpy.context.scene['V02_EXTERIOR_REUSED_AS_CONTROL_CAGE']==False
(A/'v03-final-save.json').write_text(json.dumps({'milestones':checks,'working_source_reopened':True,'decision':bpy.context.scene['STATUS'],'separate_v03_source':True,'v02_master_overwritten':False},indent=2));print('V03 MILESTONES AND FINAL SOURCE REOPENED',flush=True);os._exit(0)

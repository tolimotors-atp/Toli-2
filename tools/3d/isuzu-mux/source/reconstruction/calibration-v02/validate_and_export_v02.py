from problem_v02 import *
import csv,collections
S=json.loads((OUT/'v02-solution.json').read_text());AUD=json.loads((OUT/'v01-residual-audit.json').read_text());vrows={(o['camera'],o['landmark']):o for o in S['rows']}
# Full audit always retains all 198 V01 observations. Removed C points never receive invented V02 projections.
complete=[]
for o in AUD:
 v=vrows.get((o['camera'],o['landmark']));r={**o,'selected_core_camera':o['camera'] in S['core_cameras']}
 if v:
  status='CORE HELD-OUT' if v.get('v02_heldout') and r['selected_core_camera'] else 'CORE TRAINING' if r['selected_core_camera'] else 'EXTERNAL VALIDATION' if v.get('v02_heldout') else 'EXTERNAL POSE ANCHOR'
  r.update({'v02_status':status,'v02_prediction':v['predicted_v02'],'v02_dx':v['dx_v02'],'v02_dy':v['dy_v02'],'v02_residual':v['error_v02']})
 else:r.update({'v02_status':'REJECTED FIXED-POINT OBSERVATION' if o['confidence']=='C' else 'DETAIL/VALIDATION REFERENCE ONLY','v02_prediction':None,'v02_dx':None,'v02_dy':None,'v02_residual':None})
 complete.append(r)
complete.sort(key=lambda o:-1 if o['v02_residual'] is None else o['v02_residual'],reverse=True)
(OUT/'all-observations-v02.json').write_text(json.dumps(complete,indent=2)+'\n')
fields=['camera','landmark','category','confidence','visibility','confidence_reason','decision','v02_status','observed_x','observed_y','v01_predicted_x','v01_predicted_y','v01_dx','v01_dy','v01_euclidean_residual','v02_predicted_x','v02_predicted_y','v02_dx','v02_dy','v02_euclidean_residual']
with (OUT/'all-observations-v02.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in complete:
  vp=r['v02_prediction'] or [None,None];w.writerow({**{k:r[k] for k in fields if k in r},'observed_x':r['xy'][0],'observed_y':r['xy'][1],'v01_predicted_x':r['projected'][0],'v01_predicted_y':r['projected'][1],'v01_dx':r['dx'],'v01_dy':r['dy'],'v01_euclidean_residual':r['error_pixels'],'v02_predicted_x':vp[0],'v02_predicted_y':vp[1],'v02_dx':r['v02_dx'],'v02_dy':r['v02_dy'],'v02_euclidean_residual':r['v02_residual']})
# All 48 original landmarks remain accounted for; active structural subset is explicitly smaller.
perland=[]
for r in json.loads((OUT/'v01-landmark-audit.json').read_text()):
 rows=[o for o in complete if o['landmark']==r['landmark']];active=[o for o in rows if o['v02_residual'] is not None];core=[o for o in active if o['selected_core_camera']];errors=[o['v02_residual'] for o in core]
 r['v02_included_core_observations']=len(core);r['v02_external_observations']=len(active)-len(core);r['v02_core_rms']=float(np.sqrt(np.mean(np.square(errors)))) if errors else None;r['v02_core_max']=max(errors) if errors else None;r['v02_status']='ACTIVE STRUCTURAL' if core else 'NOT FIT: DOCUMENTED REJECTION OR DETAIL REFERENCE';perland.append(r)
(OUT/'per-landmark-v02.json').write_text(json.dumps(perland,indent=2)+'\n')
with (OUT/'per-landmark-v02.csv').open('w',newline='') as f:
 keys=['landmark','observations','confidence_classes','v01_rms','v01_max','v02_included_core_observations','v02_external_observations','v02_core_rms','v02_core_max','v02_status'];w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
 for r in perland:w.writerow({k:r.get(k) for k in keys})
with (OUT/'per-camera-v02.csv').open('w',newline='') as f:
 keys=['camera','status','included','observations','rms','median','maximum','training_rms','heldout_rms','external_test_rms','focal_36mm_equivalent','x_wb_units','y_wb_units','z_wb_units','yaw_degrees','pitch_degrees','roll_degrees','pose_rank','confidence'];w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
 for i,c in sorted(S['per_camera'].items(),key=lambda k:int(k[0])):
  status='UNDERCONSTRAINED EXTERNAL POSE' if not c['included'] and c.get('pose_rank',6)<6 else 'GLOBAL GATE FAILED / NOT ACCEPTED'
  w.writerow({'camera':i,'status':c['status'],'included':c['included'],'observations':c['observations'],'rms':c['all']['rms'],'median':c['all']['median'],'maximum':c['all']['max'],'training_rms':c['training']['rms'] if c['included'] else c.get('pose_anchors',{}).get('rms'),'heldout_rms':c['heldout']['rms'] if c['included'] else None,'external_test_rms':c.get('independent_projection',{}).get('rms'),'focal_36mm_equivalent':c['focal_36mm'],'x_wb_units':c['position'][0],'y_wb_units':c['position'][1],'z_wb_units':c['position'][2],'yaw_degrees':math.degrees(c['yaw_pitch_roll'][0]),'pitch_degrees':math.degrees(c['yaw_pitch_roll'][1]),'roll_degrees':math.degrees(c['yaw_pitch_roll'][2]),'pose_rank':c.get('pose_rank'),'confidence':status})
# Observability/geometry sensitivity: fold 9 uses none of image 9 to recover geometry.
fold=Problem([i for i in S['core_cameras'] if i!=9]);fp,_=fold.staged();foldpoints=fold.pointmap(fp);deltas=sorted([{'landmark':n,'delta_wheelbase_units':float(np.linalg.norm(np.array(v)-np.array(S['points'][n]))),'full':S['points'][n],'without_image9':v} for n,v in foldpoints.items()],key=lambda r:r['delta_wheelbase_units'],reverse=True)
# Reconstruct the chosen full vector and inspect data-only Jacobian, excluding priors from the rank test.
q=Problem(S['core_cameras']);p=q.initial.copy();p[:3]=S['frame_focal']
for g,k in GI.items():p[3+3*k:3+3*(k+1)]=S['points'][g+'_L']
for i in q.cameras:
 c=S['per_camera'][str(i)];k=q.off+6*q.ci[i];p[k:k+6]=c['yaw_pitch_roll']+c['position']
bas=q.project(p)[0][q.train].ravel();J=[]
for k in range(len(p)):
 pp=p.copy();pp[k]+=1e-5;J.append((q.project(pp)[0][q.train].ravel()-bas)/1e-5)
J=np.array(J).T;sv=np.linalg.svd(J/np.maximum(np.linalg.norm(J,axis=0),1e-12),compute_uv=False)
confidence_counts=dict(collections.Counter(r['confidence'] for r in complete));status_counts=dict(collections.Counter(r['v02_status'] for r in complete));active_core=[r for r in complete if r['v02_status'].startswith('CORE')];errors=[r['v02_residual'] for r in active_core]
checks={'observation_confidence_counts':confidence_counts,'observation_status_counts':status_counts,'active_core_landmarks':sum(bool(r['v02_included_core_observations']) for r in perland),'all_v01_landmarks_audited':len(perland),'data_only_normalized_rank':int(sum(sv>sv[0]*1e-4)),'unknowns':len(p),'normalized_smallest_singular':float(sv[-1]),'normalized_condition_number':float(sv[0]/max(sv[-1],1e-15)),'fold9_landmark_motion':deltas,'all_core_residual_rms':float(np.sqrt(np.mean(np.square(errors)))),'all_core_median':float(np.median(errors)),'core_worst':max(active_core,key=lambda r:r['v02_residual']),'open_panel_moving_observations_in_active_core':0,'rejected_classC_count':sum(r['confidence']=='C' for r in complete),'failure_classification':'CALIBRATION FAILED — CAMERA PARAMETERS UNDERCONSTRAINED','qualification':'Practical pose/depth recovery is not stable to view withholding; full local numerical rank is not proof of predictive geometric accuracy. Remaining manual annotation error is not excluded; incompatible trim or a need for new photos is not demonstrated.'}
# Never pass by omitting held-out or LOVO errors.
checks['gate']='FAIL';assert len(complete)==198 and len(perland)==48 and checks['active_core_landmarks']==20;assert all(v[2]==0 for n,v in S['points'].items() if n.startswith('contact_'));assert len(S['per_camera'])==12
for c in S['per_camera'].values():assert all(np.isfinite(c['position'])) and 50<c['focal_36mm']<100
(OUT/'validation-summary-v02.json').write_text(json.dumps(checks,indent=2)+'\n')
roles=[]
for i in range(1,14):
 role='CALIBRATION + DETAIL' if i in S['core_cameras'] else 'CALIBRATION ONLY — EXTERNAL VALIDATION' if i in [2,4] else 'DETAIL ONLY — WEAK DIAGNOSTIC POSE' if i in [1,3] else 'EXCLUDED'
 roles.append({'image':i,'role':role,'included_in_core':i in S['core_cameras'],'confidence':'GLOBAL CALIBRATION FAILED' if i!=5 else 'INTERIOR NOT USED'})
(OUT/'image-roles-v02.json').write_text(json.dumps(roles,indent=2)+'\n')
print('Audit counts',confidence_counts,status_counts,'active landmarks',checks['active_core_landmarks'],'rank',checks['data_only_normalized_rank'],'/',len(p),'condition',checks['normalized_condition_number'],'max fold9 movement',deltas[0])

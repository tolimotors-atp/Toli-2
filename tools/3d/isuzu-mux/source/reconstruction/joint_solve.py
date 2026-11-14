"""Sparse joint bundle adjustment: shared symmetric landmarks + all camera poses/intrinsics.
NumPy only. Gauge wheelbase=1. No previous mesh, manufacturer scale or camera-independent fits.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];D=json.loads((ROOT/'source/reconstruction/observations.json').read_text())
ids=sorted(map(int,D['observations']));groups=list(D['initial_landmarks']);ng=len(groups);nc=len(ids)
camindex={i:k for k,i in enumerate(ids)};gi={g:k for k,g in enumerate(groups)}
paths={r['image']:r['path'] for r in D['images']};sizes={i:Image.open(paths[i]).size for i in ids}
obs=[]
for i in ids:
 for name,xy in sorted(D['observations'][str(i)].items()):
  base,side=name.rsplit('_',1);sigma=3 if base.startswith('wc_') else 5 if base.startswith(('contact_','tiretop_')) else 7 if base.startswith(('q_','ws_','rw_')) else 6
  obs.append({'camera':i,'landmark':name,'base':base,'side':side,'xy':xy,'sigma':sigma})
counts={g:sum(o['base']==g for o in obs) for g in groups}
for i in ids:
 rows=[o for o in obs if o['camera']==i]
 for k,o in enumerate(rows):o['heldout']=bool(len(rows)>=10 and k%6==4 and not o['base'].startswith(('wc_','contact_','tiretop_')) and counts.get(o['base'],0)>=4)
train=np.array([not o['heldout'] for o in obs]);xy=np.array([o['xy'] for o in obs]);sigma=np.array([o['sigma'] for o in obs])
# Unknowns: shared track half-width and tire radius; symmetric body point coordinates; 9 parameters per camera.
initial=np.zeros(2+3*ng+9*nc);initial[:2]=[.29,.137];initial[2:2+3*ng]=np.array(list(D['initial_landmarks'].values())).ravel()
for i in ids:
 yaw,dist,elev=D['camera_initialization'][str(i)];yaw=math.radians(yaw);c=np.array([dist*math.cos(yaw),dist*math.sin(yaw),.33+dist*math.tan(elev)])
 initial[2+3*ng+9*camindex[i]:2+3*ng+9*(camindex[i]+1)]=[yaw,elev,0,*c,math.log(1.95),0,0]
ci=np.array([camindex[o['camera']] for o in obs]);sign=np.array([1 if o['side']=='L' else -1 for o in obs]);wh=np.array([sizes[o['camera']] for o in obs]);group_idx=np.array([gi.get(o['base'],-1) for o in obs]);base=[o['base'] for o in obs]
def points(p):
 pts=np.zeros((len(obs),3));vals=p[2:2+3*ng].reshape(-1,3);mask=group_idx>=0;pts[mask]=vals[group_idx[mask]];pts[:,1]*=sign
 for k,b in enumerate(base):
  if group_idx[k]<0:
   axle=.5 if b.endswith('_F') else -.5;z=p[1] if b.startswith('wc_') else 2*p[1] if b.startswith('tiretop_') else 0;pts[k]=[axle,sign[k]*p[0],z]
 return pts
# Camera uses X-right, Y-down, Z-forward. Crop shift is optimized, not hidden as geometry deformation.
def project(p):
 c=p[2+3*ng:].reshape(nc,9)[ci];yaw,el,roll=c[:,0],c[:,1],c[:,2];sy,cy=np.sin(yaw),np.cos(yaw);se,ce=np.sin(el),np.cos(el)
 right=np.stack([-sy,cy,np.zeros(len(c))],1);down=np.stack([cy*se,sy*se,-ce],1);forward=np.stack([-cy*ce,-sy*ce,-se],1)
 q=points(p)-c[:,3:6];xr=(q*right).sum(1);yr=(q*down).sum(1);z=(q*forward).sum(1);cr,sr=np.cos(roll),np.sin(roll);xx=cr*xr-sr*yr;yy=sr*xr+cr*yr
 f=np.exp(c[:,6])*wh[:,0];safe=np.maximum(z,.15)
 return np.stack([f*xx/safe+wh[:,0]*(.5+c[:,7]),f*yy/safe+wh[:,1]*(.5+c[:,8])],1),z
def priors(p):
 v=p[2:2+3*ng].reshape(ng,3);v0=initial[2:2+3*ng].reshape(ng,3);c=p[2+3*ng:].reshape(nc,9);c0=initial[2+3*ng:].reshape(nc,9)
 return np.r_[((v-v0)/.25*.10).ravel(),(p[:2]-initial[:2])*np.array([10,40]),c[:,2]/.05,(c[:,6]-c0[:,6])/.5,c[:,7]/.07,c[:,8]/.07,(c[:,0]-c0[:,0])/.6]
def residual(p):
 pred,z=project(p);r=(pred[train]-xy[train])/sigma[train,None];r=np.r_[r.ravel(),priors(p),np.minimum(z-.15,0)*50];return r
lo=np.full(len(initial),-np.inf);hi=np.full(len(initial),np.inf);lo[:2]=[.16,.08];hi[:2]=[.45,.22]
for k,g in enumerate(groups):
 off=2+3*k;v=initial[off:off+3];lo[off:off+3]=[v[0]-.35,.06,.05];hi[off:off+3]=[v[0]+.35,.48,.9]
for k in range(nc):
 j=2+3*ng+9*k;lo[j+1:j+3]=[-.25,-.15];hi[j+1:j+3]=[.65,.15];lo[j+5]=.08;hi[j+5]=6;lo[j+6:j+9]=[math.log(.55),-.18,-.18];hi[j+6:j+9]=[math.log(4.0),.18,.18]
def jac(p,r):
 J=np.empty((len(r),len(p)))
 for k in range(len(p)):
  step=1e-5*max(1,abs(p[k]));q=p.copy();q[k]+=step;J[:,k]=(residual(q)-r)/step
 return J
def fit(p,maxiter=90):
 lam=.03;r=residual(p);n_data=int(train.sum())*2
 for it in range(maxiter):
  J=jac(p,r);w=np.ones(len(r));pair=r[:n_data].reshape(-1,2);norm=np.linalg.norm(pair,axis=1);w[:n_data]=np.repeat(np.minimum(1,2.0/np.maximum(norm,1e-8)),2);sw=np.sqrt(w);A=J*sw[:,None];b=r*sw;H=A.T@A;g=A.T@b;diag=np.maximum(np.diag(H),1e-5)
  step=np.linalg.solve(H+np.diag(diag*lam),-g);q=np.clip(p+step,lo,hi);rq=residual(q);old=np.dot(r*w,r);new=np.dot(rq*w,rq)
  if new<old:
   p=q;r=rq;lam=max(1e-7,lam*.5)
   if np.linalg.norm(step)<1e-6:break
  else:lam=min(1e8,lam*5)
  if it%10==0:print('iteration',it,'weighted cost',round(float(np.dot(r*w,r)),3),'damping',lam,flush=True)
 return p,r
p,r=fit(initial.copy());pred,z=project(p);err=np.linalg.norm(pred-xy,axis=1)
J=jac(p,residual(p));dataJ=J[:int(train.sum())*2];normalized=dataJ/np.maximum(np.linalg.norm(dataJ,axis=0),1e-12);sv=np.linalg.svd(normalized,compute_uv=False)
report={'route':'CALIBRATED MANUAL MULTI-VIEW — attempted, gate pending/failed','scale':'Normalized wheelbase=1. No manufacturer metric dimensions used.','joint_parameters':len(p),'manual_observations':len(obs),'training_observations':int(train.sum()),'heldout_observations':int((~train).sum()),'overall_rms_pixels':float(np.sqrt(np.mean(err**2))),'training_rms_pixels':float(np.sqrt(np.mean(err[train]**2))),'heldout_rms_pixels':float(np.sqrt(np.mean(err[~train]**2))),'max_error_pixels':float(max(err)),'positive_depth':bool(np.all(z>.15)),'data_jacobian_rank_1e4':int(sum(sv>sv[0]*1e-4)),'unknown_count':len(p),'normalized_jacobian_smallest_singular':float(sv[-1]),'priors':'Shared symmetry; floor/contact; fixed normalized axle spacing; weak body initializer penalty; focal, principal-shift, roll/yaw soft priors. No hidden error removal.','half_track_ratio':float(p[0]),'tire_radius_ratio':float(p[1]),'per_camera':{},'observations':[]}
for i in ids:
 m=np.array([o['camera']==i for o in obs]);tm=m&train;vm=m&~train;c=p[2+3*ng+9*camindex[i]:2+3*ng+9*(camindex[i]+1)]
 # Camera-only local rank, with shared landmarks fixed, is not full joint observability.
 jj=dataJ[:,2+3*ng+9*camindex[i]:2+3*ng+9*(camindex[i]+1)];ss=np.linalg.svd(jj/np.maximum(np.linalg.norm(jj,axis=0),1e-12),compute_uv=False)
 entry={'observations':int(m.sum()),'training':int(tm.sum()),'heldout':int(vm.sum()),'rms_pixels':float(np.sqrt(np.mean(err[m]**2))),'max_pixels':float(max(err[m])),'heldout_rms_pixels':float(np.sqrt(np.mean(err[vm]**2))) if vm.any() else None,'camera_local_rank':int(sum(ss>ss[0]*1e-4)),'yaw_pitch_roll_radians':c[:3].tolist(),'camera_center_wheelbase_units':c[3:6].tolist(),'focal_pixels':float(np.exp(c[6])*sizes[i][0]),'focal_36mm_sensor_equivalent':float(np.exp(c[6])*36),'principal_point_pixels':[(.5+c[7])*sizes[i][0],(.5+c[8])*sizes[i][1]],'bounds_hit':bool(np.any(np.isclose(c,lo[2+3*ng+9*camindex[i]:2+3*ng+9*(camindex[i]+1)],atol=1e-4)) or np.any(np.isclose(c,hi[2+3*ng+9*camindex[i]:2+3*ng+9*(camindex[i]+1)],atol=1e-4)))}
 entry['landmark_gate']='PASS' if entry['rms_pixels']<5 and entry['max_pixels']<12 and entry['camera_local_rank']==9 and not entry['bounds_hit'] and entry['heldout_rms_pixels'] is not None and entry['heldout_rms_pixels']<8 else 'FAIL'
 report['per_camera'][str(i)]=entry
for k,o in enumerate(obs):report['observations'].append({**o,'projected':pred[k].tolist(),'error_pixels':float(err[k]),'outlier_over_12px':bool(err[k]>12),'robust_downweighted':bool(not o['heldout'] and err[k]/o['sigma']>2),'excluded_from_training':o['heldout']})
pts={}
for g in groups:
 v=p[2+3*gi[g]:2+3*(gi[g]+1)]
 for side,sgn in [('L',1),('R',-1)]:pts[g+'_'+side]=[float(v[0]),float(v[1]*sgn),float(v[2])]
for a,x in [('F',.5),('R',-.5)]:
 for side,sgn in [('L',1),('R',-1)]:
  for prefix,zv in [('wc',p[1]),('contact',0),('tiretop',2*p[1])]:pts[prefix+'_'+a+'_'+side]=[x,float(sgn*p[0]),float(zv)]
report['overall_landmark_gate']='PASS' if all(e['landmark_gate']=='PASS' for e in report['per_camera'].values()) and report['data_jacobian_rank_1e4']==len(p) else 'FAIL'
(ROOT/'source/reconstruction/joint-solution.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'source/reconstruction/shared-landmarks.json').write_text(json.dumps(pts,indent=2)+'\n');np.save(ROOT/'source/reconstruction/solution-parameters.npy',p)
# Minimal projection self-checks: symmetry and tire-ground gauge; no surface generated.
for g in groups:assert np.allclose(np.array(pts[g+'_L'])*[1,-1,1],pts[g+'_R'])
assert report['positive_depth'];assert all(abs(v[2])<1e-12 for k,v in pts.items() if k.startswith('contact'))
print(json.dumps({k:v for k,v in report.items() if k not in ['observations','per_camera']},indent=2));print('Per camera:',{i:round(e['rms_pixels'],2) for i,e in report['per_camera'].items()})

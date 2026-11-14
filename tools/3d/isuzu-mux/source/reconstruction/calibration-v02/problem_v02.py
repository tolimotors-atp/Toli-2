"""Staged structural calibration with shared intrinsics and geometry-LOVO validation.
Only documented A/B structural points enter; no residual-driven automatic point deletion.
NumPy/Pillow only. Scale gauge wheelbase=1; no metric manufacturer dimensions.
"""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'source/reconstruction/calibration-v02';OLD=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/reconstruction')
D=json.loads((OLD/'observations.json').read_text());AUD=json.loads((OUT/'v01-residual-audit.json').read_text());V1=json.loads((OLD/'joint-solution.json').read_text());GROUPS=['h_out','h_in','ws_base','ws_top','tl_top','tl_low'];GI={g:i for i,g in enumerate(GROUPS)}
IMAGES={r['image']:r for r in D['images']};SIZES={i:Image.open(r['path']).size for i,r in IMAGES.items()};CORE6=[6,7,9,8,11,12];CORE8=[6,7,9,8,10,11,12,13]
HOLD={6:'h_out_L',7:'tl_top_L',9:'h_out_R',8:'tl_low_R',10:'ws_top_R',11:'ws_top_L',12:'tl_top_L',13:'tl_top_R'}
def eligible(o):return o['base'] in GROUPS or o['base'].startswith(('wc_','contact_'))
ROWS=sorted([o for o in AUD if eligible(o) and (o['confidence']=='A' or o['base'].startswith('ws_') and o['confidence']=='B')],key=lambda o:(o['camera'],o['landmark']))
def camera_initial(i):
 yaw,dist,el=D['camera_initialization'][str(i)];yaw=math.radians(yaw)
 return [yaw,el,0,dist*math.cos(yaw),dist*math.sin(yaw),.33+dist*math.tan(el)]
class Problem:
 def __init__(self,cameras,hold=True):
  self.cameras=list(cameras);self.ci={i:k for k,i in enumerate(cameras)};self.rows=[o for o in ROWS if o['camera'] in cameras];self.obsci=np.array([self.ci[o['camera']] for o in self.rows]);self.sign=np.array([1 if o['side']=='L' else -1 for o in self.rows]);self.xy=np.array([o['xy'] for o in self.rows]);self.wh=np.array([SIZES[o['camera']] for o in self.rows]);self.bodyidx=np.array([GI.get(o['base'],-1) for o in self.rows]);self.train=np.array([not(hold and o['landmark']==HOLD.get(o['camera'])) for o in self.rows]);self.wheel=np.array([o['base'].startswith(('wc_','contact_')) for o in self.rows]);self.a=np.array([o['confidence']=='A' for o in self.rows]);self.sigma=np.array([2.5 if o['base'].startswith('wc_') else 3.5 if o['base'].startswith('contact_') else 4 if o['base'].startswith('ws_') and o['confidence']=='A' else 5 if o['confidence']=='B' else 3 for o in self.rows]);self.off=3+3*len(GROUPS)
  self.initial=np.r_[.29,.137,math.log(70/36),np.array([D['initial_landmarks'][g] for g in GROUPS]).ravel(),np.array([camera_initial(i) for i in cameras]).ravel()];self.lo=np.full(len(self.initial),-np.inf);self.hi=-self.lo;self.lo[:3]=[.16,.08,math.log(50/36)];self.hi[:3]=[.45,.22,math.log(100/36)]
  for k,g in enumerate(GROUPS):
   j=3+3*k;v=self.initial[j:j+3];self.lo[j:j+3]=[v[0]-.3,.07,.05];self.hi[j:j+3]=[v[0]+.3,.45,.85]
  for k in range(len(cameras)):
   j=self.off+6*k;self.lo[j+1:j+3]=[-.2,-.15];self.hi[j+1:j+3]=[.55,.15];self.lo[j+5]=.08;self.hi[j+5]=5
 def coords(self,p):
  xyz=np.zeros((len(self.rows),3));body=p[3:self.off].reshape(-1,3);m=self.bodyidx>=0;xyz[m]=body[self.bodyidx[m]];xyz[:,1]*=self.sign
  for k,o in enumerate(self.rows):
   if self.bodyidx[k]<0:xyz[k]=[.5 if o['base'].endswith('_F') else -.5,self.sign[k]*p[0],p[1] if o['base'].startswith('wc_') else 0]
  return xyz
 def project(self,p):
  c=p[self.off:].reshape(-1,6)[self.obsci];yaw,el,roll=c[:,0],c[:,1],c[:,2];sy,cy=np.sin(yaw),np.cos(yaw);se,ce=np.sin(el),np.cos(el);right=np.stack([-sy,cy,np.zeros(len(c))],1);down=np.stack([cy*se,sy*se,-ce],1);forward=np.stack([-cy*ce,-sy*ce,-se],1);q=self.coords(p)-c[:,3:];xr=(q*right).sum(1);yr=(q*down).sum(1);z=(q*forward).sum(1);cr,sr=np.cos(roll),np.sin(roll);f=np.exp(p[2])*self.wh[:,0];s=np.maximum(z,.2)
  return np.stack([f*(cr*xr-sr*yr)/s+self.wh[:,0]*.5,f*(sr*xr+cr*yr)/s+self.wh[:,1]*.5],1),z
 def residual(self,p,mask):
  pred,z=self.project(p);data=((pred[mask]-self.xy[mask])/self.sigma[mask,None]).ravel();body=(p[3:self.off]-self.initial[3:self.off])/.25*.08;c=p[self.off:].reshape(-1,6);c0=self.initial[self.off:].reshape(-1,6)
  # Weak shape initialization, constrained common focal, restrained roll; zero per-camera shifts.
  prior=np.r_[(p[:2]-self.initial[:2])*[8,25],(p[2]-self.initial[2])/.20,body,c[:,2]/.05,(c[:,0]-c0[:,0])/.6,np.minimum(z-.2,0)*30]
  return np.r_[data,prior]
 def fit(self,p,indices,mask,maxiter=60):
  indices=np.array(indices,dtype=int);lam=.01;delta=1.5;ndata=int(mask.sum())*2;r=self.residual(p,mask)
  def loss(r):
   pair=np.linalg.norm(r[:ndata].reshape(-1,2),axis=1);return float(np.sum(2*delta*delta*(np.sqrt(1+(pair/delta)**2)-1))+np.dot(r[ndata:],r[ndata:]))
  for it in range(maxiter):
   J=np.empty((len(r),len(indices)))
   for col,k in enumerate(indices):
    step=1e-5*max(1,abs(p[k]));q=p.copy();q[k]+=step;J[:,col]=(self.residual(q,mask)-r)/step
   norms=np.linalg.norm(r[:ndata].reshape(-1,2),axis=1);weights=np.ones(len(r));weights[:ndata]=np.repeat(1/np.sqrt(1+(norms/delta)**2),2);A=J*np.sqrt(weights)[:,None];b=r*np.sqrt(weights);H=A.T@A;g=A.T@b;diag=np.maximum(np.diag(H),1e-6)
   try:step=np.linalg.solve(H+np.diag(diag*lam),-g)
   except np.linalg.LinAlgError:lam*=10;continue
   q=p.copy();q[indices]+=step;q=np.clip(q,self.lo,self.hi);rr=self.residual(q,mask)
   if loss(rr)<loss(r):
    p=q;r=rr;lam=max(1e-7,lam*.5)
    if np.linalg.norm(step)<1e-6:break
   else:lam=min(1e8,lam*5)
  return p
 def metrics(self,p,mask):
  pred,z=self.project(p);e=np.linalg.norm(pred-self.xy,axis=1);v=e[mask]
  return {'n':int(mask.sum()),'rms':float(np.sqrt(np.mean(v*v))) if len(v) else None,'median':float(np.median(v)) if len(v) else None,'max':float(max(v)) if len(v) else None}
 def staged(self):
  p=self.initial.copy();stages=[]
  def stage(name,idx,mask,it=45):
   nonlocal p;p=self.fit(p,idx,mask,it);stages.append({'stage':name,'active_unknowns':len(idx),'fit_observations':int(mask.sum()),'all_structural_train':self.metrics(p,self.train),'common_focal_36mm':float(np.exp(p[2])*36),'half_track':float(p[0]),'radius':float(p[1])})
  orient=[self.off+6*k+j for k in range(len(self.cameras)) for j in range(3)];pos=[self.off+6*k+j for k in range(len(self.cameras)) for j in range(3,6)]
  stage('A vehicle-frame ratios; gauge ground/axles fixed',[0,1],self.train&self.wheel,25)
  stage('B camera orientations, A landmarks only',orient,self.train&self.a)
  stage('C camera positions, A landmarks only',pos,self.train&self.a)
  stage('B2 orientation stabilization',orient,self.train&self.a)
  stage('C2 position stabilization',pos,self.train&self.a)
  stage('D constrained single shared focal; no free principal shifts',[2],self.train&self.a,25)
  stage('E shared landmark depths; stable B windshield ties admitted',list(range(3,self.off)),self.train)
  stage('F robust joint structural bundle',list(range(len(p))),self.train,100)
  return p,stages
 def pointmap(self,p):
  out={}
  for g,k in GI.items():
   v=p[3+3*k:3+3*(k+1)]
   for side,sgn in [('L',1),('R',-1)]:out[g+'_'+side]=[float(v[0]),float(v[1]*sgn),float(v[2])]
  for axle,x in [('F',.5),('R',-.5)]:
   for side,sgn in [('L',1),('R',-1)]:
    out['wc_'+axle+'_'+side]=[x,float(sgn*p[0]),float(p[1])];out['contact_'+axle+'_'+side]=[x,float(sgn*p[0]),0.0]
  return out
 def camera_records(self,p):
  pred,z=self.project(p);err=np.linalg.norm(pred-self.xy,axis=1);out={}
  for i in self.cameras:
   k=self.ci[i];c=p[self.off+6*k:self.off+6*(k+1)];m=np.array([o['camera']==i for o in self.rows]);hm=m&~self.train
   out[str(i)]={'status':'CORE','observations':int(m.sum()),'training':self.metrics(p,m&self.train),'heldout':self.metrics(p,hm),'all':self.metrics(p,m),'focal_36mm':float(np.exp(p[2])*36),'focal_pixels':float(np.exp(p[2])*SIZES[i][0]),'principal_point':[SIZES[i][0]/2,SIZES[i][1]/2],'yaw_pitch_roll':c[:3].tolist(),'position':c[3:].tolist(),'confidence':'UNVALIDATED until visual/LOVO gate','included':True}
  return out
 def rows_report(self,p):
  pred,z=self.project(p);return [{**o,'predicted_v02':pred[k].tolist(),'dx_v02':float(pred[k,0]-o['xy'][0]),'dy_v02':float(pred[k,1]-o['xy'][1]),'error_v02':float(np.linalg.norm(pred[k]-o['xy'])),'v02_heldout':bool(not self.train[k]),'positive_depth':bool(z[k]>.2)} for k,o in enumerate(self.rows)]
# Frozen-geometry omitted-view pose estimation: anchors and test points are disjoint.
def pose_anchors(rows,i):
 names={o['landmark'] for o in rows}
 wheel={n for n in names if n.startswith(('wc_','contact_'))}
 if len(wheel)>=4:
  extra=next((n for n in sorted(names) if n.startswith('h_out_') or n.startswith('tl_top_')),None);return wheel|({extra} if extra else set())
 if i in [6,1]:return wheel|{n for n in names if n.startswith('ws_base_')}|{n for n in names if n=='ws_top_R'}
 return wheel|{n for n in names if n.startswith('tl_top_')}
def frozen_pose(i,points,frame_focal):
 q=Problem([i],hold=False);p=q.initial.copy();p[:3]=frame_focal
 for g,k in GI.items():p[3+3*k:3+3*(k+1)]=points[g+'_L']
 anchors=pose_anchors(q.rows,i);am=np.array([o['landmark'] in anchors and o['confidence']=='A' for o in q.rows]);# B windshield base may be required for frontal pose.
 if i==6:am=np.array([o['landmark'] in anchors for o in q.rows])
 p=q.fit(p,list(range(q.off,len(p))),am,90);test=~am
 # Local anchor-pose Jacobian rank detects insufficient/degenerated pose constraints.
 base=q.residual(p,am);J=[]
 for j in range(q.off,len(p)):
  pp=p.copy();pp[j]+=1e-5;J.append((q.residual(pp,am)[:2*int(am.sum())]-base[:2*int(am.sum())])/1e-5)
 J=np.array(J).T;sv=np.linalg.svd(J/np.maximum(np.linalg.norm(J,axis=0),1e-12),compute_uv=False);rank=int(sum(sv>sv[0]*1e-4)) if len(sv) else 0
 c=q.camera_records(p)[str(i)];c['status']='OMITTED/EXTERNAL POSE ONLY';c['included']=False;c['pose_anchor_names']=sorted(anchors);c['pose_anchors']=q.metrics(p,am);c['independent_projection']=q.metrics(p,test);c['pose_rank']=rank
 return q,p,c,am

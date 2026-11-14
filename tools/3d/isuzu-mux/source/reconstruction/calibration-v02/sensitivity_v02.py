from problem_v02 import *
# Minimal focal flexibility ablation: four better-constrained side/front-quarter cameras only.
# Principal shifts remain fixed; no distortion coefficients added.
class FocalOffsets(Problem):
 def __init__(self,cameras):
  super().__init__(cameras);self.nbase=len(self.initial);self.variable=[i for i in cameras if i in [7,9,10,11]];self.initial=np.r_[self.initial,np.zeros(len(self.variable))];self.lo=np.r_[self.lo,np.full(len(self.variable),-.12)];self.hi=np.r_[self.hi,np.full(len(self.variable),.12)]
 def project(self,p):
  base,z=super().project(p[:self.nbase]);center=self.wh*.5;offset={i:p[self.nbase+k] for k,i in enumerate(self.variable)};factor=np.exp(np.array([offset.get(o['camera'],0) for o in self.rows]));return center+(base-center)*factor[:,None],z
 def residual(self,p,mask):
  pred,z=self.project(p);data=((pred[mask]-self.xy[mask])/self.sigma[mask,None]).ravel();body=(p[3:self.off]-self.initial[3:self.off])/.25*.08;c=p[self.off:self.nbase].reshape(-1,6);c0=self.initial[self.off:self.nbase].reshape(-1,6)
  prior=np.r_[(p[:2]-self.initial[:2])*[8,25],(p[2]-self.initial[2])/.20,body,c[:,2]/.05,(c[:,0]-c0[:,0])/.6,np.minimum(z-.2,0)*30,p[self.nbase:]/.05]
  return np.r_[data,prior]

base=Problem(CORE8);p,stages=base.staged();flex=FocalOffsets(CORE8);q=np.r_[p,np.zeros(len(flex.variable))];q=flex.fit(q,list(range(len(q))),flex.train,90)
report={'experiment':'Four constrained per-camera focal offsets; +/-12% bounds, sigma 5% prior, locked principal centers; no point deletion','baseline_training':base.metrics(p,base.train),'baseline_heldout':base.metrics(p,~base.train),'flex_training':flex.metrics(q,flex.train),'flex_heldout':flex.metrics(q,~flex.train),'common_focal_mm':float(np.exp(q[2])*36),'camera_focal_mm':{str(i):float(np.exp(q[2]+q[flex.nbase+k])*36) for k,i in enumerate(flex.variable)}}
report['accepted']=bool(report['flex_heldout']['rms']<=5 and report['flex_heldout']['rms']<report['baseline_heldout']['rms'] and report['flex_heldout']['max']<=10);report['decision']='Not promoted without independent geometry-LOVO/visual pass' if report['accepted'] else 'Rejected: held-out target not met; do not add degrees of freedom just to lower training loss'
# Pose ambiguity in the worst structural LOVO case: geometry never saw image 9.
fold=Problem([i for i in CORE8 if i!=9]);fp,_=fold.staged();points=fold.pointmap(fp);camera=9;qprob=Problem([camera],hold=False);start=qprob.initial.copy();start[:3]=fp[:3]
for g,k in GI.items():start[3+3*k:3+3*(k+1)]=points[g+'_L']
anchors=pose_anchors(qprob.rows,camera);am=np.array([o['landmark'] in anchors and o['confidence']=='A' for o in qprob.rows]);candidates=[]
for yaw in [-.12,0,.12]:
 for height in [-.12,0,.12]:
  init=start.copy();init[qprob.off]+=yaw;init[qprob.off+5]+=height;sol=qprob.fit(init,list(range(qprob.off,len(init))),am,100)
  rr=qprob.residual(sol,am);nd=int(am.sum())*2;norm=np.linalg.norm(rr[:nd].reshape(-1,2),axis=1);cost=float(np.sum(2*1.5**2*(np.sqrt(1+(norm/1.5)**2)-1))+np.dot(rr[nd:],rr[nd:]))
  candidates.append({'init_yaw_offset':yaw,'init_height_offset':height,'anchor_objective_with_priors':cost,'anchor_result':qprob.metrics(sol,am),'independent_test':qprob.metrics(sol,~am),'camera_parameters':sol[qprob.off:].tolist()})
best=min(candidates,key=lambda c:c['anchor_objective_with_priors']);report['image9_pose_multistart']={'protocol':'Select by anchor loss plus declared priors only; independent test pixels NEVER select the pose','anchors':sorted(anchors),'geometry_fit_images':fold.cameras,'candidates':candidates,'selected':best}
# Distortion screening on available structural residuals, not an attempt to fit them away.
pred,z=base.project(p);res=pred-base.xy;center=base.wh*.5;rad=pred-center;rn=np.linalg.norm(rad,axis=1);radial=(res*rad).sum(1)/np.maximum(rn,1e-9);screen={}
for i in CORE8:
 m=np.array([o['camera']==i for o in base.rows]);corr=float(np.corrcoef(radial[m],(rn[m]/base.wh[m,0])**2)[0,1]) if m.sum()>3 and np.std(radial[m])>1e-8 else None;screen[str(i)]={'radial_error_vs_radius_squared_correlation':corr,'observations':int(m.sum())}
report['distortion_screen']={'per_camera':screen,'exif_focal_available':False,'radial_model_applied':False,'reason':'Sparse annotated vehicle features do not provide independent straight-line distortion controls. Cropped screenshots and uncertain corners confound radial residual correlation. Opposing camera signs are not proof of a common barrel/pincushion model. No extra distortion fitted to force acceptance.'}
(OUT/'intrinsic-and-pose-sensitivity.json').write_text(json.dumps(report,indent=2)+'\n')
print('Focal ablation:',report['baseline_heldout'],report['flex_heldout'],report['decision'],flush=True);print('LOVO9 best-anchor pose:',best['anchor_result'],best['independent_test'],flush=True)

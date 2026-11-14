from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,numpy as np
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');W=P/'tools/3d/isuzu-mux/manual-overlay-reconstruction';rows=json.loads((W/'references/selection.json').read_text())
corrections={11:{'fp':[389,432],'fn':[685,432],'rfo':[438,146],'rf':[611,146]},27:{'fp':[373,466],'fn':[734,466],'rfo':[459,132],'rf':[651,132]},16:{'fn':[420,414],'rn':[777,353],'rf':[588,161],'rr':[801,153]},17:{'fn':[310,316],'rn':[519,419],'rf':[414,173],'rr':[599,173]},15:{'fp':[575,417],'rp':[277,337],'rfo':[516,165],'rro':[298,157]}}
# Camera fitting uses a fixed nominal frame, never edits vehicle dimensions.
world={'fn':[-1.4225,-.785,.382],'fp':[-1.4225,.785,.382],'rn':[1.4225,-.785,.382],'rp':[1.4225,.785,.382],'rf':[-.45,-.69,1.80],'rr':[1.76,-.70,1.80],'rfo':[-.45,.69,1.80],'rro':[1.76,.70,1.80]}
def basis(az,el):
 az,el=np.radians([az,el]);direction=np.array([-np.cos(az)*np.cos(el),-np.sin(az)*np.cos(el),np.sin(el)]);forward=-direction;right=np.cross(forward,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,forward);return direction,right,up,forward
fits=[]
for r in rows:
 num=int(r['id'][-3:]);sc=r['normalization']['scale'];off=r['normalization']['offset']
 if num in corrections:r['anchors']=[{'name':n,'world':world[n],'pixel_original':xy,'pixel':[xy[0]*sc+off[0],xy[1]*sc+off[1]],'uncertainty_px_original':12 if len(n)==2 else 18} for n,xy in corrections[num].items()]
 if num==43:
  fit={'id':r['id'],'view':r['selected_view'],'type':'ORTHO','position':[0,0,12],'target':[0,0,0],'up':[0,1,0],'ortho_scale':5.15,'confidence':'LOW','fit_rms_pixels':None,'known_mismatch':'Unrelated roof-only reference; no wheel anchors. Manually framed planform only, not metric evidence.'}
 else:
  pts=np.array([a['world'] for a in r['anchors']]);pixels=np.array([a['pixel'] for a in r['anchors']]);best=None;target=np.array([0.,0.,.93]);az0=r['approximate_visual_azimuth']
  for az in np.arange(az0-12,az0+12.1,1):
   for el in np.arange(0,27,1):
    di,ri,up,fw=basis(az,el);pos=target+12*di;rel=pts-pos;depth=rel@fw;q=np.column_stack([rel@ri/depth,-(rel@up)/depth]);qc=q-q.mean(0);pc=pixels-pixels.mean(0);f=(qc*pc).sum()/(qc*qc).sum();shift=pixels.mean(0)-f*q.mean(0)
    pred=f*q+shift;rms=np.sqrt(((pred-pixels)**2).sum(1).mean());score=rms+.035*abs(az-az0)
    lens=f*36/800
    if not 18<=lens<=160:continue
    if best is None or score<best[0]:best=(score,az,el,pos,fw,up,f,shift,pred,rms,lens)
  assert best is not None, r['id']
  _,az,el,pos,fw,up,f,shift,pred,rms,lens=best
  fit={'id':r['id'],'view':r['selected_view'],'type':'PERSP','azimuth':float(az),'elevation':float(el),'position':pos.tolist(),'target':target.tolist(),'up':up.tolist(),'lens_mm_assumed_36mm_sensor':lens,'sensor_width':36,'principal_point':shift.tolist(),'fit_rms_pixels':rms,'confidence':r['confidence'] if rms<14 else 'LOW','anchors':[dict(a,projected=xy.tolist(),residual_px=float(np.linalg.norm(xy-a['pixel']))) for a,xy in zip(r['anchors'],pred)],'known_mismatch':'Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.'}
  im=Image.open(W/'normalized'/f'{num:03}.png').convert('RGB');dr=ImageDraw.Draw(im)
  def project(pts):
   rel=np.array(pts)-pos;return np.column_stack([rel@ri/(rel@fw),-(rel@up)/(rel@fw)])*f+shift
  # Explicit use of fitted basis, not the loop's last rejected angle.
  di,ri,up,fw=basis(az,el)
  for z,color in [(0,'#42e6d5'),(1.86,'#ecc76f')]:
   corners=[[-2.4125,-.93,z],[2.4125,-.93,z],[2.4125,.93,z],[-2.4125,.93,z],[-2.4125,-.93,z]];dr.line([tuple(x) for x in project(corners)],fill=color,width=2)
  for x in [-2.4125,2.4125]:
   for y in [-.93,.93]:dr.line([tuple(v) for v in project([[x,y,0],[x,y,1.86]])],fill='#ecc76f',width=1)
  for a in fit['anchors']:
   x,y=a['pixel'];u,v=a['projected'];dr.line((x,y,u,v),fill='#ff3256',width=2);dr.ellipse((x-4,y-4,x+4,y+4),outline='#ff3256',width=2);dr.ellipse((u-3,v-3,u+3,v+3),fill='#44e7d4');dr.text((x+6,y-9),a['name'],fill='#ff3256')
  dr.text((8,8),f"REFERENCE-FIT / {r['id']} / anchor RMS {rms:.1f}px / NOT CALIBRATED",fill='#e52044');im.save(W/'cameras'/f'framework-overlay-{num:03}.png')
 fits.append(fit)
(W/'references/selection.json').write_text(json.dumps(rows,indent=2));(W/'cameras/reference-fits.json').write_text(json.dumps(fits,indent=2))
print([(f['id'],round(f.get('fit_rms_pixels') or 0,1),f['confidence']) for f in fits])

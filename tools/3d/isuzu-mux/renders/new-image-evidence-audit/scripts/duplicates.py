from pathlib import Path
import json,cv2,numpy as np,itertools
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';S=P.parent/'Isuzu MU-X';r=B/'renders/new-image-evidence-audit';d=json.loads((B/'references/authoritative-folder/current-inventory.json').read_text());features={};crops={}
sift=cv2.SIFT_create(nfeatures=1200)
for row in d['images']:
 if row['previous_hash_match'] or not row['readable']:continue
 # Only the red viewer sequence has a robust common foreground-color crop.
 im=cv2.imread(str(S/row['relative_path']))
 if im is None:continue
 b,g,rr=cv2.split(im);mask=(rr.astype(float)>g.astype(float)*1.35)&(rr.astype(float)>b.astype(float)*1.25)&(rr>70)
 ys,xs=np.where(mask)
 if len(xs)<1000:continue
 x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max();w=x1-x0;h=y1-y0
 crop=im[max(0,int(y0-.08*h)):min(im.shape[0],int(y1+.35*h)),max(0,int(x0-.02*w)):min(im.shape[1],int(x1+.02*w))];crop=cv2.resize(crop,(640,400));gray=cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY);k,desc=sift.detectAndCompute(gray,None);features[row['id']]=(k,desc);crops[row['id']]=crop
matcher=cv2.BFMatcher();out=[]
for a,b in itertools.combinations(features,2):
 ka,da=features[a];kb,db=features[b];pairs=matcher.knnMatch(da,db,k=2);good=[x for x,y in pairs if x.distance<.70*y.distance]
 if len(good)<35:continue
 aa=np.float32([ka[m.queryIdx].pt for m in good]);bb=np.float32([kb[m.trainIdx].pt for m in good]);H,ok=cv2.findHomography(aa,bb,cv2.RANSAC,1.5)
 if H is None:continue
 ratio=float(ok.mean());warped=cv2.warpPerspective(crops[a],H,(640,400));mad=float(np.mean(np.abs(warped.astype(float)-crops[b].astype(float))))
 if ratio>.60:out.append({'a':a,'b':b,'ratio':ratio,'good':len(good),'aligned_rgb_mean_abs_difference':mad})
out.sort(key=lambda x:(-x['ratio'],-x['good']));(r/'near-duplicate-candidates.json').write_text(json.dumps(out,indent=2));print(json.dumps(out[:22],indent=2))

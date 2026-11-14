from pathlib import Path
import cv2,numpy as np,json,time,resource,hashlib
r=Path(__file__).resolve().parents[1];out=r/'calibration/depth';out.mkdir(exist_ok=True)
model=r/'models/model-small.onnx'
assert hashlib.sha256(model.read_bytes()).hexdigest()=='2d8c6cb8f415229daf1eb041024208e2608c9f98e17c81cc7c6ecb449c56fd58'
cv2.setNumThreads(2);net=cv2.dnn.readNetFromONNX(str(model));net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV);net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
log=[]
for t in ['18-17-10','18-17-27','18-17-14','18-17-35','18-17-18']:
 img=cv2.imread(str(r/'input/primary'/f'{t}.png'));start=time.time()
 # Official ONNX runner uses RGB [0,1], cubic 256-square resize; normalization is in this export.
 x=cv2.resize(cv2.cvtColor(img,cv2.COLOR_BGR2RGB).astype(np.float32)/255,(256,256),interpolation=cv2.INTER_CUBIC)
 net.setInput(x.transpose(2,0,1)[None]);d=net.forward().reshape(256,256)
 assert np.isfinite(d).all() and float(d.max()-d.min())>1e-5
 np.save(out/f'{t}-inverse-depth.npy',d)
 full=cv2.resize(d,(img.shape[1],img.shape[0]),interpolation=cv2.INTER_CUBIC)
 v=((full-full.min())/(full.max()-full.min())*65535).astype(np.uint16)
 cv2.imwrite(str(out/f'{t}-inverse-depth16.png'),v)
 cv2.imwrite(str(out/f'{t}-preview.png'),cv2.applyColorMap((v/257).astype(np.uint8),cv2.COLORMAP_INFERNO))
 log.append({'image':f'input/primary/{t}.png','seconds':time.time()-start,'min':float(d.min()),'max':float(d.max())})
(r/'logs/depth-result.json').write_text(json.dumps({'model':'MiDaS v2.1 small ONNX','runtime':'OpenCV DNN CPU','license':'MIT','preprocessing':'official tf/run_onnx.py: RGB0..1 cubic256square, no external normalization','inverse_depth':'relative unknown scale/shift; independently normalized previews, not metric depth; no fusion or invented camera intrinsics','results':log,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
print(json.dumps(log,indent=2))

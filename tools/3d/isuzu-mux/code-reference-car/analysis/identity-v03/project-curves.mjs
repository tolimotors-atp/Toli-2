// Pure numerical projection of authored curves; verified against wheel points from actual browser frames.
import * as T from 'three';
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {curve,lampPoint} from '../../../../../../src/components/three/mux/MuxGeometry.ts';
import {headlightCurves,tailLightCurves,bumperCornerCurves} from '../../../../../../src/components/three/mux/MuxReferenceData.ts';
const root=process.cwd(),out=root+'/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v03',frames=JSON.parse(fs.readFileSync('/tmp/mux-v03-clay/frames.json','utf8'));
const directions={front:[-1,0,.10],'front-right':[-1,-1,.40],right:[0,-1,.10],'rear-right':[1,-1,.40],rear:[1,0,.10]};
const current=fs.readFileSync(root+'/src/components/three/mux/validation.ts','utf8'),old=fs.readFileSync(root+'/tools/3d/isuzu-mux/code-reference-car/source-snapshots/identity-v02/final/validation.ts','utf8');
const cameraLines=s=>s.split('\n').filter(l=>l.includes('new T.PerspectiveCamera(')||l.includes('const views:')||l.includes('const right=new T.Vector3()')).join('\n');assert.equal(cameraLines(current),cameraLines(old));
const result={};
for(const [view,xyz] of Object.entries(directions)){
 const width=964,height=520,camera=new T.PerspectiveCamera(34,width/height,.1,80),target=new T.Vector3(0,0,.95),dir=new T.Vector3(...xyz).normalize();camera.up.set(0,0,1);
 const right=new T.Vector3().crossVectors(new T.Vector3(0,0,1),dir).normalize(),up=new T.Vector3().crossVectors(dir,right),tan=Math.tan(T.MathUtils.degToRad(17));let fit=0;for(const x of [-2.413,2.413])for(const y of [-.93,.93])for(const z of [0,1.86]){const p=new T.Vector3(x,y,z).sub(target);fit=Math.max(fit,p.dot(dir)+Math.abs(p.dot(up))/tan,p.dot(dir)+Math.abs(p.dot(right))/(tan*camera.aspect));}
 camera.position.copy(dir.multiplyScalar(fit*1.12).add(target));camera.lookAt(target);camera.updateMatrixWorld();
 const project=p=>{const q=p.clone().project(camera);return[(q.x+1)*width/2,(1-q.y)*height/2];};
 const wheel=project(new T.Vector3(-1.37,-.785,.382)),observed=frames.find(f=>f.view===view).landmarks.frontWheelNear.pixel;assert(Math.hypot(wheel[0]-observed[0],wheel[1]-observed[1])<1e-6);
 const networks={};for(const [prefix,network] of [['H',headlightCurves],['T',tailLightCurves],['B',bumperCornerCurves]])for(const [name,pts] of Object.entries(network)){networks[prefix+name]=curve(pts.map(p=>[p[0],-Math.abs(p[1]),p[2]])).getPoints(60).map(project);}
 const perimeter=rear=>[...Array.from({length:41},(_,i)=>lampPoint(i/40,0,-1,rear)),...Array.from({length:21},(_,i)=>lampPoint(1,i/20,-1,rear)),...Array.from({length:41},(_,i)=>lampPoint(1-i/40,1,-1,rear)),...Array.from({length:21},(_,i)=>lampPoint(0,1-i/20,-1,rear))].map(project);
 result[view]={networks,headlight:perimeter(false),taillight:perimeter(true),wheelProjectionError:Math.hypot(wheel[0]-observed[0],wheel[1]-observed[1])};
}
fs.writeFileSync(out+'/curve-projections.json',JSON.stringify(result,null,2));console.log('Five numerical camera projections verified against actual browser wheel anchors');

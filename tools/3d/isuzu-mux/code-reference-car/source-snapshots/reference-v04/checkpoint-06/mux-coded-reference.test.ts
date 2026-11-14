import { it, expect } from 'vitest';
import { createHash } from 'node:crypto';
import { writeFileSync } from 'node:fs';
import * as T from 'three';
import { createMux } from '@/components/three/mux/MuxVehicle';
import { measureMux,projectMuxLandmarks } from '@/components/three/mux/MuxValidation';
import { interpolate, section } from '@/components/three/mux/MuxGeometry';
import * as P from '@/components/three/mux/MuxReferencePatches';
import { dimensions, axles, bodyStations,curves,fasciaSections,normalizedLandmarks,referenceCheckpoint,shapeInfluences,headlightCurves,tailLightCurves,rearGlassCurves,rearSections,bumperCornerCurves } from '@/components/three/mux/MuxReferenceData';
function fingerprint(root:T.Group){const hash=createHash('sha256');root.traverse(o=>{if(!(o instanceof T.Mesh))return;hash.update(o.name);for(const name of Object.keys(o.geometry.attributes)){const attr=o.geometry.getAttribute(name);hash.update(Buffer.from(attr.array.buffer));}if(o.geometry.index)hash.update(Buffer.from(o.geometry.index.array.buffer));hash.update(o.position.toArray().join(','));});return hash.digest('hex');}
it('regenerates identical geometry, with locked scale, finite coordinates and symmetry',()=>{
 const first=createMux(),second=createMux(),stats=measureMux(first),one=fingerprint(first.root),two=fingerprint(second.root);
 writeFileSync(`tools/3d/isuzu-mux/code-reference-car/analysis/reference-v04/candidate-geometry.json`,JSON.stringify({stats,firstHash:one,secondHash:two,deterministic:one===two},null,2));
 writeFileSync(`tools/3d/isuzu-mux/code-reference-car/analysis/reference-v04/candidate-controls.json`,JSON.stringify({dimensions,axles,bodyStations,curves,fasciaSections,normalizedLandmarks,referenceCheckpoint,shapeInfluences,headlightCurves,tailLightCurves,rearGlassCurves,rearSections,bumperCornerCurves,v04Design:P.design},null,2));
 expect(one).toBe(two);expect(stats.invalidCoordinates).toBe(0);expect(stats.degenerateTriangles).toBe(0);expect(stats.symmetryUnpairedVertices).toBe(0);
 expect(stats.length).toBeCloseTo(dimensions.length,2);expect(stats.width).toBeCloseTo(dimensions.width,2);expect(stats.height).toBeCloseTo(dimensions.height,2);expect(stats.groundZ).toBeCloseTo(0,5);expect(axles[1]-axles[0]).toBeCloseTo(dimensions.wheelbase,8);expect(stats.triangles).toBeLessThan(100000);
 first.dispose();second.dispose();expect(first.root.children).toHaveLength(0);
});
it('keeps reference control stations ordered and debug geometry separate from website content',()=>{
 for(let i=1;i<bodyStations.length;i++)expect(bodyStations[i][0]).toBeGreaterThan(bodyStations[i-1][0]);
 const v=createMux();expect(v.diagnostics.visible).toBe(false);for(const n of ['curves','cross-sections','landmarks'])expect(v.root.getObjectByName(n)).toBeDefined();for(const n of ['front-side-window','rear-side-window','quarter-glass','windscreen','rear-glass'])expect(v.root.getObjectByName(n)).toBeDefined();expect(v.root.getObjectByName('wheels')?.children).toHaveLength(4);v.dispose();
});

it('keeps monotone station values bounded with a continuous nonzero interior slope',()=>{
 const xs=[0,.3,.8,1],ys=[.2,.4,.7,.8];
 let previous=-Infinity;for(let i=0;i<=100;i++){const value=interpolate(xs,ys,i/100);expect(value).toBeGreaterThanOrEqual(previous-1e-12);expect(value).toBeGreaterThanOrEqual(.2-1e-12);expect(value).toBeLessThanOrEqual(.8+1e-12);previous=value;}
 const epsilon=1e-5,left=(interpolate(xs,ys,.3)-interpolate(xs,ys,.3-epsilon))/epsilon,right=(interpolate(xs,ys,.3+epsilon)-interpolate(xs,ys,.3))/epsilon;expect(left).toBeGreaterThan(.1);expect(Math.abs(left-right)).toBeLessThan(.001);
});


it('keeps new V04 aperture boundaries recessed, curved and mirrored',()=>{
 for(const rear of [false,true]){const left=P.apertureBoundary(rear,-1),right=P.apertureBoundary(rear,1);const xs=right.map(p=>p.x);expect(Math.max(...xs)-Math.min(...xs)).toBeGreaterThan(.08);right.forEach((p,i)=>{expect(p.x).toBeCloseTo(left[i].x,9);expect(p.y).toBeCloseTo(-left[i].y,9);expect(p.toArray().every(Number.isFinite)).toBe(true);});}
 const projected=projectMuxLandmarks(new T.PerspectiveCamera(34,1,.1,80),964,520);expect(projected.headlight0.world.every(Number.isFinite)).toBe(true);
});
it('does not fold the rear quarter longitudinally as it turns into the bumper',()=>{
 for(const band of [0,6,12,18,24]){let previous=-Infinity;for(let i=0;i<=80;i++){const x=dimensions.length/2-.65+.65*i/80,p=section(x,1)[band];expect(p.x).toBeGreaterThanOrEqual(previous-1e-6);previous=p.x;}}
});


it('joins the V04 front and rear skins at shared boundaries without positional gaps',()=>{
 let maximumGap=0,maximumTangentAngle=0;
 for(const rear of [false,true])for(let i=0;i<=24;i++){const h=i/24,x=rear?2.12:-2.12,p=P.sectionPoint(x,h,1,rear),face=P.facePoint(p.z,p.y,rear);maximumGap=Math.max(maximumGap,p.distanceTo(face));const inward=P.sectionPoint(x+(rear?-1:1)*1e-5,h,1,rear).sub(p).normalize(),faceIn=P.facePoint(p.z,p.y-1e-6,rear).sub(face).normalize();maximumTangentAngle=Math.max(maximumTangentAngle,Math.acos(Math.min(1,Math.abs(inward.dot(faceIn))))*180/Math.PI);}
 for(let i=0;i<=32;i++){const y=-.815+1.63*i/32;maximumGap=Math.max(maximumGap,P.rearFramePoint(1.30,y).distanceTo(P.facePoint(1.30,y,true)));}
 const fender=P.frontFender(1),positions=fender.getAttribute('position');for(let i=0;i<=18;i++){const y=.64+.25*i/18;maximumGap=Math.max(maximumGap,new T.Vector3().fromBufferAttribute(positions,i).distanceTo(P.facePoint(P.frontTopZ(y),y)));}fender.dispose();
 writeFileSync('tools/3d/isuzu-mux/code-reference-car/analysis/reference-v04/join-measurements.json',JSON.stringify({maximumPositionGapMetres:maximumGap,maximumCornerTangentAngleDegrees:maximumTangentAngle,scope:'front/rear side terminals, front fender leading edge, rear frame to body',note:'Numerical sampled joints only; does not certify overall visual or reflection continuity'},null,2));expect(maximumGap).toBeLessThan(1e-5);
});
it('keeps the new front and rear apertures visible from their quarter views',()=>{
 const m=createMux();m.root.updateMatrixWorld(true);for(const rear of [false,true]){const point=P.facePoint(rear?1.15:1.02,-.75,rear),dir=new T.Vector3(rear?1:-1,-1,.4).normalize(),ray=new T.Raycaster(point.clone().addScaledVector(dir,10),dir.clone().negate());const hit=ray.intersectObject(m.root,true).find(h=>h.object instanceof T.Mesh);expect(hit?.object.name).toBe(rear?'tail-lamp-body-aperture':'headlamp-body-aperture');}m.dispose();
});

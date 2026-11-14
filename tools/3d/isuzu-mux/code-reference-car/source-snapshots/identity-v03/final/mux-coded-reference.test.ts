import { it, expect } from 'vitest';
import { createHash } from 'node:crypto';
import { writeFileSync } from 'node:fs';
import * as T from 'three';
import { createMux } from '@/components/three/mux/MuxVehicle';
import { measureMux,projectMuxLandmarks } from '@/components/three/mux/MuxValidation';
import { interpolate, lampPoint, section, rearGlassPoint } from '@/components/three/mux/MuxGeometry';
import { dimensions, axles, bodyStations,curves,fasciaSections,normalizedLandmarks,shapeInfluences,headlightCurves,tailLightCurves,rearGlassCurves,rearSections,bumperCornerCurves } from '@/components/three/mux/MuxReferenceData';
function fingerprint(root:T.Group){const hash=createHash('sha256');root.traverse(o=>{if(!(o instanceof T.Mesh))return;hash.update(o.name);for(const name of Object.keys(o.geometry.attributes)){const attr=o.geometry.getAttribute(name);hash.update(Buffer.from(attr.array.buffer));}if(o.geometry.index)hash.update(Buffer.from(o.geometry.index.array.buffer));hash.update(o.position.toArray().join(','));});return hash.digest('hex');}
it('regenerates identical geometry, with locked scale, finite coordinates and symmetry',()=>{
 const first=createMux(),second=createMux(),stats=measureMux(first),one=fingerprint(first.root),two=fingerprint(second.root);
 writeFileSync(`tools/3d/isuzu-mux/code-reference-car/analysis/identity-v03/candidate-geometry.json`,JSON.stringify({stats,firstHash:one,secondHash:two,deterministic:one===two},null,2));
 writeFileSync(`tools/3d/isuzu-mux/code-reference-car/analysis/identity-v03/candidate-controls.json`,JSON.stringify({dimensions,axles,bodyStations,curves,fasciaSections,normalizedLandmarks,shapeInfluences,headlightCurves,tailLightCurves,rearGlassCurves,rearSections,bumperCornerCurves},null,2));
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


it('keeps V03 lamp boundaries three dimensional and mirrored without shifting the wheel anchors',()=>{
 for(const rear of [false,true]){const samples=[];for(let u=0;u<=10;u++)for(let v=0;v<=6;v++){const a=lampPoint(u/10,v/6,1,rear),b=lampPoint(u/10,v/6,-1,rear);expect(a.x).toBeCloseTo(b.x,9);expect(a.y).toBeCloseTo(-b.y,9);expect(a.z).toBeCloseTo(b.z,9);expect(a.toArray().every(Number.isFinite)).toBe(true);expect(Math.abs(a.y)).toBeLessThanOrEqual(dimensions.width/2);samples.push(a.x);}expect(Math.max(...samples)-Math.min(...samples)).toBeGreaterThan(.20);}
 const projected=projectMuxLandmarks(new T.PerspectiveCamera(34,1,.1,80),964,520);expect(projected.headlight0.world).toEqual(lampPoint(0,0,-1).toArray());expect(projected.tailLamp2.world).toEqual(lampPoint(1,1,-1,true).toArray());
 for(let i=0;i<=10;i++){const a=rearGlassPoint(.5,i/10),b=rearGlassPoint(.5,1-i/10);expect(a.x).toBeCloseTo(b.x,7);expect(a.y).toBeCloseTo(-b.y,7);}
});
it('does not fold the rear quarter longitudinally as it turns into the bumper',()=>{
 for(const band of [0,6,12,18,24]){let previous=-Infinity;for(let i=0;i<=80;i++){const x=dimensions.length/2-.65+.65*i/80,p=section(x,1)[band];expect(p.x).toBeGreaterThanOrEqual(previous-1e-6);previous=p.x;}}
});

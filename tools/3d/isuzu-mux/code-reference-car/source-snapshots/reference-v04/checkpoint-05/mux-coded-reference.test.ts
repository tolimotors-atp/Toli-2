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
 writeFileSync(`tools/3d/isuzu-mux/code-reference-car/analysis/reference-v04/candidate-controls.json`,JSON.stringify({dimensions,axles,bodyStations,curves,fasciaSections,normalizedLandmarks,referenceCheckpoint,shapeInfluences,headlightCurves,tailLightCurves,rearGlassCurves,rearSections,bumperCornerCurves,v04Design:P.design,referenceCheckpoint},null,2));
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

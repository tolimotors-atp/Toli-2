import { describe,expect,it } from 'vitest';
import * as T from 'three';
import { writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { createMux as createV04 } from '@/components/three/mux/MuxVehicle';
import * as P from '@/components/three/mux/v05/MuxReferencePatches';
import { createMux as createV05 } from '@/components/three/mux/v05/MuxVehicle';

function measure(root:T.Group){
 let vertices=0,triangles=0,meshes=0,invalid=0,degenerate=0;const materials=new Set<T.Material>(),geometries=new Set<T.BufferGeometry>(),hash=createHash('sha256'),bounds=new T.Box3();
 root.updateMatrixWorld(true);
 root.traverseVisible(o=>{if(!(o instanceof T.Mesh))return;meshes++;const p=o.geometry.getAttribute('position'),index=o.geometry.index;vertices+=p.count;triangles+=(index?.count??p.count)/3;bounds.expandByObject(o);(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>materials.add(m));
  if(geometries.has(o.geometry))return;geometries.add(o.geometry);hash.update(Buffer.from(p.array.buffer,p.array.byteOffset,p.array.byteLength));
  for(let i=0;i<p.count;i++)if(!Number.isFinite(p.getX(i)+p.getY(i)+p.getZ(i)))invalid++;
  const a=new T.Vector3(),b=new T.Vector3(),c=new T.Vector3();for(let i=0;i<(index?.count??p.count);i+=3){a.fromBufferAttribute(p,index?index.getX(i):i);b.fromBufferAttribute(p,index?index.getX(i+1):i+1);c.fromBufferAttribute(p,index?index.getX(i+2):i+2);if(b.sub(a).cross(c.sub(a)).lengthSq()<1e-20)degenerate++;}
 });
 return {vertices,triangles,meshInstances:meshes,materials:materials.size,invalid,degenerate,min:bounds.min.toArray(),max:bounds.max.toArray(),hash:hash.digest('hex')};
}
describe('separate production V05 candidate',()=>{
 it('keeps the raised front-fender leading edge attached to bonnet and fascia',()=>{
  for(const side of [-1,1]){const g=P.frontFender(side),p=g.getAttribute('position');expect(new T.Vector3().fromBufferAttribute(p,0).distanceTo(P.bonnetPoint(0,side))).toBeLessThan(.00001);expect(new T.Vector3().fromBufferAttribute(p,18).distanceTo(P.sectionPoint(-2.12,1,side))).toBeLessThan(.00001);g.dispose();}
 });
 it('preserves the dimensional framework, finite efficient geometry and deterministic regeneration',()=>{
  const old=createV04(),v=createV05(),next=createV05();const v04=measure(old.root),v05=measure(v.root),repeated=measure(next.root);
  expect(v05.invalid).toBe(0);expect(v05.degenerate).toBe(0);expect(v05.triangles).toBeLessThan(120000);expect(v05.min[2]).toBeCloseTo(0,6);expect(v05.max[2]).toBeCloseTo(1.86,5);expect(v05.max[0]-v05.min[0]).toBeLessThan(4.90);expect(v05.max[1]-v05.min[1]).toBeCloseTo(2.20,5);expect(v05.hash).toBe(repeated.hash);
  for(const part of ['front-number-plate','rear-number-plate'])expect(v.root.getObjectByName(part)?.userData.text).toBe('TOLI MOTORS');
  writeFileSync('tools/3d/isuzu-mux/production-v05/geometry-statistics.json',JSON.stringify({v04,v05},null,2));old.dispose();v.dispose();next.dispose();
 });
 it('adds physical lamp structure that remains visible when emission is disabled',()=>{
  const v=createV05();for(const name of ['headlamp-clear-cover','headlamp-projector-depth','headlamp-upper-light-guide','tail-lamp-red-lens','tail-lamp-quarter-continuation','rear-bumper-graphite-valance'])expect(v.root.getObjectByName(name)).toBeDefined();
  v.production.lights(false);const rear=v.root.getObjectByName('tail-lamp-red-reflector') as T.Mesh<T.BufferGeometry,T.MeshStandardMaterial>;expect(rear.material.emissiveIntensity).toBe(0);
  const guide=v.root.getObjectByName('headlamp-upper-light-guide') as T.Mesh<T.BufferGeometry,T.MeshStandardMaterial>;expect(guide.material.emissiveIntensity).toBe(0);expect(guide.visible).toBe(true);v.production.lights(true);expect(guide.material.emissiveIntensity).toBeCloseTo(.38);v.dispose();
 });
});

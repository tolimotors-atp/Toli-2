import * as T from 'three';
import type { createMux } from './MuxVehicle';
export function measureMux(vehicle:ReturnType<typeof createMux>){
 const bounds=new T.Box3(),point=new T.Vector3(),a=new T.Vector3(),b=new T.Vector3(),c=new T.Vector3();
 const degenerateByMesh:Record<string,number>={};
 let vertices=0,triangles=0,degenerates=0,invalidCoordinates=0,meshes=0;const materials=new Set<T.Material>(),symmetric=new Set<string>();
 vehicle.root.updateMatrixWorld(true);
 const key=(x:number,y:number,z:number)=>`${Math.round(x*1e5)},${Math.round(y*1e5)},${Math.round(z*1e5)}`;
 vehicle.root.traverse(o=>{if(!(o instanceof T.Mesh))return;const p=o.geometry.getAttribute('position'),index=o.geometry.index;meshes++;vertices+=p.count;triangles+=(index?.count??p.count)/3;(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>materials.add(m));
  for(let i=0;i<p.count;i++){point.fromBufferAttribute(p,i).applyMatrix4(o.matrixWorld);if(![point.x,point.y,point.z].every(Number.isFinite))invalidCoordinates++;bounds.expandByPoint(point);if(o.parent===vehicle.body||o.parent===vehicle.windows||o.parent===vehicle.front||o.parent===vehicle.rear)symmetric.add(key(point.x,point.y,point.z));}
  for(let i=0;i<(index?.count??p.count);i+=3){const ix=(n:number)=>index?index.getX(n):n;a.fromBufferAttribute(p,ix(i));b.fromBufferAttribute(p,ix(i+1));c.fromBufferAttribute(p,ix(i+2));if(b.sub(a).cross(c.sub(a)).lengthSq()<1e-20){degenerates++;degenerateByMesh[o.name]=(degenerateByMesh[o.name]??0)+1;}}
 });
 let unpaired=0;for(const entry of symmetric){const [x,y,z]=entry.split(',').map(Number);if(!symmetric.has(`${x},${-y||0},${z}`))unpaired++;}
 const wheelGroup=vehicle.root.getObjectByName('wheels')!,centres=[...new Set(wheelGroup.children.map(o=>o.position.x))].sort((a,b)=>a-b);
 const tire=wheelGroup.children[0].children[0] as T.Mesh;tire.geometry.computeBoundingBox();const measuredTire=tire.geometry.boundingBox!.getSize(new T.Vector3()).z;
 const size=bounds.getSize(new T.Vector3());return {length:size.x,width:size.y,height:size.z,groundZ:bounds.min.z,wheelbase:centres[1]-centres[0],tireDiameter:measuredTire,vertices,triangles,meshInstances:meshes,materials:materials.size,degenerateTriangles:degenerates,degenerateByMesh,invalidCoordinates,symmetryUnpairedVertices:unpaired,symmetryToleranceMetres:1e-5,symmetryScope:'body, glazing and broad front/rear surfaces; excludes wheel spoke pattern'};
}

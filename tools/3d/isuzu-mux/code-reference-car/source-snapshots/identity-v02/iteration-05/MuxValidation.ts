import * as T from 'three';
import { axles,track,curves,type Point } from './MuxReferenceData';
import { bonnetPoint,greenhouseY,sample,fasciaPoint } from './MuxGeometry';
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

export function projectMuxLandmarks(camera:T.Camera,width:number,height:number){
 const side=(p:Point)=>new T.Vector3(p[0],-greenhouseY(p[0],p[2]),p[2]);
 const points:Record<string,T.Vector3>={frontWheelNear:new T.Vector3(axles[0],-track/2,.382),rearWheelNear:new T.Vector3(axles[1],-track/2,.382),frontWheelFar:new T.Vector3(axles[0],track/2,.382),rearWheelFar:new T.Vector3(axles[1],track/2,.382),bonnetFrontNear:bonnetPoint(0,-1),bonnetCowlNear:bonnetPoint(1,-1),windscreenLowerNear:new T.Vector3(...curves.windscreen[0]),windscreenUpperNear:new T.Vector3(...curves.windscreen[1]),frontWindowUpper:side(curves.frontWindow[1]),frontWindowRear:side(curves.frontWindow[curves.frontWindow.length-1]),rearWindowRear:side(curves.rearWindow[curves.rearWindow.length-2]),quarterFront:side(curves.quarterWindow[1]),quarterRear:side(curves.quarterWindow[2]),rearGlassLower:new T.Vector3(...curves.rearGlass[0]),roofFront:sample(curves.roofCentre,curves.roofCentre[0][0])};
 for(const [name,list,rear] of [['headlight',curves.headlamp,false],['tailLamp',curves.tailLamp,true],['frontBumper',curves.frontBumper,false],['rearBumper',curves.rearBumper,true]] as const)list.forEach((p,i)=>{points[name+i]=fasciaPoint(p[2],-Math.abs(p[1]),rear);});
 camera.updateMatrixWorld();return Object.fromEntries(Object.entries(points).map(([name,world])=>{const p=world.clone().project(camera);return[name,{world:world.toArray(),pixel:[(p.x+1)*width/2,(1-p.y)*height/2]}];}));
}

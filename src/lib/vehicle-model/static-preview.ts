import * as THREE from 'three';
import {closedInspection} from '../premium-car/inspection';
import {disposeModel,resolveNode,type ImportedVehicle} from './adapter';
import type {VehicleModelManifest} from './contract';
/** Static candidate: retain exported materials and never manufacture moving body panels. */
export function adaptStaticPreview(source:THREE.Group,manifest:VehicleModelManifest,environment:THREE.Texture):ImportedVehicle{
 const wheelNodes=manifest.wheels.map(w=>resolveNode(source,w.nodes[0]));
 if(wheelNodes.length!==4||new Set(wheelNodes).size!==4)throw new Error('Four distinct wheel assemblies are required');
 source.rotation.y+=manifest.yaw;source.updateMatrixWorld(true);
 const bounds=new THREE.Box3().setFromObject(source),size=bounds.getSize(new THREE.Vector3());
 if(!Number.isFinite(size.x+size.y+size.z)||Math.min(size.x,size.y,size.z)<=0)throw new Error('Invalid preview geometry');
 const scale=manifest.targetLength/size.x;if(!(scale>0))throw new Error('Invalid preview scale');
 source.scale.multiplyScalar(scale);source.updateMatrixWorld(true);
 const tires=new THREE.Box3();wheelNodes.forEach(w=>tires.union(new THREE.Box3().setFromObject(w)));
 const center=new THREE.Box3().setFromObject(source).getCenter(new THREE.Vector3());source.position.sub(new THREE.Vector3(center.x,tires.min.y,center.z));
 const root=new THREE.Group();root.name='ISUZU MU-X';root.add(source);root.updateMatrixWorld(true);
 const materials=new Set<THREE.MeshStandardMaterial>(),reflectionMeshes=new Set<THREE.Mesh>();
 source.traverse(n=>{if(n instanceof THREE.Mesh){for(const m of Array.isArray(n.material)?n.material:[n.material])if(m instanceof THREE.MeshStandardMaterial){m.envMap=environment;m.userData.baseOpacity=m.opacity;m.userData.envStrength=m.envMapIntensity;materials.add(m);}}});
 for(const path of manifest.reflection)resolveNode(source,path).traverse(n=>{if(n instanceof THREE.Mesh)reflectionMeshes.add(n);});
 const wheels=wheelNodes.map((node,i)=>{const position=node.getWorldPosition(new THREE.Vector3());const steer=new THREE.Group(),roll=new THREE.Group();source.add(steer);steer.position.copy(source.worldToLocal(position));steer.add(roll);roll.attach(node);return {steer,roll,front:manifest.wheels[i].front,spinAxis:manifest.wheels[i].spinAxis};});
 root.updateMatrixWorld(true);const contactPoints=wheels.map(w=>root.worldToLocal(w.steer.getWorldPosition(new THREE.Vector3())));
 let disposed=false;
 return {root,wheels,rollingRadius:manifest.rollingRadius*scale,contactPoints,materials,reflectionMeshes,
 inspection:{read:closedInspection,command:closedInspection,update:()=>false},
 dispose(){if(disposed)return;disposed=true;disposeModel(root,environment);root.clear();}};
}

import {readFileSync} from 'node:fs';
import {expect,it} from 'vitest';
import * as THREE from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {muxVehicleManifest} from '@/lib/vehicle-model/mux';
import {ACTIVE_VEHICLE_MODEL} from '@/lib/vehicle-model/contract';
import {adaptVehicleModel} from '@/lib/vehicle-model/adapter';
import {requireVehicleAsset} from '@/lib/vehicle-model/registry';
it('loads the actual static MU-X, grounds four tires, preserves materials and refuses panel animation',async()=>{
 const bytes=readFileSync('public/'+muxVehicleManifest.url);const data=new ArrayBuffer(bytes.length);new Uint8Array(data).set(bytes);
 const {scene}=await new GLTFLoader().parseAsync(data,'');let triangles=0;scene.traverse(n=>{if(n instanceof THREE.Mesh)triangles+=(n.geometry.index?.count??n.geometry.attributes.position.count)/3;});expect(triangles).toBe(34010);
 const model=adaptVehicleModel(scene,muxVehicleManifest,new THREE.Texture());const box=new THREE.Box3().setFromObject(model.root);expect(box.getSize(new THREE.Vector3()).x).toBeCloseTo(4.825,3);expect(box.min.y).toBeCloseTo(0,4);expect(model.wheels).toHaveLength(4);
 for(const w of model.wheels)expect(new THREE.Box3().setFromObject(w.roll).min.y).toBeCloseTo(0,4);
 expect(model.materials.size).toBe(10);const paint=[...model.materials].find(m=>m.name==='Silver metallic paint')!;expect(paint.color.r).toBeCloseTo(.47,3);
 expect(model.inspection.command('leftDoor').leftDoor).toBe(false);expect(model.inspection.command('hood').hood).toBe(false);expect(model.inspection.parts).toBeUndefined();
 expect(ACTIVE_VEHICLE_MODEL).toBe(muxVehicleManifest);expect(requireVehicleAsset('suv').url).toBe(muxVehicleManifest.url);model.dispose();model.dispose();
});

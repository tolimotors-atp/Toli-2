import * as T from 'three';
import { createMux as createV04 } from '../MuxVehicle';
import { createMux as createV05 } from './MuxVehicle';
import { createStudioRadiance,prefilterStudioEnvironment } from '@/lib/premium-car/studio-environment';

const canvas=document.querySelector<HTMLCanvasElement>('#mux-canvas')!,renderer=new T.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(1);renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=.85;
const scene=new T.Scene();scene.background=new T.Color(0xe5e5e5);const camera=new T.PerspectiveCamera(34,1,.1,80);camera.up.set(0,0,1);
const models={v04:createV04(),v05:createV05()};scene.add(models.v04.root,models.v05.root);
const source=createStudioRadiance(),env=prefilterStudioEnvironment(renderer,source);scene.environment=env.texture;
scene.add(new T.HemisphereLight(0xffffff,0x737782,1.4));for(const pos of [[-4,-4,7],[3,4,5]]){const light=new T.DirectionalLight(0xffffff,2.4);light.position.set(...pos as [number,number,number]);scene.add(light);}
const floor=new T.Mesh(new T.PlaneGeometry(30,30),new T.MeshStandardMaterial({color:0xd5d5d5,roughness:1}));floor.position.z=-.006;scene.add(floor);
const clay=new T.MeshStandardMaterial({color:0x969696,roughness:.55,side:T.DoubleSide}),reflection=new T.MeshStandardMaterial({color:0x999999,roughness:.15,metalness:1,side:T.DoubleSide});
const original=new Map<T.Mesh,T.Material|T.Material[]>();for(const v of Object.values(models))v.root.traverse(o=>{if(o instanceof T.Mesh)original.set(o,o.material);});
const views:Record<string,T.Vector3>={front:new T.Vector3(-1,0,.10),'front-right':new T.Vector3(-1,-1,.40),right:new T.Vector3(0,-1,.10),'rear-right':new T.Vector3(1,-1,.40),rear:new T.Vector3(1,0,.10),'front-detail':new T.Vector3(-1,-1,.18),'rear-detail':new T.Vector3(1,-1,.18)};
const focuses:Record<string,{target:T.Vector3;direction:T.Vector3;distance:number}>={};
for(const [name,position,distance,rear] of [
 ['headlight',[-2.25,-.73,1.04],1.8,false],['front fender',[-1.55,-.86,1.10],2.6,false],['mirror',[-.8,-.99,1.33],1.4,false],['doors handles',[.25,-.87,1.03],3.8,false],['greenhouse',[.6,-.78,1.51],3.8,false],['D-pillar',[1.90,-.79,1.53],1.9,true],['rear quarter',[1.65,-.9,.98],2.8,true],['rear light',[2.23,-.78,1.18],1.6,true],['rear bumper',[2.32,-.59,.56],2.5,true],['front plate',[-2.42,0,.48],1.5,false],['rear plate',[2.42,0,1.005],1.5,true]
] as [string,number[],number,boolean][]){const id=name+' closeup';const direction=new T.Vector3(rear?1:-1,name.includes('plate')?0:-.8,.16);if(['mirror','doors handles','greenhouse'].includes(name))direction.x=0;focuses[id]={target:new T.Vector3(...position as [number,number,number]),direction:direction.normalize(),distance};views[id]=direction;}
let view='front-right';
function draw(){
 const candidate=(document.querySelector<HTMLSelectElement>('#candidate')!.value) as keyof typeof models,mode=document.querySelector<HTMLSelectElement>('#mode')!.value,m=models[candidate];models.v04.root.visible=candidate==='v04';models.v05.root.visible=candidate==='v05';
 for(const [mesh,material] of original){mesh.material=mode==='clay'||mode==='body only'?clay:mode==='reflection'?reflection:material;const mats=Array.isArray(material)?material:[material];for(const mat of mats)if(mat instanceof T.MeshStandardMaterial)mat.wireframe=mode==='wireframe';}
 m.root.getObjectByName('wheels')!.visible=mode!=='body only';m.windows.visible=mode!=='body only';m.front.visible=mode!=='body only';m.rear.visible=mode!=='body only';m.exterior.root.visible=mode!=='body only';models.v05.production.root.visible=mode!=='body only';models.v05.production.lights(mode==='lights on');
 const width=canvas.clientWidth,height=canvas.clientHeight;renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix();
 const dir=views[view].clone().normalize(),target=focuses[view]?.target.clone()??new T.Vector3(0,0,.95),right=new T.Vector3().crossVectors(camera.up,dir).normalize(),up=new T.Vector3().crossVectors(dir,right),tan=Math.tan(T.MathUtils.degToRad(17));let distance=0;
 for(const x of [-2.44,2.44])for(const y of [-1.11,1.11])for(const z of [0,1.86]){const p=new T.Vector3(x,y,z).sub(target);distance=Math.max(distance,p.dot(dir)+Math.max(Math.abs(p.dot(right))/(tan*camera.aspect),Math.abs(p.dot(up))/tan));}
 if(view.includes('detail'))distance*=.64;if(focuses[view])distance=focuses[view].distance/1.10;
 camera.position.copy(target).addScaledVector(dir,distance*1.10);camera.lookAt(target);camera.updateMatrixWorld();renderer.render(scene,camera);
 const stats={candidate,mode,view,drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles};canvas.dataset.state=JSON.stringify(stats);document.querySelector('#metrics')!.textContent=JSON.stringify(stats,null,2);document.querySelector('#status')!.textContent=`${candidate} / ${mode} / ${view} — NOT ACTIVATED`;
}
for(const name of Object.keys(views)){const b=document.createElement('button');b.textContent=name;b.onclick=()=>{view=name;draw();};document.querySelector('#views')!.append(b);}
for(const id of ['candidate','mode'])document.querySelector('#'+id)!.addEventListener('change',draw);
new ResizeObserver(draw).observe(canvas);draw();
window.addEventListener('pagehide',()=>{Object.values(models).forEach(m=>m.dispose());floor.geometry.dispose();floor.material.dispose();clay.dispose();reflection.dispose();env.dispose();source.dispose();renderer.dispose();});

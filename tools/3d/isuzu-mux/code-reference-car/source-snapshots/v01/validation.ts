import * as T from 'three';
import { RectAreaLightUniformsLib } from 'three/examples/jsm/lights/RectAreaLightUniformsLib.js';
import { createStudioRadiance,prefilterStudioEnvironment } from '@/lib/premium-car/studio-environment';
import { createMux } from './MuxVehicle';
import { measureMux } from './MuxValidation';
import { primaryViews,type MuxView } from './MuxReferenceData';

// Isolated development entry; never imported by the website application.
const canvas=document.querySelector<HTMLCanvasElement>('#mux-canvas')!,status=document.querySelector<HTMLElement>('#status')!;
const renderer=new T.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(1);renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=.85;
const scene=new T.Scene();scene.background=new T.Color(0xe5e5e5);const camera=new T.PerspectiveCamera(34,1,.1,80);camera.up.set(0,0,1);
const mux=createMux();scene.add(mux.root);const target=new T.Vector3(0,0,.95);
RectAreaLightUniformsLib.init();const source=createStudioRadiance(),env=prefilterStudioEnvironment(renderer,source);scene.environment=env.texture;
scene.add(new T.HemisphereLight(0xffffff,0x777777,1.2));const key=new T.DirectionalLight(0xffffff,2.0);key.position.set(-4,4,7);scene.add(key);
for(const y of [-4,4]){const strip=new T.RectAreaLight(0xffffff,4,6,1.1);strip.position.set(0,y,5);strip.lookAt(target);scene.add(strip);}
const ground=new T.Mesh(new T.PlaneGeometry(60,60),new T.MeshStandardMaterial({color:0xd5d5d5,roughness:1}));ground.position.z=-.006;scene.add(ground);
const stats=measureMux(mux);document.querySelector('#metrics')!.textContent=JSON.stringify(stats,null,2);
const views:Record<MuxView,T.Vector3>={front:new T.Vector3(-1,0,.10),'front-left':new T.Vector3(-1,1,.40),left:new T.Vector3(0,1,.10),'rear-left':new T.Vector3(1,1,.40),rear:new T.Vector3(1,0,.10),'rear-right':new T.Vector3(1,-1,.40),right:new T.Vector3(0,-1,.10),'front-right':new T.Vector3(-1,-1,.40),overhead:new T.Vector3(.001,0,1)};
let view:MuxView='front-left',mode='clay',zoom=1;
const zebra=new T.ShaderMaterial({side:T.DoubleSide,vertexShader:'varying vec3 n; varying vec3 v; void main(){vec4 p=modelViewMatrix*vec4(position,1.); n=normalize(normalMatrix*normal);v=normalize(-p.xyz);gl_Position=projectionMatrix*p;}',fragmentShader:'varying vec3 n; varying vec3 v;void main(){vec3 r=reflect(-normalize(v),normalize(n));float q=sin((r.x*.65+r.y*.25+r.z*.6)*40.);float stripe=smoothstep(-.035,.035,q);gl_FragColor=vec4(vec3(mix(.12,.93,stripe)),1.);}'});
const originals=new Map<T.Mesh,T.Material|T.Material[]>();mux.body.traverse(o=>{if(o instanceof T.Mesh)originals.set(o,o.material);});
function draw(){
 const width=canvas.clientWidth,height=canvas.clientHeight;renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix();const dir=views[view].clone().normalize();
 const right=new T.Vector3().crossVectors(new T.Vector3(0,0,1),dir).normalize(),up=new T.Vector3().crossVectors(dir,right),tan=Math.tan(T.MathUtils.degToRad(17));let fit=0;for(const x of [-2.413,2.413])for(const y of [-.93,.93])for(const z of [0,1.86]){const p=new T.Vector3(x,y,z).sub(target);fit=Math.max(fit,p.dot(dir)+Math.abs(p.dot(up))/tan,p.dot(dir)+Math.abs(p.dot(right))/(tan*camera.aspect));}const distance=fit*1.12*zoom;
 camera.position.copy(dir.multiplyScalar(distance).add(target));camera.lookAt(target);renderer.render(scene,camera);canvas.dataset.view=view;canvas.dataset.mode=mode;canvas.dataset.ready='true';canvas.dataset.drawCalls=String(renderer.info.render.calls);canvas.dataset.renderedTriangles=String(renderer.info.render.triangles);status.textContent=`${view} / ${mode} / ${renderer.info.render.calls} draw calls · Primary geometry candidate, not approved`;
}
for(const name of primaryViews){const button=document.createElement('button');button.textContent=name;button.type='button';button.onclick=()=>{view=name;draw();};document.querySelector('#views')!.append(button);}
document.querySelector<HTMLSelectElement>('#mode')!.onchange=e=>{mode=(e.target as HTMLSelectElement).value;for(const [mesh,original] of originals){mesh.material=mode==='zebra'?zebra:original;if(original instanceof T.MeshPhysicalMaterial||original instanceof T.MeshStandardMaterial)original.wireframe=mode==='wireframe';}mux.materials.clay.metalness=mode==='reflection'?.65:0;mux.materials.clay.roughness=mode==='reflection'?.22:.44;draw();};
for(const name of ['body','wireframe','curves','cross-sections','landmarks','wheels','windows','front-landmarks','rear-landmarks']){
 const input=document.querySelector<HTMLInputElement>(`input[value="${name}"]`)!;input.onchange=()=>{if(name==='wireframe'){for(const [mesh] of originals){if(mesh.material instanceof T.MeshPhysicalMaterial||mesh.material instanceof T.MeshStandardMaterial)mesh.material.wireframe=input.checked;}}else{const object=mux.root.getObjectByName(name);if(object)object.visible=input.checked;}
 mux.diagnostics.visible=['curves','cross-sections','landmarks'].some(n=>document.querySelector<HTMLInputElement>(`input[value="${n}"]`)!.checked);draw();};
}
document.querySelector<HTMLInputElement>('#zoom')!.oninput=e=>{zoom=Number((e.target as HTMLInputElement).value);draw();};
new ResizeObserver(draw).observe(canvas);draw();
window.addEventListener('pagehide',()=>{mux.dispose();env.dispose();source.dispose();zebra.dispose();renderer.dispose();});

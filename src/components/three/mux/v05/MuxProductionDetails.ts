import * as T from 'three';
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import * as P from './MuxReferencePatches';
import * as G from '../MuxGeometry';
import { sideSurface } from './MuxExteriorDetails';

// Silver studio front/rear and rear-quarter photographs, not later-generation MU-X lamps.
export function addProductionDetails(base:Record<string,T.Material>,front:T.Group,rear:T.Group,root:T.Group){
 const chrome=new T.MeshStandardMaterial({color:0xbfc3c8,metalness:.85,roughness:.22,side:T.DoubleSide});
 const lens=new T.MeshPhysicalMaterial({color:0xa5b5c2,roughness:.12,metalness:.05,clearcoat:1,transparent:true,opacity:.16,depthWrite:false,side:T.FrontSide});
 const redLens=new T.MeshPhysicalMaterial({color:0x7c0d1b,roughness:.24,metalness:.08,clearcoat:.8,side:T.DoubleSide});
 const white=new T.MeshStandardMaterial({color:0xc8d4df,roughness:.25,metalness:.15,emissive:0xdce8fa,emissiveIntensity:.06,side:T.DoubleSide});
 const red=new T.MeshStandardMaterial({color:0xb91d30,roughness:.3,emissive:0xe21c30,emissiveIntensity:.06,side:T.DoubleSide});
 const details=new T.Group();details.name='production-details';root.add(details);
 const add=(parent:T.Group,name:string,g:T.BufferGeometry,m:T.Material)=>{const mesh=new T.Mesh(g,m);mesh.name=name;parent.add(mesh);return mesh;};
 const scaled=(pts:number[][],scale:number)=>{const y=pts.reduce((s,p)=>s+p[0],0)/pts.length,z=pts.reduce((s,p)=>s+p[1],0)/pts.length;return pts.map(p=>[y+(p[0]-y)*scale,z+(p[1]-z)*scale]);};
 const guide=(parent:T.Group,name:string,points:number[][],side:number,isRear:boolean,material:T.Material,radius=.005)=>add(parent,name,new T.TubeGeometry(G.curve(points.map(p=>{const v=P.facePoint(p[1],p[0]*side,isRear);v.x+=(isRear?1:-1)*.010;return v.toArray() as [number,number,number];})),20,radius,5,false),material);
 for(const side of [-1,1]){
  add(front,'headlamp-chrome-bezel',P.detailRim(P.design.headlight,side,false,.009),chrome);
  add(front,'headlamp-clear-cover',P.detailFace(scaled(P.design.headlight,.96),side,false,.013),lens);
  const projector=Array.from({length:25},(_,i)=>{const a=i/24*Math.PI*2;return [.727+.061*Math.cos(a),1.025+.061*Math.sin(a)];});
  guide(front,'headlamp-projector-rim',projector,side,false,chrome,.007);
  add(front,'headlamp-projector-depth',P.detailFace(projector,side,false,.006),base.glass);
  guide(front,'headlamp-upper-light-guide',[[.547,1.041],[.677,1.087],[.862,1.146]],side,false,white,.005);
  guide(front,'headlamp-lower-reflector-return',[[.633,.967],[.677,.943],[.779,.939],[.851,.971],[.859,1.091]],side,false,chrome,.004);
  add(rear,'tail-lamp-red-lens',P.detailFace(scaled(P.design.tailLight,.96),side,true,.005),redLens);
  add(rear,'tail-lamp-outer-bezel',P.detailRim(P.design.tailLight,side,true,.007),base.rubber);
  guide(rear,'tail-lamp-clear-upper-band',[[.529,1.208],[.669,1.223],[.839,1.254]],side,true,white,.009);
  for(const z of [1.108,1.145,1.18])guide(rear,'tail-lamp-red-reflector',[[.615,z],[.727,z-.012],[.848,z+.003]],side,true,red,.006);
  const wrap=P.sideDetail([[1.89,1.282],[2.105,1.289],[2.12,1.072],[1.945,1.092]],side,sideSurface);
  add(rear,'tail-lamp-quarter-continuation',wrap,redLens);
  const fog=[[.642,.699],[.818,.726],[.847,.541],[.647,.535]];
  add(front,'fog-pocket-housing',P.detailFace(fog,side,false,.005),base.rubber);add(front,'fog-pocket-surround',P.detailRim(fog,side,false,.010),chrome);
  const fogRing=Array.from({length:25},(_,i)=>{const a=i/24*Math.PI*2;return [.737+.041*Math.cos(a),.625+.041*Math.sin(a)];});
  guide(front,'fog-lamp-reflector',fogRing,side,false,chrome,.006);add(front,'fog-lamp-lens',P.detailFace(fogRing,side,false,.008),lens);
  const reflector=[[.635,.635],[.807,.662],[.824,.565],[.697,.550]];
  add(rear,'bumper-reflector-pocket',P.detailFace(reflector,side,true,.006),base.rubber);add(rear,'bumper-reflector',P.detailFace(scaled(reflector,.70),side,true,.009),red);
 }
 for(const points of [P.design.grilleUpper,P.design.grilleLower])add(front,'sculpted-chrome-grille-surround',P.detailRim(points,1,false,.025),chrome);
 for(const z of [.566,.615,.664])guide(front,'lower-grille-slat',[[-.535,z],[0,z-.002],[.535,z]],1,false,base.dark,.006);
 const rearValance=[[-.73,.530],[-.55,.551],[.55,.551],[.73,.530],[.70,.427],[-.70,.427]];
 add(rear,'rear-bumper-graphite-valance',P.detailFace(rearValance,1,true,.006),base.rubber);
 add(rear,'tailgate-chrome-brow',P.detailFace([[-.53,1.226],[.53,1.226],[.47,1.198],[-.47,1.198]],1,true,.009),chrome);
 // Dark economical cabin/underfloor prevents see-through voids behind the tinted glass.
 const blocks:T.BufferGeometry[]=[];
 const block=(size:number[],at:number[])=>{const g=new T.BoxGeometry(...size as [number,number,number]);g.translate(...at as [number,number,number]);blocks.push(g);};
 block([3.55,1.45,.13],[.15,0,.42]);block([.26,1.43,.20],[-.79,0,1.12]);
 for(const x of [-.32,.57,1.31])for(const y of [-.40,.40]){block([.40,.48,.12],[x,y,.78]);block([.10,.48,.48],[x+.15,y,1.01]);block([.09,.22,.15],[x+.15,y,1.34]);}
 const cabin=mergeGeometries(blocks)!;blocks.forEach(g=>g.dispose());add(details,'simplified-cabin-and-underfloor',cabin,base.rubber);
 return {root:details,materials:[chrome,lens,redLens,white,red],lights(on:boolean){white.emissiveIntensity=on?.38:0;red.emissiveIntensity=on?.30:0;}};
}

import * as T from 'three';
import { dimensions, curves, bodyStations, referenceCheckpoint, type Point } from '../MuxReferenceData';
import { pruneCollapsedTriangles } from '../MuxGeometry';
import * as G from '../MuxGeometry';
import * as P from './MuxReferencePatches';
import { createExteriorDetails } from './MuxExteriorDetails';
import { addProductionDetails } from './MuxProductionDetails';
import { wheels } from '../MuxWheels';
export function createMux(){
  const root=new T.Group();root.name='MU-X CODED PRODUCTION V05 — DEVELOPMENT CANDIDATE';
  const materials={clay:new T.MeshPhysicalMaterial({color:0xb4b7bd,roughness:.30,metalness:.48,clearcoat:.72,clearcoatRoughness:.22,side:T.DoubleSide}),glass:new T.MeshPhysicalMaterial({color:0x46535e,roughness:.22,metalness:.22,transparent:true,opacity:.91,depthWrite:false,side:T.FrontSide}),rubber:new T.MeshStandardMaterial({color:0x222222,roughness:.90,side:T.DoubleSide}),alloy:new T.MeshStandardMaterial({color:0x868686,roughness:.34,metalness:.5,side:T.DoubleSide}),dark:new T.MeshStandardMaterial({color:0x444444,roughness:.57,side:T.DoubleSide}),mirror:new T.MeshPhysicalMaterial({color:0xaab5c0,roughness:.10,metalness:1,side:T.DoubleSide}),plate:new T.MeshStandardMaterial({color:0xe5e4dd,roughness:.65,side:T.DoubleSide})};
  const body=new T.Group();body.name='body';const windows=new T.Group();windows.name='windows';const front=new T.Group();front.name='front-landmarks';const rear=new T.Group();rear.name='rear-landmarks';
  const add=(group:T.Group,name:string,geometry:T.BufferGeometry,material:T.Material=materials.clay)=>{const m=new T.Mesh(geometry,material);m.name=name;group.add(m);return m;};
  for(const side of [-1,1]){
    add(body,'compound-side-and-arch-volume',G.sideBody(side,-1,referenceCheckpoint>=3?1:dimensions.length/2));if(referenceCheckpoint>=3)add(body,'new-rear-quarter',P.sidePatch(side,true));add(body,'new-front-side-skin',P.sidePatch(side));add(body,'rear-arch-depth-return',P.rearArchReturn(side),materials.dark);add(body,'front-fender-crown',P.frontFender(side));
    (referenceCheckpoint>=3?P.preservedCabin(side):G.cabin(side)).forEach(g=>add(body,'painted-pillar-network',g));(referenceCheckpoint>=3?P.preservedCabin(side,true):G.cabin(side,true)).forEach((g,i)=>add(windows,['front-side-window','rear-side-window','quarter-glass'][i],g,materials.glass));if(referenceCheckpoint>=3){add(body,'new-D-pillar-side-frame',P.sideFrame(side));add(windows,'quarter-glass',P.sideFrame(side,true),materials.glass);}
  }
  add(body,'crowned-bonnet',P.bonnet());add(body,'crowned-roof',G.roof());add(body,'wrapped-front-fascia',P.endFace());add(body,'recessed-wrapped-tailgate',referenceCheckpoint>=4?P.endFace(true):G.fascia(true));
  add(windows,'windscreen',G.screen(),materials.glass);add(windows,'rear-glass',referenceCheckpoint>=3?P.rearFrame(true):G.screen(true),materials.glass);
  // Only outer apertures and recessed backing until the clay identity gates pass.
  for(const [name,points] of [['upper-grille-aperture',P.design.grilleUpper],['lower-grille-aperture',P.design.grilleLower],['lower-opening-envelope',P.design.lowerOpening]] as const)add(front,name,P.grilleBacking(points),materials.dark);
  for(const side of [-1,1]){add(front,'headlamp-body-aperture',P.apertureBacking(side),materials.dark);if(referenceCheckpoint>=4)add(rear,'tail-lamp-body-aperture',P.apertureBacking(side,true),materials.dark);else{add(rear,'tail-lamp-aperture-housing',G.lampHousing(side,true),materials.dark);add(rear,'tail-lamp-curved-lens',G.lampSurface(side,true),materials.glass);}}
  if(referenceCheckpoint>=3)add(body,'new-D-pillar-rear-frame',P.rearFrame());else add(body,'rear-roof-trailing-lip',G.rearRoofLip());if(referenceCheckpoint<4)add(rear,'lower-bumper-return',G.rearLower(),materials.dark);
  const exterior=createExteriorDetails(materials);root.add(body,windows,front,rear,wheels(materials),exterior.root);const production=addProductionDetails(materials,front,rear,root);
  // Basic rail envelope accounts for the supplied height, without spending time on rail detailing.
  for(const side of [-1,1]){const c=G.curve([[-.24,side*.68,1.80],[.05,side*.70,1.844],[1.38,side*.71,1.844],[1.78,side*.69,1.80]]);const rail=new T.TubeGeometry(c,32,.016,8,false),rp=rail.getAttribute('position');for(let i=0;i<rp.count;i++)rp.setZ(i,Math.min(dimensions.height,rp.getZ(i)));rail.computeVertexNormals();add(body,'roof-height-envelope',rail,materials.dark);}
  const cleaned=new Set<T.BufferGeometry>();root.traverse(o=>{if(o instanceof T.Mesh&&!cleaned.has(o.geometry)){pruneCollapsedTriangles(o.geometry);cleaned.add(o.geometry);}});
  const diagnostics=new T.Group();diagnostics.name='diagnostics';const curveGroup=new T.Group();curveGroup.name='curves';const sections=new T.Group();sections.name='cross-sections';const landmarks=new T.Group();landmarks.name='landmarks';
  const lineMaterial=new T.LineBasicMaterial({color:0x0864b0,depthTest:false}),sectionMaterial=new T.LineBasicMaterial({color:0xa33613,depthTest:false});
  for(const [name,points] of Object.entries(curves))for(const side of name==='bonnetCentre'||name==='roofCentre'?[1]:[-1,1]){const p=(points as Point[]).map(v=>[v[0],v[1]*side,v[2]] as Point);const line=new T.Line(new T.BufferGeometry().setFromPoints(G.curve(p).getPoints(64)),lineMaterial);line.name=name;line.renderOrder=10;curveGroup.add(line);}
  bodyStations.forEach(s=>{const x=(s[0]-.5)*dimensions.length,points=[...G.section(x,1).reverse(),...G.section(x,-1)];const line=new T.Line(new T.BufferGeometry().setFromPoints(points),sectionMaterial);line.renderOrder=11;sections.add(line);});
  const pointData=Object.values(curves).flat().flatMap(p=>p);const pg=new T.BufferGeometry();pg.setAttribute('position',new T.Float32BufferAttribute(pointData,3));landmarks.add(new T.Points(pg,new T.PointsMaterial({color:0xce2533,size:.035,depthTest:false})));
  const headlightDebug=new T.Group(),rearDebug=new T.Group();headlightDebug.name='headlight-debug';rearDebug.name='rear-debug';
  for(const [debug,isRear] of [[headlightDebug,false],[rearDebug,true]] as const){for(const side of [-1,1]){const points=P.apertureBoundary(isRear,side);points.push(points[0]);const mat=new T.LineBasicMaterial({color:isRear?0x2280bd:0xd31f3b,depthTest:false});const line=new T.Line(new T.BufferGeometry().setFromPoints(points),mat);line.renderOrder=20;debug.add(line);}debug.visible=false;}
  curveGroup.visible=false;sections.visible=false;landmarks.visible=false;diagnostics.add(curveGroup,sections,landmarks,headlightDebug,rearDebug);root.add(diagnostics);diagnostics.visible=false;
  return {root,body,windows,front,rear,exterior,production,diagnostics,materials,dispose(){const geometries=new Set<T.BufferGeometry>(),mats=new Set<T.Material>();root.traverse(o=>{if(o instanceof T.Mesh||o instanceof T.Line||o instanceof T.Points){geometries.add(o.geometry);(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>mats.add(m));}});geometries.forEach(g=>g.dispose());mats.forEach(m=>m.dispose());root.clear();}};
}

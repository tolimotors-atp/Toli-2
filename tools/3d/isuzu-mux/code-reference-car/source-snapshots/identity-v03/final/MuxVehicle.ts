import * as T from 'three';
import { dimensions, curves, bodyStations, headlightCurves,tailLightCurves,rearGlassCurves,bumperCornerCurves,type Point } from './MuxReferenceData';
import { pruneCollapsedTriangles } from './MuxGeometry';
import * as G from './MuxGeometry';
import { wheels } from './MuxWheels';
export function createMux(){
  const root=new T.Group();root.name='MU-X CODED IDENTITY V03 — UNAPPROVED CANDIDATE';
  const materials={clay:new T.MeshPhysicalMaterial({color:0x949494,roughness:.44,metalness:0,side:T.DoubleSide}),glass:new T.MeshPhysicalMaterial({color:0x30373b,roughness:.24,metalness:.08,side:T.DoubleSide}),rubber:new T.MeshStandardMaterial({color:0x222222,roughness:.90,side:T.DoubleSide}),alloy:new T.MeshStandardMaterial({color:0x868686,roughness:.34,metalness:.5,side:T.DoubleSide}),dark:new T.MeshStandardMaterial({color:0x444444,roughness:.57,side:T.DoubleSide})};
  const body=new T.Group();body.name='body';const windows=new T.Group();windows.name='windows';const front=new T.Group();front.name='front-landmarks';const rear=new T.Group();rear.name='rear-landmarks';
  const add=(group:T.Group,name:string,geometry:T.BufferGeometry,material:T.Material=materials.clay)=>{const m=new T.Mesh(geometry,material);m.name=name;group.add(m);return m;};
  for(const side of [-1,1]){
    add(body,'compound-side-and-arch-volume',G.sideBody(side));add(body,'rear-arch-depth-return',G.rearArchReturn(side),materials.dark);add(body,'front-fender-crown',G.fenderTop(side));
    G.cabin(side).forEach(g=>add(body,'painted-pillar-network',g));G.cabin(side,true).forEach((g,i)=>add(windows,['front-side-window','rear-side-window','quarter-glass'][i],g,materials.glass));
  }
  add(body,'crowned-bonnet',G.bonnet());add(body,'crowned-roof',G.roof());add(body,'wrapped-front-fascia',G.fascia());add(body,'recessed-wrapped-tailgate',G.fascia(true));
  add(windows,'windscreen',G.screen(),materials.glass);add(windows,'rear-glass',G.screen(true),materials.glass);
  // Broad identity envelopes only. No grille mesh, lamps internals, badges or decorative trim.
  for(const [name,points] of [['upper-grille-aperture',curves.grilleUpper],['lower-grille-aperture',curves.grilleLower],['lower-opening-envelope',curves.lowerOpening]] as const)add(front,name,G.fasciaEnvelope(points),materials.dark);
  for(const side of [-1,1])for(const isRear of [false,true]){const group=isRear?rear:front,prefix=isRear?'tail-lamp':'headlamp';add(group,prefix+'-aperture-housing',G.lampHousing(side,isRear),materials.dark);add(group,prefix+'-curved-lens',G.lampSurface(side,isRear),materials.glass);add(group,prefix+'-upper-signature',G.lampSignature(side,isRear),materials.alloy);if(!isRear)add(group,'simplified-headlamp-reflector',G.headlightReflector(side),materials.alloy);}
  add(body,'rear-roof-trailing-lip',G.rearRoofLip());add(rear,'lower-bumper-return',G.rearLower(),materials.dark);
  root.add(body,windows,front,rear,wheels(materials));
  // Basic rail envelope accounts for the supplied height, without spending time on rail detailing.
  for(const side of [-1,1]){const c=G.curve([[-.24,side*.68,1.80],[.05,side*.70,1.844],[1.38,side*.71,1.844],[1.78,side*.69,1.80]]);const rail=new T.TubeGeometry(c,32,.016,8,false),rp=rail.getAttribute('position');for(let i=0;i<rp.count;i++)rp.setZ(i,Math.min(dimensions.height,rp.getZ(i)));rail.computeVertexNormals();add(body,'roof-height-envelope',rail,materials.dark);}
  const cleaned=new Set<T.BufferGeometry>();root.traverse(o=>{if(o instanceof T.Mesh&&!cleaned.has(o.geometry)){pruneCollapsedTriangles(o.geometry);cleaned.add(o.geometry);}});
  const diagnostics=new T.Group();diagnostics.name='diagnostics';const curveGroup=new T.Group();curveGroup.name='curves';const sections=new T.Group();sections.name='cross-sections';const landmarks=new T.Group();landmarks.name='landmarks';
  const lineMaterial=new T.LineBasicMaterial({color:0x0864b0,depthTest:false}),sectionMaterial=new T.LineBasicMaterial({color:0xa33613,depthTest:false});
  for(const [name,points] of Object.entries(curves))for(const side of name==='bonnetCentre'||name==='roofCentre'?[1]:[-1,1]){const p=(points as Point[]).map(v=>[v[0],v[1]*side,v[2]] as Point);const line=new T.Line(new T.BufferGeometry().setFromPoints(G.curve(p).getPoints(64)),lineMaterial);line.name=name;line.renderOrder=10;curveGroup.add(line);}
  bodyStations.forEach(s=>{const x=(s[0]-.5)*dimensions.length,points=[...G.section(x,1).reverse(),...G.section(x,-1)];const line=new T.Line(new T.BufferGeometry().setFromPoints(points),sectionMaterial);line.renderOrder=11;sections.add(line);});
  const pointData=Object.values(curves).flat().flatMap(p=>p);const pg=new T.BufferGeometry();pg.setAttribute('position',new T.Float32BufferAttribute(pointData,3));landmarks.add(new T.Points(pg,new T.PointsMaterial({color:0xce2533,size:.035,depthTest:false})));
  const headlightDebug=new T.Group(),rearDebug=new T.Group();headlightDebug.name='headlight-debug';rearDebug.name='rear-debug';
  for(const [debug,networks] of [[headlightDebug,{...headlightCurves}],[rearDebug,{...tailLightCurves,glassTop:rearGlassCurves.top,glassBottom:rearGlassCurves.bottom,glassSide:rearGlassCurves.side,bumperLeft:bumperCornerCurves.left,bumperRight:bumperCornerCurves.right}]] as const){
    Object.entries(networks).forEach(([name,points],i)=>{for(const side of [-1,1]){const p=points.map(v=>[v[0],v[1]*side,v[2]] as Point),mat=new T.LineBasicMaterial({color:[0xd31f3b,0x007cda,0x2e9954,0xc27b00,0x8e27c4,0x008b92,0xd34c00,0x3344dd][i%8],depthTest:false});const line=new T.Line(new T.BufferGeometry().setFromPoints(G.curve(p).getPoints(60)),mat);line.name=name;line.renderOrder=20;debug.add(line);const pg=new T.BufferGeometry().setFromPoints(p.map(G.vec));debug.add(new T.Points(pg,new T.PointsMaterial({color:mat.color,size:.024,depthTest:false})));}});
    debug.visible=false;
  }
  curveGroup.visible=false;sections.visible=false;landmarks.visible=false;diagnostics.add(curveGroup,sections,landmarks,headlightDebug,rearDebug);root.add(diagnostics);diagnostics.visible=false;
  return {root,body,windows,front,rear,diagnostics,materials,dispose(){const geometries=new Set<T.BufferGeometry>(),mats=new Set<T.Material>();root.traverse(o=>{if(o instanceof T.Mesh||o instanceof T.Line||o instanceof T.Points){geometries.add(o.geometry);(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>mats.add(m));}});geometries.forEach(g=>g.dispose());mats.forEach(m=>m.dispose());root.clear();}};
}

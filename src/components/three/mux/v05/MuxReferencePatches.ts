import * as T from 'three';
import { mergeVertices } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import { dimensions,axles,archRadius,curves,referenceCheckpoint,type Point } from '../MuxReferenceData';
import * as G from '../MuxGeometry';

// V05 local regions: new trace-derived design boundaries, not the V03 lamp/deformation functions.
export const design={
 headlight:[[.510,1.037],[.660,1.083],[.872,1.157],[.893,1.098],[.881,.956],[.744,.918],[.610,.944]],
 tailLight:[[.475,1.213],[.658,1.235],[.851,1.272],[.874,1.210],[.866,1.065],[.726,1.048],[.586,1.090]],
 quarterGlass:[[1.45,1.290],[1.42,1.370],[1.40,1.630],[1.43,1.680],[1.89,1.663],[1.94,1.620],[2.025,1.370],[2.02,1.330],[1.54,1.290]],
 rearGlass:[[-.66,1.700],[-.49,1.721],[.49,1.721],[.66,1.700],[.75,1.415],[.75,1.335],[.52,1.315],[-.52,1.315],[-.75,1.335],[-.75,1.415]],
 frontRows:[[.39,.78,-2.31],[.52,.86,-2.4125],[.72,.89,-2.38],[.90,.895,-2.34],[1.04,.89,-2.32],[1.18,.89,-2.28]],
 rearRows:[[.39,.80,2.32],[.49,.85,2.4125],[.62,.88,2.39],[.72,.875,2.35],[.82,.865,2.335],[1.06,.855,2.335],[1.22,.84,2.29],[1.30,.815,2.26]],
 rearBaseRows:[[.39,.80,2.32],[.49,.85,2.38],[.62,.88,2.37],[.72,.875,2.35],[.82,.865,2.335],[1.06,.855,2.335],[1.22,.84,2.29],[1.30,.815,2.26]],
 grilleUpper:[[-.548,1.035],[.548,1.035],[.492,.913],[-.492,.913]],
 grilleLower:[[-.474,.866],[.474,.866],[.407,.772],[-.407,.772]],
 lowerOpening:[[-.590,.707],[.590,.707],[.552,.536],[-.552,.536]]
} satisfies Record<string,number[][]>;
const clamp=T.MathUtils.clamp;
function scalar(points:number[][],x:number,column:number){return G.interpolate(points.map(p=>p[0]),points.map(p=>p[column]),x);}
export function facePoint(z:number,y:number,rear=false){
 const rows=rear?(referenceCheckpoint>=5?design.rearRows:design.rearBaseRows):design.frontRows,width=scalar(rows,z,1),centre=scalar(rows,z,2),edge=rear?2.12:-2.12,inner=rear?.58:.53;
 const q=clamp((Math.abs(y)-inner)/(width-inner),0,1),ellipse=Math.sqrt(Math.max(0,1-q*q));
 let x=edge+(centre-edge)*ellipse;if(rear){const centreWeight=Math.pow(Math.max(0,1-Math.pow(y/.79,2)),2);x-=.016*Math.exp(-Math.pow((z-1.005)/.145,4))*centreWeight;x+=.010*Math.exp(-Math.pow((z-.79)/.16,2))*centreWeight;}
 return new T.Vector3(x,y,z);
}
function loop(points:number[][]){
 const p=points.map(v=>new T.Vector2(v[0],v[1])),shape=new T.Shape(),round=.08,start=p[0].clone().lerp(p[1],round);shape.moveTo(start.x,start.y);
 for(let n=1;n<=p.length;n++){const i=n%p.length,at=p[i],a=at.clone().lerp(p[(i+p.length-1)%p.length],round),b=at.clone().lerp(p[(i+1)%p.length],round);shape.lineTo(a.x,a.y);shape.quadraticCurveTo(at.x,at.y,b.x,b.y);}shape.closePath();return shape.getPoints(3).slice(0,-1);
}
function polygon(points:number[][],smooth=false){const pts=smooth?loop(points):points.map(p=>new T.Vector2(...p as [number,number]));const s=new T.Shape(pts);s.closePath();return s;}
function shaped(shape:T.Shape,project:(u:number,v:number)=>T.Vector3,outward:T.Vector3,levels=2){
 const source=new T.ShapeGeometry(shape,8),p=source.getAttribute('position'),idx=source.index!,positions:number[]=[],normals:number[]=[],eps=1e-4;
 const emit=(a:T.Vector2,b:T.Vector2,c:T.Vector2,depth=0)=>{
  if(depth<levels){const ab=a.clone().lerp(b,.5),bc=b.clone().lerp(c,.5),ca=c.clone().lerp(a,.5);emit(a,ab,ca,depth+1);emit(ab,b,bc,depth+1);emit(ca,bc,c,depth+1);emit(ab,bc,ca,depth+1);return;}
  const pa=project(a.x,a.y),pb=project(b.x,b.y),pc=project(c.x,c.y),order=pb.sub(pa).cross(pc.sub(pa)).dot(outward)<0?[a,c,b]:[a,b,c];
  for(const uv of order){const point=project(uv.x,uv.y),du=project(uv.x+eps,uv.y).sub(project(uv.x-eps,uv.y)),dv=project(uv.x,uv.y+eps).sub(project(uv.x,uv.y-eps)),normal=du.cross(dv).normalize();if(normal.dot(outward)<0)normal.negate();positions.push(...point.toArray());normals.push(...normal.toArray());}
 };
 for(let i=0;i<idx.count;i+=3)emit(new T.Vector2(p.getX(idx.getX(i)),p.getY(idx.getX(i))),new T.Vector2(p.getX(idx.getX(i+1)),p.getY(idx.getX(i+1))),new T.Vector2(p.getX(idx.getX(i+2)),p.getY(idx.getX(i+2))));
 source.dispose();const raw=new T.BufferGeometry();raw.setAttribute('position',new T.Float32BufferAttribute(positions,3));raw.setAttribute('normal',new T.Float32BufferAttribute(normals,3));const g=mergeVertices(raw,1e-6);raw.dispose();return g;
}
export function frontTopZ(y:number){return scalar([[0,1.075],[.64,1.075],[.89,1.18]],Math.abs(y),1);}
function faceOutline(rear=false){
 const rows=rear?design.rearRows:design.frontRows,min=rows[0][0],max=rows[rows.length-1][0],left=Array.from({length:49},(_,i)=>{const z=min+(max-min)*i/48;return[-scalar(rows,z,1),z];}),top=rear?[[scalar(rows,max,1),max]]:Array.from({length:49},(_,i)=>{const y=-.89+1.78*i/48;return[y,frontTopZ(y)];}),right=Array.from({length:49},(_,i)=>{const z=max-(max-min)*i/48;return[scalar(rows,z,1),z];});return [...left,...top.slice(rear?0:1),...right.slice(1)];
}
function mirroredHalf(source:T.BufferGeometry){
 const p=source.getAttribute('position'),n=source.getAttribute('normal'),idx=source.index!,positions:number[]=[],normals:number[]=[];
 for(let i=0;i<idx.count;i+=3){let poly=[0,1,2].map(j=>({p:new T.Vector3().fromBufferAttribute(p,idx.getX(i+j)),n:new T.Vector3().fromBufferAttribute(n,idx.getX(i+j))}));const clipped:typeof poly=[];
  for(let j=0;j<poly.length;j++){const a=poly[j],b=poly[(j+1)%poly.length],inside=a.p.y>=0;if(inside)clipped.push(a);if(inside!==(b.p.y>=0)){const t=-a.p.y/(b.p.y-a.p.y);clipped.push({p:a.p.clone().lerp(b.p,t).setY(0),n:a.n.clone().lerp(b.n,t).normalize()});}}poly=clipped;
  for(let j=1;j<poly.length-1;j++)for(const side of [1,-1])for(const v of side===1?[poly[0],poly[j],poly[j+1]]:[poly[0],poly[j+1],poly[j]]){positions.push(v.p.x,v.p.y*side,v.p.z);normals.push(v.n.x,v.n.y*side,v.n.z);}
 }
 source.dispose();const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(positions,3));g.setAttribute('normal',new T.Float32BufferAttribute(normals,3));const indexed=mergeVertices(g,1e-6);g.dispose();return indexed;
}
export function apertureBoundary(rear=false,side=1){return loop(rear?design.tailLight:design.headlight).map(p=>facePoint(p.y,p.x*side,rear));}
export function endFace(rear=false,openings=true){
 const shape=polygon(faceOutline(rear));
 if(openings)for(const side of [-1,1])shape.holes.push(new T.Path(loop(rear?design.tailLight:design.headlight).map(p=>new T.Vector2(p.x*side,p.y))));
 if(!rear)for(const pts of [design.grilleUpper,design.grilleLower,design.lowerOpening])shape.holes.push(new T.Path(loop(pts)));
 return mirroredHalf(shaped(shape,(y,z)=>facePoint(z,y,rear),new T.Vector3(rear?1:-1,0,0)));
}
export function apertureBacking(side:number,rear=false){return shaped(polygon(rear?design.tailLight:design.headlight,true),(y,z)=>facePoint(z,y*side,rear).add(new T.Vector3(rear?-.003:.003,0,0)),new T.Vector3(rear?1:-1,0,0),1);}
export function grilleBacking(points:number[][]){return mirroredHalf(shaped(polygon(points,true),(y,z)=>facePoint(z,y).add(new T.Vector3(.003,0,0)),new T.Vector3(-1,0,0)));}
const frontStart=-2.12,rearEnd=2.12;
const joinRows={front:[G.section(-1,-1),G.section(-1,1)],rear:[G.section(1,-1),G.section(1,1)]};
export function sectionPoint(x:number,h:number,side:number,rear=false){
 const join=rear?1:-1,edge=rear?rearEnd:frontStart,t=clamp((x-join)/(edge-join),0,1),hem=Math.max(.35,...axles.map(a=>Math.abs(x-a)<archRadius?.382+Math.sqrt(Math.max(0,archRadius**2-(x-a)**2)):.35));
 const joinRow=joinRows[rear?'rear':'front'][side<0?0:1],joinTop=joinRow[24],top=rear?scalar([[1,joinTop.z],[1.475,1.265],[1.90,1.29],[2.12,1.30]],x,1):scalar([[-2.12,1.18],[-1.90,1.205],[-1.37,1.265],[-1,joinTop.z]],x,1),z=hem+(top-hem)*h;
 const profile=rear?[[.35,.81],[.62,.90],[.95,.93],[1.10,.92],[top,.855]]:[[.35,.80],[.62,.89],[.95,.93],[1.10,.91],[top,.86]];
 const sorted=profile.sort((a,b)=>a[0]-b[0]);let y=scalar(sorted,z,1);const rearCrown=rear?.012*Math.exp(-Math.pow((x-axles[1])/.34,2))*Math.sin(Math.PI*h):0;y=Math.min(.93,y+rearCrown);
 const end=facePoint(rear?1.30*h+.39*(1-h):1.18*h+.39*(1-h),side*scalar(rear?design.rearRows:design.frontRows,rear?1.30*h+.39*(1-h):1.18*h+.39*(1-h),1),rear),p=new T.Vector3(x,side*y,z);
 const joinBlend=1-T.MathUtils.smoothstep(t,0,.28);p.lerp(joinRow[Math.round(h*24)],joinBlend);
 const endBlend=T.MathUtils.smoothstep(t,.70,1);p.y=T.MathUtils.lerp(p.y,end.y,endBlend);p.z=T.MathUtils.lerp(p.z,end.z,endBlend);return p;
}
export function sidePatch(side:number,rear=false){
 const start=rear?1:frontStart,end=rear?rearEnd:-1,xs=new Set(Array.from({length:65},(_,i)=>start+(end-start)*i/64));
 for(const ax of axles)for(let i=0;i<=40;i++){const x=ax+archRadius*Math.cos(i*Math.PI/40);if(x>=start&&x<=end)xs.add(x);}
 return G.surface([...xs].sort((a,b)=>a-b).map(x=>Array.from({length:25},(_,i)=>sectionPoint(x,i/24,side,rear))));
}
export function bonnetPoint(u:number,w:number){
 const x=-2.30+1.30*u,c=G.sample(curves.bonnetCentre,x),e=G.sample(curves.bonnetSide,x),p=new T.Vector3(x,w*e.y,T.MathUtils.lerp(c.z,e.z,Math.pow(Math.abs(w),2.4))),y=w*.64,z=scalar([[0,1.075],[.64,1.075]],Math.abs(y),1),nose=facePoint(z,y);
 p.z+=.020*Math.sin(Math.PI*u)*(1-Math.pow(Math.abs(w),1.8));return p.lerp(nose,1-T.MathUtils.smoothstep(u,0,.14));
}
export function bonnet(){return G.patch(48,24,(u,v)=>bonnetPoint(u,v*2-1));}
export function frontFender(side:number){return G.patch(48,18,(u,v)=>{
 const inner=bonnetPoint(u,side),x=frontStart+(-1-frontStart)*u,outer=sectionPoint(x,1,side),p=inner.clone().lerp(outer,v),front=facePoint(frontTopZ(.64+(.89-.64)*v),side*(.64+(.89-.64)*v)),a=facePoint(frontTopZ(.64),side*.64),b=facePoint(frontTopZ(.89),side*.89);
 p.add(front.sub(a.lerp(b,v)).multiplyScalar(Math.pow(1-u,3)));p.z+=.028*Math.sin(Math.PI*v)*Math.sin(Math.PI*u);return p;
});}

function clipForward(source:T.BufferGeometry,maxX:number){
 const p=source.getAttribute('position'),n=source.getAttribute('normal'),idx=source.index!,positions:number[]=[],normals:number[]=[];
 for(let i=0;i<idx.count;i+=3){const poly=[0,1,2].map(j=>({p:new T.Vector3().fromBufferAttribute(p,idx.getX(i+j)),n:new T.Vector3().fromBufferAttribute(n,idx.getX(i+j))})),clipped:typeof poly=[];
  for(let j=0;j<3;j++){const a=poly[j],b=poly[(j+1)%3],inside=a.p.x<=maxX;if(inside)clipped.push(a);if(inside!==(b.p.x<=maxX)){const t=(maxX-a.p.x)/(b.p.x-a.p.x);clipped.push({p:a.p.clone().lerp(b.p,t).setX(maxX),n:a.n.clone().lerp(b.n,t).normalize()});}}
  for(let j=1;j<clipped.length-1;j++)for(const v of [clipped[0],clipped[j],clipped[j+1]]){positions.push(...v.p.toArray());normals.push(...v.n.toArray());}
 }
 source.dispose();const raw=new T.BufferGeometry();raw.setAttribute('position',new T.Float32BufferAttribute(positions,3));raw.setAttribute('normal',new T.Float32BufferAttribute(normals,3));const g=mergeVertices(raw,1e-6);raw.dispose();return g;
}
export function preservedCabin(side:number,windows=false){return G.cabin(side,windows).map(g=>clipForward(g,1.30)).filter(g=>g.getAttribute('position').count>0);}
const beltCache=new Map<number,T.Vector3>(),oldBeltCache=new Map<number,T.Vector3>();
export function sideGlassY(x:number,z:number){
 if(!beltCache.has(x))beltCache.set(x,sectionPoint(clamp(x,1,2.12),1,1,true));if(!oldBeltCache.has(x))oldBeltCache.set(x,G.section(x,1)[24]);
 const belt=beltCache.get(x)!,old=oldBeltCache.get(x)!,roof=G.sample(curves.roofSide,x),t=clamp((z-belt.z)/(roof.z-belt.z),0,1),oldT=clamp((z-old.z)/(roof.z-old.z),0,1),own=T.MathUtils.lerp(belt.y,roof.y,t)+.008*Math.sin(t*Math.PI),previous=T.MathUtils.lerp(old.y,roof.y,oldT)+.008*Math.sin(oldT*Math.PI),base=T.MathUtils.lerp(previous,own,T.MathUtils.smoothstep(x,1.30,1.52)),edgeY=T.MathUtils.lerp(.815,.710,clamp((2.12-x)/.13,0,1));return T.MathUtils.lerp(base,edgeY,T.MathUtils.smoothstep(x,1.85,1.99));
}
export function sideFrame(side:number,glass=false){
 const outline=[[1.30,G.section(1.30,1)[24].z],[1.30,G.sample(curves.roofSide,1.30).z],[1.50,1.760],[1.99,1.705],[2.12,1.30],[1.90,1.29]],shape=polygon(glass?design.quarterGlass:outline,glass);
 if(!glass)shape.holes.push(new T.Path(loop(design.quarterGlass)));
 return shaped(shape,(x,z)=>new T.Vector3(x,side*sideGlassY(x,z),z),new T.Vector3(0,side,0));
}
export function rearFramePoint(z:number,y:number){
 const t=clamp((z-1.30)/.405,0,1),edgeX=T.MathUtils.lerp(2.12,1.99,t),width=T.MathUtils.lerp(.815,.710,t),centre=G.interpolate([1.30,1.50,1.705,1.745],[2.26,2.16,2.015,1.99],z),q=clamp((Math.abs(y)-.58)/(width-.58),0,1);
 return new T.Vector3(edgeX+(centre-edgeX)*Math.sqrt(Math.max(0,1-q*q)),y,z);
}
export function rearFrame(glass=false){
 const top=Array.from({length:33},(_,i)=>{const w=1-i/16;return[w*.710,1.745-.040*Math.pow(Math.abs(w),2.6)];});
 const shape=glass?polygon(design.rearGlass,true):polygon([[-.815,1.30],[.815,1.30],[.710,1.705],...top.slice(1),[-.815,1.30]]);
 if(!glass)shape.holes.push(new T.Path(loop(design.rearGlass)));
 return mirroredHalf(shaped(shape,(y,z)=>rearFramePoint(z,y),new T.Vector3(1,0,0)));
}

export function rearArchReturn(side:number){return G.patch(44,4,(u,v)=>{const angle=u*Math.PI,x=axles[1]+archRadius*Math.cos(angle),z=.382+archRadius*Math.sin(angle),outer=sectionPoint(x,0,side,true);return new T.Vector3(x,T.MathUtils.lerp(outer.y,side*.755,v),z+.016*v);});}

/** Detail faces use the same fascia projection as the aperture, not a flat billboard. */
export function detailFace(points:number[][],side=1,rear=false,offset=.006){return shaped(polygon(points,true),(y,z)=>facePoint(z,y*side,rear).add(new T.Vector3((rear?1:-1)*offset,0,0)),new T.Vector3(rear?1:-1,0,0),1);}
export function detailRim(points:number[][],side=1,rear=false,width=.015){
 const shape=polygon(points,true),centre=new T.Vector2(points.reduce((s,p)=>s+p[0],0)/points.length,points.reduce((s,p)=>s+p[1],0)/points.length),box=new T.Box2().setFromPoints(points.map(p=>new T.Vector2(...p as [number,number]))),size=box.getSize(new T.Vector2());
 const inner=points.map(p=>[centre.x+(p[0]-centre.x)*(1-width*2/size.x),centre.y+(p[1]-centre.y)*(1-width*2/size.y)]);shape.holes.push(new T.Path(loop(inner)));
 return shaped(shape,(y,z)=>facePoint(z,y*side,rear).add(new T.Vector3((rear?1:-1)*.007,0,0)),new T.Vector3(rear?1:-1,0,0),1);
}

export function sideDetail(points:number[][],side:number,surface:(x:number,z:number)=>number){return shaped(polygon(points,true),(x,z)=>new T.Vector3(x,side*(surface(x,z)+.003),z),new T.Vector3(0,side,0),3);}

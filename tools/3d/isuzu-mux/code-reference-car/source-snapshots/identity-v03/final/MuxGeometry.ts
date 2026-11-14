import * as T from 'three';
import { mergeVertices } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import { bodyStations, dimensions, axles, archRadius, curves, fasciaSections, shapeInfluences, headlightCurves, tailLightCurves, rearGlassCurves, rearSections, bumperCornerCurves, type Point } from './MuxReferenceData';

export const vec=(p:Point)=>new T.Vector3(...p);
export const curve=(points:readonly Point[],closed=false)=>new T.CatmullRomCurve3(points.map(vec),closed,'centripetal');
const clamp=T.MathUtils.clamp;
/** Monotone cubic interpolation retains nonzero slopes through stations without overshoot. */
export function interpolate(xs:readonly number[],ys:readonly number[],x:number){
  let i=0;while(i<xs.length-2&&x>xs[i+1])i++;
  const slope=(k:number)=>(ys[k+1]-ys[k])/(xs[k+1]-xs[k]);
  const tangent=(k:number)=>{if(k===0)return slope(0);if(k===xs.length-1)return slope(k-1);const l=slope(k-1),r=slope(k);if(l*r<=0)return 0;const h0=xs[k]-xs[k-1],h1=xs[k+1]-xs[k],w0=2*h1+h0,w1=h1+2*h0;return (w0+w1)/(w0/l+w1/r);};
  const h=xs[i+1]-xs[i],t=clamp((x-xs[i])/h,0,1),t2=t*t,t3=t2*t;
  return (2*t3-3*t2+1)*ys[i]+(t3-2*t2+t)*h*tangent(i)+(-2*t3+3*t2)*ys[i+1]+(t3-t2)*h*tangent(i+1);
}
export function sample(points:readonly (readonly number[])[],x:number){const xs=points.map(p=>p[0]);return new T.Vector3(x,interpolate(xs,points.map(p=>p[1]),x),interpolate(xs,points.map(p=>p[2]),x));}
export function surface(rows:T.Vector3[][]){
  const positions:number[]=[],indices:number[]=[],cols=rows[0].length;
  rows.forEach(row=>row.forEach(p=>positions.push(p.x,p.y,p.z)));
  for(let i=0;i<rows.length-1;i++)for(let j=0;j<cols-1;j++){const a=i*cols+j,b=a+cols;indices.push(a,b,a+1,a+1,b,b+1);}
  const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(positions,3));g.setIndex(indices);g.computeVertexNormals();return g;
}
export function patch(uCount:number,vCount:number,point:(u:number,v:number)=>T.Vector3){return surface(Array.from({length:uCount+1},(_,i)=>Array.from({length:vCount+1},(_,j)=>point(i/uCount,j/vCount))));}
const bands=[0,.025,.22,.50,.77,.94,1];
const stationX=bodyStations.map(s=>s[0]);
export function section(x:number,side:number){
  const t=(x+dimensions.length/2)/dimensions.length;
  const row=bodyStations[0].map((_,i)=>interpolate(stationX,bodyStations.map(s=>s[i]),t));
  const hem=Math.max(.35,...axles.map(ax=>Math.abs(x-ax)<archRadius?.382+Math.sqrt(archRadius**2-(x-ax)**2):.35));
  const shoulder=row[6]*dimensions.height,widths=[row[1],row[2],row[3],row[3],row[4],row[5],row[5]*.985];
  return Array.from({length:25},(_,i)=>{
    const h=i/24,z=hem+(shoulder-hem)*h;
    // Evaluate width at absolute body height: an arch must not drag the shoulder bands upward.
    const worldBand=clamp((z-.35)/(shoulder-.35),0,1),y=side*interpolate(bands,widths,worldBand)*dimensions.width/2;
    const corner=Math.pow(Math.max(0,1-Math.min(t,1-t)/.07),2)*.13*Math.pow(Math.abs(y)/.93,3);
    const point=new T.Vector3(x-Math.sign(x)*corner,y,z),rear=x>0;
    for(const influence of shapeInfluences){const weight=Math.exp(-.5*Math.pow((x-influence.x)/influence.sigma,2))*Math.pow(T.MathUtils.smoothstep(h,.30,1),2);point.z+=influence.upperLift*weight;point.y=side*Math.min(dimensions.width/2,Math.abs(point.y)+influence.lateralLift*weight);}
    const endWeight=Math.pow(Math.max(0,1-(dimensions.length/2-Math.abs(x))/.65),2);
    if(x>.95){const local=T.MathUtils.smoothstep(x,.95,1.30)*(1-T.MathUtils.smoothstep(x,1.90,2.30)),crown=Math.exp(-.5*Math.pow((x-axles[1])/.40,2));point.y=side*Math.min(dimensions.width/2,Math.abs(point.y)+local*(.027*crown*Math.sin(Math.PI*h)-.024*Math.pow(h,4)));}
    if(endWeight>0){const profile=rear?rearSections:fasciaSections.front,edgeZ=profile[0][0]+(profile[profile.length-1][0]-profile[0][0])*h,edgeProfile=sample(profile,edgeZ),edge=fasciaPoint(edgeZ,side*edgeProfile.y,rear);point.lerp(edge,endWeight);if(rear){const start=dimensions.length/2-.65,t=clamp((x-start)/.65,0,1);point.x=start+(edge.x-start)*t+(dimensions.length/2-edge.x)*t*Math.pow(1-t,2);}}
    return point;
  });
}
export function sideBody(side:number){
  // Dense samples at exact arch extrema stabilize the circular openings independently of regular stations.
  const xs=new Set(Array.from({length:161},(_,i)=>-dimensions.length/2+dimensions.length*i/160));
  for(const ax of axles)for(let i=0;i<=44;i++)xs.add(ax+archRadius*Math.cos(i*Math.PI/44));
  return surface([...xs].sort((a,b)=>a-b).map(x=>section(x,side)));
}
export function greenhouseY(x:number,z:number){
  const row=section(x,1),belt=row[row.length-1],roof=sample(curves.roofSide,x),t=clamp((z-belt.z)/(roof.z-belt.z),0,1);
  return T.MathUtils.lerp(belt.y,roof.y,t)+.008*Math.sin(t*Math.PI);
}
function outline(points:readonly Point[]){
  // Straight span plus small quadratic corner radii, not a global bevel or overshooting spline.
  const shape=new T.Shape();const p=points.map(v=>new T.Vector2(v[0],v[2]));
  const inset=.10;
  const first=p[0].clone().lerp(p[1],inset);shape.moveTo(first.x,first.y);
  for(let n=1;n<=p.length;n++){const i=n%p.length,prev=p[(i+p.length-1)%p.length],next=p[(i+1)%p.length],at=p[i],a=at.clone().lerp(prev,inset),b=at.clone().lerp(next,inset);shape.lineTo(a.x,a.y);shape.quadraticCurveTo(at.x,at.y,b.x,b.y);}
  shape.closePath();return shape;
}
export function cabin(side:number,windows=false){
  const holes=[curves.frontWindow,curves.rearWindow,curves.quarterWindow];
  const shapes=windows?holes.map(p=>outline(p as Point[])):[outline(curves.cabinOutline as Point[])];
  if(!windows)shapes[0].holes=holes.map(p=>{const h=outline(p as Point[]);return new T.Path(h.getPoints(10));});
  const geometries=shapes.map(shape=>{
    const source=new T.ShapeGeometry(shape,12),pos=source.getAttribute('position'),index=source.index!,vertices:number[]=[];
    for(let i=0;i<index.count;i+=3){const a=new T.Vector2(pos.getX(index.getX(i)),pos.getY(index.getX(i))),b=new T.Vector2(pos.getX(index.getX(i+1)),pos.getY(index.getX(i+1))),c=new T.Vector2(pos.getX(index.getX(i+2)),pos.getY(index.getX(i+2))),ab=a.clone().lerp(b,.5),bc=b.clone().lerp(c,.5),ca=c.clone().lerp(a,.5);
      for(const p of [a,ab,ca,ab,b,bc,ca,bc,c,ab,bc,ca])vertices.push(p.x,side*(greenhouseY(p.x,p.y)+(windows?.003:0)),p.y);
    }
    source.dispose();const raw=new T.BufferGeometry();raw.setAttribute('position',new T.Float32BufferAttribute(vertices,3));const g=mergeVertices(raw,1e-6);raw.dispose();g.computeVertexNormals();return g;
  });return geometries;
}
export function bonnetPoint(u:number,w:number){
  const points=curves.bonnetCentre,start=points[0][0],end=points[points.length-1][0],x=start+(end-start)*u;
  const centre=sample(points,x),edge=sample(curves.bonnetSide,x),p=new T.Vector3(x,w*edge.y,T.MathUtils.lerp(centre.z,edge.z,Math.pow(Math.abs(w),2.4)));
  const nose=fasciaPoint(fasciaSections.front[fasciaSections.front.length-1][0],p.y,false);
  const frontRoll=1-T.MathUtils.smoothstep(u,0,.16);return p.lerp(nose,frontRoll);
}
export function bonnet(){return patch(64,32,(u,v)=>bonnetPoint(u,v*2-1));}
export function fenderTop(side:number){return patch(80,20,(u,v)=>{
  const end=curves.bonnetCentre[curves.bonnetCentre.length-1][0],bodyX=-dimensions.length/2+(dimensions.length/2+end)*u;
  const inner=bonnetPoint(u,side),crown=sample(curves.fenderCrown,bodyX),row=section(bodyX,side),outer=row[row.length-1];
  const p=inner.clone().lerp(outer,v),lift=Math.max(0,crown.z-(inner.z+outer.z)*.5)*Math.sin(v*Math.PI);p.z+=lift;
  // Coons leading-edge correction is zero on both side boundaries, preserving the shared joins.
  const z=fasciaSections.front[fasciaSections.front.length-1][0],edge=fasciaPoint(z,p.y,false),a=fasciaPoint(z,inner.y,false),b=fasciaPoint(z,outer.y,false);
  const correction=edge.sub(a.lerp(b,v)).multiplyScalar(Math.pow(1-u,4));return p.add(correction);
});}
export function roof(){return patch(64,28,(u,v)=>{
  const first=curves.roofCentre[0][0],last=curves.roofCentre[curves.roofCentre.length-1][0],x=first+(last-first)*u,c=sample(curves.roofCentre as Point[],x),e=sample(curves.roofSide as Point[],x),w=v*2-1;return new T.Vector3(x,w*e.y,c.z-(c.z-e.z)*Math.pow(Math.abs(w),2.6));
});}
export function screen(rear=false){return patch(24,24,(u,v)=>{
  const pts=rear?curves.rearGlass:curves.windscreen,side=v*2-1;
  if(rear)return rearGlassPoint(1-u,v);
  const x=T.MathUtils.lerp(pts[0][0],pts[1][0],u),width=T.MathUtils.lerp(Math.abs(pts[0][1]),Math.abs(pts[1][1]),u),z=T.MathUtils.lerp(pts[0][2],pts[1][2],u);
  return new T.Vector3(x-.025*(1-side*side)*Math.sin(u*Math.PI),width*side,z+.024*(1-side*side));
});}
const frontProfile=fasciaSections.front,rearProfile=rearSections;
export function fasciaPoint(z:number,y:number,rear:boolean){
 if(rear){const zs=rearSections.map(r=>r[0]),width=interpolate(zs,rearSections.map(r=>r[1]),z),centre=interpolate(zs,rearSections.map(r=>r[2]),z),depth=interpolate(zs,rearSections.map(r=>r[3]),z),w=clamp(Math.abs(y)/width,0,1),corner=depth*(1-Math.cos(w*Math.PI/2));
  const plate=-.035*Math.exp(-Math.pow((z-.98)/.20,4))*Math.pow(Math.max(0,1-w*w),3),hatch=-.008*Math.exp(-Math.pow((z-.80)/.16,2))*(1-w*w);
  const p=new T.Vector3(centre-corner+plate+hatch,y,z+.012*w*w),cornerWeight=Math.exp(-Math.pow((z-.61)/.12,2))*T.MathUtils.smoothstep(Math.abs(y),.55,.78);if(cornerWeight>0){const c=sample(bumperCornerCurves.right.map(p=>[p[1],p[0],p[2]]),Math.abs(y));p.x=T.MathUtils.lerp(p.x,c.y,cornerWeight);}
  return p;
 }
 const p=sample(frontProfile,z),w=y/p.y;return new T.Vector3(p.z+(.14+.16*T.MathUtils.smoothstep(z,.80,1.04))*Math.pow(Math.abs(w),3),y,z+.025*Math.pow(Math.abs(w),3));
}
export function fascia(rear=false){
 const g=patch(36,42,(u,v)=>{const profile=rear?rearProfile:frontProfile,z=profile[0][0]+u*(profile[profile.length-1][0]-profile[0][0]),p=sample(profile,z);return fasciaPoint(z,p.y*(v*2-1),rear);});
 // Cut actual front/rear skin triangles behind the curved apertures; the housing ring covers the sampling edge.
 const p=g.getAttribute('position'),index=g.index!,keep:number[]=[];
 for(let i=0;i<index.count;i+=3){const ids=[index.getX(i),index.getX(i+1),index.getX(i+2)],y=ids.reduce((n,k)=>n+p.getY(k),0)/3,z=ids.reduce((n,k)=>n+p.getZ(k),0)/3;
  if(!insideLampYZ(Math.abs(y),z,rear))keep.push(...ids);
 }
 g.setIndex(keep);g.computeVertexNormals();return g;
}
export function fasciaEnvelope(points:readonly Point[],side=1,rear=false){
 return patch(12,12,(u,v)=>{const a=vec(points[0]).lerp(vec(points[1]),v),b=vec(points[3]).lerp(vec(points[2]),v),p=a.lerp(b,u),q=fasciaPoint(p.z,p.y*side,rear);q.x+=rear?.007:-.007;return q;});
}
export function envelope(points:readonly Point[],side=1){
  const pts=points.map(p=>new T.Vector3(p[0],p[1]*side,p[2])),centre=pts.reduce((a,p)=>a.add(p),new T.Vector3()).multiplyScalar(1/pts.length);
  const g=new T.BufferGeometry(),positions:number[]=[],indices:number[]=[];positions.push(...centre.toArray());pts.forEach(p=>positions.push(...p.toArray()));for(let i=0;i<pts.length;i++)indices.push(0,i+1,(i+1)%pts.length+1);g.setAttribute('position',new T.Float32BufferAttribute(positions,3));g.setIndex(indices);g.computeVertexNormals();return g;
}

/** Stock capsule poles collapse to zero-area faces; discard only those construction faces. */
export function pruneCollapsedTriangles(g:T.BufferGeometry){
 const p=g.getAttribute('position'),index=g.index,keep:number[]=[],a=new T.Vector3(),b=new T.Vector3(),c=new T.Vector3();
 for(let i=0;i<(index?.count??p.count);i+=3){const ids=[0,1,2].map(n=>index?index.getX(i+n):i+n);a.fromBufferAttribute(p,ids[0]);b.fromBufferAttribute(p,ids[1]);c.fromBufferAttribute(p,ids[2]);if(b.sub(a).cross(c.sub(a)).lengthSq()>=1e-20)keep.push(...ids);}
 g.setIndex(keep);return g;
}

function coons(top:T.Curve<T.Vector3>,bottom:T.Curve<T.Vector3>,inner:T.Curve<T.Vector3>,outer:T.Curve<T.Vector3>,u:number,v:number){
 const a=top.getPoint(u),b=bottom.getPoint(u),c=inner.getPoint(v),d=outer.getPoint(v);
 const corners=top.getPoint(0).lerp(top.getPoint(1),u).lerp(bottom.getPoint(0).lerp(bottom.getPoint(1),u),v);
 return a.multiplyScalar(1-v).add(b.multiplyScalar(v)).add(c.multiplyScalar(1-u)).add(d.multiplyScalar(u)).sub(corners);
}
const lampNetworks={
 front:{top:curve([...headlightCurves.H2,...headlightCurves.H1.slice(1)]),bottom:curve(headlightCurves.H3),inner:curve(headlightCurves.H5),outer:curve(headlightCurves.H4)},
 rear:{top:curve(tailLightCurves.upper),bottom:curve(tailLightCurves.lower),inner:curve(tailLightCurves.inner),outer:curve(tailLightCurves.outer)}
};
const frontSpine=curve(headlightCurves.H6),frontCrown=curve(headlightCurves.H7);
export function lampPoint(u:number,v:number,side=1,rear=false){
 const n=rear?lampNetworks.rear:lampNetworks.front,p=coons(n.top,n.bottom,n.inner,n.outer,u,v),blend=Math.sin(Math.PI*u)*Math.sin(Math.PI*v);
 if(rear)p.x+=.014*blend;
 else{const along=frontSpine.getPoint(v).x-coons(n.top,n.bottom,n.inner,n.outer,.5,v).x,across=frontCrown.getPoint(u).x-coons(n.top,n.bottom,n.inner,n.outer,u,.5).x;p.x+=clamp((along*Math.sin(Math.PI*u)+across*Math.sin(Math.PI*v))*.5,-.016,.008);}
 p.y*=side;return p;
}
export function lampSurface(side:number,rear=false){return patch(24,12,(u,v)=>lampPoint(u,v,side,rear));}
function lampBoundary(rear=false){const n=rear?lampNetworks.rear:lampNetworks.front;return [...n.top.getPoints(32),...n.outer.getPoints(16).slice(1),...n.bottom.getPoints(32).reverse().slice(1),...n.inner.getPoints(16).reverse().slice(1)];}
const frontBoundary=lampBoundary(),rearBoundary=lampBoundary(true);
function insideLampYZ(y:number,z:number,rear=false){const points=rear?rearBoundary:frontBoundary;let inside=false;for(let i=0,j=points.length-1;i<points.length;j=i++){const a=points[i],b=points[j];if((a.z>z)!==(b.z>z)&&y<(b.y-a.y)*(z-a.z)/(b.z-a.z)+a.y)inside=!inside;}return inside;}
export function lampHousing(side:number,rear=false){
 const path=rear?rearBoundary:frontBoundary,centre=path.reduce((a,b)=>a.add(b),new T.Vector3()).multiplyScalar(1/path.length);
 return surface([path.map(p=>new T.Vector3(p.x+(rear?-.010:.010),p.y*side,p.z)),path.map(p=>new T.Vector3(p.x+(rear?-.025:.025),Math.min(dimensions.width/2,centre.y+(p.y-centre.y)*1.055)*side,centre.z+(p.z-centre.z)*1.07))]);
}
export function lampSignature(side:number,rear=false){const n=rear?lampNetworks.rear:lampNetworks.front;return patch(28,2,(u,v)=>{const p=n.top.getPoint(u);p.z-=.009+v*.012;p.x+=rear?.007:-.007;p.y*=side;return p;});}
const glassTop=curve(rearGlassCurves.top),glassBottom=curve(rearGlassCurves.bottom),glassSide=curve(rearGlassCurves.side),glassOther=curve(rearGlassCurves.side.map(p=>[p[0],-p[1],p[2]]));
export function rearGlassPoint(u:number,v:number){return coons(glassTop,glassBottom,glassOther,glassSide,v,u).add(new T.Vector3(.012*Math.sin(Math.PI*u)*Math.sin(Math.PI*v),0,0));}
export function rearLower(){return patch(8,32,(u,v)=>{const z=.425+u*.175,profile=sample(rearSections,z),p=fasciaPoint(z,profile.y*(v*2-1)*.94,true);p.x=Math.min(dimensions.length/2,p.x+.006);return p;});}
export function rearRoofLip(){return patch(3,28,(u,v)=>{const p=glassTop.getPoint(v);p.x+=.015+u*.10;p.z+=.026-Math.sin(u*Math.PI/2)*.022;return p;});}
export function bumperCorner(side:number){return curve(side<0?bumperCornerCurves.left:bumperCornerCurves.right);}

export function rearArchReturn(side:number){return patch(44,4,(u,v)=>{const angle=u*Math.PI,x=axles[1]+archRadius*Math.cos(angle),z=.382+archRadius*Math.sin(angle),outer=section(x,side)[0];return new T.Vector3(x,outer.y*(1-v)+side*.755*v,z+.016*v);});}

export function headlightReflector(side:number){return patch(20,3,(u,v)=>{const theta=u*Math.PI*2,r=.72+.28*v,p=lampPoint(.57+.11*r*Math.cos(theta),.53+.28*r*Math.sin(theta),side);p.x-=.005;return p;});}

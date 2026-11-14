import * as T from 'three';
import { bodyStations, dimensions, axles, archRadius, curves, type Point } from './MuxReferenceData';

export const vec=(p:Point)=>new T.Vector3(...p);
export const curve=(points:readonly Point[],closed=false)=>new T.CatmullRomCurve3(points.map(vec),closed,'centripetal');
const clamp=T.MathUtils.clamp;
export function sample(points:readonly Point[],x:number){
  let i=0;while(i<points.length-2&&x>points[i+1][0])i++;
  const a=points[i],b=points[i+1],t=clamp((x-a[0])/(b[0]-a[0]),0,1),s=t*t*(3-2*t);
  return new T.Vector3(x,T.MathUtils.lerp(a[1],b[1],s),T.MathUtils.lerp(a[2],b[2],s));
}
export function surface(rows:T.Vector3[][]){
  const positions:number[]=[],indices:number[]=[],cols=rows[0].length;
  rows.forEach(row=>row.forEach(p=>positions.push(p.x,p.y,p.z)));
  for(let i=0;i<rows.length-1;i++)for(let j=0;j<cols-1;j++){const a=i*cols+j,b=a+cols;indices.push(a,b,a+1,a+1,b,b+1);}
  const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(positions,3));g.setIndex(indices);g.computeVertexNormals();return g;
}
export function patch(uCount:number,vCount:number,point:(u:number,v:number)=>T.Vector3){return surface(Array.from({length:uCount+1},(_,i)=>Array.from({length:vCount+1},(_,j)=>point(i/uCount,j/vCount))));}
const bands=[0,.025,.22,.50,.77,.94,1];
export function section(x:number,side:number){
  const t=(x+dimensions.length/2)/dimensions.length;
  let k=0;while(k<bodyStations.length-2&&t>bodyStations[k+1][0])k++;
  const a=bodyStations[k],b=bodyStations[k+1],u=clamp((t-a[0])/(b[0]-a[0]),0,1),s=u*u*(3-2*u);
  const row=a.map((v,i)=>T.MathUtils.lerp(v,b[i],s));
  const hem=Math.max(.35,...axles.map(ax=>Math.abs(x-ax)<archRadius?.382+Math.sqrt(archRadius**2-(x-ax)**2):.35));
  const shoulder=row[6]*dimensions.height,span=shoulder-hem;
  const widths=[row[1],row[2],row[3],row[3],row[4],row[5],row[5]*.985];
  return bands.map((h,i)=>{
    const y=side*widths[i]*dimensions.width/2;
    const corner=Math.pow(Math.max(0,1-Math.min(t,1-t)/.07),2)*.13*Math.pow(Math.abs(y)/.93,3);
    return new T.Vector3(x-Math.sign(x)*corner,y,hem+span*h);
  });
}
export function sideBody(side:number){
  // Dense samples at exact arch extrema stabilize the circular openings independently of regular stations.
  const xs=new Set(Array.from({length:161},(_,i)=>-dimensions.length/2+dimensions.length*i/160));
  for(const ax of axles)for(let i=0;i<=44;i++)xs.add(ax+archRadius*Math.cos(i*Math.PI/44));
  return surface([...xs].sort((a,b)=>a-b).map(x=>section(x,side)));
}
export function greenhouseY(x:number,z:number){
  const belt=.845+.014*Math.exp(-Math.pow((x-1.45)/.65,2));
  const top=.715+.020*Math.exp(-Math.pow((x-1.0)/1.0,2));
  const t=clamp((z-1.25)/.51,0,1);return T.MathUtils.lerp(belt,top,t)+.012*Math.sin(t*Math.PI);
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
  const geometries=shapes.map(shape=>{const g=new T.ShapeGeometry(shape,12),pos=g.getAttribute('position');for(let i=0;i<pos.count;i++){const x=pos.getX(i),z=pos.getY(i);pos.setXYZ(i,x,side*(greenhouseY(x,z)+(windows?.003:0)),z);}g.computeVertexNormals();return g;});return geometries;
}
export function bonnet(){return patch(64,32,(u,v)=>{
  const x=curves.bonnetCentre[0][0]+(curves.bonnetCentre[curves.bonnetCentre.length-1][0]-curves.bonnetCentre[0][0])*u;
  const centre=sample(curves.bonnetCentre as Point[],x),edge=sample(curves.bonnetSide as Point[],x),w=v*2-1;
  return new T.Vector3(x,w*edge.y,T.MathUtils.lerp(centre.z,edge.z,Math.pow(Math.abs(w),2.4)));
});}
export function fenderTop(side:number){return patch(80,16,(u,v)=>{
  const x=-2.30+1.47*u,inner=sample(curves.bonnetSide as Point[],x),crown=sample(curves.fenderCrown as Point[],x),outer=section(x,side)[6];
  const points=[new T.Vector3(x,side*inner.y,inner.z),new T.Vector3(x,side*crown.y,crown.z),outer];
  const c=new T.CatmullRomCurve3(points,false,'centripetal');const p=c.getPoint(v);p.y=T.MathUtils.clamp(p.y,-dimensions.width/2,dimensions.width/2);return p;
});}
export function roof(){return patch(64,28,(u,v)=>{
  const x=-.40+2.39*u,c=sample(curves.roofCentre as Point[],x),e=sample(curves.roofSide as Point[],x),w=v*2-1;return new T.Vector3(x,w*e.y,c.z-(c.z-e.z)*Math.pow(Math.abs(w),2.6));
});}
export function screen(rear=false){return patch(24,24,(u,v)=>{
  const pts=rear?curves.rearGlass:curves.windscreen,side=v*2-1;
  const x=T.MathUtils.lerp(pts[0][0],pts[1][0],u),width=T.MathUtils.lerp(Math.abs(pts[0][1]),Math.abs(pts[1][1]),u),z=T.MathUtils.lerp(pts[0][2],pts[1][2],u);
  return new T.Vector3(x+(rear?.025:-.025)*(1-side*side)*Math.sin(u*Math.PI),width*side,z+.024*(1-side*side));
});}
const frontProfile:Point[]=[[.39,.78,-2.30],[.48,.84,-2.4125],[.66,.88,-2.39],[.80,.89,-2.34],[.95,.89,-2.32],[1.04,.89,-2.30]];
const rearProfile:Point[]=[[.39,.82,2.32],[.48,.86,2.4125],[.67,.86,2.37],[.92,.85,2.33],[1.15,.85,2.30],[1.29,.79,2.255]];
function fasciaPoint(z:number,y:number,rear:boolean){
 const p=sample(rear?rearProfile:frontProfile,z),w=y/p.y,corner=.14*Math.pow(Math.abs(w),3),recess=rear?-.045*Math.exp(-Math.pow((z-.94)/.14,2))*Math.pow(Math.max(0,1-w*w),3):0;
 return new T.Vector3(p.z+(rear?-corner:corner)+recess,y,z+(rear?.035:.07)*Math.pow(Math.abs(w),3));
}
export function fascia(rear=false){return patch(36,42,(u,v)=>{const z=.39+u*(rear?.90:.65),p=sample(rear?rearProfile:frontProfile,z);return fasciaPoint(z,p.y*(v*2-1),rear);});}
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

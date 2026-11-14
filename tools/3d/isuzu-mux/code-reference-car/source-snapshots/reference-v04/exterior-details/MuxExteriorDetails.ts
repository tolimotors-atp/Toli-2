import * as T from 'three';
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js';
import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js';
import fontData from 'three/examples/fonts/helvetiker_bold.typeface.json?raw';
import * as G from './MuxGeometry';
import * as P from './MuxReferencePatches';

// Authored from the silver front/side/rear-quarter references; dimensions are visual estimates.
export const exteriorDesign={
 mirror:{housingWidth:.240,housingHeight:.150,housingDepth:.190,mountX:-.805,mountZ:1.295,outerY:1.10},
 frontDoor:[[-1.00,1.220],[-.87,.430],[-.80,.412],[.23,.410],[.30,.480],[.31,1.755],[-.34,1.750],[-.56,1.705]],
 rearDoor:[[.36,1.755],[.36,.425],[.93,.420],[1.04,.490],[1.08,.650],[1.15,.890],[1.23,1.220],[1.28,1.710],[1.10,1.755]],
 handles:[{name:'front',x:.170,z:1.175,length:.200},{name:'rear',x:1.050,z:1.195,length:.200}],
 plates:{text:'TOLI MOTORS',width:.460,height:.115,thickness:.006,frontZ:.480,rearZ:1.005},
 gapWidth:.003
};
const sectionCache=new Map<number,T.Vector3[]>();
export function sideSurface(x:number,z:number){
 if(!sectionCache.has(x))sectionCache.set(x,x>=-1&&x<=1?G.section(x,1):Array.from({length:25},(_,i)=>P.sectionPoint(x,i/24,1,x>0)));
 const row=sectionCache.get(x)!,top=row[24];
 if(z>top.z)return x>=1.30?P.sideGlassY(x,z):G.greenhouseY(x,z);
 const height=T.MathUtils.clamp(z,row[0].z,top.z);let i=0;while(i<row.length-2&&height>row[i+1].z)i++;return T.MathUtils.lerp(row[i].y,row[i+1].y,(height-row[i].z)/(row[i+1].z-row[i].z));
}
function roundedOutline(points:number[][],round=.075){
 const path=new T.Shape(),p=points.map(v=>new T.Vector2(v[0],v[1])),start=p[0].clone().lerp(p[1],round);path.moveTo(start.x,start.y);
 for(let n=1;n<=p.length;n++){const i=n%p.length,at=p[i],a=at.clone().lerp(p[(i+p.length-1)%p.length],round),b=at.clone().lerp(p[(i+1)%p.length],round);path.lineTo(a.x,a.y);path.quadraticCurveTo(at.x,at.y,b.x,b.y);}path.closePath();return path;
}
function doorGap(points:number[][]){
 const outline=roundedOutline(points,.035);return G.patch(96,1,(u,v)=>{const p=outline.getPoint(u),t=outline.getTangent(u),w=(v-.5)*exteriorDesign.gapWidth,x=p.x-t.y*w,z=p.y+t.x*w;return new T.Vector3(x,sideSurface(x,z)+.0025,z);});
}
function handle(x:number,z:number,length:number){return G.patch(12,8,(u,v)=>{const a=v*Math.PI*2,shape=.40+.60*Math.sin(u*Math.PI),xx=x+(u-.5)*length;return new T.Vector3(xx,sideSurface(xx,z)+.005+.018*Math.sin(u*Math.PI)+.006*shape*Math.cos(a),z+.010*shape*Math.sin(a));});}
const mirrorSections=[[.860,-.815,1.315,0,0],[.883,-.825,1.320,.072,.060],[.940,-.820,1.330,.095,.075],[1.030,-.810,1.333,.091,.073],[1.075,-.800,1.335,.061,.052],[1.100,-.805,1.335,0,0]];
function mirrorSample(y:number,column:number){return G.interpolate(mirrorSections.map(p=>p[0]),mirrorSections.map(p=>p[column]),y);}
function mirrorShell(upper:boolean){return G.patch(14,16,(u,v)=>{const y=.860+.240*u,angle=(upper?0:Math.PI)+Math.PI*v,c=Math.cos(angle),s=Math.sin(angle),signed=(n:number)=>Math.sign(n)*Math.pow(Math.abs(n),.72);return new T.Vector3(mirrorSample(y,1)+mirrorSample(y,3)*signed(c),y,mirrorSample(y,2)+mirrorSample(y,4)*signed(s));});}
function mirrorGlass(){
 const shape=roundedOutline([[.899,1.280],[1.052,1.285],[1.071,1.310],[1.059,1.376],[.917,1.386],[.895,1.360]],.14),g=new T.ShapeGeometry(shape,5),p=g.getAttribute('position');
 for(let i=0;i<p.count;i++){const y=p.getX(i),z=p.getY(i);p.setXYZ(i,mirrorSample(y,1)+mirrorSample(y,3)+.0015,y,z);}g.computeVertexNormals();return g;
}
function mirrorBase(){const g=new T.CapsuleGeometry(.025,.095,3,8);g.rotateZ(Math.PI/2);g.translate(-.805,.860,1.285);return g;}
function mirrorStalk(){const path=G.curve([[-.81,.835,1.275],[-.81,.876,1.282],[-.82,.905,1.303]]);return new T.TubeGeometry(path,6,.019,6,false);}
function plateText(){
 const font=new FontLoader().parse(JSON.parse(fontData)),g=new TextGeometry(exteriorDesign.plates.text,{font,size:1,depth:.025,curveSegments:4,bevelEnabled:false});g.computeBoundingBox();const b=g.boundingBox!,size=b.getSize(new T.Vector3()),scale=Math.min(.405/size.x,.066/size.y);g.translate(-(b.min.x+b.max.x)/2,-(b.min.y+b.max.y)/2,0);g.scale(scale,scale,scale);return g;
}
export function createExteriorDetails(materials:Record<string,T.Material>){
 const root=new T.Group();root.name='exterior-details';const mirrors=new T.Group(),doors=new T.Group(),handles=new T.Group(),plates=new T.Group();mirrors.name='mirrors';doors.name='doors';handles.name='handles';plates.name='number-plates';
 const add=(parent:T.Group,name:string,g:T.BufferGeometry,mat:T.Material)=>{const m=new T.Mesh(g,mat);m.name=name;parent.add(m);return m;};
 const shellUpper=mirrorShell(true),shellLower=mirrorShell(false),glass=mirrorGlass(),base=mirrorBase(),stalk=mirrorStalk();
 const frontGap=doorGap(exteriorDesign.frontDoor),rearGap=doorGap(exteriorDesign.rearDoor),handleGeometries=exteriorDesign.handles.map(h=>handle(h.x,h.z,h.length));
 for(const side of [-1,1]){const label=side<0?'left':'right',mirror=new T.Group(),doorSide=new T.Group(),handleSide=new T.Group();mirror.name='mirror-'+label;doorSide.name='door-definitions-'+label;handleSide.name='handles-'+label;for(const group of [mirror,doorSide,handleSide])group.scale.y=side;
  add(mirror,'mirror-mounting-base',base,materials.rubber);add(mirror,'mirror-support',stalk,materials.rubber);add(mirror,'mirror-outer-shell',shellUpper,materials.alloy);add(mirror,'mirror-lower-shell',shellLower,materials.dark);add(mirror,'mirror-glass',glass,materials.mirror);
  add(doorSide,'front-'+label+'-door-cut',frontGap,materials.rubber);add(doorSide,'rear-'+label+'-door-cut',rearGap,materials.rubber);
  exteriorDesign.handles.forEach((h,i)=>add(handleSide,h.name+'-'+label+'-door-handle',handleGeometries[i],materials.alloy));mirrors.add(mirror);doors.add(doorSide);handles.add(handleSide);
 }
 const textGeometry=plateText(),plateGeometry=new T.BoxGeometry(.460,.115,.006),mountGeometry=new T.BoxGeometry(.045,.018,.028);
 for(const rear of [false,true]){const plate=new T.Group(),z=rear?exteriorDesign.plates.rearZ:exteriorDesign.plates.frontZ,sign=rear?1:-1;
  const surface=Array.from({length:21},(_,i)=>P.facePoint(z-.0575+.115*i/20,0,rear).x),x=(rear?Math.max(...surface):Math.min(...surface))+sign*.009;
  plate.name=rear?'rear-number-plate':'front-number-plate';plate.userData.text=exteriorDesign.plates.text;plate.position.set(x,0,z);plate.setRotationFromMatrix(new T.Matrix4().makeBasis(new T.Vector3(0,sign,0),new T.Vector3(0,0,1),new T.Vector3(sign,0,0)));
  add(plate,'plate-backing',plateGeometry,materials.plate);const text=add(plate,'TOLI MOTORS',textGeometry,materials.rubber);text.position.z=.0035;
  for(const y of [-.155,.155]){const mount=add(plate,'plate-mount',mountGeometry,materials.dark);mount.position.set(y,0,-.016);}plates.add(plate);
 }
 root.add(mirrors,doors,handles,plates);return {root,mirrors,doors,handles,plates};
}

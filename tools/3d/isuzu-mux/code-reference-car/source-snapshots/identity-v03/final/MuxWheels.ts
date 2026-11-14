import * as T from 'three';
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import { axles, dimensions, track } from './MuxReferenceData';
export function wheels(materials:{rubber:T.Material;alloy:T.Material;dark:T.Material;clay:T.Material}){
  const root=new T.Group();root.name='wheels';
  const profile=new T.CatmullRomCurve3([[.245,-.120,0],[.32,-.123,0],[.368,-.10,0],[.382,-.06,0],[.382,.06,0],[.368,.10,0],[.32,.123,0],[.245,.120,0],[.245,-.120,0]].map(p=>new T.Vector3(...p as [number,number,number])));
  const tire=new T.LatheGeometry(profile.getPoints(44).map(p=>new T.Vector2(Math.min(.382,p.x),p.y)),80);
  const rim=new T.LatheGeometry([new T.Vector2(.205,-.105),new T.Vector2(.251,-.105),new T.Vector2(.259,-.092),new T.Vector2(.251,.105),new T.Vector2(.205,.105)],64);
  const disc=new T.CylinderGeometry(.194,.194,.016,48),hub=new T.CylinderGeometry(.061,.061,.04,32);
  const blade=new T.Shape();blade.moveTo(.046,-.018);blade.bezierCurveTo(.11,-.022,.19,-.012,.246,-.002);blade.lineTo(.246,.020);blade.bezierCurveTo(.17,.010,.09,.004,.046,.016);blade.closePath();
  const spoke=new T.ExtrudeGeometry(blade,{depth:.012,bevelEnabled:false,curveSegments:10});spoke.rotateX(Math.PI/2);
  const copies:T.BufferGeometry[]=[];for(let n=0;n<10;n++){const g=spoke.clone();g.rotateY(n*Math.PI/5);copies.push(g);}const spokes=mergeGeometries(copies)!;copies.forEach(g=>g.dispose());spoke.dispose();
  for(const x of axles)for(const side of [-1,1]){
    const group=new T.Group();group.position.set(x,side*track/2,dimensions.tireDiameter/2);group.name=`wheel-${x<0?'front':'rear'}-${side>0?'left':'right'}`;
    const add=(g:T.BufferGeometry,m:T.Material,y=0)=>{const o=new T.Mesh(g,m);o.position.y=y;group.add(o);};
    add(tire,materials.rubber);add(rim,materials.alloy);add(disc,materials.dark,side*.074);add(spokes,materials.alloy,side*.113);add(hub,materials.alloy,side*.114);
    const caliper=new T.Mesh(new T.CapsuleGeometry(.029,.10,4,8),materials.dark);caliper.rotation.x=Math.PI/2;caliper.position.set(-.135,side*.071,.04);group.add(caliper);root.add(group);
  }
  return root;
}

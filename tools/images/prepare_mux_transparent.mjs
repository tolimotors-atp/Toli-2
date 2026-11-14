// Reproducible alpha masks preserve the supplied vehicle pixels; no generated car artwork.
import sharp from 'sharp';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const output=path.join(root,'src/assets/vehicles/isuzu-mux');
const evidence=path.join(root,'docs/mux-transparent');
await mkdir(output,{recursive:true});await mkdir(evidence,{recursive:true});
const records=[];
for(const [view,name] of [['front','Screenshot 2026-11-08 213542.png'],['rear','Screenshot 2026-11-08 213451.png']]){
 const source=await readFile(path.join(root,'../Isuzu MU-X',name));
 const maskFile=path.join(root,`tools/images/mux-masks/${view}.svg`);
 const {width,height}=await sharp(source).metadata();
 const mask=await sharp(maskFile,{density:288}).resize(width,height).blur(.35).png().toBuffer();
 const rgba=await sharp(source).ensureAlpha().composite([{input:mask,blend:'dest-in'}]).png().toBuffer();
 const trimmed=await sharp(rgba).trim({threshold:1}).png().toBuffer();
 const fit=await sharp(trimmed).resize({width:1008,height:540,fit:'inside'}).png().toBuffer();
 const size=await sharp(fit).metadata();
 const master=await sharp({create:{width:1100,height:660,channels:4,background:'#00000000'}}).composite([{input:fit,left:Math.round((1100-size.width)/2),top:Math.round((660-size.height)/2)}]).png().toBuffer();
 await writeFile(path.join(evidence,`isuzu-mux-${view}-master.png`),master);
 for(const w of [640,1100]){
  const file=`isuzu-mux-${view}-3q-transparent${w===640?'-640':''}.webp`;
  const bytes=await sharp(master).resize(w,Math.round(w*.6)).webp({quality:92,alphaQuality:100,effort:6}).toBuffer();
  await writeFile(path.join(output,file),bytes);
  const {data,info}=await sharp(bytes).raw().toBuffer({resolveWithObject:true});
  assert.equal(info.channels,4);let transparent=0,opaque=0;for(let i=3;i<data.length;i+=4){if(data[i]===0)transparent++;if(data[i]===255)opaque++;}
  assert(transparent>info.width*info.height*.35);assert(opaque>info.width*info.height*.15);
  for(const [x,y] of [[0,0],[info.width-1,0],[0,info.height-1],[info.width-1,info.height-1]])assert.equal(data[(y*info.width+x)*4+3],0);
  records.push({view,source:name,sourceSha256:createHash('sha256').update(source).digest('hex'),sourceDimensions:[width,height],file:`src/assets/vehicles/isuzu-mux/${file}`,width:info.width,height:info.height,bytes:bytes.length,transparentPixels:transparent,opaquePixels:opaque,method:'Manually traced alpha mask; original vehicle RGB retained; proportional fit and WebP encoding only.'});
 }
}
await writeFile(path.join(evidence,'assets.json'),JSON.stringify(records,null,2)+'\n');
console.log(records);

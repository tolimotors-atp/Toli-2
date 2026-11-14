// Keep the supplied car pixels; only the authored alpha silhouette changes the background.
import sharp from 'sharp';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const dir=path.join(root,'src/assets/vehicles/isuzu-mux'),docs=path.join(root,'docs/red-mux');
await mkdir(docs,{recursive:true});
const source=await readFile(path.join(dir,'isuzu-mux-red-front-3q.png'));
const mask=await sharp(path.join(root,'tools/images/mux-masks/red-front.svg'),{density:288}).resize(1536,1024).blur(.35).png().toBuffer();
const rgb=await sharp(source).removeAlpha().png().toBuffer();
const opaque=await sharp(rgb).ensureAlpha().png().toBuffer();
const masked=await sharp(opaque).composite([{input:mask,blend:'dest-in'}]).png().toBuffer();
const cutout=await sharp(masked).trim({threshold:1}).png().toBuffer();
const fit=await sharp(cutout).resize({width:1008,height:584,fit:'inside'}).png().toBuffer();
const size=await sharp(fit).metadata();
const master=await sharp({create:{width:1100,height:660,channels:4,background:'#00000000'}}).composite([{input:fit,left:Math.round((1100-size.width)/2),top:Math.round((660-size.height)/2)}]).png().toBuffer();
await writeFile(path.join(docs,'isuzu-mux-red-cutout-master.png'),master);
const records=[];
for(const width of [640,1100]){
 const file=`isuzu-mux-red-front-3q${width===640?'-640':''}.webp`;
 const bytes=await sharp(master).resize(width,Math.round(width*.6)).webp({quality:92,alphaQuality:100,effort:6}).toBuffer();
 const {data,info}=await sharp(bytes).raw().toBuffer({resolveWithObject:true});
 assert.equal(info.channels,4);let transparent=0,opaque=0;for(let i=3;i<data.length;i+=4){if(data[i]===0)transparent++;if(data[i]===255)opaque++;}
 assert(transparent>info.width*info.height*.3);assert(opaque>info.width*info.height*.2);
 for(const [x,y] of [[0,0],[info.width-1,0],[0,info.height-1],[info.width-1,info.height-1]])assert.equal(data[(y*info.width+x)*4+3],0);
 await writeFile(path.join(dir,file),bytes);
 records.push({file:`src/assets/vehicles/isuzu-mux/${file}`,width:info.width,height:info.height,bytes:bytes.length,transparentPixels:transparent,opaquePixels:opaque,sourceSha256:createHash('sha256').update(source).digest('hex')});
}
await writeFile(path.join(docs,'assets.json'),JSON.stringify(records,null,2)+'\n');
console.log(records);

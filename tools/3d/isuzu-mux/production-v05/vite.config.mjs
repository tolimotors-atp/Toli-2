import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root=path.dirname(fileURLToPath(import.meta.url));
export default {root,base:'./',resolve:{alias:{'@':path.resolve(root,'../../../../src')}},build:{outDir:path.join(root,'build'),emptyOutDir:true},server:{host:'127.0.0.1',port:8196,strictPort:true,fs:{allow:[path.resolve(root,'../../../..')]}}};

import type {VehicleModelManifest} from './contract';
/** V04 PREVIEW / TEMPORARY PRODUCTION ASSET. Replace URL when controlled reconstruction is approved. */
export const muxVehicleManifest:VehicleModelManifest={
 url:'models/vehicles/isuzu-mux/isuzu-mux-web.glb',
 source:'tools/3d/isuzu-mux/source/production/isuzu-mux-generated-v04.blend',
 license:'Project-generated reference reconstruction',
 licenseEvidence:'tools/3d/isuzu-mux/WEB_EXPORT_V04_REPORT.md',reviewedForProject:true,
 staticPreview:true,yaw:Math.PI,targetLength:4.825,rollingRadius:.382,parts:{},
 wheels:['FL','FR','RL','RR'].map(tag=>({nodes:[['MUX_ROOT','WHEEL_'+tag]],calipers:[],pivot:[0,0,0],front:tag.startsWith('F'),spinAxis:'z'})),
 reflection:[['V03_NEW_EXTERIOR_SHELL']],materials:{paint:[],glass:[],rubber:[]},
};

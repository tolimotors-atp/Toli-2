import bpy,sys,json,os
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'tools/blender-addons'))
from toli_mux_generator.convergence_data import FRONT,REAR,FRONT_IMAGE,REAR_IMAGE,EVIDENCE
from toli_mux_generator.geometry.flow_cage import points,cubic
r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04';versions={}
def samples(o):
 ps=points(o);pairs=list(zip(ps,ps[1:]))
 if o.data.splines[0].use_cyclic_u:pairs.append((ps[-1],ps[0]))
 return [cubic(a,b,t/60)[0] for a,b in pairs for t in range(61)]
for version in ['v03','v04']:
 bpy.ops.wm.open_mainfile(filepath=str(P/f'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-{version}.blend'));s=bpy.context.scene;versions[version]={}
 for view,rows in [('front',FRONT),('rear',REAR)]:
  camera=bpy.data.objects['CAM_'+view.upper()];s.camera=camera;bpy.context.view_layer.update()
  # Physical body-width anchors in the orthographic render, not a photogrammetry fit.
  anchor=[world_to_camera_view(s,camera,Vector((0,y,1))).x for y in [-.93,.93]];den=abs(anchor[1]-anchor[0]);cx=sum(anchor)/2
  def span(n,inner=False):
   vals=[abs(world_to_camera_view(s,camera,v).x-cx) for v in samples(bpy.data.objects[n])];return 2*(min(vals) if inner else max(vals))/den
  out={}
  for label,probe,*_ in rows:
   if probe in ['BODY','QUARTER']:value=1.
   elif probe=='TIRES':value=1.570/1.860
   elif probe=='ROOF':value=2*abs(world_to_camera_view(s,camera,points(bpy.data.objects['TRACE_ROOF_EDGE'])[-1].co).x-cx)/den
   elif probe=='SHOULDER':value=2*abs(world_to_camera_view(s,camera,points(bpy.data.objects['TRACE_SHOULDER'])[-1].co).x-cx)/den
   elif probe=='GLASS_BAND':value=(1-span('TRACE_REAR_GLASS'))/2
   elif probe=='LOWER_BUMPER':value=2*abs(world_to_camera_view(s,camera,points(bpy.data.objects['TRACE_REAR_BUMPER'])[2].co).x-cx)/den
   elif probe in ['LAMP_OUTER','LAMP_INNER']:value=span('TRACE_HEADLIGHT' if view=='front' else 'TRACE_TAIL_LAMP',probe=='LAMP_INNER')
   else:value=span(probe)
   out[label]=value
  versions[version][view]=out
result={'method':'Hand-read paired photograph landmarks divided by visible body width excluding mirrors; compare sampled Bezier projections in unchanged orthographic cameras. Fractions are image-space guidance, not calibration. ±5–8px landmark uncertainty plus unquantified perspective bias.','versions':versions,'front':[],'rear':[],'evidence':EVIDENCE}
for view,rows,image in [('front',FRONT,FRONT_IMAGE),('rear',REAR,REAR_IMAGE)]:
 den=(FRONT if view=='front' else REAR)[0][2];width=den[1]-den[0]
 for label,probe,(l,rr),row,target in rows:
  reference=(rr-l)/width
  v3,v4=versions['v03'][view][label],versions['v04'][view][label]
  result[view].append({'feature':label,'source':image,'pixels':[l,rr],'row':row,'reference_ratio':reference,'fit_target':target,'v03_render_ratio':v3,'v04_render_ratio':v4,'absolute_error_before':abs(v3-reference),'absolute_error_after':abs(v4-reference)})
(r/'reference-proportions.json').write_text(json.dumps(result,indent=2));(r/'reference-evidence.json').write_text(json.dumps(EVIDENCE,indent=2))
lines=['# V04 normalized image-space proportions','',result['method'],'','Body reference width: front 340 px; rear 335 px. Feature centres are not forced to coincide: the source views have perspective/yaw.','']
for view in ['front','rear']:
 lines+=['## '+view.title(),'','|Feature|Reference|V03 rendered|V04 rendered|','|---|---:|---:|---:|']
 lines += [f"|{d['feature']}|{d['reference_ratio']:.3f}|{d['v03_render_ratio']:.3f}|{d['v04_render_ratio']:.3f}|" for d in result[view]];lines+=['']
(r/'PROPORTION_MAPS.md').write_text('\n'.join(lines));print(json.dumps({v:[(d['feature'],round(d['v03_render_ratio'],3),round(d['v04_render_ratio'],3),round(d['reference_ratio'],3)) for d in result[v]] for v in ['front','rear']}),flush=True);os._exit(0)

import bpy,sys,json,os
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'tools/blender-addons'))
import toli_mux_generator as addon
from toli_mux_generator.geometry.surface_patch import build
from toli_mux_generator.parameters import values
addon.register();bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v03.blend'));s=bpy.context.scene;p=values(s);out={}
for version in [2,3]:
 build(s,p,version=version);o=bpy.data.objects['SURFACE_ZONE_A'];rows=[]
 for t in [0,.25,.5,.75,1]:
  x=-2.18+1.36*t;x=max(-2.1799,min(-.8201,x));result={'fraction':t,'x':x}
  for state in ['base','evaluated']:
   if state=='evaluated':ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
   else:me=o.data
   segments=[]
   for f in me.polygons:
    ps=[me.vertices[i].co for i in f.vertices];cross=[]
    for a,b in zip(ps,ps[1:]+ps[:1]):
     if (a.x-x)*(b.x-x)<0:
      v=a.lerp(b,(x-a.x)/(b.x-a.x))
      if v.y<=1e-6:cross.append([float(-v.y),float(v.z)])
    if len(cross)==2:segments.append(cross)
   result[state]=segments
   if state=='evaluated':ev.to_mesh_clear()
  rows.append(result)
 out['V0'+str(version)]=rows
r=P/'tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03';(r/'bonnet-edge-roll-sections.json').write_text(json.dumps(out,indent=2));print('Five actual base/evaluated cross sections saved',flush=True);os._exit(0)

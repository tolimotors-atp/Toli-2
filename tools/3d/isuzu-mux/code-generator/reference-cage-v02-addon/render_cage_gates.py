import bpy,os
from pathlib import Path
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v01.blend'));s=bpy.context.scene;r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v01';s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=720;s.render.resolution_y=480;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';col=bpy.data.collections['TOLI_MUX_REFERENCE_CAGE']
for view in ['FRONT','FRONT34','SIDE','REAR34','REAR']:
 for o in col.objects:
  kind=o.get('trace_class','section');o.hide_render=(view=='FRONT' and kind not in ['front','section']) or (view=='REAR' and kind not in ['rear','section']) or (view=='SIDE' and kind in ['front','rear'])
 s.camera=bpy.data.objects['CAM_'+view];s.render.filepath=str(r/(view.lower()+'.png'));bpy.ops.render.render(write_still=True)
os._exit(0)

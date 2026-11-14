import bpy,os
from pathlib import Path
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-curve-soft-detail-v01.blend'));s=bpy.context.scene;r=P/'tools/3d/isuzu-mux/code-generator/renders/deep-detail-v01';s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=720;s.render.resolution_y=480;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA'
for view in ['FRONT','FRONT34','SIDE','REAR34','REAR']:
 s.camera=bpy.data.objects['CAM_'+view];s.render.filepath=str(r/('alpha-'+view.lower()+'.png'));bpy.ops.render.render(write_still=True)
os._exit(0)

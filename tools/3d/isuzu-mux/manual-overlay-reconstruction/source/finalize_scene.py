import bpy,shutil,os
from pathlib import Path
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';W=B/'manual-overlay-reconstruction';master=B/'source/production/isuzu-mux-manual-overlay-v01.blend';bpy.ops.wm.open_mainfile(filepath=str(master));s=bpy.context.scene
bpy.data.objects['REFERENCE_FIT_MUX-043'].rotation_euler=(0,0,0)
t=bpy.data.texts['overlay_tools.py'];t.clear();t.write((W/'source/overlay_tools.py').read_text());s['visual_approval']='C — STILL GENERIC / INCORRECT; STOP. NOT APPROVED.'
s['remaining_limits']='Incorrect glazing/D-pillar; bonnet/fender seams; generic front; incorrect rear-quarter/bumper wrap. No details/export/integration.'
bpy.ops.wm.save_as_mainfile(filepath=str(master));dest=W/'milestones/isuzu-mux-manual-overlay-v01-gated.blend';assert not dest.exists();shutil.copy2(master,dest);print('Saved failed-gate checkpoint, no geometry changed',flush=True);os._exit(0)

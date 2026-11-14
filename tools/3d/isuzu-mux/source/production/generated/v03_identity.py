import bpy,bmesh,json,math,os,ast
from pathlib import Path
from mathutils import Vector
O=Path(os.environ.get('MUX_V03_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';A=D/'generated';R=O/'renders/v03';g=json.loads((A/'v03-gates.json').read_text());assert g['greenhouse']=='PASS'
bpy.ops.wm.open_mainfile(filepath=str(D/'milestones/isuzu-mux-v03-greenhouse.blend'));s=bpy.context.scene;body=bpy.data.objects['V03_NEW_EXTERIOR_SHELL'];ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());col=bpy.data.collections['V03_EXTERIOR'];black=bpy.data.materials['Graphite polymer'];chrome=bpy.data.materials['Brushed bright metal'];red=bpy.data.materials['Rear red lens']
tree=ast.parse((A/'v03_greenhouse.py').read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['patch','roundpoly']];exec(compile(ast.Module(body=defs,type_ignores=[]),'V03_surface_helpers','exec'))
surface_patch=patch
def patch(name,points,axis,side,material=None):
 return surface_patch(name,points,axis,side,material,.024 if material==chrome else .014)
# Only large identity envelopes. No badges, optical internals, fine trim or separated body panels.
patch('V03_GRILLE_ENVELOPE',[(-.48,.80),(-.615,1.02),(-.54,1.105),(.54,1.105),(.615,1.02),(.48,.80)],'X',-1)
patch('V03_GRILLE_UPPER_BAR',[(-.54,1.085),(.54,1.085),(.57,1.035),(.48,1.02),(-.48,1.02),(-.57,1.035)],'X',-1,chrome)
patch('V03_GRILLE_LOWER_BAR',[(-.54,.965),(-.46,.89),(.46,.89),(.54,.965),(.42,.94),(-.42,.94)],'X',-1,chrome)
patch('V03_LOWER_OPENING',[(-.55,.72),(.55,.72),(.51,.54),(-.51,.54)],'X',-1)
for side in [-1,1]:
 lamp=[(side*.54,1.055),(side*.85,1.175),(side*.865,1.13),(side*.855,.99),(side*.70,.96),(side*.565,1.01)]
 patch('V03_HEADLAMP_ENVELOPE_'+str(side),lamp,'X',-1)
 patch('V03_CORNER_OPENING_'+str(side),[(side*.65,.55),(side*.79,.55),(side*.79,.77),(side*.70,.78)],'X',-1)
 patch('V03_REAR_OUTER_LAMP_'+str(side),[(side*.73,1.25),(side*.89,1.285),(side*.89,1.07),(side*.73,1.06)],'X',1,red)
 patch('V03_REAR_INNER_LAMP_'+str(side),[(side*.715,1.25),(side*.44,1.19),(side*.52,1.06),(side*.715,1.06)],'X',1,red)
 patch('V03_REAR_LAMP_SIDE_WRAP_'+str(side),[(2.06,1.29),(2.38,1.25),(2.38,1.08),(2.20,1.10)],'Y',side,red)
patch('V03_REAR_BUMPER_INSERT',[(-.79,.62),(.79,.62),(.74,.48),(-.74,.48)],'X',1)
s['V03_STAGE']='Identity envelope study only — recognition review before surfaces, panel cuts or details';s['V03_IDENTITY_LIMIT']='Opaque shell-projected lamp/intake regions and double-bar envelopes; no optics, grille mesh or badges. Not production-finished parts.'
bpy.ops.wm.save_as_mainfile(filepath=str(D/'milestones/isuzu-mux-v03-identity.blend'));bpy.ops.wm.save_as_mainfile(filepath=str(D/'isuzu-mux-generated-v03.blend'))
for name in ['FRONT','FRONT_34','SIDE','REAR_34','REAR']:
 s.camera=bpy.data.objects['CAM_COMPARE_'+name];s.render.filepath=str(R/('v03-identity-'+name.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('V03 IDENTITY STUDY SAVED; NO PANELS, BADGES OR INTERNAL DETAILS',flush=True);os._exit(0)

"""Pass 3A only: landmark-guided macro candidate. No detail/export/integration.
Load the immutable Pass 2 milestone before running.
"""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sc=bpy.context.scene
assert (ROOT/'references/pass3-landmarks.json').exists()
body=bpy.data.objects['BODY_PASS2_CONTINUOUS'];body.name='BODY_PASS3A_PROPORTION_STUDY'
# Keep wheel anchors, shorten ONLY overhang regions of the existing authored cage.
for v in body.data.vertices:
 x,y,z=v.co
 if x>1.425:v.co.x=1.425+(x-1.425)*.80
 if x< -1.425:v.co.x=-1.425+(x+1.425)*.84
 # Lower the high belt/shoulder while preserving the successful roof crown.
 influence=max(0,1-abs(z-1.22)/.55)
 v.co.z-=.075*influence
 # Remove some inflated shoulder width; retain the original mirror workflow.
 v.co.y-=.020*math.exp(-((z-1.12)/.18)**2)*min(1,y/.8)
body.data.update()
sc['status']='PASS 3A PROPORTION CHECK — NOT APPROVED; NO DETAILS'
sc['reference_landmarks']='references/pass3-landmarks.json; pixel and world estimates explicitly uncertain'
# Add labeled world guides in an editable non-rendering collection.
coll=bpy.data.collections.new('PASS3_LANDMARK_GUIDES — estimates');sc.collection.children.link(coll)
guides={'FRONT_WHEEL':(1.425,.825,.39),'REAR_WHEEL':(-1.425,.825,.39),'FRONT_TIP':(2.30,0,.68),'REAR_TIP':(-2.31,0,.68),'COWL':(1.02,0,1.22),'WINDSCREEN_TOP':(.32,0,1.80),'ROOF_PEAK':(-.7,0,1.86),'BELT':(0,.85,1.17),'ROCKER':(0,.86,.36),'A_BASE':(1.02,.82,1.22),'A_TOP':(.32,.75,1.80),'B':(-.42,.80,1.50),'C':(-1.29,.80,1.50),'D':(-2.12,.77,1.50),'FRONT_ARCH_APEX':(1.425,.94,.86),'REAR_ARCH_APEX':(-1.425,.94,.86),'GRILLE_TOP':(2.30,0,1.05),'GRILLE_BOTTOM':(2.30,0,.72),'GRILLE_EDGE':(2.28,.56,.90),'HEADLIGHT_INNER':(2.24,.57,1.06),'HEADLIGHT_OUTER':(2.12,.88,1.13),'LOWER_INTAKE':(2.30,0,.49),'BUMPER_CORNER':(2.23,.86,.55),'TAILGATE_EDGE':(-2.26,.72,1.02),'REAR_GLASS':(-2.20,0,1.47),'TAILLAMP_BOUNDARY':(-2.21,.88,1.17),'REAR_BUMPER':(-2.30,.85,.55),'SPOILER':(-2.03,0,1.82)}
for name,pos in guides.items():
 o=bpy.data.objects.new(name,None);coll.objects.link(o);o.location=pos;o.empty_display_type='SPHERE';o.empty_display_size=.025;o.hide_render=True;o['status']='Estimated guide, not completed geometry'
# Neutral material override deliberately excludes badges/grille identity from silhouette assessment.
mat=bpy.data.materials.new('PASS3A FLAT GREY');mat.diffuse_color=(.38,.40,.42,1);mat.use_nodes=True;p=mat.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(.38,.40,.42,1);p.inputs['Roughness'].default_value=.65
# Save the editable checkpoint with study materials retained.
for file in ['source/milestones/isuzu-mux-body-pass3a.blend','source/milestones/isuzu-mux-body-pass3.blend']:
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/file))
sc.view_layers[0].material_override=mat
sc.render.engine='CYCLES';sc.cycles.samples=8;sc.render.resolution_x=1000;sc.render.resolution_y=650
cam=sc.camera;cam.data.type='PERSP';cam.data.lens=65
for name,pos in {'front':(9.5,0,1.55),'left':(0,10.4,1.65),'rear':(-9.5,0,1.55)}.items():
 cam.location=pos;cam.rotation_euler=(Vector((0,0,.95))-cam.location).to_track_quat('-Z','Y').to_euler();sc.render.filepath=str(ROOT/'renders/pass3a'/('proportions-'+name+'.png'));bpy.ops.render.render(write_still=True)

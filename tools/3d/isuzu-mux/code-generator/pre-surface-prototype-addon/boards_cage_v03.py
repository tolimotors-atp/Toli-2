from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json,runpy,math
P=Path(__file__).resolve().parents[3];r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v03';old=r/'baseline-v02';src=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');data=json.loads((r/'coordinates.json').read_text());td=runpy.run_path(str(P/'tools/blender-addons/toli_mux_generator/traced_data.py'))
f=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',18);small=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',14)
views=[('front','18-17-10'),('front34','18-17-27'),('side','18-17-14'),('rear34','18-17-31'),('rear','18-17-18')]
b=Image.new('RGB',(2400,2810),'#16191f');d=ImageDraw.Draw(b)
for i,(v,t) in enumerate(views):
 ims=[Image.open(src/f'Screenshot From 2026-11-06 {t}.png').crop((5,65,1033,530)),Image.open(old/f'{v}.png'),Image.open(r/f'{v}.png')]
 # Apply the same alpha-union crop to V01/V02; no per-version reframing.
 boxes=[im.getchannel('A').getbbox() for im in ims[1:]]
 box=(max(0,min(b[0] for b in boxes)-25),max(0,min(b[1] for b in boxes)-25),min(960,max(b[2] for b in boxes)+25),min(640,max(b[3] for b in boxes)+25))
 ims[1:]=[im.crop(box) for im in ims[1:]]
 for j,im in enumerate(ims):
  if im.mode=='RGBA':bg=Image.new('RGBA',im.size,(22,25,31,255));bg.alpha_composite(im);im=bg.convert('RGB')
  im=ImageOps.contain(im,(780,500));b.paste(im,(j*800+(800-im.width)//2,i*560+45+(500-im.height)//2));d.text((j*800+16,i*560+12),['REFERENCE','CAGE V02','CAGE V03'][j]+' / '+v,font=f,fill='white')
d.text((16,2790),'Inferred depth, not calibrated. Matched cameras/light/crop between cages; source photos are perspective.',font=small,fill='#cccbd0');b.save(r/'reference-v02-v03-comparison.jpg',quality=95)
def inverse_z(z,knots):
 for (v0,z0),(v1,z1) in zip(knots,knots[1:]):
  if z>=z1:return v0+(z-z0)/(z1-z0)*(v1-v0)
 return knots[-1][0]
def uv(source,co):
 x,y,z=co
 if source=='side':
  knots=[(144,-2.4125),(284,-1.4225),(776,1.4225),(928,2.4125)]
  for (u0,x0),(u1,x1) in zip(knots,knots[1:]):
   if x<=x1:return (u0+(x-x0)/(x1-x0)*(u1-u0),455-z/1.86*331)
  return (928,455-z/1.86*331)
 center,half,knots=(543,165,[(132,1.86),(249,1.30),(350,.88),(480,0)]) if source=='front' else (528,173,[(140,1.86),(257,1.30),(413,.28),(476,0)])
 return (center+y/.93*half,inverse_z(z,knots))
for source,filename in td['SOURCES'].items():
 im=Image.open(src/filename).convert('RGB');dr=ImageDraw.Draw(im)
 for name,(s,pts,depth,closed) in td['TRACES'].items():
  if s!=source:continue
  dr.line(pts+([pts[0]] if closed else []),fill='#f7ad49',width=1)
  out=[uv(source,c) for c in data['TRACE_'+name]['points']];dr.line(out+([out[0]] if closed else []),fill='#20dfec',width=2)
 dr.rectangle((5,5,1028,53),fill='#181b22');dr.text((14,9),'Source landmarks: amber / V03 controls: cyan. Control polygons, not calibrated reprojection.',font=small,fill='white');dr.text((14,29),'Main silhouette/windows locked; local fender, shoulder and rear joins refined.',font=small,fill='#a9dfe9');im.save(r/f'native-traces-{source}.jpg',quality=95)

# Section controls shown at useful scale without inventing surfaced body panels.
canvas=Image.new('RGB',(2400,1180),'#171b22');dr=ImageDraw.Draw(canvas)
groups=[('FRONT / FIVE BONNET ROLLS + COWL',['SECTION_BONNET_'+str(i) for i in range(5)]),('GREENHOUSE + D-PILLAR',['SECTION_WINDSCREEN_MID','SECTION_B_ROOF','SECTION_C_ROOF','SECTION_D_BODY']),('REAR / WHEEL + GLASS + LAMP + BUMPER',['SECTION_REAR_FENDER','SECTION_REAR_GLASS','SECTION_LAMP_BAND','SECTION_TAILGATE','SECTION_UPPER_BUMPER','SECTION_LOWER_BUMPER'])]
colors=['#ff7864','#ffd365','#69dec2','#64b7ff','#cf99ff','#f1a5dc']
for j,(title,names) in enumerate(groups):
 ox=j*800;dr.text((ox+20,20),title,font=f,fill='white')
 for z in [0,.5,1,1.5,2]:
  py=760-z*310;dr.line((ox+35,py,ox+765,py),fill='#303741');dr.text((ox+40,py+4),f'Z {z:.1f}',font=small,fill='#959da8')
 dr.line((ox+400,90,ox+400,780),fill='#68727e')
 for i,n in enumerate(names):
  co=data[n]['points'];pts=[(ox+400+y*310,760-z*310) for x,y,z in co];dr.line(pts,fill=colors[i%6],width=3)
  for x,y in pts:dr.ellipse((x-3,y-3,x+3,y+3),fill=colors[i%6])
  dr.text((ox+24,820+i*30),n,font=small,fill=colors[i%6])
dr.text((20,1120),'Actual V03 Y/Z control polygons; inferred cage sections, not surfaced cross-sections or calibrated depths.',font=f,fill='white');canvas.save(r/'depth-sections-v03.jpg',quality=95)
# Large local photo/cage comparisons. Crop windows match V02/V03 exactly.
crops=json.loads((r/'join-crops.json').read_text());evidence={'J01':('18-17-27',(240,235,600,455)),'J02':('18-17-27',(325,165,600,330)),'J04':('18-17-31',(525,130,785,290)),'J05':('18-17-31',(430,220,690,425)),'J06':('18-17-31',(555,240,860,355)),'J07':('18-17-31',(555,325,885,465)),'J08':('18-17-31',(530,140,870,350))}
board=Image.new('RGB',(2400,7*500),'#171b22');bd=ImageDraw.Draw(board)
for row,(join,meta) in enumerate(crops.items()):
 photo,box=evidence[join];ims=[Image.open(src/f'Screenshot From 2026-11-06 {photo}.png').crop(box)]+[Image.open(r/'joins'/version/(join.lower()+'.png')) for version in ['v02','v03']]
 local=Image.new('RGB',(2400,500),'#171b22');ld=ImageDraw.Draw(local)
 for j,im in enumerate(ims):
  if im.mode=='RGBA':bg=Image.new('RGBA',im.size,(22,25,31,255));bg.alpha_composite(im);im=bg.convert('RGB')
  im=ImageOps.contain(im,(780,420));local.paste(im,(800*j+(800-im.width)//2,50+(420-im.height)//2));ld.text((800*j+16,12),join+' / '+['REFERENCE EVIDENCE','V02','V03'][j],font=f,fill='white')
 ld.text((15,478),'Uncalibrated photo evidence; cage close-ups share camera, scale and target. Wire cage only.',font=small,fill='#bec6d0');local.save(r/('join-'+join.lower()+'.jpg'),quality=95);board.paste(local,(0,row*500))
board.save(r/'join-comparison.jpg',quality=95)

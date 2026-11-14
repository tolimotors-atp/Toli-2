from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
import json
W=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction');R=W/'renders/v01';F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',21);SM=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',16)
views=['front','front34','side','rear34','rear','overhead'];ids=['011','016','012','017','013'];labels=['FRONT','FRONT 3/4','SIDE','REAR 3/4','REAR'];sil={
'011':[(304,220),(316,163),(329,145),(350,133),(446,133),(473,150),(497,194),(513,223),(531,256),(550,320),(549,375),(540,400),(513,400),(503,371),(332,371),(326,402),(299,404),(292,384),(286,319),(287,262)],
'012':[(112,289),(114,255),(135,236),(247,215),(278,196),(319,166),(359,145),(399,138),(615,137),(655,146),(669,167),(690,202),(704,231),(713,294),(703,314),(661,327),(650,357),(625,377),(594,378),(567,361),(557,340),(281,340),(271,365),(248,385),(215,387),(186,369),(171,339),(136,333),(116,316)],
'013':[(292,221),(309,180),(323,156),(344,149),(471,149),(489,163),(506,196),(514,220),(529,237),(539,320),(534,375),(529,402),(500,402),(492,377),(317,377),(311,402),(280,404),(275,377),(273,323),(279,249)],
'016':[(128,298),(137,263),(161,241),(223,219),(264,203),(306,170),(343,151),(398,139),(475,137),(590,140),(622,145),(638,173),(649,216),(660,237),(663,273),(652,312),(636,323),(625,350),(604,370),(580,370),(561,353),(549,335),(376,365),(359,395),(338,410),(314,409),(292,391),(278,370),(153,350),(130,328)],
'017':[(211,258),(220,232),(238,215),(260,205),(286,181),(315,159),(346,148),(398,144),(480,149),(570,153),(599,164),(624,186),(638,214),(655,234),(661,294),(659,327),(641,346),(621,365),(606,381),(582,383),(560,373),(430,357),(421,387),(403,406),(383,404),(366,385),(356,356),(265,322),(251,342),(235,345),(218,331),(211,301)]}
# Hand-read approximate reference boundaries; these are diagnostic traces, not measured/segmented truth.
internal={
'011':[[(316,222),(328,165),(469,165),(509,222),(316,222)],[(317,233),(349,261),(495,261),(522,233)]],
'012':[[(269,217),(321,176),(353,161),(429,159),(432,215),(269,217)],[(443,159),(552,161),(565,170),(555,207),(444,216),(443,159)],[(584,161),(641,167),(665,202),(594,202),(584,161)],[(139,250),(260,223)]],
'013':[[(296,224),(318,175),(486,175),(510,224),(296,224)],[(282,255),(330,260),(489,260),(529,251)],[(291,310),(511,310)]],
'016':[[(227,217),(310,179),(352,167),(390,171),(361,223),(227,217)],[(369,224),(407,175),(432,172),(439,215),(369,224)],[(449,174),(530,173),(536,203),(450,214),(449,174)],[(547,173),(598,170),(626,211),(560,210),(547,173)],[(148,256),(241,235),(351,227)]],
'017':[[(271,214),(298,180),(318,168),(336,171),(329,218),(271,214)],[(340,171),(390,176),(379,220),(338,218),(340,171)],[(405,176),(445,179),(458,222),(406,217),(405,176)],[(472,183),(589,176),(629,220),(474,235),(472,183)],[(440,253),(503,262),(643,245)]]}
selection=json.loads((W/'references/selection.json').read_text())
def neutral(im):
 im=im.convert('RGBA');out=Image.new('RGBA',im.size,(218,218,218,255));out.alpha_composite(im);return out.convert('RGB')
def board(files,name,cols=3):
 count=len(files);out=Image.new('RGB',(cols*800,((count+cols-1)//cols)*565),'#191e25');d=ImageDraw.Draw(out)
 for i,(path,label) in enumerate(files):
  x=(i%cols)*800;y=(i//cols)*565;im=Image.open(path);im=neutral(im);im.thumbnail((800,520));out.paste(im,(x+(800-im.width)//2,y+38));d.text((x+12,y+8),label,font=F,fill='white')
 out.save(R/name,quality=94)
for mode in ['clay','reflection','wire','zebra']:board([(R/f'{mode}-{v}.png',f'{mode.upper()} / {v}') for v in views],f'{mode}-six-view.jpg')
for r in selection:
 id=r['id'][-3:];ref=Image.open(W/'normalized'/f'{id}.png').convert('RGB');render=Image.open(R/f'clay-{id}.png').convert('RGBA');model=neutral(render);mix=ref.copy();a=render.getchannel('A').point(lambda x:round(x*.5));mix.paste(render.convert('RGB'),(0,0),a);d=ImageDraw.Draw(mix);d.text((8,8),f"{r['id']} / 50% overlay / reference-fit, not calibrated",font=SM,fill='#b91036');mix.save(R/f'overlay-{id}.png')
 ref.save(R/f'reference-{id}.png');model.save(R/f'model-{id}.png')
 # Actual rendered model silhouette; includes tires, excludes studio and absent trim.
 alpha=render.getchannel('A').point(lambda x:255 if x>128 else 0);edge=ImageChops.difference(alpha.filter(ImageFilter.MaxFilter(3)),alpha.filter(ImageFilter.MinFilter(3)));silim=ref.copy();silim.paste('#ff7733',(0,0,800,520),edge)
 if id in sil:
  sd=ImageDraw.Draw(silim);sd.line(sil[id]+[sil[id][0]],fill='#00d5df',width=2);sd.text((8,8),'CYAN: coarse hand reference trace / ORANGE: rendered model',font=SM,fill='#9b1232');silim.save(R/f'silhouette-overlay-{id}.png')
 if id in internal:
  wire=Image.open(R/f'wire-{id}.png').convert('RGBA');w=ref.copy();w.paste(wire.convert('RGB'),(0,0),wire.getchannel('A').point(lambda x:round(x*.45)));d=ImageDraw.Draw(w)
  for points in internal[id]:d.line(points,fill='#00d5df',width=2)
  d.text((8,8),'CYAN: approximate reference internal boundaries / model control net',font=SM,fill='#a41435');w.save(R/f'internal-wire-overlay-{id}.png')
board([(R/f'overlay-{id}.png',label+' / 50% reference overlay') for id,label in zip(ids,labels)]+[(R/'overlay-043.png','OVERHEAD / low confidence plan only')],'reference-overlay-six-view.jpg')
board([(R/f'silhouette-overlay-{id}.png',label+' / approximate silhouette comparison') for id,label in zip(ids,labels)],'silhouette-five-view.jpg')
board([(R/f'internal-wire-overlay-{id}.png',label+' / internal-boundary comparison') for id,label in zip(ids,labels)],'internal-boundary-five-view.jpg')
comparison=[]
for id,label in zip(ids,labels):comparison += [(R/f'reference-{id}.png',label+' / REFERENCE'),(R/f'previous-clay-{id}.png',label+' / EXISTING-PHOTO V01'),(R/f'model-{id}.png',label+' / MANUAL-OVERLAY V01')]
board(comparison,'reference-previous-new-comparison.jpg')
close=['bonnet-fender','fender-a-pillar','cowl-windscreen','greenhouse','d-pillar','rear-quarter','rear-bumper-corner'];board([(R/f'clay-{v}.png',v) for v in close],'primary-surface-closeups.jpg')
(W/'diagnostics/hand-reference-traces.json').write_text(json.dumps({'canvas':[800,520],'note':'Coarse visually read contours. Not precise masks, not photogrammetric correspondences, no calibrated accuracy or IoU claimed. Mirror/roof rail/step details excluded where practical.','silhouette':sil,'internal':internal},indent=2))
print('Comparison, overlay, silhouette, internal-boundary and close-up boards saved')

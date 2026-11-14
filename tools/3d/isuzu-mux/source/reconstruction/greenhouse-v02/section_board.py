from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,os
O=Path(os.environ.get('MUX_GREENHOUSE_OUTPUT',Path(__file__).resolve().parents[3]));A=O/'source/reconstruction/greenhouse-v02';cuts=json.loads((A/'cross-section-cuts.json').read_text());im=Image.new('RGB',(1500,1600),'#20242a');d=ImageDraw.Draw(im);f=ImageFont.load_default(size=16)
d.text((12,10),'G01–G11 / actual triangulated surface cuts (white) and station controls (orange)',fill='white',font=f);d.text((12,35),'Wheelbase = 1; no physical metres or calibrated depth claimed. Unjoined strips remain visible.',fill='#cccccc',font=f)
for i,c in enumerate(cuts):
 col=i%3;row=i//3;x0=col*500;y0=70+row*365
 d.text((x0+14,y0+5),c['id']+' '+c['region'],fill='white',font=f);d.text((x0+14,y0+28),f"x = {c['x']:.3f}",fill='#aaaaaa',font=f)
 def pt(y,z):return(x0+250+y*650,y0+325-(z-.40)*900)
 for z in [.45,.50,.55,.60,.65]:
  d.line([pt(-.34,z),pt(.34,z)],fill='#3b4148');d.text((x0+2,pt(0,z)[1]),str(z),fill='#aaaaaa',font=f)
 for y in [-.3,-.15,0,.15,.3]:d.line([pt(y,.4),pt(y,.66)],fill='#3b4148')
 r=c['controls'];pts=[]
 for j in range(17):
  t=-1+2*j/16;pts.append(pt(r['roof_halfwidth']*t,r['upper_z']+r['crown']*(1-t*t)))
 d.line(pts,fill='#d78337',width=2)
 for side in (-1,1):d.line([pt(side*r['lower_halfwidth'],r['lower_z']),pt(side*r['roof_halfwidth'],r['upper_z'])],fill='#d78337',width=2)
 for a,b in c['actual_mesh_intersections']:d.line([pt(*a),pt(*b)],fill='#f3f5f6',width=2)
 # The station guide is not a closed body section. The lower gap is intentional: no door/body geometry exists.
x0=1000;y0=70+3*365;d.text((x0+14,y0+5),'Width / tumblehome controls',fill='white',font=f)
for k,color in [('roof_halfwidth','#eeeeee'),('lower_halfwidth','#d78337')]:
 pts=[(x0+40+(c['x']+.405)/1.125*420,y0+300-(c['controls'][k]-.22)/.10*220) for c in cuts];d.line(pts,fill=color,width=3)
d.text((x0+14,y0+45),'White: roof half-width',fill='#eeeeee',font=f);d.text((x0+14,y0+70),'Orange: lower side half-width',fill='#d78337',font=f)
im.save(O/'renders/greenhouse-cross-sections-v02.jpg',quality=96)
print('All eleven actual mesh cuts plotted')

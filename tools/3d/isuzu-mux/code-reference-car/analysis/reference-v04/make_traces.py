from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
import json
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');W=P/'tools/3d/isuzu-mux/code-reference-car';D=W/'reference-data/v04';O=W/'renders/reference-v04';R=P.parent/'Isuzu MU-X'
def view(s,features):return {'file':str(R/f'Screenshot From 2026-11-06 {s}.png'),'imageSize':Image.open(R/f'Screenshot From 2026-11-06 {s}.png').size,'features':features}
V={
'front':view('18-17-10',{
'bonnetLeading':[[455,311],[500,308],[609,308],[654,311]],'bonnetCentre':[[532,249],[534,277],[535,308]],'bonnetSide':[[653,248],[666,270],[689,290]],'grilleOuter':[[455,311],[654,311],[644,350],[611,370],[490,370],[464,347],[455,311]],'grilleInner':[[478,319],[628,319],[618,336],[488,336],[478,319]],'lampUpper':[[644,319],[663,308],[689,290]],'lampOuter':[[689,290],[697,309],[699,334]],'lampLower':[[699,334],[678,345],[653,350],[644,319]],'lampInner':[[644,319],[644,335],[653,350]],'bumperUpper':[[402,351],[474,370],[637,371],[701,348]],'bumperLower':[[397,418],[473,427],[637,429],[701,416]],'lowerOpening':[[475,378],[641,378],[636,399],[480,400],[475,378]],'frontArch':[[375,351],[375,395],[382,442]],'fenderCrown':[[688,288],[683,269],[672,250]],'shoulderDeparture':[[674,251],[668,231],[654,211]]}),
'front34':view('18-17-27',{
'bonnetLeading':[[177,287],[223,295],[276,309]],'bonnetCentre':[[329,228],[252,253],[185,282]],'bonnetSide':[[441,250],[390,258],[352,286]],'grille':[[176,290],[274,312],[244,342],[174,331],[176,290]],'lampUpper':[[252,319],[300,299],[358,286]],'lampLower':[[252,335],[295,339],[334,327],[358,286]],'fenderCrown':[[354,286],[404,271],[466,278],[500,307]],'frontArch':[[335,404],[350,359],[384,333],[430,324],[469,341],[488,384]],'aPillar':[[441,250],[482,194],[533,157]],'windscreen':[[329,228],[409,165],[527,169],[441,250],[329,228]],'shoulder':[[501,267],[641,249],[759,224]],'wheelCentres':[[432,410],[791,354]]}),
'side':view('18-17-14',{
'bonnetProfile':[[153,284],[212,254],[330,224]],'windscreen':[[330,224],[402,163],[445,145]],'roof':[[405,146],[533,126],[794,129],[863,146]],'windowLine':[[377,241],[580,257],[722,245]],'quarterGlass':[[784,161],[846,162],[874,218],[804,226],[784,161]],'dPillarOuter':[[861,147],[885,173],[900,230]],'shoulder':[[339,264],[578,270],[752,260],[876,253]],'belt':[[378,246],[578,260],[730,248]],'lowerBody':[[336,405],[568,405],[728,398]],'frontArch':[[212,396],[215,345],[244,316],[280,312],[318,331],[336,384]],'rearArch':[[728,392],[730,343],[761,309],[804,300],[841,318],[853,379]],'rearQuarter':[[750,260],[836,257],[887,276],[912,321]],'bumperTermination':[[923,302],[924,346],[909,371],[857,390]],'wheelCentres':[[274,386],[790,382]]}),
'rear':view('18-17-18',{
'roofTermination':[[404,152],[455,145],[596,145],[645,156]],'dPillarOuter':[[404,160],[381,207],[372,252]],'dPillarInner':[[418,170],[404,216],[395,249]],'rearGlass':[[418,169],[630,170],[651,229],[640,248],[399,251],[398,222],[418,169]],'lampUpper':[[365,257],[393,271],[429,280]],'lampLower':[[429,280],[414,299],[364,299],[365,257]],'lampInner':[[429,280],[414,299]],'lampOuter':[[365,257],[362,278],[364,299]],'tailgate':[[431,274],[616,274],[631,345],[612,366],[429,365],[414,344],[431,274]],'shoulder':[[365,249],[430,264],[615,264],[681,249]],'quarterOuter':[[365,301],[368,353],[373,405]],'bumperUpper':[[374,373],[440,383],[606,383],[671,374]],'bumperFace':[[373,382],[444,403],[607,403],[674,383]],'bumperLower':[[374,411],[438,424],[610,424],[675,409]],'wheelCentres':[[390,425],[650,425]]}),
'rear34':view('18-17-31',{
'quarterVolume':[[533,267],[552,288],[563,325],[576,365]],'rearArch':[[476,404],[479,353],[509,322],[549,316],[582,337],[594,397]],'shoulder':[[356,242],[469,257],[567,252],[648,267]],'dPillar':[[588,159],[613,172],[620,246]],'rearGlass':[[620,176],[794,167],[828,220],[804,246],[621,252],[620,176]],'tailLamp':[[569,254],[615,270],[666,281],[650,301],[575,303],[569,254]],'tailgateDepth':[[665,277],[803,258],[814,332],[789,356],[650,372]],'bumperCorner':[[594,371],[623,381],[647,394],[649,414]],'lowerBumper':[[626,420],[745,411],[806,386]],'wheelCentres':[[326,365],[622,388]]}),
'oppositeFront':view('18-17-25',{'lamp':[[625,290],[668,304],[716,320],[722,337],[645,335],[625,290]],'fender':[[590,280],[619,308],[627,358]],'grille':[[710,304],[831,288],[842,335],[744,354]],'windscreen':[[493,166],[628,161],[715,235],[535,251],[493,166]]}),
'oppositeRear':view('18-17-35',{'lamp':[[303,278],[345,264],[416,252],[406,300],[341,309],[303,278]],'dPillar':[[355,170],[349,209],[356,246]],'bumperCorner':[[410,368],[400,389],[389,400]],'quarter':[[343,273],[375,290],[412,331]]})}
(D/'image-traces.json').write_text(json.dumps({'method':'fresh manual pixel-space design polylines, no image warp; uncalibrated; primary views not averaged','views':V},indent=2))
locks={k:{'primary':v['file'],'support':[]} for k,v in V.items()};locks['front']['support']=[str(R/'Screenshot From 2026-11-06 18-08-46.png'),str(R/'20250902050117_Isuzu_mu-X_Silver_Metallic[1].avif')];locks['rear34']['support']=[str(R/'Screenshot 2026-11-08 213459.png'),str(R/'Screenshot 2026-11-08 213502.png')];(D/'reference-locks.json').write_text(json.dumps(locks,indent=2))
# Shared semantic constraints. Depth orders come from quarter views, not front-only extrusion.
landmarks=[
{'name':'headlightInnerUpper','observations':{'front':[644,319],'front34':[252,319]},'surface':'frontFace','yz':[.54,1.025],'relation':'forward of outer tip; near grille upper end'},
{'name':'headlightOuterUpper','observations':{'front':[689,290],'front34':[358,286]},'surface':'frontFace','yz':[.865,1.115],'relation':'higher and rearward, wrapping toward front fender'},
{'name':'headlightInnerLower','observations':{'front':[653,350],'front34':[252,335]},'surface':'frontFace','yz':[.64,.935],'relation':'outboard of upper inner corner'},
{'name':'headlightOuterLower','observations':{'front':[699,334],'front34':[334,327]},'surface':'frontFace','yz':[.875,.965],'relation':'lower return on same body corner'},
{'name':'rearLampInnerUpper','observations':{'rear':[429,280],'rear34':[666,281]},'surface':'rearFace','yz':[.49,1.205],'relation':'near hatch; rearward of outer quarter tip'},
{'name':'rearLampOuterUpper','observations':{'rear':[365,257],'rear34':[569,254]},'surface':'rearFace','yz':[.86,1.265],'relation':'upper corner wraps into quarter'},
{'name':'rearLampInnerLower','observations':{'rear':[414,299],'rear34':[650,301]},'surface':'rearFace','yz':[.59,1.065],'relation':'diagonal taper toward hatch'},
{'name':'rearGlassLower','observations':{'rear':[640,248],'rear34':[804,246]},'surface':'rearFrame','yz':[.75,1.33],'relation':'forward at side relative to centre; shares D-pillar shell'},
{'name':'quarterGlassRear','observations':{'side':[874,218],'rear34':[613,240]},'worldEstimate':[2.04,.78,1.33],'relation':'just forward of D-pillar outer return'},
{'name':'rearArchCrown','observations':{'side':[804,300],'rear34':[549,316]},'worldEstimate':[1.475,.93,.819],'relation':'same rear axle, fixed .437 arch radius'},
{'name':'frontArchCrown','observations':{'side':[280,312],'front34':[430,324]},'worldEstimate':[-1.37,.93,.819],'relation':'fixed front axle; outer skin controls surround, wheel does not move'},
{'name':'bumperCorner','observations':{'rear':[671,374],'rear34':[623,381]},'surface':'rearFace','yz':[.86,.63],'relation':'gradual face-to-corner-to-side ellipse; no independent protruding layer'}]
(D/'cross-view-landmarks.json').write_text(json.dumps({'accuracy':'semantic reconciliation and visual estimates only; no calibrated triangulation','landmarks':landmarks,'unresolved':['camera pitch and lens calibration','exact tangent/normal field across unobserved body corners','rear-quarter crown depth between visible contours']},indent=2))
def sheet(keys,name):
 out=Image.new('RGB',(1400,460*((len(keys)+1)//2)),'#ddd');draw=ImageDraw.Draw(out)
 for i,k in enumerate(keys):
  v=V[k];im=Image.open(v['file']).convert('RGB');dd=ImageDraw.Draw(im)
  for j,(n,pts) in enumerate(v['features'].items()):
   color=['#ff2f59','#1aaf74','#0077ee','#d68000'][j%4];dd.line([tuple(q) for q in pts],fill=color,width=3);dd.text(tuple(pts[0]),n,fill=color,stroke_width=1,stroke_fill='white')
  im=ImageOps.contain(im,(690,420));x=i%2*700;y=i//2*460;out.paste(im,(x+(700-im.width)//2,y+35));draw.text((x+10,y+10),k+' / '+Path(v['file']).name,fill='#222')
 out.save(O/name,quality=95)
sheet(['front','front34','side','oppositeFront'],'fresh-front-traces.jpg');sheet(['rear','rear34','side','oppositeRear'],'fresh-rear-traces.jpg')
(D/'checkpoint-01.md').write_text('Checkpoint 1: all 43 original files re-inspected via fresh inventory/contact sheets; five full-resolution primary views inspected again. New manual design traces and shared semantic observations saved before major geometry changes. Depth remains an authored estimate, not calibrated reconstruction. Primary silver-family sources, compatible red support only. No V03 surface values imported into this dataset.\n')
print('Fresh traces and cross-view semantic dataset saved; no geometry edits')

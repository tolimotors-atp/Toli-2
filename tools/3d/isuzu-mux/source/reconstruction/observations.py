"""Manual image-pixel annotations, not automatic features or precise survey data.
L/R are physical vehicle left/right (+/-Y). Rim centers preferred; hidden hubs excluded.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
obs={}
def add(i,side=None,**points):
 d=obs.setdefault(i,{})
 for k,p in points.items():d[k+('_'+side if side else '')]=p
# Canonical front/open: only fixed fascia and visible ground contacts. No raised-bonnet/hidden glass anchors.
add(1,'R',h_out=[246,299],h_in=[309,351],g_top=[294,320],g_low=[321,384],bumper=[218,442],contact_F=[244,503])
add(1,'L',h_out=[558,299],h_in=[500,351],g_top=[513,320],g_low=[487,384],bumper=[589,442],contact_F=[564,503])
# Open left and right: fixed quarter glass, body lamps and tire anchors; door glass excluded.
add(2,'L',wc_F=[218,355],wc_R=[764,356],tiretop_F=[218,279],contact_F=[218,431],tiretop_R=[764,280],contact_R=[764,429],h_out=[142,225],h_in=[82,264],q_ft=[774,115],q_fb=[791,159],q_rt=[848,112],q_rb=[887,169],tl_top=[849,182],tl_low=[878,227],arch_F=[218,268],arch_R=[764,258])
add(4,'R',wc_F=[850,362],wc_R=[309,360],tiretop_F=[850,286],contact_F=[850,435],tiretop_R=[309,285],contact_R=[309,437],h_out=[930,225],h_in=[986,264],q_ft=[293,119],q_fb=[281,171],q_rt=[214,114],q_rb=[169,178],tl_top=[216,187],tl_low=[178,232],arch_F=[850,270],arch_R=[309,266])
# Rear/open: no moving hatch glass/lamp segment points.
add(3,'L',contact_R=[329,458],tl_top=[315,211],tl_low=[307,258])
add(3,'R',contact_R=[644,458],tl_top=[649,211],tl_low=[672,258])
# Closed front.
add(6,'R',contact_F=[399,478],h_out=[405,291],h_in=[466,341],g_top=[461,313],g_low=[482,365],bumper=[393,423],ws_base=[410,244],ws_top=[431,167])
add(6,'L',contact_F=[683,474],h_out=[692,289],h_in=[644,340],g_top=[649,311],g_low=[621,364],bumper=[700,421],ws_base=[659,242],ws_top=[621,165])
add(7,'L',wc_F=[293,396],wc_R=[778,385],tiretop_F=[293,332],contact_F=[293,458],tiretop_R=[778,324],contact_R=[778,447],h_out=[227,271],h_in=[164,308],ws_base=[419,221],ws_top=[487,154],q_ft=[783,165],q_fb=[798,213],q_rt=[865,160],q_rb=[895,218],tl_top=[852,230],tl_low=[872,271],arch_F=[293,312],arch_R=[778,299])
add(9,'R',wc_F=[772,389],wc_R=[282,391],tiretop_F=[772,325],contact_F=[772,455],tiretop_R=[282,328],contact_R=[282,458],h_out=[836,265],h_in=[890,301],ws_base=[664,224],ws_top=[562,155],q_ft=[280,166],q_fb=[269,212],q_rt=[207,160],q_rb=[163,218],tl_top=[209,235],tl_low=[179,271],arch_F=[772,306],arch_R=[282,311])
add(8,'L',contact_R=[377,478],tl_top=[366,251],tl_low=[367,299],rw_top=[408,183],rw_base=[380,249],hatch_low=[389,353])
add(8,'R',contact_R=[672,475],tl_top=[682,251],tl_low=[683,299],rw_top=[626,181],rw_base=[653,250],hatch_low=[654,353])
# Front quarters. Closest fixed lamps/glass are preferred; ambiguous far points carry larger uncertainty.
add(10,'R',wc_F=[562,416],wc_R=[275,357],tiretop_F=[562,346],contact_F=[562,484],tiretop_R=[275,307],contact_R=[275,412],ws_base=[535,246],ws_top=[487,163],h_out=[626,288],h_in=[716,338],g_top=[714,309],g_low=[738,356],q_ft=[297,156],q_fb=[296,200],q_rt=[255,150],q_rb=[237,191],arch_F=[562,327],arch_R=[275,286])
add(10,'L',ws_base=[708,235],ws_top=[650,160],g_top=[833,292],g_low=[835,339])
add(11,'L',wc_F=[423,411],wc_R=[783,359],tiretop_F=[423,343],contact_F=[423,480],tiretop_R=[783,305],contact_R=[783,416],ws_base=[472,247],ws_top=[535,163],h_out=[360,286],h_in=[268,338],g_top=[278,309],g_low=[259,351],q_ft=[778,155],q_fb=[788,199],q_rt=[811,150],q_rb=[833,190],arch_F=[423,324],arch_R=[783,287])
add(11,'R',ws_base=[329,234],ws_top=[421,158],g_top=[184,289],g_low=[180,336])
add(12,'L',wc_R=[513,414],wc_F=[304,351],tiretop_R=[513,344],contact_R=[513,484],tiretop_F=[304,302],contact_F=[304,408],rw_top=[644,181],rw_base=[611,253],tl_top=[570,254],tl_low=[574,300],q_ft=[550,181],q_fb=[546,234],q_rt=[613,177],q_rb=[613,251],hatch_low=[629,354],arch_R=[513,321],arch_F=[304,283])
add(12,'R',rw_top=[785,176],rw_base=[848,246],hatch_low=[852,331])
add(13,'R',wc_R=[475,412],wc_F=[774,351],tiretop_R=[475,343],contact_R=[475,481],tiretop_F=[774,304],contact_F=[774,412],rw_top=[342,183],rw_base=[377,253],tl_top=[414,254],tl_low=[410,300],q_ft=[442,181],q_fb=[447,235],q_rt=[376,176],q_rb=[376,250],hatch_low=[359,354],arch_R=[475,320],arch_F=[774,283])
add(13,'L',rw_top=[219,181],rw_base=[159,247],hatch_low=[157,333])
# Single shared sparse landmark initializer. Not sampled from any previous mesh.
init={'h_out':[.73,.32,.40],'h_in':[.80,.20,.33],'g_top':[.82,.20,.375],'g_low':[.835,.17,.265],'bumper':[.82,.31,.14],'ws_base':[.33,.27,.445],'ws_top':[.10,.235,.625],'q_ft':[-.46,.265,.62],'q_fb':[-.49,.30,.455],'q_rt':[-.70,.26,.61],'q_rb':[-.78,.30,.44],'tl_top':[-.77,.33,.435],'tl_low':[-.81,.32,.34],'rw_top':[-.70,.245,.605],'rw_base':[-.82,.285,.45],'hatch_low':[-.83,.27,.20],'arch_F':[.5,.335,.315],'arch_R':[-.5,.335,.315]}
view={'1':[0,3.2,.08],'2':[85,3.8,.06],'3':[180,3.6,.07],'4':[-85,3.8,.06],'6':[-3,4.3,.08],'7':[80,4.1,.07],'8':[180,4.3,.08],'9':[-80,4.1,.07],'10':[-47,4.5,.13],'11':[47,4.5,.13],'12':[140,4.5,.13],'13':[-140,4.5,.13]}
# Revision 1: magnified image review, not copying projected positions.
revisions=[]
for i,name,new,why in [
 (7,'ws_base_L',[374,231],'Original pick was side-window/A-pillar foot, not windshield glass'),
 (7,'ws_top_L',[474,163],'Use outer windshield border, not side roof trim'),
 (9,'ws_base_R',[686,234],'Original pick was side-window foot, not windshield glass'),
 (9,'ws_top_R',[578,165],'Use windshield border, not side roof trim'),
 (10,'ws_top_L',[633,165],'Far windshield corner was placed on outer silver A-pillar'),
 (11,'ws_top_L',[532,169],'Outer windshield border at roof'),
 (11,'ws_top_R',[424,165],'Outer windshield border at roof'),
 (8,'rw_top_L',[397,179],'Consistent outer black glazing border, not transparent inner area'),
 (8,'rw_top_R',[642,178],'Consistent outer black glazing border'),
 (8,'rw_base_L',[378,250],'Consistent outer black glazing border'),
 (8,'rw_base_R',[668,251],'Consistent outer black glazing border'),
 (12,'rw_top_L',[609,176],'Consistent outer black glazing border'),
 (12,'rw_base_L',[593,241],'Consistent outer black glazing border'),
 (12,'rw_top_R',[824,166],'Consistent outer black glazing border'),
 (12,'rw_base_R',[850,237],'Consistent outer black glazing border'),
 (13,'rw_top_R',[380,176],'Consistent outer black glazing border'),
 (13,'rw_base_R',[377,245],'Consistent outer black glazing border'),
 (13,'rw_top_L',[217,166],'Consistent outer black glazing border'),
 (13,'rw_base_L',[159,233],'Consistent outer black glazing border')]:
 revisions.append({'image':i,'landmark':name,'initial':obs[i][name],'revised':new,'reason':why});obs[i][name]=new
(ROOT/'source/reconstruction/annotation-revisions.json').write_text(json.dumps(revisions,indent=2)+'\n')
allrows=json.loads(Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/references/inventory.json').read_text())
result={'annotation_method':'Manual pixel picks after image-grid inspection. Approximate; uncertainty 3px hubs, 5px tire tangencies, 6–8px body/glass corners. No automated feature matching.','scale':'Wheelbase=1 gauge; no manufacturer dimensions. Track/radius jointly estimated.','initial_landmarks':init,'camera_initialization':view,'images':allrows,'observations':{str(k):v for k,v in sorted(obs.items())},'excluded_image':{'5':'Interior panorama; no reliable common exterior anchors'},'excluded_features':['Open door glass/handles','Raised bonnet/hatch contours','Moving hatch-mounted lamp segments','Occluded hubs','View-dependent roof extrema','Reflections, badges and UI overlays']}
(ROOT/'source/reconstruction/observations.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':print(sum(len(v) for v in obs.values()),'manual observations across',len(obs),'cameras')

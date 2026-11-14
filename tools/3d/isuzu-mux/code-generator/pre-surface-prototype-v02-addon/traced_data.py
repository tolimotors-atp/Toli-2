"""Manual native-screenshot pixel traces, not calibrated CAD.
All coordinates remain auditable. X/Z anchors correct perspective only approximately;
3D depth bands are explicitly inferred from front/rear/three-quarter evidence.
"""
SOURCES={'side':'Screenshot From 2026-11-06 18-17-14.png','front':'Screenshot From 2026-11-06 18-17-10.png','rear':'Screenshot From 2026-11-06 18-17-18.png'}
# key: (source, pixel points, inferred depth fraction, closed)
TRACES={
 'SIDE_MASTER':('side',[(144,328),(172,276),(240,247),(335,224),(368,218),(425,170),(452,149),(525,132),(650,127),(775,132),(854,145),(895,194),(915,275),(928,335),(904,378)],.96,False),
 'SILL':('side',[(211,383),(348,377),(520,377),(686,377),(864,382)],.94,False),
 'SHOULDER':('side',[(193,290),(278,269),(355,276),(514,286),(678,282),(797,268),(904,278)],1,False),
 'BELT':('side',[(384,245),(500,246),(599,244),(735,238),(889,237)],.89,False),
 'BONNET_EDGE':('side',[(176,274),(239,247),(333,225),(368,218)],.88,False),
 'BONNET_CENTER':('side',[(171,263),(251,238),(332,217),(368,211)],0,False),
 'WINDSCREEN_CENTER':('side',[(368,211),(414,177),(451,149)],0,False),
 'A_PILLAR':('side',[(383,238),(423,190),(462,161)],.77,False),
 'ROOF_EDGE':('side',[(452,149),(525,132),(650,127),(775,132),(854,145)],.74,False),
 'ROOF_CENTER':('side',[(452,142),(525,126),(650,124),(775,129),(854,141)],0,False),
 'FRONT_WINDOW':('side',[(398,234),(450,177),(479,166),(587,163),(588,237)],.81,True),
 'REAR_WINDOW':('side',[(600,164),(716,165),(735,175),(728,210),(712,224),(600,237)],.82,True),
 'QUARTER_GLASS':('side',[(781,153),(849,155),(869,172),(884,215),(817,218),(791,203)],.74,True),
 'B_PILLAR':('side',[(591,161),(594,239)],.84,False),
 'C_PILLAR':('side',[(749,151),(759,235)],.82,False),
 'D_PILLAR':('side',[(863,144),(895,191),(907,239)],.73,False),
 'FRONT_ARCH':('side',[(203,379),(212,330),(239,295),(278,282),(319,290),(348,316),(365,377)],1,False),
 'FRONT_FENDER_CROWN':('side',[(186,336),(213,293),(246,272),(283,265),(323,277),(356,306),(374,358)],1,False),
 'FRONT_DOOR_RETURN':('side',[(367,269),(373,315),(374,373)],.96,False),
 'REAR_ARCH':('side',[(690,377),(701,325),(731,290),(773,279),(817,290),(847,323),(861,380)],1,False),
 'REAR_FENDER_CROWN':('side',[(673,352),(697,301),(737,271),(777,263),(822,277),(859,315),(878,365)],1,False),
 'REAR_QUARTER_RETURN':('side',[(858,243),(902,267),(922,319),(905,373)],.94,False),
 'BONNET_FRONT':('front',[(401,295),(449,308),(493,313),(543,314)],-.47,False),
 'HEADLIGHT':('front',[(399,297),(447,313),(491,334),(482,346),(435,337),(407,322)],-.46,True),
 'GRILLE_UPPER':('front',[(484,315),(511,318),(543,318)],-.50,False),
 'GRILLE_SURROUND':('front',[(474,320),(497,337),(505,350),(543,351)],-.50,False),
 'GRILLE_LOWER':('front',[(489,365),(510,375),(543,375)],-.50,False),
 'FRONT_LOWER_OPENING':('front',[(469,390),(489,415),(543,417)],-.50,False),
 'FRONT_BUMPER':('front',[(388,334),(384,389),(403,431),(453,440),(543,441)],-.49,False),
 'WINDSCREEN_BOTTOM':('front',[(406,242),(467,248),(543,249)],-.19,False),
 'WINDSCREEN_TOP':('front',[(430,173),(483,168),(543,168)],-.08,False),
 'FRONT_ROOF':('front',[(415,156),(475,137),(543,132)],.02,False),
 'REAR_GLASS':('rear',[(411,182),(455,180),(528,180),(528,257),(385,250),(396,207)],.43,True),
 'TAIL_LAMP':('rear',[(365,257),(389,269),(447,278),(425,300),(361,298),(359,281)],.48,True),
 'TAILGATE':('rear',[(388,303),(391,341),(412,356),(528,358)],.49,False),
 'REAR_BUMPER':('rear',[(363,356),(363,388),(386,411),(528,413)],.50,False),
 'REAR_LOWER_TRIM':('rear',[(389,386),(448,395),(528,397)],.50,False),
}
# Hand readings have roughly 5–10 px uncertainty. These are not solved camera poses.
ANCHORS={'side_x':[(144,-.5),(284,'front_axle'),(776,'rear_axle'),(928,.5)],'side_z':[455,124],'front_center':543,'front_half_body':165,'front_z':[480,132],'rear_center':528,'rear_half_body':173,'rear_z':[476,130]}

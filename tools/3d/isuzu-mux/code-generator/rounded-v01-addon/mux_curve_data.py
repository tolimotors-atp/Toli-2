"""Normalized MU-X curve constraints: X/length, Y/half-width, Z/height.
Visual approximations from the older silver family; not calibrated CAD.
14/21: side;10/27: bonnet/front;18/31/35: quarter/rear.
Each named polyline is a purpose-specific Bezier control polygon.
"""
CURVES={
'CURVE_SIDE_MASTER':[(-.5,.84,.47),(-.46,.95,.58),(-.35,.99,.64),(-.19,.94,.69),(-.08,.77,.93),(.04,.75,.99),(.28,.74,.98),(.39,.71,.91),(.47,.84,.70),(.5,.88,.48)],
'CURVE_BONNET_CENTER':[(-.48,0,.59),(-.39,0,.64),(-.28,0,.67),(-.18,0,.69)],
'CURVE_BONNET_LEFT_EDGE':[(-.48,.74,.56),(-.40,.88,.61),(-.29,.88,.65),(-.18,.85,.67)],
'CURVE_BONNET_FRONT':[(-.48,-.74,.56),(-.49,0,.59),(-.48,.74,.56)],
'CURVE_BONNET_REAR':[(-.18,-.85,.67),(-.18,0,.69),(-.18,.85,.67)],
'CURVE_SHOULDER':[(-.43,.96,.55),(-.30,1,.62),(-.17,.97,.65),(.08,.97,.66),(.30,1,.67),(.44,.95,.65)],
'CURVE_BELT':[(-.18,.87,.69),(.02,.88,.70),(.24,.88,.71),(.42,.84,.70)],
'CURVE_LOWER_BODY':[(-.43,.91,.26),(-.18,.92,.25),(.05,.93,.27),(.26,.94,.29),(.46,.89,.28)],
'CURVE_SILL':[(-.40,.88,.15),(-.18,.90,.15),(.10,.90,.15),(.40,.86,.17)],
'CURVE_WINDSCREEN_BOTTOM':[(-.18,-.83,.69),(-.19,0,.70),(-.18,.83,.69)],
'CURVE_WINDSCREEN_TOP':[(-.075,-.70,.94),(-.08,0,.96),(-.075,.70,.94)],
'CURVE_A_PILLAR_LEFT':[(-.18,.86,.69),(-.13,.79,.81),(-.075,.72,.95)],
'CURVE_ROOF_CENTER':[(-.08,0,.96),(.04,0,1),(.25,0,.995),(.37,0,.96)],
'CURVE_ROOF_LEFT_EDGE':[(-.075,.72,.95),(.04,.74,.97),(.25,.73,.965),(.37,.68,.93)],
'CURVE_WINDOW_UPPER':[(-.13,.79,.81),(-.05,.76,.93),(.12,.76,.93),(.29,.74,.92),(.37,.71,.88)],
'CURVE_WINDOW_LOWER':[(-.17,.87,.71),(.02,.88,.72),(.20,.88,.73),(.37,.85,.74)],
'CURVE_QUARTER_GLASS_UPPER':[(.27,.75,.92),(.33,.72,.91),(.37,.71,.88)],
'CURVE_QUARTER_GLASS_LOWER':[(.27,.87,.73),(.34,.85,.74),(.40,.80,.76)],
'CURVE_QUARTER_GLASS_REAR':[(.37,.71,.88),(.39,.76,.82),(.40,.80,.76)],
'CURVE_D_PILLAR_LEFT':[(.37,.68,.93),(.41,.73,.85),(.45,.84,.71)],
'CURVE_REAR_QUARTER_RETURN':[(.30,1,.67),(.41,.97,.65),(.48,.88,.58),(.5,.83,.38)],
'CURVE_REAR_GLASS':[(.39,-.64,.91),(.38,0,.94),(.39,.64,.91),(.46,.76,.74),(.47,0,.72),(.46,-.76,.74)],
'CURVE_TAILGATE':[(.47,-.77,.73),(.49,0,.72),(.47,.77,.73),(.50,.80,.35),(.50,0,.33),(.50,-.80,.35)],
'CURVE_REAR_BUMPER':[(.48,-.90,.34),(.5,0,.32),(.48,.90,.34)],
'CURVE_HEADLIGHT':[(-.475,.45,.59),(-.43,.92,.64),(-.46,.96,.53),(-.49,.55,.51)],
'CURVE_GRILLE_OUTER':[(-.492,-.53,.58),(-.50,0,.59),(-.492,.53,.58),(-.50,.44,.43),(-.50,-.44,.43)],
'CURVE_GRILLE_INNER':[(-.501,-.42,.53),(-.502,0,.54),(-.501,.42,.53),(-.503,.34,.46),(-.503,-.34,.46)],
'CURVE_FRONT_BUMPER':[(-.47,-.95,.40),(-.50,0,.38),(-.47,.95,.40)],
'CURVE_TAILLAMP_LEFT':[(.44,.82,.68),(.47,.92,.65),(.49,.85,.55),(.498,.48,.58)],
}
CLOSED={'CURVE_REAR_GLASS','CURVE_TAILGATE','CURVE_HEADLIGHT','CURVE_GRILLE_OUTER','CURVE_GRILLE_INNER','CURVE_TAILLAMP_LEFT'}
# Curves spanning the centreline are already bilateral. These others use one side only.
MIRROR={name for name,points in CURVES.items() if any(p[1]>0 for p in points) and all(p[1]>=0 for p in points)}
SOURCES={'front':['18-17-10','18-17-27'],'side':['18-17-14','18-17-21'],'rear':['18-17-18','18-17-31','18-17-35']}

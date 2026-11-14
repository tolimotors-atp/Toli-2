/** V02 authored interpretation of supplied images. No calibrated CAD/depth claim. X front negative, Z up. */
export const dimensions = { length:4.825, width:1.860, height:1.860, wheelbase:2.845, tireDiameter:.764 } as const;
export type Point = readonly [number,number,number];
export const axles = [-1.370,1.475] as const;
export const track = 1.570;
export const archRadius = .437;
export const normalizedLandmarks = {
  side:{source:'MUX-012',file:'Screenshot From 2026-11-06 18-17-14.png',points:{nose:[.140,.470],tail:[.894,.470],frontAxle:[.278,.648],rearAxle:[.755,.648],cowl:[.350,.355],aRoof:[.445,.235],roofRear:[.782,.221],sill:[.470,.652],quarterFront:[.737,.284],quarterRear:[.830,.282]}},
  front:{source:'MUX-011',file:'Screenshot From 2026-11-06 18-17-10.png',points:{roof:[.499,.210],cowl:[.502,.415],hoodEdge:[.503,.522],grilleTop:[.503,.543],grilleBottom:[.503,.637],leftBody:[.337,.527],rightBody:[.681,.527],tireGround:[.502,.820]}},
  rear:{source:'MUX-013',file:'Screenshot From 2026-11-06 18-17-18.png',points:{roof:[.500,.238],glassBase:[.500,.443],lampLeft:[.365,.483],lampRight:[.637,.483],hatchBase:[.500,.634],bumperBase:[.500,.710]}}
} as const;
// Nonuniform X/L stations. Bands are half-width ratios; Z values are height-normalized.
export const bodyStations = [
 // x, sill-width, low-width, max-width, shoulder-width, belt-width, shoulder-Z
 [0,.75,.80,.86,.83,.77,.511], [.028,.84,.91,.96,.94,.87,.548],
 [.085,.87,.94,.98,.99,.91,.589], [.151,.87,.96,1,1,.92,.616],
 [.2161,.88,.97,1,1,.93,.637], [.258,.89,.95,.99,.97,.93,.653],
 [.295,.89,.94,.97,.95,.91,.656], [.340,.89,.94,.97,.95,.91,.648],
 [.385,.89,.93,.96,.94,.90,.640], [.440,.89,.93,.96,.94,.90,.638],
 [.510,.89,.93,.96,.94,.90,.640], [.570,.89,.94,.97,.95,.91,.645],
 [.650,.89,.95,.99,.98,.93,.655], [.720,.89,.97,1,1,.94,.665],
 [.8057,.89,.97,1,1,.94,.662], [.850,.88,.96,1,.99,.93,.650],
 [.900,.86,.94,.99,.97,.91,.632], [.950,.83,.91,.96,.94,.88,.610],
 [1,.76,.84,.90,.88,.82,.584]
] as const;
// Authored metres, centralized here. Curves follow visible form; depth between views is estimated.
export const curves = {
 bonnetCentre:[[-2.30,0,1.025],[-2.08,0,1.105],[-1.55,0,1.205],[-1.18,0,1.230],[-1.00,0,1.240]],
 bonnetSide:[[-2.25,.64,1.005],[-2.03,.67,1.080],[-1.53,.68,1.180],[-1.18,.68,1.200],[-1.00,.69,1.215]],
 fenderCrown:[[-2.26,.78,1.02],[-1.92,.88,1.16],[-1.37,.91,1.23],[-1.12,.87,1.235],[-.95,.85,1.230]],
 roofCentre:[[-.57,0,1.755],[-.32,0,1.800],[.65,0,1.815],[1.50,0,1.800],[1.99,0,1.745]],
 roofSide:[[-.57,.695,1.715],[-.32,.715,1.760],[.65,.725,1.775],[1.50,.735,1.760],[1.99,.710,1.705]],
 shoulder:[[-2.30,.80,1.03],[-1.4,.91,1.21],[-.6,.86,1.23],[.6,.87,1.25],[1.48,.91,1.23],[2.25,.84,1.12]],
 belt:[[-.88,.82,1.25],[-.3,.84,1.255],[.5,.85,1.26],[1.35,.86,1.27],[2.20,.80,1.22]],
 lowerBody:[[-2.22,.78,.42],[-.90,.85,.40],[.45,.84,.38],[1.05,.86,.40],[2.25,.78,.43]],
 sill:[[-.90,.835,.36],[0,.835,.35],[1.03,.85,.36]],
 rearShoulder:[[1.00,.88,1.25],[1.475,.93,1.24],[1.95,.90,1.20],[2.32,.82,1.10]],
 // Side envelopes use x/z; y is projected onto a continuous greenhouse cross-section.
 cabinOutline:[[-1.08,0,1.19],[-.89,0,1.44],[-.55,0,1.73],[-.29,0,1.78],[1.60,0,1.750],[1.99,0,1.705],[2.27,0,1.20],[1.92,0,1.17]],
 frontWindow:[[-.96,0,1.235],[-.57,0,1.700],[-.35,0,1.725],[.27,0,1.728],[.28,0,1.220]],
 rearWindow:[[.385,0,1.230],[.38,0,1.73],[1.10,0,1.725],[1.20,0,1.690],[1.18,0,1.340],[1.02,0,1.265]],
 quarterWindow:[[1.46,0,1.275],[1.36,0,1.700],[1.95,0,1.675],[2.030,0,1.280]],
 windscreen:[[-1.00,-.805,1.235],[-.61,-.685,1.72],[-.61,.685,1.72],[-1.00,.805,1.235]],
 rearGlass:[[2.255,-.79,1.220],[1.990,-.710,1.705],[1.990,.710,1.705],[2.255,.79,1.220]],
 grille:[[-2.31,-.58,1.035],[-2.31,.58,1.035],[-2.38,.40,.765],[-2.38,-.40,.765]],
 headlamp:[[-2.30,.59,1.01],[-2.14,.86,1.04],[-2.15,.87,.91],[-2.35,.61,.88]],
 grilleUpper:[[-2.32,-.53,1.015],[-2.32,.53,1.015],[-2.37,.46,.945],[-2.37,-.46,.945]],
 grilleLower:[[-2.37,-.48,.895],[-2.37,.48,.895],[-2.39,.37,.815],[-2.39,-.37,.815]],
 lowerOpening:[[-2.405,-.57,.71],[-2.405,.57,.71],[-2.38,.52,.53],[-2.38,-.52,.53]],
 frontBumper:[[-2.39,-.82,.78],[-2.4125,-.60,.47],[-2.4125,.60,.47],[-2.39,.82,.78]],
 tailLamp:[[2.20,.88,1.21],[2.38,.60,1.18],[2.39,.47,1.03],[2.25,.87,1.01]],
 tailgate:[[2.32,-.68,1.23],[2.39,.68,1.23],[2.39,.61,.60],[2.39,-.61,.60]],
 rearBumper:[[2.35,-.82,.68],[2.4125,-.60,.43],[2.4125,.60,.43],[2.35,.82,.68]]
} satisfies Record<string,Point[]>;
export const primaryViews = ['front','front-left','left','rear-left','rear','rear-right','right','front-right','overhead'] as const;
export type MuxView = typeof primaryViews[number];

// Z, half-width, X: shared nose/hatch boundaries for side skins and end surfaces.
export const fasciaSections={
 front:[[.39,.78,-2.30],[.48,.84,-2.4125],[.66,.88,-2.39],[.80,.89,-2.34],[.95,.89,-2.32],[1.04,.89,-2.30]],
 rear:[[.39,.82,2.32],[.48,.86,2.4125],[.67,.86,2.37],[.92,.85,2.33],[1.15,.85,2.30],[1.22,.79,2.255]]
} satisfies Record<string,Point[]>;

export const identityIteration=3;

export const shapeInfluences=[
 {name:'front-fender',x:axles[0],sigma:.38,upperLift:.045,lateralLift:.045},
 {name:'rear-quarter',x:axles[1],sigma:.44,upperLift:.032,lateralLift:.035}
] as const;

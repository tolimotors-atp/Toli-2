"""Approximate paired image landmarks, not camera calibration.
Width fractions use the visible body excluding mirrors. Uncertainty includes yaw/perspective.
"""
FRONT_IMAGE='Screenshot From 2026-11-06 18-17-10.png'
REAR_IMAGE='Screenshot From 2026-11-06 18-17-18.png'
# label, existing curve/probe, left/right pixels, sampled image row, bounded fit target
FRONT=[
 ('Body width','BODY',(377,717),335,1.0),
 ('Bonnet leading width','TRACE_BONNET_FRONT',(400,690),297,.853),
 ('Lower windscreen width','TRACE_WINDSCREEN_BOTTOM',(402,664),240,.780),
 ('Headlamp outer span','LAMP_OUTER',(400,692),305,.860),
 ('Headlamp inner span','LAMP_INNER',(487,633),330,.430),
 ('Upper grille width','TRACE_GRILLE_UPPER',(489,627),320,.406),
 ('Grille surround width','TRACE_GRILLE_SURROUND',(455,655),330,.588),
 ('Lower grille width','TRACE_GRILLE_LOWER',(492,627),350,.397),
 ('Lower opening width','TRACE_FRONT_LOWER_OPENING',(462,642),385,.530),
 ('Bumper width','TRACE_FRONT_BUMPER',(385,715),391,.970),
 ('Tire-centre span','TIRES',(399,687),445,None)]
REAR=[
 ('Body width','BODY',(359,694),290,1.0),
 ('Rear roof termination','ROOF',(412,642),150,None),
 ('Rear glass lower width','TRACE_REAR_GLASS',(383,670),245,.850),
 ('Lower glass side band','GLASS_BAND',(359,383),245,None),
 ('Shoulder termination','SHOULDER',(365,690),280,None),
 ('Lamp outer span','LAMP_OUTER',(360,693),280,.980),
 ('Lamp inner span','LAMP_INNER',(447,608),280,.480),
 ('Tailgate width','TRACE_TAILGATE',(393,663),330,None),
 ('Quarter maximum width','QUARTER',(359,694),310,None),
 ('Upper bumper width','TRACE_REAR_BUMPER',(366,687),375,.955),
 ('Lower bumper width','LOWER_BUMPER',(384,671),405,.855)]
# Each join names the observed contour and existing control, rather than inventing new structure.
EVIDENCE={
 'J01':{'images':[FRONT_IMAGE,'Screenshot From 2026-11-06 18-17-27.png'],'contour':'Broad hood crown rolling into the painted fender above the front arch','curves':['SECTION_BONNET_0..4','FENDER_TO_BONNET','TRACE_FRONT_FENDER_CROWN'],'parameter':'bonnet_roll_drop=.095; roll_height_drop=.026; fender_bridge_mid_drop=.035','v03_difference':'Uniform .12 edge drop made the outer roll too steep and detached from the crown'},
 'J02':{'images':['Screenshot From 2026-11-06 18-17-27.png','Screenshot From 2026-11-06 18-17-14.png'],'contour':'Painted cowl/A-root outside the narrower lower screen','curves':['TRACE_BONNET_EDGE','TRACE_A_PILLAR','TRACE_WINDSCREEN_BOTTOM','COWL_ROOT_BLEND'],'parameter':'cowl_half_width=.790; lower_screen_width_fraction=.780','v03_difference':'Glass and painted cowl shared one excessive width; no visible frame allowance'},
 'J04':{'images':['Screenshot From 2026-11-06 18-17-14.png','Screenshot From 2026-11-06 18-17-31.png',REAR_IMAGE],'contour':'Raked quarter-glass termination and defined painted D-frame under the rear roof','curves':['TRACE_D_PILLAR','TRACE_QUARTER_GLASS','REAR_ROOF_GLASS_RETURN'],'parameter':'D_middle_half_width=.735; D_base_half_width=.820; quarter_glass_handle_length=.72 of V03','v03_difference':'Generic bowed D-frame; rounded glass-corner handles dilute the visible angular cut'},
 'J05':{'images':['Screenshot From 2026-11-06 18-17-14.png','Screenshot From 2026-11-06 18-17-31.png'],'contour':'Shoulder rises progressively into a substantial but bounded rear arch crown','curves':['TRACE_SHOULDER','TRACE_REAR_FENDER_CROWN','SHOULDER_TO_QUARTER'],'parameter':'rear_crown_delta_peak=-.006; asymmetric falloff=.48/.68','v03_difference':'Local crown and shoulder have competing peaks'},
 'J06':{'images':['Screenshot From 2026-11-06 18-17-31.png',REAR_IMAGE],'contour':'Wide outer lamp wrapping into quarter, tapering inward at hatch','curves':['TRACE_TAIL_LAMP','TRACE_REAR_QUARTER_RETURN','QUARTER_TO_LAMP'],'parameter':'lamp_outer_fraction=.980; lamp_inner_fraction=.480; lamp_outer_X=2.065/2.09','v03_difference':'Lamp cut nearly correct in rear projection but insufficiently composed with the side return'},
 'J07':{'images':['Screenshot From 2026-11-06 18-17-31.png',REAR_IMAGE],'contour':'Broad upper bumper tapering toward the lower undercut','curves':['TRACE_REAR_BUMPER','SECTION_UPPER_BUMPER','SECTION_LOWER_BUMPER','REAR_BUMPER_RETURN'],'parameter':'upper_width_fraction=.955; lower_width_fraction=.855; bounded common-handle balance ±15%','v03_difference':'Upper/lower bumper widths too narrow and common continuation retains a curvature step'},
 'J08':{'images':['Screenshot From 2026-11-06 18-17-31.png',REAR_IMAGE],'contour':'Rear glass flares toward its lower corners above the lamp/hatch band','curves':['TRACE_REAR_GLASS','TRACE_D_PILLAR','D_TO_REAR_GLASS','SECTION_REAR_GLASS'],'parameter':'lower_glass_width_fraction=.850; D base half-width=.820; existing six glass controls reordered into open half-perimeter','v03_difference':'Lower rear glass too narrow; closing each mirrored half through the centre creates a false seam absent from the photograph'}}

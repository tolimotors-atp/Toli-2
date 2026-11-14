"""MU-X visual constraints, not CAD: older silver reference family only.
X normalized to vehicle length, front negative. Heights/widths are metres at baseline.
Front/bonnet: 18-17-10,27; side/arches:14,21; cabin/rear:18,31,35.
Perspective readings guide profiles; fitted 3D sections remain VISUAL APPROXIMATIONS.
"""
# x, half-width, body top, shoulder height, door convexity
BODY=[(-.50,.78,.91,.75,.01),(-.47,.86,1.06,.90,.015),(-.40,.91,1.16,1.00,.03),(-.30,.93,1.22,1.08,.05),(-.22,.90,1.25,1.12,.035),(-.14,.89,1.29,1.15,.025),(.02,.90,1.29,1.16,.03),(.20,.91,1.30,1.17,.045),(.30,.93,1.30,1.16,.055),(.40,.91,1.28,1.14,.04),(.47,.86,1.23,1.08,.025),(.50,.82,1.14,.97,.015)]
# x, lower halfwidth, upper halfwidth, lower edge, roof center
CABIN=[(-.18,.76,.68,1.28,1.30),(-.13,.78,.69,1.29,1.48),(-.065,.77,.69,1.29,1.77),(.015,.76,.70,1.29,1.84),(.15,.76,.70,1.30,1.86),(.28,.75,.68,1.31,1.85),(.36,.73,.65,1.31,1.79),(.425,.70,.61,1.29,1.63),(.465,.67,.57,1.26,1.32)]
ARCH={'front_clearance':.075,'rear_clearance':.060,'top_clearance':.070,'flare':.035,'lower_termination':.20}
# Side window envelopes x,z (m); actual perspective-derived layout, not glass CAD.
WINDOWS=[ [(-.65,1.34),(-.25,1.73),(.14,1.74),(.14,1.34)],[(.23,1.34),(.23,1.74),(.99,1.72),(1.04,1.36)],[(1.18,1.37),(1.12,1.70),(1.57,1.62),(1.79,1.40)] ]

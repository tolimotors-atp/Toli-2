# V03 rear error map — BEFORE geometry corrections

Compared V02 rear and rear-right clay renders with full-resolution silver 18-17-18 (direct rear), 18-17-31 (rear-left quarter), 18-17-35 (opposite rear quarter), and side 18-17-14/18-17-21. Compatible red Screenshot 2026-11-08 213459/213502/213507 and Screenshot (4)/(5)/(6)/(7) are secondary wrap checks; trim and colour do not override silver geometry.

| Region | Reference | V02 error | Cause | Local correction |
|---|---|---|---|---|
| Roof width | Softly narrowed rear roof with slim lip | Roof ends abruptly in a slab | roofSide last span / absent lip | Retain forward roof; coordinate local trailing edge and shallow lip |
| D-pillars | Relatively narrow curved surround | Thick diagonal wedge | cabinOutline / quarterWindow termination | Narrow surround, coordinated glass side return |
| Rear glass | Tapered rounded trapezoid, lower edge curved | Rectangular-looking ruled screen | screen(true) linear corners | Curved top/bottom/side Coons boundaries |
| Shoulder | Continuous side-to-lamp sweep | Flat band ending abruptly | rear section upper bands | Local upper taper and compound quarter crown |
| Quarter width | Full arch mass narrowing into corner | Flat side next to wheel | section width bands / rear influence | Local mid-band bulge and separate belt taper |
| Tail lamp | Swept tailgate section wrapping onto quarter | Flat rear-facing four-corner patch | fasciaEnvelope ignores authored X | Curve-driven upper/lower/inner/outer loft with actual X-depth |
| Tailgate | Glass, upper hatch, lamp level, main recess differ in depth | Blank barrel-like vertical slab | rear fascia sparse Z profile and narrow Gaussian recess | Dedicated depth rows and broad controlled plate/hatch recess |
| Bumper | Raised step, projecting face, lower dark return | Same smooth surface as hatch | profile .48-.76 insufficient hierarchy | Independent step/face/lower rows; restrained lower inset |
| Bumper corners | Broad continuous round return to quarter | Corner shape/tangents wrong | fixed .14*w^3 corner | Explicit mirrored cross-section corner curves controlling X/Y/Z |
| Lower rear | Broad undercut and modest lower trim | Featureless rounded bottom | lower profile and absent undercut | Supported simple lower return; no invented diffuser |
| Taper | Gradual rear-quarter/glass/hatch relation | Generic thick cabin and rear barrel | unrelated surface endpoints | Same rear profile controls side terminal and rear face; unchanged cameras |

No global body restart, no wheel/forward cowl/dimension changes. V02 source and renders preserved before this pass. All figures remain uncalibrated visual estimates.

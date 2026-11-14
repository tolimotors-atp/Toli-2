import bpy,json
from .geometry.flow_cage import JOIN_CURVES,JOIN_STATION
from .geometry.reference_cage import COL

def join_visibility(self,context):
 s=context.scene;col=bpy.data.collections.get(COL)
 if not col:return
 names=[COL,'TOLI_CAGE_SUPPORT','TOLI_MUX_REFERENCES'];objects=[o for n in names if (c:=bpy.data.collections.get(n)) for o in c.objects]
 if 'v03_debug_states' in s:
  for name,state in json.loads(s['v03_debug_states']).items():
   if (o:=bpy.data.objects.get(name)):o.hide_viewport,o.hide_render=state
 if self.join_debug!='OFF':
  if 'v03_debug_states' not in s:s['v03_debug_states']=json.dumps({o.name:[o.hide_viewport,o.hide_render] for o in objects})
  targets=JOIN_CURVES[self.join_debug];station='SLICE_'+JOIN_STATION[self.join_debug]
  for o in objects:
   allowed=o.name in targets or o.name.removesuffix('_R') in targets or o.name==station
   if o.name.startswith('CAGE_WHEEL'):allowed=(o.location.x<0)==(self.join_debug in ['J01','J02','J03'])
   o.hide_viewport=not allowed;o.hide_render=not allowed
 else:
  if 'v03_debug_states' in s:del s['v03_debug_states']
 combs=bpy.data.collections.get('TOLI_CAGE_COMBS')
 if combs:
  for o in combs.objects:
   visible=self.show_curvature_combs and (self.join_debug=='OFF' or o.get('comb_source') in JOIN_CURVES[self.join_debug])
   o.hide_viewport=not visible;o.hide_render=not visible

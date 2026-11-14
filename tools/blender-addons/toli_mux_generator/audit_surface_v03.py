import bpy,sys,json,os
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'tools/blender-addons'))
import toli_mux_generator as addon
from toli_mux_generator.geometry.surface_patch import build,SURFACES
from toli_mux_generator.parameters import values
addon.register();bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v03.blend'))
s=bpy.context.scene;p=values(s);R=P/'tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03';out={};sections={}
for version in [2,3]:
 build(s,p,version=version);zones={};section_rows={}
 for o in bpy.data.collections[SURFACES].objects:
  labels=json.loads(o['patch_labels']);adj=[[] for _ in o.data.vertices];edges=[[] for _ in o.data.vertices];edge_faces={tuple(sorted(e.vertices)):[] for e in o.data.edges}
  for f in o.data.polygons:
   label=labels[o.data.attributes['patch_id'].data[f.index].value]
   for v in f.vertices:adj[v].append(label)
   for key in f.edge_keys:edge_faces[tuple(sorted(key))].append(f.index)
  for e in o.data.edges:
   for v in e.vertices:edges[v].append(e)
  audit=[]
  for v in o.data.vertices:
   boundary=any(len(edge_faces[tuple(sorted(e.vertices))])==1 for e in edges[v.index]);valence=len(edges[v.index])
   if (not boundary and valence!=4) or (boundary and valence not in [2,3]):
    audit.append({'id':v.index,'co':list(v.co),'valence':valence,'boundary':boundary,'patches':sorted(set(adj[v.index])),'reflection_sensitive':any(t in ['bonnet_center','bonnet_outer','fender_upper','rear_roof','D_surface','quarter_upper','quarter_crown'] for t in adj[v.index])})
  zones[o['zone']]={'extraordinary_vertices':audit,'count':len(audit),'sensitive_count':sum(v['reflection_sensitive'] for v in audit),'all_quad':all(len(f.vertices)==4 for f in o.data.polygons)}
  cuts={'A':[(0,x) for x in [-.835,-.795,-.755,-.71]],'B':[(2,z) for z in [1.38,1.55,1.70]],'C':[]}[o['zone']];rows=[]
  for axis,position in cuts:
   row={'axis':axis,'position':position}
   for state in ['base','evaluated']:
    if state=='evaluated':ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
    else:me=o.data
    segments=[]
    for face in me.polygons:
     ps=[me.vertices[i].co for i in face.vertices];cross=[]
     for a,b in zip(ps,ps[1:]+ps[:1]):
      if (a[axis]-position)*(b[axis]-position)<0:
       v=a.lerp(b,(position-a[axis])/(b[axis]-a[axis]))
       if v.y<0 and (o['zone']=='A' or v.x>1.85):cross.append(list(v))
     if len(cross)==2:segments.append(cross)
    row[state]=segments
    if state=='evaluated':ev.to_mesh_clear()
   rows.append(row)
  section_rows[o['zone']]=rows
 out[f'V0{version}']=zones;sections[f'V0{version}']=section_rows
(R/'pole-audit.json').write_text(json.dumps(out,indent=2));(R/'root-and-pillar-sections.json').write_text(json.dumps(sections,indent=2))
assert all(v['all_quad'] for version in out.values() for v in version.values())
print(json.dumps({version:{z:{k:v[k] for k in ['count','sensitive_count']} for z,v in zones.items()} for version,zones in out.items()}),flush=True);os._exit(0)

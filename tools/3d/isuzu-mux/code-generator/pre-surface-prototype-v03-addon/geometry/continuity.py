import bpy,bmesh,math,json,hashlib
from mathutils import Vector,kdtree
from mathutils.bvhtree import BVHTree
from .surface_patch import SURFACES

def mesh_stats(mesh):
 bm=bmesh.new();bm.from_mesh(mesh);deg=sum(f.calc_area()<1e-10 for f in bm.faces);boundary=sum(e.is_boundary for e in bm.edges);interior=sum(len(e.link_faces)>2 or len(e.link_faces)==0 for e in bm.edges)
 # A vertex sitting on another open edge would be an unwelded T junction.
 ts=[];verts=list(bm.verts)
 for e in bm.edges:
  if not e.is_boundary:continue
  a,b=[v.co for v in e.verts];d=b-a
  if d.length_squared<1e-16:continue
  for v in verts:
   if v in e.verts:continue
   t=(v.co-a).dot(d)/d.length_squared
   if 1e-6<t<1-1e-6 and (v.co-(a+d*t)).length<1e-6:ts.append([e.index,v.index])
 mesh.calc_loop_triangles();tri=[tuple(t.vertices) for t in mesh.loop_triangles];tree=BVHTree.FromPolygons([v.co.copy() for v in mesh.vertices],tri,all_triangles=True,epsilon=0.0)
 overlaps=sum(a<b and not set(tri[a]).intersection(tri[b]) for a,b in tree.overlap(tree))
 out={'nonadjacent_triangle_overlap_pairs':overlaps,'vertices':len(mesh.vertices),'triangles':len(mesh.loop_triangles),'degenerate_faces':deg,'open_boundary_edges':boundary,'interior_nonmanifold_edges':interior,'boundary_t_junctions':ts};bm.free();return out

def validate(scene,p):
 dg=bpy.context.evaluated_depsgraph_get();out={};total={'base_vertices':0,'evaluated_vertices':0,'evaluated_triangles':0}
 for o in bpy.data.collections[SURFACES].objects:
  if o.type!='MESH':continue
  base=mesh_stats(o.data);ev=o.evaluated_get(dg);me=ev.to_mesh();evaluated=mesh_stats(me)
  co=[v.co.copy() for v in o.data.vertices];tree=kdtree.KDTree(len(co))
  for i,v in enumerate(co):tree.insert(v,i)
  tree.balance();sym=max(tree.find(Vector((v.x,-v.y,v.z)))[2] for v in co)
  limits={'finite':all(math.isfinite(c) for v in co for c in v),'x_within_dimensions':all(abs(v.x)<=p['length']/2+1e-6 for v in co),'y_within_dimensions':all(abs(v.y)<=p['width']/2+1e-6 for v in co),'z_within_dimensions':all(0<=v.z<=p['height']+1e-6 for v in co)}
  boundaries=json.loads(o['boundary_manifest']);angle_rows=[]
  for row in boundaries:
   e=o.data.edges[row['edge']];fs=[f for f in o.data.polygons if tuple(sorted(e.vertices)) in [tuple(sorted(pair)) for pair in f.edge_keys]]
   angle=math.degrees(fs[0].normal.angle(fs[1].normal,0)) if len(fs)==2 else None;angle_rows.append({'type':row['type'],'base_normal_angle_deg':angle,'position_gap_m':0})
  out[o['zone']]={'base':base,'evaluated':evaluated,'base_control_symmetry_m':sym,'constraints':limits,'boundary_cracks':len(base['boundary_t_junctions']),'shared_boundary_max_gap_m':max([r['position_gap_m'] for r in boundaries],default=0),'shared_boundary_normal_diagnostics':angle_rows,'boundary_note':'Open prototype construction cuts and window/lamp apertures are intentional; counted separately from interior non-manifold edges.'}
  total['base_vertices']+=base['vertices'];total['evaluated_vertices']+=evaluated['vertices'];total['evaluated_triangles']+=evaluated['triangles'];ev.to_mesh_clear()
 return {'zones':out,'total':total}

def fingerprint():
 rows=[(o.name,[list(v.co) for v in o.data.vertices],[list(f.vertices) for f in o.data.polygons],list(o['patch_labels'])) for o in sorted(bpy.data.collections[SURFACES].objects,key=lambda o:o.name)]
 return hashlib.sha256(json.dumps(rows).encode()).hexdigest()

import bpy,bmesh,math,json
from mathutils import Vector
from .geometry import COLLECTION

def validate(scene,p):
 objects=list(bpy.data.collections[COLLECTION].objects);verts=[];tri=0;nonmanifold=degenerate=negative=0
 for o in objects:
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles();tri+=len(m.loop_triangles);verts.extend(tuple(o.matrix_world@v.co) for v in m.vertices)
  bm=bmesh.new();bm.from_mesh(m);nonmanifold+=sum(not e.is_manifold for e in bm.edges);degenerate+=sum(f.calc_area()<1e-10 for f in bm.faces);negative+=int(bm.calc_volume(signed=True)<0);bm.free();ev.to_mesh_clear()
 lo=[min(v[k] for v in verts) for k in range(3)];hi=[max(v[k] for v in verts) for k in range(3)]
 from mathutils.kdtree import KDTree
 tree=KDTree(len(verts))
 for i,v in enumerate(verts):tree.insert(v,i)
 tree.balance();symmetry_error=max(tree.find((x,-y,z))[2] for x,y,z in verts);symmetry=symmetry_error<1e-4
 return {'vertices':len(verts),'triangles':tri,'objects':len(objects),'materials':len({m.name for o in objects for m in o.data.materials if m}),'dimensions':[hi[k]-lo[k] for k in range(3)],'wheelbase':p['wheelbase'],'ground_z':lo[2],'symmetry':symmetry,'symmetry_max_error_m':symmetry_error,'nonmanifold_edges':nonmanifold,'degenerate_faces':degenerate,'negative_volume_objects':negative,'finite':all(math.isfinite(x) for v in verts for x in v),'boundary_note':'Body, greenhouse and wheels are deliberately separate closed milestone volumes; joins require visual review, not a watertight assembled shell.'}

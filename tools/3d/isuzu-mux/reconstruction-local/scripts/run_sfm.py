from pathlib import Path
import json,time,sqlite3,hashlib
import pycolmap as p
import cv2,numpy as np
r=Path(__file__).resolve().parents[1]
# Conservative ROI, not precision segmentation: keep all roof/tires in the oblique rear views.
for name,box in [('18-17-31.png',(250,60,880,440)),('18-17-35.png',(120,50,900,445))]:
 a=np.zeros((465,1028),np.uint8);x1,y1,x2,y2=box;a[y1:y2,x1:x2]=255
 cv2.imwrite(str(r/'masks'/f'{name}.png'),a)
reader=p.ImageReaderOptions();reader.camera_model='SIMPLE_PINHOLE';reader.mask_path=r/'masks'
f=p.FeatureExtractionOptions();f.num_threads=2;f.use_gpu=False;f.max_image_size=1030;f.sift.max_num_features=4096
m=p.FeatureMatchingOptions();m.num_threads=2;m.use_gpu=False
opt=p.IncrementalPipelineOptions();opt.num_threads=2;opt.min_model_size=3;opt.max_num_models=3;opt.init_num_trials=100;opt.max_runtime_seconds=120;opt.random_seed=0
(r/'calibration/sparse').mkdir(parents=True,exist_ok=True)
start=time.time();db=r/'calibration/registration.db'
assert not db.exists(), 'Preserve the recorded trial: use a fresh output directory for a new run.'
p.extract_features(db,r/'input/primary',camera_mode=p.CameraMode.PER_IMAGE,reader_options=reader,extraction_options=f,device=p.Device.cpu)
p.match_exhaustive(db,matching_options=m,device=p.Device.cpu)
models=p.incremental_mapping(db,r/'input/primary',r/'calibration/sparse',options=opt)
con=sqlite3.connect(db)
stats={'images_submitted':sorted(x.name for x in (r/'input/primary').glob('*.png')),'features':con.execute('select image_id,rows from keypoints').fetchall(),'raw_matches':con.execute('select pair_id,rows from matches').fetchall(),'verified_pairs':con.execute('select pair_id,rows,config from two_view_geometries').fetchall(),'models':[],'elapsed_seconds':time.time()-start,'settings':{'camera':'independent SIMPLE_PINHOLE, unknown focal default1.2x max dimension','features':4096,'threads':2,'mapper_max_runtime_seconds':120,'min_model_size':3,'init_trials':100,'gpu':False}}
for key,model in models.items():
 s={'model':key,'registered_images':model.num_reg_images(),'points':model.num_points3D(),'summary':model.summary(),'images':[im.name for im in model.images.values() if im.has_pose]}
 model.export_PLY(r/'pointcloud'/f'sparse-{key}.ply');stats['models'].append(s)
(r/'logs/sfm-result.json').write_text(json.dumps(stats,indent=2))
print(json.dumps(stats,indent=2))
assert len(stats['images_submitted'])==8

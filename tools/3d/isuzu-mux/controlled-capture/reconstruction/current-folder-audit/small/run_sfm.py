from pathlib import Path
import json,time,sqlite3,statistics,os
import pycolmap as p
R=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/controlled-capture/reconstruction/current-folder-audit/small');db=R/'registration.db';assert not db.exists(),'Do not overwrite an earlier test.'
reader=p.ImageReaderOptions();reader.camera_model='SIMPLE_PINHOLE';reader.mask_path=R/'masks'
f=p.FeatureExtractionOptions();f.num_threads=2;f.use_gpu=False;f.max_image_size=1200;f.sift.max_num_features=4096
m=p.FeatureMatchingOptions();m.num_threads=2;m.use_gpu=False
opt=p.IncrementalPipelineOptions();opt.num_threads=2;opt.min_model_size=3;opt.max_num_models=3;opt.init_num_trials=100;opt.max_runtime_seconds=120;opt.random_seed=0
started=time.time();p.extract_features(db,R/'images',camera_mode=p.CameraMode.PER_IMAGE,reader_options=reader,extraction_options=f,device=p.Device.cpu);p.match_exhaustive(db,matching_options=m,device=p.Device.cpu);models=p.incremental_mapping(db,R/'images',R/'sparse',options=opt)
con=sqlite3.connect(db);out={'tools':{'pycolmap':p.__version__,'device':'CPU','threads':2},'settings':{'camera_model':'independent SIMPLE_PINHOLE per image; unknown focal prior default, not EXIF calibration','max_features':4096,'max_image_size':1200,'mapper_time_limit_seconds':120,'min_model_size':3,'init_num_trials':100,'mask':'reviewed coarse vehicle envelopes; viewer-floor graphics excluded'},'images_attempted':len(list((R/'images').glob('*.png'))),'features':con.execute('select image_id,rows from keypoints').fetchall(),'raw_matches':con.execute('select pair_id,rows from matches').fetchall(),'verified_pairs':con.execute('select pair_id,rows,config from two_view_geometries').fetchall(),'elapsed_seconds':time.time()-started,'models':[]}
for key,model in models.items():
 cameras=[]
 for im in model.images.values():
  if not im.has_pose:continue
  pose=im.cam_from_world();cameras.append({'name':im.name,'center':list(im.projection_center()),'rotation_world_to_camera':pose.rotation.matrix().tolist(),'camera_id':im.camera_id})
 points=[{'xyz':list(v.xyz),'error':float(v.error),'track_length':v.track.length(),'rgb':list(map(int,v.color))} for v in model.points3D.values()]
 errors=[v['error'] for v in points];tracks=[v['track_length'] for v in points]
 result={'model':key,'registered_images':model.num_reg_images(),'registration_percentage':100*model.num_reg_images()/out['images_attempted'],'sparse_points':len(points),'summary':model.summary(),'point_error_mean':statistics.mean(errors) if errors else None,'point_error_median':statistics.median(errors) if errors else None,'point_error_max':max(errors) if errors else None,'track_length_mean':statistics.mean(tracks) if tracks else None,'cameras':cameras,'camera_intrinsics':{str(k):{'model':v.model_name,'width':v.width,'height':v.height,'params':list(v.params)} for k,v in model.cameras.items()}}
 (R/'sparse'/f'model-{key}-points.json').write_text(json.dumps(points));model.export_PLY(R/'sparse'/f'model-{key}.ply');out['models'].append(result)
(R/'logs/registration-result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2),flush=True)

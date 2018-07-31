import azure.mgmt.batchai as batchai
from datetime import datetime
from util import bai, fileshare
from iteration_utilities import grouper
import os

if __name__ == '__main__':

  now = datetime.utcnow()

  # set up batch AI client with credentials
  bai_client = bai.setup_bai()
  fs_client = fileshare.setup_file_share()
  
  # get a reference to the cluster we want to use
  cluster = bai.get_cluster(bai_client, os.getenv('CLUSTER_NAME'))

  # create an experiment 
  experiment_name = now.strftime(
    "{0}_%m_%d_%Y_%H%M%S".format(os.getenv('EXPERIMENT_PREFIX'))
  )
  experiment = bai.create_experiment(bai_client, experiment_name)

  # create name output dir
  output_dir = now.strftime(
    "{0}_%m_%d_%Y_%H%M%S".format(
      os.getenv('FS_OUTPUT_IMG_DIRECTORY_PREFIX')
    )
  )

  # create output dir in storage
  fileshare.create_dir(
    blob_service=fs_client,
    blob_dir_name=output_dir
  )

  # set up directories to access for the jobs
  mapping = [
    ('SCRIPT', os.getenv('FS_SCRIPT_DIRECTORY')),
    ('STYLE', os.getenv('FS_STYLE_IMG_DIRECTORY')),
    ('CONTENT', os.getenv('FS_CONTENT_IMG_DIRECTORY')),
    ('OUTPUT', output_dir)
  ]
    
  input_dirs = []
  for dir_id, dir_name in mapping:
    input_dirs.append(
      batchai.models.InputDirectory(
        id=dir_id,
        path='$AZ_BATCHAI_MOUNT_ROOT/{0}/{1}'.format(
          os.getenv('CLUSTER_CONTAINER_MNT_PATH'),
          dir_name
        )
      )
    )

  # create array of content img names inside content img dir
  content_img_names = fileshare.list_blobs_in_dir(
    blob_service=fs_client, 
    blob_dir_name=os.getenv('FS_CONTENT_IMG_DIRECTORY')
  )

  # create a job per chunk
  for group_i, img_name_group in \
      enumerate(grouper(
        content_img_names, 
        int(os.getenv('JOB_BATCH_SIZE'))
      )):
        
    img_list_str = ','.join(img_name_group)

    # set the job name [ex job_01_01_2000_111111]
    job_name = datetime.utcnow().strftime(
      "{0}{1}_%m_%d_%Y_%H%M%S".format(
        os.getenv('JOB_NAME_PREFIX'),
        group_i
      )
    )

    # create params for the job
    job_params = bai.create_job_params(
      cluster=cluster,
      input_dirs=input_dirs,
      output_dirs=None,
      container_image="pytorch/pytorch:0.4_cuda9_cudnn7",
      command_line=("python $AZ_BATCHAI_INPUT_SCRIPT/{0} " + \
        "--style-image $AZ_BATCHAI_INPUT_STYLE/{1} " + \
        "--content-image-dir $AZ_BATCHAI_INPUT_CONTENT " + \
        "--content-image-list {2} " \
        "--output-image-dir $AZ_BATCHAI_INPUT_OUTPUT").format(
          os.getenv('LOCAL_SCRIPT_FILE'),
          os.getenv('LOCAL_STYLE_IMG_FILE'),
          img_list_str
        ),
      job_prep_command_line="pip install scikit-image"
    )

    # create job
    job = bai.create_job(
      bai_client, 
      job_name, 
      job_params, 
      experiment_name
    )

    print('Created Job: {}'.format(job.name))


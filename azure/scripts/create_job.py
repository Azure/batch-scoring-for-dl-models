import azure.mgmt.batchai as batchai
from datetime import datetime
from util import bai, fileshare
from iteration_utilities import grouper
import argparse
import os

if __name__ == '__main__':

  # set up parser
  parser = argparse.ArgumentParser( \
    description='Script for creating a set of BatchAI jobs.')
  parser.add_argument(
    '--content-images-blob-dir', 
    dest='content_images_blob_dir', 
    help='The name of the content images directory in blob.',
    default=os.getenv('FS_CONTENT_DIR')
  )
  parser.add_argument(
    '--job-batch-size',
    dest='job_batch_size',
    help='The number of images to process for BatchAI job.',
    default=os.getenv('JOB_BATCH_SIZE')
  )

  args = parser.parse_args()
  content_images_blob_dir = args.content_images_blob_dir
  job_batch_size = args.job_batch_size

  # set date to be used by experiment name and output dirname
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
  output_images_dir = now.strftime(
    "{0}_%m_%d_%Y_%H%M%S".format(
      os.getenv('FS_OUTPUT_DIR_PREFIX')
    )
  )

  # create output dir in storage
  fileshare.create_dir(
    blob_service=fs_client,
    blob_dir_name=output_images_dir
  )

  # set up directories to access for the jobs
  mapping = [
    ('FILES', os.getenv('FS_INPUT_DIR')),
    ('CONTENT_IMGS', content_images_blob_dir),
    ('OUTPUT_IMGS', output_images_dir)
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
    blob_dir_name=content_images_blob_dir
  )

  # create a job per chunk
  for group_i, img_name_group in \
      enumerate(grouper(
        content_img_names, 
        int(job_batch_size)
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
      command_line=("python $AZ_BATCHAI_INPUT_FILES/{0} " + \
        "--style-image $AZ_BATCHAI_INPUT_FILES/{1} " + \
        "--content-image-dir $AZ_BATCHAI_INPUT_CONTENT_IMGS " + \
        "--content-image-list {2} " \
        "--output-image-dir $AZ_BATCHAI_INPUT_OUTPUT_IMGS").format(
          os.getenv('FS_SCRIPT_NAME'),
          os.getenv('FS_STYLE_IMG_NAME'),
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


import azure.mgmt.batchai as batchai
from datetime import datetime
from util import bai, fileshare
from iteration_utilities import grouper
import argparse
import os
import time
import logging
from logging.handlers import RotatingFileHandler
import sys

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
  parser.add_argument(
    '--log-path',
    dest='log_path',
    help='The path of the log file to create.',
    default=None
  )

  args = parser.parse_args()
  content_images_blob_dir = args.content_images_blob_dir
  job_batch_size = args.job_batch_size
  log_path = args.log_path

  # set up logger
  handler_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  )

  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)

  console_handler = logging.StreamHandler(sys.stdout)
  console_handler.setFormatter(handler_format)
  logger.addHandler(console_handler)

  if log_path is not None:
    file_handler = RotatingFileHandler(
      os.path.join(log_path, 'create_job.log'), 
      maxBytes=20000
    )
    file_handler.setFormatter(handler_format)
    logger.addHandler(file_handler)

  logger.propagate = False

  # set date to be used by experiment name, output/logging dirname
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
    "{0}_{1}_%m_%d_%Y_%H%M%S".format(
      os.getenv('FS_OUTPUT_DIR_PREFIX'),
      content_images_blob_dir
    )
  )

  # create name of log dir
  logger_dir = now.strftime(
    "{0}_{1}_%m_%d_%Y_%H%M%S".format(
      os.getenv('FS_LOGGER_DIR_PREFIX'),
      content_images_blob_dir
    )
  )

  # create mounted output images dir in storage
  fileshare.create_dir(
    blob_service=fs_client,
    blob_dir_name=output_images_dir
  )

  # create mounted logging dir in storage
  fileshare.create_dir(
    blob_service=fs_client,
    blob_dir_name=logger_dir
  )

  # set up input directories to access for the jobs
  mapping = [
    ('FILES', os.getenv('FS_INPUT_DIR')),
    ('CONTENT_IMGS', content_images_blob_dir),
    ('OUTPUT_IMGS', output_images_dir),
    ('LOGGER', logger_dir)
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
  t0 = time.time()
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
        "--output-image-dir $AZ_BATCHAI_INPUT_OUTPUT_IMGS " + \
				"--style-weight {3} " + \
				"--content-weight {4} " + \
				"--num-steps {5} " + \
				"--image-size {6} " + \
        "--log-path $AZ_BATCHAI_INPUT_LOGGER " + \
        "--log-file {7}").format(
          os.getenv('FS_SCRIPT_NAME'),
          os.getenv('FS_STYLE_IMG_NAME'),
          img_list_str,
          os.getenv('STYLE_WEIGHT'),
          os.getenv('CONTENT_WEIGHT'),
          os.getenv('NUM_STEPS'),
          os.getenv('IMAGE_SIZE'),
          job_name # use job_name as log_file name too
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

    logger.debug("Created job #{}, named {}, with {} images." \
      .format(group_i, job.name, len(img_name_group))
    )

  # log total time to create jobs
  t1 = time.time()
  create_jobs_time = t1 - t0
  logger.debug(
    "Time (in seconds) it took to create all BatchAI jobs: {}" \
    .format(create_jobs_time)
  )
  logger.debug(
    "Time (in seconds) it takes to create a single BatchAI job " + \
    "on average: {}".format(create_jobs_time/group_i)
  )



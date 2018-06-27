import azure.mgmt.batchai as batchai
from datetime import datetime
from util import bai
import os

if __name__ == '__main__':

  # set up batch AI client with credentials
  client = bai.setup_bai()

  # input dirs
  mapping = [
    ('SCRIPT', os.getenv('FS_SCRIPT_DIRECTORY')),
    ('MODEL', os.getenv('FS_MODEL_DIRECTORY')),
    ('DATA', os.getenv('FS_DATA_DIRECTORY'))
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

  # output dirs
  output_dirs = [
    batchai.models.OutputDirectory(
      id='RESULT',
      path_prefix='$AZ_BATCHAI_MOUNT_ROOT/{0}'.format(
        os.getenv('CLUSTER_CONTAINER_MNT_PATH')
      )
    )
  ]

  # get a reference to the cluster we want to use
  cluster = bai.get_cluster(client, os.getenv('CLUSTER_NAME'))

  # create an experiment 
  experiment_name = os.getenv('EXPERIMENT')
  experiment = bai.create_experiment(client, experiment_name)

  # set the job name [ex job_01_01_2000_111111]
  job_name = datetime.utcnow().strftime(
    "{0}_%m_%d_%Y_%H%M%S".format(os.getenv('JOB_NAME_PREFIX'))
  )

  # create params for the job
  job_params = bai.create_job_params(
    cluster=cluster,
    input_dirs=input_dirs,
    output_dirs=output_dirs,
    container_image="pytorch/pytorch:0.4_cuda9_cudnn7",
    command_line=("python $AZ_BATCHAI_INPUT_SCRIPT/{0} " + \
      "--model $AZ_BATCHAI_INPUT_MODEL/{1} " + \
      "--data $AZ_BATCHAI_INPUT_DATA " + \
      "--output $AZ_BATCHAI_OUTPUT_RESULT").format(
        os.getenv('LOCAL_SCRIPT_FILE'),
        os.getenv('LOCAL_MODEL_FILE')
      ),
    job_prep_command_line="pip install scikit-image"
  )

  # create job
  job = bai.create_job(client, job_name, job_params, experiment_name)

  print('Created Job: {}'.format(job.name))


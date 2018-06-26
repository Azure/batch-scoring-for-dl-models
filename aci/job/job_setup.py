import azure.mgmt.batchai.models as models
import azure.mgmt.batchai as batchai
from azure.storage.file import FileService
from azure.common.credentials import ServicePrincipalCredentials
from datetime import datetime
import sys
import os


# =========================
# Setup credentials
# =========================
creds = ServicePrincipalCredentials(
  client_id=os.getenv('AAD_CLIENT_ID'),
  secret=os.getenv('AAD_SECRET'),
  tenant=os.getenv('AAD_TENANT')
)

batchai_client = batchai.BatchAIManagementClient(
  credentials=creds, 
  subscription_id=os.getenv('SUBSCRIPTION_ID')
)

# ========================
# Run Azure Batch AI Job
# ========================

# create input directories
input_directories = [
  models.InputDirectory(
    id='SCRIPT',
    path='$AZ_BATCHAI_MOUNT_ROOT/{0}/{1}'.format(
      os.getenv('CLUSTER_CONTAINER_MNT_PATH'),
      os.getenv('FS_SCRIPT_DIRECTORY'))
  ),
  models.InputDirectory(
    id='MODEL',
    path='$AZ_BATCHAI_MOUNT_ROOT/{0}/{1}'.format(
      os.getenv('CLUSTER_CONTAINER_MNT_PATH'),
      os.getenv('FS_MODEL_DIRECTORY')
    )
  ),
  # TODO this should be generated/provided by Functions V2
  models.InputDirectory(
    id='DATA',
    path='$AZ_BATCHAI_MOUNT_ROOT/{0}/{1}'.format(
      os.getenv('CLUSTER_CONTAINER_MNT_PATH'),
      os.getenv('FS_DATA_DIRECTORY')
    )
  )
]

# create output directories
output_directories = [
  models.OutputDirectory(
    id='RESULT',
    path_prefix='$AZ_BATCHAI_MOUNT_ROOT/{0}'.format(os.getenv('CLUSTER_CONTAINER_MNT_PATH'))
  )
]

# get a reference to the cluster we want to use
cluster = batchai_client.clusters.get(
  resource_group_name=os.getenv('RESOURCE_GROUP_NAME'), 
  workspace_name=os.getenv('WORKSPACE'),
  cluster_name=os.getenv('CLUSTER_NAME')
)

# create an experiment (which is the logical container for a job)
experiment = batchai_client.experiments.create(
  resource_group_name=os.getenv('RESOURCE_GROUP_NAME'),
  workspace_name=os.getenv('WORKSPACE'),
  experiment_name=os.getenv('JOB_EXPERIMENT_NAME')
)

# set the std_out path prefix
std_output_path_prefix = '$AZ_BATCHAI_MOUNT_ROOT/{0}'.format(os.getenv('CLUSTER_CONTAINER_MNT_PATH'))

# set the job name [ex job_01_01_2000_111111]
job_name = datetime.utcnow().strftime("{0}_%m_%d_%Y_%H%M%S".format(os.getenv('JOB_NAME_PREFIX')))

# create parameters for the job
parameters = models.JobCreateParameters(
  cluster=models.ResourceId(id=cluster.id),
  node_count=os.getenv('JOB_NODE_COUNT'),
  input_directories=input_directories,
  output_directories=output_directories,
  std_out_err_path_prefix=std_output_path_prefix,
  job_preparation=models.JobPreparation(
    command_line="pip install scikit-image"
  ),
  container_settings=models.ContainerSettings(
    image_source_registry=models.ImageSourceRegistry(
      # image='tensorflow/tensorflow:1.8.0-gpu-py3'
      image='pytorch/pytorch:0.4_cuda9_cudnn7'
    )
  ),
  custom_toolkit_settings=models.CustomToolkitSettings(
    command_line=("python $AZ_BATCHAI_INPUT_SCRIPT/{0} " +
        "--model $AZ_BATCHAI_INPUT_MODEL/{1} " +
        "--data $AZ_BATCHAI_INPUT_DATA " +
        "--output $AZ_BATCHAI_OUTPUT_RESULT").format(
      os.getenv('LOCAL_SCRIPT_FILE'),
      os.getenv('LOCAL_MODEL_FILE')
    )
  )
)

# create job
job = batchai_client.jobs.create(
  resource_group_name=os.getenv('RESOURCE_GROUP_NAME'),
  workspace_name=os.getenv('WORKSPACE'),
  experiment_name=os.getenv('JOB_EXPERIMENT_NAME'),
  job_name=job_name, 
  parameters=parameters
).result()

print('Created Job: {}'.format(job.name))


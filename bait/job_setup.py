import azure.mgmt.batchai.models as models
import azure.mgmt.batchai as batchai
from azure.storage.file import FileService
from azure.common.credentials import ServicePrincipalCredentials
from datetime import datetime
from config import config
import sys
import os


# =========================
# Setup credentials
# =========================
creds = ServicePrincipalCredentials(
  client_id=config.get('aad_client_id'),
  secret=config.get('aad_secret'),
  tenant=config.get('aad_tenant')
)

batchai_client = batchai.BatchAIManagementClient(
  credentials=creds, 
  subscription_id=config.get('subscription_id')
)

# ========================
# Run Azure Batch AI Job
# ========================

# create input directories
input_directories = [
  models.InputDirectory(
    id='SCRIPT',
    path='$AZ_BATCHAI_MOUNT_ROOT/{0}/{1}'.format(
      config.get('cluster_container_mnt_path'),
      config.get('fs_script_directory'))
  ),
  models.InputDirectory(
    id='MODEL',
    path='$AZ_BATCHAI_MOUNT_ROOT/{0}/{1}'.format(
      config.get('cluster_container_mnt_path'),
      config.get('fs_model_directory')
    )
  ),
  # TODO this should be generated/provided by Functions V2
  models.InputDirectory(
    id='DATA',
    path='$AZ_BATCHAI_MOUNT_ROOT/{0}/{1}'.format(
      config.get('cluster_container_mnt_path'),
      config.get('fs_data_directory')
    )
  )
]

# create output directories
output_directories = [
  models.OutputDirectory(
    id='RESULT',
    path_prefix='$AZ_BATCHAI_MOUNT_ROOT/{0}'.format(config.get('cluster_container_mnt_path')),
    path_suffix='results'
  )
]

# get a reference to the cluster we want to use
cluster = batchai_client.clusters.get(
  resource_group_name=config.get('resource_group_name'), 
  workspace_name=config.get('workspace_name'),
  cluster_name=config.get('cluster_name')
)

# create an experiment (which is the logical container for a job)
experiment = batchai_client.experiments.create(
  resource_group_name=config.get('resource_group_name'),
  workspace_name=config.get('workspace_name'),
  experiment_name=config.get('job_experiment_name')
)

# set the std_out path prefix
std_output_path_prefix = '$AZ_BATCHAI_MOUNT_ROOT/{0}'.format(config.get('cluster_container_mnt_path'))

# set the job name [ex job_01_01_2000_111111]
job_name = datetime.utcnow().strftime("{0}_%m_%d_%Y_%H%M%S".format(config.get('job_name_prefix')))

# create parameters for the job
parameters = models.JobCreateParameters(
  cluster=models.ResourceId(id=cluster.id),
  node_count=config.get('job_node_count'),
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
      config.get('local_script_file'),
      config.get('local_model_file')
    )
  )
)

# create job
job = batchai_client.jobs.create(
  resource_group_name=config.get('resource_group_name'),
  workspace_name=config.get('workspace_name'),
  experiment_name=config.get('job_experiment_name'),
  job_name=job_name, 
  parameters=parameters
).result()

print('Created Job: {}'.format(job.name))


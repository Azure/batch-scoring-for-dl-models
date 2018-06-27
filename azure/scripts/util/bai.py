import azure.mgmt.batchai as batchai
from azure.storage.file import FileService
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from datetime import datetime
import os


def setup_bai(
    aad_client_id: str = os.getenv('AAD_CLIENT_ID'),
    aad_secret: str = os.getenv('AAD_SECRET'),
    aad_tenant: str = os.getenv('AAD_TENANT'),
    subscription_id: str = os.getenv('SUBSCRIPTION_ID'),
    rg: str = os.getenv('RESOURCE_GROUP'),
    location: str = os.getenv('REGION')
  ) -> 'batchai.BatchAIManagementClient':
  '''
  Setup credentials, batch AI client, and the resource
    group that the resources will be created in

  All optional arguments will default to using the
    associated environment variable if the parameter
    is not provided.

  Args:
    aad_client_id (str, optional): The client id you get 
      from creating your Service Principle. 
    aad_secret (str, optional): The secret key you get 
      from creating your Service Principle. 
    aad_tenant (str, optional): The tenant id that your
      Service Principle is created in. 
    subscription_id (str, optional): The subscription id
      you wish for your Batch AI resources to be created
      in. 
    rg (str, optional): The Resource Group you will
      create your work in. 
    location (str, optional): The location/region that
      will create your Azure resources in. 

  Returns:
    BatchAIManagementClient: An instance of the Batch AI 
      managment client that can be used to manage Batch
      AI resources.

  '''
  creds = ServicePrincipalCredentials(
    client_id=aad_client_id,
    secret=aad_secret,
    tenant=aad_tenant
  )

  resource_management_client = ResourceManagementClient(
    credentials=creds, 
    subscription_id=subscription_id
  )

  resource = resource_management_client \
    .resource_groups.create_or_update(rg, {
      'location': location
    })

  batchai_client = batchai.BatchAIManagementClient(
    credentials=creds, 
    subscription_id=subscription_id
  )

  return batchai_client


def get_cluster(
    batchai_client: 'BatchAIManagementClient',
    name: str,
    rg: str = os.getenv('RESOURCE_GROUP'),
    ws: str = os.getenv('WORKSPACE'),
  ) -> 'batchai.models.Cluster':
  '''
  Get a BatchAI cluster by cluster name

  All optional arguments will default to using the
    associated environment variable if the parameter
    is not provided.

  Args:
    batchai_client (BatchAIManagementClient): The
      management client to manage Batch AI resources
    name (str): The name of the cluster to get
    rg (str, optional): The resource group to look for 
      the cluster under. 
    ws (str, optional): The Batch AI Workspace to look
      for the cluster under. 

  Returns:
    batchai.models.Cluster: The cluster object that 
      is provided by the BatchAI management sdk.

  '''
  return batchai_client.clusters.get(
    resource_group_name=rg,
    workspace_name=ws,
    cluster_name=name
  )


def create_experiment(
    batchai_client: 'BatchAIManagementClient',
    name: str,
    rg: str = os.getenv('RESOURCE_GROUP'),
    ws: str = os.getenv('WORKSPACE'),
  ) -> 'batchai.models.Experiment':
  '''
  Create a BatchAI Experiment (which is the logical
    container for a job)

  All optional arguments will default to using the
    associated environment variable if the parameter
    is not provided.

  Args:
    batchai_client (BatchAIManagementClient): The
      management client to manage Batch AI resources
    name (str): The name of the Experiment
    rg (str, optional): The resource group to create
      the experiment in. 
    ws (str, optional): The Batch AI Workspace to
      create the experiment in.

  Returns:
    batchai.models.Experiment: The experiment object 
      that is provided by the BatchAI management sdk.

  '''
  return batchai_client.experiments.create(
    resource_group_name=rg,
    workspace_name=ws,
    experiment_name=name
  )


def create_job_params(
    cluster: 'batchai.models.Cluster',
    input_dirs: ['batchai.models.InputDirectory'],
    output_dirs: ['batchai.models.OutputDirectory'],
    container_image: str,
    command_line: str,
    job_prep_command_line: str = '',
    node_count: int = os.getenv('JOB_NODE_COUNT'),
    cluster_mnt_path: str = os.getenv('CLUSTER_CONTAINER_MNT_PATH')
  ):
  '''
  Create the parameter object for the Batch AI job.

  All optional arguments will default to using the
    associated environment variable if the parameter
    is not provided.

  Args:
    cluster (batchai.models.Cluster): The cluster to 
      the parameters for.
    input_dir (List(batchai.models.InputDirectory)):
      A list of the input directories to setup.
    output_dir (List(batchai.models.OutputDirectory)):
      A list of the output directories to setup.
    container_image (str): The container image to use
      when running the job.
    command_line (str): The command line to execute.
    job_prep_command_line (str, optional): Optional
      command line to execute during job_preparation.
    node_count (int, optional): The number of nodes
      to use for the job. 
    cluster_mnt_path (str, optional): The mnt path
      of the file share on the cluster. 

  Returns:
    batchai.models.JobCreateParameters: The Parameter
      object to pass into the job during creation.

  '''
  return batchai.models.JobCreateParameters(
    cluster=batchai.models.ResourceId(id=cluster.id),
    node_count=node_count,
    input_directories=input_dirs,
    output_directories=output_dirs,
    std_out_err_path_prefix='$AZ_BATCHAI_MOUNT_ROOT/{0}'\
      .format(cluster_mnt_path),
    job_preparation=batchai.models.JobPreparation(
      command_line=job_prep_command_line
    ),
    container_settings=batchai.models.ContainerSettings(
      image_source_registry=batchai.models.ImageSourceRegistry(
        image=container_image
      )
    ),
    custom_toolkit_settings=batchai.models.CustomToolkitSettings(
      command_line=command_line
    )
  )


def create_job(
    batchai_client: 'BatchAIManagementClient',
    job_name: str,
    job_params: 'batchai.models.JobCreateParameters',
    experiment_name: str,
    rg: str = os.getenv('RESOURCE_GROUP'),
    ws: str = os.getenv('WORKSPACE'),
  ) -> 'batchai.models.Job':
  '''
  Create a BatchAI Experiment (which is the logical
    container for a job)

  All optional arguments will default to using the
    associated environment variable if the parameter
    is not provided.

  Args:
    batchai_client (BatchAIManagementClient): The
      management client to manage Batch AI resources
    job_name (str): The name of the job.
    job_params (JobCreateParameters): The parameters
      to pass to the job.
    job_experiment_name (str): The name of the
      experiment to create the job under.
    rg (str, optional): The resource group to create
      the job in. 
    ws (str, optional): The Batch AI Workspace to
      create the job in.

  Returns:
    batchai.models.Job: The Job object 
      that is provided by the BatchAI management sdk.

  '''
  return batchai_client.jobs.create(
    resource_group_name=rg,
    workspace_name=ws,
    experiment_name=experiment_name,
    job_name=job_name, 
    parameters=job_params
  ).result()


def create_workspace(
    batchai_client: 'BatchAIManagementClient',
    rg: str = os.getenv('RESOURCE_GROUP'),
    ws: str = os.getenv('WORKSPACE'),
    location: str = os.getenv('REGION')
  ) -> 'batchai.models.WorkSpace':
  '''
  Create a BatchAI Workspace 

  All optional arguments will default to using the
    associated environment variable if the parameter
    is not provided.

  Args:
    batchai_client (BatchAIManagementClient): The
      management client to manage Batch AI resources
    rg (str, optional): The resource group to create
      the workspace in. 
    ws (str, optional): The Batch AI Workspace to
      create the job in.
    location (str, optional): The location/region that
      will create your Workspace in.

  Returns:
    batchai.models.Workspace: The Workspace object 
      that is provided by the BatchAI management sdk.

  '''
  return batchai_client \
    .workspaces \
    .create(rg, ws, location) \
    .result()


def create_autoscale_cluster(
    batchai_client: 'BatchAIManagementClient',
    cluster_name: str,
    vm_size: str = os.getenv('CLUSTER_VM_SIZE'),
    vm_priority: str = \
      os.getenv('CLUSTER_VM_PRIORITY'),
    min_nodes: int = \
      os.getenv('CLUSTER_MINIMUM_NODE_COUNT'), 
    max_nodes: int = \
      os.getenv('CLUSTER_MAXIMUM_NODE_COUNT'),
    initial_nodes: int = \
      os.getenv('CLUSTER_INITIAL_NODE_COUNT'),
    ws: str = os.getenv('WORKSPACE'),
    rg: str = os.getenv('RESOURCE_GROUP'),
    storage_account_name: str = \
      os.getenv('STORAGE_ACCOUNT_NAME'),
    storage_account_key: str = \
      os.getenv('STORAGE_ACCOUNT_KEY'),
    container_name: str = \
      os.getenv('AZURE_CONTAINER_NAME'),
    cluster_mnt_path: str = \
      os.getenv('CLUSTER_CONTAINER_MNT_PATH'),
    admin_user_name: str = \
      os.getenv('ADMIN_USER_NAME'),
    admin_user_password: str = \
      os.getenv('ADMIN_USER_PASSWORD')
  ) -> None:
  '''
  Create an autoscale Batch AI cluster

  All optional arguments will default to using the
    associated environment variable if the parameter
    is not provided.

  Args:
    batchai_client (BatchAIManagementClient): The
      management client to manage Batch AI resources
    cluster_name (str): The name of the cluster you
      wish to create.
    vm_size (str, optional): The vm size of the
      cluster you with to create. 
    vm_priority (str, optional): Choose between low
      priority or dedicated. 
    min_nodes (int, optional): Minimum number of 
      nodes in the autoscale cluster.
    max_nodes (int, optional): Maximum number of
      nodes in the autoscale cluster.
    initial_nodes (int, optional): Initial number 
      of nodes in the autoscale cluster.
    ws (str, optional): The workspace to create the
      cluster in.
    rg (str, optional): The resource group to
      create the cluster in.
    storage_account_name (str, optional): The
      storage account to use when mounting the
      blob container.
    storage_account_key (str, optional): The
      key to use when mounting the blob container.
    container_name (str, optional): The name of
      the container to use in storage.
    cluster_mnt_path (str, optional): The mnt path
      of the file share on the cluster.
    admin_user_name (str, optional): The username
      of the user to create for accessing the
      cluster.
    admin_user_password (str, optional): The
      password of the user to create for accesing
      the cluster.

  Returns:
    None
  '''

  volumes = batchai.models.MountVolumes(
    azure_blob_file_systems=[
      batchai.models.AzureBlobFileSystemReference(
        account_name=storage_account_name,
        credentials=batchai.models.AzureStorageCredentialsInfo(
          account_key=storage_account_key
        ),
        container_name=container_name,
        relative_mount_path=cluster_mnt_path
      )
    ]
  )

  scale_settings = batchai.models.ScaleSettings(
    auto_scale=batchai.models.AutoScaleSettings(
      minimum_node_count=min_nodes,
      maximum_node_count=max_nodes,
      initial_node_count=initial_nodes
    )
  )

  parameters = batchai.models.ClusterCreateParameters(
    vm_size=vm_size,
    vm_priority=vm_priority,
    scale_settings=scale_settings,
    node_setup=batchai.models.NodeSetup(
      mount_volumes=volumes
    ),
    user_account_settings=batchai.models.UserAccountSettings(
      admin_user_name=admin_user_name,
      admin_user_password=admin_user_password
    )
  )

  _ = batchai_client.clusters.create(
    resource_group_name=rg,
    workspace_name=ws,
    cluster_name=cluster_name,
    parameters=parameters
  ).result()



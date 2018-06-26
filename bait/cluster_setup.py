import azure.mgmt.batchai.models as models
import azure.mgmt.batchai as batchai
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
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
  credentials=creds, subscription_id=os.getenv('SUBSCRIPTION_ID')
)

# =========================
# Create Resource Group
# =========================
resource_management_client = ResourceManagementClient(
  credentials=creds, 
  subscription_id=os.getenv('SUBSCRIPTION_ID')
)
resource = resource_management_client.resource_groups.create_or_update(
  os.getenv('RESOURCE_GROUP_NAME'), 
  {'location': os.getenv('REGION')}
)

# =========================
# Create BAIT workspace
# =========================
_ = batchai_client.workspaces.create(
  os.getenv('RESOURCE_GROUP_NAME'),
  os.getenv('WORKSPACE'),
  os.getenv('REGION')
).result()

# =========================
# Create BAIT Cluster
# =========================
volumes = models.MountVolumes(
  azure_blob_file_systems=[
    models.AzureBlobFileSystemReference(
      account_name=os.getenv('STORAGE_ACCOUNT_NAME'),
      credentials=models.AzureStorageCredentialsInfo(
        account_key=os.getenv('STORAGE_ACCOUNT_KEY')
      ),
      container_name=os.getenv('AZURE_CONTAINER_NAME'),
      relative_mount_path=os.getenv('CLUSTER_CONTAINER_MNT_PATH')
    )
  ]
)

scale_settings = None
# use autoscale settings
if os.getenv('cluster_auto_scale'):
  scale_settings = models.ScaleSettings(
    auto_scale=models.AutoScaleSettings(
      minimum_node_count=os.getenv('CLUSTER_MINIMUM_NODE_COUNT'),
      maximum_node_count=os.getenv('CLUSTER_MAXIMUM_NODE_COUNT'),
      initial_node_count=os.getenv('CLUSTER_INITIAL_NODE_COUNT')
    )
  )
  
# use manual settings
else:
  scale_settings = models.ScaleSettings(
    manual=models.ManualScaleSettings(
      target_node_count=os.getenv('CLUSTER_STATIC_NODE_COUNT')
    )
  )

parameters = models.ClusterCreateParameters(
  vm_size=os.getenv('CLUSTER_VM_SIZE'),
  vm_priority=os.getenv('CLUSTER_VM_PRIORITY'),
  scale_settings=scale_settings,
  node_setup=models.NodeSetup(
    mount_volumes=volumes
  ),
  user_account_settings=models.UserAccountSettings(
    admin_user_name=os.getenv('ADMIN_USER_NAME'),
    admin_user_password=os.getenv('ADMIN_USER_PASSWORD')
  )
)

_ = batchai_client.clusters.create(
  resource_group_name=os.getenv('RESOURCE_GROUP_NAME'), 
  workspace_name=os.getenv('WORKSPACE'),
  cluster_name=os.getenv('CLUSTER_NAME'),
  parameters=parameters
).result()


# =========================
# List cluster
# =========================
cluster = batchai_client.clusters.get(
  os.getenv('RESOURCE_GROUP_NAME'), 
  os.getenv('WORKSPACE'),
  os.getenv('CLUSTER_NAME')
)

print('Cluster state: {0}; Allocated: {1}; Idle: {2}; '
      'Unusable: {3}; Running: {4}; Preparing: {5}; Leaving: {6}'.format(
  cluster.allocation_state,
  cluster.current_node_count,
  cluster.node_state_counts.idle_node_count,
  cluster.node_state_counts.unusable_node_count,
  cluster.node_state_counts.running_node_count,
  cluster.node_state_counts.preparing_node_count,
  cluster.node_state_counts.leaving_node_count))


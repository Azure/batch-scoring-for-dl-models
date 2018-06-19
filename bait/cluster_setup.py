import azure.mgmt.batchai.models as models
from config import config
import os

# =========================
# Setup credentials
# =========================
from azure.common.credentials import ServicePrincipalCredentials
import azure.mgmt.batchai as batchai
import azure.mgmt.batchai.models as models

creds = ServicePrincipalCredentials(
  client_id=config.get('aad_client_id'),
  secret=config.get('aad_secret'), 
  tenant=config.get('aad_tenant')
)

batchai_client = batchai.BatchAIManagementClient(
  credentials=creds, subscription_id=config.get('subscription_id')
)

# =========================
# Create Resource Group
# =========================
from azure.mgmt.resource import ResourceManagementClient

resource_management_client = ResourceManagementClient(
  credentials=creds, 
  subscription_id=config.get('subscription_id')
)
resource = resource_management_client.resource_groups.create_or_update(
  config.get('resource_group_name'), 
  {'location': config.get('region')}
)

# =========================
# Create Cluster
# =========================
volumes = models.MountVolumes(
  azure_file_shares=[
    models.AzureFileShareReference(
      account_name=config.get('storage_account_name'),
      credentials=models.AzureStorageCredentialsInfo(
        account_key=config.get('storage_account_key')
      ),
      azure_file_url='https://{0}.file.core.windows.net/{1}'.format(
        config.get('storage_account_name'),
        config.get('file_share_name')
      ),
      relative_mount_path=config.get('cluster_fs_mnt_path')
    )
  ]
)

scale_settings = None
# use autoscale settings
if config.get('cluster_auto_scale'):
  scale_settings = models.ScaleSettings(
    auto_scale=models.AutoScaleSettings(
      minimum_node_count=config.get('cluster_minimum_node_count'),
      maximum_node_count=config.get('cluster_maximum_node_count'),
      initial_node_count=config.get('cluster_initial_node_count')
    )
  )
  
# use manual settings
else:
  scale_settings = models.ScaleSettings(
    manual=models.ManualScaleSettings(
      target_node_count=config.get('cluster_static_node_count')
    )
  )

parameters = models.ClusterCreateParameters(
  location=config.get('region'),
  vm_size=config.get('cluster_vm_size'),
  vm_priority=config.get('cluster_vm_priority'),
  scale_settings=scale_settings,
  node_setup=models.NodeSetup(
    mount_volumes=volumes
  ),
  user_account_settings=models.UserAccountSettings(
    admin_user_name=config.get('admin_user_name'),
    admin_user_password=config.get('admin_user_password')
    # admin_user_ssh_public_key=cfg.admin_ssh_key
  )
)

_ = batchai_client.clusters.create(
  resource_group_name=config.get('resource_group_name'), 
  cluster_name=config.get('cluster_name'),
  parameters=parameters
).result()


# =========================
# List cluster
# =========================
cluster = batchai_client.clusters.get(
  config.get('resource_group_name'), 
  config.get('cluster_name')
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


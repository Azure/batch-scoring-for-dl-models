import os 

# =========================
# Get Variables
# =========================
config = {}

config['aad_client_id']              = os.getenv('CREDENTIALS_AAD_CLIENT_ID')
config['aad_secret']                 = os.getenv('CREDENTIALS_AAD_SECRET')
config['aad_tenant']                 = os.getenv('CREDENTIALS_AAD_TENANT')
config['storage_account_name']       = os.getenv('CREDENTIALS_STORAGE_ACCOUNT_NAME')
config['storage_account_key']        = os.getenv('CREDENTIALS_STORAGE_ACCOUNT_KEY')
config['admin_user_name']            = os.getenv('CREDENTIALS_ADMIN_USER_NAME')
config['admin_user_password']        = os.getenv('CREDENTIALS_ADMIN_USER_PASSWORD')

config['subscription_id']            = os.getenv('ACCOUNT_SUBSCRIPTION_ID')
config['resource_group_name']        = os.getenv('ACCOUNT_RESOURCE_GROUP_NAME')
config['region']                     = os.getenv('ACCOUNT_REGION')

config['azure_file_share_name']      = os.getenv('AZURE_FILE_SHARE_NAME')
config['azure_container_name']       = os.getenv('AZURE_CONTAINER_NAME')
config['fs_script_directory']        = os.getenv('FS_SCRIPT_DIRECTORY')
config['fs_model_directory']         = os.getenv('FS_MODEL_DIRECTORY')
config['fs_result_directory']        = os.getenv('FS_RESULT_DIRECTORY')
config['fs_data_directory']          = os.getenv('FS_DATA_DIRECTORY')

config['local_script_file']          = os.getenv('LOCAL_SCRIPT_FILE') # name of file (not path)
config['local_script_path']          = os.getenv('LOCAL_SCRIPT_PATH') # name of relative path
config['local_model_file']           = os.getenv('LOCAL_MODEL_FILE')  # name of file (not path)
config['local_model_path']           = os.getenv('LOCAL_MODEL_PATH')  # name of file (not path)

config['workspace_name']             = os.getenv('WORKSPACE')

config['job_experiment_name']        = os.getenv('JOB_EXPERIMENT_NAME')
config['job_name_prefix']            = os.getenv('JOB_NAME_PREFIX')
config['job_node_count']             = os.getenv('JOB_NODE_COUNT')

config['cluster_name']               = os.getenv('CLUSTER_NAME')
config['cluster_fs_mnt_path']        = os.getenv('CLUSTER_FILE_SHARE_MNT_PATH')
config['cluster_container_mnt_path'] = os.getenv('CLUSTER_CONTAINER_MNT_PATH')
config['cluster_vm_size']            = os.getenv('CLUSTER_VM_SIZE')
config['cluster_vm_priority']        = os.getenv('CLUSTER_VM_PRIORITY')
config['cluster_auto_scale']         = os.getenv('CLUSTER_AUTO_SCALE')
config['cluster_static_node_count']  = os.getenv('CLUSTER_STATIC_NODE_COUNT')
config['cluster_minimum_node_count'] = os.getenv('CLUSTER_MINIMUM_NODE_COUNT')
config['cluster_maximum_node_count'] = os.getenv('CLUSTER_MAXIMUM_NODE_COUNT')
config['cluster_initial_node_count'] = os.getenv('CLUSTER_INITIAL_NODE_COUNT')



# export all vars as environment variables
set -a

# =========================
# Credentials 
# =========================

# the following fields can be found from creating a service principal
# please reference ___ for instructions on how to create a service principal

CREDENTIALS_AAD_CLIENT_ID='<aad_client_guid>'
CREDENTIALS_AAD_SECRET='<aad_secret>'
CREDENTIALS_AAD_TENANT='<aad_tenant>'

# the following fields can be found from your storage account

CREDENTIALS_STORAGE_ACCOUNT_NAME='<storage_account_name>'
CREDENTIALS_STORAGE_ACCOUNT_KEY='<storage_account_key>'

# Enter the desired username/password for ssh-ing into your batch ai cluster

CREDENTIALS_ADMIN_USER_NAME='<some_username>'
CREDENTIALS_ADMIN_USER_PASSWORD='<some_password>'


# =========================
# Account
# =========================

# the subscription id of your azure account
ACCOUNT_SUBSCRIPTION_ID='<subscription_id>'

# ex. 'batchscoringrg' 
ACCOUNT_RESOURCE_GROUP_NAME='<resource_group_name>'

# ex. 'eastus' - please reference ____ for available locations
ACCOUNT_REGION='<azure_region>'


# =========================
# Azure File Share (AFS) 
# =========================

# ex. 'myfileshare' - name of the azure file-share
AFS_FILE_SHARE_NAME='<name of your file_share>'

# ex. 'directory' - directory for scripts
AFS_SCRIPT_DIRECTORY='<name of your scripts directory>'

# ex. 'result' - directory for results
AFS_RESULT_DIRECTORY='<name of the results directory>'

# ex. 'model' - directory for models
AFS_MODEL_DIRECTORY='<name of the models directory>'

# TESTING ONLY - ex. 'models' - directory for models
AFS_DATA_DIRECTORY='<name of the data directory>'


# =========================
# Local 
# =========================

# must be in: `/scoring_script/<scoring_script>`
LOCAL_SCRIPT_FILE='score0.py'
LOCAL_SCRIPT_PATH='../scoring_script/pytorch_classification'

# must in in: `/models/<model_directory>/...`
LOCAL_MODEL_FILE='model0'
LOCAL_MODEL_PATH='../model/pytorch_classification'


# =========================
# BatchAI 
# =========================

# ex. 'my_workspace'
WORKSPACE='<workspace name>'

# ex. 'my_experiment'
JOB_EXPERIMENT_NAME='<experiment name>'

# ex. 'job' - each job has the id: <prefix_mm_dd_yyyy_time>
JOB_NAME_PREFIX='<prefix of job name>'

# ex. '1' - number of nodes to use for the job
JOB_NODE_COUNT='<num nodes for job>'

# ex. 'bob_nc6_0'
CLUSTER_NAME='<name of your cluster>'

# ex. 'afs'
CLUSTER_FILE_SHARE_MNT_PATH='<file_share_mnt_path>'

# ex. 'STANDARD_NC6' -  please reference ____ for available vm sizes TODO
CLUSTER_VM_SIZE='<vm_size>'

# 'dedicated' or 'low-priority'
CLUSTER_VM_PRIORITY='<vm_priority>'

# autoscale boolean
CLUSTER_AUTO_SCALE='<"True" of "False">'

# Following field is used if 'auto_scale' is set to False
CLUSTER_STATIC_NODE_COUNT='<num nodes in cluster>'

# Following fields are used if 'auto_scale' is set to True
CLUSTER_MINIMUM_NODE_COUNT='<min nodes in cluster>'
CLUSTER_MAXIMUM_NODE_COUNT='<max nodes in cluster>'
CLUSTER_INITIAL_NODE_COUNT='<initial nodes in cluster>'


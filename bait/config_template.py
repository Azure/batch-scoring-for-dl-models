CREDENTIALS = {
  # the following fields can be found from creating a service principal
  #   please reference ___ for instructions on how to create a service principal
  'aad_client_id': '<str: aad_client_id>',
  'aad_secret': '<str: aad_secret>',
  'aad_tenant': '<str: aad_tenant>',

  # the following fields can be found from your storage account
  'storage_account_name': '<str: storage_account_name>',
  'storage_account_key': '<str: storage_account_key',

  # Enter the desired username/password for ssh-ing into your batch ai cluster
  'admin_user_name': '<str: username_to_login>',
  'admin_user_password': '<str: password_to_login>'
}

ACCOUNT = {
  # the subscription id of your azure account
  'subscription_id': '<str: azure_subscription_id>',

  # ex. 'batchscoringrg' 
  'resource_group_name': '<str: azure_resource_group>',

  # ex. 'eastus' - please reference ____ for available locations
  'region': '<str: location>'
}

AFS_PATHS = {
  # ex. 'myfileshare' - name of the azure file-share
  'azure_file_share_name': '<str: azure_file_share_name>',

  # ex. 'directory' - directory for scripts
  'script_directory': '<str: scripts_directory>',

  # ex. 'results' - directory for results
  'results_directory': '<str: results_directory>',

  # ex. 'models' - directory for models
  'model_directory': '<str: models_directory>'
}

LOCAL = {
  # must be in: `/scripts/<scoring_script>`
  'script_name': '<str: name_of_script>', 

  # must in in: `/models/<model_directory>/...`
  'model_directory': '<str: name_of_model_directory>' 
}

JOB = {
  # ex. 'job' - each job has the id: <prefix_mm_dd_yyyy_time>
  'name_prefix': '<str: prefix_of_jobs',

  # ex. '1' - number of nodes to use for the job
  'node_count': '<int: nodes for the job>'
}

CLUSTER = {
  # ex. 'bob_nc6_0'
  'name': '<str: name_of_cluster>',

  # ex. 'afs'
  'file_share_mnt_path': '<str: file_share_mnt_path>',

  # ex. 'STANDARD_NC6' -  please reference ____ for available vm sizes TODO
  'vm_size': '<str: vm_size>', 

  # ex. 'dedicated'
  'vm_priority': '<str: "dedicated" or "low-priority">',

  # autoscale
  'auto_scale': '<bool: True or False>',

  # Following field is used if 'auto_scale' is set to False
  'static_node_count': '<int: number_of_static_nodes>',

  # Following fields are used if 'auto_scale' is set to True
  'minimum_node_count': '<int: max_nodes>',
  'maximum_node_count': '<int: max_nodes>',
  'initial_node_count': '<int: initial_number_of_nodes>'
}

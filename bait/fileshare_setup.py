from azure.storage.file import FileService
import config
import os

'''
Create/attach fileshare & add files to it
Azure File share should have the following directories after this script is executed:

/fileshare
--/scripts
----/script1.py
----/script2.py
----...
--/models
----/model0
------/checkpoint
------/model0.meta
------...
----/model1
----...

'''

# create & setup azure file share
file_service = FileService(
  config.CREDENTIALS['storage_account_name'], 
  config.CREDENTIALS['storage_account_key']
)
file_service.create_share(
  config.AFS_PATHS['azure_file_share_name'], 
  fail_on_exist=False
)
print('Done')

# create directory for storing the scripts
local_script_name = config.LOCAL['script_name']
local_script_path = os.path.join(
  os.path.dirname(__file__), 
  '../scripts/{0}'.format(local_script_name)
)

file_service.create_directory(
  share_name=config.AFS_PATHS['azure_file_share_name'], 
  directory_name=config.AFS_PATHS['script_directory'], 
  fail_on_exist=False
)
file_service.create_file_from_path(
  share_name=config.AFS_PATHS['azure_file_share_name'], 
  directory_name=config.AFS_PATHS['script_directory'], 
  file_name=local_script_name, 
  local_file_path=local_script_path
)
print('Done')

# create directory for storing the models
local_model_directory = config.LOCAL['model_directory'] # a single model uses a directory
local_model_path = os.path.join(
  os.path.dirname(__file__), 
  '../models/{0}'.format(local_model_directory)
)

file_service.create_directory(
  share_name=config.AFS_PATHS['azure_file_share_name'],
  directory_name=os.path.join(config.AFS_PATHS['model_directory'], local_model_directory),
  fail_on_exist=False
)

for file in os.listdir(local_model_path):
  local_file_path = os.path.join(local_model_path, file)
  if os.path.isfile(local_file_path):
    file_service.create_file_from_path(
      share_name=config.AFS_PATHS['azure_file_share_name'],
      directory_name=os.path.join(config.AFS_PATHS['model_directory'], local_model_directory),
      file_name=file,
      local_file_path=local_file_path
    )
print('Done')



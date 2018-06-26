from azure.storage.file import FileService
from azure.storage.blob import BlockBlobService
import argparse
from config import config
import os

'''
Create/attach fileshare & add files to it
Azure File share should have the following directories after this script is executed:

/fileshare (Azure)
--/script
----/script1.py
----/script2.py
----...
--/model
----/model0
------/checkpoint
------/model0.meta
------...
----/model1
----...

'''

if __name__ == '__main__':
  # set up parser
  parser = argparse.ArgumentParser(description='script uploading files to the fileshare.')
  parser.add_argument('--upload-data', dest='upload_data', action='store_true')
  parser.set_defaults(upload_data=False)

  args = parser.parse_args()

  # ===========================================
  # create & setup azure blob as share
  # ===========================================

  # azure blob container (bfs)
  block_blob_service = BlockBlobService(
    account_name=config.get('storage_account_name'), 
    account_key=config.get('storage_account_key')
  ) 
  block_blob_service.create_container(
    config.get('azure_container_name'),
    fail_on_exist=False
  ) 

  # ===========================================
  # create directory for storing the scripts
  # ===========================================

  local_script_path = os.path.join(
    os.path.dirname(__file__), 
    os.path.join(
      config.get('local_script_path'), 
      config.get('local_script_file')
    )
  )

  block_blob_service.create_blob_from_path(
    container_name=config.get('azure_container_name'),
    blob_name=os.path.join(
      config.get('fs_script_directory'), 
      config.get('local_script_file')
    ),
    file_path=local_script_path
  )

  # ===========================================
  # create directory for storing the models
  # ===========================================

  local_model_path = os.path.join(
    os.path.dirname(__file__), 
    os.path.join(
      config.get('local_model_path'),
      config.get('local_model_file')
    )
  )

  block_blob_service.create_blob_from_path(
    container_name=config.get('azure_container_name'),
    blob_name=os.path.join(
      config.get('fs_model_directory'), 
      config.get('local_model_file')
    ),
    file_path=local_model_path
  )


  # ===========================================
  # TESTING ONLY
  # create directory for data
  # ===========================================

  if args.upload_data:
    local_data_dir_path = os.path.join(
      os.path.dirname(__file__), 
      '../data/pytorch_classification/cifar/test'
    )

    for file in os.listdir(local_data_dir_path):
      local_data_file_path = os.path.join(local_data_dir_path, file)
      if os.path.isfile(local_data_file_path):
        block_blob_service.create_blob_from_path(
          container_name=config.get('azure_container_name'),
          blob_name=os.path.join(config.get('fs_data_directory'), file),
          file_path=local_data_file_path
        )




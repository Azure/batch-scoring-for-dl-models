from azure.storage.file import FileService
from azure.storage.blob import BlockBlobService
import argparse
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
    account_name=os.getenv('STORAGE_ACCOUNT_NAME'), 
    account_key=os.getenv('STORAGE_ACCOUNT_KEY')
  ) 
  block_blob_service.create_container(
    os.getenv('AZURE_CONTAINER_NAME'),
    fail_on_exist=False
  ) 

  # ===========================================
  # create directory for storing the scripts
  # ===========================================

  local_script_path = os.path.join(
    os.path.dirname(__file__), 
    os.path.join(
      os.getenv('LOCAL_SCRIPT_PATH'), 
      os.getenv('LOCAL_SCRIPT_FILE')
    )
  )

  block_blob_service.create_blob_from_path(
    container_name=os.getenv('AZURE_CONTAINER_NAME'),
    blob_name=os.path.join(
      os.getenv('FS_SCRIPT_DIRECTORY'), 
      os.getenv('LOCAL_SCRIPT_FILE')
    ),
    file_path=local_script_path
  )

  # ===========================================
  # create directory for storing the models
  # ===========================================

  local_model_path = os.path.join(
    os.path.dirname(__file__), 
    os.path.join(
      os.getenv('LOCAL_MODEL_PATH'),
      os.getenv('LOCAL_MODEL_FILE')
    )
  )

  block_blob_service.create_blob_from_path(
    container_name=os.getenv('AZURE_CONTAINER_NAME'),
    blob_name=os.path.join(
      os.getenv('FS_MODEL_DIRECTORY'), 
      os.getenv('LOCAL_MODEL_FILE')
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
          container_name=os.getenv('AZURE_CONTAINER_NAME'),
          blob_name=os.path.join(os.getenv('FS_DATA_DIRECTORY'), file),
          file_path=local_data_file_path
        )




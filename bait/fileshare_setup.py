from azure.storage.file import FileService
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
  # create & setup azure file share
  # ===========================================

  file_service = FileService(
    config.get('storage_account_name'),
    config.get('storage_account_key')
  )
  file_service.create_share(
    config.get('afs_file_share_name'),
    fail_on_exist=False
  )
  print('Done')

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

  file_service.create_directory(
    share_name=config.get('afs_file_share_name'),
    directory_name=config.get('afs_script_directory'), 
    fail_on_exist=False
  )

  file_service.create_file_from_path(
    share_name=config.get('afs_file_share_name'), 
    directory_name=config.get('afs_script_directory'), 
    file_name=config.get('local_script_file'), 
    local_file_path=local_script_path
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

  file_service.create_directory(
    share_name=config.get('afs_file_share_name'),
    directory_name=config.get('afs_model_directory'),
    fail_on_exist=False
  )

  file_service.create_file_from_path(
    share_name=config.get('afs_file_share_name'),
    directory_name=config.get('afs_model_directory'),
    file_name=config.get('local_model_file'),
    local_file_path=local_model_path
  )

  # ====================================================
  # # if model is a set of files in a dir, such as in TF:
  # ====================================================
  # 
  # for file in os.listdir(local_model_path):
  #   local_file_path = os.path.join(local_model_path, file)
  #   if os.path.isfile(local_file_path):
  #     file_service.create_file_from_path(
  #       share_name=config.AFS_PATHS['azure_file_share_name'],
  #       directory_name=os.path.join(config.AFS_PATHS['model_directory'], local_model_directory),
  #       file_name=file,
  #       local_file_path=local_file_path
  #     )

  # ===========================================
  # TESTING ONLY
  # create directory for data
  # ===========================================

  if args.upload_data:
    local_data_dir_path = os.path.join(
      os.path.dirname(__file__), 
      '../data/pytorch_classification/cifar/test'
    )

    file_service.create_directory(
      share_name=config.get('afs_file_share_name'),
      directory_name=config.get('afs_data_directory'),
      fail_on_exist=False
    )

    for file in os.listdir(local_data_dir_path):
        local_data_file_path = os.path.join(local_data_dir_path, file)
        if os.path.isfile(local_data_file_path):
          file_service.create_file_from_path(
            share_name=config.get('afs_file_share_name'),
            directory_name=config.get('afs_data_directory'),
            file_name=file,
            local_file_path=local_data_file_path
          )


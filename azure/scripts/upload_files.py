from util import fileshare as fs
import argparse
import os

if __name__ == '__main__':
  '''
  Create blob fileshare & your scoring script & model 
    files to it

  Azure container will have the following directories 
    after this script is executed:

    /blob-container (Azure)
    --/script
    ----/script.py
    ----...
    --/model
    ----/model0
    ----...
    --/data (for testing only)
    ----/0001-cat.png
    ----/0002-dog.png
    ----...

  '''

  # set up parser
  parser = argparse.ArgumentParser( \
    description='script for uploading files to blob.')
  parser.add_argument(
    '--upload-data', 
    dest='upload_data', 
    help='use this flag to upload data files',
    action='store_true'
  )
  parser.set_defaults(upload_data=False)
  args = parser.parse_args()

  # setup blob container
  blob_service = fs.setup_file_share()

  # upload scoring script
  fs.create_blob_in_dir(
    blob_service=blob_service,
    blob_dir_name=os.getenv('FS_SCRIPT_DIRECTORY'),
    local_file_path=os.getenv('LOCAL_SCRIPT_PATH'),
    local_file_name=os.getenv('LOCAL_SCRIPT_FILE')
  )

  # upload model file
  fs.create_blob_in_dir(
    blob_service=blob_service,
    blob_dir_name=os.getenv('FS_MODEL_DIRECTORY'),
    local_file_path=os.getenv('LOCAL_MODEL_PATH'),
    local_file_name=os.getenv('LOCAL_MODEL_FILE')
  )

  # TESTING ONLY
  # create directory and upload files for 'data'
  if args.upload_data:
    fs.create_blobs_in_dir(
      blob_service=blob_service,
      blob_dir_name=os.getenv('FS_DATA_DIRECTORY'),
      local_dir_path='../../../pytorch_image_classification/data/cifar/test'
    )


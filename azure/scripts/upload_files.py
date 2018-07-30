from util import fileshare as fs
import argparse
import os

if __name__ == '__main__':
  '''
  Create blob fileshare and add style image, style
    transfer script and output directory to it

  Azure container will have the following directories 
    after this script is executed:

    /blob-container (Azure)
    --/script
    ----/style_transfer_script.py
    --/style_img
    ----/vangogh.jpg
    --/content_img (for testing only)
    ----/0001-cat.jpg
    ----/0002-cat.jpg
    ----...
    --/output_img

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

  # upload style image
  fs.create_blob_in_dir(
    blob_service=blob_service,
    blob_dir_name=os.getenv('FS_STYLE_IMG_DIRECTORY'),
    local_file_path=os.getenv('LOCAL_STYLE_IMG_PATH'),
    local_file_name=os.getenv('LOCAL_STYLE_IMG_FILE')
  )

  # TESTING ONLY
  # create directory and upload files for 'content_imgs'
  if args.upload_data:
    fs.create_blobs_in_dir(
      blob_service=blob_service,
      blob_dir_name=os.getenv('FS_CONTENT_IMG_DIRECTORY'),
      local_dir_path='../../../pytorch_style_transfer/images/content_images'
    )


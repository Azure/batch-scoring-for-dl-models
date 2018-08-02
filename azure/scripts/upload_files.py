from util import fileshare as fs
import argparse
import os

if __name__ == '__main__':

  # set up parser
  parser = argparse.ArgumentParser( \
    description='script for uploading files to blob.')
  parser.add_argument(
    '--style-transfer-script',
    dest='style_transfer_script',
    help='The full relative path to the style-transfer \
      script you wish you upload'
  )
  parser.add_argument(
    '--style-image',
    dest='style_image',
    help='The full relative path to the style image you \
      wish you upload'
  )
  parser.add_argument(
    '--content-images-dir', 
    dest='content_images_dir', 
    help='The full relative path to the directory of \
      content images you wish to upload'
  )
  parser.add_argument(
    '--content-images-blob-dir',
    dest='content_images_blob_dir',
    help='The name of the content images directory to \
      put all content images into.',
    default=os.getenv('FS_CONTENT_DIR')
  )

  args = parser.parse_args()
  style_transfer_script= args.style_transfer_script
  style_image = args.style_image
  content_images_dir = args.content_images_dir
  content_images_blob_dir = args.content_images_blob_dir

  # check that paths are good
  if style_transfer_script:
    assert os.path.exists(style_transfer_script)
  if style_image: 
    assert os.path.exists(style_image)
  if content_images_dir:
    assert os.path.isdir(content_images_dir)

  # check that user is uploading at least one thing
  if style_transfer_script is None and \
    style_image is None and \
    content_images_dir is None:
    print("You are not uploading anything!")
    exit()

  # setup blob container
  blob_service = fs.setup_file_share()

  # upload style-transfer script
  if style_transfer_script:
    style_transfer_script_name = os.path.basename(
      style_transfer_script
    )
    style_transfer_script_path = os.path.dirname(
      os.path.abspath(style_transfer_script)
    )

    fs.create_blob_in_dir(
      blob_service=blob_service,
      blob_dir_name=os.getenv('FS_INPUT_DIRECTORY'),
      blob_file_name=os.getenv('FS_SCRIPT_NAME'),
      local_file_path=style_transfer_script_path,
      local_file_name=style_transfer_script_name
    )

  # upload style image
  if style_image:
    style_image_name = os.path.basename(style_image)
    style_image_path = os.path.dirname(
      os.path.abspath(style_image)
    )

    fs.create_blob_in_dir(
      blob_service=blob_service,
      blob_dir_name=os.getenv('FS_INPUT_DIRECTORY'),
      blob_file_name=os.getenv('FS_STYLE_IMG_NAME'),
      local_file_path=style_image_path,
      local_file_name=style_image_name
    )

  # create directory and upload files for 'content_imgs'
  if content_images_dir:
    blob_dir_name = content_images_blob_dir \
      if content_images_blob_dir \
      else os.path.basename(content_images_dir)

    fs.create_blobs_in_dir(
      blob_service=blob_service,
      blob_dir_name=blob_dir_name,
      local_dir_path=os.path.abspath(content_images_dir)
    )


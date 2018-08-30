from azure.storage.file import FileService
from azure.storage.blob import BlockBlobService
import os


def list_blobs_in_dir(
    blob_service: 'BlockBlobService',
    blob_dir_name: str,
    container_name: str = os.getenv('AZURE_CONTAINER_NAME')
  ) -> 'BlobBlockList':
  '''
  TODO
  '''
  blob_list = blob_service.list_blobs(container_name, blob_dir_name)
  blobs = [blob.name.split('/')[1] for blob in blob_list]
  return blobs


def setup_file_share(
    container_name: str = os.getenv('AZURE_CONTAINER_NAME')
  ) -> 'BlockBlobService':
  '''
  Create & setup Azure blob as share
  
  Args:
    container_name (str, optional): Name of container, will 
      default to using environment variable if param is not 
      provided.

  Returns:
    BlockBlobService: Instance of the Block Blob Service.

  '''
  blob_service = BlockBlobService(
    account_name=os.getenv('STORAGE_ACCOUNT_NAME'), 
    account_key=os.getenv('STORAGE_ACCOUNT_KEY')
  ) 
  blob_service.create_container(
    container_name,
    fail_on_exist=False
  ) 

  return blob_service


def create_dir(
    blob_service: 'BlockBlobService', 
    blob_dir_name: str, 
    container_name: str = os.getenv('AZURE_CONTAINER_NAME')
  ) -> None:
  '''
  Create directory in storage container
  This is done by adding an empty tmp file to the directory

  Args:
    blob_service (BlockBlobService): Instance of the Block
      Blob Service to use.
    blob_dir_name (str): Name of the directory to create 
      in the storage container.
    container_name (str, optional): Name of container, will
      default to using environment variable if param is not
      provided.

  Returns:
    None

  '''
  blob_service.create_blob_from_bytes(
    container_name=container_name,
    blob_name=os.path.join(blob_dir_name, '.tmp'),
    blob=b'foo'
  )


def create_blob_in_dir(
    blob_service: 'BlockBlobService', 
    blob_dir_name: str, 
    local_file_path: str, 
    local_file_name: str, 
    blob_file_name: str,
    container_name: str = os.getenv('AZURE_CONTAINER_NAME')
  ) -> None:
  '''
  TODO: Remove
  Create directory in storage container & add a blob to it.

  Args:
    blob_service (BlockBlobService): Instance of the Block
      Blob Service to use.
    blob_dir_name (str): Name of the directory to create 
      in the storage container.
    local_file_path (str): Path of the file you want to 
      upload. The path should be defined relative to the
      location of this script.
    local_file_name (str): Name of the file you want to
      upload.
    blob_file_name (str): Name of the blob.
    container_name (str, optional): Name of container, will
      default to using environment variable if param is not
      provided.

  Returns:
    None

  '''
  file_path = os.path.join(
    os.path.dirname(__file__), 
    os.path.join(local_file_path, local_file_name)
  )

  blob_service.create_blob_from_path(
    container_name=container_name,
    blob_name=os.path.join(blob_dir_name, blob_file_name),
    file_path=file_path
  )


def create_blobs_in_dir(
    blob_service: 'BlockBlobService', 
    blob_dir_name: str, 
    local_dir_path: str, 
    container_name: str = os.getenv('AZURE_CONTAINER_NAME')
  ) -> None:
  '''
  TODO: remove
  Create directory in storage container & add multiple 
    blobs to it.

  Args:
    blob_service (BlockBlobService): Instance of the Block
      Blob Service to use.
    blob_dir_name (str): Name of the directory to create 
      in the storage container.
    local_dir_path (str): Path of the dir you want to 
      upload. The path should be defined relative to the
      location of this script.
    container_name (str, optional): Name of container, will
      default to using environment variable if param is not
      provided.

  Returns:
    None

  '''
 
  dir_path = os.path.join(
    os.path.dirname(__file__), 
    local_dir_path,
  )

  for file in os.listdir(dir_path):
    file_path = os.path.join(dir_path, file)
    if os.path.isfile(file_path):
      blob_service.create_blob_from_path(
        container_name=container_name,
        blob_name=os.path.join(blob_dir_name, file),
        file_path=file_path
      )
 


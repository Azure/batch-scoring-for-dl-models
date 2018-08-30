#!/bin/bash

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -t|--tag)
    TAG="$2"
    shift # past argument
    shift # past value
    ;;
    -c|--cluster-name)
    CLUSTER_NAME="$2" # not in use atm
    shift # past argument
    shift # past value
    ;;
    *)
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

sudo docker run \
  -e AAD_CLIENT_ID=$AAD_CLIENT_ID \
  -e AAD_SECRET=$AAD_SECRET \
  -e AAD_TENANT=$AAD_TENANT \
  -e STORAGE_ACCOUNT_NAME=$STORAGE_ACCOUNT_NAME \
  -e STORAGE_ACCOUNT_KEY=$STORAGE_ACCOUNT_KEY \
  -e ADMIN_USER_NAME=$ADMIN_USER_NAME\
  -e ADMIN_USER_PASSWORD=$ADMIN_USER_PASSWORD \
  -e SUBSCRIPTION_ID=$SUBSCRIPTION_ID \
  -e RESOURCE_GROUP=$RESOURCE_GROUP \
  -e REGION=$REGION \
  -e AZURE_CONTAINER_NAME=$AZURE_CONTAINER_NAME \
  -e FS_INPUT_DIR=$FS_INPUT_DIR \
  -e FS_SCRIPT_NAME=$FS_SCRIPT_NAME \
  -e FS_STYLE_IMG_NAME=$FS_STYLE_IMG_NAME \
  -e FS_CONTENT_DIR=$FS_CONTENT_DIR \
  -e FS_OUTPUT_DIR_PREFIX=$FS_OUTPUT_DIR_PREFIX \
  -e FS_LOGGER_DIR_PREFIX=$FS_LOGGER_DIR_PREFIX \
  -e WORKSPACE=$WORKSPACE \
  -e EXPERIMENT_PREFIX=$EXPERIMENT_PREFIX \
  -e JOB_NAME_PREFIX=$JOB_NAME_PREFIX \
  -e JOB_NODE_COUNT=$JOB_NODE_COUNT \
  -e JOB_BATCH_SIZE=$JOB_BATCH_SIZE \
  -e CLUSTER_NAME=$CLUSTER_NAME \
  -e CLUSTER_CONTAINER_MNT_PATH=$CLUSTER_CONTAINER_MNT_PATH \
	-e STYLE_WEIGHT=$STYLE_WEIGHT \
  -e CONTENT_WEIGHT=$CONTENT_WEIGHT \
	-e NUM_STEPS=$NUM_STEPS \
  -e IMAGE_SIZE=$IMAGE_SIZE \
  ${TAG}

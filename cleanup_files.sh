#!/bin/bash
# This script is used to restore the state of the directory to the original state

# remove all video files
rm -rf pytorch/video

# remove all log files
rm pytorch/*.log

# remove video generated frames & any output images
mkdir .t
mv pytorch/images/sample_content_images .t
mv pytorch/images/style_images .t
rm -rf pytorch/images
mkdir pytorch/images
mv .t/sample_content_images pytorch/images
mv .t/style_images pytorch/images
rm -rf .t

# remove generated arm template for logic app deployment
rm azure/arm/trigger_arm.json


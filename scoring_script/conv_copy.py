# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Simple, end-to-end, LeNet-5-like convolutional MNIST model example.

This should achieve a test error of 0.7%. Please keep this model as simple and
linear as possible, it is meant as a tutorial for simple convolutional models.
Run with --self_test on the command line to execute a short self-test.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import gzip
import os
import sys
import time
import platform

import numpy
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--use_fp16',
      default=False,
      help='Use half floats instead of full floats if True.',
      action='store_true')
  parser.add_argument(
      '--self_test',
      default=False,
      action='store_true',
      help='True if running a self test.')

  result_output_path = os.environ.get('AZ_BATCHAI_OUTPUT_RESULT')
  input_scripts_path = os.environ.get('AZ_BATCHAI_INPUT_SCRIPTS')
  input_models_path = os.environ.get('AZ_BATCHAI_INPUT_MODELS')
  print("=============================")
  print("AZ_BATCHAI_OUTPUT_RESULT path:")
  print(result_output_path)
  print("AZ_BATCHAI_INPUT_SCRIPTS path:")
  print(os.listdir(input_scripts_path))
  print("AZ_BATCHAI_INPUT_MODELS path:")
  print(os.listdir(input_models_path))
  print("PYTHON Version:")
  print(platform.python_version())
  print("=============================")
  if not os.path.exists(result_output_path):
    pass
  else:
    filename = 'touch_test.txt'
    try:
      f = open(os.path.join(result_output_path, filename), 'wb')
      f.close()
    except IOError:
      print("Wrong path provided")



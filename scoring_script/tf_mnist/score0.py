import tensorflow as tf
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os

tf.reset_default_graph()

# First, load the image again
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = dir_path + "/raw_data/mnist_zero.png"
image = mpimg.imread(filename)
image = tf.image.resize_images(image, [28, 28])
image = tf.reshape(image[:, :, 2], [-1, 784])

with tf.Session() as sess:
  print("=================")
  print(type(image.eval()))
  print(image.dtype)
  print(image.shape)
  print("=================")

  #First let's load meta graph and restore weights
  saver = tf.train.import_meta_graph('./models/model0.meta')
  saver.restore(sess, tf.train.latest_checkpoint('./models'))

  # Now, let's access and create placeholders variables
  graph = tf.get_default_graph()
  x = graph.get_tensor_by_name("input/input:0")
  keep_prob = graph.get_tensor_by_name("input/keep_prob:0")
  preds = graph.get_tensor_by_name("evaluation/preds:0")

  # Calculate accuracy for MNIST test images
  print("score image:", \
    sess.run(tf.argmax(preds, 1), feed_dict={x: image.eval(), keep_prob: 1.0}))


'''
Credit:
This code is largely based off the work by __Alexis Jacq__ `<https://alexis-jacq.github.io>`, and is the implementation of the paper: _Image Style Transfer Using Convolutional Neural Networks_ `<https://arxiv.org/avs/1508.06576>` developed by __Leon A. Gatys__, __Alexander S. Ecker__, and __Matthias Bethge__.
'''

from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image
import torchvision.transforms as transforms
import torchvision.models as models
import torchvision.utils as util
from torch.utils.data import DataLoader
import copy
import argparse
import os
import time
import logging
from logging.handlers import RotatingFileHandler
import sys

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#===================================#
# Define content dataset            #
#===================================#

class ContentDataset(torch.utils.data.Dataset):

  def __init__(self, root_dir, files=None, transform=None):
    '''
    Args:
      root_dir (string): dir with all the images
      files ([string], optional): array of all the images to use in root_dir
        if not specified, use all images in root_dir
      transform (callable, optional): Optional transform to be
        applied on a sample
    '''
    self.root_dir = root_dir

    self.files = [f for f in (os.listdir(root_dir) if files is None else files) \
                  if os.path.isfile(os.path.join(root_dir, f))]

    self.transform = transform

  def __len__(self):
    return len(self.files)

  def __getitem__(self, idx):
    img_name = self.files[idx]
    img = Image.open(os.path.join(self.root_dir, img_name))

    if self.transform:
      img = self.transform(img)

    return img, img_name

#===================================#
# Define classes for Style transfer #
#===================================#

class StyleLoss(nn.Module):

  def __init__(self, target_feature):
    super(StyleLoss, self).__init__()
    self.target = self._gram_matrix(target_feature).detach()

  def forward(self, input):
    G = self._gram_matrix(input)
    self.loss = F.mse_loss(G, self.target)
    return input
  
  def _gram_matrix(self, input):
    a, b, c, d = input.size()  
    # a=batch size(=1)
    # b=number of feature maps
    # (c,d)=dimensions of a f. map (N=c*d)

    features = input.view(a * b, c * d)  # resise F_XL into \hat F_XL

    G = torch.mm(features, features.t())  # compute the gram product

    # we 'normalize' the values of the gram matrix
    # by dividing by the number of element in each feature maps.
    return G.div(a * b * c * d)


class ContentLoss(nn.Module):

  def __init__(self, target,):
    super(ContentLoss, self).__init__()
    # we 'detach' the target content from the tree used
    # to dynamically compute the gradient: this is a stated value,
    # not a variable. Otherwise the forward method of the criterion
    # will throw an error.
    self.target = target.detach()

  def forward(self, input):
    self.loss = F.mse_loss(input, self.target)
    return input
  
  
# create a module to normalize input image so we can easily put it in a
# nn.Sequential
class Normalization(nn.Module):

  def __init__(self, mean, std):
    super(Normalization, self).__init__()
    # .view the mean and std to make them [C x 1 x 1] so that they can
    # directly work with image Tensor of shape [B x C x H x W].
    # B is batch size. C is number of channels. H is height and W is width.
    self.mean = torch.tensor(mean).view(-1, 1, 1)
    self.std = torch.tensor(std).view(-1, 1, 1)

  def forward(self, img):
    # normalize img
    return (img - self.mean) / self.std


#===================================#
# Define Helper Functions           #
#===================================#

# desired depth layers to compute style/content losses:
def get_style_model_and_losses(cnn, normalization_mean, normalization_std,
                               style_img, content_img,
                               content_layers=['conv_4'],
                               style_layers=['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']):
  cnn = copy.deepcopy(cnn)

  # normalization module
  normalization = Normalization(normalization_mean, normalization_std).to(device)

  # just in order to have an iterable access to or list of content/syle
  # losses
  content_losses = []
  style_losses = []

  # assuming that cnn is a nn.Sequential, so we make a new nn.Sequential
  # to put in modules that are supposed to be activated sequentially
  model = nn.Sequential(normalization)

  i = 0  # increment every time we see a conv
  for layer in cnn.children():
    if isinstance(layer, nn.Conv2d):
      i += 1
      name = 'conv_{}'.format(i)
    elif isinstance(layer, nn.ReLU):
      name = 'relu_{}'.format(i)
      # The in-place version doesn't play very nicely with the ContentLoss
      # and StyleLoss we insert below. So we replace with out-of-place
      # ones here.
      layer = nn.ReLU(inplace=False)
    elif isinstance(layer, nn.MaxPool2d):
      name = 'pool_{}'.format(i)
    elif isinstance(layer, nn.BatchNorm2d):
      name = 'bn_{}'.format(i)
    else:
      raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))

    model.add_module(name, layer)

    if name in content_layers:
      # add content loss:
      target = model(content_img).detach()
      content_loss = ContentLoss(target)
      model.add_module("content_loss_{}".format(i), content_loss)
      content_losses.append(content_loss)

    if name in style_layers:
      # add style loss:
      target_feature = model(style_img).detach()
      style_loss = StyleLoss(target_feature)
      model.add_module("style_loss_{}".format(i), style_loss)
      style_losses.append(style_loss)

  # now we trim off the layers after the last content and style losses
  for i in range(len(model) - 1, -1, -1):
    if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
      break

  model = model[:(i + 1)]

  return model, style_losses, content_losses


def get_input_optimizer(input_img):
  # this line to show that input is a parameter that requires a gradient
  optimizer = optim.LBFGS([input_img.requires_grad_()])
  return optimizer


def run_style_transfer(cnn, normalization_mean, normalization_std,
                       content_img, style_img, input_img, num_steps=300,
                       style_weight=10000000, content_weight=1, 
                       tmp_dir=False):
    
  """
  Run the style transfer.
  This function takes a tmp_dir parameter. If this parameter is specified,
      then intermediate results (at every 50 steps) will be saved to the 
      location specified in the parameter. If the parameter is set to
      False, then no intermediate results will be saved to disk.
  """
  logger = logging.getLogger('root')
  
  model, style_losses, content_losses = get_style_model_and_losses(cnn,
      normalization_mean, normalization_std, style_img, content_img)
  optimizer = get_input_optimizer(input_img)
  
  run = [0]
  while run[0] <= num_steps:

    def closure():
      # correct the values of updated input image
      input_img.data.clamp_(0, 1)

      optimizer.zero_grad()
      model(input_img)
      style_score = 0
      content_score = 0

      for sl in style_losses:
        style_score += sl.loss
      for cl in content_losses:
        content_score += cl.loss

      style_score *= style_weight
      content_score *= content_weight

      loss = style_score + content_score
      loss.backward()

      run[0] += 1
      if run[0] % 50 == 0:
        logger.debug('run #{:_>4} - Style Loss : {:4f} Content Loss: {:4f}'.format(
          run[0], style_score.item(), content_score.item()))
        
        # save tmp folder
        if tmp_dir:
          if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
          util.save_image(input_img, '{0}/tmp_{1:0>4}.jpg'.format(tmp_dir, run[0]))

      return style_score + content_score

    optimizer.step(closure)

  # a last correction...
  input_img.data.clamp_(0, 1)

  return input_img

#===================================#
# Main Process: Load content/style images & apply style transfer
#===================================#

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Style Transfer script for Pytorch')
  parser.add_argument(
    '--style-image',
    dest='style_image',
    help='The path of the style image',
    default='images/style_images/sample_vangogh.jpg'
  )
  parser.add_argument(
    '--content-image-dir',
    dest='content_image_dir',
    help='The path of the directory of the content images.',
    default='./images/content_images'
  )
  parser.add_argument(
    '--content-image-list',
    dest='content_image_list',
    help='A comma separated list of images to use in the content_image_dir',
    default=None
  )
  parser.add_argument(
    '--output-image-dir',
    dest='output_image_dir',
    help='The path where the output images would be stored.',
    default='./images/output_images'
  )
  parser.add_argument(
    '--style-weight',
    dest='style_weight',
    type=int,
    help='The weight to use when optimizing the style loss.',
    default=10**8
  )
  parser.add_argument(
    '--content-weight',
    dest='content_weight',
    type=int,
    help='The weight to use when optimizing the content loss.',
    default=1
  )
  parser.add_argument(
    '--num-steps',
    dest='num_steps',
    type=int,
    help='The number of steps to use when optimizing the style transfer loss function.',
    default=300
  )
  parser.add_argument(
    '--image-size',
    dest='image_size',
    type=int,
    help='The pixel dimension of the output image (W=H)'
  )
  parser.add_argument(
    '--log-path',
    dest='log_path',
    help='The path of the log file to create.',
    default='.'
  )
  parser.add_argument(
    '--log-file',
    dest='log_file',
    help='The name of the file to log to.',
    default=None
  )
  args = parser.parse_args()

  style_image = args.style_image
  content_image_dir = args.content_image_dir
  content_image_list = args.content_image_list
  output_image_dir = args.output_image_dir
  style_weight = args.style_weight
  content_weight = args.content_weight
  num_steps = args.num_steps
  image_size = args.image_size
  log_path = args.log_path
  log_file = args.log_file

  # check that all the paths and image references are good
  assert os.path.exists(style_image)
  assert os.path.exists(content_image_dir)
  assert os.path.exists(output_image_dir)
  assert os.path.isdir(content_image_dir)
  assert os.path.isdir(output_image_dir)
  if content_image_list is not None:
    for image_file in content_image_list.split(','):
      assert os.path.exists(os.path.join(content_image_dir, image_file))
  assert os.path.isdir(log_path)
  
  # set up logger
  handler_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  console_handler = logging.StreamHandler(sys.stdout)
  console_handler.setFormatter(handler_format)
  file_handler = RotatingFileHandler(
    os.path.join(
      log_path, 
      '{}.log'.format(log_file) if log_file else 'style_transfer_script.log'
    ), 
    maxBytes=20000
  )
  file_handler.setFormatter(handler_format)

  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)
  logger.addHandler(console_handler)
  logger.addHandler(file_handler)
  logger.propagate = False

  # log script paramters
  num_images = len(content_image_list.split(',')) \
    if content_image_list is not None \
    else len(os.listdir(content_image_dir))
  logger.debug("Images to process: %i" % num_images)

  # Setup image transformations
  if not image_size:
    image_size = 512 if torch.cuda.is_available() else 128  # use small size if no gpu
  logger.debug("GPU detected: %s, image size: %s" % (str(torch.cuda.is_available()), image_size))

  # setup loader
  loader = transforms.Compose([
    transforms.Resize(image_size),  # scale imported image
    transforms.CenterCrop(image_size), # crop on center
    transforms.ToTensor()])  # transform it into a torch tensor

  # Setup content image loader
  content_img_set = ContentDataset(
    root_dir=content_image_dir, 
    files=content_image_list.split(','), 
    transform=loader)
  content_img_loader = DataLoader(content_img_set, batch_size=1, shuffle=False, num_workers=1)

  # Load style image
  t0 = time.time()
  style_img = loader(Image.open(style_image)).unsqueeze(0).to(device, torch.float)
  t1 = time.time()
  style_img_time = t1 - t0
  logger.debug("Time (in seconds) to load style image: %f" % style_img_time)

  # load vgg19
  t0 = time.time()
  cnn = models.vgg19(pretrained=True).features.to(device).eval()
  t1 = time.time()
  load_cnn_time = t1 - t0
  logger.debug("Time (in seconds) to load VGG19 model: %f" % load_cnn_time)

  # VGG networks are trained on images with each channel 
  # normalized by mean=[0.485, 0.456, 0.406] and std=[0.229, 0.224, 0.225]. 
  cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
  cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)

  # store image outputs in memory
  output_imgs = []
  content_imgs = []

  # run style transfer on each content image
  t0 = time.time()
  
  for content_img_batch, content_filename_batch in content_img_loader:

    # load image and add image to content image array
    content_img = content_img_batch[0].unsqueeze(0).to(device, torch.float)
    content_filename = content_filename_batch[0]
    content_imgs.append(content_img)

    # use white noise image as input image:
    # input_img = torch.randn(content_img.data.size(), device=device)
    # use content image as input image:
    input_img = content_img.clone()

    # style transfer!
    logger.debug("Running Style Transfer on %s" % content_filename)
    output = run_style_transfer(cnn, cnn_normalization_mean, cnn_normalization_std,
                                content_img, style_img, input_img, num_steps=num_steps,
                                style_weight=style_weight, content_weight=content_weight)

    # add output image to array
    output_imgs.append(output)

    # save output image
    util.save_image(output, os.path.join(
      output_image_dir, '{0}.jpg'.format(content_filename.split('.')[0])
    ))

  # log total time to run jobs
  t1 = time.time()
  style_transfer_time = t1 - t0
  logger.debug("Time (in seconds) to apply style-transfer to batch of %i images: %f" \
    % (num_images, style_transfer_time))
  logger.debug("Average Time (in seconds) to apply style-transfer to each image: %f" \
    % (style_transfer_time / num_images))

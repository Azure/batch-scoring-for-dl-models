import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from datetime import datetime
from skimage import io, transform
from torch.utils.data import DataLoader

import argparse
import os

# ============================================= #
# Define CNN Architecture
# ============================================= #

class Net(nn.Module):
  def __init__(self):
    super(Net, self).__init__()
    self.conv1 = nn.Conv2d(3, 6, 5)
    self.pool = nn.MaxPool2d(2, 2)
    self.conv2 = nn.Conv2d(6, 16, 5)
    self.fc1 = nn.Linear(16 * 5 * 5, 120)
    self.fc2 = nn.Linear(120, 84)
    self.fc3 = nn.Linear(84, 10)

  def forward(self, x):
    x = self.pool(F.relu(self.conv1(x)))
    x = self.pool(F.relu(self.conv2(x)))
    x = x.view(-1, 16 * 5 * 5)
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = self.fc3(x)
    return x

net = Net()
net.cuda()

# ============================================= #
# Dataset Class
# ============================================= #

class CifarDataset(torch.utils.data.Dataset):
  
  def __init__(self, root_dir, transform=None):
    '''
    Args:
      root_dir (string): dir with all the images
      transform (callable, optional): Optional transform to be
        applied on a sample
    '''
    self.root_dir = root_dir
    self.files = [f for f in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, f))]
    self.transform = transform

  def __len__(self):
    return len(self.files)

  def __getitem__(self, idx):
    img_name = self.files[idx]
    img = io.imread(os.path.join(self.root_dir, img_name))

    if self.transform:
      img = self.transform(img)

    return img, img_name


# ============================================= #
# Transformer - Rescale
# ============================================= #

class Rescale(object):

  def __init__(self, output_size):
    assert isinstance(output_size, (int, tuple))
    self.output_size = output_size

  def __call__(self, image):
    h, w = image.shape[:2]
    if isinstance(self.output_size, int):
      if h > w:
        new_h, new_w = self.output_size * h / w, self.output_size
      else:
        new_h, new_w = self.output_size, self.output_size * w / h
    else:
      new_h, new_w = self.output_size

    img = transform.resize(image, (int(new_h), int(new_w)))
    return img


# ============================================= #
# Load trained weights of CNN 
# ============================================= #

def load_weights(net, model_path):
  '''
  load weights from path and return model/net
  '''
  net.load_state_dict(torch.load(model_path))
  net.cuda()
  return net


# ============================================= #
# Entry point
# ============================================= #

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Scoring script for Pytorch')
  parser.add_argument(
    '--model',
    help='The path where your model weights are saved',
    default='model0'
  )
  parser.add_argument(
    '--data',
    help='The path where the data your want to score are located',
    default='data/cifar/test/'
  )
  parser.add_argument(
    '--output',
    help='the path where the results should be stored',
    default='.'
  )
  args = parser.parse_args()

  model_path = args.model
  data_path = args.data
  output_path = args.output

  net = Net()
  net = load_weights(net, model_path)

  # create cifar dataset
  cifar_dataset = CifarDataset(
    data_path, 
    transform=torchvision.transforms.Compose([Rescale(32)])
  )

  # create data loader from dataset
  dataloader = DataLoader(cifar_dataset, batch_size=1, shuffle=True, num_workers=4)

  # define classes to map predictions to 
  label_map = {
    'dog': 0,
    'bird': 1, 
    'airplane': 2,
    'horse': 3,
    'frog': 4,
    'automobile': 5,
    'cat': 6,
    'deer': 7,
    'truck': 8, 
    'ship': 9
  }

  def get_category(i):
    for k, v in label_map.items():
      if v == i:
        return k

  # score!
  with torch.no_grad():
    time = datetime.utcnow().strftime("%m_%d_%Y_%H%M%S")
    with open(os.path.join(output_path, 'scores_{0}'.format(time)), "w") as file:
      for img, img_name in dataloader:

        # enforce shape (img in batch, channels, height, width)
        img = img.view([1, 3, 32, 32])

        # cast tensor to float
        img = img.float()
            
        outputs = net(img.cuda())
        _, predicted = torch.max(outputs.data, 1)

        # write to output
        file.write('Predictd: %10s | Filename: %25s' % (get_category(predicted[0]), img_name))
        file.write('\n')




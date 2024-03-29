# -*- coding: utf-8 -*-
"""Final GAN test.ipynb

Automatically generated by Colaboratory.

"""

!pip install tensorboardX

from google.colab import drive
drive.mount('/content/drive',force_remount=True)

!git clone https://github.com/shionhonda/viton-gan #Dataset

!unzip '/content/drive/My Drive/viton_resize.zip'

ls

cd viton-gan/

ls

cd viton_gan/

!mv '/content/viton_resize/test' '/content/viton-gan/viton_gan/data'
!mv '/content/viton_resize/train' '/content/viton-gan/viton_gan/data'
!mv '/content/viton_resize/val' '/content/viton-gan/viton_gan/data'
!mv '/content/viton_resize/val_pairs.txt' '/content/viton-gan/viton_gan/data'

import argparse

opt = argparse.Namespace(checkpoint = '/content/drive/My Drive/checkpoints/gmm_train_new/gmm_final.pth',
                         data_root = '/content/viton-gan/viton_gan/data',
                         out_dir = '/content/viton-gan/viton_gan/results',
                         name = 'GMM',
                         batch_size = 16,
                         n_worker = 4,
                         gpu_id = '0',
                         log_freq = 100,
                         radius = 5,
                         fine_width = 192,
                         fine_height = 256,
                         grid_size = 5)

from run_gmm import *

model = GMM(opt)
load_checkpoint(model, opt.checkpoint)
model.cuda()
model.eval()
modes = [ 'test']
for mode in modes:
	print('Run on {} data'.format(mode.upper()))
	dataset = GMMDataset(opt, mode, data_list=mode+'_pairs.txt', train=False)
	dataloader = DataLoader(dataset, batch_size=opt.batch_size, num_workers=opt.n_worker, shuffle=False)   
	with torch.no_grad():
		run(opt, model, dataloader, mode)
print('Successfully completed')

opt = argparse.Namespace(checkpoint = '/content/drive/My Drive/viton-gan/tom_gen_epoch_50.pth',
                         data_root = '/content/viton-gan/viton_gan/data',
                         out_dir = '/content/viton-gan/viton_gan/output2',
                         name = 'TOM',
                         batch_size = 16,
                         n_worker = 4,
                         gpu_id = '0',
                         log_freq = 100,
                         radius = 5,
                         fine_width = 192,
                         fine_height = 256,
                         grid_size = 5)

from run_tom import *

model = UnetGenerator(25, 4, 6, ngf=64, norm_layer=nn.InstanceNorm2d)
load_checkpoint(model, opt.checkpoint)
model.cuda()
model.eval()
mode = 'test'
print('Run on {} data'.format(mode.upper()))
dataset = TOMDataset(opt, mode, data_list=mode+'_pairs.txt', train=False)
dataloader = DataLoader(dataset, batch_size=opt.batch_size, num_workers=opt.n_worker, shuffle=False)   
with torch.no_grad():
	run(opt, model, dataloader, mode)
print('Successfully completed')


#!/usr/bin/env python3

import os
import cv2
import glob
import torch
import numpy as np
import urllib.request
from PIL import Image, ImageOps
import torchvision.transforms as transforms


use_large_model = True

if use_large_model:
	midas = torch.hub.load('intel-isl/MiDaS', 'DPT_Large')
else:
	midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
midas.to(device)
midas.eval()

midas_transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')

if use_large_model:
	transform = midas_transforms.dpt_transform
	print('Using large (slow) model.')
else:
	transform = midas_transforms.small_transform
	print('Using small (fast) model.')


for file in glob.glob('./rgb/*.jpg'):

	img = cv2.imread(file)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	
	input_batch = transform(img).to(device)
	
	with torch.no_grad():
		prediction = midas(input_batch)
	
		prediction = torch.nn.functional.interpolate(
			prediction.unsqueeze(1),
			size = img.shape[:2],
			mode = 'bicubic',
			align_corners = False,
		).squeeze()
	
	output = prediction.cpu().numpy()
	
	output_normalized = (output * 255 / np.max(output)).astype('uint8')
	output_image = Image.fromarray(output_normalized)
	output_image_converted = output_image.convert('RGB').save(file.replace('rgb', 'depth'))
	print('Converted: ' + file)
print('Done.')
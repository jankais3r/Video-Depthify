#!/usr/bin/env python3

import os
import glob
import numpy as np
from PIL import Image

items = len(glob.glob('./depth/*.jpg')) - 2
first = './depth/000001.jpg'
last = './depth/' + str(items + 2).zfill(6) + '.jpg'
w, h = Image.open(first).size
Image.open(first).save(first.replace('depth', 'averaged'))

for idx in range(items):
	current = idx + 2
	arr = np.zeros((h, w, 3), np.float)
	
	prev = np.array(Image.open('./depth/' + str(current - 1).zfill(6) + '.jpg'), dtype = np.float)
	curr = np.array(Image.open('./depth/' + str(current).zfill(6) + '.jpg'), dtype = np.float)
	next = np.array(Image.open('./depth/' + str(current + 1).zfill(6) + '.jpg'), dtype = np.float)
	
	arr = arr+prev/3
	arr = arr+curr/3
	arr = arr+next/3
	
	arr = np.array(np.round(arr), dtype = np.uint8)
	
	out = Image.fromarray(arr,mode = 'RGB')
	out.save('./averaged/' + str(current).zfill(6) + '.jpg')
	#print('Averaged: ' + str(current).zfill(6) + '.jpg')

Image.open(last).save(last.replace('depth', 'averaged'))
print('Done.')
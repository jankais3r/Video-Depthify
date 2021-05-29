#!/usr/bin/env python3

import glob
from PIL import Image

def get_concat_v(im1, im2):
	dst = Image.new('RGB', (im1.width, im1.height + im2.height))
	dst.paste(im1, (0, 0))
	dst.paste(im2, (0, im1.height))
	return dst

for file in glob.glob("./rgb/*.jpg"):
	im1 = Image.open(file)
	try:
		im2 = Image.open(file.replace('rgb', 'averaged'))
	except:
		im2 = Image.open(file.replace('rgb', 'depth'))
	get_concat_v(im1, im2).save(file.replace('rgb', 'merged'))
	#print("Merged: " + file)
print('Done.')
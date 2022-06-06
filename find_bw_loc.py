# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 13:37:55 2021

@author: Syncer
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import argparse

# parsing
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', default='stitches')
args = parser.parse_args()

iw = 16
ih = 16
offset = [ 42,  57,  58, 231, 356, 392, 392,
          392, 548, 548, 548, 548, 582, 607,
          613, 622, 639, 646, 651, 654, 705]

image = np.asarray(Image.open('E:/SYNCER STUDIO/YT/Repentance/resources/death items.png'))
with open('E:/python_workspace/isaac_script/full_item_list.txt') as f:
    ilist = f.readlines()

ilist = [t.strip('\n') for t in ilist]

w = image.shape[1]
h = image.shape[0]
nw = w // iw
nh = h // ih

target = args.name
tid = -1

for i, t in enumerate(ilist):
    if t.lower() == target.lower():
        tid = i
        break

if tid == -1:
    print('Not found')
    assert(0)
print(tid)
    
ttid = tid
for i in offset:
    if tid >= i:
        ttid += 1

tw = ttid % nw
th = (ttid - tw) // nw

plt.imshow(image[th*ih:th*ih+ih, tw*iw:tw*iw+iw, :])
plt.show()

print(-tw*256)
print(-th*256)
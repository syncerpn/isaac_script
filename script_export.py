# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 17:05:40 2021

@author: Syncer
"""
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import os

from Font   import Font
from Text   import Text_box
from Effect import Effect

root = './'
res_dir = ''
common_fnt_file = 'pftempestasevencondensed.fnt'
common_font = Font(root + res_dir + common_fnt_file)

# --script text
script_file = 'script.txt'
script_effect = Effect()
script_effect.add_effect_drop_shadow([0,0])
script_effect.add_effect_scale(1)

script_effect_list = [script_effect.r_drop_shadow, script_effect.r_scale]

f_list = [script_file]
e_list = [script_effect_list]

for i, f_name in enumerate(f_list):
    eff = e_list[i]
    if not os.path.isfile(root + f_name):
        print('[FAILED] file not found: ', f_name)
        continue
    
    with open(root + f_name) as f:
        text_raw = f.readlines()
        
    text_raw = [t.strip('\n') for t in text_raw]
    text_list = []
    line = []
    for t in text_raw:
        if t == '':
            text_list.append('\n'.join(line))
            line = []
        else:
            line.append(t)
    if len(line) > 0:
        text_list.append('\n'.join(line))
    
    for j, text in enumerate(text_list):
        print('[ INFO ] ' + f_name + ': ' + text)
        text_box = Text_box(text, common_font, 'center')
        image = Effect.render(text_box.im, eff)
        plt.imsave(root + f_name[:-4] + '_' + str(j+1) + '.png', image)
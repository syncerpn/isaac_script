# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 15:58:18 2021

@author: Syncer
"""

from struct import unpack, calcsize
import numpy as np
import os
from PIL import Image

from Char import Char

class Font:
    @staticmethod
    def read_block(fmt, data, data_pointer):
        data_pointer_end = data_pointer + calcsize(fmt)
        return data_pointer_end, unpack(fmt, data[data_pointer:data_pointer_end])
    
    def kern_test(self):
        text = ''
        for i in range(len(self.kerns)):
            a, b, _ = self.kerns[i]
            text += chr(a) + chr(b) + 'a' + ' '
        return text
        
    def __init__(self, file_name):
        self.file_name = file_name

        fmt_header = '=3sB' # header format
        fmt_block_id_size = '=BI' # block identifier/size format
        fmt_info = '=HBBHBBBBBBBB' # info format
        fmt_common = '=HHHHHBBBBB' # common format
        fmt_chars = '=IHHHHhhhBB' # chars format
        fmt_kerning_pairs = '=IIh' # kerning format
        
        dp = 0
        pages_list = []
        chars = []
        self.kerns = []
        
        with open(file_name, 'rb') as f:
            data = f.read()
        
        while dp < len(data):
            if dp == 0:
                dp, _ = Font.read_block(fmt_header, data, dp)
                
            dp, (block_id, block_size,) = Font.read_block(fmt_block_id_size, data, dp)
            
            if block_id == 1:
                fmt_info += str(block_size - calcsize(fmt_info)) + 's'
                dp, _ = Font.read_block(fmt_info, data, dp)
                
            elif block_id == 2:
                dp, (self.line_height, self.base, _, _, pages, _,
                     _, _, _, _) = Font.read_block(fmt_common, data, dp)
            
            elif block_id == 3:
                fmt_page = '=' + str(block_size) + 's'
                dp, (page,) = Font.read_block(fmt_page, data, dp)
                pages_list.append(page[:-1])
                
            elif block_id == 4:
                n_char = block_size // calcsize(fmt_chars)
                for i in range(n_char):
                    dp, char = Font.read_block(fmt_chars, data, dp)
                    chars.append(char)
                    
            elif block_id == 5:
                n_kern = block_size // calcsize(fmt_kerning_pairs)
                for i in range(n_kern):
                    dp, kern = Font.read_block(fmt_kerning_pairs, data, dp)
                    self.kerns.append(kern)
        
        fnt_bmps = []
        
        for i in range(len(pages_list)):
            fnt_bmp = np.asarray(Image.open(os.path.dirname(self.file_name) + '/' + pages_list[0].decode()))
            # ===only need once===
            # fix using alpha mask
            # rgb_map_fix   = fnt_bmp[:,:,0:3] * (fnt_bmp[:,:,3:4] != 0)
            # alpha_map_fix = ((fnt_bmp[:,:,3:4] == 255) * 255).astype(np.uint8)
            
            # fnt_bmp = np.concatenate((rgb_map_fix, alpha_map_fix), axis=2)
            # Image.fromarray(fnt_bmp).save(root + pages_list[0].decode())
            # ===only need once===
            fnt_bmps.append(fnt_bmp)
            
        self.chars = {}
        self.line_et = 0
        self.line_eb = 0
        for i in range(len(chars)):
            ch_id, ch_x, ch_y, ch_w, ch_h, ch_xo, ch_yo, ch_xa, ch_page, ch_chnl = chars[i]
            if ch_yo < self.line_et:
                self.line_et = ch_yo
                
            if ch_h + ch_yo - self.line_height > self.line_eb:
                self.line_eb = ch_h + ch_yo - self.line_height
                
            self.chars[ch_id] = Char(ch_id, fnt_bmps, ch_x, ch_y, ch_w, ch_h, ch_xo, ch_yo, ch_xa, ch_page, ch_chnl)

        

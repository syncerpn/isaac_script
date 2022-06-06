# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 16:40:05 2021

@author: Syncer
"""

import numpy as np
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 07:02:34 2021

@author: Syncer
"""

# render color code: 'r', 'g', 'b'

class Text_line:
    # place_char: place the char image into text line image
    @staticmethod
    def parse_text_color(text):
        color_code = None
        valid_text = ''
        colors = []
        
        i = 0
        while i < len(text):
            c = text[i]
            if c == '[':
                i = i+1
                color_code = text[i]
            elif c == ']':
                color_code = None
            elif c == '\n':
                break
            else:
                colors.append(color_code)
                valid_text += c
            i = i+1
        
        return valid_text, colors
    
    @staticmethod
    def colorize_char_image(image, color):
        char_image = image.copy()
        if color is not None:
            char_image_mask = char_image[:,:,3] != 0
            if color == 'r':
                char_image[char_image_mask, 1] = 0
                char_image[char_image_mask, 2] = 0
            elif color == 'g':
                char_image[char_image_mask, 0] = 0
                char_image[char_image_mask, 2] = 0
            elif color == 'b':
                char_image[char_image_mask, 0] = 0
                char_image[char_image_mask, 1] = 0
            elif color == 'c':
                char_image[char_image_mask, 0] = 0
            elif color == 'm':
                char_image[char_image_mask, 1] = 0
            elif color == 'y':
                char_image[char_image_mask, 2] = 0
            else:
                assert(0) # unknown color code
        return char_image
    
    def place_char(self, cch, pch, color):
        kern = 0
        for j in range(len(self.font.kerns)):
            if self.font.kerns[j][0] == pch.id and self.font.kerns[j][1] == cch.id:
                kern = self.font.kerns[j][2]
                break
        
        self.psy = cch.yo - self.font.line_et
        self.psx = self.curs_offs + cch.xo + kern
        
        expand_l = 0
        if self.psx < 0:
            expand_l = -self.psx
            self.curs_offs = self.curs_offs - self.psx
            self.psx = 0
        
        self.pey = self.psy + cch.h
        self.pex = self.psx + cch.w
        
        expand_r = max(self.pex - self.im.shape[1], 0)
        self.im = np.pad(self.im, ((0, 0),(expand_l, expand_r),(0,0)))
        self.im[self.psy:self.pey, self.psx:self.pex, :] |= Text_line.colorize_char_image(cch.im, color)
        
        self.curs_offs = self.curs_offs + cch.xa + kern
    
    # init: init all attributes and render the text image
    def __init__(self, text, font):
        self.curs_offs = 0 # from border to cursor left
        
        assert(len(text) > 0)
        self.text, self.colors = Text_line.parse_text_color(text)
        self.font = font
                
        self.psy, self.pey = 0, 0
        self.psx, self.pex = 0, 0
        
        cch = self.font.chars[ord(self.text[0])]
        color = self.colors[0]
        
        # calculate placement point
        self.psy = cch.yo - self.font.line_et
        self.psx = self.curs_offs + cch.xo
        
        if self.psx < 0:
            self.curs_offs -= self.psx
            self.psx = 0
        
        self.pey = self.psy + cch.h
        self.pex = self.psx + cch.w
        
        self.im = np.zeros((self.font.line_eb + self.font.line_height - self.font.line_et, self.pex, 4), dtype=np.uint8)
        self.im[self.psy:self.pey, self.psx:self.pex, :] = Text_line.colorize_char_image(cch.im, color)
        
        self.first_curs_offs = self.curs_offs
        #cursor jump
        self.curs_offs += cch.xa
        
        for i in range(1, len(self.text)):
            pch = cch
            cch = self.font.chars[ord(self.text[i])]
            color = self.colors[i]
            self.place_char(cch, pch, color)
    
    # cat: concatenate the current text line with another textline
    def cat(self, new_text):
        assert(len(new_text) > 0)
        valid_text, colors = Text_line.parse_text_color(new_text)
        
        cch = self.font.chars[ord(self.text[-1])]
        
        for i in range(len(valid_text)):
            pch = cch
            cch = self.font.chars[ord(valid_text[i])]
            color = colors[i]
            self.place_char(cch, pch, color)

        self.text += valid_text # update the text held by the object
        self.colors += colors
        
        
class Text_box:    
    # render_align: render aligned text
    def render_align(self):
        if self.align == 'left':
            # calculate image size            
            global_cursor = 0
            global_text_w = 0
            
            # first line first
            if self.Text_lines[0] is not None:
                line_cursor = self.Text_lines[0].first_curs_offs
                line_text_w = self.Text_lines[0].im.shape[1] - line_cursor
                
                global_cursor = line_cursor if line_cursor > global_cursor else global_cursor
                global_text_w = line_text_w if line_text_w > global_text_w else global_text_w
                
            # next lines next
            for i in range(1,len(self.text_list)-1):
                if self.Text_lines[i] is not None:
                    line_cursor = self.Text_lines[i].first_curs_offs
                    line_text_w = self.Text_lines[i].im.shape[1] - line_cursor
                    
                    global_cursor = line_cursor if line_cursor > global_cursor else global_cursor
                    global_text_w = line_text_w if line_text_w > global_text_w else global_text_w
            
            # last line last
            if self.Text_lines[-1] is not None:
                line_cursor = self.Text_lines[-1].first_curs_offs
                line_text_w = self.Text_lines[-1].im.shape[1] - line_cursor
                
                global_cursor = line_cursor if line_cursor > global_cursor else global_cursor
                global_text_w = line_text_w if line_text_w > global_text_w else global_text_w
            
            im_w = global_cursor + global_text_w
            im_h = -self.font.line_et + self.font.line_height * len(self.text_list) + self.font.line_eb
            self.im = np.zeros((im_h, im_w, 4), dtype=np.uint8)
            
            # merge text line image
            # first line first
            ih = 0
            if self.Text_lines[0] is not None:
                line_cursor = self.Text_lines[0].first_curs_offs
                x_offs = global_cursor - line_cursor
                self.im[ih:ih+self.Text_lines[0].im.shape[0], x_offs:x_offs+self.Text_lines[0].im.shape[1], :] |= self.Text_lines[0].im
            ih += self.font.line_height
            
            for i in range(1, len(self.text_list)):
                if self.Text_lines[i] is not None:
                    line_cursor = self.Text_lines[i].first_curs_offs
                    x_offs = global_cursor - line_cursor
                    self.im[ih:ih+self.Text_lines[i].im.shape[0], x_offs:x_offs+self.Text_lines[i].im.shape[1], :] |= self.Text_lines[i].im
                ih += self.font.line_height
                    
        elif self.align == 'center':
            # calculate image size
            im_w = 0            
            # first line first
            if self.Text_lines[0] is not None:
                line_text_w = self.Text_lines[0].im.shape[1]
                im_w = line_text_w if line_text_w > im_w else im_w
                
            # next lines next
            for i in range(1,len(self.text_list)-1):
                if self.Text_lines[i] is not None:
                    line_text_w = self.Text_lines[i].im.shape[1]
                    im_w = line_text_w if line_text_w > im_w else im_w
            
            # last line last
            if self.Text_lines[-1] is not None:
                line_text_w = self.Text_lines[-1].im.shape[1]
                im_w = line_text_w if line_text_w > im_w else im_w
            
            im_h = -self.font.line_et + self.font.line_height * len(self.text_list) + self.font.line_eb
            self.im = np.zeros((im_h, im_w, 4), dtype=np.uint8)
            
            # merge text line image
            # first line first
            ih = 0
            if self.Text_lines[0] is not None:
                line_w = self.Text_lines[0].im.shape[1]
                x_offs = (im_w - line_w) // 2
                self.im[ih:ih+self.Text_lines[0].im.shape[0], x_offs:x_offs+self.Text_lines[0].im.shape[1], :] |= self.Text_lines[0].im
            ih += self.font.line_height
            
            for i in range(1, len(self.text_list)):
                if self.Text_lines[i] is not None:
                    line_w = self.Text_lines[i].im.shape[1]
                    x_offs = (im_w - line_w) // 2
                    self.im[ih:ih+self.Text_lines[i].im.shape[0], x_offs:x_offs+self.Text_lines[i].im.shape[1], :] |= self.Text_lines[i].im
                ih += self.font.line_height
    
        if self.align == 'right':
            # calculate image size
            im_w = 0
            
            global_cursor = 0
            global_text_w = 0
            
            # first line first
            if self.Text_lines[0] is not None:
                line_text_w = self.Text_lines[0].curs_offs
                line_cursor = self.Text_lines[0].im.shape[1] - line_text_w
                
                global_text_w = line_text_w if line_text_w > global_text_w else global_text_w
                global_cursor = line_cursor if line_cursor > global_cursor else global_cursor
                
            # next lines next
            for i in range(1,len(self.text_list)-1):
                if self.Text_lines[i] is not None:
                    line_text_w = self.Text_lines[i].curs_offs
                    line_cursor = self.Text_lines[i].im.shape[1] - line_text_w
                    
                    global_text_w = line_text_w if line_text_w > global_text_w else global_text_w
                    global_cursor = line_cursor if line_cursor > global_cursor else global_cursor
            
            # last line last
            if self.Text_lines[-1] is not None:
                line_text_w = self.Text_lines[-1].curs_offs
                line_cursor = self.Text_lines[-1].im.shape[1] - line_text_w
                
                global_text_w = line_text_w if line_text_w > global_text_w else global_text_w
                global_cursor = line_cursor if line_cursor > global_cursor else global_cursor
            
            im_w = global_cursor + global_text_w
            im_h = -self.font.line_et + self.font.line_height * len(self.text_list) + self.font.line_eb
            self.im = np.zeros((im_h, im_w, 4), dtype=np.uint8)
            
            # merge text line image
            # first line first
            ih = 0
            if self.Text_lines[0] is not None:
                line_text_w = self.Text_lines[0].curs_offs
                x_offs = global_text_w - line_text_w
                self.im[ih:ih+self.Text_lines[0].im.shape[0], x_offs:x_offs+self.Text_lines[0].im.shape[1], :] |= self.Text_lines[0].im
            ih += self.font.line_height
            
            for i in range(1, len(self.text_list)):
                if self.Text_lines[i] is not None:
                    line_text_w = self.Text_lines[i].curs_offs
                    x_offs = global_text_w - line_text_w
                    self.im[ih:ih+self.Text_lines[i].im.shape[0], x_offs:x_offs+self.Text_lines[i].im.shape[1], :] |= self.Text_lines[i].im
                ih += self.font.line_height
    
    # init: init all attributes and render the text image
    def __init__(self, text, font, align='left'):
        self.Text_lines = []
        assert(len(text) > 0)
        
        self.text_list = text.split('\n')
        for t in self.text_list:
            if len(t) > 0:
                self.Text_lines.append(Text_line(t, font))
            else:
                self.Text_lines.append(None)
            
        self.font = font
        self.align = align
        
        self.im = None
        
        self.render_align()
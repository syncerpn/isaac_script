# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 15:57:09 2021

@author: Syncer
"""

class Char:
    def __init__(self, cid, bmps, x, y, w, h, xo, yo, xa, page, chnl):
        self.id = cid
        self.xo = xo
        self.yo = yo
        self.xa = xa
        self.w = w
        self.h = h
        
        if chnl == 15:
            self.im = bmps[page][y:y+h, x:x+w, :]
        elif chnl == 8:
            self.im = bmps[page][y:y+h, x:x+w, 3]
        elif chnl == 4:
            self.im = bmps[page][y:y+h, x:x+w, 2]
        elif chnl == 2:
            self.im = bmps[page][y:y+h, x:x+w, 1]
        elif chnl == 1:
            self.im = bmps[page][y:y+h, x:x+w, 0]
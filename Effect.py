# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 16:09:33 2021

@author: Syncer
"""

import numpy as np
    
class Effect:
    @staticmethod
    def render(target, effect_list):
        output = np.copy(target)
        
        for e in effect_list:
            output = e(output)
        
        return output
    
    def __init__(self):
        self.drop_shadow = None
        self.scale = None
        
    # effect: add background
    def add_effect_background(self, background):
        self.background = background
    
    def remove_effect_background(self):
        self.background = None
    
    def r_background(self, target):
        assert(self.background is not None)
        tw = target.shape[1]
        th = target.shape[0]
        
        cropped_background = np.zeros((self.background.shape[0], tw, 4), dtype=np.uint8)
        cropped_background[:,0:tw//2,:] = self.background[:,0:tw//2,:]
        cropped_background[:, tw//2:,:] = self.background[:,-tw//2:,:]
        
        bw = cropped_background.shape[1]
        bh = cropped_background.shape[0]
        
        ow = max(bw, tw)
        oh = max(bh, th)
        
        output = np.zeros((oh, ow, 4), dtype=np.uint8)
        
        bx = (ow - bw) // 2
        by = (oh - bh) // 2
        output[by:by+bh, bx:bx+bw, :] = cropped_background
        
        tx = (ow - tw) // 2
        ty = (oh - th) // 2
        target_padded = np.pad(target, ((oh - th - ty, ty),(ow - tw - tx, tx), (0,0)))
        target_mask = target_padded[:,:,3] != 0
        output[target_mask, :] = target_padded[target_mask, :]
        return output
        
    # effect: drop shadow
    def add_effect_drop_shadow(self, drop_shadow):
        self.drop_shadow = drop_shadow
    
    def remove_effect_drop_shadow(self):
        self.drop_shadow = None
    
    def r_drop_shadow(self, target):
        assert(self.drop_shadow is not None)
        shadow = np.copy(target)
        
        expand_l = max(0, -self.drop_shadow[0])
        expand_r = max(0,  self.drop_shadow[0])
        expand_t = max(0, -self.drop_shadow[1])
        expand_b = max(0,  self.drop_shadow[1])
        
        output = np.pad(target, ((expand_t, expand_b),(expand_l, expand_r), (0,0)))
        output_mask = output[:,:,3] != 0 # alpha mask
        
        shadow = np.pad(target, ((expand_b, expand_t),(expand_r, expand_l), (0,0)))
        shadow_mask = shadow[:,:,3] != 0 # alpha mask
        shadow[shadow_mask, 0:3] = 0
        
        output_shadow_mask = (output_mask != shadow_mask) & shadow_mask
        output[output_shadow_mask, :] = shadow[output_shadow_mask, :] 
        # output[output_shadow_mask, 3] = 128
        return output
        
    # effect: scale
    def add_effect_scale(self, scale):
        self.scale = scale
    
    def remove_effect_scale(self):
        self.scale = None
        
    def r_scale(self, target):
        assert(self.scale is not None)
        return np.repeat(np.repeat(target, self.scale, axis = 0), self.scale, axis=1)
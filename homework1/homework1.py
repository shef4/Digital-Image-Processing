# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 14:12:20 2022

@author: sefun
"""
import math
import cv2
import os
import numpy as np

class Affine_Transformation():
    def __init__(self, img, mode='black'):
        self.img = img
        self.mode = mode
    
    def set_image(img):
        self.img = img
    
    def empty_image(self):
        img_res = None
        if self.mode == 'black':
            img_res = np.zeros(self.img.shape).astype(np.uint8)
        else:
            img_res = np.zeros(self.img.shape).astype(np.uint8)
            img_res[:][:][:] = 255
        return img_res
    
    #traverse image and apply mapping
    def transform_image(self, mapping):
        img_res = self.empty_image()
        for x in range(self.img.shape[1]):
            for y in range(self.img.shape[0]):
                new_x , new_y = mapping(x,y)
                if new_x >= self.img.shape[1] or new_x < 0: continue
                if new_y >= self.img.shape[0] or new_y < 0: continue
                img_res[new_y][new_x][:] = self.img[y][x][:] 
        return img_res
    
    #define maapping as function then call transform image
    def image_scale(self, sx, sy):
        def scale(x,y):
            return int(x*sx) , int(y*sy)
        img_res = self.transform_image(scale)
        return img_res
    
    def image_translate(self,tx, ty):
        def translate(x,y):
            return int(x+tx) , int(y+ty)
        img_res = self.transform_image(translate)
        return img_res
    
    def image_shear(self, sv, sh):
        def shear(x,y):
            return int(x+(y*sh)) , int(y+(x*sv))
        img_res = self.transform_image(shear)
        return img_res
    
    def image_rotate(self, r_theta):
        def rotate(x,y):
            return int((x*math.cos(r_theta))-(y*math.sin(r_theta))),int((x*math.sin(r_theta))+(y*math.cos(r_theta)))
        img_res = self.transform_image(rotate)
        return img_res
    
def main():
    path = "girl.tif"

    img = cv2.imread(path)

    at = Affine_Transformation(img, 'black')
    
    tx = 50
    ty = -100
    img_t = at.image_translate(tx, ty)
    cv2.imshow("Translated Image", img_t)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
 
    sx = 1
    sy = 2
    img_s = at.image_scale(sx, sy)
    cv2.imshow("Scaled Image", img_s)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    sv = 0.15
    sh = 1
    img_sh = at.image_shear(sv, sh)
    cv2.imshow("sheared Image", img_sh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    r_theta = -0.1
    img_r = at.image_rotate(r_theta)
    cv2.imshow("Rotated Image", img_r)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
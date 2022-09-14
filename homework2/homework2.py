# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 14:12:20 2022

@author: sefun
"""
import math
import cv2
import os
import numpy as np

class intXform4e():
    def __init__(self, img , mode=None, gamma = 1.0, normalize = True):
        self.img = img 
        if normalize:
            self.set_norm_image(img)
        self.MAX = 1
        self.mode = mode
        #run transform
        if self.mode == "neg":
            img_res = self.intensity_transform(self.neg_func)
        elif self.mode == "log":
            img_res = self.intensity_transform(self.log_func)
        elif self.mode == "gamma":
            img_res = self.intensity_transform(self.gamma_func, gamma)
        else:
            print("Transform function by calling self.intensity_transform(transform) where transform = self.FOO_func")
            return
        self.set_norm_image(img_res)

    def set_norm_image(self,img):
        img_norm = self.empty_image()
        img_norm = cv2.normalize(img,  img_norm, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        self.img = np.array(img_norm, dtype = np.float32)

    def set_image(self,img):
        #self.img = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        self.img = np.array(img, dtype = np.float32)

    def get_img(self):
        return self.img

    def empty_image(self):
        return np.zeros(self.img.shape).astype(np.float32)
    
    #traverse image and apply transform
    def intensity_transform(self, transform, gamma = None):
        new_img = self.empty_image()
        for y in range(self.img.shape[0]): #image traversal
            for x in range(self.img.shape[1]):
                #local pixel bound
                min_x , max_x= max(x-1,0) , min(x+2,self.img.shape[1]-1)
                min_y , max_y = max(y-1,0) , min(y+2,self.img.shape[0]-1)
                local_pixels = self.img[min_y:max_y , min_x:max_x]
                #set new intensity
                new_int = transform(local_pixels) if self.mode != "gamma" else transform(local_pixels, gamma) 
                new_img[y,x] = np.float32(new_int)
        return new_img

    # transform function
    def neg_func(self,local_pixels):
        mid_x= min(1,local_pixels.shape[1]-1)
        mid_y = min(1,local_pixels.shape[0]-1)
        return self.MAX - local_pixels[mid_y,mid_x,0]

    def log_func(self,local_pixels):
        mid_x= min(1,local_pixels.shape[1]-1)
        mid_y = min(1,local_pixels.shape[0]-1)
        #c = self.MAX/(np.log(1 + np.max(local_pixels)))
        c = 1
        return c*np.log(1 + local_pixels[mid_y,mid_x,0])

    def gamma_func(self,local_pixels, gamma):
        mid_x= min(1,local_pixels.shape[1]-1)
        mid_y = min(1,local_pixels.shape[0]-1)
        return self.MAX*(local_pixels[mid_y,mid_x,0]/self.MAX)**gamma

    
def main():
    path = "spillway-dark.tif"
    
    img = cv2.imread(path)
    
    mode = "neg"
    ixf = intXform4e(np.array(img, dtype = np.float32 ),mode)
    cv2.imshow(mode+" Intensity Image", ixf.get_img())
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(ixf.get_img())

    mode = "log"
    ixf = intXform4e(np.array(img, dtype = np.float32 ),mode)
    cv2.imshow(mode+" Intensity Image", ixf.get_img())
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(ixf.get_img())

    mode = "gamma"
    ixf = intXform4e(np.array(img, dtype = np.float32 ),mode)
    cv2.imshow(mode+" Intensity Image", ixf.get_img())
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(ixf.get_img())

    mode1 = "log"
    log = intXform4e(np.array(img, dtype = np.float32 ),mode1)
    mode2 = "gamma"
    gamma = 1.35
    ixf = intXform4e(np.array(log.get_img(), dtype = np.float32 ),mode2, gamma)
    cv2.imshow(mode1+" "+ mode2+" Intensity Image", ixf.get_img())
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(ixf.get_img())

if __name__ == "__main__":
    main()
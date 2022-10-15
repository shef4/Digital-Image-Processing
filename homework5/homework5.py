# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 14:12:20 2022

@author: sefun
"""
import math
import cv2
import matplotlib.pyplot as plt
import os
import numpy as np

class Noise_Filters():
    def __init__(self, img, mode="amf",window=1, threshold=0):
        self.img = img 
        self.mode = mode
        self.threshold = threshold
        self.window = window
        self.vlength = ((2*window)+1)**2
        self.set_image(img)
        #run transform
        img_res=None
        if mode=="amf":
            img_res = self.transform_image(self.adaptive_median_filter)
        else:
            img_res = self.transform_image(self.median_filter)
        self.set_image(img_res)

    def set_image(self,img):
        #self.img = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        self.img = np.array(img, dtype = np.uint8)

    def get_image(self):
        return self.img

    def empty_image(self):
        return np.zeros(self.img.shape).astype(np.uint8)
    
    #traverse image and apply transform
    def transform_image(self, transform):
        new_img = self.empty_image()
        for y in range(self.window,self.img.shape[0]-(self.window+1)): #image traversal
            for x in range(self.window,self.img.shape[1]-(self.window+1)):
                #local pixel bound
                min_x , max_x= x-self.window , x+(self.window+1)
                min_y , max_y = y-self.window , y+(self.window+1)
                pixel_window = self.img[min_y:max_y , min_x:max_x]
                #update intensity
                new_int = transform(pixel_window)
                new_img[y,x] = new_int
        return new_img

    def adaptive_median_filter(self,pixel_window):
        mid_x= pixel_window.shape[1]//2
        mid_y = pixel_window.shape[0]//2
        res = pixel_window[mid_y,mid_x]
        # #creat
        # target_vector = np.reshape(pixel_window, ((self.vlength),))
        #get median
        median = np.median(pixel_window[:,:,0])
        if self.threshold > 0:
            scale = np.absolute(pixel_window[:,:,0]-median)
            sk = 1.4826*np.median(scale)
            center_pixel_abs_diff=abs(pixel_window[mid_y,mid_x,0]-median)
            #if center pixel value greter than scale then it is an outlier
            if center_pixel_abs_diff>(self.threshold*sk):
                res = median
        else:
            res = median
        return res

    def median_filter(self,pixel_window):
        # Add median filter to image
        return np.median(pixel_window[:,:,0])

def main():
    path = "noisy_image.png"
    img = cv2.imread(path)
    # cv2.imshow("Noisy Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # adm filter
    # nf = Noise_Filters(img=img, mode="amf", window=1, threshold=0)
    # cv2.imshow("Adaptive Median Filtered Image", nf.get_image())
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    nf = Noise_Filters(img=img, mode="amf", window=100, threshold=0)
    cv2.imshow("Adaptive Median Filtered Image", nf.get_image())
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # median filter
    # nf = Noise_Filters(img, mode="mf")
    # cv2.imshow("Median Filtered Image", nf.get_image())
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
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

class Frequency_Filters():
    def __init__(self, img , mode=None, method="g",d0 = 10, n = 10, normalize = True):
        self.img = img 
        self.set_image(self.img,normalize)
        self.mode = mode
        self.method = method
        #create filter
        if self.mode=="lowpass":
            self.d0 = d0
            self.n = n
            self.filter = self.create_filter(self.lowpass)
        else:
            print("Filter generator requires function by calling self.create_filter(filter) where filter = FOO_func(u,v)")
            return
        #convert image to frequency domain
        self.img_freq = np.fft.fftshift(np.fft.fft2(self.img))
        #apply filter
        img_res_freq = self.img_freq*self.filter
        #convert result top spoactial domain and update image
        img_res = np.abs(np.fft.ifft2(np.fft.ifftshift(img_res_freq)))
        self.set_norm_image(img_res)

    def set_norm_image(self,img):
        img_norm = self.empty_image()
        img_norm = cv2.normalize(img,  img_norm, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        self.img = np.array(img_norm, dtype = np.float32)

    def set_image(self,img, normalize = True):
        self.img = np.array(img, dtype = np.float32)
        if normalize: 
            self.set_norm_image(self.img)

    def get_image(self):
        return self.img

    def empty_image(self):
        return np.zeros(self.img.shape).astype(np.float32)
    
    #traverse image and apply transform
    def create_filter(self, filter_func):
        new_filter = self.empty_image()
        for u in range(self.img.shape[0]): #image traversal
            for v in range(self.img.shape[1]):
                #set intensity
                new_filter[u,v] = np.float32(filter_func(u,v))
        return new_filter

    # transform function
    def lowpass(self,u,v):
        D = np.sqrt((u-self.img.shape[0]/2)**2 + (v-self.img.shape[1]/2)**2)
        intensity = 1
        if self.method == "g":
            intensity = np.exp(-D**2/(2*self.d0*self.d0))
        elif self.method == "bw":
            intensity = 1 / (1 + (D/self.d0)**self.n)
        return intensity


def main():
    path = "testpattern1024.tif"
    img = cv2.imread(path)
    # cv2.imshow("Original Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Gaussian filter
    # ff = Frequency_Filters( img=img , mode="lowpass", method="g",d0 = 200)
    # cv2.imshow("Gaussian Lowpass Filtered Image", ff.get_image())
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Butterworth filter
    ff = Frequency_Filters( img=img , mode="lowpass", method="bw",d0 = 100, n = 1)
    cv2.imshow("Butterworth Lowpass Filtered Image", ff.get_image())
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # # adm filter
    # path = "checkerboard1024-shaded.tif"
    # img = cv2.imread(path)
    # ff = Frequency_Filters( img=img , mode="lowpass", method="bw",d0 = 100, n = 10)
    # cv2.imshow("Butterworth Lowpass Filtered on Checker Board Image", ff.get_image())
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
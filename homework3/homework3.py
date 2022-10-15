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

class histogram_equalizor():
    def __init__(self, img):
        self.img = img 
        self.set_image(img)
        #run transform
        img_res = self.hist_eq()
        self.set_image(img_res)
        self.original_hist = None
        self.equalized_hist = None

    def set_image(self,img):
        #self.img = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        self.img = np.array(img, dtype = np.uint8)

    def get_img(self):
        return self.img

    def empty_image(self):
        return np.zeros(self.img.shape).astype(np.uint8)

    def hist_eq(self):
        #STEP 1: Normalized cumulative histogram
        img_array = np.asarray(self.img)
        histogram_array = np.bincount(img_array.flatten(), minlength=256)
        num_pixels = np.sum(histogram_array)
        histogram_array = histogram_array/num_pixels
        chistogram_array = np.cumsum(histogram_array)
        
        #STEP 2: Pixel mapping lookup table
        transform_map = np.floor(255 * chistogram_array).astype(np.uint8)

        #STEP 3: Transformation
        img_list = list(img_array.flatten())
        eq_img_list = [transform_map[p] for p in img_list]
        new_img = np.reshape(np.asarray(eq_img_list), img_array.shape)
        return new_img

def main():
    path = "low_contrast.png"
    img = cv2.imread(path)
    # cv2.imshow("Low Contrast Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    ixf = histogram_equalizor(img)
    cv2.imshow(" Historgram Equalized LC Image", ixf.get_img())
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    hist,bins = np.histogram(img.flatten(),256,[0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    plt.plot(cdf_normalized, color = 'b')
    plt.hist(img.flatten(),256,[0,256], color = 'r')
    plt.xlim([0,256])
    plt.legend(('cdf','orginal'), loc = 'upper left')
    plt.show()

    path = "high_contrast.jpg"
    img = cv2.imread(path)
    # cv2.imshow("High Contrast Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # ixf = histogram_equalizor(img)
    # cv2.imshow("Historgram Equalized HC Image", ixf.get_img())
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    hist,bins = np.histogram(img.flatten(),256,[0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    plt.plot(cdf_normalized, color = 'b')
    plt.hist(img.flatten(),256,[0,256], color = 'r')
    plt.xlim([0,256])
    plt.legend(('cdf','orginal'), loc = 'upper left')
    plt.show()

    path = "light_contrast.jpg"
    img = cv2.imread(path)
    # cv2.imshow("High Contrast Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    ixf = histogram_equalizor(img)
    cv2.imshow("Historgram Equalized LiC Image", ixf.get_img())
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    hist,bins = np.histogram(img.flatten(),256,[0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    plt.plot(cdf_normalized, color = 'b')
    plt.hist(img.flatten(),256,[0,256], color = 'r')
    plt.xlim([0,256])
    plt.legend(('cdf','orginal'), loc = 'upper left')
    plt.show()


    path = "dark_contrast.jpg"
    img = cv2.imread(path)
    # cv2.imshow("High Contrast Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    ixf = histogram_equalizor(img)
    cv2.imshow("Historgram Equalized DC Image", ixf.get_img())
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    hist,bins = np.histogram(img.flatten(),256,[0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    plt.plot(cdf_normalized, color = 'b')
    plt.hist(img.flatten(),256,[0,256], color = 'r')
    plt.xlim([0,256])
    plt.legend(('cdf','orginal'), loc = 'upper left')
    plt.show()



if __name__ == "__main__":
    main()
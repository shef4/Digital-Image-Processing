# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 14:12:20 2022

@author: sefun
"""
import math
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np


def brFilterTF4e(self,img,P,Q,C_n,W):
    
    crow,ccol = P//2 , Q//2
    kernel = np.zeros((P,Q), dtype=np.float)
    for u in range(P):
        for v in range(Q):
            D = np.sqrt((crow-u)**2 + (ccol-v)**2)
            num = D**2-C_n**2
            den = D*W if crow!=u or ccol!=v else 1
            kernel[u,v] = 1-(np.exp(-(num/den)**2))
    
    cv2.normalize(kernel, kernel, 1.0, 0, cv2.NORM_L1)
    
    res_img = cv2.filter2D(img,-1,kernel)

    return res_img

def gaussian_pyramid(self,img,max_lvl=None):
    #if max level not provided reduce still smaller axis reaches 1
    if max_lvl==None:
        max_lvl = int(np.log2(min(img.shape[:2])))
    gp = []
    curr_img = img
    for i in range(max_lvl+1):
        #add image
        gp.append(curr_img)
        # down sample 
        curr_img = cv2.pyrDown(curr_img)
    return gp

def laplacian_pyramid(self,img,max_lvl=None):
    #if max level not provided reduce still smaller axis reaches 1
    if max_lvl==None:
        max_lvl = int(np.log2(min(img.shape[:2])))
    lp = []
    curr_img = img
    kernel_size = (3,3)
    for i in range(max_lvl+1):
        # create image at level i
        blurred_img = cv2.blur(curr_img,kernel_size)
        L = cv2.subtract(curr_img,blurred_img)
        #add image
        lp.append(L)
        #down sample image
        curr_img = cv2.pyrDown(blurred_img)
    return lp




def main(): 

    # Problem 1 Results
    path1 = "test_images/apple_gray.jpg"
    img1 = cv2.imread(path1)
    cv2.imshow("P2 Original apple Image", img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #create gaussian pyramid
    p2_imgs = gaussian_pyramid(img1,3)
    for i,p2_img in enumerate(p2_imgs):
        cv2.imwrite('problem2/gp_lvl'+str(i)+'.png',p2_img)
        cv2.imshow('P2 New image',p2_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #create laplacian pyramid
    p2_imgs = laplacian_pyramid(img1,3)
    for i,p2_img in enumerate(p2_imgs):
        cv2.imwrite('problem2/lp_lvl'+str(i)+'.png',p2_img)
        cv2.imshow('P2 New image',p2_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # PROBLEM 3 RESULTS
    path = "periodicnoise.jpg"
    img = cv2.imread(path)
    # cv2.imshow("P3 Original Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    #set image
    mt = Midterm()

    #create image
    P = img.shape[0]+20
    Q = img.shape[1]+20
    C_n = 200
    W = 11500
    p3_img = brFilterTF4e(img,P,Q,C_n,W)
    cv2.imwrite('problem3/filtered_image.png',p3_img)
    cv2.imshow('P3 New image',p3_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()
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


def sobel_filters(img):
    print("gradient detection")
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)
    
    Ix = cv2.filter2D(src=img, ddepth=-1, kernel=Kx)
    Iy = cv2.filter2D(src=img, ddepth=-1, kernel=Ky)
    
    G = np.hypot(Ix, Iy)
    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix)
    
    return (G, theta)

def non_max_suppression(img, D):
    print("non max suppression")
    M, N = img.shape
    Z = np.zeros((M,N), dtype=np.float32)
    angle = D * 180. / np.pi
    angle[angle < 0] += 180

    
    for i in range(1,M-1):
        for j in range(1,N-1):
            try:
                q = 255
                r = 255
                
               #angle 0
                if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                    q = img[i, j+1]
                    r = img[i, j-1]
                #angle 45
                elif (22.5 <= angle[i,j] < 67.5):
                    q = img[i+1, j-1]
                    r = img[i-1, j+1]
                #angle 90
                elif (67.5 <= angle[i,j] < 112.5):
                    q = img[i+1, j]
                    r = img[i-1, j]
                #angle 135
                elif (112.5 <= angle[i,j] < 157.5):
                    q = img[i-1, j-1]
                    r = img[i+1, j+1]

                if (img[i,j] >= q) and (img[i,j] >= r):
                    Z[i,j] = img[i,j]
                else:
                    Z[i,j] = 0

            except IndexError as e:
                pass
    
    return Z

def threshold(img, lowThresholdRatio=0.03, highThresholdRatio=0.09):
    print("double threshold")
    highThreshold = img.max() * highThresholdRatio;
    lowThreshold = highThreshold * lowThresholdRatio;
    
    M, N = img.shape
    res = np.zeros((M,N), dtype=np.float32)
    
    weak = np.float32(0.3)
    strong = np.float32(1)
    
    strong_i, strong_j = np.where(img >= highThreshold)
    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))
    
    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak
    
    print("edge tracking")
    M, N = res.shape  
    for i in range(1, M-1):
        for j in range(1, N-1):
            if (res[i,j] == weak):
                try:
                    if ((res[i+1, j-1] == strong) or (res[i+1, j] == strong) or (res[i+1, j+1] == strong)
                        or (res[i, j-1] == strong) or (res[i, j+1] == strong)
                        or (res[i-1, j-1] == strong) or (res[i-1, j] == strong) or (res[i-1, j+1] == strong)):
                        res[i, j] = strong
                    else:
                        res[i, j] = 0
                except IndexError as e:
                    pass
    return res

def gaussian_pyramid(img,max_lvl=None):
    print("blur img")
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

def laplacian_pyramid(img,max_lvl=None):
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
    path = "rubics_cube.jpg"
    colorimg = cv2.imread(path)
    img1 = cv2.cvtColor(colorimg, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("P2 Original apple Image", img1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



    #create laplacian pyramid
    p2_imgs = laplacian_pyramid(img1,3)
    for i,p2_img in enumerate(p2_imgs):
        cv2.imwrite('results/log_lvl'+str(i)+'.png',p2_img)
        # cv2.imshow('P2 New image',p2_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


    #create gaussian pyramid
    p2_imgs = gaussian_pyramid(img1,3)
    # for i,p2_img in enumerate(p2_imgs):
    #     cv2.imwrite('results/gp_lvl'+str(i)+'.png',p2_img)
    #     G, theta = sobel_filters(p2_img)
    #     print(G.shape)
    #     print(theta.shape)
    #     g_img = np.zeros(G.shape)
    #     t_img = np.zeros(theta.shape)
    #     for x in range(G.shape[0]):
    #         for y in range(G.shape[1]):
    #             g_img[x,y] = G[x,y]
    #             t_img[x,y] = theta[x,y]

    #     cv2.imwrite('results/G_gp_lvl'+str(i)+'.png',g_img)
    #     cv2.imwrite('results/Theta_gp_lvl'+str(i)+'.png',t_img)

    #     p3_img = non_max_suppression(G, theta)
    #     cv2.imwrite('results/NMS_gp_lvl'+str(i)+'.png',p3_img)
        
    #     p4_img = threshold(p3_img, lowThresholdRatio=0.2, highThresholdRatio=0.22)
    #     cv2.imwrite('results/DT_ED_gp_lvl'+str(i)+'.png',p4_img)
    
    for i in range(4):
        G, theta = sobel_filters(p2_imgs[i])
        print(G.shape)
        print(theta.shape)
        g_img = np.zeros(G.shape)
        t_img = np.zeros(theta.shape)
        for x in range(G.shape[0]):
            for y in range(G.shape[1]):
                g_img[x,y] = G[x,y]
                t_img[x,y] = theta[x,y]
        cv2.imshow('P2 New image',g_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # cv2.imshow('P2 New image',t_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        p3_img = non_max_suppression(G, theta)
        # cv2.imshow('P2 New image',p3_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        p4_img = threshold(p3_img, lowThresholdRatio=0.2, highThresholdRatio=0.22)
        # cv2.imshow('P2 New image',p4_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    





if __name__ == "__main__":
    main()
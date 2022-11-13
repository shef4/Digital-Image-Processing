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

class Midterm():
    def desired_hist(self):
        a = 1/384
        res_hist = [0]*256
        for i in range(256):
            if i < 64 or i >191:
                res_hist[i] = 2*a
            elif 63 < i < 192:
                res_hist[i] = a
        return res_hist

    def find_nearest_above(self, desired_hist, data):
        diff = desired_hist - data
        mask = np.ma.less_equal(diff, -1)

        if np.all(mask):
            c = np.abs(diff).argmin()
            return c 
        masked_diff = np.ma.masked_array(diff, mask)
        return masked_diff.argmin()

    def hist_match(self,img):
        img = np.array(img, dtype = np.uint8)
        oldshape = img.shape
        img = img.ravel()

        bin_idx, curr_counts = np.unique(img, return_inverse=True,return_counts=True)[1:3]

        desired_counts = self.desired_hist()

        curr_hist_eq = np.cumsum(curr_counts).astype(np.float64)
        curr_hist_eq /= curr_hist_eq[-1]
        
        desired_hist_eq = np.cumsum(desired_counts).astype(np.float64)
        desired_hist_eq /= desired_hist_eq[-1]

        curr_hist = np.around(curr_hist_eq*255)
        desired_hist = np.around(desired_hist_eq*255)
        
        # Map the rounded values
        new_mapping=[]
        for data in curr_hist[:]:
            new_mapping.append(self.find_nearest_above(desired_hist,data))
        new_mapping= np.array(new_mapping,dtype='uint8')

        return new_mapping[bin_idx].reshape(oldshape)

    
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

    def image_blend(self,img1,img2,max_lvl=None):
        #if max level not provided reduce still smaller axis reaches 1
        if max_lvl==None:
            max_lvl = int(np.log2(min(img1.shape[0],img1.shape[1],img2.shape[0],img2.shape[1])))
        lp1 = self.laplacian_pyramid(img1)
        lp2 = self.laplacian_pyramid(img2)
        kernel = cv2.imread("test_images/mask_gray.jpg")
        k = self.gaussian_pyramid(kernel)
        LS = []
        for i,l in enumerate(zip(lp1,lp2)):
            cols = l[0].shape[1]
            l1 = l[0]*abs((k[i]//255)-1)
            l2 = l[1]*(k[i]//255)
            ls = np.hstack((l1[:,:cols//2], l2[:,cols//2:]))
            LS.append(ls)
        
        res_img = LS[-1]
        print(len(LS))
        for i in range(len(LS)-1,-1,-1):
            res_img = cv2.add(res_img, LS[i])
            res_img = cv2.pyrUp(res_img)
        return res_img




def main():
    
    # # PROBLEM 1 RESULTS
    # path = "high_contrast.jpg"
    # img = cv2.imread(path)
    # cv2.imshow("P1 Original Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # #set image
    # mt = Midterm()

    # #create image
    # p1_img = mt.hist_match(img)
    # cv2.imwrite('problem1/new_image.png',p1_img)
    # cv2.imshow('P1 New image',p1_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # #plot histogram
    # plt.hist(p1_img.flatten(),256,[0,256], color = 'b')
    # plt.hist(img.flatten(),256,[0,256], color = 'r')
    # plt.xlim([0,256])
    # plt.legend(('cdf','orginal'), loc = 'upper left')
    # plt.show()

    # #plot histogram transformation function
    # hist,bins = np.histogram(p1_img.flatten(),256,[0,256])
    # cdf = hist.cumsum()
    # cdf_normalized = cdf * float(hist.max()) / cdf.max()
    # plt.plot(cdf_normalized, color = 'b')
    # plt.xlim([0,256])
    # plt.show()

    # # Problem 2 Results
    # path1 = "test_images/apple_gray.jpg"
    # img1 = cv2.imread(path1)
    # path2 = "test_images/orange_gray.jpg"
    # img2 = cv2.imread(path2)
    # cv2.imshow("P2 Original apple Image", img1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imshow("P2 Original orange Image", img2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # #set image
    # mt = Midterm()

    # #create gaussian pyramid
    # p2_imgs = mt.gaussian_pyramid(img1,3)
    # for i,p2_img in enumerate(p2_imgs):
    #     cv2.imwrite('problem2/gp_lvl'+str(i)+'.png',p2_img)
    #     cv2.imshow('P2 New image',p2_img)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    # #create laplacian pyramid
    # p2_imgs = mt.laplacian_pyramid(img1,3)
    # for i,p2_img in enumerate(p2_imgs):
    #     cv2.imwrite('problem2/lp_lvl'+str(i)+'.png',p2_img)
    #     cv2.imshow('P2 New image',p2_img)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    # #create image blend
    # p2_img = mt.image_blend(img1,img2,3)
    # cv2.imwrite('problem2/img_blend.png',p2_img)
    # cv2.imshow('P2 New image',p2_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

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
    p3_img = mt.brFilterTF4e(img,P,Q,C_n,W)
    cv2.imwrite('problem3/filtered_image.png',p3_img)
    cv2.imshow('P3 New image',p3_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()
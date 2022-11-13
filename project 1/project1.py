# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 14:12:20 2022

@author: sefun
"""
import math,cmath
import matplotlib.pyplot as plt
import os
import cv2
from scipy.signal import gaussian
import scipy.fftpack as fp

import numpy as np

def im2freq(data): 
    return fp.rfft(fp.rfft(data, axis=0),axis=1)

def freq2im(f): 
    return fp.irfft(fp.irfft(f, axis=1),axis=0)

def wiener_filter(img, kernel):
    K = 35000*25
    res_img = np.zeros(img.shape)
    #read image and compute FFT
    g = img[:,:,0]
    G = np.fft.fft2(g)
    
    #2. pad kernels with zeros and compute fft
    h = kernel
    h_padded = np.zeros(g.shape[0:2]) 
    h_padded[:h.shape[0],:h.shape[1]] = np.copy(h)
    H = np.fft.fft2(h_padded)
    
    #3. Find the inverse filter term
    weiner_term = (abs(H)**2 + K)/(abs(H)**2)
    H_weiner = H*weiner_term
    # normalize to [0,1]
    H_norm = H_weiner/abs(H_weiner.max())
    
    G_norm = G/abs(G.max())
    F_temp = G_norm/H_norm
    F_norm = F_temp/abs(F_temp.max())
    
    #rescale to original scale
    F_hat  = F_norm*abs(G.max())
    
    f_hat = np.fft.ifft2( F_hat )
    res_img = abs(f_hat)
    return res_img

def inverse_filter(img, kernel):
    h = kernel
    res_img = np.zeros(img.shape)
    
    #1.read image and compute fft
    g = img[:,:,0]
    G = np.fft.fft2(g)
    
    #2. pad kernels with zeros and compute fft
    h_padded = np.zeros(g.shape[0:2]) 
    h_padded[:h.shape[0],:h.shape[1]] = np.copy(h)
    H =  np.fft.fft2(h_padded)
    
    # normalize to [0,1]
    H_norm = H/abs(H.max())
    G_norm = G/abs(G.max())
    F_temp = G_norm/H_norm
    F_norm = F_temp/abs(F_temp.max())
    
    #rescale to original scale
    F_hat  = F_norm*abs(G.max())
    
    # 3. apply Inverse Filter and compute IFFT
    f_hat = np.fft.ifft2(F_hat)
    res_img = abs(f_hat)

    return res_img

def gaussian_kernel(kernel_size = 3):
	h = gaussian(kernel_size, kernel_size / 3).reshape(kernel_size, 1)
	h = np.dot(h, h.transpose())
	h /= np.sum(h)
	return h

def motion_blur(a,b,T):
    # The greater the size, the more the motion.
    kernel_size = 30
    
    # Create the vertical kernel.
    kernel = np.zeros((kernel_size, kernel_size))
    
    # Fill the middle row with ones.
    for u in range(kernel_size):
        for v in range(kernel_size):
            if (u*a+v*b)==0:
                kernel[u,v] = T
            else:
                var = math.pi*(u*a+v*b)
                cvar = complex(0,var)
                kernel[u,v] = (T/var) * math.sin(var)* cmath.exp(cvar).real
    # Normalize.
    #kernel /= kernel_size
    kernel = kernel/abs(kernel.max())
    return kernel

def mean_squared_error(orignal_img,restored_img):
    #if max level not provided reduce still smaller axis reaches 1
    orignal_img = orignal_img[:,:,0]
    mse = np.sum((orignal_img.astype("float") - restored_img.astype("float")) ** 2)
    mse /= float(orignal_img.shape[0] * orignal_img.shape[1])
    return mse

def signal_to_noise_ratio(orignal_img,restored_img):
    #if max level not provided reduce still smaller axis reaches 1
    orignal_img = orignal_img[:,:,0]
    snr = np.sum(orignal_img.astype("float") ** 2)
    snr /= np.sum((orignal_img.astype("float") - restored_img.astype("float")) ** 2)
    snr = math.log10(snr)
    snr *= 10
    return snr


def main():
    path = "high_contrast.jpg"
    img = cv2.imread(path)

    a = 0.1
    b = 0.1
    T = 1
    kernel_g = gaussian_kernel()
    mb_kernel = motion_blur(a,b,T)
    mb_img = cv2.filter2D(img, -1, mb_kernel)

    sig = 0.0065
    mb_img1 = cv2.GaussianBlur(mb_img, (7, 7), sigmaX=sig)
    cv2.imshow('Motion Blurred Image sig=0.0065',mb_img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if_img1 = inverse_filter(mb_img1, kernel_g)
    mse_if1 = mean_squared_error(img,if_img1)
    snr_if1 = signal_to_noise_ratio(img,if_img1)
    print("Inverse Filtered Image sig=65 MSE =",mse_if1)
    print("Inverse Filtered Image sig=65 SNR =",snr_if1)    
    cv2.imshow('Inverse Filtered Image sig=0.0065',if_img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    wf_img1 = wiener_filter(mb_img1, kernel_g)
    mse_wf1 = mean_squared_error(img,wf_img1)
    snr_wf1 = signal_to_noise_ratio(img,wf_img1)
    print("Wiener Filtered Image sig=650 MSE =",mse_wf1)
    print("Wiener Filtered Image sig=650 SNR =",snr_wf1)
    cv2.imshow('Wiener Filtered Image sig=0.0065',wf_img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    sig = 65
    mb_img2 = cv2.GaussianBlur(mb_img, (7, 7), sigmaX=sig)
    cv2.imshow('Motion Blurred Image sig=65',mb_img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if_img2 = inverse_filter(mb_img2, kernel_g)
    mse_if2 = mean_squared_error(img,if_img2)
    snr_if2 = signal_to_noise_ratio(img,if_img2)
    print("Inverse Filtered Image sig=65 MSE =",mse_if2)
    print("Inverse Filtered Image sig=65 SNR =",snr_if2)
    cv2.imshow('Inverse Filtered Image sig=65',if_img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    wf_img2 = wiener_filter(mb_img2, kernel_g)
    mse_wf2 = mean_squared_error(img,wf_img2)
    snr_wf2 = signal_to_noise_ratio(img,wf_img2)
    print("Wiener Filtered Image sig=650 MSE =",mse_wf2)
    print("Wiener Filtered Image sig=650 SNR =",snr_wf2)
    cv2.imshow('Wiener Filtered Image sig=65',wf_img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    sig = 650
    mb_img3 = cv2.GaussianBlur(mb_img, (7, 7), sigmaX=sig)
    cv2.imshow('Motion Blurred Image sig=650',mb_img3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if_img3 = inverse_filter(mb_img3, kernel_g)
    mse_if3 = mean_squared_error(img,if_img3)
    snr_if3 = signal_to_noise_ratio(img,if_img3)
    print("Inverse Filtered Image sig=65 MSE =",mse_if3)
    print("Inverse Filtered Image sig=65 SNR =",snr_if3)
    cv2.imshow('Inverse Filtered Image sig=65',if_img3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    wf_img3 = wiener_filter(mb_img3, kernel_g)
    mse_wf3 = mean_squared_error(img,wf_img3)
    snr_wf3 = signal_to_noise_ratio(img,wf_img3)
    print("Wiener Filtered Image sig=650 MSE =",mse_wf3)
    print("Wiener Filtered Image sig=650 SNR =",snr_wf3)
    cv2.imshow('Wiener Filtered Image sig=650',wf_img3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





if __name__ == "__main__":
    main()
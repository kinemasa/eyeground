"""
血管強調を行う

morph血管強調フィルタ
等方性ウェーブレットフィルタ

input :眼底画像
output : 血管強調画像
"""

import cv2
import matplotlib.pyplot as plt
import math
import numpy as np
from skimage.exposure import rescale_intensity
import re
import glob
import sys
import os

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def extract_green_channel(file):
    img = cv2.imread(file)
    gr = np.zeros_like(img)
    gr = img[:,:,1]
    return gr


##カーネルとの畳み込み処理を行う
def convolve2D(image,kernel):
    (iH, iW) = image.shape
    (kH, kW) = kernel.shape
    pad = (kW - 1) // 2
    img = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    w = np.zeros((iH,iW), dtype = "float32")
    output = np.zeros((iH, iW), dtype = "float32")
    for y in np.arange(pad, iH + pad):
        for x in np.arange(pad, iW + pad):
            roi = img[y - pad:y + pad + 1, x - pad:x + pad + 1]
            output[y - pad,x - pad] = (roi * kernel).sum()
    
    w = image - output

    output = rescale_intensity(output, in_range = (0,255))
    output = (output * 255).astype("uint8")
    return output, w


def isotropic_undec_wavelet_filter2D(image):
    # Bi-spline cubic function is given by h
    c_prv = image
    C1 = 1. / 16.
    C2 = 4. / 16.
    C3 = 6. / 16.
    W = []
    kernel_sizes = [5,9,17]
    for idx, ks in enumerate(kernel_sizes):
        ks = ks//2
        kernel = np.zeros((1, kernel_sizes[idx]), dtype = 'float32')
        kernel[0][0] = C1
        kernel[0][kernel_sizes[idx]-1] = C1
        kernel[0][int(ks/2)] = C2
        kernel[0][int(kernel_sizes[idx]/4+ks)] = C2
        kernel[0][ks] = C3
        
      
        c_nxt, w = convolve2D(c_prv, kernel.T * kernel)
        c_prv = c_nxt
        W.append(w)
        A = kernel.T * kernel

    #     Computing the result Iiuw
    W1_median =cv2.medianBlur(W[1],3)
    W2_median =cv2.medianBlur(W[2],3)
    Iiuw = W[1]+W[2]
    
    # plt.imsave(output_dir +"wavelet.png",Iiuw)
    return Iiuw, c_nxt, W

def rotate_image(image, angle):
    height, width = image.shape[:2]
    image_center = (width / 2, height / 2)

    rotation_image = cv2.getRotationMatrix2D(image_center, angle, 1)

    radians = math.radians(angle)
    sin = math.sin(radians)
    cos = math.cos(radians)
    bound_w = int((height * abs(sin)) + (width * abs(cos)))
    bound_h = int((height * abs(cos)) + (width * abs(sin)))

    rotation_image[0, 2] += ((bound_w / 2) - image_center[0])
    rotation_image[1, 2] += ((bound_h / 2) - image_center[1])

    rotated_image = cv2.warpAffine(image, rotation_image, (bound_w, bound_h))
    return rotated_image 


if __name__ =="__main__":
    INPUT_DIR = "C:\\Users\\kine0\\tumuraLabo\\eyeground\\result-mini-integrate5\\tumu-13-mini1\\"
    files = sorted(glob.glob(INPUT_DIR+'*'), key=natural_keys)
    
    num = len(files)

    OUTPUT_DIR1= 'C:\\Users\\kine0\\tumuraLabo\\eyeground\\result-mini-wavelet\\'
    subject1= 'tumu-13-mini1'
    subject2= 'cafe15-tumu3-equalizehist'
    output_dir1 = OUTPUT_DIR1 + subject1+"\\"
    output_dir2 = OUTPUT_DIR1 + subject2+"\\"
    # os.mkdir(output_dir1)
    # os.mkdir(output_dir2)


    i = 0
    for f in files:
        img =f
        img_gray =cv2.imread(f,0)
        
        grChannel= extract_green_channel(img)
        filtered_result, _, W = isotropic_undec_wavelet_filter2D(grChannel)
        output_file = output_dir1 + str(i) +".png"
    
        # output_file2 = output_dir2 + str(i) +".png"
        plt.gray()
        plt.imsave(output_file,filtered_result)
        i += 1
        sys.stdout.flush()
        sys.stdout.write('\rProcessing... (%d/%d)' %(i,num))

    i = 0


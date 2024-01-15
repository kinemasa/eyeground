"""
入力したファイルに対して
5枚を一つの区切りとして位置補正を行う
0(mod 5)が基準
1,2,3,4(mod 5)枚目の写真と基準の写真との位置ずれを検出しAffine変換で補正する.
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


OUTPUT_DIR ="C:\\Users\\kine0\\labo\\ImageSensing2\\gantei\\BloodVessel\\result\\cafe15tumu1-stab\\"

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def stab(img_file):
    num = len(img_file)
    img1 =img_file[0]
    img1 =cv2.imread(img1)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY).astype(np.float32)
    k =0
    cv2.imwrite(OUTPUT_DIR +"stab0"+".png", img1)
    for k  in range(1,num):
        img2 = img_file[k]
        img2 = cv2.imread(img2)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY).astype(np.float32)
        (x, y), r = cv2.phaseCorrelate(gray1,gray2)
        print(x, y, r)

        W = img1.shape[1]
        H = img1.shape[0]


        

        # affine変換による平行移動
        M = np.float32([[1, 0, -x], [0, 1, -y]])
        aligned_img= cv2.warpAffine(gray2, M, (W, H))
        
       
        cv2.imwrite(OUTPUT_DIR +"stab" +str(k)+".png", aligned_img)








if __name__ == "__main__":

    INPUT_DIR ="C:\\Users\\kine0\\labo\\ImageSensing2\\gantei\\BloodVessel\\result\\cafe15tumu1-templetetriming\\"
    
    files = sorted(glob.glob(INPUT_DIR+'*'), key=natural_keys)
    
    
    num =len(files)
    stab(files)


    
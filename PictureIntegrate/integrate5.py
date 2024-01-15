"""
5枚ずつの画像の積算を行う

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


OUTPUT_DIR ="C:\\Users\\kine0\\labo\\ImageSensing2\\gantei\\BloodVessel\\result\\cafe15tumu1-addmean10\\"

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def addmean(img_file):
    num = len(img_file)
    
    img1  =  cv2.imread(img_file[0])
    h,w,_ = img1.shape
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY).astype(np.float32)
    
    for k  in range(0,num,10):
        base_array=np.zeros((h,w),np.float32)
        for  t in range(0,10):
            img =cv2.imread(img_file[k+t],0)
            base_array +=img

        base_array /= 10
        base_array = base_array.astype(np.uint8)
        cv2.imwrite(output_dir +"addmean" +str(k) +".png",base_array)



if __name__ == "__main__":

    INPUT_DIR ="C:\\Users\\kine0\\labo\\ImageSensing2\\gantei\\BloodVessel\\result\\cafe15tumu1-stab\\"
    
    files = sorted(glob.glob(INPUT_DIR+'*'), key=natural_keys)
    
    OUTPUT_DIR1= 'C:\\Users\\kine0\\tumuraLabo\\eyeground\\result\\'

    subject= 'sample'
    output_dir = OUTPUT_DIR1 + subject+"\\"
    os.mkdir(output_dir)

    
    addmean(files)

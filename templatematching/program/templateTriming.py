"""
テンプレートマッチングを用いて動画から対象の画像群を切り出す

input :眼底画像群フォルダ
output :テンプレートマッチングを行ってトリミングを行った画像群
"""

import cv2
import numpy as np
import glob
import sys
import os
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

  
# INPUT_DIR = "D:\\1214\\cafe100mg-15\\tumu1\\"
INPUT_DIR = "C:\\Users\\kine0\\labo\\ImageSensing2\\gantei\\BloodVessel\\result\\cafe15tumu1-addmean5\\"
files = glob.glob(INPUT_DIR+'*')
OUTPUT_DIR= 'C:\\Users\\kine0\\labo\\ImageSensing2\\gantei\\BloodVessel\\result\\\\'
temp = cv2.imread("C:\\Users\\kine0\\labo\\ImageSensing2\\templete-example.png")
num = len(files)

##import picture
img_name = files[0]
img = cv2.imread(img_name)
img_copy=cv2.imread(img_name)

width = int(img.shape[1])
height = int(img.shape[0])



##import picture
i = 0
for f in files:
    basename=os.path.basename(f)
    root, ext = os.path.splitext(basename)

    img = cv2.imread(f)
    
    
    ##template matching
    temp_height,temp_width = temp.shape[:2]
    match = cv2.matchTemplate(img,temp,cv2.TM_CCOEFF_NORMED)#ZNCC
    min_value,max_value ,min_pt,max_pt = cv2.minMaxLoc(match)
    pt = max_pt

    selectRoi_crop = img[int(pt[1]):int(pt[1]+temp_height),int(pt[0]):int(pt[0]+temp_width)]
    output_file = OUTPUT_DIR + str(i) +".png"
    cv2.imwrite(output_file,selectRoi_crop)
    i += 1

    sys.stdout.flush()
    sys.stdout.write('\rProcessing... (%d/%d)' %(i,num))

i = 0


if __name__ =="__main__":

    ## input
    # INPUT_DIR = "D:\\1214\\cafe100mg-15\\tumu1\\"
    INPUT_DIR = "C:\\Users\\kine0\\labo\\ImageSensing2\\gantei\\BloodVessel\\result\\cafe15tumu1-addmean5\\"
    files = glob.glob(INPUT_DIR+'*')
    files = sorted(glob.glob(INPUT_DIR+'*'), key=natural_keys)
    temp = cv2.imread("C:\\Users\\kine0\\labo\\ImageSensing2\\templete-example.png")

    OUTPUT_DIR1= 'C:\\Users\\kine0\\labo\\ImageSensing2\\gantei\\BloodVessel\\result\\'

    subject= 'sample'
    output_dir = OUTPUT_DIR1 + subject
    os.mkdir(output_dir)

    
    num = len(files)

    ##import picture
    i = 0
    for f in files:
        img = cv2.imread(f)
        ##template matching
        temp_height,temp_width = temp.shape[:2]
        match = cv2.matchTemplate(img,temp,cv2.TM_CCOEFF_NORMED)#ZNCC
        min_value,max_value ,min_pt,max_pt = cv2.minMaxLoc(match)
        pt = max_pt
        selectRoi_crop = img[int(pt[1]):int(pt[1]+temp_height),int(pt[0]):int(pt[0]+temp_width)]
        output_file =output_dir +str(i) +".png"
        cv2.imwrite(output_file,selectRoi_crop)
        i += 1

    sys.stdout.flush()
    sys.stdout.write('\rProcessing... (%d/%d)' %(i,num))

i = 0
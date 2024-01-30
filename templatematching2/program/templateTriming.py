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



if __name__ =="__main__":

    ## input
    INPUT_DIR = "C:\\Users\\kine0\\tumuraLabo\\eyeground\\result\\tumu-13-contrast\\"
    files = glob.glob(INPUT_DIR+'*')
    files = sorted(glob.glob(INPUT_DIR+'*'), key=natural_keys)
    temp = cv2.imread("C:\\Users\\kine0\\tumuraLabo\\eyeground\\eyeground\\templatematching2\\result\\tumu-13-mini1-template.png",0)

    OUTPUT_DIR1= 'C:\\Users\\kine0\\tumuraLabo\\eyeground\\result-mini\\'

    subject= 'tumu-13-mini-1'
    output_dir = OUTPUT_DIR1 + subject+"\\"


    os.mkdir(output_dir)

    
    num = len(files)

    ##import picture
    i = 0
    for f in files:
        img = cv2.imread(f,0)
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
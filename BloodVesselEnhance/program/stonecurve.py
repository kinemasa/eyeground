"""
トーンカーブを用いることで画像全体のコントラストを上昇させる

input :入力画像
output : コントラスト強調画像
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import re
import glob
import sys

def sigmoidTone(input_img):
    output_float = 255 / (1 + np.exp(-0.05 * (input_img - 57.5) ) ) # 計算結果をいったん実数型(float)で保持
    return output_float.astype(np.uint8)

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]



if __name__ =="__main__":

    ## input
    INPUT_DIR = "C:\\Users\\kine0\\tumuraLabo\\eyeground\\result\\cafe15tumu2-addmean\\"
    files = glob.glob(INPUT_DIR+'*')
    files = sorted(glob.glob(INPUT_DIR+'*'), key=natural_keys)
    

    OUTPUT_DIR1= 'C:\\Users\\kine0\\tumuraLabo\\eyeground\\result\\'

    subject= 'cafe15-tumu2-stone'
    output_dir = OUTPUT_DIR1 + subject+"\\"


    # os.mkdir(output_dir)

    
    num = len(files)

    ##import picture
    i = 0
    for f in files:
        img = cv2.imread(f,0)
        ##template matching
        stone =sigmoidTone(img)
        output_file =output_dir +str(i) +".png"
        plt.gray()
        plt.imsave(output_file,stone)
        # cv2.imwrite(output_file,stone)
        i += 1

        sys.stdout.flush()
        sys.stdout.write('\rProcessing... (%d/%d)' %(i,num))

i = 0


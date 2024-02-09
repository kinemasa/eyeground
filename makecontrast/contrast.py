"""
y=ax +b　の形でコントラストを強調する

input :眼底画像群フォルダ
output :コントラスト強調画像群
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
    INPUT_DIR = "C:\\Users\\kine0\\tumuraLabo\\eyeground\\result\\tumu-1\\"
    files = glob.glob(INPUT_DIR+'*')
    files = sorted(glob.glob(INPUT_DIR+'*'), key=natural_keys)
    OUTPUT_DIR1= 'C:\\Users\\kine0\\tumuraLabo\\eyeground\\result\\'

    subject= 'tumu-13-contrast'
    output_dir = OUTPUT_DIR1 + subject+"\\"

    # os.mkdir(output_dir)
    



    
    num = len(files)

    ##import picture
    i = 0
    for f in files:
        img = cv2.imread(f,0)
        # コントラストと明るさの変更
        alpha = 1.5  # コントラストの倍率（1より大きい値でコントラストが上がる）
        beta = -130  # 明るさの調整値（正の値で明るくなる
        adjusted_image = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        
        output_file =output_dir +str(i) +".png"
        cv2.imwrite(output_file,adjusted_image)
        i += 1

        sys.stdout.flush()
        sys.stdout.write('\rProcessing... (%d/%d)' %(i,num))

i = 0



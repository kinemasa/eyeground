"""
元画像を二値化して細繊化アルゴリズムを施すコード

入力；画像フォルダ群
出力：細線可アルゴリズム適応して元画像の真ん中に線を引いたもの

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


def binary_otsu(img,i):
    img =cv2.imread(img,0)
    ret, img_otsu = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
    cv2.imwrite(OUTPUT_DIR1 +str(i)+".png",img_otsu)

# 表示
def display_result_image(cap, color_image, skeleton,i):
    colorimg = color_image.copy()

    # カラー画像に細線化を合成
    colorimg = colorimg 
    colorimg[skeleton == 255] = 0

    # cv2.imshow(cap + '_skeleton', skeleton)
    # cv2.imshow(cap + '_color image', colorimg)
    # cv2.waitKey(0)
    cv2.imwrite(OUTPUT_DIR+subject1 +"-colorimg.png",colorimg)
    cv2.imwrite(OUTPUT_DIR +subject1+"-skelton.png",skeleton)

# 細線化
def thinning(img,i):
    img =cv2.imread(img,0)
    _, gray = cv2.threshold(img, 0, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # 二値画像反転
    image = 255-gray

    # # 細線化(スケルトン化) THINNING_ZHANGSUEN
    # skeleton1   =   cv2.ximgproc.thinning(image, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    # display_result_image('ZHANGSUEN', img, skeleton1)

    # 細線化(スケルトン化) THINNING_GUOHALL 
    skeleton2   =   cv2.ximgproc.thinning(image, thinningType=cv2.ximgproc.THINNING_GUOHALL)
    display_result_image('GUOHALL', img, skeleton2,i)








if __name__ == "__main__":

    INPUT_DIR ="C:\\Users\\kine0\\tumuraLabo\\eyeground\\result-mini-all\\cafe60-tumu2\\"

    OUTPUT_DIR ="C:\\Users\\kine0\\tumuraLabo\\eyeground\\result-mini-thinning\\"
    

    subject1 = "cafe60-tumu2"
    files = sorted(glob.glob(INPUT_DIR+'*'), key=natural_keys)
    
    for  i, file in enumerate(files):
        thinning(file,i)



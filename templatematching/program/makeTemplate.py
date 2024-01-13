"""
テンプレートマッチングに用いるテンプレート画像を作成する

input :眼底画像 
output :テンプレート画像
"""
import cv2
import numpy as np
import glob
import sys
import csv
import re
import os


def getVideoROI(img):
    roi = cv2.selectROI(img)
    cv2.destroyAllWindows()
    return roi




if __name__ == "__main__":

    ## import dir_file
    dir_name = 'D:\\1214\\cafe100mg-15\\tumu1\\'
    # dir_name = "C:\\Users\\kine0\\labo\\ImageSensing2\\gantei\\BloodVessel\\result\\cafe15tumu1-addmean5\\"
    files = glob.glob(dir_name+'*')

    ## output file
    OUTPUT_DIR = "C:\\Users\\kine0\\tumuraLabo\\eyeground\\eyeground\\templatematching\\result\\"
    subject ="sample"
    ## import First file
    imgFirst_name = files[0]
    img = cv2.imread(imgFirst_name)
    width = int(img.shape[1])
    height = int(img.shape[0])
    
    roi = getVideoROI(img)
    ## crop
    selectRoi_crop = img[int(roi[1]):int(roi[1]+roi[3]),int(roi[0]):int(roi[0]+roi[2])]
    ##checkROI
    cv2.rectangle(img,(roi[0],roi[1]),(roi[0]+roi[2],roi[1]+roi[3]),(0,0,200),3)

    ##OUTPUT

    cv2.imwrite(OUTPUT_DIR+subject+"-template.png", selectRoi_crop)

    cv2.imwrite(OUTPUT_DIR+subject+"-checktemplate.png", img)
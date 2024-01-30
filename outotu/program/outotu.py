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


def unevenness(img, kernel,i):	# 凹凸係数
    img =cv2.imread(img)
    blur = cv2.blur(img, kernel)

    img = img/blur
    img = np.clip(img*255, 0, 255).astype(np.uint8)
    cv2.imwrite(output_dir+str(i)+".png",img)
    




if __name__ == "__main__":

    INPUT_DIR ="C:\\Users\\kine0\\tumuraLabo\\eyeground\\result-mini-wavelet\\cafe15-tumu1-mini1\\"
    OUTPUT_DIR1 ="C:\\Users\\kine0\\tumuraLabo\\eyeground\\result-outotu\\"

    subject ="cafe15-tumu1-mini1"
    output_dir = OUTPUT_DIR1 + subject +"\\"
    # os.mkdir(output_dir)
    files = sorted(glob.glob(INPUT_DIR+'*'), key=natural_keys)
    
    for  i, file in enumerate(files):
        unevenness(file,(51,51),i)

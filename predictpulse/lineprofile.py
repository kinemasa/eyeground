"""
ラインプロファイルによって血管径の変動を確認する
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy import ndimage
import math
from skimage.measure import profile_line
from scipy.interpolate import interp1d
from scipy import signal
import glob
import os
import re
import csv
from sklearn import preprocessing


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


#ブレゼンハムアルゴリズム。指定した2点がつくる線分を構成する座標と輝度値を返す。
def bresenham_march(img, p1, p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    #tests if any coordinate is outside the image
    if (   x1 >= img.shape[0]
        or x2 >= img.shape[0]
        or y1 >= img.shape[1]
        or y2 >= img.shape[1]
    ): #tests if line is in image, necessary because some part of the line must be inside, it respects the case that the two points are outside
        if not cv2.clipLine((0, 0, *img.shape), p1, p2):
            print("not in region")
            return
    steep = math.fabs(y2 - y1) > math.fabs(x2 - x1)
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    # takes left to right
    also_steep = x1 > x2
    if also_steep:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    dx = x2 - x1
    dy = math.fabs(y2 - y1)
    error = 0.0
    delta_error = 0.0
    # Default if dx is zero
    if dx != 0:
        delta_error = math.fabs(dy / dx)
    y_step = 1 if y1 < y2 else -1
    y = y1
    ret = []
    for x in range(x1, x2):
        p = (y, x) if steep else (x, y)
        if p[0] < img.shape[0] and p[1] < img.shape[1]:
            #ret.append((p, img[p]))
            ret.append([p[0], p[1], img[p[0]][p[1]]])   #この1文だけオリジナルから変更している
        error += delta_error
        if error >= 0.5:
            y += y_step
            error -= 1
    if also_steep:  # because we took the left to right instead
        ret.reverse()
    return ret

    #バターワースフィルタ（ローパス）
def lowpass(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2                           #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "low")            #フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)                  #信号に対してフィルタをかける
    return y            

#バターワースフィルタ（バンドパス）
def bandpass(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2 #ナイキスト周波数
    wp = fp / fn  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "band") #フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x) #信号に対してフィルタをかける
    return y  



def bandpass_filter_pulse(pulse, band_width, sample_rate):
    """
    バンドパスフィルタリングにより脈波をデノイジングする．

    Parameters
    ---------------
    pulse : np.float (1 dim)
        脈波データ
    band_width : float (1dim / 2cmps)
        通過帯 [Hz] (e.g. [0.75, 4.0])
    sample_rate : int
        データのサンプルレート

    Returns
    ---------------
    pulse_sg : np.float (1 dim)
        デノイジングされた脈波

    """

    # バンドパスフィルタリング
    nyq = 0.5 * sample_rate
    b, a = signal.butter(1, [band_width[0] / nyq, band_width[1] / nyq], btype='band')
    pulse_bp = signal.filtfilt(b, a, pulse)

    return pulse_bp



if  __name__ == "__main__":

    INPUT_DIR ="C:\\Users\\kine0\\labo\\ImageSensing2\\gantei\\BloodVessel\\result\\cafe15tumu1-minitrimingoutotu\\"

    
    OUTPUT_DIR1= 'C:\\Users\\kine0\\tumuraLabo\\eyeground\\result\\'

    subject= 'lineprofile'
    output_dir = OUTPUT_DIR1 + subject+"\\"
    os.mkdir(output_dir)
    output_file= output_dir +"\\result.csv"

    files = sorted(glob.glob(INPUT_DIR+'*'), key=natural_keys)
    
    ## start_point,end_point
    sx =28
    sy =22
    ex =31
    ey =33


    start = (sy, sx)
    end = (ey, ex)
    fwhm_value =[]
    for file in files:
        profile_value =[]
        center_value =[]
        img = cv2.imread(file,0)
        temp = img.copy()

        profile = bresenham_march(img, start, end)
        length = len(profile)
        x = np.arange(length)   

        for i in range(length):
            profile_value.append(profile[i][2])

        
        fmin =float(min(profile_value))
        fmax =float(max(profile_value))
        center = (fmax+fmin)/2

        for i in range(length):
            center_value.append(center)
        
        func1 = interp1d(x,profile_value,kind="cubic")
        func2 = interp1d(x,center_value,kind="cubic")
        x1 = np.arange(min(x),max(x),0.01)
        y1=func1(x1)
        y2=func2(x1)
        # 交点の座標を取得
        idx = np.argwhere(y1 - y2  < 0.001)
        fwhm = len(idx)
        
        fwhm_value.append(fwhm)
        # cv2.line(temp,(sx,sy),(ex,ey),(0,0,255),1) 
        # cv2.namedWindow('temp',cv2.WINDOW_NORMAL)
        # cv2.imshow("temp",temp)
        # plt.plot(x1, y1)
        # plt.plot(x1,y2)
        # plt.plot(x1[idx], y2[idx],label='Intersection',color='green')
        # plt.show()

    




    normalized_fwhm = preprocessing.minmax_scale(fwhm_value)
    fp1 = 3 #通過域端周波数[Hz]
    fs1 = 5       #阻止域端周波数[Hz]
    # fp2 = 0.75       #阻止域端周波数[Hz]
    # fs2 = 0.74       #阻止域端周波数[Hz]
    gpass = 3       #通過域端最大損失[dB]
    gstop = 10      #阻止域端最小損失[dB]

    samplerate = 60
    data_filt =bandpass_filter_pulse(normalized_fwhm, [0.75,5.0], samplerate)
    # data_filt1 =lowpass(fwhm_value,samplerate,fp1,fp1,gpass,gstop)
    # data_filt2 =highpass(data_filt1,samplerate,fp2,fp2,gpass,gstop)

    with open(output_file, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        
        for val in data_filt:
            writer.writerow([val])
        




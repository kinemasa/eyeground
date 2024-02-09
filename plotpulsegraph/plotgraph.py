"""
csvファイルからグラフを作成する

input :csvファイル
output :グラフ画像
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
import numpy as np
from scipy.interpolate import interp1d
from scipy import signal
from sklearn import preprocessing

def spline_interp(in_x, in_y):
    out_x = np.linspace(np.min(in_x), np.max(in_x), np.size(in_x)*100) # もとのxの個数より多いxを用意
    func_spline = interp1d(in_x, in_y, kind='cubic') # cubicは3次のスプライン曲線
    out_y = func_spline(out_x) # func_splineはscipyオリジナルの型

    return out_x, out_y

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

save__filename ="C:\\Users\\kine0\\tumuraLabo\\eyeground\\result.png"
df=pd.read_csv("C:\\Users\\kine0\\tumuraLabo\\eyeground\\interpolate\\cafe15-tumu1-mini-1\\interpolate101.csv")
x = df.index.values.tolist()
y = df.iloc[:,0]
# band_df = bandpass_filter_pulse(y,[0.75,5.0],60)
x =x[0:36]
y =y[0:36]

x2, y2 = spline_interp(x, y)
fig,ax = plt.subplots()

ax.plot(x2, y2, color='darkorange', label='spline', alpha=0.7)
# ax.plot(time, pulse, color='g',label="linear", alpha=0.7)

plt.legend()
# plt.xticks(np.arange(0, 20, 1))
# plt.yticks(np.arange(-0.2, 0.3, 0.05))
plt.savefig(save__filename)
plt.show()


# plt.plot(time,pulse)
# plt.show()

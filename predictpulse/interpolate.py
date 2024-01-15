"""
ラインプロファイルで算出した値に対して
テンプレートマッチングが出来ていない箇所を取り除き
３次スプライン補間を行う
"""

import pandas as pd 
import numpy as np
import csv

OUTPUT_FILE ="C:\\Users\\kine0\\tumuraLabo\\eyeground\\result\\result.csv"
#データをdfに読み込み。pandasをpdとして利用。
df = pd.read_csv("C:\\Users\\kine0\\labo\\ImageSensing2\\gantei\\BloodVessel\\result\\mean.csv",header=None)

#dfの中身を確認
df_new = df.iloc[0:225,0]
print(df_new)
df_new[5]= np.nan
df_new[6]= np.nan
df_new[36]= np.nan
df_new[50]= np.nan
df_new[51]= np.nan
df_new[52]= np.nan
df_new[53]= np.nan
df_new[54]= np.nan
df_new[99]= np.nan
df_new[105]= np.nan
df_new[152]= np.nan
df_new[225]= np.nan

print(df_new.info())
df_interporate = df_new
df_interporate.interpolate('cubic',inplace=True)

with open(OUTPUT_FILE, 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for val in df_interporate:
        writer.writerow([val])

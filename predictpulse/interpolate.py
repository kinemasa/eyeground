"""
ラインプロファイルで算出した値に対して
テンプレートマッチングが出来ていない箇所を取り除き
３次スプライン補間を行う

input :lineprofile.csv
output : スプライン補間を行った後のcsv
"""

import pandas as pd 
import numpy as np
import csv
import os
OUTPUT_DIR1 ="C:\\Users\\kine0\\tumuraLabo\\eyeground\\interpolate\\"
subject ="takahashi-1-mini1"
ouput_dir = OUTPUT_DIR1 +subject
# os.makedirs(ouput_dir)
output_file = ouput_dir+"\\interpolate3.csv"

#データをdfに読み込み。pandasをpdとして利用。
df = pd.read_csv("C:\\Users\\kine0\\tumuraLabo\\eyeground\\lineprofile\\takahashi-1-mini1\\lineprofile3.csv",header=None)

#dfの中身を確認
df_new = df.iloc[0:241,0]
print(df_new)


# df_new[4]= np.nan
# df_new[89]= np.nan
# df_new[90] =np.nan
# df_new[96]= np.nan
# df_new[147]= np.nan
# df_new[148]= np.nan
# df_new[149]= np.nan








print(df_new.info())
df_interporate = df_new
df_interporate.interpolate('spline',order =3 ,inplace=True)

with open(output_file, 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for val in df_interporate:
        writer.writerow([val])

"""
テンプレートマッチングを用いて対象を抜き出し確認する

input :眼底画像 テンプレート画像
output :テンプレートマッチング結果画像
"""

import cv2

if __name__ =="__main__":
   #input image
   img = cv2.imread('sample.png')
   temp = cv2.imread("template.png")
   ## output file
   OUTPUT_DIR = "..\\result\\"
   subject ="sample"
   
   
   height,width = temp.shape[:2]
   
   
   ##template matching
   match = cv2.matchTemplate(img,temp,cv2.TM_CCOEFF_NORMED)#ZNCC
   min_value,max_value ,min_pt,max_pt = cv2.minMaxLoc(match)
   pt = max_pt

   ##output result
   cv2.rectangle(img,(pt[0],pt[1]),(pt[0]+width,pt[1]+height),(0,0,200),3)
   cv2.imwrite(OUTPUT_DIR+subject+"-templateresulted.png",img)
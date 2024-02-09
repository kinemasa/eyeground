# eyeground
卒業研究で用いた眼底画像処理用のプログラム

結果はテンプレートはgit 管理　

複数画像になる場合はgit管理外に出す

## １．BloodVesselEnhance
眼底血管を強調するための処理を行う

## ２．makecontrast
コントラスト強調

## ３．outotu
照明ムラ補正
## ４．pictureintegrate
画像積算
## ５．position
位置補正

## ６．templatematching
テンプレートマッチングを行う

## 7．thinnig
二値化と細線化を行い中心線を求める

# 実行順番
眼底写真フォルダを用意した後
2(コントラスト強調)->6(テンプレートマッチング)->5(位置合わせ)->4(画像平均化)->7(血管強調フィルタ)


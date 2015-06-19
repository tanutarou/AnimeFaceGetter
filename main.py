# -*- coding: utf-8 -*-
import cv2
import json
import os
import urllib2

def GetAnimeFace(image_path, key, num):
    #顔画像保存ディレクトリの作成
    if os.path.exists(key + "_face")==False:
        os.mkdir(key + "_face")

    #分類器のパス
    cascade_path = "./lbpcascade_animeface.xml"
    #ファイルの読み込み
    image = cv2.imread(image_path)
    #グレースケールに変換
    image_gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    #特徴量の取得
    cascade = cv2.CascadeClassifier(cascade_path)
    #顔認識
    facerect = cascade.detectMultiScale(image_gray, minNeighbors=1, minSize=(1, 1))

    print "number of detect faces:",len(facerect)

    if len(facerect) > 0:
        for i,rect in enumerate(facerect):
            #検出された領域でトリミング
            trimmed = image[rect[1]:(rect[1]+rect[3]), rect[0]:rect[0]+rect[2]]
            #作成するファイル名
            mkfilename = key+"_face//img" + str(num) + "face" + str(i) + ".jpg"
            #ファイルに出力
            cv2.imwrite(mkfilename, trimmed)

def ImgSearch(key, n):
    img_url = []
    url = "http://ajax.googleapis.com/ajax/services/search/images?q={0}&v=1.0&rsz=large&start={1}"
    #一度に取得できる画像が８個まで？
    for i in range((n/8)+1):
        res = urllib2.urlopen(url.format(key, i*8))
        #jsonファイルを読み込む
        data = json.load(res)
        #urlを抽出する
        img_url += [result["url"] for result in data["responseData"]["results"]]

    return img_url

def ImgDownload(key, urls):
    print "Download Start..."
    if os.path.exists(key)==False:
        os.mkdir(key)

    opener = urllib2.build_opener()
    for i in range(len(set(urls))):
        try:
            #拡張子をextに取得,rootはそれ以外
            root, ext = os.path.splitext(urls[i])
            req = urllib2.Request(urls[i])
            img_file = open(key+"//"+str(i)+ext, "wb")
            img_file.write(opener.open(req).read())
            img_file.close()
            GetAnimeFace(key+"//"+str(i)+ext, key, i)
            print "Download ",key + str(i)
        except:
            continue
    print "Download End"

def main():
    key = "%E3%82%A2%E3%83%8B%E3%83%A1"
    urls = ImgSearch(key, 10)
    ImgDownload(key, urls)

main()

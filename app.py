#参考　https://punhundon-lifeshift.com/tesseract_ocr
from PIL import Image
import sys

import os

import pyocr
import pyocr.builders

import re

# インストール済みのTesseractのパスを通す
path_tesseract = r"C:\Program Files\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

# OCRエンジンの取得
tools = pyocr.get_available_tools()
tool = tools[0]


tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))


langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))

lang_num=1
lang = langs[lang_num]
print("Will use lang '%s'" % (lang))

input_name = input("ファイルの名前を入力してください。")

#画像ファイルの場所を指定（一回目）
input_file = input("ファイルのパスを入力してください。")

#日本語で読み込み
txt = tool.image_to_string(
    Image.open(input_file),
    lang="jpn",
    builder=pyocr.builders.TextBuilder(tesseract_layout=3))

#正規表現操作

txt = re.sub('([あ-んア-ン一-龥ー])\s+((?=[あ-んア-ン一-龥ー]))',
    r'\1\2', txt)

#複数枚写真を入力する（繰り返し）

input_continue = input("続けて画像を読み込ませますか？　(y/n)")

while input_continue == "y" :
        
        #画像ファイルの場所・ファイル名を指定できるようにする
        input_file = input("ファイルのパスを入力してください。")

        #日本語で読み込み
        txtex = tool.image_to_string(
            Image.open(input_file),
            lang="jpn",
            builder=pyocr.builders.TextBuilder(tesseract_layout=3))

        #正規表現操作

        txtex = re.sub('([あ-んア-ン一-龥ー])\s+((?=[あ-んア-ン一-龥ー]))',
            r'\1\2', txtex)
        
        txt = txt + txtex
        
        input_continue = input("続けて画像を読み込ませますか？　(y/n)")
else :
    f = open('%s.txt.'%input_name, 'a')
    f.write('%s'%txt)
    f.close()
    

#検索部分    
import os

#拡張子なしのファイル名 os.path.splitext()
#拡張子ありのファイル名 os.path.basename()

input_dic = input("検索を開始しますか？(y/n)")

#タイトルをリスト化
title_list = list()
#ファイルの内容（文章）をリスト化
contents_list = list()

while input_dic == "y" :
    
    input_readfile = input("ファイルのパスを入力してください")
    
    #ファイルの内容読み込み
    
    readfile = open(r'%s'%input_readfile, 'r')
    data = readfile.read()
    readfile.close()
    
    #拡張子ありのファイル名取得
    title = os.path.basename(r'%s.txt'%input_readfile)
    #タイトルのリストの末尾に新しい要素を追加
    title_list.append(title)
    #ファイルの内容（文章）のリストの末尾に新しい要素を追加
    contents_list.append(data)
    
    input_dic = input("続けてファイルを読み込みますか？(y/n)")
    
    
else :
    #辞書作成
    dic = {title_list[i]: contents_list[i] for i in range(len(contents_list))}
   
#検索　
word = input("調べたい語句を入力してください")
 
for key, value in dic.items():
    if word in value:
        print (key)

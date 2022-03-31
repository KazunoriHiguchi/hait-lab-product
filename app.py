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

#画像ファイルの場所・ファイル名を指定できるようにする
input_file = input("ファイルのパスを入力してください。")

#日本語で読み込み
txt = tool.image_to_string(
    Image.open(input_file),
    lang="jpn",
    builder=pyocr.builders.TextBuilder(tesseract_layout=3))

#正規表現操作

txt = re.sub('([あ-んア-ン一-龥ー])\s+((?=[あ-んア-ン一-龥ー]))',
    r'\1\2', txt)

print( txt )

input_name = input("ファイルの名前を入力してください。")

f = open('%s.txt.'%input_name, 'a')
f.write('%s'%txt)
f.close()

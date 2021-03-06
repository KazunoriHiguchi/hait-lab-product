from flask import Flask, render_template, request, session
from wtforms import Form, FloatField, SubmitField, validators, ValidationError
import numpy as np
import joblib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import pyocr
import sys
from datetime import timedelta  # 時間情報を用いるため

# 検索タブの方の実装は未着手

# グローバルな変数の定義
dic = {}
count = 0

app = Flask(__name__)

# app.secret_key = 'user'
# app.permanent_session_lifetime = timedelta(
#    minutes=5)  # -> 5分 #(days=5) -> 5日保存

@app.route('/', methods=['GET', 'POST'])

def predicts():
    
    # グローバル変数を明記
    global dic
    global count
    
    # 最初にURLを開く際には、画像ファイルが選択されてないので文字認識の動作を飛ばす
    if count != 0:
        # まず入力された画像ファイルをカレントディレクトリに保存する
        # 保存時のファイル名は、入力されたファイルの名称が引き継がれるようにしたいが、やり方がわからない
        print(request.form.getlist('name')[0])
        print(request.files['img_file'])
        file = request.files['img_file']
        filename = request.form.getlist('name')[0]
        file.save(filename)

		# 保存した画像ファイルから文字を読み取り、ターミナルに出力する
        tools = pyocr.get_available_tools()
        tool = tools[0]
        # filename = 'img_file'
        txt = tool.image_to_string(
            Image.open(filename),
            lang='jpn',
            builder=pyocr.builders.TextBuilder()
        )
        txt = txt.replace(' ', '')
        txt = txt.replace('\n\n', '\n')
        # ターミナルに文字認識の結果を出力
        print('txt', txt)
        # このあと、それぞれの行をdicに格納していくコードを書く
        # session.permanent = True
        # session[filename] = txt
        dic[filename] = txt

    count += 1
    
    return render_template('index.html', answer="")

    # if request.method == 'POST':
    #     return render_template('index.html')
 
    # else:
    #     return render_template('index.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    # print(session['img_file'])
    print(request.form.getlist('search')[0])
    target = request.form.getlist('search')[0]
    answer = 'Not Found'
    # for key, value in session.items():
    #     print(key, value)
    #     if target in value:
    #         print(key)
    #         #　answer = key
            
    for key, value in dic.items():
        # print(key, value)
        if target in value:
            print('key', key)
            answer = key

    return render_template('index.html', answer=answer)
    

# main関数
if __name__ == "__main__":
    app.run()

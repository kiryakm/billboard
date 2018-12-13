from flask import Flask, render_template, request
from ftplib import FTP
import base64
import re
import os
import subprocess

from loader import *



app = Flask(__name__)


@app.route('/upload', methods=['GET', 'POST'])  #загрузка картинки
def upload():
    #получаю картинку в base64 и название картинки из принятого json
    img = request.json['data']
    name = request.json['name']
    #num = request.json['num']
    img = re.sub('data:image/png;base64,', '', img) #убираю лишнее из строки картинки
    with open("img/" + name + ".png", "wb") as fh:  #декодирую из base64 и сохраняю в папку img
        fh.write(base64.b64decode(img))
    return render_template("index.html")

# @app.route('/send', methods=['GET', 'POST'])  #загрузка картинки
# def send():
#     print("sending")
#     subprocess.Popen([r"C:\Users\Yakimenko.K.A\source\repos\makeBinScript\makeBinScript\bin\Release\makeBinScript.exe"])
#     os.system('"C:/Users/Yakimenko.K.A/source/repos/makeBinScript/makeBinScript/bin/Release/makeBinScript.exe"')
#     Connect()
#     ClearScreen(15)
#     p = "C:/Users/Yakimenko.K.A/Documents/PyProjects/billboard/img/"
#     path = list()
#     for root, dirs, files in os.walk(p):
#         for filename in files:
#             path.append(p + filename)
#     print(path[0])
#     makeData(path[0], 0, 0, 0, 2, 0, 0, False, True)
#     print("send")

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)

